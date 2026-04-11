import os
import json
from statistics import mean

from vortex.vortex_v1_2_3 import VectaetosSimulation, VortexConfig


ARTIFACTS_DIR = "artifacts"
OUTPUT_FILE = "vortex_state.jsonl"


# =========================
# SINGLE RUN
# =========================
def run_single(seed: int, steps: int = 500):
    # reset output file → determinism + clean state
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    config = VortexConfig(
        steps=steps,
        seed=seed
    )

    sim = VectaetosSimulation(config)
    sim.run()

    if not os.path.exists(OUTPUT_FILE):
        raise FileNotFoundError(f"{OUTPUT_FILE} not found after run")

    with open(OUTPUT_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("Empty vortex_state.jsonl")
        last_line = lines[-1]

    result = json.loads(last_line)

    # uloženie jednotlivého runu
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(f"{ARTIFACTS_DIR}/run_{seed}.json", "w") as f:
        json.dump(result, f, indent=2)

    return result


# =========================
# AGGREGATION (FIXED)
# =========================
def aggregate(runs):
    keys = ["E", "C", "T", "M", "S"]

    def avg(key):
        values = []
        for r in runs:
            poles = r.get("poles", [])
            for p in poles:
                values.append(p.get(key, 0))
        return mean(values) if values else 0.0

    return {
        "E": avg("E"),
        "C": avg("C"),
        "T": avg("T"),
        "M": avg("M"),
        "S": avg("S"),
        "runs": len(runs)
    }


# =========================
# MAIN
# =========================
def main():
    seeds = list(range(42, 42 + 8))  # Σ1–Σ8 mapping

    runs = []
    for seed in seeds:
        result = run_single(seed)
        runs.append(result)

    aggregated = aggregate(runs)

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    with open(f"{ARTIFACTS_DIR}/multi_run.json", "w") as f:
        json.dump({
            "aggregated": aggregated,
            "runs": runs
        }, f, indent=2)

    print("Multi-run complete.")
    print(f"Saved → {ARTIFACTS_DIR}/multi_run.json")


if __name__ == "__main__":
    main()
