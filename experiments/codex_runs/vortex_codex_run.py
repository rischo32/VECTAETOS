from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import math
import random
from typing import Any

NODES = ("INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE")
SIGMA_COMPONENTS = ("E", "C", "T", "M", "S")


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int | None = 42
    depth: int = 4
    perturbations: int = 4
    relation_amplitude: float = 0.35
    perturbation_amplitude: float = 0.12
    artifact_root: str = "artifacts"


@dataclass(frozen=True)
class PoleState:
    E: float
    C: float
    T: float
    M: float
    S: float


@dataclass(frozen=True)
class Phi:
    sigma: tuple[str, ...]
    R: list[list[float]]


@dataclass(frozen=True)
class TrajectoryState:
    step: int
    path: str
    label: str
    K: bool
    topology_hash: str
    coherence: float
    sigma: dict[str, dict[str, float]]


@dataclass(frozen=True)
class QEEvent:
    step: int
    path: str
    topology_hash: str
    coherence: float


@dataclass(frozen=True)
class ExperimentArtifacts:
    config: dict[str, Any]
    phi: dict[str, Any]
    trajectories: list[list[dict[str, Any]]]
    qe_events: list[dict[str, Any]]
    topology_hash: str
    summary: dict[str, Any]


class RMK:
    sigma = NODES
    components = SIGMA_COMPONENTS

    @staticmethod
    def sample_R(seed: int | None, amplitude: float) -> list[list[float]]:
        rng = random.Random(seed)
        size = len(RMK.sigma)
        matrix = [[0.0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(i + 1, size):
                value = _round_float(rng.uniform(-amplitude, amplitude))
                matrix[i][j] = value
                matrix[j][i] = _round_float(-value)
        return matrix

    @staticmethod
    def delta_structure(matrix: list[list[float]]) -> list[dict[str, Any]]:
        deltas = []
        for i, j, k in combinations(range(len(RMK.sigma)), 3):
            delta_value = _round_float(matrix[i][j] + matrix[j][k] + matrix[k][i])
            deltas.append(
                {
                    "triad": [RMK.sigma[i], RMK.sigma[j], RMK.sigma[k]],
                    "value": delta_value,
                }
            )
        return deltas

    @staticmethod
    def coherence(matrix: list[list[float]]) -> float:
        deltas = RMK.delta_structure(matrix)
        if not deltas:
            return 1.0
        total = sum(abs(entry["value"]) for entry in deltas)
        return _round_float(1.0 - (total / len(deltas)))


def _round_float(value: float) -> float:
    rounded = round(float(value), 12)
    if abs(rounded) < 1e-12:
        return 0.0
    return rounded


def _hash_payload(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(serialized.encode("utf-8")).hexdigest()


def topology_hash(matrix: list[list[float]]) -> str:
    return _hash_payload({"sigma": NODES, "R": matrix})


def _sample_seed(seed: int | None) -> int:
    if seed is None:
        return random.SystemRandom().randrange(0, 2**63)
    return seed


def sample_sigma(seed: int | None) -> dict[str, PoleState]:
    rng = random.Random(seed)
    sigma = {}
    for node in NODES:
        sigma[node] = PoleState(
            E=_round_float(rng.uniform(-1.0, 1.0)),
            C=_round_float(rng.uniform(-1.0, 1.0)),
            T=_round_float(rng.uniform(-1.0, 1.0)),
            M=_round_float(rng.uniform(-1.0, 1.0)),
            S=_round_float(rng.uniform(-1.0, 1.0)),
        )
    return sigma


def construct_phi(cfg: ExperimentConfig) -> tuple[Phi, dict[str, PoleState], int]:
    run_seed = _sample_seed(cfg.seed)
    matrix = RMK.sample_R(run_seed, cfg.relation_amplitude)
    sigma = sample_sigma(run_seed ^ 0xA5A5A5A5)
    return Phi(sigma=NODES, R=matrix), sigma, run_seed


def perturb_sigma(sigma: dict[str, PoleState], seed: int, amplitude: float) -> dict[str, PoleState]:
    rng = random.Random(seed)
    perturbed = {}
    for node in NODES:
        state = sigma[node]
        perturbed[node] = PoleState(
            E=_round_float(math.tanh(state.E + rng.uniform(-amplitude, amplitude))),
            C=_round_float(math.tanh(state.C + rng.uniform(-amplitude, amplitude))),
            T=_round_float(math.tanh(state.T + rng.uniform(-amplitude, amplitude))),
            M=_round_float(math.tanh(state.M + rng.uniform(-amplitude, amplitude))),
            S=_round_float(math.tanh(state.S + rng.uniform(-amplitude, amplitude))),
        )
    return perturbed


def evolve_sigma(phi: Phi, sigma: dict[str, PoleState]) -> dict[str, PoleState]:
    evolved = {}
    for i, node in enumerate(phi.sigma):
        state = sigma[node]
        e = state.E + sum(phi.R[i][j] * sigma[other].E for j, other in enumerate(phi.sigma))
        c = state.C + sum(phi.R[i][j] * sigma[other].C for j, other in enumerate(phi.sigma))
        t = state.T + sum(phi.R[i][j] * sigma[other].T for j, other in enumerate(phi.sigma))
        m = state.M + sum(phi.R[i][j] * sigma[other].M for j, other in enumerate(phi.sigma))
        s = state.S + sum(phi.R[i][j] * sigma[other].S for j, other in enumerate(phi.sigma))
        evolved[node] = PoleState(
            E=_round_float(math.tanh(e)),
            C=_round_float(math.tanh(c)),
            T=_round_float(math.tanh(t)),
            M=_round_float(math.tanh(m)),
            S=_round_float(math.tanh(s)),
        )
    return evolved


def _sigma_payload(sigma: dict[str, PoleState]) -> dict[str, dict[str, float]]:
    return {node: asdict(sigma[node]) for node in NODES}


def K_phi(sigma: dict[str, PoleState]) -> bool:
    for node in NODES:
        state = sigma[node]
        for component in SIGMA_COMPONENTS:
            value = getattr(state, component)
            if not math.isfinite(value):
                return False
    return True


def _is_transition(source: dict[str, PoleState], candidate: dict[str, PoleState]) -> bool:
    return _sigma_payload(source) != _sigma_payload(candidate)


def _branch_seed(run_seed: int, path: str, step: int, perturbation_index: int) -> int:
    digest = sha256(f"{run_seed}|{path}|{step}|{perturbation_index}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def _state_record(
    sigma: dict[str, PoleState],
    step: int,
    path: str,
    label: str,
    K: bool,
    topology: str,
    coherence: float,
) -> TrajectoryState:
    return TrajectoryState(
        step=step,
        path=path,
        label=label,
        K=K,
        topology_hash=topology,
        coherence=coherence,
        sigma=_sigma_payload(sigma),
    )


def _generate_trajectories(
    phi: Phi,
    sigma: dict[str, PoleState],
    cfg: ExperimentConfig,
    step: int,
    path: str,
    run_seed: int,
    topology: str,
    coherence: float,
) -> tuple[list[list[TrajectoryState]], list[QEEvent]]:
    current = _state_record(
        sigma=sigma,
        step=step,
        path=path,
        label="REALIZABLE",
        K=True,
        topology=topology,
        coherence=coherence,
    )
    if step >= cfg.depth:
        return [[current]], []
    realizable_children: list[tuple[int, dict[str, PoleState]]] = []
    for perturbation_index in range(cfg.perturbations):
        branch_seed = _branch_seed(run_seed, path, step, perturbation_index)
        perturbed_sigma = perturb_sigma(sigma, branch_seed, cfg.perturbation_amplitude)
        candidate_sigma = evolve_sigma(phi, perturbed_sigma)
        if K_phi(candidate_sigma) and _is_transition(sigma, candidate_sigma):
            realizable_children.append((perturbation_index, candidate_sigma))
    if not realizable_children:
        qe_path = f"{path}.qe"
        qe_state = _state_record(
            sigma=sigma,
            step=step + 1,
            path=qe_path,
            label="QE",
            K=False,
            topology=topology,
            coherence=coherence,
        )
        qe_event = QEEvent(
            step=step + 1,
            path=qe_path,
            topology_hash=topology,
            coherence=coherence,
        )
        return [[current, qe_state]], [qe_event]
    trajectories: list[list[TrajectoryState]] = []
    qe_events: list[QEEvent] = []
    for perturbation_index, candidate_sigma in realizable_children:
        child_path = f"{path}.{perturbation_index}"
        child_trajectories, child_qe_events = _generate_trajectories(
            phi=phi,
            sigma=candidate_sigma,
            cfg=cfg,
            step=step + 1,
            path=child_path,
            run_seed=run_seed,
            topology=topology,
            coherence=coherence,
        )
        for child_trajectory in child_trajectories:
            trajectories.append([current, *child_trajectory])
        qe_events.extend(child_qe_events)
    return trajectories, qe_events


def summarize_artifacts(
    trajectories: list[list[TrajectoryState]],
    qe_events: list[QEEvent],
    cfg: ExperimentConfig,
    run_seed: int,
    topology: str,
    coherence: float,
) -> dict[str, Any]:
    label_counts = {"REALIZABLE": 0, "QE": 0}
    for trajectory in trajectories:
        for state in trajectory:
            label_counts[state.label] = label_counts.get(state.label, 0) + 1
    return {
        "seed": run_seed,
        "depth": cfg.depth,
        "perturbations": cfg.perturbations,
        "topology_hash": topology,
        "coherence": coherence,
        "trajectory_count": len(trajectories),
        "qe_event_count": len(qe_events),
        "label_counts": label_counts,
    }


def run_experiment(cfg: ExperimentConfig) -> ExperimentArtifacts:
    phi, sigma, run_seed = construct_phi(cfg)
    topology = topology_hash(phi.R)
    coherence = RMK.coherence(phi.R)
    trajectories, qe_events = _generate_trajectories(
        phi=phi,
        sigma=sigma,
        cfg=cfg,
        step=0,
        path="root",
        run_seed=run_seed,
        topology=topology,
        coherence=coherence,
    )
    summary = summarize_artifacts(trajectories, qe_events, cfg, run_seed, topology, coherence)
    return ExperimentArtifacts(
        config={**asdict(cfg), "seed": run_seed},
        phi={
            "sigma": phi.sigma,
            "R": phi.R,
            "delta": RMK.delta_structure(phi.R),
            "coherence": coherence,
        },
        trajectories=[[asdict(state) for state in trajectory] for trajectory in trajectories],
        qe_events=[asdict(event) for event in qe_events],
        topology_hash=topology,
        summary=summary,
    )


def save_artifacts(artifacts: ExperimentArtifacts, artifact_root: Path) -> None:
    artifact_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "config": artifacts.config,
        "topology_hash": artifacts.topology_hash,
        "phi": artifacts.phi,
        "summary": artifacts.summary,
    }
    (artifact_root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (artifact_root / "trajectories.json").write_text(json.dumps(artifacts.trajectories, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (artifact_root / "qe_events.json").write_text(json.dumps(artifacts.qe_events, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (artifact_root / "summary.json").write_text(json.dumps(artifacts.summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> ExperimentConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--perturbations", type=int, default=4)
    parser.add_argument("--relation-amplitude", type=float, default=0.35)
    parser.add_argument("--perturbation-amplitude", type=float, default=0.12)
    parser.add_argument("--artifact-root", type=str, default="artifacts")
    args = parser.parse_args()
    return ExperimentConfig(
        seed=args.seed,
        depth=args.depth,
        perturbations=args.perturbations,
        relation_amplitude=args.relation_amplitude,
        perturbation_amplitude=args.perturbation_amplitude,
        artifact_root=args.artifact_root,
    )


def main() -> None:
    cfg = parse_args()
    artifacts = run_experiment(cfg)
    artifact_root = Path(__file__).resolve().parent / cfg.artifact_root / f"seed_{artifacts.config['seed']}_d{cfg.depth}_p{cfg.perturbations}"
    save_artifacts(artifacts, artifact_root)
    print(json.dumps(artifacts.summary, sort_keys=True))


if __name__ == "__main__":
    main()
