import numpy as np
from .encode_v2 import encode_v2


# --------------------------------------------------
# FIXED TRANSFORMATION SET (IMMUTABLE)
# --------------------------------------------------
# MUST match implementation.py

TRANSFORMS = (
    lambda x: x[::-1],
    lambda x: x[:len(x)//2],
    lambda x: x + x
)


# --------------------------------------------------
# ENCODE V3 (TRANSFORMATION-BASED)
# --------------------------------------------------

def encode_v3(a):
    """
    Encode object via transformation response.

    Returns:
    (I, S, V, T) — structural invariants only
    """

    base = encode_v2(a)

    # Apply fixed transforms
    variants = [encode_v2(t(a)) for t in TRANSFORMS]

    # --------------------------------------------------
    # I — Identity Stability (mean distance)
    # --------------------------------------------------
    I = sum(
        sum(abs(base[i] - v[i]) for i in range(len(base)))
        for v in variants
    ) / len(variants)

    # --------------------------------------------------
    # V — Variability (pairwise distance spread)
    # --------------------------------------------------
    pairwise = []

    for i in range(len(variants)):
        for j in range(i + 1, len(variants)):
            d = sum(abs(variants[i][k] - variants[j][k]) for k in range(len(base)))
            pairwise.append(d)

    V = sum(pairwise) / (len(pairwise) + 1e-12)

    # --------------------------------------------------
    # S — Sensitivity (normalized variability)
    # --------------------------------------------------
    S = V / (len(variants) + 1e-12)

    # --------------------------------------------------
    # T — Closure inconsistency (average over all pairs)
    # --------------------------------------------------
    closure_errors = []

    for t1 in TRANSFORMS:
        for t2 in TRANSFORMS:

            x1 = t1(t2(a))
            x2 = t2(t1(a))

            e1 = encode_v2(x1)
            e2 = encode_v2(x2)

            e = sum(abs(e1[i] - e2[i]) for i in range(len(base)))
            closure_errors.append(e)

    T = sum(closure_errors) / (len(closure_errors) + 1e-12)

    return (I, S, V, T)
