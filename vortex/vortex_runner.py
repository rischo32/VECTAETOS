import os
import json
from statistics import mean

from vortex.vortex_v1_2_3 import VectaetosSimulation, VortexConfig


ARTIFACTS_DIR = "artifacts"
OUTPUT_FILE = "vortex_state.jsonl"


def run_single(seed: int, steps: int = 500):
    config = VortexConfig(
        steps=steps,
        seed=seed
    )

    sim = VectaetosSimulation(config)
    sim.run()  # zapisuje do vortex_state.jsonl

    if not os.path.exists(OUTPUT_FILE):
        raise FileNotFoundError(f"{OUTPUT_FILE} not found after run")

    with open(OUTPUT_FILE, "r") as f:
        last_line = f.readlines()[-1]

    result = json.loads(last_line)

    # uložiť separátne pre audit
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(f"{ARTIFACTS_DIR}/run_{seed}.json", "w") as f:
        json.dump(result, f, indent=2)

    return result


def aggregate(runs):
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


def main():
    seeds = list(range(42, 42 + 8))  # 8 trajektórií (Σ1–Σ8)

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


if __name__ == "__main__":
    main()
