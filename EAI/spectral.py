import numpy as np


def reconstruct_R(delta_values, n):
    """
    Minimal reconstruction of antisymmetric matrix R from Δ.

    delta_values: array of size nC3
    n: number of nodes

    returns: R ∈ so(n)
    """

    R = np.zeros((n, n))
    idx = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                d = delta_values[idx]

                # distribute curvature with orientation
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
    Compute eigenvalue spectrum of R
    """

    eigvals = np.linalg.eigvals(R)
    eigvals = np.sort(np.abs(eigvals))[::-1]

    return eigvals


def dominance_ratio(eigs):
    """
    Continuous dominance measure (no threshold)
    """

    if len(eigs) < 2:
        return 0.0

    return eigs[0] / (eigs[1] + 1e-12)
