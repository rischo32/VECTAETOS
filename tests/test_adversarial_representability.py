import numpy as np
import pytest

from ek_core.representability import is_representable


N = 8

TRIPLES: tuple[tuple[int, int, int], ...] = tuple(
    (i, j, k)
    for i in range(N)
    for j in range(i + 1, N)
    for k in range(j + 1, N)
)

TETRAS: tuple[tuple[int, int, int, int], ...] = tuple(
    (i, j, k, l)
    for i in range(N)
    for j in range(i + 1, N)
    for k in range(j + 1, N)
    for l in range(k + 1, N)
)

TRIPLE_INDEX: dict[tuple[int, int, int], int] = {
    triple: index for index, triple in enumerate(TRIPLES)
}


def delta_index(i: int, j: int, k: int) -> int:
    """
    Return index of an ordered canonical triple i < j < k.
    """
    triple = tuple(sorted((i, j, k)))

    if len(set(triple)) != 3:
        raise ValueError(f"Invalid triangle indices: {(i, j, k)}")

    return TRIPLE_INDEX[triple]


def delta_value(delta: np.ndarray, i: int, j: int, k: int) -> float:
    """
    Read Δ(i,j,k) from canonical i < j < k vector representation.
    """
    return float(delta[delta_index(i, j, k)])


def make_delta(entries: dict[tuple[int, int, int], float]) -> np.ndarray:
    """
    Build a 56-dimensional Δ vector from sparse triangle entries.
    """
    delta = np.zeros(len(TRIPLES), dtype=float)

    for triple, value in entries.items():
        delta[delta_index(*triple)] = float(value)

    return delta


def deterministic_antisymmetric_R() -> np.ndarray:
    """
    Deterministic antisymmetric R ∈ so(8).

    This avoids np.random and gives reproducible CI behavior.
    """
    r = np.zeros((N, N), dtype=float)

    for i in range(N):
        for j in range(i + 1, N):
            value = ((i + 1) * 17.0 - (j + 1) * 11.0 + (i + 1) * (j + 1)) / 37.0
            r[i, j] = value
            r[j, i] = -value

    return r


def delta_from_R(r: np.ndarray) -> np.ndarray:
    """
    Compute Δ = d₁R with:

        Δ(i,j,k) = R_ij + R_jk + R_ki

    for i < j < k.
    """
    if r.shape != (N, N):
        raise ValueError(f"Expected R shape {(N, N)}, got {r.shape}")

    delta = np.zeros(len(TRIPLES), dtype=float)

    for index, (i, j, k) in enumerate(TRIPLES):
        delta[index] = r[i, j] + r[j, k] + r[k, i]

    return delta


def tetra_boundary(delta: np.ndarray, i: int, j: int, k: int, l: int) -> float:
    """
    Compute d₂Δ on tetrahedron i < j < k < l:

        (d₂Δ)(i,j,k,l)
        = Δ(j,k,l) - Δ(i,k,l) + Δ(i,j,l) - Δ(i,j,k)

    If Δ = d₁R, then d₂Δ = 0.
    """
    if not (i < j < k < l):
        raise ValueError(f"Expected i < j < k < l, got {(i, j, k, l)}")

    return (
        delta_value(delta, j, k, l)
        - delta_value(delta, i, k, l)
        + delta_value(delta, i, j, l)
        - delta_value(delta, i, j, k)
    )


def max_abs_tetra_boundary(delta: np.ndarray) -> float:
    """
    Local witness that Δ violates the d₂Δ = 0 consistency condition.
    """
    return max(abs(tetra_boundary(delta, *tetra)) for tetra in TETRAS)


def assert_representable(delta: np.ndarray) -> None:
    assert delta.shape == (56,)
    assert np.isfinite(delta).all()
    assert bool(is_representable(delta)), "Expected Δ ∈ Im(d₁), but it was rejected"


def assert_not_representable(delta: np.ndarray) -> None:
    assert delta.shape == (56,)

    try:
        result = is_representable(delta)
    except (ValueError, TypeError, AssertionError, FloatingPointError):
        return

    assert not bool(result), "Expected Δ ∉ Im(d₁), but it passed"


def test_accept_zero_delta() -> None:
    """
    Zero curvature is representable by R = 0.
    """
    delta = np.zeros(56, dtype=float)

    assert max_abs_tetra_boundary(delta) == 0.0
    assert_representable(delta)


def test_accept_delta_constructed_from_antisymmetric_R() -> None:
    """
    Any Δ explicitly constructed as d₁R from R ∈ so(8) must be representable.
    """
    r = deterministic_antisymmetric_R()

    np.testing.assert_allclose(r + r.T, np.zeros((N, N)), rtol=0.0, atol=1e-12)
    np.testing.assert_allclose(np.diag(r), np.zeros(N), rtol=0.0, atol=1e-12)

    delta = delta_from_R(r)

    assert max_abs_tetra_boundary(delta) < 1e-10
    assert_representable(delta)


def test_reject_isolated_triangle_delta() -> None:
    """
    A single isolated triangular 2-cochain is not a valid d₁R image.

    This is the main adversarial case:
    it is deterministic and structurally outside Im(d₁).
    """
    delta = make_delta({(0, 1, 2): 1.0})

    assert max_abs_tetra_boundary(delta) > 0.0
    assert_not_representable(delta)


@pytest.mark.parametrize(
    "entries",
    [
        {(0, 1, 2): 1.0, (0, 1, 3): -0.25},
        {(0, 2, 5): 0.75, (1, 3, 7): -1.25},
        {(2, 4, 6): 3.0},
    ],
)
def test_reject_boundary_inconsistent_sparse_delta(
    entries: dict[tuple[int, int, int], float],
) -> None:
    """
    Sparse hand-built Δ values usually violate d₂Δ = 0.

    We explicitly verify the violation before calling is_representable.
    """
    delta = make_delta(entries)

    assert max_abs_tetra_boundary(delta) > 0.0
    assert_not_representable(delta)


@pytest.mark.parametrize(
    "bad_value",
    [np.nan, np.inf, -np.inf],
)
def test_reject_non_finite_delta(bad_value: float) -> None:
    """
    Non-finite Δ must never pass representability.
    """
    delta = np.zeros(56, dtype=float)
    delta[0] = bad_value

    assert_not_representable(delta)


def test_representability_is_deterministic() -> None:
    """
    Same Δ must always produce the same result.
    """
    r = deterministic_antisymmetric_R()
    delta = delta_from_R(r)

    first = bool(is_representable(delta))
    second = bool(is_representable(delta.copy()))

    assert first == second
