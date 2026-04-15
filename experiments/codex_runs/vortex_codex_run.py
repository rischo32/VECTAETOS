from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math
import random
from typing import Any

NODES = ("INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE")


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 42
    depth: int = 4
    perturbations: int = 4
    relation_amplitude: float = 0.35
    perturbation_amplitude: float = 0.12
    artifact_root: str = "artifacts"
    validity_epsilon: float = 1e-9


@dataclass(frozen=True)
class StateRecord:
    step: int
    path: str
    label: str
    sigma: list[float]
    topology_hash: str
    relation_hash: str
    perturbation_index: int | None
    sampled_perturbations: list[dict[str, Any]]


@dataclass(frozen=True)
class ExperimentArtifacts:
    config: dict[str, Any]
    nodes: tuple[str, ...]
    relation_hash: str
    relation_matrix: list[list[float]]
    trajectories: list[list[dict[str, Any]]]
    summary: dict[str, Any]


def _round_float(value: float) -> float:
    rounded = round(float(value), 12)
    if abs(rounded) < 1e-12:
        return 0.0
    return rounded


def _canonical_sigma(values: list[float]) -> list[float]:
    return [_round_float(value) for value in values]


def _canonical_matrix(matrix: list[list[float]]) -> list[list[float]]:
    return [[_round_float(value) for value in row] for row in matrix]


def _hash_payload(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(serialized.encode("utf-8")).hexdigest()


def build_relation_matrix(seed: int, amplitude: float) -> list[list[float]]:
    rng = random.Random(seed)
    size = len(NODES)
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            value = rng.uniform(-amplitude, amplitude)
            matrix[i][j] = _round_float(value)
            matrix[j][i] = _round_float(-value)
    return matrix


def relation_hash(matrix: list[list[float]]) -> str:
    return _hash_payload({"nodes": NODES, "R": _canonical_matrix(matrix)})


def build_initial_sigma(seed: int) -> list[float]:
    rng = random.Random(seed ^ 0xA5A5A5A5)
    return _canonical_sigma([rng.uniform(-1.0, 1.0) for _ in NODES])


def _branch_seed(seed: int, path: str, step: int, perturbation_index: int) -> int:
    digest = sha256(f"{seed}|{path}|{step}|{perturbation_index}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def perturb_sigma(sigma: list[float], seed: int, amplitude: float) -> list[float]:
    rng = random.Random(seed)
    perturbed = []
    for value in sigma:
        delta = rng.uniform(-amplitude, amplitude)
        perturbed.append(math.tanh(value + delta))
    return _canonical_sigma(perturbed)


def evolve_sigma(matrix: list[list[float]], sigma: list[float]) -> list[float]:
    size = len(sigma)
    evolved = []
    for i in range(size):
        influence = 0.0
        for j in range(size):
            influence += matrix[i][j] * sigma[j]
        evolved.append(math.tanh(sigma[i] + influence))
    return _canonical_sigma(evolved)


def is_realizable(current: list[float], candidate: list[float], epsilon: float) -> bool:
    if len(current) != len(candidate):
        return False
    moved = False
    for source, target in zip(current, candidate):
        if not math.isfinite(target):
            return False
        if target < -1.0 - epsilon or target > 1.0 + epsilon:
            return False
        if abs(source - target) > epsilon:
            moved = True
    return moved


def topology_hash(matrix: list[list[float]], sigma: list[float]) -> str:
    return _hash_payload({"nodes": NODES, "R": _canonical_matrix(matrix), "sigma": _canonical_sigma(sigma)})


def _sample_transitions(
    matrix: list[list[float]],
    sigma: list[float],
    cfg: ExperimentConfig,
    path: str,
    step: int,
    matrix_hash: str,
) -> tuple[list[tuple[int, list[float]]], list[dict[str, Any]]]:
    realizable_children: list[tuple[int, list[float]]] = []
    sampled_perturbations: list[dict[str, Any]] = []
    for perturbation_index in range(cfg.perturbations):
        derived_seed = _branch_seed(cfg.seed, path, step, perturbation_index)
        perturbed_sigma = perturb_sigma(sigma, derived_seed, cfg.perturbation_amplitude)
        candidate_sigma = evolve_sigma(matrix, perturbed_sigma)
        realizable = is_realizable(sigma, candidate_sigma, cfg.validity_epsilon)
        sampled_perturbations.append(
            {
                "perturbation_index": perturbation_index,
                "seed": derived_seed,
                "perturbed_sigma": perturbed_sigma,
                "candidate_sigma": candidate_sigma,
                "label": "REALIZABLE" if realizable else "QE",
                "topology_hash": topology_hash(matrix, candidate_sigma),
                "relation_hash": matrix_hash,
            }
        )
        if realizable:
            realizable_children.append((perturbation_index, candidate_sigma))
    return realizable_children, sampled_perturbations


def _state_record(
    matrix: list[list[float]],
    sigma: list[float],
    step: int,
    path: str,
    label: str,
    matrix_hash: str,
    perturbation_index: int | None,
    sampled_perturbations: list[dict[str, Any]],
) -> StateRecord:
    return StateRecord(
        step=step,
        path=path,
        label=label,
        sigma=_canonical_sigma(sigma),
        topology_hash=topology_hash(matrix, sigma),
        relation_hash=matrix_hash,
        perturbation_index=perturbation_index,
        sampled_perturbations=sampled_perturbations,
    )


def _generate_trajectories(
    matrix: list[list[float]],
    sigma: list[float],
    cfg: ExperimentConfig,
    step: int,
    path: str,
    matrix_hash: str,
    perturbation_index: int | None,
) -> list[list[StateRecord]]:
    if step >= cfg.depth:
        terminal = _state_record(
            matrix=matrix,
            sigma=sigma,
            step=step,
            path=path,
            label="REALIZABLE",
            matrix_hash=matrix_hash,
            perturbation_index=perturbation_index,
            sampled_perturbations=[],
        )
        return [[terminal]]

    children, sampled_perturbations = _sample_transitions(
        matrix=matrix,
        sigma=sigma,
        cfg=cfg,
        path=path,
        step=step,
        matrix_hash=matrix_hash,
    )

    current = _state_record(
        matrix=matrix,
        sigma=sigma,
        step=step,
        path=path,
        label="REALIZABLE",
        matrix_hash=matrix_hash,
        perturbation_index=perturbation_index,
        sampled_perturbations=sampled_perturbations,
    )

    if not children:
        qe_state = _state_record(
            matrix=matrix,
            sigma=sigma,
            step=step + 1,
            path=f"{path}.qe",
            label="QE",
            matrix_hash=matrix_hash,
            perturbation_index=None,
            sampled_perturbations=[],
        )
        return [[current, qe_state]]

    trajectories: list[list[StateRecord]] = []
    for child_index, child_sigma in children:
        child_path = f"{path}.{child_index}"
        for child_trajectory in _generate_trajectories(
            matrix=matrix,
            sigma=child_sigma,
            cfg=cfg,
            step=step + 1,
            path=child_path,
            matrix_hash=matrix_hash,
            perturbation_index=child_index,
        ):
            trajectories.append([current, *child_trajectory])
    return trajectories


def summarize_artifacts(trajectories: list[list[StateRecord]], matrix_hash: str, cfg: ExperimentConfig) -> dict[str, Any]:
    label_counts = {"REALIZABLE": 0, "QE": 0}
    unique_topologies: set[str] = set()
    leaves = []
    for trajectory in trajectories:
        for state in trajectory:
            label_counts[state.label] = label_counts.get(state.label, 0) + 1
            unique_topologies.add(state.topology_hash)
        leaves.append(trajectory[-1].label)
    leaf_counts = {"REALIZABLE": 0, "QE": 0}
    for label in leaves:
        leaf_counts[label] = leaf_counts.get(label, 0) + 1
    return {
        "seed": cfg.seed,
        "depth": cfg.depth,
        "perturbations": cfg.perturbations,
        "relation_hash": matrix_hash,
        "trajectory_count": len(trajectories),
        "state_count": sum(len(trajectory) for trajectory in trajectories),
        "label_counts": label_counts,
        "leaf_counts": leaf_counts,
        "unique_topology_count": len(unique_topologies),
    }


def run_experiment(cfg: ExperimentConfig) -> ExperimentArtifacts:
    matrix = build_relation_matrix(cfg.seed, cfg.relation_amplitude)
    matrix_hash = relation_hash(matrix)
    initial_sigma = build_initial_sigma(cfg.seed)
    trajectories = _generate_trajectories(
        matrix=matrix,
        sigma=initial_sigma,
        cfg=cfg,
        step=0,
        path="root",
        matrix_hash=matrix_hash,
        perturbation_index=None,
    )
    trajectory_payload = [[asdict(state) for state in trajectory] for trajectory in trajectories]
    summary = summarize_artifacts(trajectories, matrix_hash, cfg)
    return ExperimentArtifacts(
        config=asdict(cfg),
        nodes=NODES,
        relation_hash=matrix_hash,
        relation_matrix=_canonical_matrix(matrix),
        trajectories=trajectory_payload,
        summary=summary,
    )


def save_artifacts(artifacts: ExperimentArtifacts, artifact_root: Path) -> None:
    artifact_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "config": artifacts.config,
        "nodes": artifacts.nodes,
        "relation_hash": artifacts.relation_hash,
        "relation_matrix": artifacts.relation_matrix,
        "summary": artifacts.summary,
    }
    (artifact_root / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (artifact_root / "summary.json").write_text(json.dumps(artifacts.summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (artifact_root / "trajectories.json").write_text(json.dumps(artifacts.trajectories, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> ExperimentConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--perturbations", type=int, default=4)
    parser.add_argument("--relation-amplitude", type=float, default=0.35)
    parser.add_argument("--perturbation-amplitude", type=float, default=0.12)
    parser.add_argument("--artifact-root", type=str, default="artifacts")
    parser.add_argument("--validity-epsilon", type=float, default=1e-9)
    args = parser.parse_args()
    return ExperimentConfig(
        seed=args.seed,
        depth=args.depth,
        perturbations=args.perturbations,
        relation_amplitude=args.relation_amplitude,
        perturbation_amplitude=args.perturbation_amplitude,
        artifact_root=args.artifact_root,
        validity_epsilon=args.validity_epsilon,
    )


def main() -> None:
    cfg = parse_args()
    artifacts = run_experiment(cfg)
    artifact_root = Path(__file__).resolve().parent / cfg.artifact_root / f"seed_{cfg.seed}_d{cfg.depth}_p{cfg.perturbations}"
    save_artifacts(artifacts, artifact_root)
    print(json.dumps(artifacts.summary, sort_keys=True))


if __name__ == "__main__":
    main()
