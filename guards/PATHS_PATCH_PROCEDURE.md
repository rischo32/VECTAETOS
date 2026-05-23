# VECTAETOS — Paths Core Patch Procedure

## Goal

Add:

```text
guards/core/paths.py
```

This prepares future repo path guard, path-policy contracts, and cleaner refactors of text/code guards.

## Boundary

This patch is read-only.

It classifies paths but does not globally exclude repository areas and does not define ontology.

## Steps

```bash
cp /path/from/patch/guards/core/paths.py guards/core/paths.py

# optionally update guards/core/README.md with README_PATHS_UPDATE.md

python3 -m py_compile \
  guards/core/findings.py \
  guards/core/reporting.py \
  guards/core/text_scan.py \
  guards/core/immutable_blob.py \
  guards/core/contracts.py \
  guards/core/paths.py
```

## Smoke test

```bash
python3 - <<'PY'
from guards.core.paths import describe_path, validate_repo_path
from guards.core.reporting import render_text_report

for path in [
    "anchors/CORE.md",
    "guards/core/findings.py",
    "contracts/perimeters/p1.json",
    "tests/guards/fixtures/must_fail/example.md",
    "../escape.md",
]:
    print(describe_path(path))

print(render_text_report(
    validate_repo_path("../escape.md"),
    title="Path smoke",
    mode="report",
))
PY
```

## Expected

```text
anchors/CORE.md → role=anchor
guards/core/findings.py → role=guard_core
contracts/perimeters/p1.json → role=contract
tests/.../fixtures/... → role=fixture
../escape.md → PATH-INVALID finding
```

## Commit

```bash
git add guards/core/paths.py guards/core/README.md
git commit -m "Add shared guard path core"
git push
```
