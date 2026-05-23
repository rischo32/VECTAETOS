# VECTAETOS™ Guard Core

**Path:** `guards/core/`  
**Status:** shared implementation core  
**Scope:** repository perimeter diagnostics only  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Feedback into Φ:** none  

---

## 0. Purpose

`guards/core/` contains shared helper modules for VECTAETOS repository guards.

Its role is to make guard outputs, reports, severity handling, and exit-code behavior consistent across all current and future guards.

It is not a new guard by itself.

It is not an ontology layer.

It is not a contract source.

It is not a replacement for anchors.

---

## 1. What this directory is

```text
guards/core/ = shared non-authoritative guard infrastructure
```

It provides reusable primitives for:

```text
finding schema
severity levels
confidence levels
drift-vector labels
perimeter scope labels
evidence-class labels
deterministic JSON rendering
human report rendering
safe PASS / FAIL wording
exit-code calculation
GitHub step-summary rendering
```

The intended flow is:

```text
individual guard detects pattern
    ↓
guard creates shared Finding
    ↓
reporting renders text / JSON / GitHub summary
    ↓
workflow receives deterministic exit code
```

---

## 2. What this directory is not

`guards/core/` must never become:

```text
ontology source
truth authority
decision layer
optimizer
controller
runtime agent
deployment validator
safety proof
empirical proof
Φ modifier
K(Φ) evaluator
κ estimator
QE resolver
Vortex selector
Projection interpreter
EK authority
```

Core modules may expose diagnostics.

They must not define meaning.

---

## 3. Current modules

### `findings.py`

Defines the shared `Finding` object and controlled enums.

It answers the question:

```text
What shape must a guard finding have?
```

Main responsibilities:

```text
one shared finding schema
required fields such as guard_id, rule_id, scope, vector, severity
stable diagnostic finding id
ontology_authority invariant
auto_fix_allowed invariant
path normalization
JSON-compatible conversion support
```

Important boundary:

```text
Finding = diagnostic record
Finding ≠ verdict
Finding ≠ truth claim
Finding ≠ metaphysical proof
```

### `reporting.py`

Defines deterministic rendering and exit-code mapping.

It answers the question:

```text
How should guard findings be rendered and when should CI fail?
```

Main responsibilities:

```text
stable finding ordering
JSON report rendering
human text report rendering
GitHub step-summary rendering
severity threshold handling
exit code calculation
safe PASS / FAIL language
```

Important boundary:

```text
Exit code = repository-state signal
Exit code ≠ truth value
CI failure ≠ metaphysical proof
CI pass ≠ empirical validation
```

---

## 4. Required Finding fields

Every refactored guard should eventually emit a shared finding with at least:

```yaml
guard_id: "GUARD-12"
guard_file: "guards/coherence_vocabulary_guard.py"
rule_id: "FC-KAPPA-METRIC"
contract_schema_version: "1.0"

scope: "P1_semantic_vocabulary"
vector: "V3_forbidden_conversion"
severity: "BLOCKER"
confidence: "high"

path: "formal/example.md"
message: "Pattern appears to convert κ into a metric."
ontology_authority: false
auto_fix_allowed: false
```

Mandatory posture:

```text
ontology_authority must always be false
auto_fix_allowed must default to false
rule_id must be stable
contract_schema_version must be present
```

---

## 5. Severity semantics

```text
INFO    = contextual note
WARN    = possible drift / review signal
HARD    = strong architectural violation
BLOCKER = repository-state refusal at strict enforcement
```

Severity is not truth.

Severity is not danger proof.

Severity is not deployment judgment.

---

## 6. Exit-code contract

Shared reporting uses this exit-code convention:

```text
0 = no findings at configured enforcement level
1 = blocker finding detected
2 = guard infrastructure failure / confidence unavailable
3 = invalid contract / missing anchor trace / invalid manifest signature
4 = invalid CLI usage
```

These exit codes are operational signals only.

They do not encode ontology, truth, safety, or empirical validation.

---

## 7. Safe report language

Allowed:

```text
PASS: No configured blocker was detected within the declared perimeter.
FAIL: Configured blocker detected within declared repository perimeter.
FAIL: Guard infrastructure error; confidence unavailable.
This is a repository-state result, not empirical validation.
```

Forbidden:

```text
PASS: ontology preserved.
PASS: VECTAETOS is safe.
PASS: semantic correctness proven.
PASS: deployment ready.
FAIL: ontology is false.
FAIL: truth invalidated.
```

---

## 8. Import rule

Individual guards should import from core only for shared infrastructure.

Allowed:

```python
from guards.core.findings import Finding, Severity, Confidence, Scope, DriftVector
from guards.core.reporting import render_json, render_text_report, exit_code_for
```

Forbidden:

```text
core importing individual guards
core selecting which guard is correct
core changing guard rules dynamically
core modifying repository files
core mutating Φ or any ontology-facing structure
```

Direction must remain:

```text
individual guard → guards/core
```

not:

```text
guards/core → individual guard authority
```

---

## 9. Refactor discipline

Existing guards should be migrated gradually.

Recommended order:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-01 canonical_ontology_guard.py
3. GUARD-03 vectaetos_code_behavior_audit.py
4. remaining text guards
5. future integrity / incident / supply-chain guards
```

Each refactor must preserve the guard’s intended perimeter and only standardize:

```text
finding shape
report rendering
exit-code behavior
safe wording
```

It must not silently change ontology, rule meaning, or enforcement scope.

---

## 10. Test expectation

Every core module must remain:

```text
Python 3.11+ compatible
standard-library only unless explicitly approved
deterministic
side-effect minimal
non-networked
non-agentic
non-authoritative
```

Minimum local checks:

```bash
python3 -m py_compile guards/core/findings.py guards/core/reporting.py
```

Smoke-test imports:

```bash
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
```

---

## 11. Final boundary sentence

```text
guards/core/ standardizes how guard diagnostics are represented and reported.
It does not decide what VECTAETOS is.
```

Slovak:

```text
guards/core/ zjednocuje spôsob, akým guardy zapisujú a hlásia diagnostiku.
Nerozhoduje, čo je VECTAETOS.
```
