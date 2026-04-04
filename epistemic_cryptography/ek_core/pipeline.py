from typing import List, Dict, Tuple, Union

from .reconstruct import reconstruct_delta
from .representability import is_representable
from .stabilization import stabilize_delta
from .canonical import canonicalize
from .hash import structural_hash
from .merkle import merkle_root
from .kappa import kappa_signature

Index = int
Triple = Tuple[Index, Index, Index]


# =========================
# CORE STEP
# =========================

def ek_step(outputs) -> Dict:
    """
    Single EK 2.0 step.

    Input:
        outputs → raw system outputs

    Output:
        structural artifact
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

    # 5. hash (STRUCTURAL)
    h = structural_hash(delta_c)

    # 6. κ (structure only)
    kappa = kappa_signature(delta_c)

    return {
        "delta": delta_c,
        "hash": h,
        "kappa": kappa,
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
# 🔥 PUBLIC API (CRITICAL)
# =========================

def run_pipeline(delta: Union[Dict[Triple, float], List[List]]) -> Dict:
    """
    Unified EK entrypoint.

    Accepts:
    - Δ directly (dict)
    - or stream (list of outputs)

    Guarantees:
    - no feedback
    - no mutation
    - deterministic
    """

    # CASE 1: already Δ
    if isinstance(delta, dict):
        delta_c = canonicalize(delta)

        return {
            "delta": delta_c,
            "hash": structural_hash(delta_c),
            "kappa": kappa_signature(delta_c),
        }

    # CASE 2: trajectory
    elif isinstance(delta, list):
        return ek_trajectory(delta)

    else:
        raise TypeError("Unsupported input type for run_pipeline")
