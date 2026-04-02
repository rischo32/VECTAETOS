from typing import Dict, Tuple, List

Index = int
Triple = Tuple[Index, Index, Index]


def compute_node_degrees(delta: Dict[Triple, float]) -> Dict[Index, float]:
    """
    Structural invariant:
    degree of each node based on Delta.

    No interpretation.
    No optimization.
    """

    degree = {}

    for (i, j, k), v in delta.items():
        w = abs(v)

        degree[i] = degree.get(i, 0.0) + w
        degree[j] = degree.get(j, 0.0) + w
        degree[k] = degree.get(k, 0.0) + w

    return degree


def canonical_permutation(delta: Dict[Triple, float]) -> Tuple[Index, ...]:
    """
    Deterministic ordering of indices.

    Uses intrinsic structure only.
    No global comparison.
    """

    nodes = set()
    for (i, j, k) in delta.keys():
        nodes.update([i, j, k])

    nodes = sorted(nodes)

    degree = compute_node_degrees(delta)

    # stable deterministic sort
    nodes_sorted = sorted(nodes, key=lambda i: (degree.get(i, 0.0), i))

    return tuple(nodes_sorted)


def apply_permutation(
    delta: Dict[Triple, float],
    perm: Tuple[Index, ...],
) -> Dict[Triple, float]:
    """
    Reindex Delta according to permutation.

    perm = new ordering of indices
    """

    inv = {perm[i]: i for i in range(len(perm))}

    result = {}

    for (i, j, k), v in delta.items():
        result[(inv[i], inv[j], inv[k])] = v

    return result


def canonicalize(delta: Dict[Triple, float]) -> Dict[Triple, float]:
    """
    Canonical representative of Delta.

    Properties:
    - deterministic
    - permutation-invariant (indirectly)
    - no optimization
    - no global search
    """

    perm = canonical_permutation(delta)
    return apply_permutation(delta, perm)
