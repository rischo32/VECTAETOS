import json
import hashlib
import subprocess
import sys
import os

OUTPUT_1 = "artifacts/run_1.json"
OUTPUT_2 = "artifacts/run_2.json"


def run_simulation(output_path):
    # uprav podľa tvojho vortex entrypointu
    result = subprocess.run(
        ["python", "simulation_vortex_5d.py"],
        capture_output=True,
        text=True
    )

    # tu musíš uložiť výstup (prispôsob podľa projektu)
    with open(output_path, "w") as f:
        json.dump({"output": result.stdout}, f)


def normalize(data):
    # odstráň nestabilné veci
    return {
        "output": data["output"].strip()
    }


def hash_data(data):
    s = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()


def load(path):
    with open(path) as f:
        return json.load(f)


def main():
    os.makedirs("artifacts", exist_ok=True)

    print("▶ Run 1")
    run_simulation(OUTPUT_1)

    print("▶ Run 2")
    run_simulation(OUTPUT_2)

    d1 = normalize(load(OUTPUT_1))
    d2 = normalize(load(OUTPUT_2))

    h1 = hash_data(d1)
    h2 = hash_data(d2)

    report = {
        "hash_1": h1,
        "hash_2": h2,
        "match": h1 == h2
    }

    with open("artifacts/determinism_report.json", "w") as f:
        json.dump(report, f, indent=2)

    if h1 != h2:
        print("❌ NON-DETERMINISTIC")
        sys.exit(1)

    print("✅ DETERMINISTIC")


if __name__ == "__main__":
    main()
