#!/usr/bin/env python3
"""
VECTAETOS :: MULTI-TRAJECTORY VORTEX RUNNER
"""

from pathlib import Path
import json
import time
from statistics import mean, variance

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
    return sim.run()


def extract_metrics(result: dict):
    poles = result["final_state"]

    return {
        "E": mean(p["E"] for p in poles),
        "C": mean(p["C"] for p in poles),
        "T": mean(p["T"] for p in poles),
        "M": mean(p["M"] for p in poles),
        "S": mean(p["S"] for p in poles),
        "aporia_count": len(result.get("aporia_events", []))
    }


def run_multi(n: int = 8, steps: int = 1000):
    seeds = list(range(1, n + 1))

    metrics = []

    for s in seeds:
        res = run_single(seed=s, steps=steps)
        m = extract_metrics(res)
        metrics.append(m)

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
        "timestamp": int(time.time()),
        "meta": {
            "trajectories": n,
            "steps": steps
        },
        "aggregate": agg,
        "samples": metrics
    }


def save_snapshot(data: dict):
    path = ARTIFACTS / "multi_run.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def append_log(data: dict):
    path = ARTIFACTS / "run_2.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(data) + "\n")


def main():
    data = run_multi(n=8, steps=1000)

    snapshot_path = save_snapshot(data)
    append_log(data)

    print(f"[Φ] snapshot → {snapshot_path}")
    print(f"[Φ] log append → artifacts/run_2.jsonl")


if __name__ == "__main__":
    main()
