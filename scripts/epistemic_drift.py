import json
from pathlib import Path

OBS_PATH = Path("docs/observatory.json")


def load_observatory():
    if not OBS_PATH.exists():
        return []

    with open(OBS_PATH) as f:
        data = json.load(f)

    # observatory môže byť dict alebo list
    if isinstance(data, dict):
        return data.get("history", [])

    if isinstance(data, list):
        return data

    return []


def drift_score(a, b):
    diff = sum(x != y for x, y in zip(a, b))
    return diff / len(a)


def main():

    history = load_observatory()

    if len(history) < 2:
        print("Not enough data for drift detection")
        return

    prev_hash = history[-2]["root_hash"]["sha256"]
    new_hash = history[-1]["root_hash"]["sha256"]

    score = drift_score(prev_hash, new_hash)

    print(f"Epistemic drift score: {score:.6f}")

    if score > 0.05:
        print("WARNING: Ontology drift detected")


if __name__ == "__main__":
    main()
