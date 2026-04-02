import hashlib
from typing import Dict, Tuple

Index = int
Triple = Tuple[Index, Index, Index]


def serialize_delta(delta: Dict[Triple, float]) -> bytes:
    """
    Canonical serialization of Delta.

    Requirements:
    - deterministic
    - order-invariant
    - no interpretation
    """

    # sort keys lexicographically
    items = sorted(delta.items())

    parts = []

    for (i, j, k), v in items:
        parts.append(f"{i},{j},{k}:{v:.12f}")

    serialized = "|".join(parts)

    return serialized.encode("utf-8")


def hash_delta(delta: Dict[Triple, float]) -> str:
    """
    Compute structural hash.

    This is NOT:
    - score
    - metric
    - classification

    This IS:
    - structural identity fingerprint
    """

    data = serialize_delta(delta)

    h = hashlib.sha256(data).hexdigest()

    return h


def hash_phi(delta_canonical: Dict[Triple, float]) -> str:
    """
    Final EK 2.0 hash.

    Input MUST be canonicalized Delta.

    No internal canonicalization allowed
    (to avoid hidden transformations).
    """

    return hash_delta(delta_canonical)
