import copy
from typing import Dict, Tuple, List

import numpy as np

from .stabilization import stabilize_delta
from .canonical import canonicalize
from .hash import hash_phi

Index = int
Triple = Tuple[Index, Index, Index]


def perturb_delta(
    delta: Dict[Triple, float],
    epsilon: float = 1e-6,
) -> Dict[Triple, float]:
    """
    Deterministic perturbation (NO randomness).
    """

    perturbed = {}

    for (i, j, k), v in delta.items():
        shift = ((i + j + k) % 3 - 1) * epsilon
        perturbed[(i, j, k)] = v + shift

    return perturbed


def kappa_trace(
    delta: Dict[Triple, float],
    steps: int = 5,
) -> List[str]:
    """
    κ trace = sequence of hashes under controlled perturbations.
    """

    traces = []
    current = copy.deepcopy(delta)

    for _ in range(steps):
        current = perturb_delta(current)
        stable = stabilize_delta(current)
        canon = canonicalize(stable)
        h = hash_phi(canon)
        traces.append(h)

    return traces


def kappa_signature(
    delta: Dict[Triple, float]
) -> np.ndarray:
    """
    κ signature = deterministic numeric embedding of structure.

    Requirements:
    - no NaN
    - deterministic
    - non-trivial variance
    - no interpretation
    """

    if not delta:
        return np.zeros(1)

    # stabilizácia → canonical
    stable = stabilize_delta(delta)
    canon = canonicalize(stable)

    # extrahuj hodnoty deterministicky
    items = sorted(canon.items())  # order invariant
    values = np.array([v for _, v in items], dtype=float)

    # ochrana proti nulovej norme
    norm = np.linalg.norm(values)

    if norm == 0:
        return np.zeros_like(values)

    return values / norm
