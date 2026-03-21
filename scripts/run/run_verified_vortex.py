import json
import hashlib
import subprocess
import sys
import os

# ===== CONFIG =====
SEED = "42"
ARTIFACT_DIR = "artifacts"

OUT1 = f"{ARTIFACT_DIR}/run1.json"
OUT2 = f"{ARTIFACT_DIR}/run2.json"

BANNED = [
    "you are",
    "you want",
    "the user",
    "this means",
    "most precise",
    "i think",
    "it seems",
    "probably"
]

# ===== VORTEX PARSE =====

def run_vortex():
    result = subprocess.run(
        ["python", "vortex/vortex_v2.0.py", "--seed", SEED],
        capture_output=True,
        text=True
    )

    lines = result.stdout.split("\n")

    capture = False
    state_lines = []

    for line in lines:
        if "FINAL POLE STATES" in line:
            capture = True
            continue
        if "SIMULATION SUMMARY" in line:
            break
        if capture and line.strip():
            state_lines.append(line.strip())

    return state_lines


def normalize(state_lines):
    data = {}

    for line in state_lines:
        if ":" not in line:
            continue

        key, rest = line.split(":", 1)
        parts = rest.strip().split()

        values = {}
        for p in parts:
            if "=" in p:
                k, v = p.split("=")
                values[k] = round(float(v), 6)

        data[key.strip()] = values

    return data


def strict_check(text_lines):
    joined = " ".join(text_lines).lower()
    return [b for b in BANNED if b in joined]


def hash_data(data):
    s = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()


# ===== PIPELINE =====

def run_once(path):
    raw = run_vortex()

    # STRICT MODE
    violations = strict_check(raw)
    if violations:
        print("❌ STRICT FAIL:", violations)
        sys.exit(1)

    data = normalize(raw)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return data


def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    print("▶ RUN 1")
    d1 = run_once(OUT1)

    print("▶ RUN 2")
    d2 = run_once(OUT2)

    h1 = hash_data(d1)
    h2 = hash_data(d2)

    report = {
        "hash1": h1,
        "hash2": h2,
        "match": h1 == h2
    }

    with open(f"{ARTIFACT_DIR}/report.json", "w") as f:
        json.dump(report, f, indent=2)

    if h1 != h2:
        print("❌ NON-DETERMINISTIC")
        sys.exit(1)

    print("✅ VERIFIED")
    print("HASH:", h1)


if __name__ == "__main__":
    main()
