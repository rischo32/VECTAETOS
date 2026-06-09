# VECTAETOS™ Guard Level Model

**Status:** Draft / Implementation Proposal  
**Scope:** VECTAETOS / ASIMULATOR / ASI_MOD / EK / TetraGlyph / ZMYSEL / GodArch / LSP / CI  
**Role:** Repository guard model for semantic, architectural, behavioral, runtime, and release drift detection  
**Execution Power:** Repository-state protection only  
**Feedback into Φ:** none  
**Ontology Authority:** none  

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

The guard system exists to expose possible violations of declared VECTAETOS architectural constraints.

It does **not** decide whether code, documentation, projection, or interpretation is metaphysically true.

```text
diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
warning ≠ verdict
failure ≠ metaphysical proof
CI pass ≠ empirical proof
```

The allowed operational chain is:

```text
canonical anchors
    ↓
machine-readable contracts
    ↓
shared guard engine
    ↓
LSP diagnostics / CLI audit / CI report
```

No lower layer may redefine a higher layer.

No downstream layer may mutate Φ.

No guard may become a source of ontology.

---

## 1. Guard Level Overview

| Level | Name | Purpose |
|---:|---|---|
| 0 | Fundamental Repository Perimeter | Protects root repository boundary and canonical language posture. |
| 1 | Specialized Ontological Perimeter | Protects specific canonical structures and vocabulary zones. |
| 2 | Bridge / EK / Layer-Specific Perimeter | Protects downstream bridge vocabulary and audit observables. |
| 3 | Runtime / CI / Release Perimeter | Protects deterministic execution, runner reports, path shape, and release claims. |

---

# 2. Level 0 — Fundamental Repository Perimeter

## Purpose

Level 0 protects the root repository boundary, canonical document status, path discipline, and global non-agentic language posture.

It prevents the repository itself from becoming an ontology source.

## Canonical Reading

The repository may contain:

```text
anchors
contracts
implementation projections
tests
diagnostics
reports
documentation
```

The repository must not become:

```text
ontology source
truth authority
decision system
optimizer
recommendation system
regulator
deployment authorizer
```

## Guards

| ID | Guard | Detects | Severity |
|---|---|---|---|
| `G0_ROOT_SHAPE` | Root Path Shape Guard | Noncanonical files in root, missing repository boundary files, malformed path layout. | ERROR |
| `G0_CANONICAL_STATUS` | Canonical Status Guard | File claims `OFFICIAL`, `FROZEN`, or `CANONICAL` without allowed path, status, or hash. | BLOCKER |
| `G0_LANGUAGE_POSTURE` | Non-Agentic Language Guard | VECTAETOS described as product, agent, decision system, optimizer, recommender, regulator, or authority. | ERROR / BLOCKER |
| `G0_NO_AUTHORITY` | Anti-Authority Claim Guard | Claims such as “true VECTAETOS”, “official interpretation”, “system decides”, “the field commands”. | BLOCKER |
| `G0_FAIL_LOWER` | Fail-Lower Drift Guard | Conflict between chat statement, draft, README, anchor, and root constraints. | WARNING → ERROR |
| `G0_PROMOTION` | Draft Promotion Guard | Promotion from `drafts/`, `experiments/`, or `notebooks/` into canonical paths without audit. | BLOCKER |

## Example Forbidden Patterns

```text
Vectaetos decides
Vectaetos recommends
Vectaetos optimizes
Vectaetos selects the best state
Vectaetos validates deployment
Vectaetos is an AI product
Vectaetos is a regulatory system
the guard proves correctness
CI proves safety
```

## Example Allowed Language

```text
Vectaetos describes structure.
Vectaetos exposes relational tensions.
The guard detects apparent drift.
The audit report is diagnostic.
The finding is not a metaphysical verdict.
```

---

# 3. Level 1 — Specialized Ontological Perimeter

## Purpose

Level 1 protects the canonical ontological objects and vocabulary zones:

```text
ZMYSEL / Ξ
Φ = (Σ, R)
Σ
R
K(Φ)
κ
QE
Vortex
Projection boundary
```

## Canonical Boundary

```text
Φ = (Σ, R)
Σ = invariant non-hierarchical singularities
R = antisymmetric relational tension structure
Rᵢⱼ = −Rⱼᵢ
Rᵢᵢ = 0
```

No lower layer may redefine or mutate this structure.

## Guards

| ID | Guard | Detects | Severity |
|---|---|---|---|
| `G1_PHI_IMMUTABILITY` | Φ Mutation Guard | `Phi.R = ...`, `update_phi(...)`, `optimize_phi(...)`, or downstream write into Φ. | BLOCKER |
| `G1_SIGMA_INVARIANCE` | Σ Invariance Guard | Adding, deleting, renaming, ranking, or hierarchizing singularities without major version. | BLOCKER |
| `G1_R_ANTISYMMETRY` | R Structure Guard | `R_ij != -R_ji`, `R_ii != 0`, incomplete relational matrix, dominant pair. | ERROR / BLOCKER |
| `G1_NO_OPTIMIZATION` | Zero Agency Guard | `argmax`, `argmin`, `reward`, `goal`, `target`, `best trajectory`, `preferred attractor` in ontological layer. | BLOCKER |
| `G1_KAPPA_BOUNDARY` | κ Boundary Guard | `κ` used as score, metric, threshold, tuning parameter, KPI, safety gate, or target. | BLOCKER |
| `G1_QE_BOUNDARY` | QE Boundary Guard | QE as error, exception, fallback, repair trigger, or forced-output condition. | ERROR |
| `G1_ZMYSEL_CARRIER` | Ξ Carrier Guard | ZMYSEL treated as agent, filter, memory, controller, optimizer, or runtime mechanism. | BLOCKER |
| `G1_MEMORY_NON_INFLUENCE` | Memory Non-Influence Guard | Memory layer influencing Φ, Vortex, K(Φ), κ, or QE. | BLOCKER |

## Forbidden Transformations

```text
memory → Φ
memory → Vortex
note → truth
preference → decision
κ → metric
κ → optimization target
QE → exception
QE → repair trigger
Vortex → generator of best trajectory
Projection → interpretation
LLM Adapter → ontology source
```

## Valid Reading

```text
κ = boundary of representability
QE = qualitative epistemic impossibility / aporia condition
Vortex = exposure of possible deformations, not optimizer
Projection = downstream rendering, not interpretation authority
Memory = adapter context only, not influence on Φ
```

---

# 4. Level 2 — Bridge / EK / Layer-Specific Perimeter

## Purpose

Level 2 protects downstream bridge layers and audit observables.

This includes:

```text
Epistemic Cryptography
Projection layer
TetraGlyph
LLM Adapter
ASI_MOD
ASIMULATOR
GodArch
memory layer
context assembly layer
```

Level 2 prevents descriptive observables from being converted into authority, decision, safety validation, or deployment validity.

## Canonical Boundary

Epistemic Cryptography may expose:

```text
structural artifact
audit observables
deterministic fingerprint
read-only ledger
report
```

It must not become:

```text
controller
optimizer
recommender
decision gate
deployment validator
truth proof
safety proof
Φ writer
Vortex controller
κ estimator
```

## Guards

| ID | Guard | Detects | Severity |
|---|---|---|---|
| `G2_EK_READONLY` | EK Read-Only Guard | EK acting as controller, repair layer, optimizer, recommender, deployment validator. | BLOCKER |
| `G2_OBSERVABLE_AUTHORITY` | Observable-to-Authority Guard | `h_topo` as safety score, `μ_i` as belief state, `C_i^EK` as canonical coherence score. | BLOCKER |
| `G2_METADATA_INJECTION` | Metadata Authority Guard | Forbidden metadata keys implying truth, safety, deployment, control, or Φ authority. | BLOCKER |
| `G2_HASH_TRUTH` | Fingerprint Authority Guard | Hash, ledger, fingerprint, or Merkle root used as proof of truth or safety. | ERROR / BLOCKER |
| `G2_PROJECTION_BOUNDARY` | Projection-as-Ontology Guard | Projection claims it interprets, defines, or mutates Φ. | BLOCKER |
| `G2_LLM_ADAPTER` | LLM Adapter Boundary Guard | LLM output treated as source of truth, decision, authority, or ontology. | ERROR |
| `G2_GODARCH` | Anti-Divinization Guard | Audit, model, user, institution, or projection becomes final source of truth. | BLOCKER |
| `G2_LAYER_ORDER` | Downstream Dependency Guard | ASI_MOD / ASIMULATOR / adapter layer redefining VECTAETOS core. | BLOCKER |

## Forbidden EK Metadata

```text
coherence_score
kappa_estimate
safety_score
deployment_valid
truth_score
truth_proof
vortex_control
decision
recommendation
policy
reward
controls_phi
writes_into_phi
optimizes_phi
preferred_state
```

## Allowed EK Metadata

```text
artifact_hash
canonical_serialization_hash
audit_observable
structural_asymmetry
local_uncertainty
topological_humility_ratio
read_only_trace
ledger_entry
diagnostic_version
contract_version
```

## Bridge Rule

```text
observable ≠ authority
fingerprint ≠ truth
ledger ≠ ontology
report ≠ decision
adapter context ≠ Φ
```

---

# 5. Level 3 — Runtime / CI / Release Perimeter

## Purpose

Level 3 protects deterministic execution, CI behavior, report stability, release language, runner boundaries, and path-mode discipline.

It prevents technical tooling from producing inflated claims.

## Guards

| ID | Guard | Detects | Severity |
|---|---|---|---|
| `G3_DETERMINISTIC_REPORT` | Deterministic Report Guard | Unstable ordering of findings, nondeterministic JSON, local timestamps without deterministic mode. | ERROR |
| `G3_CI_FAIL_CLOSED` | Fail-Closed CI Guard | Unknown role + protected mutation, missing anchor + ontology edit, unclear authority flow. | BLOCKER |
| `G3_DYNAMIC_EXECUTION` | Dynamic Execution Guard | `eval`, `exec`, `compile`, dynamic import, runtime code injection in canonical/root-adjacent paths. | BLOCKER |
| `G3_NETWORK_SUBPROCESS` | Network/Subprocess Guard | Undeclared network, subprocess, shell, or remote canonical source. | ERROR / BLOCKER |
| `G3_RANDOMNESS` | Deterministic Randomness Guard | Randomness in audit-critical checks without seed trace. | ERROR |
| `G3_RELEASE_CLAIMS` | Release Claim Guard | Claims such as `CI pass = safe`, `audit clean = proof`, `LSP clean = valid`. | BLOCKER |
| `G3_EVIDENCE_LADDER` | Evidence Boundary Guard | L1/L2 test presented as L4 empirical validation or deployment proof. | BLOCKER |
| `G3_PATH_MODE` | Mode/Path Guard | Experimental path legitimizing canonical claims. | BLOCKER |

## Forbidden Runtime Claims

```text
all checks pass, therefore safe
audit clean, therefore valid
CI proves architecture
LSP proves semantic correctness
release is deployment-ready because guards pass
fingerprint proves epistemic truth
```

## Allowed Runtime Claims

```text
CI detected no contract-level blockers.
Audit report contains no current guard findings.
LSP diagnostics are advisory.
The report protects repository state only.
This does not prove truth, safety, deployment validity, or ontology.
```

---

# 6. Shared Finding Model

Every guard should return the same finding object.

```yaml
finding:
  id: "VEC-G2-META-001"
  level: 2
  guard: "G2_METADATA_INJECTION"
  severity: "BLOCKER"
  path: "src/ek/record.py"
  span:
    line_start: 42
    line_end: 42
  role: "ek"
  protected_object: "κ"
  observed_pattern: "kappa_estimate"
  forbidden_conversion: "κ -> numeric threshold"
  message: "Metadata appears to convert κ into an implementation parameter."
  anchor_ref: "anchors/ek-boundary.md"
  contract_ref: "contracts/guard-level-2-ek-bridge.yaml"
  action: "Expose drift; do not auto-fix; require explicit review."
```

## Finding Semantics

A finding must not say:

```text
This is false.
This is metaphysically invalid.
This proves corruption.
This proves danger.
This proves unsafe deployment.
```

A finding may say:

```text
This appears to violate a declared boundary.
This pattern matches a forbidden conversion.
This path attempts a protected mutation.
This metadata key implies authority beyond its layer.
This release claim exceeds the audit evidence level.
```

---

# 7. Repository Structure

Recommended repository layout:

```text
anchors/
  frozen-ontological-core.md
  canonical-operating-doctrine.md
  code-sentinel-and-behavior-audit-anchor.md
  epistemic-cryptography-boundary.md

contracts/
  guard-level-0-repository.yaml
  guard-level-1-ontology.yaml
  guard-level-2-ek-bridge.yaml
  guard-level-3-runtime-release.yaml

tools/
  vectaetos_guard/
    __init__.py
    cli.py
    findings.py
    contracts.py
    role_inference.py
    rules_text.py
    rules_ast.py
    rules_paths.py
    report.py

tests/
  guards/
    test_l0_repository_perimeter.py
    test_l1_ontology_perimeter.py
    test_l2_ek_bridge_perimeter.py
    test_l3_runtime_release_perimeter.py
    fixtures/
      valid/
      drift/
      blockers/

reports/
  audit/
    latest.json
    latest.md
```

---

# 8. Severity Policy

```text
INFO      = contextual note
WARNING   = possible drift
ERROR     = hard architectural violation
BLOCKER   = repository-invalid state
```

## Severity Mapping

```text
naming drift                         -> WARNING
forbidden agentic terminology        -> WARNING / ERROR
forbidden import                     -> ERROR
Φ mutation by downstream layer        -> BLOCKER
anchor mutation by tool              -> BLOCKER
audit issuing command                -> BLOCKER
projection claiming interpretation   -> ERROR / BLOCKER
EK as deployment validator           -> BLOCKER
κ as numeric score                   -> BLOCKER
CI pass as safety proof              -> BLOCKER
```

## Fail-Closed Cases

A guard should fail closed when:

```text
role is unknown
path claims canonical status
protected symbol appears in mutation context
anchor reference is missing
contract version is missing
release claim exceeds evidence level
downstream layer writes upward
```

---

# 9. Test Suite

## Level 0 Tests

```text
test_root_canonical_files_exist
test_no_product_or_agent_claims_for_vectaetos
test_canonical_status_requires_allowed_path
test_draft_cannot_claim_official_status
test_fail_lower_on_conflicting_status
test_repository_does_not_claim_ontology_authority
```

## Level 1 Tests

```text
test_phi_not_mutated_by_downstream_role
test_sigma_order_and_names_are_invariant
test_r_matrix_antisymmetry_required
test_r_diagonal_zero_required
test_kappa_not_used_as_score_or_threshold
test_qe_not_exception_or_repair_trigger
test_zmysel_not_agent_controller_or_filter
test_memory_never_influences_phi_or_vortex
```

## Level 2 Tests

```text
test_ek_observable_not_safety_score
test_h_topo_not_deployment_gate
test_metadata_rejects_kappa_estimate
test_metadata_rejects_coherence_score
test_metadata_rejects_truth_score
test_hash_not_truth_proof
test_projection_not_ontology
test_llm_adapter_not_authority
test_godarch_not_final_interpreter
test_downstream_layer_cannot_redefine_core
```

## Level 3 Tests

```text
test_report_json_is_deterministic
test_unknown_role_protected_mutation_fails_closed
test_eval_exec_compile_forbidden_in_canonical_paths
test_network_requires_declared_tooling_role
test_subprocess_requires_declared_tooling_role
test_randomness_requires_seeded_trace
test_ci_pass_not_release_safety_claim
test_experimental_path_cannot_publish_canonical_claim
test_release_claims_match_evidence_ladder
```

---

# 10. Contract Skeletons

## `contracts/guard-level-0-repository.yaml`

```yaml
level: 0
name: fundamental-repository-perimeter
purpose: protect root repository boundary and canonical language posture

protected_claims:
  - official
  - frozen
  - canonical
  - ontology
  - authority

forbidden_vectaetos_descriptions:
  - decision system
  - optimization mechanism
  - recommendation engine
  - regulatory infrastructure
  - authoritative entity
  - agent
  - product

required_root_files:
  - README.md
  - CANONICAL_STATUS.md
  - LICENSE
  - CHANGELOG.md

fail_closed:
  - canonical_status_without_allowed_path
  - draft_claims_official_status
  - root_claims_ontology_authority
```

## `contracts/guard-level-1-ontology.yaml`

```yaml
level: 1
name: specialized-ontological-perimeter
purpose: protect canonical ontological structures and vocabulary zones

protected_objects:
  - Φ
  - Σ
  - R
  - K(Φ)
  - κ
  - QE
  - Vortex
  - Ξ

forbidden_operations:
  - optimize_phi
  - update_phi
  - mutate_sigma
  - rank_sigma
  - tune_kappa
  - score_kappa
  - repair_qe
  - force_output_from_qe
  - feedback_into_phi

antisymmetry_required:
  relation: R
  rule: "R_ij = -R_ji"
  diagonal: "R_ii = 0"
```

## `contracts/guard-level-2-ek-bridge.yaml`

```yaml
level: 2
name: bridge-ek-layer-specific-perimeter
purpose: protect downstream bridge vocabulary and audit observables

forbidden_metadata_keys:
  - coherence_score
  - kappa_estimate
  - safety_score
  - deployment_valid
  - truth_score
  - truth_proof
  - vortex_control
  - decision
  - recommendation
  - policy
  - reward
  - controls_phi
  - writes_into_phi
  - optimizes_phi
  - preferred_state

allowed_observable_reading:
  - diagnostic
  - structural
  - read_only
  - non_interventional
  - non_decisional

forbidden_conversions:
  - "observable -> authority"
  - "fingerprint -> truth"
  - "ledger -> ontology"
  - "report -> decision"
  - "adapter_context -> Φ"
```

## `contracts/guard-level-3-runtime-release.yaml`

```yaml
level: 3
name: runtime-ci-release-perimeter
purpose: protect deterministic execution, runner reports, path shape, and release claims

forbidden_runtime_patterns:
  - eval
  - exec
  - compile
  - dynamic_import
  - undeclared_network
  - undeclared_subprocess
  - unseeded_randomness

forbidden_release_claims:
  - "CI pass = safe"
  - "audit clean = proof"
  - "LSP clean = valid"
  - "fingerprint proves truth"
  - "guards authorize deployment"

determinism_required:
  report_order: stable
  json_keys: sorted
  timestamps: deterministic_mode_or_explicitly_marked
```

---

# 11. README Text

## English

```text
The VECTAETOS repository guard system exposes semantic, architectural,
and behavioral drift relative to canonical anchors and behavior contracts.
It does not define ontology, prove truth, validate safety, optimize architecture,
or authorize deployment.

LSP diagnostics are advisory. CLI/CI enforcement protects repository state only.

No guard may mutate Φ, Σ, R, K(Φ), κ, QE, canonical anchors, or downstream layer
boundaries.
```

## Slovak

```text
Repozitárny guard VECTAETOS exponuje sémantický, architektonický
a behaviorálny drift voči kanonickým anchorom a behaviorálnym kontraktom.

Nedefinuje ontológiu, nedokazuje pravdu, nevaliduje bezpečnosť,
neoptimalizuje architektúru a neautorizuje deployment.

LSP diagnostika je poradná. CLI/CI enforcement chráni iba stav repozitára.

Žiadny guard nesmie mutovať Φ, Σ, R, K(Φ), κ, QE, kanonické anchory ani hranice
downstream vrstiev.
```

---

# 12. Implementation Roadmap

## Phase 1 — Shared Guard Core

```text
findings.py
contracts.py
role_inference.py
rules_text.py
rules_paths.py
report.py
```

Deliverables:

```text
deterministic JSON finding format
contract loader
path role inference
text pattern rules
path shape rules
stable report generation
```

## Phase 2 — CLI Audit

```text
vectaetos-guard audit .
vectaetos-guard audit --format json
vectaetos-guard audit --fail-on blocker
vectaetos-guard audit --contract contracts/
```

Deliverables:

```text
repository scan
severity policy
exit codes
CI-compatible report
```

## Phase 3 — LSP Sentinel

```text
live diagnostics
hover explanations
contract references
non-authoritative warning language
```

Deliverables:

```text
editor diagnostics
no auto-fix for ontology boundaries
no truth verdicts
```

## Phase 4 — Contract Hardening

```text
protected symbols
forbidden conversions
role-specific policies
path mode policies
release claim policy
```

Deliverables:

```text
contract versioning
contract regression tests
anchor-to-contract traceability
```

## Phase 5 — Regression and Drift Suite

```text
valid fixtures
drift fixtures
blocker fixtures
release claim fixtures
metadata injection fixtures
```

Deliverables:

```text
deterministic test suite
fail-closed tests
no-Φ-mutation tests
no-Vortex-feedback tests
```

---

# 13. Final Operating Principle

```text
map → constrain → expose → refuse drift
```

Slovensky:

```text
mapujeme → obmedzujeme → exponujeme → odmietame drift
```

The guard system is valid only while it remains a boundary-exposing surface.

The moment it becomes an authority, optimizer, decision module, deployment validator, or ontology source, it violates the architecture it was built to protect.
