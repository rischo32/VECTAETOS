#!/usr/bin/env python3

import sys
import json
from simulation_vortex_5D import VortexConfig, Sigma

# --------- SIMPLE STATE CLASSIFICATION ----------

def classify_sigma(s):
    """
    klasifikácia jedného uzla
    """
    if s.C < 0.3 and s.T > 0.7:
        return "QE"

    if s.C > 0.6 and s.T < 0.4:
        return "stable"

    return "unstable"


# --------- SIMULATION MOCK (LIGHT VERSION) ----------

def run_light_vortex(steps=50):
    """
    minimalistická simulácia bez zásahu do core
    """
    config = VortexConfig(steps=steps)

    sigmas = [Sigma.random_init(config) for _ in range(config.poles)]

    history = []

    for step in range(config.steps):
        snapshot = []

        for s in sigmas:
            # jednoduchá dynamika (NEINTERVENČNÁ)
            s.T += 0.01 - 0.02 * s.C
            s.C += 0.01 - 0.01 * s.T
            s.clamp(config)

            snapshot.append(classify_sigma(s))

        history.append(snapshot)

    return history


# --------- AGGREGATION ----------

def summarize(history):
    stable = 0
    unstable = 0
    qe = 0

    for step in history:
        for s in step:
            if s == "stable":
                stable += 1
            elif s == "unstable":
                unstable += 1
            elif s == "QE":
                qe += 1

    return stable, unstable, qe


# --------- MAIN ----------

def run(prompt: str):
    print("\nINPUT:")
    print(prompt)

    history = run_light_vortex()

    stable, unstable, qe = summarize(history)

    print("\nTRAJECTORY REPORT\n")

    print(f"stable:   {stable}")
    print(f"unstable: {unstable}")
    print(f"QE:       {qe}")

    print("\nINTERPRETATION:")
    if qe > stable:
        print("→ pole smeruje k apórii")
    elif stable > unstable:
        print("→ pole má stabilizačné trajektórie")
    else:
        print("→ pole je oscilujúce / nestabilné")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Použitie: python vortex_cli.py 'tvoj vstup'")
        sys.exit(1)

    run(sys.argv[1])
