import json
import hashlib
from pathlib import Path

with open("ontology_hash.json") as f:
    stored = json.load(f)

for file, expected in stored.items():
    p = Path(file)

    if not p.exists():
        raise SystemExit(f"Missing canonical file: {file}")

    h = hashlib.sha256(p.read_bytes()).hexdigest()

    if h != expected:
        raise SystemExit(f"Ontology violation: {file} modified")

print("Canonical ontology intact.")
