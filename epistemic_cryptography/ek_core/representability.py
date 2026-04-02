from itertools import combinations
from typing import Dict, Tuple

Index = int
Triple = Tuple[Index, Index, Index]


def is_representable(delta: Dict[Triple, float], tol: float = 1e-9) -> bool:
    """
    Check if Delta_hat ∈ D (i.e. Delta_hat is representable as dR).

    This is equivalent to the closure condition:
        dDelta = 0

    For every quadruple (i, j, k, l):

        Δ(j,k,l)
      - Δ(i,k,l)
      + Δ(i,j,l)
      - Δ(i,j,k)
      = 0

    No optimization.
    No reconstruction.
    Pure structural invariant.
    """

    indices = set()
    for (i, j, k) in delta.keys():
        indices.update([i, j, k])

    indices = sorted(indices)

    for (i, j, k, l) in combinations(indices, 4):

        val = (
            delta.get((j, k, l), 0.0)
            - delta.get((i, k, l), 0.0)
            + delta.get((i, j, l), 0.0)
            - delta.get((i, j, k), 0.0)
        )

        if abs(val) > tol:
            return False

    return True


def representability_residual(delta: Dict[Triple, float]) -> float:
    """
    Diagnostic ONLY (not for decision logic).

    Returns maximum violation of closure condition.

    NOTE:
    - NOT for thresholding
    - NOT for classification
    - NOT for decision use
    """

    indices = set()
    for (i, j, k) in delta.keys():
        indices.update([i, j, k])

    indices = sorted(indices)

    max_violation = 0.0

    for (i, j, k, l) in combinations(indices, 4):

        val = (
            delta.get((j, k, l), 0.0)
            - delta.get((i, k, l), 0.0)
            + delta.get((i, j, l), 0.0)
            - delta.get((i, j, k), 0.0)
        )

        max_violation = max(max_violation, abs(val))

    return max_violation
