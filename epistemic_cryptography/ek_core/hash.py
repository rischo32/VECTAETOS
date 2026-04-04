import hashlib
from typing import Dict, Tuple

from ek_core.canonical import canonicalize

Index = int
Triple = Tuple[Index, Index, Index]


def serialize_delta(delta: Dict[Triple, float]) -> bytes:
    """
    Canonical serialization of Delta.

    Guarantees:
    - deterministic
    - order-invariant
    - float-stable
    """

    items = sorted(delta.items())

    parts = []

    for (i, j, k), v in items:
        parts.append(f"{i},{j},{k}:{v:.12f}")

    serialized = "|".join(parts)

    return serialized.encode("utf-8")


def structural_hash(delta: Dict[Triple, float]) -> str:
    """
    Structural identity hash.

    Properties:
    - invariant under representation
    - deterministic
    - no semantics
    """

    # 🔥 CRITICAL: enforce canonical form
    delta_c = canonicalize(delta)

    data = serialize_delta(delta_c)

    return hashlib.sha256(data).hexdigest()


def hash_delta(delta: Dict[Triple, float]) -> str:
    """
    Alias for structural_hash (backward compatibility).
    """
    return structural_hash(delta)


def hash_phi(delta: Dict[Triple, float]) -> str:
    """
    EK 2.0 hash entrypoint.

    Unlike previous version:
    - DOES NOT trust caller
    - ALWAYS canonicalizes internally
    """

    return structural_hash(delta)
