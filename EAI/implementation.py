from encode_v3 import encode_v3
from delta import compute_delta
from spectral import reconstruct_R, spectral_signature
from kappa import kappa_signature


# --------------------------------------------------
# FIXED TRANSFORMATION SET (IMMUTABLE)
# --------------------------------------------------
# DO NOT MODIFY
# These transforms are predefined, deterministic,
# and must remain unchanged to preserve non-intervention

TRANSFORMS = (
    lambda x: x[::-1],
    lambda x: x[:len(x)//2],
    lambda x: x + x
)


# --------------------------------------------------
# INTERNAL EXECUTION (SEALED)
# --------------------------------------------------

def _run_eai(system, inputs, transforms):

    # NON-INTERVENTION GUARANTEE:
    # inputs must be predefined and not modified during execution

    # Step 1: collect outputs (read-only interaction)
    outputs = [system(q) for q in inputs]

    # Step 2: encode (structural only)
    encodings = [encode_v3(o, transforms) for o in outputs]

    # Step 3: curvature
    delta = compute_delta(encodings)

    # Step 4: reconstruct relational structure
    R = reconstruct_R(delta, len(encodings))

    # Step 5: spectral signature
    eigs = spectral_signature(R)

    # Step 6: κ trace (closure distribution only)
    kappa_trace = [kappa_signature(o, transforms) for o in outputs]

    return {
        "encodings": encodings,
        "delta": delta.tolist(),
        "R": R.tolist(),
        "spectrum": eigs.tolist(),
        "kappa_trace": kappa_trace  # NOT a metric, NOT a signal
    }


# --------------------------------------------------
# PUBLIC API (CONSTRAINED ENTRY POINT)
# --------------------------------------------------

def run_eai(system, inputs):
    """
    Epistemic Audit Execution

    Constraints:
    - inputs must be predefined
    - no adaptive behavior allowed
    - transforms are fixed and immutable
    - no feedback loop permitted

    Returns:
    Structural artifact only (non-interpretative)
    """

    # Defensive checks (minimal, non-invasive)
    assert isinstance(inputs, list), "inputs must be a predefined list"

    return _run_eai(system, inputs, TRANSFORMS)
