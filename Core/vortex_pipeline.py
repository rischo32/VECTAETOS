from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
import random
from typing import Any

SIGMA = ("INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE")


@dataclass(frozen=True)
class PoleState:
    E: float
    C: float
    T: float
    M: float
    S: float


@dataclass(frozen=True)
class Phi:
    Sigma: tuple[str, ...]
    R: list[list[float]]


class RMK:
    Sigma = SIGMA

    @staticmethod
    def sample_R(seed: int | None = 42, amplitude: float = 0.35) -> list[list[float]]:
        rng = random.Random(seed)
        size = len(RMK.Sigma)
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
        size = len(RMK.Sigma)
        for i in range(size):
            for j in range(i + 1, size):
                for k in range(j + 1, size):
                    deltas.append(
                        {
                            "triad": [RMK.Sigma[i], RMK.Sigma[j], RMK.Sigma[k]],
                            "value": _round_float(matrix[i][j] + matrix[j][k] + matrix[k][i]),
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
    return _hash_payload({"Sigma": SIGMA, "R": matrix})


def sample_sigma(seed: int | None = 42) -> dict[str, PoleState]:
    rng = random.Random(seed)
    sigma = {}
    for pole in SIGMA:
        sigma[pole] = PoleState(
            E=_round_float(rng.uniform(-1.0, 1.0)),
            C=_round_float(rng.uniform(-1.0, 1.0)),
            T=_round_float(rng.uniform(-1.0, 1.0)),
            M=_round_float(rng.uniform(-1.0, 1.0)),
            S=_round_float(rng.uniform(-1.0, 1.0)),
        )
    return sigma


def construct_phi(seed: int | None = 42, amplitude: float = 0.35) -> Phi:
    return Phi(Sigma=SIGMA, R=RMK.sample_R(seed=seed, amplitude=amplitude))


def perturb_sigma(sigma: dict[str, PoleState], seed: int, amplitude: float = 0.12) -> dict[str, PoleState]:
    rng = random.Random(seed)
    perturbed = {}
    for pole in SIGMA:
        state = sigma[pole]
        perturbed[pole] = PoleState(
            E=_round_float(math.tanh(state.E + rng.uniform(-amplitude, amplitude))),
            C=_round_float(math.tanh(state.C + rng.uniform(-amplitude, amplitude))),
            T=_round_float(math.tanh(state.T + rng.uniform(-amplitude, amplitude))),
            M=_round_float(math.tanh(state.M + rng.uniform(-amplitude, amplitude))),
            S=_round_float(math.tanh(state.S + rng.uniform(-amplitude, amplitude))),
        )
    return perturbed


def evolve_sigma(phi: Phi, sigma: dict[str, PoleState]) -> dict[str, PoleState]:
    evolved = {}
    for i, pole in enumerate(phi.Sigma):
        state = sigma[pole]
        evolved[pole] = PoleState(
            E=_round_float(math.tanh(state.E + sum(phi.R[i][j] * sigma[other].E for j, other in enumerate(phi.Sigma)))),
            C=_round_float(math.tanh(state.C + sum(phi.R[i][j] * sigma[other].C for j, other in enumerate(phi.Sigma)))),
            T=_round_float(math.tanh(state.T + sum(phi.R[i][j] * sigma[other].T for j, other in enumerate(phi.Sigma)))),
            M=_round_float(math.tanh(state.M + sum(phi.R[i][j] * sigma[other].M for j, other in enumerate(phi.Sigma)))),
            S=_round_float(math.tanh(state.S + sum(phi.R[i][j] * sigma[other].S for j, other in enumerate(phi.Sigma)))),
        )
    return evolved


def _sigma_payload(sigma: dict[str, PoleState]) -> dict[str, dict[str, float]]:
    return {pole: asdict(sigma[pole]) for pole in SIGMA}


def K_phi(sigma: dict[str, PoleState]) -> bool:
    for pole in SIGMA:
        state = sigma[pole]
        if not math.isfinite(state.E):
            return False
        if not math.isfinite(state.C):
            return False
        if not math.isfinite(state.T):
            return False
        if not math.isfinite(state.M):
            return False
        if not math.isfinite(state.S):
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


def _relational_matrix_from_sigma(sigma: dict[str, dict[str, float]]) -> list[list[float]]:
    size = len(SIGMA)
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            t_i = sigma[SIGMA[i]]["T"]
            t_j = sigma[SIGMA[j]]["T"]
            c_i = sigma[SIGMA[i]]["C"]
            c_j = sigma[SIGMA[j]]["C"]
            value = _round_float(abs(t_i - t_j) * ((c_i + c_j) / 2.0))
            matrix[i][j] = value
            matrix[j][i] = _round_float(-value)
    return matrix


def compute_epistemic(sigma_sequence: list[dict[str, Any]], R: list[list[float]]) -> dict[str, Any]:
    mu_sequence = []
    total_asymmetry = 0.0
    proof_states = []

    for entry in sigma_sequence:
        sigma = entry["sigma"] if "sigma" in entry else entry
        t_values = [sigma[pole]["T"] for pole in SIGMA]
        mean_t = sum(t_values) / len(t_values)
        mu = [_round_float(abs(sigma[pole]["T"] - mean_t) + (1.0 - sigma[pole]["C"])) for pole in SIGMA]

        matrix = _relational_matrix_from_sigma(sigma)
        canonical_A = _canonicalize_matrix(matrix)
        delta = _delta_from_matrix(canonical_A)
        triality_variance = _triality_variance(delta)
        asymmetry = _round_float(
            sum(abs(canonical_A[i][j]) for i in range(len(SIGMA)) for j in range(i + 1, len(SIGMA)))
        )
        total_asymmetry = _round_float(total_asymmetry + asymmetry)

        proof_states.append(
            {
                "canonical_A": canonical_A,
                "delta": delta,
                "triality_variance": triality_variance,
            }
        )
        mu_sequence.append(mu)

    total_mu = _round_float(sum(sum(mu) for mu in mu_sequence))
    denominator = total_mu + total_asymmetry
    topological_humility = 0.0 if denominator == 0.0 else _round_float(total_mu / denominator)

    proof = {
        "canonical_A": [state["canonical_A"] for state in proof_states],
        "delta": [state["delta"] for state in proof_states],
        "triality_variance": [state["triality_variance"] for state in proof_states],
        "hash": _hash_payload(
            {
                "R": _canonicalize_matrix(R),
                "canonical_A": [state["canonical_A"] for state in proof_states],
                "delta": [state["delta"] for state in proof_states],
                "triality_variance": [state["triality_variance"] for state in proof_states],
            }
        ),
    }

    return {
        "mu": mu_sequence,
        "total_asymmetry": total_asymmetry,
        "topological_humility": topological_humility,
        "proof": proof,
    }


def detect_QE(phi: Phi, sigma: dict[str, PoleState], seed: int, step: int, trials: int = 50) -> bool:
    rng = random.Random((seed << 32) ^ step)

    for _ in range(trials):
        perturb_seed = rng.randint(0, 2**32 - 1)
        candidate = evolve_sigma(phi, perturb_sigma(sigma, perturb_seed))
        if K_phi(candidate):
            return False

    return True


def vortex(phi: Phi, sigma: dict[str, PoleState], steps: int, seed: int) -> list[dict[str, Any]]:
    states = []
    current = sigma
    topo = topology_hash(phi.R)
    rng = random.Random(seed)

    for t in range(steps):
        perturb_seed = rng.randint(0, 2**32 - 1)
        candidate = evolve_sigma(phi, perturb_sigma(current, perturb_seed))

        if detect_QE(phi, current, seed, t):
            label = "QE"
        else:
            label = "REALIZABLE"

        states.append(
            {
                "step": t,
                "label": label,
                "sigma": _sigma_payload(candidate),
                "topology_hash": topo,
            }
        )
        current = candidate

    return states


def run(seed: int | None = 42, steps: int = 50) -> dict[str, Any]:
    phi = construct_phi(seed=seed)
    sigma = sample_sigma(seed=seed)
    states = vortex(phi, sigma, steps, seed)

    return {
        "seed": seed,
        "phi": {
            "Sigma": phi.Sigma,
            "R": phi.R,
        },
        "states": states,
        "epistemic": compute_epistemic(states, phi.R),
        "topology_hash": topology_hash(phi.R),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
