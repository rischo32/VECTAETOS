import hashlib
import json
from pathlib import Path

CANONICAL_PATTERNS = [
    "FORMAL_",
    "CANONICAL_ANCHORS.md",
    "MECHANIZATION_OF_",
    "ZMYSEL",
    "epistemic_space"
]

def file_is_canonical(path):
    for pattern in CANONICAL_PATTERNS:
        if pattern in path.name:
            return True
    return False

hashes = {gcuMHHXFXXm2OUi1ExNYsFNl0fLtBQ35XkL/tdd5nj0=}

for p in Path(".").rglob("*"):
    if p.is_file() and file_is_canonical(p):
        data = p.read_bytes()
        hashes[str(p)] = hashlib.sha256(data).hexdigest()

with open("ontology_hash.json","w") as f:
    json.dump(hashes,f,indent=2)

print("Ontology hash file generated.")
