from encode_v3 import encode_v3
from delta import compute_delta
from spectral import reconstruct_R, spectral_signature
from kappa import kappa_signature


def run_eai(system, inputs, transforms):

    # Step 1: collect outputs
    outputs = [system(q) for q in inputs]

    # Step 2: encode
    encodings = [encode_v3(o, transforms) for o in outputs]

    # Step 3: curvature
    delta = compute_delta(encodings)

    # Step 4: reconstruct R
    R = reconstruct_R(delta, len(encodings))

    # Step 5: spectrum
    eigs = spectral_signature(R)

    # Step 6: kappa
    kappa = [kappa_signature(o, transforms) for o in outputs]

    return {
        "encodings": encodings,
        "delta": delta.tolist(),
        "R": R.tolist(),
        "spectrum": eigs.tolist(),
        "kappa": kappa
    }
