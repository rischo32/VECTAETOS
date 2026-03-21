#!/usr/bin/env python3
"""
VECTAETOS © — Projection Adapter v2 (Multi-Π + Glyph)

STATUS:
- NON-ONTOLOGICAL
- DESCRIPTIVE ONLY
- NO EPISTEMIC AUTHORITY

PURPOSE:
- Generate projection space Π(Φ|Σ)
- Provide entropy (H)
- Provide Merkle integrity
- Map projections → TetraGlyph shapes

IMPORTANT:
- This module does NOT compute Φ, K(Φ), κ
- This module does NOT interpret meaning
- This module produces candidate projections only
"""

import random
import math
import hashlib
import json
from datetime import datetime

# External bridge
from TetraGlyph.glyph_projection import multi_projection_to_glyphs


# ─────────────────────────────────────────────
# AXIOMS (Σ₁…Σ₈)
# ─────────────────────────────────────────────

AXIOMS = {
    "INT": "Intent",
    "LEX": "Existence",
    "VER": "Truth",
    "LIB": "Freedom",
    "UNI": "Unity",
    "REL": "Reciprocity",
    "WIS": "Wisdom",
    "CRE": "Creation"
}


# ─────────────────────────────────────────────
# SIGNAL EXTRACTION (SHALLOW, NON-SEMANTIC)
# ─────────────────────────────────────────────

def extract_signal(text: str) -> dict:
    base = {k: 1.0 for k in AXIOMS.keys()}
    text = text.lower()

    if "zmysel" in text or "why" in text:
        base["VER"] += 0.5
        base["WIS"] += 0.3

    if "rozhodnutie" in text or "decision" in text:
        base["INT"] += 0.4
        base["LIB"] += 0.3

    if "konflikt" in text or "napatie" in text:
        base["REL"] += 0.6
        base["UNI"] -= 0.2

    return base


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
    return {
        name: operator(signal)
        for name, operator in PROJECTION_OPERATORS.items()
    }


# ─────────────────────────────────────────────
# ENTROPY (H)
# ─────────────────────────────────────────────

def entropy(dist: dict) -> float:
    h = 0.0
    for p in dist.values():
        if p > 0:
            h -= p * math.log(p)
    return h


def entropy_map(projections: dict) -> dict:
    return {k: entropy(v) for k, v in projections.items()}


# ─────────────────────────────────────────────
# MERKLE TREE
# ─────────────────────────────────────────────

def hash_distribution(dist: dict) -> str:
    data = json.dumps(dist, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def merkle_root(hashes: list) -> str:
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

def generate_projection_bundle(query_text: str) -> dict:
    """
    Multi-Π projection bundle.
    Returns projection space, not answer.
    """

    signal = extract_signal(query_text)

    projections = multi_projection(signal)
    entropies = entropy_map(projections)
    merkle = merkle_from_projections(projections)

    glyphs = multi_projection_to_glyphs({
        "projections": projections
    })

    return {
        "type": "multi_projection_bundle",
        "axioms": AXIOMS,
        "projections": projections,
        "glyphs": glyphs,
        "entropy": entropies,
        "merkle": merkle,
        "epistemic_status": "descriptive_only",
        "authority": "none",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# ─────────────────────────────────────────────
# CLI ENTRY
# ─────────────────────────────────────────────

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python projection_adapter_v2.py '<query>'")
        sys.exit(1)

    query = sys.argv[1].strip()

    if len(query) < 3:
        print("Input too short.")
        sys.exit(1)

    result = generate_projection_bundle(query)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
