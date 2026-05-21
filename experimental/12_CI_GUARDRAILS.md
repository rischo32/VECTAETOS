# CI Guardrails — VECTAETOS / OAAT

Status: Draft implementation plan  
Purpose: Mechanize non-agentic and layer-boundary constraints.

---

## 1. Ontology Guard

Reject changes introducing forbidden terms in canonical core unless explicitly whitelisted.

Forbidden in core:

```text
optimize
optimizer
reward
policy update
goal function
maximize
minimize
best action
preferred state
rank outputs
self-improve
autonomous agent
```

Allow only in:

- risk register
- negative examples
- guardrail documentation

---

## 2. Canonical Anchor Hash Lock

Canonical files must have hashes.

Downstream repositories reference hashes.

If canonical anchor changes:

- require major/minor version update
- require changelog
- require compatibility statement

---

## 3. Import Boundary Guard

Allowed direction:

```text
VECTAETOS → ASIMULATOR → ASI_MOD
```

Forbidden:

```text
ASI_MOD → VECTAETOS
ASIMULATOR → VECTAETOS as authority
ASI_MOD → ASIMULATOR as authority
audit → ontology
memory → Φ
projection → Φ
```

---

## 4. No Feedback Loop Guard

Static and runtime tests must reject:

```text
output → Φ
projection → Φ
audit → Φ
memory → Φ
web → ontology
dialogue → ontology
```

---

## 5. Non-Optimization Test

Search code for:

- argmax
- argmin
- reward
- loss.backward
- optimizer.step
- reinforcement
- policy_gradient
- train loop affecting Φ
- objective function in Vortex

---

## 6. QE Projection Guard

If QE marker is present, projection layer must not generate field content.

Allowed:

```text
NON_REPRESENTABILITY_MARKER
```

Forbidden:

```text
fallback answer
replacement answer
moral refusal framed as field result
corrective suggestion as ontology
```

---

## 7. Audit Read-Only Guard

Audit modules may write logs.

Audit modules must not write:

- R
- Φ
- Σ
- K
- 𝒟
- Vortex state
- projection decision

---

## 8. Assembly Manifest

Required file:

```text
assembly_manifest.json
```

Fields:

```json
{
  "root": "VECTAETOS",
  "modules": ["ASIMULATOR", "ASI_MOD"],
  "canonical_anchor_hashes": {},
  "valid_flow": ["VECTAETOS", "ASIMULATOR", "ASI_MOD"],
  "reverse_flow_allowed": false
}
```

---

## 9. Fail-Closed Boot

ASIMULATOR / ASI_MOD must fail if:

- VECTAETOS anchor unavailable
- hash mismatch
- invalid dependency direction
- assembly manifest missing
- empirical gate not satisfied for operative mode

---

## 10. CI Reports

Each PR should generate:

```text
ontology_guard_report.md
boundary_guard_report.md
non_optimization_report.md
qe_projection_report.md
audit_readonly_report.md
```
