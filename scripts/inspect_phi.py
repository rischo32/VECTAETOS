#!/usr/bin/env python3

import json
from pathlib import Path

DATA_PATH = Path("artifacts/multi_run.json")


def load():
    if not DATA_PATH.exists():
        print("❌ multi_run.json not found")
        return None

    with open(DATA_PATH) as f:
        return json.load(f)


def show_aggregate(data):
    agg = data.get("aggregated", {})

    print("\n=== Φ AGGREGATE ===")
    for k, v in agg.items():
        print(f"{k}: {v}")


def show_runs(data):
    runs = data.get("runs", [])

    print("\n=== Φ RUNS ===")
    for i, r in enumerate(runs[:8], 1):
        p = r["poles"][0]  # zjednodušený výpis
        print(f"Σ{i} → E:{p['E']:.3f} C:{p['C']:.3f} T:{p['T']:.3f}")


def main():
    data = load()
    if not data:
        return

    show_aggregate(data)
    show_runs(data)


if __name__ == "__main__":
    main()
