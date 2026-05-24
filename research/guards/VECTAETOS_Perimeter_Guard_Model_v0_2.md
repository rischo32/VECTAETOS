# VECTAETOS™ Perimeter Guard Model v0.2

**Status:** Implementation Proposal  
**Scope:** VECTAETOS repository perimeter only  
**Execution Power:** Repository-state protection only  
**Feedback into Φ:** none  
**Ontology Authority:** none  
**Core Sentence:** Guard exponuje drift; nedefinuje pravdu.

---

## 0. Core Boundary

```text
guard = drift detection surface
guard ≠ truth
guard ≠ ontology
guard ≠ authority
guard ≠ optimizer
guard ≠ decision module
guard ≠ Φ
```

The perimeter guard system exists to expose possible drift relative to canonical anchors, machine-readable contracts, and declared repository boundaries.

It does **not** decide whether an implementation, document, bridge, projection, audit report, release claim, or interpretation is metaphysically true.

```text
diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
warning ≠ verdict
failure ≠ metaphysical proof
CI pass ≠ empirical proof
```

Allowed operational chain:

```text
canonical anchors
    ↓
machine-readable contracts
    ↓
shared guard kernel
    ↓
individual guards
    ↓
LSP diagnostics / CLI audit / CI report
```

No lower layer may redefine a higher layer.

No downstream layer may mutate Φ.

No guard may become a source of ontology.

---

## 1. Design Thesis

The existing guard table is useful as a **guard inventory**.

This proposal upgrades it into a **perimeter architecture**:

```text
inventory → kernel
levels → perimeters
patterns → forbidden conversions
findings → typed evidence records
guards → contract-traced drift detectors
CI failure → repository-state refusal only
```

Working posture:

```text
mapujeme → obmedzujeme → exponujeme → odmietame drift
```

Not:

```text
rozhodujeme → optimalizujeme → dokazujeme → autorizujeme
```

---

## 2. Perimeter Model

Instead of treating guards only as linear `Level 0–3`, use:

```text
Perimeter = scope layer × drift vector × evidence class × enforcement mode
```

This keeps the current level model human-readable, while making implementation stricter and more composable.

---

## 3. Perimeter Rings

### P0 — Canonical Repository Perimeter

**Purpose:** Protect root repository boundary, canonical anchors, formal files, status files, and canonical routing.

**Protected surfaces:**

```text
anchors/
formal/
MASTER_INDEX.md
canonical status files
guard files
semantic errata registry
promotion paths
root repository shape
```

**Related guards:**

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-11 master_index_router_guard.py
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
```

**Primary drift vectors:**

```text
V0_authority_inflation
V1_upward_mutation
V6_path_status_laundering
V7_contract_drift
```

---

### P1 — Semantic / Ontological Vocabulary Perimeter

**Purpose:** Protect canonical language around ZMYSEL / Ξ, Φ, Σ, R, K(Φ), κ, QE, Vortex, Triality, and related boundary terms.

**Protected surfaces:**

```text
ZMYSEL / Ξ
Φ = (Σ, R)
Σ
R
K(Φ)
κ
QE
Vortex
Triality / OAAT
canonical vocabulary
```

**Related guards:**

```text
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
GUARD-12 coherence_vocabulary_guard.py
```

**Primary drift vectors:**

```text
V2_agency_injection
V3_forbidden_conversion
V8_negation_blindness
V9_silence_qe_coercion
```

---

### P2 — Code Behavior Perimeter

**Purpose:** Protect Python source behavior, role-specific permissions, and non-agentic execution discipline.

**Protected surfaces:**

```text
Python source behavior
role-specific permissions
read-only guard behavior
dynamic execution
network/subprocess/randomness
file mutation
ontology-like assignments
selection / ranking behavior
Vortex non-agentic behavior
```

**Related guards:**

```text
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-07 vortex_non_agentic_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
```

**Primary drift vectors:**

```text
V1_upward_mutation
V2_agency_injection
V5_nondeterminism
V3_forbidden_conversion
```

---

### P3 — Bridge / Projection / Trace Perimeter

**Purpose:** Protect downstream read-only bridge vocabulary, projection boundaries, EK observables, and trace layers.

**Protected surfaces:**

```text
EK observables
Φ → EK bridge
projection vocabulary
runes / glyphs / TetraGlyph
memory traces
logs
ledger language
LTL / ESM / EAT / MML
```

**Related guards:**

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
```

**Primary drift vectors:**

```text
V0_authority_inflation
V1_upward_mutation
V3_forbidden_conversion
V4_evidence_overclaim
```

---

### P4 — Runtime / Evidence / Release Perimeter

**Purpose:** Protect deterministic execution, evidence posture, public claims, release text, DOI language, and CI-report boundaries.

**Protected surfaces:**

```text
deterministic execution
import direction
repository path discipline
release notes
DOI text
README badges
public-facing statements
evidence class boundaries
```

**Related guards:**

```text
GUARD-04 empirical_claim_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-19 repo_path_guard.py
GUARD-20 release_claim_guard.py
```

**Primary drift vectors:**

```text
V4_evidence_overclaim
V5_nondeterminism
V6_path_status_laundering
V0_authority_inflation
```

---

## 4. Drift Vector Taxonomy

Every guard finding should map to one or more drift vectors.

```yaml
drift_vectors:
  V0_authority_inflation:
    detects: "diagnostic/report/guard/CI becomes truth authority"

  V1_upward_mutation:
    detects: "lower layer attempts to mutate higher layer"

  V2_agency_injection:
    detects: "agent, decision, optimization, reward, ranking, best-state language"

  V3_forbidden_conversion:
    detects: "κ→metric, QE→exception, projection→interpretation, report→decision"

  V4_evidence_overclaim:
    detects: "static compliance represented as empirical proof"

  V5_nondeterminism:
    detects: "unseeded randomness, time, network, undeclared subprocess"

  V6_path_status_laundering:
    detects: "draft/research file claims canonical/frozen/official status"

  V7_contract_drift:
    detects: "contract invents rule not traceable to anchor"

  V8_negation_blindness:
    detects: "guard would flag a forbidden phrase inside an explicit negation"

  V9_silence_qe_coercion:
    detects: "forced output where QE/aporia/silence should remain valid"
```

---

## 5. Evidence Classes

Evidence posture must be explicit.

```text
E0 text claim
E1 static text scan
E2 AST / contract compliance
E3 deterministic test suite
E4 empirical validation
E5 external replication / deployment evidence
```

Allowed:

```text
E2 compliant
no blocker findings
static audit clean
CI perimeter checks passed
```

Forbidden:

```text
safe
validated
deployment-ready
proves correctness
empirically confirmed
guard-certified ontology
CI-proven safety
```

Guard clean state means:

```text
No configured blocker was detected within the declared perimeter.
```

It does **not** mean:

```text
The system is safe.
The ontology is true.
Deployment is valid.
The implementation is empirically proven.
```

---

## 6. Enforcement Modes

```yaml
enforcement_modes:
  advisory:
    ci_exit: 0
    purpose: "developer-facing signal only"

  report:
    ci_exit: 0
    purpose: "repository report without blocking"

  strict:
    ci_exit: 1_on_blocker
    purpose: "repository-state refusal"

  fail_closed:
    ci_exit: 2_on_guard_runtime_error
    purpose: "guard infrastructure failure blocks confidence"

  experimental:
    ci_exit: 0
    purpose: "collect signal before enforcement"
```

Rule:

```text
Strict CI failure is repository-state refusal, not metaphysical proof.
```

---

## 7. Unified Finding Format

All guards should emit one shared finding shape.

```yaml
finding:
  id: "VEC-P1-CONV-001"
  guard_id: "GUARD-12"
  guard_file: "guards/coherence_vocabulary_guard.py"
  scope: "P1_semantic_vocabulary"
  vector: "V3_forbidden_conversion"
  severity: "BLOCKER"
  confidence: "high"

  path: "formal/BRIDGE_PHI_TO_EK.md"
  line: 128
  role: "formal_bridge"

  protected_object: "κ"
  observed_pattern: "kappa_estimate"
  forbidden_conversion: "κ -> numeric estimate"

  negated_context: false
  evidence_class_claimed: null
  evidence_class_allowed: "E1_static_scan"

  anchor_ref: "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md"
  contract_ref: "contracts/perimeters/p1_semantic_vocabulary.yaml"

  message: "Pattern appears to convert κ from representability boundary into numeric estimate."
  safer_form: "Use boundary-of-representability language; do not expose κ as metric, estimate, threshold, or score."

  ontology_authority: false
  auto_fix_allowed: false
```

Mandatory fields:

```text
guard_id
scope
vector
severity
confidence
path
message
ontology_authority
auto_fix_allowed
```

Rule:

```text
auto_fix_allowed: false
```

For ontology-facing text, guards may report drift but must not automatically rewrite meaning.

---

## 8. Contract Layout

Recommended repository contract structure:

```text
contracts/
  perimeter_kernel.yaml

  perimeters/
    p0_repository.yaml
    p1_semantic_vocabulary.yaml
    p2_code_behavior.yaml
    p3_bridge_projection_trace.yaml
    p4_runtime_evidence_release.yaml

  vectors/
    authority_inflation.yaml
    upward_mutation.yaml
    agency_injection.yaml
    forbidden_conversion.yaml
    evidence_overclaim.yaml
    nondeterminism.yaml
    path_status_laundering.yaml
    contract_drift.yaml
    negation_blindness.yaml
    silence_qe_coercion.yaml

  evidence/
    evidence_classes.yaml

  roles/
    code_roles.yaml
```

This separates:

```text
what is protected
where it is protected
which drift vector is being detected
which evidence class is allowed
how strongly CI enforces it
```

---

## 9. Shared Guard Kernel

Before adding more individual guard files, create a shared deterministic kernel.

```text
guards/core/
  findings.py
  contracts.py
  text_scan.py
  ast_scan.py
  roles.py
  capabilities.py
  reporting.py
  paths.py
```

### `guards/core/findings.py`

Responsibilities:

```text
Finding dataclass / Pydantic model
severity enum
drift vector enum
evidence class enum
JSON rendering
GitHub annotation rendering
```

### `guards/core/contracts.py`

Responsibilities:

```text
load YAML/JSON contracts
validate contract schema
trace rule → anchor_ref
fail closed on invalid contract
```

### `guards/core/text_scan.py`

Responsibilities:

```text
line scanning
window scanning
regex pattern scanning
negated context detection
forbidden conversion detection
```

### `guards/core/ast_scan.py`

Responsibilities:

```text
Python AST parsing
call detection
import detection
assignment detection
function/class name detection
filesystem/network/subprocess/randomness detection
```

### `guards/core/roles.py`

Responsibilities:

```text
declared role detection
inferred role detection
role policy lookup
```

### `guards/core/capabilities.py`

Responsibilities:

```text
allow_network
allow_subprocess
allow_file_write
allow_randomness
allow_selection
protect_ontology_assignments
```

### `guards/core/reporting.py`

Responsibilities:

```text
human report
JSON report
GitHub annotations
exit code calculation
```

---

## 10. Guard Inventory v0.2

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-04 empirical_claim_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-06 no_feedback_loop_guard.py
GUARD-07 vortex_non_agentic_guard.py
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
GUARD-11 master_index_router_guard.py
GUARD-12 coherence_vocabulary_guard.py
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-19 repo_path_guard.py
GUARD-20 release_claim_guard.py
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
```

---

## 11. New Guards

### GUARD-00 — Perimeter Kernel Guard

**File:**

```text
guards/perimeter_kernel_guard.py
```

**Perimeter:**

```text
P0
```

**Purpose:**

```text
Checks that no guard, runner, manifest, or contract claims ontology authority.
```

**Detects:**

```text
guard proves truth
guard validates ontology
guard authorizes deployment
CI proves safety
runner decides validity
manifest defines ontology
contract replaces anchor
```

**Output:**

```text
BLOCKER on authority inflation
```

---

### GUARD-21 — Promotion Ledger Guard

**File:**

```text
guards/promotion_ledger_guard.py
```

**Perimeter:**

```text
P0 / P4
```

**Purpose:**

```text
Prevents status laundering when files move between draft, research, formal, anchor, release, or public-facing paths.
```

**Detects:**

```text
drafts/ → anchors/ without ledger
research/ → formal/ without ledger
experimental file claims canonical status
release text claims stronger status than source
```

**Required ledger shape:**

```yaml
promotion:
  from_path:
  to_path:
  source_hash:
  target_hash:
  anchor_refs:
  contract_refs:
  human_review_note:
  claim_delta:
  major_version_required: true|false
```

**Output:**

```text
BLOCKER if promotion path lacks explicit read-only trace.
```

---

### GUARD-22 — Contract Traceability Guard

**File:**

```text
guards/contract_traceability_guard.py
```

**Perimeter:**

```text
P0 / P1 / P2 / P3 / P4
```

**Purpose:**

```text
Ensures contracts project anchors instead of inventing ontology.
```

**Detects:**

```text
contract rule has no anchor_ref
contract stronger than anchor without note
contract weaker than anchor
contract adds operational power
contract changes protected object list
contract creates new source of truth
```

**Output:**

```text
BLOCKER for untraceable normative rule in strict contracts.
WARN for advisory or experimental rules without full trace.
```

---

## 12. Guard-Specific Requirements

### GUARD-01 — Canonical Ontology Guard

Current role is strong: diff-based scan, protected file mutation detection, semantic drift phrase detection, errata registry recognition.

Recommended additions:

```text
negated_context detection
forbidden_conversion metadata
protected_object metadata
JSON output mode
contract-based pattern loading
shared Finding format
```

Hardcoded patterns should migrate into contracts over time.

The Python script should become a deterministic scanner, not the source of rule meaning.

---

### GUARD-03 — Code Behavior Audit

Current role is strong: static AST audit, declared/inferred VECTAETOS roles, dynamic execution checks, network/subprocess/randomness checks, file mutation checks, protected ontology assignment review, Vortex selection/optimization protection.

Recommended additions:

```text
--format json
--fail-on WARN|HARD|BLOCKER
role capability matrix
explicit evidence_class
protected object mapping
contract trace refs
shared Finding format
```

Suggested role capability shape:

```yaml
roles:
  guard:
    allow_network: false
    allow_subprocess: false
    allow_file_write: false
    allow_randomness: false
    allow_selection_functions: true
    protect_ontology_assignments: true

  git_guard:
    allow_network: false
    allow_subprocess: true
    allow_file_write: false
    allow_randomness: false
    allow_selection_functions: true
    subprocess_allowlist:
      - git
    protect_ontology_assignments: true

  report_writer:
    allow_network: false
    allow_subprocess: false
    allow_file_write: true
    allow_randomness: false
    allow_selection_functions: true
    protect_ontology_assignments: true

  vortex:
    allow_network: false
    allow_subprocess: false
    allow_file_write: false
    allow_randomness: false
    allow_selection_functions: false
    protect_ontology_assignments: true
```

---

## 13. Forbidden Conversion Table

```yaml
forbidden_conversions:
  - id: "FC-KAPPA-METRIC"
    protected_object: "κ"
    forbidden_targets:
      - metric
      - score
      - threshold
      - tunable parameter
      - numeric estimate
    allowed_language:
      - boundary of representability
      - non-metric boundary
      - not a score
      - not an optimization target

  - id: "FC-K-PHI-SCORE"
    protected_object: "K(Φ)"
    forbidden_targets:
      - score
      - reward
      - metric
      - objective
      - target
    allowed_language:
      - coherence predicate
      - binary predicate where formally defined
      - representability condition

  - id: "FC-QE-ERROR"
    protected_object: "QE"
    forbidden_targets:
      - error
      - bug
      - exception
      - fallback
      - failure
      - repair trigger
    allowed_language:
      - non-representability
      - qualitative epistemic aporia
      - legitimate boundary state

  - id: "FC-VORTEX-OPTIMIZER"
    protected_object: "Vortex"
    forbidden_targets:
      - optimizer
      - best trajectory selector
      - ranker
      - reward executor
      - policy updater
    allowed_language:
      - candidate trajectory exposure
      - non-teleological exploration
      - descriptive trajectory rendering

  - id: "FC-PROJECTION-INTERPRETER"
    protected_object: "Projection"
    forbidden_targets:
      - interpreter
      - truth authority
      - prescription layer
      - decision layer
    allowed_language:
      - structural exposure
      - rendering
      - marker layer

  - id: "FC-EK-AUTHORITY"
    protected_object: "Epistemic Cryptography"
    forbidden_targets:
      - authority
      - decision module
      - control layer
      - intervention layer
      - optimizer
    allowed_language:
      - structural audit
      - non-interventional observability
      - read-only coherence exposure

  - id: "FC-MEMORY-PHI"
    protected_object: "Memory / Trace"
    forbidden_targets:
      - ontology updater
      - Φ modifier
      - Vortex feedback source
      - canonical source
    allowed_language:
      - read-only trace
      - adapter context
      - audit trail
      - non-authoritative memory
```

---

## 14. Negated Context Rule

Guard scanners must not blindly flag forbidden terms when they occur inside explicit negation.

Allowed:

```text
VECTAETOS is not an optimizer.
κ is not a metric.
QE is not an exception.
Projection does not interpret.
EK does not decide.
Memory does not modify Φ.
CI pass is not empirical validation.
```

Forbidden:

```text
VECTAETOS optimizes trajectories.
κ_score = 0.84
QE exception handler
Projection interprets meaning.
EK decides validity.
Memory updates Φ.
CI pass proves safety.
```

Implementation sketch:

```text
If forbidden phrase appears inside a short negation window,
classify as negated_context=true and do not block.

If same line also contains operational implementation language,
escalate to WARN for review.
```

Example:

```text
"QE is not an exception" → OK
"QEExceptionHandler repairs aporia" → BLOCKER
```

---

## 15. Release Claim Boundary

Release/public language may say:

```text
Repository perimeter checks passed.
No configured blocker findings were detected.
Static audit found no hard violations.
This is a repository-state protection result.
This is not empirical validation.
```

Release/public language must not say:

```text
VECTAETOS is safe.
VECTAETOS is validated.
Deployment is authorized.
CI proves correctness.
Guard clean means ontology is true.
The system is empirically confirmed.
```

---

## 16. Recommended GUARD_TABLE.md Columns

Extend the current table with:

```text
Perimeter
Drift vectors
Evidence class
Enforcement mode
Output format
```

Example:

```markdown
| ID | Guard | Perimeter | Vectors | Evidence | Enforcement | Status |
|---|---|---|---|---|---|---|
| GUARD-01 | canonical_ontology_guard.py | P0 | V1,V6 | E1 | strict | ACTIVE |
| GUARD-03 | vectaetos_code_behavior_audit.py | P2 | V1,V2,V5 | E2 | strict | ACTIVE |
| GUARD-13 | ek_observable_non_authority_guard.py | P3 | V0,V3,V4 | E1 | report/strict | PLANNED |
| GUARD-20 | release_claim_guard.py | P4 | V0,V4 | E1 | strict | PLANNED |
```

---

## 17. Recommended Build Order

```text
0. guards/core/findings.py
1. guards/core/contracts.py
2. guards/core/text_scan.py
3. guards/core/ast_scan.py
4. guards/core/reporting.py
5. GUARD-00 perimeter_kernel_guard.py
6. GUARD-12 coherence_vocabulary_guard.py
7. GUARD-13 ek_observable_non_authority_guard.py
8. GUARD-14 bridge_phi_to_ek_guard.py
9. GUARD-15 projection_boundary_guard.py
10. GUARD-16 memory_trace_boundary_guard.py
11. GUARD-17 determinism_guard.py
12. GUARD-18 import_boundary_guard.py
13. GUARD-19 repo_path_guard.py
14. GUARD-20 release_claim_guard.py
15. GUARD-21 promotion_ledger_guard.py
16. GUARD-22 contract_traceability_guard.py
```

Rationale:

```text
Shared output and contract traceability should stabilize before expanding the guard perimeter.
```

---

## 18. Minimal Repository Patch Plan

### Phase A — Normalize Outputs

Create:

```text
guards/core/findings.py
guards/core/reporting.py
```

Update:

```text
canonical_ontology_guard.py
vectaetos_code_behavior_audit.py
```

Goal:

```text
all guards emit shared JSON + human report
```

---

### Phase B — Extract Contracts

Create:

```text
contracts/perimeter_kernel.yaml
contracts/perimeters/p0_repository.yaml
contracts/perimeters/p1_semantic_vocabulary.yaml
contracts/vectors/forbidden_conversion.yaml
contracts/evidence/evidence_classes.yaml
```

Goal:

```text
guard code scans; contracts define rules
```

---

### Phase C — Add Conversion and Negation Awareness

Implement in:

```text
guards/core/text_scan.py
```

Goal:

```text
detect forbidden conversion
avoid false positives in explicit negation
```

---

### Phase D — Add P3 Guards

Implement:

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
```

Goal:

```text
protect bridge/projection/trace layers from authority drift
```

---

### Phase E — Add P4 Release Boundary

Implement:

```text
GUARD-20 release_claim_guard.py
```

Goal:

```text
prevent static audit claims from being presented as empirical validation
```

---

### Phase F — Add Governance Perimeter

Implement:

```text
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
```

Goal:

```text
prevent status laundering and contract drift
```

---

## 19. Canonical Repo Sentence

Recommended sentence for README / guard docs:

```text
The VECTAETOS perimeter guard system exposes semantic, architectural,
behavioral, runtime, and release-claim drift relative to canonical anchors
and machine-readable contracts. It protects repository state only. It does
not define ontology, prove truth, validate safety, optimize behavior,
authorize deployment, or mutate Φ.
```

Slovak version:

```text
Perimeter guard systém VECTAETOS exponuje sémantický, architektonický,
behaviorálny, runtime a release-claim drift voči kanonickým anchorom
a strojovo čitateľným kontraktom. Chráni iba stav repozitára. Nedefinuje
ontológiu, nedokazuje pravdu, nevaliduje bezpečnosť, neoptimalizuje správanie,
neautorizuje deployment a nemutuje Φ.
```

---

## 20. Final Statement

This model preserves the existing guard inventory while adding a stricter perimeter architecture.

It keeps guards non-agentic, non-authoritative, non-optimizing, non-decisional, and non-mutating toward Φ.

```text
Guard exposes drift.
Contract projects anchor constraints.
Anchor preserves semantic source.
CI refuses repository state.
None of these becomes ontology.
```

End of document.
