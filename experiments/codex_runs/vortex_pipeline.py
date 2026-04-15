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


def detect_QE(phi: Phi, sigma: dict[str, PoleState], trials: int = 50) -> bool:
    for i in range(trials):
        candidate = evolve_sigma(phi, perturb_sigma(sigma, i))
        if K_phi(candidate):
            return False
    return True


def vortex(phi: Phi, sigma: dict[str, PoleState], steps: int) -> list[dict[str, Any]]:
    states = []
    current = sigma
    topo = topology_hash(phi.R)
    coherence = RMK.coherence(phi.R)
    for t in range(steps):
        candidate = evolve_sigma(phi, perturb_sigma(current, t))
        if detect_QE(phi, current):
            label = "QE"
        else:
            label = "REALIZABLE"
        states.append(
            {
                "step": t,
                "label": label,
                "sigma": _sigma_payload(candidate),
                "topology_hash": topo,
                "coherence": coherence,
            }
        )
        current = candidate
    return states


def run(seed: int | None = 42, steps: int = 50) -> dict[str, Any]:
    phi = construct_phi(seed=seed)
    sigma = sample_sigma(seed=seed)
    return {
        "phi": {
            "Sigma": phi.Sigma,
            "R": phi.R,
        },
        "states": vortex(phi, sigma, steps),
        "topology_hash": topology_hash(phi.R),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
