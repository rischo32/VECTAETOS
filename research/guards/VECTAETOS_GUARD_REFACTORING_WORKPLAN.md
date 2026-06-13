# VECTAETOS™ Guard Perimeter Refactoring Plan

**Status:** Working implementation plan  
**Document role:** repository refactoring plan, not canonical ontology anchor  
**Scope:** existing guard refactor + future guard implementation  
**Mode:** inspect → report → prepare patch → human applies  
**Connector discipline:** read-only unless a bounded write is explicitly requested later  
**Baseline model:** `guards/VECTAETOS_PERIMETER_GUARD_MODEL_FINAL_HARDENED_UPGRADED.md`  
**Target public path:** `guards/GUARD_PERIMETER_MODEL.md`

---

## 0. Boundary

This plan does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

It only defines a repository implementation path for refactoring guard scripts and adding future perimeter guards.

```text
plan ≠ ontology
guard ≠ truth
contract ≠ ontology
CI ≠ empirical proof
hash ≠ semantic truth
EK event ≠ decision
```

---

## 1. Current repo state

### Observed

The upgraded perimeter model is already inside `guards/`, but under the long generated filename:

```text
guards/VECTAETOS_PERIMETER_GUARD_MODEL_FINAL_HARDENED_UPGRADED.md
```

The model itself recommends the canonical implementation path:

```text
guards/GUARD_PERIMETER_MODEL.md
```

The model baseline is:

```text
Model Version: 0.3-final-hardened-upgraded
Schema Baseline: perimeter-finding-schema/1.0
```

The current `guards/GUARD_TABLE.md` is still organized as a Level 0–3 human-readable map and lists active GUARD-01 through GUARD-11, with GUARD-12 through GUARD-20 planned.

The upgraded model now defines:

```text
Perimeter = scope layer × drift vector × evidence class × enforcement mode × integrity posture
```

and extends the inventory through GUARD-30.

---

## 2. Refactoring principle

Do not rewrite all guards at once.

Refactor through a shared kernel and compatibility layer.

```text
existing guards → adapter output → shared Finding → unified reports → contracts → new guards
```

Forbidden implementation pattern:

```text
rewrite all guards independently
add 20 new guards before shared kernel
move rules into contracts without traceability
make guard clean state imply ontology/safety
```

Allowed implementation pattern:

```text
stabilize shared schema
add compatibility wrapper
refactor active guards one by one
add contracts after schema
add new guards only when core is stable
```

---

## 3. Target architecture

```text
guards/
  GUARD_PERIMETER_MODEL.md
  GUARD_TABLE.md
  README.md

  core/
    __init__.py
    findings.py
    reporting.py
    text_scan.py
    contracts.py
    ast_scan.py
    roles.py
    capabilities.py
    paths.py
    immutable_blob.py
    crypto_integrity.py
    incident_boundary.py

  canonical_ontology_guard.py
  vectaetos_boundary_guard.py
  vectaetos_code_behavior_audit.py
  empirical_claim_guard.py
  repo_layer_boundary_guard.py
  no_feedback_loop_guard.py
  vortex_non_agentic_guard.py
  qe_aporia_guard.py
  triality_guard.py
  vector_drift_guard.py
  master_index_router_guard.py
  coherence_vocabulary_guard.py

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
    timing_side_channel.yaml
    inter_guard_coupling.yaml
    ontology_creep.yaml
    dependency_supply_chain.yaml
    anchor_integrity_drift.yaml
    guard_runtime_integrity.yaml

  evidence/
    evidence_classes.yaml

  roles/
    code_roles.yaml

  paths/
    path_policy.yaml

tests/
  guards/
    fixtures/
      must_pass/
      must_warn/
      must_fail/
```

---

## 4. Unified Finding schema requirements

Every refactored guard must be able to emit the shared finding shape.

Required minimum:

```yaml
id: "VEC-P1-FC-KAPPA-METRIC-001"
guard_id: "GUARD-12"
guard_file: "guards/coherence_vocabulary_guard.py"
rule_id: "FC-KAPPA-METRIC"
contract_schema_version: "1.0"

scope: "P1_semantic_vocabulary"
vector: "V3_forbidden_conversion"
severity: "BLOCKER"
confidence: "high"

path: "formal/example.md"
line: 42
role: "formal"

protected_object: "κ"
observed_pattern: "kappa_estimate"
forbidden_conversion: "κ -> numeric estimate"

negated_context: false
evidence_class_claimed: null
evidence_class_allowed: "E1_static_scan"

anchor_ref: "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md"
contract_ref: "contracts/perimeters/p1_semantic_vocabulary.yaml"

message: "Pattern appears to convert κ from representability boundary into numeric estimate."
safer_form: "Use boundary-of-representability language."

ontology_authority: false
auto_fix_allowed: false
```

Invariants:

```text
ontology_authority must always be false
auto_fix_allowed must default to false
rule_id must be stable
contract_schema_version must be present
finding ids must be deterministic
report ordering must be stable
```

---

## 5. Phase plan

## Phase A — Repo hygiene and naming

Goal:

```text
make current perimeter model visible under the intended path
```

Actions:

```text
1. Rename/copy:
   guards/VECTAETOS_PERIMETER_GUARD_MODEL_FINAL_HARDENED_UPGRADED.md
   → guards/GUARD_PERIMETER_MODEL.md

2. Archive or remove duplicate generated perimeter model files only after checking references.

3. Update GUARD_TABLE.md to point to the upgraded perimeter model.
```

Acceptance:

```text
guards/GUARD_PERIMETER_MODEL.md exists
old generated filename is not the primary reference
GUARD_TABLE does not claim Level 0–3 as final architecture
```

---

## Phase B — Shared reporting core

Create:

```text
guards/core/findings.py
guards/core/reporting.py
```

Responsibilities:

```text
Finding dataclass
Severity / Confidence enums
stable finding id helper
json rendering with sorted keys
human report rendering
safe PASS / FAIL wording
exit code mapping
```

Exit code contract:

```text
0 = no findings at configured enforcement level
1 = blocker finding detected
2 = guard infrastructure failure / confidence unavailable
3 = invalid contract / missing anchor trace / invalid manifest signature
4 = invalid CLI usage
```

Acceptance:

```text
core imports with Python 3.11+
unit fixture can render deterministic JSON twice identically
no output language claims ontology, truth, safety, or deployment validity
```

---

## Phase C — Text scan core

Create:

```text
guards/core/text_scan.py
```

Responsibilities:

```text
window scanning
regex matching
negated context detection
meta-example detection
forbidden conversion detection
path-aware exclusions
```

Required behavior:

```text
"κ is not a metric" → no blocker
"κ_score = 0.84" → blocker
"Forbidden: κ -> metric" in fixture/meta-example → no active blocker, or fixture-mode expected finding
"QEExceptionHandler repairs aporia" → blocker
```

Acceptance:

```text
must-pass fixtures do not produce blockers
must-warn fixtures produce warning only
must-fail fixtures produce the expected rule_id
```

---

## Phase D — Contract loader and traceability

Create:

```text
guards/core/contracts.py
contracts/perimeter_kernel.yaml
contracts/perimeters/p0_repository.yaml
contracts/perimeters/p1_semantic_vocabulary.yaml
contracts/vectors/forbidden_conversion.yaml
contracts/evidence/evidence_classes.yaml
contracts/roles/code_roles.yaml
contracts/paths/path_policy.yaml
```

Responsibilities:

```text
load YAML/JSON
validate schema_version
validate rule id uniqueness
require anchor_ref for strict rules
require vector and evidence_class_allowed
fail closed on invalid contract
```

Acceptance:

```text
strict rule without anchor_ref fails with exit 3
duplicate rule_id fails with exit 3
contract_schema_version appears in all findings
```

---

## Phase E — Refactor active text guards

Refactor order:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-08 qe_aporia_guard.py
3. GUARD-10 vector_drift_guard.py
4. GUARD-02 vectaetos_boundary_guard.py
5. GUARD-04 empirical_claim_guard.py
6. GUARD-05 repo_layer_boundary_guard.py
7. GUARD-06 no_feedback_loop_guard.py
8. GUARD-07 vortex_non_agentic_guard.py
9. GUARD-09 triality_guard.py
11. GUARD-11 master_index_router_guard.py
```

Rationale:

```text
start with the guard most affected by negation/meta-example blindness
then converge all text guards on shared Finding/reporting
```

Each refactor must preserve current behavior unless explicitly changed by a contract.

Acceptance per guard:

```text
--format text|json supported
--fail-on WARN|HARD|BLOCKER supported where applicable
stable JSON output
safe PASS / FAIL language
finding includes rule_id, scope, vector, evidence_class_allowed
```

---

## Phase F — Refactor active diff/AST guards

Refactor order:

```text
1. GUARD-01 canonical_ontology_guard.py
2. GUARD-03 vectaetos_code_behavior_audit.py
```

GUARD-01 additions:

```text
shared Finding output
JSON output
safe PASS / FAIL wording
negation-aware changed-line scan
meta-example/context handling
path policy support
```

GUARD-03 additions:

```text
shared Finding output
JSON output
role capability matrix
import alias resolution
contract-based role policies
explicit evidence_class: E2_AST_contract_compliance
```

Alias cases to catch:

```python
import subprocess as sp
sp.run(["curl", "x"])

from subprocess import run
run(["git", "status"])
```

Acceptance:

```text
existing workflows still run
self-protection remains
trusted base guard behavior remains
AST alias resolution catches subprocess/network/file mutation paths
```

---

## Phase G — Integrity hardening core

Create:

```text
guards/core/immutable_blob.py
guards/core/crypto_integrity.py
guards/core/incident_boundary.py
```

Responsibilities:

```text
anchor byte hashing
guard runtime identity hashing
manifest validation
signed-manifest verification placeholder
incident bundle shape
non-agentic incident language
```

Important boundary:

```text
hash verifies bytes, not truth
signature verifies attestation, not ontology
incident report exposes drift, not decision
```

Acceptance:

```text
anchor hash mismatch produces repository-state finding only
incident bundle contains no autonomous remediation instruction
no EK event is phrased as enforcement authority
```

---

## Phase H — New perimeter guards

Implement only after shared core is stable.

Order:

```text
GUARD-00 perimeter_kernel_guard.py
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
GUARD-23 guard_runtime_integrity_guard.py
GUARD-24 anchor_blob_integrity_guard.py
GUARD-25 ontology_creep_guard.py
GUARD-26 inter_guard_coupling_guard.py
GUARD-27 evidence_attestation_guard.py
GUARD-28 dependency_supply_chain_guard.py
GUARD-29 runtime_sandbox_guard.py
GUARD-30 incident_boundary_guard.py
```

No new guard should define private severity, private report shape, or private evidence language.

---

## 6. GUARD_TABLE update

The current table should be upgraded from:

```text
Level / Status / Required / Primary role
```

to:

```text
ID
Guard
Perimeter
Vectors
Evidence
Enforcement
Integrity posture
Status
Required
Output
```

Example:

```markdown
| ID | Guard | Perimeter | Vectors | Evidence | Enforcement | Integrity | Status |
|---|---|---|---|---|---|---|---|
| GUARD-01 | canonical_ontology_guard.py | P0/P1 | V1,V3,V6,V14 | E1 | strict/fail_closed | trusted-base | ACTIVE |
| GUARD-03 | vectaetos_code_behavior_audit.py | P2 | V1,V2,V5,V15 | E2 | strict | runtime-aware | ACTIVE |
| GUARD-12 | coherence_vocabulary_guard.py | P1/P3 | V3,V8,V12 | E1 | report→strict | text-scan | PLANNED/REFAC |
```

---

## 7. Workflow policy

Because the repository uses strict GitHub Actions policy, workflows should avoid unpinned external actions unless repository policy changes.

Allowed pattern:

```text
manual git checkout using github.token
python3 guard execution
summary written to GITHUB_STEP_SUMMARY
no external upload-artifact unless policy permits pinned internal action
```

Required workflow language:

```text
PASS: No configured blocker was detected within the declared perimeter.
FAIL: Configured blocker detected within declared repository perimeter.
FAIL: Guard infrastructure error; confidence unavailable.
```

Forbidden workflow language:

```text
ontology preserved
VECTAETOS is safe
semantic correctness proven
deployment ready
```

---

## 8. PR plan without connector write

Because connector access is treated as read-only, the assistant should not create the PR directly.

Prepared PR title:

```text
Refactor guard perimeter toward shared hardened model
```

Prepared PR body:

```md
## Summary

This PR begins alignment of the VECTAETOS guard system with the upgraded perimeter model:

- introduces `guards/GUARD_PERIMETER_MODEL.md` as the working implementation proposal
- prepares shared guard-core refactoring
- defines rule-id / contract-schema requirements
- defines path policy and fixture policy
- preserves non-authoritative guard posture

## Boundary

This PR does not define ontology, truth, safety, deployment validity, Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

It only updates repository perimeter implementation structure.

## Acceptance

- no guard output claims truth/safety/deployment validity
- no auto-fix is introduced for ontology-facing text
- no lower layer gains authority over anchors
- future guard findings must include `rule_id` and `contract_schema_version`
```

Suggested branch name:

```text
refactor/hardened-guard-perimeter-core
```

---

## 9. Stop conditions

STOP if any patch introduces:

```text
guard as truth authority
contract as ontology source
CI as empirical proof
hash as semantic truth
signature as ontology
EK event as decision
auto-fix for ontology-facing text
feedback into Φ
Vortex path selection authority
κ as score / threshold / metric
QE as runtime exception / fallback
```

---

## 10. Immediate next action

Recommended first implementation patch:

```text
guards/GUARD_PERIMETER_MODEL.md
guards/core/findings.py
guards/core/reporting.py
```

Not yet:

```text
new GUARD-23 to GUARD-30
full contract extraction
large rewrite of GUARD-01
large rewrite of GUARD-03
```

Reason:

```text
shared output schema must stabilize before expanding the perimeter
```

End of plan.
