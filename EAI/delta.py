import numpy as np

def distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def compute_delta(encodings):
    """
    Compute curvature Δ over all triplets.

    encodings: list of vectors (encode outputs)

    returns: np.array of Δ values
    """

    n = len(encodings)
    deltas = []

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                dij = distance(encodings[i], encodings[j])
                djk = distance(encodings[j], encodings[k])
                dki = distance(encodings[k], encodings[i])

                closure = abs((dij + djk + dki))
                delta = dij + djk + dki - closure

                deltas.append(delta)

    return np.array(deltas)
