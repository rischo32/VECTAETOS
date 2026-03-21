#!/usr/bin/env python3
"""
VECTAETOS © — Projection Adapter (Non-Ontological)

STATUS:
- This file is NOT part of the epistemic field Φ.
- It does NOT compute Φ, K(Φ), κ, impulses, or decisions.
- It generates a candidate runic tension projection Π(Φ|Σ)
  using heuristic, non-authoritative mapping.

PURPOSE:
- Bridge between human textual input and visual / symbolic projection.
- Intended for UI, demos, and infrastructural mediation ONLY.

ONTOLOGICAL NOTICE:
- No result produced by this module has epistemic authority.
- All outputs are descriptive projections, not evaluations or answers.
"""

import sys
import json
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Axiomatic centers (Σ₁…Σ₈)
# Order is fixed and MUST NOT be reinterpreted
# ─────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────
# Projection Heuristic
# This does NOT analyze meaning.
# It produces a candidate tension configuration only.
# ─────────────────────────────────────────────────────────────

def generate_candidate_tensions(query_text: str) -> dict:
    """
    Generate a candidate tension vector Π(Φ|Σ)
    using simple, transparent heuristics.

    This function does NOT:
    - interpret truth
    - classify intent
    - optimize coherence
    """

    text = query_text.lower()

    # Neutral baseline (non-zero to avoid false calm)
    tensions = {key: 0.50 for key in AXIOMS.keys()}

    # Heuristic signals (explicitly shallow by design)

    if any(word in text for word in ["neviem", "neistota", "uncertain", "doubt"]):
        tensions["WIS"] = 0.82
        tensions["VER"] = 0.35

    if any(word in text for word in ["rozhodnutie", "decision", "volba", "choice"]):
        tensions["INT"] = 0.78
        tensions["LIB"] = 0.70

    if any(word in text for word in ["konflikt", "spor", "problem", "napatie"]):
        tensions["REL"] = 0.80
        tensions["UNI"] = 0.42

    if any(word in text for word in ["zmysel", "meaning", "preco", "why"]):
        tensions["VER"] = 0.75
        tensions["WIS"] = 0.68

    if any(word in text for word in ["tvorit", "create", "novy", "build"]):
        tensions["CRE"] = 0.77
        tensions["INT"] = max(tensions["INT"], 0.65)

    return tensions


# ─────────────────────────────────────────────────────────────
# Runic Projection (Textual)
# Not an explanation. Not an answer.
# ─────────────────────────────────────────────────────────────

def generate_projection_text(tensions: dict) -> str:
    """
    Produce a human-readable projection note.
    This is NOT an interpretation.
    """

    ordered = sorted(tensions.items(), key=lambda x: x[1], reverse=True)
    high = ordered[0]
    low = ordered[-1]

    return (
        "Projekcia poľa naznačuje zvýšené napätie medzi axiomatickými ťažiskami:\n\n"
        f"• {high[0]} ({AXIOMS[high[0]]}) — {high[1]*100:.0f}%\n"
        f"• {low[0]} ({AXIOMS[low[0]]}) — {low[1]*100:.0f}%\n\n"
        "Toto NIE JE odpoveď.\n"
        "Je to obraz vzťahov, ktoré sa aktivovali.\n\n"
        "Ak niečo chýba, nie je to riešenie —\n"
        "ale otázka, ktorá ešte nevznikla."
    )


# ─────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python projection_adapter.py '<query text>'")
        sys.exit(1)

    query = sys.argv[1].strip()

    if len(query) < 5:
        print("Input too short to generate a projection.")
        sys.exit(1)

    tensions = generate_candidate_tensions(query)
    projection = generate_projection_text(tensions)

    result = {
        "type": "runic_projection_candidate",
        "axioms": AXIOMS,
        "tensions": tensions,
        "projection": projection,
        "epistemic_status": "descriptive_only",
        "authority": "none",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
