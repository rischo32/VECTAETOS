# VECTAETOS — Immutable Blob Core Patch Procedure

## Goal

Add the next shared integrity core module:

```text
guards/core/immutable_blob.py
```

This is preparation for future:

```text
GUARD-24 anchor_blob_integrity_guard.py
```

but it does not implement GUARD-24 yet.

## Boundary

This patch is read-only.

It does not quarantine files, revert git commits, send webhooks, mutate anchors, or claim semantic truth.

## Steps

```bash
# 1. Copy the file into repo
cp /path/from/patch/guards/core/immutable_blob.py guards/core/immutable_blob.py

# 2. Optionally update guards/core/README.md with README_IMMUTABLE_BLOB_UPDATE.md

# 3. Compile
python3 -m py_compile \
  guards/core/findings.py \
  guards/core/reporting.py \
  guards/core/text_scan.py \
  guards/core/immutable_blob.py

# 4. Smoke test with a temporary manifest
python3 - <<'PY'
from pathlib import Path
import json
import tempfile

from guards.core.immutable_blob import (
    build_manifest,
    render_manifest_json,
    verify_manifest,
)
from guards.core.reporting import render_text_report

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "anchors").mkdir()
    target = root / "anchors" / "SMOKE.md"
    target.write_text("# smoke\n", encoding="utf-8")

    manifest = build_manifest(root=root, paths=["anchors/SMOKE.md"], include_sha3_512=True)
    manifest_path = root / "anchor_manifest.json"
    manifest_path.write_text(render_manifest_json(manifest), encoding="utf-8")

    clean = verify_manifest(root=root, manifest_path=manifest_path)
    print(render_text_report(clean, title="Immutable blob smoke clean", mode="report"))

    target.write_text("# changed\n", encoding="utf-8")
    findings = verify_manifest(root=root, manifest_path=manifest_path)
    print(render_text_report(findings, title="Immutable blob smoke changed", mode="report"))
PY

# 5. Review
git diff -- guards/core/immutable_blob.py guards/core/README.md

# 6. Commit
git add guards/core/immutable_blob.py guards/core/README.md
git commit -m "Add read-only immutable blob integrity core"
git push
```

## Expected behavior

```text
unchanged file → no findings
modified file → BLOB-SIZE-MISMATCH and/or BLOB-SHA256-MISMATCH
missing manifest → BLOB-MANIFEST-INVALID
missing file → BLOB-MISSING
```

## Do not add yet

```text
GUARD-24
self_verify.py
nuclear.py
external sentinel runner
signed manifests
```

Those come after this core module is stable.
