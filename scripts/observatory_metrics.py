# =========================================
# VECTAETOS :: OBSERVATORY METRICS
# Version: 2.0.0 (robust + merkle integrated)
# =========================================

import sys
import os
import json
import hashlib
from datetime import datetime

# 🔥 ROOT PATH FIX (kritické pre CI)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ✅ teraz už import funguje
from tetraglyph.epistemic_merkle import EpistemicMerkleLedger


INPUT_FILE = "observatory_output.json"
OUTPUT_FILE = "observatory_metrics.json"


def load_input(path):
    if not os.path.exists(path):
        print(f"[WARN] {path} not found → creating fallback")
        return {
            "runs": [],
            "status": "empty"
        }

    with open(path, "r") as f:
        return json.load(f)


def compute_basic_metrics(data):
    runs = data.get("runs", [])

    return {
        "run_count": len(runs),
        "status": data.get("status", "unknown"),
    }


def compute_hash(data):
    serialized = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(serialized).hexdigest()


def main():
    data = load_input(INPUT_FILE)

    metrics = compute_basic_metrics(data)

    # 🔐 Epistemic Merkle
    ledger = EpistemicMerkleLedger()

    for run in data.get("runs", []):
        ledger.add_leaf(json.dumps(run, sort_keys=True))

    merkle_root = ledger.get_root()

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "merkle_root": merkle_root,
        "data_hash": compute_hash(data),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print("[OK] Observatory metrics generated")
    print(f"Merkle root: {merkle_root}")


if __name__ == "__main__":
    main()
