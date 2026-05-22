#!/usr/bin/env python3
"""
VECTAETOS — EK Core Representability Check

Purpose:
    Determine whether a 56-dimensional curvature vector Δ is algebraically
    representable as Δ = d1 R over the complete 8-node relational field.

This module does NOT:
    - compute K(Φ)
    - compute κ
    - compute truth
    - compute safety
    - select trajectories
    - optimize anything
    - mutate Φ or R

It only checks the structural condition:

    Δ ∈ Im(d1)

For the complete simplex over 8 nodes, this is equivalent to:

    d2 Δ = 0

because H^2 of the simplex is trivial.

Python: 3.11+
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Final

import numpy as np


N_NODES: Final[int] = 8
DELTA_DIM: Final[int] = 56
DEFAULT_ATOL: Final[float] = 1e-9


TRIPLES: Final[tuple[tuple[int, int, int], ...]] = tuple(
    (i, j, k)
    for i in range(N_NODES)
    for j in range(i + 1, N_NODES)
    for k in range(j + 1, N_NODES)
)

TETRAS: Final[tuple[tuple[int, int, int, int], ...]] = tuple(
    (i, j, k, l)
    for i in range(N_NODES)
    for j in range(i + 1, N_NODES)
    for k in range(j + 1, N_NODES)
    for l in range(k + 1, N_NODES)
)

TRIPLE_INDEX: Final[dict[tuple[int, int, int], int]] = {
    triple: index for index, triple in enumerate(TRIPLES)
}


def _as_delta_vector(delta: Iterable[float] | np.ndarray) -> np.ndarray | None:
    """
    Convert input to canonical 56-dimensional float vector.

    Returns None for invalid input.
    """
    try:
        arr = np.asarray(delta, dtype=float)
    except (TypeError, ValueError):
        return None

    if arr.shape != (DELTA_DIM,):
        return None

    if not np.isfinite(arr).all():
        return None

    return arr


def _delta_index(i: int, j: int, k: int) -> int:
    """
    Return canonical index for a triangle.

    The canonical vector ordering is lexicographic over i < j < k.
    """
    triple = tuple(sorted((i, j, k)))

    if len(set(triple)) != 3:
        raise ValueError(f"Invalid triangle indices: {(i, j, k)}")

    return TRIPLE_INDEX[triple]


def _delta_value(delta: np.ndarray, i: int, j: int, k: int) -> float:
    """
    Read Δ(i,j,k) from canonical vector representation.
    """
    return float(delta[_delta_index(i, j, k)])


def tetra_boundary(delta: Iterable[float] | np.ndarray, i: int, j: int, k: int, l: int) -> float:
    """
    Compute the oriented tetrahedral boundary:

        (d2 Δ)(i,j,k,l)
        = Δ(j,k,l) - Δ(i,k,l) + Δ(i,j,l) - Δ(i,j,k)

    for i < j < k < l.

    If Δ = d1 R, then d2 Δ = 0.
    """
    arr = _as_delta_vector(delta)

    if arr is None:
        raise ValueError("Expected finite Δ vector with shape (56,)")

    if not (i < j < k < l):
        raise ValueError(f"Expected i < j < k < l, got {(i, j, k, l)}")

    return (
        _delta_value(arr, j, k, l)
        - _delta_value(arr, i, k, l)
        + _delta_value(arr, i, j, l)
        - _delta_value(arr, i, j, k)
    )


def boundary_residual(delta: Iterable[float] | np.ndarray) -> float:
    """
    Return max absolute d2Δ residual.

    This is a structural observable only.
    It is not K(Φ), not κ, not truth, not safety.
    """
    arr = _as_delta_vector(delta)

    if arr is None:
        return float("inf")

    return max(abs(tetra_boundary(arr, *tetra)) for tetra in TETRAS)


def is_representable(delta: Iterable[float] | np.ndarray, *, atol: float = DEFAULT_ATOL) -> bool:
    """
    Check whether Δ is representable as Δ = d1 R.

    Returns:
        True  if Δ satisfies d2Δ = 0 within tolerance.
        False otherwise.

    This is a deterministic structural check only.
    """
    arr = _as_delta_vector(delta)

    if arr is None:
        return False

    if atol < 0:
        raise ValueError("atol must be non-negative")

    residual = boundary_residual(arr)

    return bool(residual <= atol)


__all__ = [
    "DELTA_DIM",
    "N_NODES",
    "TRIPLES",
    "TETRAS",
    "boundary_residual",
    "is_representable",
    "tetra_boundary",
]
