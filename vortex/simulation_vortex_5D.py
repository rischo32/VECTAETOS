#!/usr/bin/env python3
# VECTAETOS — Φ Simulation Vortex (5D) — Deterministic Prototype
# E, C, T, M, S
# Outputs field_state.json for web projection

import json
import random

STATE_FILE = "field_state.json"
DT_STEPS = 1  # deterministický krok (žiadny real-time sleep)

# 🔒 determinism
SEED = 42
random.seed(SEED)

# Inicializácia stavu poľa
phi = {
    "E": 0.6,  # Energy
    "C": 0.7,  # Coherence
    "T": 0.2,  # Tension
    "M": 0.3,  # Memory
    "S": 0.1   # Entropy
}

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def compute_rune(phi):
    """
    ⚠️ PROTOTYPE ONLY
    Descriptive mapping — nie rozhodovací mechanizmus.
    """
    if phi["C"] < 0.25:
        return "ᛁ"   # rozpad
    if phi["T"] > 0.7:
        return "ᚦ"   # tenzia
    if phi["C"] > 0.75:
        return "ᚱ"   # integrita
    if phi["S"] > 0.6:
        return "⊘"   # QE / apória
    return "ᚨ"       # otvorené pole

def step_phi(phi):
    """
    Deterministická evolúcia (pseudo-stochastická cez seed)
    """
    phi["T"] += random.uniform(-0.02, 0.02)
    phi["C"] += (0.01 - phi["T"] * 0.015)
    phi["S"] += abs(phi["T"]) * 0.01
    phi["M"] += 0.005 * (1 - phi["M"])

    for k in phi:
        phi[k] = clamp(phi[k])

    return phi

def run(steps=100):
    results = []

    for step in range(steps):
        step_phi(phi)
        rune = compute_rune(phi)

        out = {
            "step": step,
            "phi": dict(phi),
            "rune": rune
        }

        results.append(out)

    return results

def main():
    data = run(steps=100)

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
