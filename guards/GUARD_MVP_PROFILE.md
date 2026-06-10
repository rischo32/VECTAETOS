# VECTAETOS™ — GUARD_MVP_PROFILE.md

**Status:** implementation baseline  
**Path:** `guards/GUARD_MVP_PROFILE.md`  
**Depends on:** `guards/GUARD_PERIMETER_MODEL.md`, `guards/MATICA_PERIMETER.md`  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Feedback into Φ:** none  
**Version:** v0.4-mvp-baseline  
**Date:** 2026-05-23  

---

## 0. Boundary

This document defines the smallest executable guard perimeter for VECTAETOS.

It is not a canonical ontology anchor.

It does not replace `GUARD_PERIMETER_MODEL.md`.

It does not replace `MATICA_PERIMETER.md`.

It selects the first operational subset from the full guard matrix.

```text
MVP perimeter = smallest executable protection surface
MVP perimeter ≠ full perimeter
MVP perimeter ≠ empirical proof
MVP perimeter ≠ deployment validation
```

Core invariant:

```text
Guard exponuje drift; nedefinuje pravdu.
```

---

## 1. Why MVP exists

The full matrix contains GUARD-00 through GUARD-30.

Implementing all guards before the shared kernel is stable would create fragmented enforcement.

The MVP exists to protect the highest-risk invariants first.

```text
smaller running perimeter > complete theoretical perimeter
```

Slovak:

```text
Menší guard systém, ktorý reálne beží, je silnejší než úplný perimeter, ktorý zostane teoretický.
```

---

## 2. MVP guard set

The first executable perimeter contains five guards:

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-12 coherence_vocabulary_guard.py
GUARD-20 release_claim_guard.py
```

These guards cover:

```text
root authority drift
canonical ontology mutation
code behavior mutation
semantic vocabulary conversion
release / evidence overclaim
```

---

## 3. MVP risk coverage

| Risk | Guard | Level | Status |
|---|---|---:|---|
| guard claims authority | GUARD-00 | 0 | planned |
| unsafe PASS / FAIL wording | GUARD-00 | 0 | planned |
| anchor modified silently | GUARD-01 | 0 | active/refac |
| canonical text drift | GUARD-01 | 0 | active/refac |
| Python mutates protected layer | GUARD-03 | 3 | active/refac |
| subprocess / network / exec drift | GUARD-03 | 3 | active/refac |
| κ becomes metric | GUARD-12 | 2 | planned |
| K(Φ) becomes score | GUARD-12 | 2 | planned |
| QE becomes error / fallback | GUARD-12 | 2 | planned |
| EK becomes authority | GUARD-12 | 2/4 | planned |
| release claims safety | GUARD-20 | 5 | planned |
| README badge overclaims evidence | GUARD-20 | 5 | planned |
| CI pass becomes proof | GUARD-20 | 5 | planned |

---

## 4. MVP guard roles

### GUARD-00 — perimeter_kernel_guard.py

Primary level:

```text
Level 0 — Fundamental Repository Perimeter
```

Role:

```text
enforce safe report language
validate shared finding shape
reject authority-inflating guard output
validate exit-code discipline
```

Must detect:

```text
ontology preserved
truth proven
deployment ready
VECTAETOS is safe
guard decides
CI proves safety
```

Must not:

```text
modify files
quarantine
auto-revert
interpret ontology
```

---

### GUARD-01 — canonical_ontology_guard.py

Primary level:

```text
Level 0 — Fundamental Repository Perimeter
```

Role:

```text
protect canonical anchors and high-risk canonical repository surfaces
```

Must detect:

```text
unauthorized canonical anchor changes
protected vocabulary mutation in changed files
path/status laundering around anchors
authority inflation in canonical files
```

Shared core target:

```text
findings.py
reporting.py
text_scan.py
paths.py
immutable_blob.py later
```

---

### GUARD-03 — vectaetos_code_behavior_audit.py

Primary level:

```text
Level 3 — Code Behavior Perimeter
```

Role:

```text
static AST audit of Python behavior against role capability boundaries
```

Must detect:

```text
dynamic execution
network calls
subprocess calls
uncontrolled randomness
file writes in protected roles
ontology-facing assignments
Vortex selection / optimization language in code
inter-guard coupling
```

Shared core target:

```text
ast_scan.py
roles.py
capabilities.py
findings.py
reporting.py
```

---

### GUARD-12 — coherence_vocabulary_guard.py

Primary level:

```text
Level 2 — Semantic / Ontological Vocabulary Perimeter
```

Role:

```text
broad semantic vocabulary boundary scanner
```

Must detect forbidden conversions:

```text
κ -> metric / threshold / score / parameter
K(Φ) -> score / reward / objective / optimization target
QE -> exception / fallback / error / failure
Vortex -> optimizer / selector / recommender
Projection -> interpretation / prescription
EK observable -> truth / safety / validation authority
```

Must be:

```text
negation-aware
meta-example-aware
contract-traced
deterministic
read-only
```

Shared core target:

```text
text_scan.py
contracts.py
findings.py
reporting.py
```

---

### GUARD-20 — release_claim_guard.py

Primary level:

```text
Level 5 — Runtime / Evidence / Release Perimeter
```

Role:

```text
protect public claims, release text, README badges, DOI language, and evidence posture
```

Must detect:

```text
CI pass means safety
static scan proves correctness
documentation proves empirical validation
single test proves universal safety
hash proves semantic truth
signature proves ontology
```

Shared core target:

```text
text_scan.py
contracts.py
findings.py
reporting.py
paths.py
```

---

## 5. MVP shared core requirement

MVP guards must emit the same `Finding` shape.

Required core:

```text
guards/core/findings.py
guards/core/reporting.py
guards/core/text_scan.py
guards/core/contracts.py
guards/core/paths.py
guards/core/roles.py
guards/core/capabilities.py
guards/core/ast_scan.py
```

Optional for MVP phase 1:

```text
guards/core/immutable_blob.py
```

`immutable_blob.py` is already useful, but full anchor manifest enforcement can remain phase 2 if manifests are not ready.

---

## 6. MVP execution order

Recommended strict order:

```text
1. GUARD-00 perimeter kernel
2. GUARD-01 canonical ontology guard
3. GUARD-12 coherence vocabulary guard
4. GUARD-03 code behavior audit
5. GUARD-20 release claim guard
```

Reason:

```text
kernel defines output boundary
canonical guard protects root
vocabulary guard blocks semantic conversion
code guard blocks behavior mutation
release guard blocks public overclaim
```

Alternative local order:

```text
1. GUARD-12
2. GUARD-03
3. GUARD-01
4. GUARD-20
5. GUARD-00
```

Use this alternative only during refactor when GUARD-00 is not implemented yet.

---

## 7. MVP enforcement profile

Initial profile:

```yaml
default_mode: report
strict_on:
  - protected canonical files
  - release claims
  - dynamic execution in guard code
  - ontology-facing assignments
  - κ / K(Φ) / QE forbidden conversions
```

CI profile after stabilization:

```yaml
default_mode: strict
fail_on:
  - BLOCKER
allow_warn:
  - experimental guard findings
  - fixture-marked must-warn cases
  - known migration warnings
```

---

## 8. MVP fixtures

Every MVP guard needs fixtures:

```text
tests/guards/fixtures/must_pass/
tests/guards/fixtures/must_warn/
tests/guards/fixtures/must_fail/
```

Fixture policy:

```text
must_pass  = no blocker
must_warn  = warning expected
must_fail  = exact rule_id expected
```

Required MVP fixture cases:

```text
κ is not a metric                           -> must_pass
κ_score = 0.84                              -> must_fail
QE is not an exception                      -> must_pass
class QEExceptionHandler                    -> must_fail or warn by role
CI pass is not empirical proof              -> must_pass
CI pass proves safety                       -> must_fail
Projection does not interpret               -> must_pass
Projection interprets meaning               -> must_fail
```

---

## 9. MVP stop conditions

Stop refactor if any MVP guard introduces:

```text
auto-fix for ontology-facing text
auto-revert
auto-quarantine
network call
hidden external state
runtime import of target source
guard output as authority
contract as ontology
hash as truth
CI pass as safety
feedback into Φ
```

---

## 10. MVP relation to full matrix

MVP does not remove the full matrix.

It creates the first runnable perimeter slice.

Full expansion resumes after MVP passes.

Next expansion after MVP:

```text
GUARD-19 repo_path_guard.py
GUARD-22 contract_traceability_guard.py
GUARD-24 anchor_blob_integrity_guard.py
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
```

---

## 11. Commit strategy

Recommended commit sequence:

```text
1. Add GUARD_MVP_PROFILE.md
2. Update guards/README.md to reference model + matrix + MVP
3. Refactor GUARD-12
4. Add GUARD-12 fixtures
5. Refactor GUARD-01
6. Refactor GUARD-03
7. Add GUARD-20
8. Add GUARD-00
```

Do not bundle all changes into one commit.

---

## 12. Final posture

```text
MVP means first executable perimeter.
It does not mean complete safety.
```

Slovak:

```text
MVP znamená prvý spustiteľný perimeter.
Neznamená úplnú bezpečnosť.
```

End.
