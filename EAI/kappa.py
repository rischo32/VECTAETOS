import numpy as np


def kappa_signature(encodings):
    """
    κ (kappa) = structural trace of encoding distribution

    NON-EVALUATIVE
    NON-INTERVENTIONAL
    NO TRANSFORMS (internally resolved upstream)

    Input:
        encodings: list of vectors

    Output:
        list (structural trace only)
    """

    n = len(encodings)

    if n == 0:
        return []

    enc = np.array(encodings)

    # 1. centroid
    centroid = np.mean(enc, axis=0)

    # 2. deviations (distance from centroid)
    deviations = np.linalg.norm(enc - centroid, axis=1)

    # 3. normalize (scale-invariant trace)
    total = np.sum(deviations)

    if total == 0:
        return deviations.tolist()

    kappa = deviations / total

    return kappa.tolist()
