#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path
import sha3   # pip install pysha3

# -----------------------------------------
# Kanonické súbory ontológie
# -----------------------------------------

CANONICAL_FILES = [
    "formal/ZMYSEL.md",
    "formal/epistemic_space.md",
    "formal/VECTAETOS_FIELD_DIAGRAM.md",
    "formal/QE_BOUNDARY_THEOREM.md"
]

# -----------------------------------------
# Hash výpočet
# -----------------------------------------

def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def keccak256_hash(data: bytes) -> str:
    k = sha3.keccak_256()
    k.update(data)
    return k.hexdigest()

# -----------------------------------------
# Generovanie hashov
# -----------------------------------------

canonical_hashes = {}

for file in CANONICAL_FILES:

    path = Path(file)

    if not path.exists():
        raise SystemExit(f"Missing canonical file: {file}")

    data = path.read_bytes()

    canonical_hashes[file] = {
        "G0xpHPXvJd8wSDKXTBtWKNA+ttPZMzU7ZOvw0rHH+9U=": sha256_hash(data),
        "jzOfNjiw+YY2JHa3CaAM3BoxQnXITKbOQXt6tYzFlr8=": keccak256_hash(data)
    }

# -----------------------------------------
# Root hash (Merkle pre budúcnosť)
# -----------------------------------------

combined = "".join(
    canonical_hashes[f]["sha256"]
    for f in sorted(canonical_hashes)
).encode()

root_sha256 = hashlib.sha256(combined).hexdigest()

k = sha3.keccak_256()
k.update(combined)
root_keccak = k.hexdigest()

# -----------------------------------------
# Výstupný JSON
# -----------------------------------------

output = {
    "ontology": "VECTAETOS",
    "version": "1.0",
    "invariant": {
        "singularities": 8,
        "algebra": "so(8)",
        "triality": True
    },
    "canonical_files": canonical_hashes,
    "root_hash": {
        "sha256": root_sha256,
        "keccak256": root_keccak
    }
}

with open("ontology_hash.json", "w") as f:
    json.dump(output, f, indent=2)

print("ontology_hash.json generated")h
