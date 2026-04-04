from typing import Dict, Tuple, Union
import numpy as np

Index = int
Triple = Tuple[Index, Index, Index]


def _vector_to_dict(delta: np.ndarray) -> Dict[Triple, float]:
    """
    Convert ℝ^56 vector → Dict[(i,j,k) → value]
    using lexicographic ordering of triples.
    """
    if delta.shape[0] != 56:
        raise ValueError("Delta vector must have dimension 56.")

    triples = []
    for i in range(8):
        for j in range(i + 1, 8):
            for k in range(j + 1, 8):
                triples.append((i, j, k))

    return {triples[t]: float(delta[t]) for t in range(56)}


def _collect_indices(delta: Dict[Triple, float]):
    indices = set()
    for (i, j, k) in delta.keys():
        indices.add(i)
        indices.add(j)
        indices.add(k)
    return sorted(indices)


def is_representable(
    delta: Union[Dict[Triple, float], np.ndarray],
    tol: float = 1e-9,
) -> bool:
    """
    Check if Δ ∈ 𝒟 (i.e. Δ = dR for some R ∈ so(8)).

    Equivalent condition:
        dΔ = 0   (closure condition)

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

    # --- Normalize input ---
    if isinstance(delta, np.ndarray):
        try:
            delta = _vector_to_dict(delta)
        except Exception:
            return False

    if not isinstance(delta, dict):
        return False

    # --- Collect indices ---
    indices = _collect_indices(delta)

    # --- Check closure condition ---
    for i in indices:
        for j in indices:
            for k in indices:
                for l in indices:
                    if len({i, j, k, l}) < 4:
                        continue

                    val = (
                        delta.get((j, k, l), 0.0)
                        - delta.get((i, k, l), 0.0)
                        + delta.get((i, j, l), 0.0)
                        - delta.get((i, j, k), 0.0)
                    )

                    if abs(val) > tol:
                        return False

    return True
