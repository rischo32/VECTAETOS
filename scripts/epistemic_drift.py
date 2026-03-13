import json
from pathlib import Path

OBS_PATH = Path("docs/observatory.json")

def load_observatory():
    if not OBS_PATH.exists():
        return {"history": []}

    with open(OBS_PATH) as f:
        return json.load(f)


def drift_score(prev_hash, new_hash):
    if prev_hash == new_hash:
        return 0

    # jednoduchá Hamming distance
    diff = sum(a != b for a, b in zip(prev_hash, new_hash))
    return diff / len(prev_hash)


def main():

    data = load_observatory()
    history = data.get("history", [])

    if len(history) < 2:
        print("Not enough data for drift detection")
        return

    prev = history[-2]["root_hash"]["sha256"]
    new = history[-1]["root_hash"]["sha256"]

    score = drift_score(prev, new)

    print(f"Epistemic drift score: {score:.4f}")

    if score > 0.05:
        print("WARNING: Ontology drift detected")

if __name__ == "__main__":
    main()
