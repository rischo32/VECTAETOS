import copy
from typing import Dict, Tuple, List

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

    NO:
    - threshold
    - classification
    - decision

    YES:
    - structural sensitivity trace
    """

    traces = []

    current = copy.deepcopy(delta)

    for _ in range(steps):

        # perturb
        current = perturb_delta(current)

        # stabilization
        stable = stabilize_delta(current)

        # canonical
        canon = canonicalize(stable)

        # hash
        h = hash_phi(canon)

        traces.append(h)

    return traces
