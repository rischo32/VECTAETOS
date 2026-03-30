from .encode_v3 import encode_v3
from .delta import compute_delta
from .spectral import reconstruct_R, spectral_signature
from .kappa import kappa_signature


# IMMUTABLE TRANSFORMS (locked)
TRANSFORMS = (
    lambda x: x[::-1],
    lambda x: x[:len(x)//2],
    lambda x: x + x,
)


def run_eai(system, inputs):
    return _run_eai(system, inputs, TRANSFORMS)


def _run_eai(system, inputs, transforms):

    # 1. collect outputs (no adaptation, no feedback)
    outputs = [system(x) for x in inputs]

    # 2. encoding (FIXED: no transforms passed)
    encodings = [encode_v3(o) for o in outputs]

    # 3. curvature
    delta = compute_delta(encodings)

    # 4. relational structure
    n = len(encodings)
    R = reconstruct_R(delta, n)

    # 5. spectrum
    spectrum = spectral_signature(R)

    # 6. κ trace (structure only)
    kappa = kappa_signature(encodings)

    return {
        "encodings": encodings,
        "delta": delta.tolist(),
        "R": R.tolist(),
        "spectrum": spectrum.tolist(),
        "kappa_trace": kappa
    }
