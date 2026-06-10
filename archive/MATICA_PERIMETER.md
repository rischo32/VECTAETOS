# VECTAETOS™ — MATICA_PERIMETER.md

**Status:** implementation matrix  
**Path:** `guards/MATICA_PERIMETER.md`  
**Replaces:** `GUARDS_TABLE_FINAL.md` as working table  
**Depends on:** `guards/GUARD_PERIMETER_MODEL.md`  
**Ontology authority:** none  
**Decision authority:** none  
**Feedback into Φ:** none  
**Version:** v0.4-draft-level-0-5  
**Date:** 2026-05-23  

---

## 0. Boundary

This document is the implementation matrix for VECTAETOS repository guards.

It is not a canonical ontology anchor.

It does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, ZMYSEL, or any canonical meaning.

It maps guards to:

```text
level × drift vector × evidence class × enforcement mode × integrity posture
```

Core invariant:

```text
Guard exponuje drift; nedefinuje pravdu.
```

---

## 1. Replacement note

`GUARDS_TABLE_FINAL.md` is treated as a source inventory / previous draft.

`guards/MATICA_PERIMETER.md` is the cleaned implementation matrix.

Main corrections:

```text
P0–P4 notation replaced by Level 0–5
GUARD-06 restored
GUARD-07 kept as Vortex non-agentic guard
GUARD-19 aligned with repo_path_guard.py
GUARD-22 aligned with contract_traceability_guard.py
GUARD-24 aligned with anchor_blob_integrity_guard.py
long prose moved out of table cells
```

---

## 2. Level index

```text
Level 0 — Fundamental Repository Perimeter
Level 1 — Specialized Ontological Perimeter
Level 2 — Semantic / Ontological Vocabulary Perimeter
Level 3 — Code Behavior Perimeter
Level 4 — Bridge / Projection / Trace Perimeter
Level 5 — Runtime / Evidence / Release Perimeter
```

---

## 3. Drift vectors

```text
V0  authority_inflation
V1  upward_mutation
V2  agency_injection
V3  forbidden_conversion
V4  evidence_overclaim
V5  nondeterminism
V6  path_status_laundering
V7  contract_drift
V8  negation_blindness
V9  silence_qe_coercion
V10 timing_side_channel
V11 inter_guard_coupling
V12 ontology_creep
V13 dependency_supply_chain
V14 anchor_integrity_drift
V15 guard_runtime_integrity
```

---

## 4. Evidence classes

```text
E0 text claim
E1 static scan
E2 AST / contract compliance
E3 deterministic test suite
E4 empirical validation
E5 external replication
E6 independent audit
E7 formal guard verification
```

Evidence class is a claim limit.

It is not a truth rank.

---

## 5. Status legend

```text
ACTIVE       implemented or already used in guard perimeter
PLANNED      named guard, not yet implemented
CORE_READY   shared core already exists for this guard family
REFAC        existing guard needs shared-core refactor
MVP          candidate for first executable perimeter
```

---

## 6. Guard matrix

| ID | Guard file | Level | Vectors | Evidence | Mode | Posture | Status | Role |
|---|---|---:|---|---|---|---|---|---|
| GUARD-00 | `perimeter_kernel_guard.py` | 0 | V0,V1,V14,V15 | E1 | strict | kernel | PLANNED,MVP | perimeter kernel |
| GUARD-01 | `canonical_ontology_guard.py` | 0 | V0,V1,V7,V14 | E1 | strict | anchors | ACTIVE,REFAC,MVP | canonical boundary |
| GUARD-02 | `vectaetos_boundary_guard.py` | 0 | V1,V6,V7 | E1 | strict | layer boundary | PLANNED | repo boundary |
| GUARD-03 | `vectaetos_code_behavior_audit.py` | 3 | V1,V2,V5,V11,V12 | E2 | strict | AST | ACTIVE,REFAC,MVP | code behavior |
| GUARD-04 | `empirical_claim_guard.py` | 5 | V4,V5 | E1,E3 | strict | evidence | PLANNED | claim boundary |
| GUARD-05 | `repo_layer_boundary_guard.py` | 0 | V6,V7 | E1 | strict | paths | PLANNED | layer shape |
| GUARD-06 | `no_feedback_loop_guard.py` | 1 | V2,V11 | E0,E1 | strict | non-feedback | PLANNED | feedback block |
| GUARD-07 | `vortex_non_agentic_guard.py` | 1 | V2,V3,V5 | E0,E1 | strict | vortex boundary | ACTIVE,REFAC | vortex non-agentic |
| GUARD-08 | `qe_aporia_guard.py` | 1 | V3,V8,V9 | E0,E1 | strict | QE boundary | ACTIVE,REFAC | QE aporia |
| GUARD-09 | `triality_guard.py` | 1 | V2,V3,V9 | E0,E1 | strict | triality | ACTIVE,REFAC | triality boundary |
| GUARD-10 | `vector_drift_guard.py` | 2 | V3,V8,V12 | E0,E1 | report | vocabulary | ACTIVE,REFAC | vector terms |
| GUARD-11 | `master_index_router_guard.py` | 0 | V1,V6,V7 | E1 | strict | router | ACTIVE,REFAC | index router |
| GUARD-12 | `coherence_vocabulary_guard.py` | 2 | V3,V8,V9,V12 | E0,E1 | strict | vocabulary | PLANNED,MVP | coherence terms |
| GUARD-13 | `ek_observable_non_authority_guard.py` | 4 | V0,V3,V4 | E1,E2 | strict | EK read-only | PLANNED | EK observables |
| GUARD-14 | `bridge_phi_to_ek_guard.py` | 4 | V1,V3,V12 | E2 | strict | bridge | PLANNED | Φ→EK bridge |
| GUARD-15 | `projection_boundary_guard.py` | 4 | V0,V2,V3 | E1,E2 | strict | projection | PLANNED | projection boundary |
| GUARD-16 | `memory_trace_boundary_guard.py` | 4 | V1,V4,V7 | E1,E2 | strict | traces | PLANNED | memory traces |
| GUARD-17 | `determinism_guard.py` | 3 | V5,V10 | E3 | strict | determinism | PLANNED | deterministic tests |
| GUARD-18 | `import_boundary_guard.py` | 3 | V1,V2,V7 | E2 | strict | imports | PLANNED | import direction |
| GUARD-19 | `repo_path_guard.py` | 0 | V6,V7 | E1 | strict | paths | CORE_READY | path policy |
| GUARD-20 | `release_claim_guard.py` | 5 | V4,V7 | E1,E4 | strict | release | PLANNED,MVP | release claims |
| GUARD-21 | `promotion_ledger_guard.py` | 5 | V4,V6,V7 | E1,E3 | strict | promotion | PLANNED | promotion ledger |
| GUARD-22 | `contract_traceability_guard.py` | 0 | V7,V12 | E1 | strict | contracts | CORE_READY | contract trace |
| GUARD-23 | `guard_runtime_integrity_guard.py` | 0 | V15,V13 | E1 | strict | guard runtime | PLANNED | runtime identity |
| GUARD-24 | `anchor_blob_integrity_guard.py` | 0 | V14,V6 | E1 | strict | anchor bytes | CORE_READY | anchor hashes |
| GUARD-25 | `ontology_creep_guard.py` | 2 | V8,V12 | E1,E2 | strict | semantics | PLANNED | slow drift |
| GUARD-26 | `inter_guard_coupling_guard.py` | 3 | V11,V2 | E1,E2 | strict | independence | PLANNED | guard isolation |
| GUARD-27 | `evidence_attestation_guard.py` | 5 | V4,V7 | E4,E5 | strict | attestation | PLANNED | evidence wording |
| GUARD-28 | `dependency_supply_chain_guard.py` | 5 | V13,V15 | E1 | strict | dependencies | PLANNED | dependency lock |
| GUARD-29 | `runtime_sandbox_guard.py` | 5 | V2,V5,V10,V13 | E2,E3 | strict | sandbox | PLANNED | runtime sandbox |
| GUARD-30 | `incident_boundary_guard.py` | 5 | V1,V2,V4,V5 | E4,E5 | strict | incident | PLANNED | incident limits |

---

## 7. Level-to-guard view

### Level 0 — Fundamental Repository Perimeter

```text
GUARD-00 perimeter kernel
GUARD-01 canonical ontology boundary
GUARD-02 repository boundary
GUARD-05 repository layer boundary
GUARD-11 master index router
GUARD-19 repository path policy
GUARD-22 contract traceability
GUARD-23 guard runtime integrity
GUARD-24 anchor blob integrity
```

### Level 1 — Specialized Ontological Perimeter

```text
GUARD-06 no feedback loop
GUARD-07 Vortex non-agentic boundary
GUARD-08 QE aporia boundary
GUARD-09 Triality boundary
```

### Level 2 — Semantic / Ontological Vocabulary Perimeter

```text
GUARD-10 vector drift
GUARD-12 coherence vocabulary
GUARD-25 ontology creep
```

### Level 3 — Code Behavior Perimeter

```text
GUARD-03 code behavior audit
GUARD-17 determinism
GUARD-18 import boundary
GUARD-26 inter-guard coupling
```

### Level 4 — Bridge / Projection / Trace Perimeter

```text
GUARD-13 EK observable non-authority
GUARD-14 Φ to EK bridge
GUARD-15 projection boundary
GUARD-16 memory trace boundary
```

### Level 5 — Runtime / Evidence / Release Perimeter

```text
GUARD-04 empirical claim guard
GUARD-20 release claim guard
GUARD-21 promotion ledger guard
GUARD-27 evidence attestation guard
GUARD-28 dependency supply-chain guard
GUARD-29 runtime sandbox guard
GUARD-30 incident boundary guard
```

---

## 8. MVP perimeter

The first executable perimeter should be smaller than the full matrix.

Recommended MVP:

```text
GUARD-00 perimeter kernel
GUARD-01 canonical ontology guard
GUARD-03 code behavior audit
GUARD-12 coherence vocabulary guard
GUARD-20 release claim guard
```

MVP purpose:

```text
block root authority drift
block canonical ontology mutation
block code behavior mutation
block vocabulary conversion
block release/evidence overclaim
```

Do not implement all 31 guards before shared core stabilizes.

---

## 9. Current shared core support

Already planned or built core modules:

```text
guards/core/findings.py
guards/core/reporting.py
guards/core/text_scan.py
guards/core/immutable_blob.py
guards/core/contracts.py
guards/core/paths.py
guards/core/roles.py
guards/core/capabilities.py
guards/core/ast_scan.py
```

Core-to-guard support:

```text
findings.py       → all guards
reporting.py      → all guards
text_scan.py      → GUARD-08,09,10,12,13,15,20,25,27
immutable_blob.py → GUARD-24
contracts.py      → GUARD-22
paths.py          → GUARD-02,05,19
roles.py          → GUARD-03,17,18,26,29
capabilities.py   → GUARD-03,17,18,26,29
ast_scan.py       → GUARD-03,17,18,26,29
```

---

## 10. Refactoring order

Recommended order:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-01 canonical_ontology_guard.py
3. GUARD-03 vectaetos_code_behavior_audit.py
4. GUARD-08 qe_aporia_guard.py
5. GUARD-09 triality_guard.py
6. GUARD-10 vector_drift_guard.py
7. GUARD-11 master_index_router_guard.py
8. GUARD-20 release_claim_guard.py
9. GUARD-19 repo_path_guard.py
10. GUARD-22 contract_traceability_guard.py
11. GUARD-24 anchor_blob_integrity_guard.py
```

Reason:

```text
stabilize vocabulary
then root ontology
then code behavior
then specialized vocabulary
then path / contract / blob integrity
```

---

## 11. Forbidden transformations

No guard may transform itself into:

```text
truth authority
ontology source
optimizer
planner
decision system
recommendation engine
runtime controller
feedback loop into Φ
auto-fix layer for ontology-facing text
auto-revert mechanism
auto-quarantine mechanism
```

---

## 12. Safe claim language

Allowed:

```text
configured blocker detected
repository-state drift exposed
static scan finding
AST compliance finding
byte integrity mismatch
evidence class mismatch
```

Forbidden:

```text
truth invalidated
ontology proven
VECTAETOS safe
deployment valid
hash proves meaning
CI proves safety
guard decides
```

---

## 13. Relation to other files

```text
guards/GUARD_PERIMETER_MODEL.md
    defines perimeter grammar

guards/MATICA_PERIMETER.md
    maps all guards to that grammar

guards/GUARD_MVP_PROFILE.md
    selects first executable subset

guards/README.md
    public guide for guard directory

guards/core/README.md
    guide for shared implementation kernel
```

Conflict order:

```text
canonical anchor
    >
MASTER_INDEX
    >
GUARD_PERIMETER_MODEL
    >
MATICA_PERIMETER
    >
GUARD_MVP_PROFILE
    >
README
    >
implementation note
```

---

## 14. Final posture

```text
The matrix maps guard responsibility.
It does not create guard authority.
```

Slovak:

```text
Matica mapuje zodpovednosť guardov.
Nevytvára autoritu guardov.
```

End.
