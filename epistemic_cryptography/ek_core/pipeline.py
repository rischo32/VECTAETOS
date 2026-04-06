from typing import List, Dict, Tuple, Union, Callable

from .reconstruct import reconstruct_delta
from .representability import is_representable
from .stabilization import stabilize_delta
from .canonical import canonicalize
from .hash import structural_hash
from .merkle import merkle_root
from .kappa import kappa_signature, kappa_trace

Index = int
Triple = Tuple[Index, Index, Index]


# =========================
# CORE STEP
# =========================

def ek_step(outputs) -> Dict:
    """
    Single EK 2.0 step.
    """

    # 1. reconstruct
    delta_hat = reconstruct_delta(outputs)

    # 2. representability constraint
    if not is_representable(delta_hat):
        raise ValueError("Invalid epistemic structure (Delta not in D)")

    # 3. stabilization
    delta_stable = stabilize_delta(delta_hat)

    # 4. canonical
    delta_c = canonicalize(delta_stable)

    # 5. hash
    h = structural_hash(delta_c)

    # 6. κ
    kappa_sig = kappa_signature(delta_c)
    kappa_tr = kappa_trace(delta_c)

    return {
        "delta": delta_c,
        "hash": h,
        "kappa": kappa_sig,
        "kappa_trace": kappa_tr,
    }


# =========================
# TRAJECTORY
# =========================

def ek_trajectory(stream: List[List]) -> Dict:
    """
    Process sequence of outputs.
    """

    hashes = []
    artifacts = []

    for outputs in stream:
        try:
            step = ek_step(outputs)

            hashes.append(step["hash"])
            artifacts.append(step)

        except ValueError:
            continue

    root = merkle_root(hashes)

    return {
        "artifact": {
            "steps": artifacts,
            "hashes": hashes,
            "merkle_root": root,
            "length": len(hashes),
        }
    }


# =========================
# PUBLIC API
# =========================

def run_pipeline(system: Callable, inputs: List):
    """
    STRICT:
    - no feedback
    - no mutation
    """

    return [system(x) for x in inputs]
