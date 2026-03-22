import json
import os
from datetime import datetime

# IMPORT — MUSÍ sedieť s názvom súboru
from vortex.vortex_v1_2_3 import VectaetosSimulation, VortexConfig


OUTPUT_DIR = "artifacts"
JSONL_PATH = os.path.join(OUTPUT_DIR, "multi_run.jsonl")
JSON_PATH = os.path.join(OUTPUT_DIR, "multi_run.json")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_single(seed: int, steps: int = 500):
    config = VortexConfig(
        steps=steps,
        seed=seed,
        epistemic_crypto=True,
        qe_detection=True
    )

    sim = VectaetosSimulation(config)
    result = sim.run()

    return result


def aggregate_runs(runs):
    """
    jednoduchý agregát — priemer posledného stavu
    """
    n = len(runs)

    agg = {
        "timestamp": datetime.utcnow().isoformat(),
        "runs": n,
        "singularities": [],
        "epistemic": {}
    }

    # predpoklad: poles = list[8] dictov
    poles_matrix = [r["poles"] for r in runs]

    for i in range(8):
        E = sum(poles_matrix[j][i]["E"] for j in range(n)) / n
        C = sum(poles_matrix[j][i]["C"] for j in range(n)) / n
        T = sum(poles_matrix[j][i]["T"] for j in range(n)) / n
        M = sum(poles_matrix[j][i]["M"] for j in range(n)) / n
        S = sum(poles_matrix[j][i]["S"] for j in range(n)) / n

        agg["singularities"].append({
            "Σ": i + 1,
            "E": round(E, 3),
            "C": round(C, 3),
            "T": round(T, 3),
            "M": round(M, 3),
            "S": round(S, 3),
        })

    # epistemic agregácia (len z prvého runu pre stabilitu)
    e = runs[-1].get("epistemic", {})

    agg["epistemic"] = {
        "qe": runs[-1].get("qe_aporia", {}).get("aporia", False),
        "h": round(e.get("topological_humidity", 0.0), 4),
        "asymmetry": round(e.get("total_asymmetry", 0.0), 4),
        "integrity": 1.0 if e.get("integrity", True) else 0.0,
        "triality": "OK" if e.get("triality_preserved", True) else "FAIL"
    }

    return agg


def main():
    ensure_output_dir()

    seeds = [42, 43, 44, 45]  # multi-trajectories
    runs = []

    for seed in seeds:
        result = run_single(seed)
        runs.append(result)

        # append do JSONL (história)
        with open(JSONL_PATH, "a") as f:
            f.write(json.dumps(result) + "\n")

    # agregácia → snapshot
    aggregated = aggregate_runs(runs)

    with open(JSON_PATH, "w") as f:
        json.dump(aggregated, f, indent=2)

    print("✔ multi-run complete")
    print(f"→ {JSONL_PATH}")
    print(f"→ {JSON_PATH}")


if __name__ == "__main__":
    main()
