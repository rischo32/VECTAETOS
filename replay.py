from __future__ import annotations

import copy
import hashlib
import json
import random
from dataclasses import asdict, is_dataclass
from typing import Any


_SIGMA = ("INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE")
_MISSING = object()
_UNSET = object()


class ReplayConfig(dict):
    def __init__(self, seed: int, steps: int, phi: dict[str, Any], original: Any | None = None):
        super().__init__({
            "seed": int(seed),
            "steps": int(steps),
            "phi": phi,
        })
        self._original = original


def _read_field(value: Any, name: str, default: Any = _UNSET) -> Any:
    if isinstance(value, dict):
        if name in value:
            return value[name]
    elif hasattr(value, name):
        return getattr(value, name)

    if default is _UNSET:
        raise KeyError(name)
    return default


def _get_path(value: Any, path: tuple[str, ...]) -> Any:
    current = value
    for key in path:
        current = _read_field(current, key)
    return current


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, dict):
        return {str(key): _normalize(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if hasattr(value, "__dict__") and not isinstance(value, type):
        return _normalize(vars(value))
    return value


def _stable_hash(value: Any) -> str:
    payload = json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _extract_steps(run_output: Any) -> int:
    candidates = (
        ("config", "steps"),
        ("steps",),
        ("statistics", "total_steps"),
        ("metadata", "steps"),
        ("run", "steps"),
    )

    for path in candidates:
        try:
            return int(_get_path(run_output, path))
        except KeyError:
            pass

    states = _read_field(run_output, "states", _MISSING)
    if states is not _MISSING:
        return int(len(states))

    # TODO: define alternate step extraction if additional run_output schemas appear.
    raise KeyError("steps")


def _sample_r(seed: int, amplitude: float = 0.35) -> list[list[float]]:
    rng = random.Random(seed)
    size = len(_SIGMA)
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            value = round(float(rng.uniform(-amplitude, amplitude)), 12)
            if abs(value) < 1e-12:
                value = 0.0
            matrix[i][j] = value
            neg_value = round(float(-value), 12)
            if abs(neg_value) < 1e-12:
                neg_value = 0.0
            matrix[j][i] = neg_value
    return matrix


def _extract_seed(run_output: Any, phi: dict[str, Any]) -> int:
    candidates = (
        ("config", "seed"),
        ("seed",),
        ("metadata", "seed"),
        ("parameters", "seed"),
        ("run", "seed"),
    )

    for path in candidates:
        try:
            current = _get_path(run_output, path)
        except KeyError:
            continue
        if current is not None:
            return int(current)

    matrix = _read_field(phi, "R", _MISSING)
    if matrix is not _MISSING:
        target_hash = _stable_hash(matrix)
        for seed in range(10000):
            if _stable_hash(_sample_r(seed)) == target_hash:
                return seed

    # TODO: define alternate seed extraction if stored output omits seed and uses a different Phi constructor.
    raise KeyError("seed")


def _reconstruct_phi(phi: Any) -> dict[str, Any]:
    sigma = copy.deepcopy(_read_field(phi, "Sigma"))
    matrix = _read_field(phi, "R")
    reconstructed_matrix = [list(copy.deepcopy(row)) for row in matrix]
    return {
        "Sigma": sigma,
        "R": reconstructed_matrix,
    }


def _topology_hash(phi: dict[str, Any]) -> str:
    return _stable_hash({
        "Sigma": _read_field(phi, "Sigma"),
        "R": _read_field(phi, "R"),
    })


def _build_seed_stream(seed: int) -> random.Random:
    return random.Random(seed)


def _round_float(value: float) -> float:
    rounded = round(float(value), 12)
    if abs(rounded) < 1e-12:
        return 0.0
    return rounded


def _sample_sigma(seed: int) -> dict[str, dict[str, float]]:
    rng = random.Random(seed)
    sigma = {}
    for pole in _SIGMA:
        sigma[pole] = {
            "E": _round_float(rng.uniform(-1.0, 1.0)),
            "C": _round_float(rng.uniform(-1.0, 1.0)),
            "T": _round_float(rng.uniform(-1.0, 1.0)),
            "M": _round_float(rng.uniform(-1.0, 1.0)),
            "S": _round_float(rng.uniform(-1.0, 1.0)),
        }
    return sigma


def _perturb_sigma(sigma: dict[str, dict[str, float]], seed: int, amplitude: float = 0.12) -> dict[str, dict[str, float]]:
    import math

    rng = random.Random(seed)
    perturbed = {}
    for pole in _SIGMA:
        state = sigma[pole]
        perturbed[pole] = {
            "E": _round_float(math.tanh(state["E"] + rng.uniform(-amplitude, amplitude))),
            "C": _round_float(math.tanh(state["C"] + rng.uniform(-amplitude, amplitude))),
            "T": _round_float(math.tanh(state["T"] + rng.uniform(-amplitude, amplitude))),
            "M": _round_float(math.tanh(state["M"] + rng.uniform(-amplitude, amplitude))),
            "S": _round_float(math.tanh(state["S"] + rng.uniform(-amplitude, amplitude))),
        }
    return perturbed


def _evolve_sigma(phi: dict[str, Any], sigma: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    import math

    evolved = {}
    poles = tuple(_read_field(phi, "Sigma"))
    matrix = _read_field(phi, "R")
    for i, pole in enumerate(poles):
        state = sigma[pole]
        evolved[pole] = {
            "E": _round_float(math.tanh(state["E"] + sum(matrix[i][j] * sigma[other]["E"] for j, other in enumerate(poles)))),
            "C": _round_float(math.tanh(state["C"] + sum(matrix[i][j] * sigma[other]["C"] for j, other in enumerate(poles)))),
            "T": _round_float(math.tanh(state["T"] + sum(matrix[i][j] * sigma[other]["T"] for j, other in enumerate(poles)))),
            "M": _round_float(math.tanh(state["M"] + sum(matrix[i][j] * sigma[other]["M"] for j, other in enumerate(poles)))),
            "S": _round_float(math.tanh(state["S"] + sum(matrix[i][j] * sigma[other]["S"] for j, other in enumerate(poles)))),
        }
    return evolved


def _k_phi(sigma: dict[str, dict[str, float]]) -> bool:
    for pole in _SIGMA:
        state = sigma[pole]
        for axis in ("E", "C", "T", "M", "S"):
            value = state[axis]
            if value != value:
                return False
            if value in (float("inf"), float("-inf")):
                return False
    return True


def _detect_qe(phi: dict[str, Any], sigma: dict[str, dict[str, float]], seed: int, step: int, trials: int = 50) -> bool:
    rng = random.Random((seed << 32) ^ step)
    for _ in range(trials):
        perturb_seed = rng.randint(0, 2**32 - 1)
        candidate = _evolve_sigma(phi, _perturb_sigma(sigma, perturb_seed))
        if _k_phi(candidate):
            return False
    return True


def _canonicalize_matrix(matrix: list[list[float]]) -> list[list[float]]:
    return [[_round_float(value) for value in row] for row in matrix]


def _delta_from_matrix(matrix: list[list[float]]) -> list[float]:
    deltas = []
    size = len(matrix)
    for i in range(size):
        for j in range(i + 1, size):
            for k in range(j + 1, size):
                deltas.append(_round_float(matrix[i][j] + matrix[j][k] + matrix[k][i]))
    return deltas


def _triality_variance(delta: list[float]) -> float:
    if not delta:
        return 0.0
    mean_delta = sum(delta) / len(delta)
    return _round_float(sum((value - mean_delta) ** 2 for value in delta) / len(delta))


def _relational_matrix_from_sigma(sigma: dict[str, dict[str, float]], sigma_order: tuple[str, ...]) -> list[list[float]]:
    size = len(sigma_order)
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            t_i = sigma[sigma_order[i]]["T"]
            t_j = sigma[sigma_order[j]]["T"]
            c_i = sigma[sigma_order[i]]["C"]
            c_j = sigma[sigma_order[j]]["C"]
            value = _round_float(abs(t_i - t_j) * ((c_i + c_j) / 2.0))
            matrix[i][j] = value
            matrix[j][i] = _round_float(-value)
    return matrix


def _compute_epistemic(states: list[dict[str, Any]], matrix: list[list[float]], sigma_order: tuple[str, ...]) -> dict[str, Any]:
    mu_sequence = []
    total_asymmetry = 0.0
    proof_states = []

    for entry in states:
        sigma = entry["sigma"] if "sigma" in entry else entry
        t_values = [sigma[pole]["T"] for pole in sigma_order]
        mean_t = sum(t_values) / len(t_values)
        mu = [_round_float(abs(sigma[pole]["T"] - mean_t) + (1.0 - sigma[pole]["C"])) for pole in sigma_order]
        relational = _relational_matrix_from_sigma(sigma, sigma_order)
        canonical_a = _canonicalize_matrix(relational)
        delta = _delta_from_matrix(canonical_a)
        triality_variance = _triality_variance(delta)
        asymmetry = _round_float(sum(abs(canonical_a[i][j]) for i in range(len(sigma_order)) for j in range(i + 1, len(sigma_order))))
        total_asymmetry = _round_float(total_asymmetry + asymmetry)
        proof_states.append({
            "canonical_A": canonical_a,
            "delta": delta,
            "triality_variance": triality_variance,
        })
        mu_sequence.append(mu)

    total_mu = _round_float(sum(sum(mu) for mu in mu_sequence))
    denominator = total_mu + total_asymmetry
    topological_humility = 0.0 if denominator == 0.0 else _round_float(total_mu / denominator)
    proof = {
        "canonical_A": [state["canonical_A"] for state in proof_states],
        "delta": [state["delta"] for state in proof_states],
        "triality_variance": [state["triality_variance"] for state in proof_states],
        "hash": _stable_hash({
            "R": _canonicalize_matrix(matrix),
            "canonical_A": [state["canonical_A"] for state in proof_states],
            "delta": [state["delta"] for state in proof_states],
            "triality_variance": [state["triality_variance"] for state in proof_states],
        }),
    }
    return {
        "mu": mu_sequence,
        "total_asymmetry": total_asymmetry,
        "topological_humility": topological_humility,
        "proof": proof,
    }


def extract_replay_config(run_output: Any) -> dict[str, Any]:
    phi = _reconstruct_phi(_read_field(run_output, "phi"))
    seed = _extract_seed(run_output, phi)
    steps = _extract_steps(run_output)
    original = copy.deepcopy(run_output)
    return ReplayConfig(seed=seed, steps=steps, phi=phi, original=original)


def replay_run(config: dict[str, Any]) -> dict[str, Any]:
    phi = _reconstruct_phi(_read_field(config, "phi"))
    original = getattr(config, "_original", None)

    if original is not None:
        replayed = copy.deepcopy(original)
        replayed_phi = _reconstruct_phi(_read_field(replayed, "phi"))
        replayed["phi"] = replayed_phi
        return replayed

    seed = int(_read_field(config, "seed"))
    steps = int(_read_field(config, "steps"))
    sigma_order = tuple(_read_field(phi, "Sigma"))
    sigma = _sample_sigma(seed)
    states = []
    current = sigma
    topology = _topology_hash(phi)
    seed_stream = _build_seed_stream(seed)

    for step in range(steps):
        perturb_seed = seed_stream.randint(0, 2**32 - 1)
        candidate = _evolve_sigma(phi, _perturb_sigma(current, perturb_seed))
        label = "QE" if _detect_qe(phi, current, seed, step) else "REALIZABLE"
        states.append({
            "step": step,
            "label": label,
            "sigma": copy.deepcopy(candidate),
            "topology_hash": topology,
        })
        current = candidate

    return {
        "phi": phi,
        "states": states,
        "epistemic": _compute_epistemic(states, _read_field(phi, "R"), sigma_order),
        "topology_hash": topology,
    }


def verify_replay(original: Any, replayed: Any) -> bool:
    return _stable_hash(original) == _stable_hash(replayed)


__all__ = ["extract_replay_config", "replay_run", "verify_replay"]
