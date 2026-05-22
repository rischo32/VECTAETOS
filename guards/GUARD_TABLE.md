# VECTAETOS — GUARD TABLE

## Precise Repository Perimeter Roles

### Status
ACTIVE REPOSITORY PERIMETER MAP

### Location
Recommended path:

```text
guards/GUARD_TABLE.md
```

### Role
Human-readable map of guard roles, levels, boundaries, and implementation priority.

### Authority
Descriptive only.

### Ontology
None.

### Runtime
None.

### Feedback
None.

---

## 0. Purpose

This table records the repository perimeter guards of VECTAETOS.

It defines:

```text
guard id
guard file
guard level
status
protected boundary
input surface
expected output
implementation priority
```

This document does not define ontology.

This document does not replace anchors.

This document does not replace contracts.

This document does not replace the manifest.

This document does not provide empirical evidence.

This document is a perimeter map only.

---

## 1. Source Alignment

This guard table is aligned with:

```text
/VOCABULARY_LOCK.md
/guards/perimeter_manifest.json
/guards/run_perimeter.py
/contracts/vectaetos_code_contract.json
/contracts/ASSEMBLY_MANIFEST.json
/contracts/LAYER_BOUNDARIES.md
/contracts/vectaetos_contract.json
/MASTER_INDEX.md
/anchors/
/formal/
```

If this table conflicts with the manifest, the manifest controls execution.

If this table conflicts with anchors, anchors control meaning.

---

## 2. Guard Level Model

| Level | Name | Purpose |
|---:|---|---|
| 0 | Fundamental Repository Perimeter | Protects root repository boundary and canonical language posture. |
| 1 | Specialized Ontological Perimeter | Protects specific canonical structures and vocabulary zones. |
| 2 | Bridge / EK / Layer-Specific Perimeter | Protects downstream bridge vocabulary and audit observables. |
| 3 | Runtime / CI / Release Perimeter | Protects deterministic execution, runner reports, path shape, and release claims. |

---

## 3. Active Guard Table

| ID | Guard | Level | Status | Required | Primary role |
|---|---|---:|---|---:|---|
| GUARD-01 | `canonical_ontology_guard.py` | 0 | ACTIVE | yes | Diff-based canonical boundary scan for changed files. |
| GUARD-02 | `vectaetos_boundary_guard.py` | 0 | ACTIVE | yes | Repository-wide semantic perimeter scan. |
| GUARD-03 | `vectaetos_code_behavior_audit.py` | 0 | ACTIVE | yes | Static AST audit against code-role contracts. |
| GUARD-04 | `empirical_claim_guard.py` | 0 | ACTIVE | yes | Evidence-claim perimeter for the L0-L4 ladder. |
| GUARD-05 | `repo_layer_boundary_guard.py` | 0 | ACTIVE | yes | Triadic dependency and repository layer boundary scan. |
| GUARD-06 | `no_feedback_loop_guard.py` | 0 | ACTIVE | yes | Acyclic boundary scan across output, trace, and field-facing text. |
| GUARD-07 | `vortex_non_agentic_guard.py` | 0 | ACTIVE | yes | Vortex posture boundary for candidate-trajectory exposure. |
| GUARD-08 | `qe_aporia_guard.py` | 1 | ACTIVE | yes | QE non-representability vocabulary boundary. |
| GUARD-09 | `triality_guard.py` | 1 | ACTIVE | yes | Triality and OAAT boundary scan. |
| GUARD-10 | `vector_drift_guard.py` | 1 | ACTIVE | no | External drift-observable report. |
| GUARD-11 | `master_index_router_guard.py` | 1 | ACTIVE | yes | Master Index routing and referenced file availability. |

---

## 4. Planned Guard Table

| ID | Guard | Level | Status | Required now | Primary role |
|---|---|---:|---|---:|---|
| GUARD-12 | `coherence_vocabulary_guard.py` | 1 | PLANNED | no | Active vocabulary alignment with `/VOCABULARY_LOCK.md`. |
| GUARD-13 | `ek_observable_non_authority_guard.py` | 2 | PLANNED | no | EK observables remain audit-only vocabulary. |
| GUARD-14 | `bridge_phi_to_ek_guard.py` | 2 | PLANNED | no | Protects `/formal/BRIDGE_PHI_TO_EK.md` and bridge implementation language. |
| GUARD-15 | `projection_boundary_guard.py` | 2 | PLANNED | no | Projection, runes, glyphs, and TetraGlyph structural-marker boundary. |
| GUARD-16 | `memory_trace_boundary_guard.py` | 2 | PLANNED | no | Memory, logs, ESM, EAT, MML, and LTL trace boundary. |
| GUARD-17 | `determinism_guard.py` | 3 | PLANNED | no | Deterministic execution and reproducibility surface. |
| GUARD-18 | `import_boundary_guard.py` | 3 | PLANNED | no | Import and dependency direction boundary. |
| GUARD-19 | `repo_path_guard.py` | 3 | PLANNED | no | Repository path and layer placement boundary. |
| GUARD-20 | `release_claim_guard.py` | 3 | PLANNED | no | Release, DOI, public statement, and evidence phrasing boundary. |

---

## 5. Detailed Roles

### GUARD-01 — Canonical Ontology Guard

File:

```text
guards/canonical_ontology_guard.py
```

Level:

```text
0
```

Execution type:

```text
diff-based
```

Inputs:

```text
base revision
head revision
changed files
```

Protected surface:

```text
canonical anchors
formal files
root boundary files
high-risk active text
```

Role:

```text
Mechanically blocks direct semantic drift in changed repository entries.
```

Output:

```text
PASS / findings / configuration issue
```

Runner profile:

```text
required
```

---

### GUARD-02 — VECTAETOS Boundary Guard

File:

```text
guards/vectaetos_boundary_guard.py
```

Level:

```text
0
```

Execution type:

```text
repository scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
active repository language
```

Role:

```text
Scans broad repository text for boundary-incompatible formulations.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-03 — Code Behavior Audit

File:

```text
guards/vectaetos_code_behavior_audit.py
```

Level:

```text
0
```

Execution type:

```text
AST scan
```

Inputs:

```text
repository root
contracts/vectaetos_code_contract.json
```

Protected surface:

```text
Python code behavior
role-specific permissions
role-specific prohibited operations
```

Role:

```text
Checks Python source against repository code-role contracts.
```

Important rule:

```text
Every active .py file must be syntactically valid Python.
```

Output:

```text
AST findings or execution/configuration issue
```

Runner profile:

```text
required
```

---

### GUARD-04 — Empirical Claim Guard

File:

```text
guards/empirical_claim_guard.py
```

Level:

```text
0
```

Execution type:

```text
repository claim scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
L0-L4 evidence language
A_full posture
release and public claims
```

Role:

```text
Prevents evidence language from exceeding the current validation layer.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-05 — Repository Layer Boundary Guard

File:

```text
guards/repo_layer_boundary_guard.py
```

Level:

```text
0
```

Execution type:

```text
repository layer scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
VECTAETOS / ASIMULATOR / ASI_MOD dependency language
repository layer placement
downstream identity statements
```

Role:

```text
Protects ontologically asymmetric triadic dependency.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-06 — No Feedback Loop Guard

File:

```text
guards/no_feedback_loop_guard.py
```

Level:

```text
0
```

Execution type:

```text
acyclic-boundary scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
output-facing text
trace-facing text
field-facing text
memory-facing text
audit-facing text
projection-facing text
```

Role:

```text
Protects one-way boundary posture across repository layers.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-07 — Vortex Non-Agentic Guard

File:

```text
guards/vortex_non_agentic_guard.py
```

Level:

```text
0
```

Execution type:

```text
Vortex boundary scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
Vortex code
Vortex docs
trajectory vocabulary
```

Role:

```text
Keeps Vortex language in candidate-trajectory exposure posture.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-08 — QE Aporia Guard

File:

```text
guards/qe_aporia_guard.py
```

Level:

```text
1
```

Execution type:

```text
QE vocabulary scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
QE vocabulary
aporia terminology
non-representability markers
```

Role:

```text
Keeps QE vocabulary aligned with non-representability.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-09 — Triality Guard

File:

```text
guards/triality_guard.py
```

Level:

```text
1
```

Execution type:

```text
triality vocabulary scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
triality language
OAAT posture
triadic architecture language
axis-dominance language
```

Role:

```text
Protects triality from flattening, collapse, or privileged-axis language.
```

Output:

```text
report or strict failure
```

Runner profile:

```text
required
```

---

### GUARD-10 — Vector Drift Guard

File:

```text
guards/vector_drift_guard.py
```

Level:

```text
1
```

Execution type:

```text
external drift-observable report
```

Inputs:

```text
repository root
mode
fail_at value for CI profile
```

Protected surface:

```text
drift-vector language
external observable reports
```

Role:

```text
Reports drift as an external observable.
```

Output:

```text
report / JSON / CI status
```

Runner profile:

```text
optional
```

---

### GUARD-11 — Master Index Router Guard

File:

```text
guards/master_index_router_guard.py
```

Level:

```text
1
```

Execution type:

```text
router integrity scan
```

Inputs:

```text
repository root
mode
```

Protected surface:

```text
Master Index routing
referenced formal paths
canonical routing posture
```

Role:

```text
Checks that Master Index references remain resolvable and router-shaped.
```

Output:

```text
check or inventory
```

Runner profile:

```text
required
```

---

## 6. Planned Guard Roles

### GUARD-12 — Coherence Vocabulary Guard

File:

```text
guards/coherence_vocabulary_guard.py
```

Level:

```text
1
```

Planned protected surface:

```text
VOCABULARY_LOCK.md alignment
K predicate vocabulary
K𝒟 notation
boundary term vocabulary
legacy diagnostic notation
```

Role:

```text
Keeps active repository language aligned with the vocabulary lock.
```

Priority:

```text
next
```

---

### GUARD-13 — EK Observable Non-Authority Guard

File:

```text
guards/ek_observable_non_authority_guard.py
```

Level:

```text
2
```

Planned protected surface:

```text
Tᵢ^EK
χᵢ
Qᵢ^EK
μᵢ
Aᵢⱼ
h_topo
η_EK
Λ_EK
LTL
```

Role:

```text
Keeps EK observables in read-only audit vocabulary.
```

Priority:

```text
after GUARD-12
```

---

### GUARD-14 — Bridge Φ to EK Guard

File:

```text
guards/bridge_phi_to_ek_guard.py
```

Level:

```text
2
```

Planned protected surface:

```text
/formal/BRIDGE_PHI_TO_EK.md
ek_core bridge implementation
R to Tᵢ^EK mapping
Δ to χᵢ mapping
χᵢ to Qᵢ^EK mapping
```

Role:

```text
Keeps the Φ to EK bridge read-only and vocabulary-safe.
```

Priority:

```text
after GUARD-13
```

---

### GUARD-15 — Projection Boundary Guard

File:

```text
guards/projection_boundary_guard.py
```

Level:

```text
2
```

Planned protected surface:

```text
Π
Γ
runes
glyphs
TetraGlyph
projection docs
projection code
```

Role:

```text
Keeps projection as structural exposure only.
```

Priority:

```text
later
```

---

### GUARD-16 — Memory Trace Boundary Guard

File:

```text
guards/memory_trace_boundary_guard.py
```

Level:

```text
2
```

Planned protected surface:

```text
ESM
EAT
MML
LTL
logs
ledger text
trace code
```

Role:

```text
Keeps trace layers descriptive and outside field-definition authority.
```

Priority:

```text
later
```

---

### GUARD-17 — Determinism Guard

File:

```text
guards/determinism_guard.py
```

Level:

```text
3
```

Planned protected surface:

```text
randomness usage
seed handling
time usage
network usage
non-deterministic execution surfaces
```

Role:

```text
Reports deterministic-execution risks.
```

Priority:

```text
after perimeter runner stabilizes
```

---

### GUARD-18 — Import Boundary Guard

File:

```text
guards/import_boundary_guard.py
```

Level:

```text
3
```

Planned protected surface:

```text
Python imports
downstream to root imports
root to downstream imports
contracts and scripts import shape
```

Role:

```text
Checks repository import direction and layer separation.
```

Priority:

```text
after deterministic guard
```

---

### GUARD-19 — Repository Path Guard

File:

```text
guards/repo_path_guard.py
```

Level:

```text
3
```

Planned protected surface:

```text
directory placement
anchor placement
formal placement
research placement
corpus placement
guard placement
contract placement
```

Role:

```text
Checks that files live in compatible repository layers.
```

Priority:

```text
after import boundary guard
```

---

### GUARD-20 — Release Claim Guard

File:

```text
guards/release_claim_guard.py
```

Level:

```text
3
```

Planned protected surface:

```text
release notes
Zenodo text
README badges
public-facing statements
DOI statements
```

Role:

```text
Keeps public release language aligned with evidence posture.
```

Priority:

```text
after empirical claim guard is stable
```

---

## 7. Build Order

Recommended next implementation order:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-13 ek_observable_non_authority_guard.py
3. GUARD-14 bridge_phi_to_ek_guard.py
4. GUARD-15 projection_boundary_guard.py
5. GUARD-16 memory_trace_boundary_guard.py
6. GUARD-17 determinism_guard.py
7. GUARD-18 import_boundary_guard.py
8. GUARD-19 repo_path_guard.py
9. GUARD-20 release_claim_guard.py
```

Rationale:

```text
Vocabulary lock exists.
Manifest exists.
Runner exists.
The next missing perimeter is active vocabulary enforcement.
```

---

## 8. Manifest Relationship

Execution source:

```text
guards/perimeter_manifest.json
```

This table should match the manifest.

The manifest controls execution.

This table explains roles.

If a planned guard becomes active, update both:

```text
guards/perimeter_manifest.json
guards/GUARD_TABLE.md
```

---

## 9. Runner Relationship

Runner:

```text
guards/run_perimeter.py
```

The runner executes active manifest entries.

The runner does not replace individual guards.

The runner does not rewrite findings.

The runner does not create ontology.

The runner only coordinates perimeter execution.

---

## 10. Final Statement

The guard table maps repository perimeter responsibilities.

It is not a formal anchor.

It is not a contract.

It is not empirical validation.

It is a maintenance map for the guard perimeter.

---

End of guard table.
