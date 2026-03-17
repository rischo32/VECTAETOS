# =========================================
# VECTAETOS :: OBSERVATORY METRICS
# Version: 2.0.0 (robust + merkle integrated)
# =========================================

import json
import os
import hashlib

# 🔗 Merkle import
from tetraglyph.epistemic_merkle import EpistemicMerkleLedger


INPUT_FILE = "observatory_output.json"
OUTPUT_FILE = "observatory_metrics.json"


# =========================================
# SAFE LOAD
# =========================================

def safe_load_json(path):
    if not os.path.exists(path):
        print(f"[WARN] Missing file: {path}")
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return None


# =========================================
# HASH (STATE FINGERPRINT)
# =========================================

def compute_state_hash(data):
    try:
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
    except Exception as e:
        print(f"[WARN] Hash generation failed: {e}")
        return None


# =========================================
# DEFAULT METRICS
# =========================================

def default_metrics():
    return {
        "status": "NO_DATA",
        "num_poles": 0,
        "topological_humility": None,
        "dominant_mode": None,
        "triality_preserved": None,
        "total_asymmetry": None,
        "state_hash": None,
        "merkle_root": None
    }


# =========================================
# BUILD METRICS
# =========================================

def build_metrics(data):

    poles = data.get("poles", [])
    epistemic = data.get("epistemic", {})

    state_hash = compute_state_hash(data)

    # 🌳 Merkle
    ledger = EpistemicMerkleLedger()

    if state_hash:
        ledger.append(state_hash)
        merkle_root = ledger.root()
    else:
        merkle_root = None

    return {
        "status": "OK",
        "num_poles": len(poles),
        "topological_humility": epistemic.get("topological_humility"),
        "dominant_mode": epistemic.get("dominant_mode"),
        "triality_preserved": epistemic.get("triality_preserved"),
        "total_asymmetry": epistemic.get("total_asymmetry"),
        "state_hash": state_hash,
        "merkle_root": merkle_root
    }


# =========================================
# MAIN
# =========================================

def main():

    data = safe_load_json(INPUT_FILE)

    if data is None:
        metrics = default_metrics()
    else:
        metrics = build_metrics(data)

    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(metrics, f, indent=2)

        print("[OK] Observatory metrics generated")

    except Exception as e:
        print("[CRITICAL] Failed to write metrics:", str(e))
        raise


if __name__ == "__main__":
    main()
