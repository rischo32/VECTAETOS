import json
import hashlib
import base64
from pathlib import Path


FORMAL_DIR = Path("formal")


def sha256_b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def sha3_256_b64(data):
    return base64.b64encode(hashlib.sha3_256(data).digest()).decode()


with open("ontology_hash.json") as f:
    reference = json.load(f)


for file, hashes in reference["canonical_files"].items():

    path = Path(file)

    if not path.exists():
        raise SystemExit(f"Missing canonical file: {file}")

    data = path.read_bytes()

    if sha256_b64(data) != hashes["sha256"]:
        raise SystemExit(f"Ontology drift detected in {file}")


print("Ontology integrity verified.")
