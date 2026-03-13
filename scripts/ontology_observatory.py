#!/usr/bin/env python3

import json
import time
from pathlib import Path

OBSERVATORY_FILE = Path("docs/observatory.json")
ONTOLOGY_HASH = Path("ontology_hash.json")


if not ONTOLOGY_HASH.exists():
    raise SystemExit("ontology_hash.json not found")


with open(ONTOLOGY_HASH) as f:
    ontology = json.load(f)


root_sha256 = ontology["root_hash"]["sha256"]
root_sha3 = ontology["root_hash"]["sha3_256"]


entry = {
    "timestamp": int(time.time()),
    "root_sha256": root_sha256,
    "root_sha3": root_sha3,
    "singularities": ontology["invariant"]["singularities"],
    "algebra": ontology["invariant"]["algebra"],
    "triality": ontology["invariant"]["triality"]
}


history = []

if OBSERVATORY_FILE.exists():
    with open(OBSERVATORY_FILE) as f:
        history = json.load(f)


history.append(entry)


OBSERVATORY_FILE.parent.mkdir(exist_ok=True)


with open(OBSERVATORY_FILE, "w") as f:
    json.dump(history, f, indent=2)


print("Epistemic Observatory updated.")
