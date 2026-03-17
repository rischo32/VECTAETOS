# =========================================
# VECTAETOS :: OBSERVATORY METRICS
# Version: 1.1.0 (robust + no-fail)
# =========================================

import json
import os

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
# DEFAULT METRICS (fallback)
# =========================================

def default_metrics():
    return {
        "status": "NO_DATA",
        "num_poles": 0,
        "topological_humility": None,
        "dominant_mode": None,
        "triality_preserved": None,
        "total_asymmetry": None,
        "merkle_root": None
    }


# =========================================
# MAIN
# =========================================

def main():

    data = safe_load_json(INPUT_FILE)

    if data is None:
        metrics = default_metrics()

    else:
        poles = data.get("poles", [])
        epistemic = data.get("epistemic", {})

        metrics = {
            "status": "OK",
            "num_poles": len(poles),
            "topological_humility": epistemic.get("topological_humility"),
            "dominant_mode": epistemic.get("dominant_mode"),
            "triality_preserved": epistemic.get("triality_preserved"),
            "total_asymmetry": epistemic.get("total_asymmetry"),
            "merkle_root": None  # zatiaľ placeholder
        }

    # uloženie vždy (nikdy nespadne)
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(metrics, f, indent=2)

        print("[OK] Observatory metrics generated")

    except Exception as e:
        print("[CRITICAL] Failed to write metrics:", str(e))
        raise


if __name__ == "__main__":
    main()
