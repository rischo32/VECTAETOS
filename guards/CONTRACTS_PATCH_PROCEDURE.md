# VECTAETOS — Contracts Core Patch Procedure

## Goal

Add:

```text
guards/core/contracts.py
```

This prepares future contract-traced guards without implementing GUARD-22 yet.

## Boundary

This patch is read-only.

It validates machine-readable contract shape. It does not define ontology and does not replace anchors.

## Steps

```bash
cp /path/from/patch/guards/core/contracts.py guards/core/contracts.py

# optionally update guards/core/README.md with README_CONTRACTS_UPDATE.md

python3 -m py_compile \
  guards/core/findings.py \
  guards/core/reporting.py \
  guards/core/text_scan.py \
  guards/core/immutable_blob.py \
  guards/core/contracts.py
```

## Smoke test

```bash
python3 - <<'PY'
from pathlib import Path
import tempfile
import json

from guards.core.contracts import validate_contract_file, load_contract
from guards.core.reporting import render_text_report

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    good = root / "p1_semantic_vocabulary.json"
    good.write_text(json.dumps({
        "schema_version": "1.0",
        "contract_role": "p1_semantic_vocabulary",
        "rules": [
            {
                "id": "FC-KAPPA-METRIC",
                "anchor_ref": "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md",
                "vector": "V3_forbidden_conversion",
                "scope": "P1_semantic_vocabulary",
                "evidence_class_allowed": "E1_static_scan",
                "enforcement_mode": "strict",
                "severity": "BLOCKER",
                "message": "κ must not be converted into metric/score/threshold language."
            }
        ]
    }, indent=2), encoding="utf-8")

    bad = root / "bad.json"
    bad.write_text(json.dumps({
        "schema_version": "1.0",
        "rules": [
            {
                "id": "BAD",
                "vector": "V3_forbidden_conversion"
            }
        ]
    }), encoding="utf-8")

    print(load_contract(good))
    print(render_text_report(
        validate_contract_file(bad),
        title="Contract smoke",
        mode="report",
    ))
PY
```

## Expected

```text
good contract loads
bad contract emits CONTRACT-INVALID finding
```

## Commit

```bash
git add guards/core/contracts.py guards/core/README.md
git commit -m "Add shared guard contract core"
git push
```
