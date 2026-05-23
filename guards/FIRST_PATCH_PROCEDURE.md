# VECTAETOS — First Guard Core Patch Procedure

## Goal

Start the hardened perimeter refactor with the smallest safe patch:

```text
guards/GUARD_PERIMETER_MODEL.md
guards/core/__init__.py
guards/core/findings.py
guards/core/reporting.py
```

## Boundary

This patch does not refactor active guards yet.
It only introduces the shared model path and shared reporting/finding primitives.

## Steps

```bash
mkdir -p guards/core

cp guards/VECTAETOS_PERIMETER_GUARD_MODEL_FINAL_HARDENED_UPGRADED.md guards/GUARD_PERIMETER_MODEL.md

# copy files from this patch into:
# guards/core/__init__.py
# guards/core/findings.py
# guards/core/reporting.py

python3 -m py_compile guards/core/findings.py guards/core/reporting.py

python3 - <<'PY'
from guards.core.findings import make_finding, Severity, Confidence, Scope, DriftVector
from guards.core.reporting import render_json, render_text_report

finding = make_finding(
    guard_id="GUARD-00",
    guard_file="guards/perimeter_kernel_guard.py",
    rule_id="P0-KERNEL-SMOKE",
    scope=Scope.P0_REPOSITORY,
    vector=DriftVector.V0_AUTHORITY_INFLATION,
    severity=Severity.INFO,
    confidence=Confidence.HIGH,
    path="guards/GUARD_PERIMETER_MODEL.md",
    message="Smoke test diagnostic only.",
    evidence_class_allowed="E1_static_scan",
)

print(render_json([finding]))
print(render_text_report([finding], title="Smoke", mode="report"))
PY

git diff -- guards/GUARD_PERIMETER_MODEL.md guards/core

git add guards/GUARD_PERIMETER_MODEL.md guards/core/__init__.py guards/core/findings.py guards/core/reporting.py
git commit -m "Introduce shared guard finding and reporting core"
git push
```

## Expected result

```text
No active guard behavior changes yet.
No ontology claim introduced.
New shared schema is ready for GUARD-12 / GUARD-01 / GUARD-03 refactor.
```
