#!/usr/bin/env python3
"""
VECTAETOS :: MULTI-TRAJECTORY VORTEX RUNNER

- wrapper nad vortex_v1.2.3.py
- generuje N trajektórií (seed sweep)
- NEVYBERÁ, NEOPTIMALIZUJE
- exportuje agregovanú projekciu
"""

from pathlib import Path
import json
from copy import deepcopy
from statistics import mean, variance

# IMPORT CORE (explicitne, žiadne hádanie)
from vortex.vortex_v1_2_3 import VectaetosSimulation, VortexConfig


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def run_single(seed: int, steps: int = 1000):
    cfg = VortexConfig(
        steps=steps,
        seed=seed,
        verbose=False
    )
    sim = VectaetosSimulation(cfg)
    result = sim.run()
    return result


def extract_metrics(result: dict):
    poles = result["final_state"]

    E = mean(p["E"] for p in poles)
    C = mean(p["C"] for p in poles)
    T = mean(p["T"] for p in poles)
    M = mean(p["M"] for p in poles)
    S = mean(p["S"] for p in poles)

    return {
        "E": E,
        "C": C,
        "T": T,
        "M": M,
        "S": S,
        "aporia_count": len(result.get("aporia_events", []))
    }


def run_multi(n: int = 8, steps: int = 1000):
    seeds = list(range(1, n + 1))

    trajectories = []
    metrics = []

    for s in seeds:
        res = run_single(seed=s, steps=steps)
        m = extract_metrics(res)

        trajectories.append(res)
        metrics.append(m)

    # agregácia (bez výberu)
    agg = {
        "trajectories": n,
        "E_mean": mean(m["E"] for m in metrics),
        "C_mean": mean(m["C"] for m in metrics),
        "T_mean": mean(m["T"] for m in metrics),
        "M_mean": mean(m["M"] for m in metrics),
        "S_mean": mean(m["S"] for m in metrics),
        "T_var": variance(m["T"] for m in metrics) if n > 1 else 0.0,
        "aporia_total": sum(m["aporia_count"] for m in metrics),
    }

    return {
        "meta": {
            "trajectories": n,
            "steps": steps
        },
        "aggregate": agg,
        "samples": metrics
    }


def save_output(data: dict):
    path = ARTIFACTS / "multi_run.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def main():
    data = run_multi(n=8, steps=1000)
    path = save_output(data)
    print(f"[Φ multi] saved → {path}")


if __name__ == "__main__":
    main()
