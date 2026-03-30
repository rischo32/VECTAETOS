import numpy as np


def reconstruct_R(delta_values, n):
    """
    Reconstruct antisymmetric matrix R from Δ.
    """

    R = np.zeros((n, n))
    idx = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                d = delta_values[idx]

                R[i, j] += d
                R[j, k] += d
                R[k, i] += d

                R[j, i] -= d
                R[k, j] -= d
                R[i, k] -= d

                idx += 1

    return R


def spectral_signature(R):
    """
    Raw eigenvalue spectrum (no interpretation, no sorting)
    """

    return np.linalg.eigvals(R)
