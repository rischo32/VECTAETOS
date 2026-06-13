#!/usr/bin/env python3
"""Generate signed guard runtime manifest."""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
GUARDS_DIR = REPO_ROOT / "guards"

GUARD_FILES = [
    "GUARD-00_perimeter_kernel_guard.py",
    "GUARD-01_canonical_ontology_guard.py",
    "GUARD-12_coherence_vocabulary_guard.py",
    # ... all guards
]

def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "schema_version": "1.0",
    "manifest_id": "vectaetos-guard-runtime-manifest",
    "hash_algorithm": "sha256",
    "signature_algorithm": "ed25519",
    "repo_commit": "GIT_COMMIT_SHA_HERE",  # Replace at generation time
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "guards": [],
}

for guard_file in GUARD_FILES:
    guard_path = GUARDS_DIR / guard_file
    if guard_path.exists():
        manifest["guards"].append({
            "guard_id": guard_file.replace(".py", "").split("_", 1)[0],
            "path": f"guards/{guard_file}",
            "sha256": hash_file(guard_path),
            "perimeter": "P0_canonical_repository",  # Adjust per guard
            "vectors": ["V0_authority_inflation"],     # Adjust per guard
            "contract_refs": ["contracts/perimeter_kernel.yaml"],
            "allowed_dependencies": ["pydantic", "yaml"],
            "max_memory_mb": 512,
            "max_cpu_seconds": 30.0,
            "allow_network": False,
            "allow_subprocess": False,
            "write_paths": ["reports/", "logs/"],
        })

# Write manifest
manifest_path = GUARDS_DIR / "config" / "guard_runtime_manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))

print(f"Generated manifest: {manifest_path}")
print(f"Total guards: {len(manifest['guards'])}")

# TODO: Sign with Ed25519 private key
# sig = sign(manifest_path.read_bytes(), PRIVATE_KEY)
# (manifest_path.with_suffix('.sig')).write_bytes(sig)
