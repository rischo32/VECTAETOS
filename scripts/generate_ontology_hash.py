#!/usr/bin/env python3

import hashlib
import json
import base64
from pathlib import Path


FORMAL_DIR = Path("formal")


def sha256_b64(data: bytes):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def sha3_256_b64(data: bytes):
    return base64.b64encode(hashlib.sha3_256(data).digest()).decode()


canonical_files = {}

for file in sorted(FORMAL_DIR.glob("*.md")):

    data = file.read_bytes()

    canonical_files[str(file)] = {
        "sha256": sha256_b64(data),
        "sha3_256": sha3_256_b64(data)
    }


combined = "".join(
    canonical_files[f]["sha256"]
    for f in sorted(canonical_files)
).encode()


root_sha256 = base64.b64encode(hashlib.sha256(combined).digest()).decode()
root_sha3 = base64.b64encode(hashlib.sha3_256(combined).digest()).decode()


output = {
    "ontology": "VECTAETOS",
    "version": "1.0",
    "invariant": {
        "singularities": 8,
        "algebra": "so(8)",
        "triality": True
    },
    "canonical_files": canonical_files,
    "root_hash": {
        "sha256": root_sha256,
        "sha3_256": root_sha3
    }
}


with open("ontology_hash.json", "w") as f:
    json.dump(output, f, indent=2)

print("Ontology Merkle root generated.")
