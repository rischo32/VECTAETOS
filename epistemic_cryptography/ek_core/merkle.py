import hashlib
from typing import List


def hash_pair(a: str, b: str) -> str:
    """
    Deterministic pair hashing.

    Order is FIXED (no sorting).
    """

    data = (a + b).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def merkle_layer(hashes: List[str]) -> List[str]:
    """
    Build one layer of the Merkle tree.

    Rules:
    - deterministic pairing
    - no reordering
    - no optimization
    """

    if len(hashes) == 0:
        return []

    if len(hashes) == 1:
        return hashes

    next_layer = []

    for i in range(0, len(hashes), 2):
        left = hashes[i]

        if i + 1 < len(hashes):
            right = hashes[i + 1]
        else:
            # duplicate last (standard deterministic rule)
            right = left

        next_layer.append(hash_pair(left, right))

    return next_layer


def merkle_root(hashes: List[str]) -> str:
    """
    Compute Merkle root.

    Input:
    ordered list of EK hashes

    No:
    - sorting
    - filtering
    - interpretation
    """

    current = list(hashes)

    if not current:
        return ""

    while len(current) > 1:
        current = merkle_layer(current)

    return current[0]
