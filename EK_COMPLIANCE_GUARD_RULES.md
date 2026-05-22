# EK Compliance Guard Rules (OAAT)

Status: Draft Guard Pack v1 
Purpose: Define **machine-checkable** conditions that block forbidden EK interpretation patterns and misuse in OAAT outputs.

---

## 1. Scope
These guards validate output payloads that combine:
- Runic state (`field_state`, `system_k`)
- EK metrics (`h_topo`, `mu`, optional `mu_tot`, `A_tot`)
- ASI_MOD narrative + state assessment
- claim/evidence mapping

Implemented in code at:
- `/home/team/shared/vectaetos/implementation/ek_compliance_guards.py`

---

## 2. Guard Categories

### A) Telemetry Validity Guards
- **EKG-001..004**: enforce valid rune/system_k/h_topo ranges.
- **EKG-005..006**: enforce `mu` vector shape and numeric non-negativity.
- **EKG-007..008**: enforce `system_k` ↔ `field_state` consistency:
  - `system_k=0` ⇒ `field_state=⊘`
  - `system_k=1` ⇒ `field_state≠⊘`
- **EKG-009**: if `mu_tot` and `A_tot` are present, ensure `h_topo = mu_tot/(mu_tot+A_tot)`.

### B) Interpretation Consistency Guards
- **EKG-010**: confidence band must be in `{HIGH, MODERATE, LOW}`.
- **EKG-011**: clarity band must match `h_topo` band mapping:
  - `[0.00,0.20]` → `CRISP`
  - `(0.20,0.45]` → `STABLE_QUALIFIED`
  - `(0.45,0.70]` → `CONTESTED`
  - `(0.70,1.00]` → `OPAQUE`
- **EKG-012**: forbid `HIGH` confidence when `h_topo >= 0.71`.
- **EKG-013**: if `system_k=0`, `narrative_mode` must be `APORIA`.
- **EKG-014**: require non-empty `uncertainty` narrative section.

### C) Evidence Integrity Guards
- **EKG-015**: require non-empty `evidence_map`.
- **EKG-016..019**: each claim must include supported metric tokens; unsupported tokens are rejected.

Allowed metric token patterns:
- `h_topo`, `mu_tot`, `A_tot`, `SYSTEM_K`, `FIELD_STATE`
- `mu[i]` where `i ∈ [0..7]`
- `A[i,j]` where `i,j ∈ [0..7]`

### D) Forbidden Misuse Language Guards
- **EKG-020**: reject absolute safety language (`risk-free`, `zero risk`, `guaranteed secure`, etc.).
- **EKG-021**: reject autonomous remediation claims.
- **EKG-022**: reject imperative prescriptive language (`you must`, `must immediately`, etc.).
- **EKG-023**: reject overconfident certainty language in contested/opaque bands (`h_topo >= 0.46`).
- **EKG-024**: reject stability claims when `system_k=0`.

---

## 3. Enforcement Outcome
Guard evaluation returns:
- `compliant: bool`
- `violation_count: int`
- `violations: [{code, severity, message, path}]`

This supports hard-fail gating in CI/CD or runtime response filters.

---

## 4. Intended Use in OAAT
1. ASIMULATOR/ASI_MOD produces output payload.
2. EK compliance checker evaluates payload.
3. If non-compliant, payload is blocked or rewritten with bounded-failure narrative.
4. Violations are logged as tamper-evident audit records.

These guards preserve OAAT separation-of-concerns by preventing dialogue-layer overreach and EK misinterpretation inflation.
