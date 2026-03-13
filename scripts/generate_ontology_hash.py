#!/usr/bin/env python3

import hashlib
import json
import base64
from pathlib import Path
import sha3


# -------------------------------
# Canonical ontology files
# -------------------------------

CANONICAL_FILES = [
    "formal/ZMYSEL.md"
]


# -------------------------------
# Hash helpers (Base64)
# -------------------------------

def sha256_hash_b64(data: bytes) -> str:
    h = hashlib.sha256(data).digest()
    return base64.b64encode(h).decode()


def keccak256_hash_b64(data: bytes) -> str:
    k = sha3.keccak_256()
    k.update(data)
    h = k.digest()
    return base64.b64encode(h).decode()


# -------------------------------
# Generate hashes
# -------------------------------

canonical_hashes = {}

for file in CANONICAL_FILES:

    path = Path(file)

    if not path.exists():
        raise SystemExit(f"Missing canonical file: {file}")

    data = path.read_bytes()

    canonical_hashes[file] = {
        "sha256": sha256_hash_b64(data),
        "keccak256": keccak256_hash_b64(data)
    }


# -------------------------------
# Merkle-like root hash
# -------------------------------

combined = "".join(
    canonical_hashes[f]["sha256"]
    for f in sorted(canonical_hashes)
).encode()


root_sha256 = base64.b64encode(
    hashlib.sha256(combined).digest()
).decode()


k = sha3.keccak_256()
k.update(combined)

root_keccak = base64.b64encode(
    k.digest()
).decode()


# -------------------------------
# Output JSON
# -------------------------------

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


print("Ontology hash generated:")
print(json.dumps(output, indent=2))
