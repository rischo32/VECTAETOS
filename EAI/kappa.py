from .encode_v2 import encode_v2


# --------------------------------------------------
# κ SIGNATURE (CLOSURE TRACE)
# --------------------------------------------------
# κ is NOT:
# - a metric
# - a score
# - a signal
#
# κ is a structural trace of closure inconsistency
# under fixed transformation composition
# --------------------------------------------------


def kappa_signature(a, transforms):
    """
    Compute κ as closure trace.

    Parameters:
    - a: system output
    - transforms: fixed, predefined transformation set

    Returns:
    - sorted list of closure errors (structural trace only)
    """

    errors = []

    for t1 in transforms:
        for t2 in transforms:

            # composition
            x1 = t1(t2(a))
            x2 = t2(t1(a))

            # encode (structural, non-semantic)
            e1 = encode_v2(x1)
            e2 = encode_v2(x2)

            # closure error (L1 distance)
            e = sum(abs(i - j) for i, j in zip(e1, e2))

            errors.append(e)

    # IMPORTANT:
    # sorting ensures deterministic structural representation
    return sorted(errors)


# --------------------------------------------------
# FORBIDDEN OPERATIONS (DOCUMENTATION ONLY)
# --------------------------------------------------
# The following must NEVER be implemented:
#
# - kappa_transition(...)
# - threshold detection
# - scoring functions
# - classification based on κ
#
# Reason:
# These introduce interpretation and violate:
# ∂Φ / ∂EAI = 0
#
# κ must remain a terminal structural artifact.
# --------------------------------------------------
