# LICENSE INTEGRITY MANIFEST

## Purpose

`LICENSE_INTEGRITY_MANIFEST.sha256` is a byte-integrity map for the VECTAETOS license stack.

It is tamper-evidence only.

It does not decide legal validity, truth, ontology, safety, or deployment admissibility.

## Registry

The machine-readable license registry lives in:

```text
contracts/LICENSE_REGISTRY.json
```

## Generate

Run after all license files and the registry are final:

```bash
sha256sum \
  LICENSES/VCL-2.0.md \
  LICENSES/VTP-1.0.md \
  LICENSES/VNAL-1.1.md \
  LICENSES/VPL-1.0.md \
  LICENSES/AEPL-2.0-VECTAETOS.md \
  contracts/LICENSE_REGISTRY.json \
  > LICENSES/LICENSE_INTEGRITY_MANIFEST.sha256
```

## Verify

```bash
python3 guards/license_stack_guard.py --repo-root . --registry contracts/LICENSE_REGISTRY.json --mode report --no-require-hashes
python3 guards/license_stack_guard.py --repo-root . --registry contracts/LICENSE_REGISTRY.json --mode strict --require-hashes
```
