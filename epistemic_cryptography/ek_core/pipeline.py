from typing import List, Dict, Tuple

from .reconstruct import reconstruct_delta
from .representability import is_representable
from .stabilization import stabilize_delta
from .canonical import canonicalize
from .hash import hash_phi
from .merkle import merkle_root

Index = int
Triple = Tuple[Index, Index, Index]


def ek_step(outputs) -> Tuple[Dict[Triple, float], str]:
    """
    Single EK 2.0 step.

    Returns:
    - canonical Delta
    - hash
    """

    # reconstruct
    delta_hat = reconstruct_delta(outputs)

    # validity (structural only)
    if not is_representable(delta_hat):
        raise ValueError("Invalid epistemic structure (Delta not in D)")

    # stabilize
    delta_stable = stabilize_delta(delta_hat)

    # canonicalize
    delta_c = canonicalize(delta_stable)

    # hash
    h = hash_phi(delta_c)

    return delta_c, h


def ek_trajectory(stream: List[List]) -> Dict:
    """
    Process a sequence of system outputs.

    Returns:
    - hashes
    - merkle root
    """

    hashes = []
    deltas = []

    for outputs in stream:
        try:
            delta_c, h = ek_step(outputs)
            hashes.append(h)
            deltas.append(delta_c)

        except ValueError:
            # invalid Φ → skip WITHOUT interpretation
            continue

    root = merkle_root(hashes)

    return {
        "hashes": hashes,
        "merkle_root": root,
        "length": len(hashes),
    }
