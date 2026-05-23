# VECTAETOS — Text Scan Core Patch Procedure

## Goal

Add the next shared core module:

```text
guards/core/text_scan.py
```

Optionally update:

```text
guards/core/README.md
```

## Boundary

This patch does not refactor active guards yet.

It only adds the shared text scanning primitives needed by future GUARD-12 and later text-guard refactors.

## Steps

```bash
# 1. Copy the file into repo
cp /path/from/patch/guards/core/text_scan.py guards/core/text_scan.py

# 2. Optionally update guards/core/README.md with README_TEXT_SCAN_UPDATE.md

# 3. Compile
python3 -m py_compile guards/core/findings.py guards/core/reporting.py guards/core/text_scan.py

# 4. Smoke test
python3 - <<'PY'
from guards.core.findings import Scope, DriftVector, Severity
from guards.core.text_scan import make_rule, scan_text_to_findings
from guards.core.reporting import render_text_report

rule = make_rule(
    rule_id="FC-KAPPA-METRIC",
    pattern=r"\\b(κ|kappa)\\b.{0,80}\\b(metric|score|threshold|parameter)\\b",
    message="Pattern appears to convert κ into metric/score/threshold/parameter language.",
    scope=Scope.P1_SEMANTIC_VOCABULARY,
    vector=DriftVector.V3_FORBIDDEN_CONVERSION,
    severity=Severity.BLOCKER,
    protected_object="κ",
    forbidden_conversion="κ -> metric/score/threshold/parameter",
)

text = '''
κ is not a metric.
κ_score = 0.84
Forbidden example: κ -> metric
'''

findings = scan_text_to_findings(
    path="example.md",
    text=text,
    rules=[rule],
    guard_id="GUARD-12",
    guard_file="guards/coherence_vocabulary_guard.py",
)

print(render_text_report(findings, title="Text scan smoke", mode="report"))
PY

# 5. Review
git diff -- guards/core/text_scan.py guards/core/README.md

# 6. Commit
git add guards/core/text_scan.py guards/core/README.md
git commit -m "Add shared guard text scan core"
git push
```

## Expected behavior

```text
"κ is not a metric" is skipped as negated-safe context.
"κ_score = 0.84" is emitted as a finding.
"Forbidden example: κ -> metric" is skipped as meta-example context.
```
