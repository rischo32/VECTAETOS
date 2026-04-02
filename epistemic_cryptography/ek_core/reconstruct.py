from typing import List
import numpy as np


def embed_output(x) -> np.ndarray:
    """
    Deterministic embedding of system output into R^8.

    MUST BE:
    - fixed
    - non-adaptive
    - independent of dataset

    Example: simple numeric hashing
    """

    vec = np.zeros(8)

    s = str(x)

    for i, ch in enumerate(s):
        vec[i % 8] += (ord(ch) % 31) / 31.0

    return vec


def reconstruct_R(outputs: List) -> np.ndarray:
    """
    Construct antisymmetric matrix R_hat ∈ so(8)

    R_ij = sum_k (v_k[i] * v_k[j]) antisymmetrized

    No optimization.
    No fitting.
    Pure aggregation.
    """

    vectors = [embed_output(o) for o in outputs]

    R = np.zeros((8, 8))

    for v in vectors:
        outer = np.outer(v, v)
        R += outer - outer.T  # enforce antisymmetry

    return R


def compute_delta(R: np.ndarray):
    """
    Compute Delta_hat = dR

    Discrete exterior derivative:

    Δ(i,j,k) =
        R(j,k)
      - R(i,k)
      + R(i,j)
    """

    delta = {}

    n = R.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                val = (
                    R[j, k]
                    - R[i, k]
                    + R[i, j]
                )

                delta[(i, j, k)] = float(val)

    return delta


def reconstruct_delta(outputs: List):
    """
    Full reconstruction pipeline:

    outputs → R_hat → Delta_hat

    No feedback.
    No adaptivity.
    """

    R_hat = reconstruct_R(outputs)
    delta_hat = compute_delta(R_hat)

    return delta_hat
