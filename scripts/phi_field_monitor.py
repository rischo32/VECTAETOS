import json
from pathlib import Path
from datetime import datetime

OBS_PATH = Path("docs/observatory.json")
FIELD_PATH = Path("docs/field_state.json")


def load_observatory():
    if not OBS_PATH.exists():
        return []

    with open(OBS_PATH) as f:
        data = json.load(f)

    if isinstance(data, dict):
        return data.get("history", [])

    return data


def compute_triality_balance(root_hash):
    # jednoduchý proxy metric
    digits = sum(c.isdigit() for c in root_hash)
    letters = sum(c.isalpha() for c in root_hash)

    if letters + digits == 0:
        return 0

    return digits / (letters + digits)


def compute_entropy(root_hash):
    unique = len(set(root_hash))
    return unique / len(root_hash)


def main():

    history = load_observatory()

    if not history:
        print("No observatory data")
        return

    root_hash = history[-1]["root_hash"]["sha256"]

    triality = compute_triality_balance(root_hash)
    entropy = compute_entropy(root_hash)

    field_state = {
        "timestamp": datetime.utcnow().isoformat(),
        "root_hash": root_hash,
        "triality_balance": triality,
        "vortex_entropy": entropy,
        "singularities": 8,
        "algebra": "so(8)"
    }

    FIELD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(FIELD_PATH, "w") as f:
        json.dump(field_state, f, indent=2)

    print("Φ field state updated")


if __name__ == "__main__":
    main()
