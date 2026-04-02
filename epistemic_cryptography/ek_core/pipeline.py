from typing import List, Dict, Tuple

from .reconstruct import reconstruct_delta
from .representability import is_representable
from .stabilization import stabilize_delta
from .canonical import canonicalize
from .hash import hash_phi
from .merkle import merkle_root
from .kappa import kappa_trace

Index = int
Triple = Tuple[Index, Index, Index]


def ek_step(outputs) -> Dict:
    """
    Single EK 2.0 step.

    Returns full structural artifact.
    """

    # --- 1. reconstruct ---
    delta_hat = reconstruct_delta(outputs)

    # --- 2. representability (hard constraint) ---
    if not is_representable(delta_hat):
        raise ValueError("Invalid epistemic structure (Delta not in D)")

    # --- 3. stabilization ---
    delta_stable = stabilize_delta(delta_hat)

    # --- 4. canonicalization ---
    delta_c = canonicalize(delta_stable)

    # --- 5. hash ---
    h = hash_phi(delta_c)

    # --- 6. kappa trace (NON-INTERPRETATIVE) ---
    k_trace = kappa_trace(delta_stable)

    return {
        "delta": delta_c,
        "hash": h,
        "kappa_trace": k_trace,
    }


def ek_trajectory(stream: List[List]) -> Dict:
    """
    Process a sequence of outputs (trajectory).

    NO:
    - interpretation
    - filtering based on meaning

    YES:
    - structural accumulation
    """

    hashes = []
    artifacts = []

    for outputs in stream:
        try:
            step = ek_step(outputs)

            hashes.append(step["hash"])
            artifacts.append(step)

        except ValueError:
            # invalid Φ → skip WITHOUT interpretation
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
