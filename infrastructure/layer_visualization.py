#!/usr/bin/env python3
"""
VECTAETOS :: LAYER VISUALIZATION

Epistemic Rendering Layer (ERL)

- Non-agentic
- Non-interventional
- Descriptive only

Vizualizuje stav Φ bez interpretácie.
"""

from typing import Dict, List, Optional


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _bar(value: float, width: int = 10) -> str:
    value = max(0.0, min(1.0, value))
    filled = int(value * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def _intensity(val: float) -> str:
    if val > 0.9:
        return "█"
    elif val > 0.7:
        return "▓"
    elif val > 0.4:
        return "▒"
    elif val > 0.1:
        return "░"
    else:
        return "."


# ============================================================
# FIELD STATE
# ============================================================

def visualize_field_state(state: Dict) -> str:
    lines = []

    epi = state.get("epistemic", {})
    ltl = epi.get("LTL", "?")

    lines.append(f"Φ STATE | LTL={ltl}")
    lines.append("=" * 40)

    poles = state.get("poles", [])
    mu = epi.get("mu", [])

    for i, pole in enumerate(poles):
        C = pole.get("C", 0.0)
        m = mu[i] if i < len(mu) else 0.0

        lines.append(
            f"Σ{i}: C={C:.2f} | μ={m:.2f} | {_bar(C)}"
        )

    return "\n".join(lines)


# ============================================================
# RELATIONAL MAP
# ============================================================

def visualize_relations(A: List[List[float]]) -> str:
    if not A:
        return ""

    lines = []
    lines.append("RELATIONAL MAP (|R_ij|)")
    lines.append("=" * 40)

    n = len(A)

    for i in range(n):
        row = []
        for j in range(n):
            row.append(_intensity(abs(A[i][j])))
        lines.append(" ".join(row))

    return "\n".join(lines)


# ============================================================
# ENTROPY / DISTRIBUTION
# ============================================================

def visualize_distribution(M: List[float]) -> str:
    if not M:
        return ""

    lines = []
    lines.append("DISTRIBUTION (M)")
    lines.append("=" * 40)

    total = sum(M) if sum(M) > 0 else 1.0

    for i, m in enumerate(M):
        p = m / total
        lines.append(f"{i:02d}: {_bar(p, 20)} {p:.3f}")

    return "\n".join(lines)


# ============================================================
# TEMPORAL TRACE
# ============================================================

def visualize_temporal(history: List[Dict]) -> str:
    if not history:
        return ""

    lines = []
    lines.append("TEMPORAL TRACE (h)")
    lines.append("=" * 40)

    for state in history[-20:]:
        epi = state.get("epistemic", {})
        h = epi.get("topological_humility", 0.5)
        ltl = epi.get("LTL", "?")

        lines.append(f"{ltl:>5}: {_bar(h, 20)} {h:.3f}")

    return "\n".join(lines)


# ============================================================
# MASTER RENDER
# ============================================================

def render_full_state(state: Dict, history: Optional[List[Dict]] = None) -> str:
    blocks = []

    blocks.append(visualize_field_state(state))

    A = state.get("epistemic", {}).get("A_matrix", [])
    rel = visualize_relations(A)
    if rel:
        blocks.append(rel)

    M = state.get("epistemic", {}).get("M_distribution", [])
    dist = visualize_distribution(M)
    if dist:
        blocks.append(dist)

    if history:
        temp = visualize_temporal(history)
        if temp:
            blocks.append(temp)

    return "\n\n".join(blocks)


# ============================================================
# CLI (optional live monitor)
# ============================================================

if __name__ == "__main__":
    import json
    import time

    FILE = "vortex_state.jsonl"

    def load_last():
        try:
            with open(FILE, "r") as f:
                lines = f.readlines()
                return json.loads(lines[-1]) if lines else {}
        except:
            return {}

    try:
        while True:
            state = load_last()
            print("\033c", end="")  # clear terminal
            print(render_full_state(state))
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopped.")
