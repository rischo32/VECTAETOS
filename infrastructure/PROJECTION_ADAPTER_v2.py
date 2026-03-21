# ─────────────────────────────────────────────────────────────
# Projection Operators (Π)
# Non-deterministic, non-authoritative
# ─────────────────────────────────────────────────────────────

import random


def projection_local(signal: dict) -> dict:
    """Local curvature-inspired projection (proxy)."""
    weights = {k: abs(v) for k, v in signal.items()}
    total = sum(weights.values()) or 1.0
    return {k: weights[k] / total for k in weights}


def projection_cycle(signal: dict) -> dict:
    """Combinatorial projection (flat participation)."""
    n = len(signal)
    return {k: 1.0 / n for k in signal}


def projection_relax(signal: dict) -> dict:
    """Maximum entropy projection."""
    n = len(signal)
    return {k: 1.0 / n for k in signal}


def projection_rand(signal: dict) -> dict:
    """Random admissible projection."""
    values = [random.random() for _ in signal]
    total = sum(values)
    return {k: v / total for k, v in zip(signal.keys(), values)}


# ─────────────────────────────────────────────────────────────
# Projection Selector (NON-semantic, shallow)
# ─────────────────────────────────────────────────────────────

def select_projection_operator(text: str):
    text = text.lower()

    if any(w in text for w in ["neistota", "uncertain", "doubt"]):
        return projection_relax

    if any(w in text for w in ["konflikt", "napatie", "spor"]):
        return projection_local

    if any(w in text for w in ["nahodne", "random"]):
        return projection_rand

    return projection_cycle


# ─────────────────────────────────────────────────────────────
# Signal Extraction (very shallow proxy)
# ─────────────────────────────────────────────────────────────

def extract_signal(text: str) -> dict:
    """Non-semantic signal extraction."""
    base = {k: 1.0 for k in AXIOMS.keys()}

    if "zmysel" in text or "why" in text:
        base["VER"] += 0.5
        base["WIS"] += 0.3

    if "rozhodnutie" in text or "decision" in text:
        base["INT"] += 0.4
        base["LIB"] += 0.3

    if "konflikt" in text:
        base["REL"] += 0.6
        base["UNI"] -= 0.2

    return base


# ─────────────────────────────────────────────────────────────
# Main Projection Pipeline
# ─────────────────────────────────────────────────────────────

def generate_candidate_tensions(query_text: str) -> dict:
    """
    Generates candidate projection via Π operators.
    No epistemic authority.
    """

    signal = extract_signal(query_text)
    operator = select_projection_operator(query_text)

    distribution = operator(signal)

    return distribution
