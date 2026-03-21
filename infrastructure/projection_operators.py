"""
VECTAETOS — Projection Operators (Π)
Multi-projection / Entropy / Merkle

NON-ONTOLOGICAL
DESCRIPTIVE ONLY
NO EPISTEMIC AUTHORITY
"""

import random
import math
import hashlib
import json
from datetime import datetime


# ─────────────────────────────────────────────
# Π OPERATORS
# ─────────────────────────────────────────────

def projection_local(signal: dict) -> dict:
    weights = {k: abs(v) for k, v in signal.items()}
    total = sum(weights.values()) or 1.0
    return {k: weights[k] / total for k in weights}


def projection_cycle(signal: dict) -> dict:
    n = len(signal)
    return {k: 1.0 / n for k in signal}


def projection_relax(signal: dict) -> dict:
    n = len(signal)
    return {k: 1.0 / n for k in signal}


def projection_rand(signal: dict) -> dict:
    values = [random.random() for _ in signal]
    total = sum(values)
    return {k: v / total for k, v in zip(signal.keys(), values)}


PROJECTION_OPERATORS = {
    "local": projection_local,
    "cycle": projection_cycle,
    "relax": projection_relax,
    "rand": projection_rand
}


# ─────────────────────────────────────────────
# MULTI-Π PROJECTION
# ─────────────────────────────────────────────

def multi_projection(signal: dict) -> dict:
    """
    Generate multiple projections simultaneously.
    No selection = no authority.
    """

    projections = {}

    for name, operator in PROJECTION_OPERATORS.items():
        projections[name] = operator(signal)

    return projections


# ─────────────────────────────────────────────
# ENTROPY (H)
# ─────────────────────────────────────────────

def entropy(distribution: dict) -> float:
    """
    Shannon entropy (descriptive only).
    """
    h = 0.0
    for p in distribution.values():
        if p > 0:
            h -= p * math.log(p)
    return h


def entropy_map(projections: dict) -> dict:
    return {k: entropy(v) for k, v in projections.items()}


# ─────────────────────────────────────────────
# MERKLE TREE (PROJECTIONS)
# ─────────────────────────────────────────────

def hash_distribution(dist: dict) -> str:
    data = json.dumps(dist, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def merkle_root(hashes: list) -> str:
    """
    Simple Merkle root (pairwise hash).
    """
    if not hashes:
        return None

    level = hashes

    while len(level) > 1:
        next_level = []

        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left

            combined = (left + right).encode()
            next_level.append(hashlib.sha256(combined).hexdigest())

        level = next_level

    return level[0]


def merkle_from_projections(projections: dict) -> dict:
    hashes = {k: hash_distribution(v) for k, v in projections.items()}
    root = merkle_root(list(hashes.values()))

    return {
        "leaf_hashes": hashes,
        "merkle_root": root
    }


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def generate_projection_bundle(signal: dict) -> dict:
    """
    Full projection bundle:
    - multi Π
    - entropy
    - merkle integrity
    """

    projections = multi_projection(signal)
    entropies = entropy_map(projections)
    merkle = merkle_from_projections(projections)

    return {
        "type": "multi_projection_bundle",
        "projections": projections,
        "entropy": entropies,
        "merkle": merkle,
        "epistemic_status": "descriptive_only",
        "authority": "none",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
