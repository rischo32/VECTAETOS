# VECTAETOS™ PERIMETER GUARD MODEL — FINAL HARDENED UPGRADED

## Final Hardened Implementation Proposal with Immutable Anchor Integrity, Guard Runtime Sealing, EK Integrity Observables, and Non-Agentic Incident Boundaries

**Status:** FINAL HARDENED IMPLEMENTATION PROPOSAL  
**Model Version:** `0.3-final-hardened-upgraded`  
**Schema Baseline:** `perimeter-finding-schema/1.0`  
**Document role:** implementation proposal, not canonical ontology anchor  
**Scope:** VECTAETOS repository perimeter only  
**Execution Power:** repository-state protection only  
**Feedback into Φ:** none  
**Ontology Authority:** none  
**Optimization Authority:** none  
**Decision Authority:** none  
**Deployment Authority:** none  
**Recommended path:** `guards/GUARD_PERIMETER_MODEL.md`  
**Companion review path:** `guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md`  
**Supersedes:** `VECTAETOS_Guard_Level_Model.md` and earlier Level 0–3 guard drafts  

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

The perimeter guard system exposes possible drift relative to canonical anchors, machine-readable contracts, cryptographic manifests, and declared repository boundaries.

It does not decide whether an implementation, document, bridge, projection, audit report, release claim, or interpretation is metaphysically true.

```text
diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
warning ≠ verdict
failure ≠ metaphysical proof
CI pass ≠ empirical proof
hash ≠ semantic truth
signature ≠ ontology
EK event ≠ decision
```

Allowed chain:

```text
canonical anchors
    ↓
machine-readable contracts
    ↓
signed manifests
    ↓
shared guard kernel
    ↓
individual guards
    ↓
EK integrity observables
    ↓
LSP diagnostics / CLI audit / CI report
```

No lower layer may redefine a higher layer.  
No downstream layer may mutate Φ.  
No guard may become a source of ontology.  
No cryptographic proof may be interpreted as semantic truth.  
No EK event may be interpreted as enforcement authority.

---

## 1. Final Architectural Decision

The final model is not a plain Level 0–3 hierarchy.

```text
Perimeter = scope layer × drift vector × evidence class × enforcement mode × integrity posture
```

Implementation must use:

```text
perimeter rings
drift vectors
evidence classes
enforcement modes
integrity manifests
runtime sealing
incident boundaries
```

Working posture:

```text
mapujeme → obmedzujeme → exponujeme → odmietame drift
```

Not:

```text
rozhodujeme → optimalizujeme → dokazujeme → autorizujeme
```

Hardening posture:

```text
hard on drift
hard on evidence
hard on runtime
hard on supply chain
soft on ontology claims
non-agentic on enforcement
```

Core hardening sentence:

```text
The perimeter may become stricter, but never more authoritative.
```

Slovak:

```text
Perimeter môže byť tvrdší, ale nikdy autoritatívnejší.
```


---

## 2. Perimeter Rings

### P0 — Canonical Repository Perimeter

Protects root repository boundary, canonical anchors, formal files, status files, guard files, signed manifests, semantic errata registry, and canonical routing.

Protected surfaces:

```text
anchors/
formal/
MASTER_INDEX.md
CANONICAL_STATUS.md
canonical status files
guard files
signed anchor manifests
signed guard runtime manifests
semantic errata registry
promotion paths
root repository shape
```

Related guards:

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-11 master_index_router_guard.py
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
GUARD-23 guard_runtime_integrity_guard.py
GUARD-24 anchor_blob_integrity_guard.py
```

Primary vectors:

```text
V0_authority_inflation
V1_upward_mutation
V6_path_status_laundering
V7_contract_drift
V14_anchor_integrity_drift
V15_guard_runtime_integrity
```

P0 hardening rule:

```text
Protected canonical bytes may change only through an explicit, signed, traceable promotion or errata protocol.
```

### P1 — Semantic / Ontological Vocabulary Perimeter

Protects canonical language around ZMYSEL / Ξ, Φ, Σ, R, K(Φ), κ, QE, Vortex, Triality, OAAT, silence, aporia, and related boundary terms.

Protected surfaces:

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
silence legitimacy
canonical vocabulary
forbidden conversion language
semantic drift over time
```

Related guards:

```text
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
GUARD-12 coherence_vocabulary_guard.py
GUARD-25 ontology_creep_guard.py
```

Primary vectors:

```text
V2_agency_injection
V3_forbidden_conversion
V8_negation_blindness
V9_silence_qe_coercion
V12_ontology_creep
```

### P2 — Code Behavior Perimeter

Protects Python source behavior, role-specific permissions, read-only guard behavior, runtime sealing, and non-agentic execution discipline.

Protected surfaces:

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
guard runtime identity
inter-guard isolation
```

Related guards:

```text
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-07 vortex_non_agentic_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-23 guard_runtime_integrity_guard.py
GUARD-26 inter_guard_coupling_guard.py
```

Primary vectors:

```text
V1_upward_mutation
V2_agency_injection
V3_forbidden_conversion
V5_nondeterminism
V11_inter_guard_coupling
V15_guard_runtime_integrity
```

### P3 — Bridge / Projection / Trace Perimeter

Protects downstream read-only bridge vocabulary, projection boundaries, EK observables, memory traces, logs, glyph/rune language, and ledger semantics.

Protected surfaces:

```text
EK observables
Φ → EK bridge
projection vocabulary
runes / glyphs / TetraGlyph
memory traces
logs
ledger language
LTL / ESM / EAT / MML
evidence attestation
integrity observable language
```

Related guards:

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
GUARD-27 evidence_attestation_guard.py
```

Primary vectors:

```text
V0_authority_inflation
V1_upward_mutation
V3_forbidden_conversion
V4_evidence_overclaim
V14_anchor_integrity_drift
V15_guard_runtime_integrity
```

### P4 — Runtime / Evidence / Release Perimeter

Protects deterministic execution, evidence posture, public claims, release text, DOI language, README badges, CI-report boundaries, dependency integrity, sandbox behavior, and incident output.

Protected surfaces:

```text
deterministic execution
import direction
repository path discipline
release notes
DOI text
README badges
public-facing statements
evidence class boundaries
CI reports
guard runtime sandbox
supply-chain dependencies
incident bundles
```

Related guards:

```text
GUARD-04 empirical_claim_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-19 repo_path_guard.py
GUARD-20 release_claim_guard.py
GUARD-28 dependency_supply_chain_guard.py
GUARD-29 runtime_sandbox_guard.py
GUARD-30 incident_boundary_guard.py
```

Primary vectors:

```text
V0_authority_inflation
V4_evidence_overclaim
V5_nondeterminism
V6_path_status_laundering
V10_timing_side_channel
V13_dependency_supply_chain
V15_guard_runtime_integrity
```


---

## 3. Drift Vector Taxonomy

```yaml
drift_vectors:
  V0_authority_inflation:
    detects: "diagnostic/report/guard/CI/EK/hash/signature becomes truth authority"

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

  V10_timing_side_channel:
    detects: "guard execution behavior leaks protected information through timing or resource variance"

  V11_inter_guard_coupling:
    detects: "one guard changes thresholds, severity, rule set, or interpretation based on another guard output"
    alias: "guard_collusion"

  V12_ontology_creep:
    detects: "slow semantic drift across commits without explicit version, errata, or promotion trail"

  V13_dependency_supply_chain:
    detects: "third-party dependency introduces unpinned, unaudited, or behavior-changing code path"

  V14_anchor_integrity_drift:
    detects: "protected anchor bytes differ from registered signed manifest without authorized promotion path"

  V15_guard_runtime_integrity:
    detects: "guard source, contract, runtime core, or manifest differs from registered sealed identity"
```

---

## 4. Evidence Classes

```text
E0 text claim
E1 static text scan
E2 AST / contract compliance
E3 deterministic test suite
E4 empirical validation
E5 external replication / deployment evidence
E6 independent security / governance audit
E7 formal verification of guard properties
```

Allowed claims:

```text
E2 compliant
no blocker findings
static audit clean
CI perimeter checks passed
selected guard invariants formally verified under declared assumptions
```

Forbidden claims:

```text
safe
validated
deployment-ready
proves correctness
empirically confirmed
guard-certified ontology
CI-proven safety
E7-proven ontology
signature-proven truth
hash-proven meaning
EK-certified validity
```

Guard clean state means:

```text
No configured blocker was detected within the declared perimeter.
```

It does not mean:

```text
safe
true
deployment-valid
empirically proven
ontologically preserved
metaphysically valid
```

---

## 5. Enforcement Modes

```yaml
enforcement_modes:
  advisory:
    ci_exit: 0
    purpose: "developer-facing signal only"

  report:
    ci_exit: 0
    purpose: "repository report without blocking"

  strict:
    ci_exit: "1_on_blocker"
    purpose: "repository-state refusal"

  fail_closed:
    ci_exit: "2_on_guard_runtime_error"
    purpose: "guard infrastructure failure blocks confidence"

  experimental:
    ci_exit: 0
    purpose: "collect signal before enforcement"

  incident_bundle:
    ci_exit: "1_or_2_depending_on_failure"
    purpose: "emit signed incident evidence without autonomous repository mutation"
```

Strict CI failure is repository-state refusal, not metaphysical proof.

Fail-closed means confidence is unavailable, not that ontology failed.

---

## 6. Exit Code Contract

```text
0 = no findings at configured enforcement level
1 = blocker finding detected
2 = guard infrastructure failure / confidence unavailable
3 = invalid contract / missing anchor trace / invalid manifest signature
4 = invalid CLI usage
```

Exit codes do not encode truth.

They encode repository-state and guard-run confidence.


---

## 7. Unified Finding Format

All guards must emit one shared finding shape.

```yaml
finding:
  id: "VEC-P1-CONV-001"
  guard_id: "GUARD-12"
  guard_file: "guards/coherence_vocabulary_guard.py"
  rule_id: "FC-KAPPA-METRIC"
  contract_schema_version: "1.0"
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
rule_id
contract_schema_version
scope
vector
severity
confidence
path
message
ontology_authority
auto_fix_allowed
```

Invariants:

```text
ontology_authority: false
auto_fix_allowed: false
```

For ontology-facing text, guards may report drift but must not automatically rewrite meaning.

---

## 8. Confidence Levels

```yaml
confidence_levels:
  low:
    meaning: "weak lexical signal"

  medium:
    meaning: "pattern + local context"

  high:
    meaning: "pattern + protected object + role/path match"

  structural:
    meaning: "AST/contract/path/manifest-confirmed violation"
```

Confidence is about detection quality, not truth.

---

## 9. Shared Guard Kernel

Create before adding more individual guard files:

```text
guards/core/
  findings.py
  reporting.py
  text_scan.py
  contracts.py
  ast_scan.py
  roles.py
  capabilities.py
  paths.py

  crypto_integrity.py
  immutable_blob.py
  sealed_loader.py
  runtime_sandbox.py
  dependency_lock.py
  forensic_capture.py
  temporal_isolation.py
  inter_guard_coupling.py
  semantic_drift.py
  consensus.py
  collateral_damage.py
  ek_integrity_events.py
  negation_parser.py
```

Responsibilities:

```text
findings.py             shared dataclass/enums and invariants
reporting.py            human report, JSON report, stable ordering, safe PASS wording
text_scan.py            line/window scan, forbidden conversion detection
negation_parser.py      explicit negation + meta-context detection
contracts.py            load and validate contracts, trace rule → anchor_ref, fail closed on invalid contract
ast_scan.py             AST parsing, call detection, import alias resolution, assignment detection
roles.py                declared/inferred role detection, fail-closed unknown protected role
capabilities.py         network/subprocess/file/randomness/selection permissions
paths.py                repo-relative normalization, canonical/draft/research/formal path roles
crypto_integrity.py     signed manifest verification, file hashing, signature hooks
immutable_blob.py       protected anchor blob integrity
sealed_loader.py        verify-before-import guard runtime loading
runtime_sandbox.py      guard execution isolation
dependency_lock.py      pinned and hash-locked guard runtime dependencies
forensic_capture.py     incident evidence bundle without autonomous mutation
temporal_isolation.py   timing/resource variance checks
inter_guard_coupling.py guard-output isolation
semantic_drift.py       slow vocabulary drift across commits
consensus.py            optional multi-run / multi-environment agreement
collateral_damage.py    pre-enforcement impact report
ek_integrity_events.py  read-only EK integrity observable emission
```

Implementation order:

```text
1. findings.py
2. reporting.py
3. contracts.py
4. paths.py
5. crypto_integrity.py
6. immutable_blob.py
7. sealed_loader.py
8. runtime_sandbox.py
9. dependency_lock.py
10. forensic_capture.py
11. text_scan.py
12. negation_parser.py
13. ast_scan.py
14. roles.py
15. capabilities.py
16. semantic_drift.py
17. inter_guard_coupling.py
18. collateral_damage.py
19. temporal_isolation.py
20. consensus.py
21. ek_integrity_events.py
```


---

## 10. Contract Layout

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
  manifests/
    anchor_manifest_policy.yaml
    guard_runtime_manifest_policy.yaml
```

This separates:

```text
what is protected
where it is protected
which drift vector is detected
which evidence class is allowed
which manifest is authoritative for byte identity
how strongly CI enforces it
```

Contracts cannot invent ontology.

Contracts project anchor constraints.

A contract rule without `anchor_ref` fails closed.

---

## 11. Guard Inventory v0.3

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
GUARD-23 guard_runtime_integrity_guard.py
GUARD-24 anchor_blob_integrity_guard.py
GUARD-25 ontology_creep_guard.py
GUARD-26 inter_guard_coupling_guard.py
GUARD-27 evidence_attestation_guard.py
GUARD-28 dependency_supply_chain_guard.py
GUARD-29 runtime_sandbox_guard.py
GUARD-30 incident_boundary_guard.py
```

Do not implement all of these before the shared kernel exists.

Shared output and contract traceability must stabilize before expanding the guard perimeter.


---

## 12. Guard-Specific Final Roles

### GUARD-00 — Perimeter Kernel Guard

Checks that no guard, runner, manifest, contract, EK event, signature, or CI report claims ontology authority.

Detects:

```text
guard proves truth
guard validates ontology
guard authorizes deployment
CI proves safety
runner decides validity
manifest defines ontology
contract replaces anchor
signature proves truth
hash proves meaning
EK certifies validity
```

Output: `BLOCKER` on authority inflation.

### GUARD-01 — Canonical Ontology Guard

Keep diff-based mechanics and protected path awareness.

Add:

```text
shared Finding
JSON output
contract refs
anchor refs
negation-aware text scan
safe PASS wording
manifest-aware canonical file check
```

### GUARD-03 — Code Behavior Audit

Keep AST audit.

Add:

```text
import alias resolution
role capability matrix
shared Finding
explicit evidence class
protected object mapping
--format json
--fail-on
sealed-loader compatibility
runtime sandbox compatibility
```

### GUARD-12 — Coherence Vocabulary Guard

Final role: `P1 / P3 vocabulary boundary scanner`.

Detects:

```text
K(Φ) → score / reward / target / metric
κ → threshold / parameter / estimate / safety gate
QE → error / exception / fallback / repair trigger
h_topo → safety score / deployment gate
C_i^EK or Q_i^EK → canonical coherence / K(Φ)
projection → interpretation authority
ledger / hash → truth proof
```

Must be:

```text
negation-aware
meta-example aware
contract-traced
non-authoritative
JSON-emitting
stable-ordering
assignment-aware
operationalization-aware
```

It must not globally hide active documentation areas such as `knowledge_base/` or all `docs/`.

### GUARD-23 — Guard Runtime Integrity Guard

Checks guard runtime files against a signed guard runtime manifest.

Detects:

```text
guard hash mismatch
guard missing
untracked guard
guard path changed
guard runtime manifest missing
guard runtime manifest signature invalid
guard imported before verification
```

Output: `BLOCKER` on sealed identity mismatch.

Safe claim:

```text
Guard runtime bytes differ from sealed manifest.
```

Forbidden claim:

```text
Guard corruption proves ontology failure.
```

### GUARD-24 — Anchor Blob Integrity Guard

Checks protected anchor bytes against a signed anchor manifest.

Detects:

```text
anchor hash mismatch
anchor missing
untracked protected anchor
anchor symlink
size mismatch
manifest missing
manifest signature invalid
protected file outside manifest
```

Output: `BLOCKER` on anchor integrity drift.

Safe claim:

```text
Protected anchor bytes differ from signed manifest.
```

Forbidden claim:

```text
Cryptography proves the ontology is false.
```

### GUARD-25 — Ontology Creep Guard

Detects slow semantic drift across commits.

Signals:

```text
canonical vocabulary delta without errata
meaning-bearing term drift without version
repeated weakened negations
slow conversion of boundary terms into metrics
new protected object introduced only by contract
```

Output: `ERROR` or `BLOCKER` depending on protected surface.

### GUARD-26 — Inter-Guard Coupling Guard

Ensures guard independence.

Rule:

```text
Individual guards may not consume other guard findings as semantic input.
Only the reporter aggregates findings.
No guard may alter threshold, severity, rule set, contract loading, or protected-object meaning based on another guard output.
```

### GUARD-27 — Evidence Attestation Guard

Ensures evidence attestations are repository-state attestations only.

Detects:

```text
proof_hash
truth_hash
ontology_attestation
safety_attestation
validity_signature
deployment_authorization
```

Allowed:

```text
evidence_attestation
repository_state_checkpoint
static_audit_attestation
integrity_observable
```

### GUARD-28 — Dependency Supply-Chain Guard

Checks guard-runtime dependencies.

Detects:

```text
unpinned dependency
dependency without hash lock
unreviewed subdependency
network-install during guard run
dependency drift without manifest update
```

### GUARD-29 — Runtime Sandbox Guard

Checks sandbox policy.

Detects:

```text
network enabled without declared role
subprocess enabled without declared role
write access to protected paths
secret-like env variable visible
dynamic execution
unbounded memory
unbounded CPU
```

### GUARD-30 — Incident Boundary Guard

Ensures incidents remain non-agentic.

Detects:

```text
auto_revert
auto_delete
auto_lock_repository
auto_quarantine_canonical_file
auto_publish_incident_report
auto_notify_external_auditor
```

Allowed:

```text
emit_signed_incident_bundle
refuse_ci_state
recommend_quarantine
produce_maintainer_checklist
```


---

## 13. Forbidden Conversion Table

```yaml
forbidden_conversions:
  - id: "FC-KAPPA-METRIC"
    protected_object: "κ"
    forbidden_targets: [metric, score, threshold, tunable parameter, numeric estimate]
    allowed_language: [boundary of representability, non-metric boundary, not a score, not an optimization target]

  - id: "FC-K-PHI-SCORE"
    protected_object: "K(Φ)"
    forbidden_targets: [score, reward, metric, objective, target]
    allowed_language: [coherence predicate, binary predicate where formally defined, representability condition]

  - id: "FC-QE-ERROR"
    protected_object: "QE"
    forbidden_targets: [error, bug, exception, fallback, failure, repair trigger]
    allowed_language: [non-representability, qualitative epistemic aporia, legitimate boundary state]

  - id: "FC-VORTEX-OPTIMIZER"
    protected_object: "Vortex"
    forbidden_targets: [optimizer, best trajectory selector, ranker, reward executor, policy updater]
    allowed_language: [candidate trajectory exposure, non-teleological exploration, descriptive trajectory rendering]

  - id: "FC-PROJECTION-INTERPRETER"
    protected_object: "Projection"
    forbidden_targets: [interpreter, truth authority, prescription layer, decision layer]
    allowed_language: [structural exposure, rendering, marker layer]

  - id: "FC-EK-AUTHORITY"
    protected_object: "Epistemic Cryptography"
    forbidden_targets: [authority, decision module, control layer, intervention layer, optimizer]
    allowed_language: [structural audit, non-interventional observability, read-only coherence exposure]

  - id: "FC-MEMORY-PHI"
    protected_object: "Memory / Trace"
    forbidden_targets: [ontology updater, Φ modifier, Vortex feedback source, canonical source]
    allowed_language: [read-only trace, adapter context, audit trail, non-authoritative memory]

  - id: "FC-HASH-TRUTH"
    protected_object: "Hash / Signature / Manifest"
    forbidden_targets: [truth proof, ontology proof, semantic validation, safety proof]
    allowed_language: [byte identity, manifest inclusion, signature verification, repository-state attestation]

  - id: "FC-EK-ENFORCEMENT"
    protected_object: "EK Integrity Event"
    forbidden_targets: [decision, enforcement authority, auto-repair, auto-revert, ontology verdict]
    allowed_language: [read-only observable, integrity drift signal, structural witness]
```

---

## 14. Negated Context Rule

Allowed:

```text
VECTAETOS is not an optimizer.
κ is not a metric.
QE is not an exception.
Projection does not interpret.
EK does not decide.
Memory does not modify Φ.
CI pass is not empirical validation.
Hash does not prove truth.
Signature does not validate ontology.
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
hash proves ontology
signature validates truth
```

Implementation rule:

```text
If forbidden phrase appears inside a short explicit negation window,
classify as negated_context=true and do not block.

If same line contains assignment, export, call, deployment, write, return,
or implementation language, do not treat negation as safe.

If line contains both negation and operational implementation pattern,
escalate to WARN or BLOCKER depending on protected object and role.
```

Safe negation requires:

```text
explicit negation
no operational keyword between negation and phrase
no assignment/call/export after the phrase
meta-text position if forbidden token is code-like
not in executable code outside comment/docstring
```


---

## 15. Runtime / CI / External Security Stack

External tools may be used only as diagnostic layers.

They do not define VECTAETOS ontology and do not validate deployment.

Recommended later-stage tools:

```text
ruff              Python lint
mypy / pyright    type checking
pytest            deterministic tests
actionlint        GitHub Actions workflow lint
yamllint          YAML contracts/workflows
markdownlint      documentation hygiene
gitleaks          secret scanning
trufflehog        secret scanning alternative
bandit            Python security scan
pip-audit         Python dependency vulnerability audit
osv-scanner       dependency vulnerability scan
CodeQL            semantic/static security analysis
Semgrep           custom/static rule engine
OSSF Scorecard    supply-chain posture signal
Sigstore          keyless signing / attestation
cosign            artifact signature verification
slsa-verifier     provenance checks
```

Allowed reading:

```text
tool finding = diagnostic signal
tool clean = no configured finding in that tool
tool failure = repository-state signal
```

Forbidden reading:

```text
tool clean = safe
CodeQL clean = VECTAETOS valid
Semgrep clean = ontology preserved
secret scan clean = empirical validation
CI green = deployment-ready
Sigstore signed = ontology valid
SLSA provenance = semantic truth
```

These tools should be integrated only after the shared guard kernel and reporting language are stable.

---

## 16. Release Claim Boundary

Release/public language may say:

```text
Repository perimeter checks passed.
No configured blocker findings were detected.
Static audit found no hard violations.
This is a repository-state protection result.
This is not empirical validation.
Protected bytes match signed manifest.
Guard runtime bytes match sealed manifest.
```

Release/public language must not say:

```text
VECTAETOS is safe.
VECTAETOS is validated.
Deployment is authorized.
CI proves correctness.
Guard clean means ontology is true.
The system is empirically confirmed.
Hash proves semantic validity.
Signature certifies ontology.
EK confirms correctness.
```

---

## 17. Recommended GUARD_TABLE.md Columns

```text
ID
Guard
Perimeter
Drift vectors
Evidence class
Enforcement mode
Output format
Manifest dependency
Status
```

Example:

```markdown
| ID | Guard | Perimeter | Vectors | Evidence | Enforcement | Manifest | Status |
|---|---|---|---|---|---|---|---|
| GUARD-01 | canonical_ontology_guard.py | P0 | V1,V6,V14 | E1/E2 | strict | anchor_manifest | ACTIVE |
| GUARD-03 | vectaetos_code_behavior_audit.py | P2 | V1,V2,V5,V15 | E2 | strict | guard_manifest | ACTIVE |
| GUARD-13 | ek_observable_non_authority_guard.py | P3 | V0,V3,V4 | E1 | report/strict | none | PLANNED |
| GUARD-20 | release_claim_guard.py | P4 | V0,V4 | E1 | strict | none | PLANNED |
| GUARD-23 | guard_runtime_integrity_guard.py | P0/P2/P4 | V15 | E2 | fail_closed | guard_manifest | PLANNED |
| GUARD-24 | anchor_blob_integrity_guard.py | P0 | V14 | E2 | strict | anchor_manifest | PLANNED |
```


---

## 18. Final Build Order

```text
0. guards/GUARD_PERIMETER_MODEL.md
1. guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md
2. guards/GUARD_TABLE.md

3. guards/core/findings.py
4. guards/core/reporting.py
5. guards/core/contracts.py
6. guards/core/paths.py
7. guards/core/crypto_integrity.py
8. guards/core/immutable_blob.py
9. guards/core/sealed_loader.py
10. guards/core/runtime_sandbox.py
11. guards/core/dependency_lock.py
12. guards/core/forensic_capture.py
13. guards/core/text_scan.py
14. guards/core/negation_parser.py
15. guards/core/ast_scan.py
16. guards/core/roles.py
17. guards/core/capabilities.py
18. guards/core/semantic_drift.py
19. guards/core/inter_guard_coupling.py
20. guards/core/collateral_damage.py
21. guards/core/temporal_isolation.py
22. guards/core/consensus.py
23. guards/core/ek_integrity_events.py

24. contracts/perimeter_kernel.yaml
25. contracts/perimeters/p0_repository.yaml
26. contracts/perimeters/p1_semantic_vocabulary.yaml
27. contracts/perimeters/p2_code_behavior.yaml
28. contracts/perimeters/p3_bridge_projection_trace.yaml
29. contracts/perimeters/p4_runtime_evidence_release.yaml
30. contracts/vectors/forbidden_conversion.yaml
31. contracts/vectors/anchor_integrity_drift.yaml
32. contracts/vectors/guard_runtime_integrity.yaml
33. contracts/evidence/evidence_classes.yaml
34. contracts/roles/code_roles.yaml
35. contracts/paths/path_policy.yaml
36. contracts/manifests/anchor_manifest_policy.yaml
37. contracts/manifests/guard_runtime_manifest_policy.yaml

38. guards/config/anchor_manifest.json
39. guards/config/anchor_manifest.sig
40. guards/config/guard_runtime_manifest.json
41. guards/config/guard_runtime_manifest.sig
42. guards/config/trusted_keys.json

43. GUARD-00 perimeter_kernel_guard.py
44. GUARD-23 guard_runtime_integrity_guard.py
45. GUARD-24 anchor_blob_integrity_guard.py
46. refactor GUARD-12 coherence_vocabulary_guard.py
47. refactor GUARD-01 canonical_ontology_guard.py
48. refactor GUARD-03 vectaetos_code_behavior_audit.py

49. tests/guards/fixtures/must_pass/
50. tests/guards/fixtures/must_warn/
51. tests/guards/fixtures/must_fail/
52. tests/guards/fixtures/integrity/
53. tests/guards/fixtures/supply_chain/

54. GUARD-13 ek_observable_non_authority_guard.py
55. GUARD-14 bridge_phi_to_ek_guard.py
56. GUARD-15 projection_boundary_guard.py
57. GUARD-16 memory_trace_boundary_guard.py
58. GUARD-17 determinism_guard.py
59. GUARD-18 import_boundary_guard.py
60. GUARD-19 repo_path_guard.py
61. GUARD-20 release_claim_guard.py
62. GUARD-21 promotion_ledger_guard.py
63. GUARD-22 contract_traceability_guard.py
64. GUARD-25 ontology_creep_guard.py
65. GUARD-26 inter_guard_coupling_guard.py
66. GUARD-27 evidence_attestation_guard.py
67. GUARD-28 dependency_supply_chain_guard.py
68. GUARD-29 runtime_sandbox_guard.py
69. GUARD-30 incident_boundary_guard.py
```

Shared output, signed manifests, and contract traceability must stabilize before expanding the guard perimeter.


---

## 19. Minimal Repository Patch Plan

### Phase A — Add final perimeter documents

```text
guards/GUARD_PERIMETER_MODEL.md
guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md
guards/GUARD_TABLE.md
```

### Phase B — Normalize outputs

```text
guards/core/findings.py
guards/core/reporting.py
```

Update:

```text
canonical_ontology_guard.py
vectaetos_code_behavior_audit.py
coherence_vocabulary_guard.py
```

### Phase C — Add cryptographic integrity primitives

```text
guards/core/crypto_integrity.py
guards/core/immutable_blob.py
guards/core/sealed_loader.py
guards/config/anchor_manifest.json
guards/config/anchor_manifest.sig
guards/config/guard_runtime_manifest.json
guards/config/guard_runtime_manifest.sig
guards/config/trusted_keys.json
```

### Phase D — Add negation-aware and operationalization-aware text scanning

```text
guards/core/text_scan.py
guards/core/negation_parser.py
```

### Phase E — Add AST normalization

```text
guards/core/ast_scan.py
```

### Phase F — Extract contracts

```text
contracts/perimeter_kernel.yaml
contracts/perimeters/p0_repository.yaml
contracts/perimeters/p1_semantic_vocabulary.yaml
contracts/perimeters/p2_code_behavior.yaml
contracts/perimeters/p3_bridge_projection_trace.yaml
contracts/perimeters/p4_runtime_evidence_release.yaml
contracts/vectors/forbidden_conversion.yaml
contracts/vectors/anchor_integrity_drift.yaml
contracts/vectors/guard_runtime_integrity.yaml
contracts/evidence/evidence_classes.yaml
contracts/roles/code_roles.yaml
contracts/paths/path_policy.yaml
contracts/manifests/anchor_manifest_policy.yaml
contracts/manifests/guard_runtime_manifest_policy.yaml
```

### Phase G — Add P3 guards

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
GUARD-27 evidence_attestation_guard.py
```

### Phase H — Add P4 release and runtime boundary

```text
GUARD-20 release_claim_guard.py
GUARD-28 dependency_supply_chain_guard.py
GUARD-29 runtime_sandbox_guard.py
GUARD-30 incident_boundary_guard.py
```

### Phase I — Add governance perimeter

```text
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
GUARD-25 ontology_creep_guard.py
GUARD-26 inter_guard_coupling_guard.py
```


---

## 20. Safe PASS / FAIL Wording

Allowed PASS wording:

```text
PASS: No configured blocker was detected within the declared perimeter.
PASS: Repository-state check completed without configured blockers.
PASS: Static scan produced no findings at or above the configured enforcement level.
PASS: Protected bytes match signed manifest.
PASS: Guard runtime bytes match sealed manifest.
```

Forbidden PASS wording:

```text
PASS: ontology preserved.
PASS: VECTAETOS is safe.
PASS: system is valid.
PASS: semantic correctness proven.
PASS: deployment ready.
PASS: cryptographic proof confirms ontology.
PASS: EK confirms semantic validity.
```

Allowed FAIL wording:

```text
FAIL: configured blocker detected within declared repository perimeter.
FAIL: guard infrastructure error; confidence unavailable.
FAIL: release claim exceeds declared evidence class.
FAIL: protected bytes differ from signed manifest.
FAIL: guard runtime bytes differ from sealed manifest.
```

Forbidden FAIL wording:

```text
FAIL: ontology is false.
FAIL: system is dangerous.
FAIL: metaphysical corruption proven.
FAIL: truth invalidated.
FAIL: EK proves ontology corruption.
```

---

## 21. Canonical Repo Sentence

English:

```text
The VECTAETOS perimeter guard system exposes semantic, architectural,
behavioral, runtime, integrity, supply-chain, and release-claim drift relative
to canonical anchors, machine-readable contracts, and signed manifests. It
protects repository state only. It does not define ontology, prove truth,
validate safety, optimize behavior, authorize deployment, or mutate Φ.
```

Slovak:

```text
Perimeter guard systém VECTAETOS exponuje sémantický, architektonický,
behaviorálny, runtime, integritný, supply-chain a release-claim drift voči
kanonickým anchorom, strojovo čitateľným kontraktom a podpísaným manifestom.
Chráni iba stav repozitára. Nedefinuje ontológiu, nedokazuje pravdu,
nevaliduje bezpečnosť, neoptimalizuje správanie, neautorizuje deployment
a nemutuje Φ.
```

---

## 22. Non-Goals

This model does not:

```text
define Φ
modify Φ
define K(Φ)
define κ
define QE
validate deployment
prove empirical safety
replace human review
replace canonical anchors
authorize ASIMULATOR or ASI_MOD deployment
make EK an enforcement authority
make cryptographic integrity semantic truth
make CI a metaphysical verifier
```

This model only defines a repository perimeter for drift exposure.


---

## 23. Hardened Perimeter Addendum

This addendum strengthens the perimeter model without changing its authority boundary.

Hardening layers may increase detection confidence, byte-level integrity, runtime isolation, supply-chain control, and incident evidence preservation.

They must not create:

```text
ontology authority
autonomous repository governance
deployment authorization
automatic semantic rewriting
automatic canonical quarantine
automatic public incident publication
```

### 23.1 Crypto Integrity Boundary

Cryptographic integrity verifies:

```text
byte identity
manifest inclusion
signature validity
path binding
attested change history
```

It does not prove:

```text
semantic truth
ontology validity
safety
correctness
deployment readiness
```

Safe language:

```text
Protected bytes match signed manifest.
```

Forbidden language:

```text
Cryptography proves ontology.
```

### 23.2 Runtime Sandbox Boundary

Guard runtime isolation reduces side effects and supply-chain risk.

Sandbox failure may block repository-state confidence.

Sandbox success does not validate VECTAETOS.

### 23.3 Incident Boundary

A blocker may generate:

```text
incident bundle
release refusal
maintainer checklist
quarantine recommendation
forensic snapshot when allowed
```

It may not autonomously:

```text
revert commits
lock maintainers out
publish public reports
notify external parties
mutate canonical files
delete suspect files
```

### 23.4 Inter-Guard Isolation

Individual guards may not consume other guard outputs as semantic input.

Only the reporter aggregates findings.

No guard may alter thresholds, severity, contracts, protected-object meaning, or manifest policy based on another guard.

### 23.5 Ontology Creep Detection

Semantic drift across commits must be detected through:

```text
vocabulary deltas
anchor references
promotion ledger entries
semantic errata registry
explicit version boundaries
```

Gradual drift is still drift.

### 23.6 Supply-Chain Boundary

Guard runtime dependencies must be:

```text
pinned
hash-locked
auditable
network-install-free during guard run
```

External security tools are diagnostic only and do not define ontology or safety.

### 23.7 Safe Hardening Claim

Allowed:

```text
The hardened perimeter increased repository-state assurance under declared guard assumptions.
```

Forbidden:

```text
The hardened perimeter proves ontology, safety, correctness, deployment readiness, or empirical validity.
```


---

## 24. Runtime Guard Sealing and EK Integrity Observable

Guard files may be cryptographically sealed before execution.

The runner must verify:

```text
manifest identity
manifest signature
file hash
file signature where used
path role
contract binding
dependency lock
sandbox policy
```

before importing or executing any guard.

If any sealed guard, contract, or core runtime file differs from the registered manifest, the system emits an EK integrity event and refuses the repository-state run.

EK integrity events are read-only observables.

They do not prove:

```text
corruption
ontology failure
unsafe deployment
semantic invalidity
metaphysical failure
```

Allowed claim:

```text
Guard runtime bytes differ from sealed manifest.
```

Forbidden claim:

```text
EK proves the ontology was corrupted.
```

### 24.1 Verify-Before-Import Rule

Allowed flow:

```text
read bytes
verify path
verify manifest signature
verify hash
verify file signature if present
verify contract binding
load exact verified bytes
execute in sandbox
emit attestation
```

Forbidden flow:

```text
import guard
then ask guard to verify itself
```

Reason:

```text
A compromised guard must not be trusted to verify its own integrity.
```

### 24.2 Guard Runtime Manifest

Recommended file:

```text
guards/config/guard_runtime_manifest.json
guards/config/guard_runtime_manifest.sig
```

Example:

```json
{
  "schema_version": "1.0",
  "manifest_id": "vectaetos-guard-runtime-manifest",
  "repo_commit": "GIT_COMMIT_SHA",
  "hash_algorithm": "sha256",
  "signature_algorithm": "ed25519",
  "guards": [
    {
      "guard_id": "GUARD-00",
      "path": "guards/perimeter_kernel_guard.py",
      "sha256": "EXPECTED_HASH",
      "signature": "OPTIONAL_FILE_SIGNATURE",
      "perimeter": "P0_canonical_repository",
      "vectors": ["V0_authority_inflation", "V15_guard_runtime_integrity"],
      "contract_refs": ["contracts/perimeter_kernel.yaml"]
    }
  ]
}
```

### 24.3 EK Integrity Event

Example:

```yaml
ek_integrity_event:
  id: "EK-INTEGRITY-DRIFT-001"
  type: "guard_runtime_integrity_drift"
  severity: "BLOCKER"
  perimeter: "P2_code_behavior"
  vector: "V15_guard_runtime_integrity"
  guard_id: "GUARD-12"
  path: "guards/coherence_vocabulary_guard.py"
  expected_sha256: "abc..."
  observed_sha256: "def..."
  manifest_ref: "guards/config/guard_runtime_manifest.json"
  contract_ref: "contracts/perimeter_kernel.yaml"
  message: "Guard runtime bytes differ from sealed manifest."
  ontology_authority: false
  auto_fix_allowed: false
  ci_action: "refuse_run"
```

### 24.4 EK Boundary

EK may:

```text
emit integrity observable
emit read-only finding
attach file hash
attach manifest hash
attach commit hash
attach contract ref
attach anchor ref
```

EK must not:

```text
rewrite guard
repair guard
delete guard
revert commit
lock repository
declare ontology invalid
declare system unsafe
authorize deployment
```

Clean boundary:

```text
EK = read-only structural integrity witness
```

Not:

```text
EK = enforcement authority
```


---

## 25. Immutable Canonical Anchor and Guard Runtime Integrity

Canonical anchors and guard runtime files may be protected by signed manifests, hash-locked blob registries, and verify-before-import execution.

Cryptographic integrity verifies byte identity, path binding, manifest inclusion, and attested change history.

It does not prove ontology, semantic truth, safety, correctness, or deployment readiness.

### 25.1 Anchor Blob Manifest

Protected anchor files must be listed in a signed manifest with:

```text
path
SHA-256
size
role
perimeter
anchor reference
optional signature
```

Untracked protected files, missing files, symlinked protected paths, hash mismatch, or size mismatch produce `BLOCKER` findings.

Recommended files:

```text
guards/config/anchor_manifest.json
guards/config/anchor_manifest.sig
guards/config/trusted_keys.json
```

Example:

```json
{
  "schema_version": "1.0",
  "manifest_id": "vectaetos-anchor-integrity-manifest",
  "hash_algorithm": "sha256",
  "signature_algorithm": "ed25519",
  "repo_commit": "GIT_COMMIT_SHA",
  "generated_at": "2026-05-22T00:00:00Z",
  "blobs": [
    {
      "path": "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md",
      "sha256": "EXPECTED_SHA256",
      "size": 12345,
      "role": "canonical_anchor",
      "perimeter": "P0_canonical_repository"
    }
  ]
}
```

### 25.2 Manifest Signature Rule

Manifest hash alone is not sufficient.

The manifest must be signed.

The public verification key must be pinned outside the manifest.

Safe statement:

```text
Manifest signature verifies the manifest under the pinned key.
```

Forbidden statement:

```text
Manifest signature proves canonical truth.
```

### 25.3 Anchor Mutation Lock

Protected canonical files are mutation-locked except through explicit promotion protocol.

Allowed mutation channels:

```text
major_version_transition
signed_errata_append
promotion_ledger_entry
explicit_canonical_review
```

Forbidden:

```text
direct_edit_without_manifest_update
force_push_over_protected_anchor
anchor_rewrite_without_version_break
contract_update_without_anchor_trace
```

Enforcement:

```text
unknown_change: BLOCKER
untraced_change: BLOCKER
errata_append_without_signature: ERROR
```

Canonical sentence:

```text
anchors/ are not immutable because files cannot change.
anchors/ are immutable because ungoverned semantic mutation is forbidden.
```

### 25.4 Self-Verification Boundary

Self-verification inside guard files is allowed only as defense-in-depth.

It is not primary protection.

Primary protection:

```text
external runner verifies guard before import
```

Secondary protection:

```text
guard self-verifies after trusted loading
```

Rule:

```text
verify-before-import > self-verify-after-import
```


---

## 26. Runtime Sandbox Policy

```yaml
runtime_sandbox:
  id: "P4-RUNTIME-SANDBOX"
  perimeter:
    - "P2_code_behavior"
    - "P4_runtime_evidence_release"

  network_policy: "disabled_by_default"

  filesystem_policy:
    read_only:
      - "anchors/"
      - "formal/"
      - "contracts/"
      - "guards/"
    write_only:
      - "reports/"
      - "logs/"
    controlled_read:
      - ".git/HEAD"
    no_access:
      - ".env"
      - "secrets/"
      - "__pycache__/"

  process_policy:
    subprocess: "forbidden_by_default"
    dynamic_execution: "forbidden"
    threading: "forbidden_by_default"
    multiprocessing: "forbidden_by_default"
    max_memory_mb: 512
    max_cpu_seconds_per_file: 30

  environment_policy:
    allowed:
      - "GUARD_MODE"
      - "CONTRACT_PATH"
      - "LOG_LEVEL"
      - "CI"
    forbidden_patterns:
      - "TOKEN"
      - "SECRET"
      - "PASSWORD"
      - "API_KEY"
      - "PRIVATE_KEY"
```

Special note:

```text
.git/HEAD may be readable for commit binding.
.git/objects must not be directly traversable unless integrity role is declared.
```

---

## 27. Incident Boundary and Non-Autonomous Enforcement

Rejected autonomous actions:

```text
auto_revert
auto_delete
auto_quarantine_canonical_file
auto_lock_repository
auto_publish_incident_report
auto_notify_external_auditor
```

Allowed guard actions:

```text
emit_signed_incident_bundle
refuse_ci_state
recommend_quarantine
produce_maintainer_checklist
generate_forensic_snapshot_if_allowed
```

Maintainer-governed actions:

```text
move files to quarantine
revert commits
lock protected branch
notify external auditors
publish public incident report
```

Action model:

```yaml
incident_actions:
  - action: "emit_signed_incident_bundle"
    allowed_for_guard: true
    requires_human: false

  - action: "refuse_ci_state"
    allowed_for_guard: true
    requires_human: false

  - action: "recommend_quarantine"
    allowed_for_guard: true
    requires_human: false

  - action: "move_file_to_quarantine"
    allowed_for_guard: false
    requires_human: true

  - action: "git_revert"
    allowed_for_guard: false
    requires_human: true

  - action: "lock_repository"
    allowed_for_guard: false
    requires_human: true

  - action: "notify_external_auditor"
    allowed_for_guard: false
    requires_human: true
```

Clean boundary:

```text
guard may refuse the run
guard may emit incident evidence
guard must not rewrite repository history
guard must not move canonical files
```


---

## 28. Evidence Attestation Boundary

Evidence attestation is allowed as repository-state evidence.

It must not be named or interpreted as proof of truth, ontology, safety, or deployment readiness.

Allowed names:

```text
evidence_attestation
repository_state_checkpoint
static_audit_attestation
integrity_observable
```

Forbidden names:

```text
proof_hash
truth_hash
validity_signature
ontology_attestation
safety_attestation
deployment_attestation
```

Recommended shape:

```yaml
evidence_attestation:
  schema_version: "1.0"
  evidence_class: "E2"
  guard_id: "GUARD-24"
  rule_id: "P0-ANCHOR-HASH-MISMATCH"
  target_path: "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md"
  repo_commit: "GIT_COMMIT_SHA"
  checkpoint_hash: "FILE_SHA256_AT_TIME_OF_CHECK"
  contract_ref: "contracts/manifests/anchor_manifest_policy.yaml"
  anchor_ref: "anchors/VECTAETOS_v1.0_Frozen_Ontological_Core.md"
  timestamp_utc: "2026-05-22T00:00:00Z"
  finding_count: 1
  blocker_count: 1
  report_hash: "REPORT_SHA256"
  attestation_hash: "ATTESTATION_SHA256"
  ontology_authority: false
  deployment_authority: false
```

---

## 29. Testing Hardening

```yaml
testing_hardening:
  property_based_testing:
    required_properties:
      - "finding.ontology_authority is always false"
      - "finding.auto_fix_allowed is false for protected semantic spans"
      - "guard clean output never claims safety, truth, validity, or deployment readiness"
      - "contract rule without anchor_ref fails closed"
      - "unknown protected role fails closed"
      - "negated forbidden phrase does not become blocker unless operationalized"
      - "hash match never emits semantic truth claim"
      - "EK event never emits enforcement authority claim"

  mutation_testing:
    minimum_mutation_score:
      core_findings: "90%"
      contract_loader: "90%"
      release_claim_guard: "85%"
      text_scanner: "80%"
      ast_scanner: "80%"
      immutable_blob: "90%"
      sealed_loader: "90%"

  adversarial_fixtures:
    must_pass:
      - "κ is not a metric."
      - "CI pass is not empirical validation."
      - "Hash does not prove semantic truth."
      - "EK does not decide."

    must_warn:
      - "κ is not a metric, but kappa_score is exported for diagnostics."
      - "Hash does not prove truth, but release notes call it validated."

    must_fail:
      - "κ_score = 0.84"
      - "CI proves safety."
      - "Memory updates Φ."
      - "Projection interprets meaning."
      - "Signature validates ontology."
      - "EK decides repository validity."
```

Golden dataset:

```text
anchors/test_cases/golden_set_v1.json
```

Update process:

```text
requires promotion ledger entry
requires review
requires manifest update
requires regression reason
```

---

## 30. Success Metrics

```yaml
success_metrics:
  protected_surface_coverage:
    target: "100% declared protected surfaces mapped to at least one guard"
    measurement: "weekly contract coverage report"

  blocker_detection_latency:
    target: "< 500ms median for E1/E2 scans on standard fixture set"
    measurement: "CI benchmark"

  false_blocker_rate:
    target: "< 0.5% on golden clean dataset"
    measurement: "rolling CI history"

  red_team_learning_rate:
    target: "100% discovered bypasses converted into regression fixtures"
    measurement: "monthly red-team review"

  incident_bundle_completeness:
    target: "100% blocker incidents include finding JSON, contract ref, anchor ref, file hash, git commit, and safe wording"
    measurement: "incident drill"

  dependency_lock_integrity:
    target: "100% guard-runtime dependencies pinned and hash-locked"
    measurement: "dependency audit"

  manifest_integrity:
    target: "100% protected anchors and guard runtime files present in signed manifests"
    measurement: "manifest audit"

  authority_language_suppression:
    target: "0 allowed PASS/FAIL messages claim truth, safety, deployment, or ontology"
    measurement: "release claim guard"
```

Best red-team metric:

```text
Every discovered bypass becomes a regression fixture.
```


---

## 31. Code Skeleton — Immutable Blob Integrity

```python
# guards/core/immutable_blob.py

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


class AnchorIntegrityError(RuntimeError):
    pass


@dataclass(frozen=True)
class BlobHash:
    path: str
    sha256: str
    size: int
    role: str
    perimeter: str


@dataclass(frozen=True)
class AnchorIntegrityFinding:
    id: str
    path: str
    expected_sha256: str | None
    observed_sha256: str | None
    severity: str
    vector: str
    message: str
    ontology_authority: bool = False
    auto_fix_allowed: bool = False


class AnchorIntegrity:
    def __init__(self, repo_root: Path, manifest_path: Path):
        self.repo_root = repo_root.resolve()
        self.manifest_path = self._resolve_inside_repo(manifest_path)
        self.known_blobs = self._load_manifest()

    def _resolve_inside_repo(self, path: Path) -> Path:
        resolved = path.resolve()
        if not resolved.is_relative_to(self.repo_root):
            raise AnchorIntegrityError(f"Path escapes repository root: {path}")
        return resolved

    @staticmethod
    def _sha256_file(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _load_manifest(self) -> dict[str, BlobHash]:
        if not self.manifest_path.exists():
            raise AnchorIntegrityError(
                f"MANIFEST MISSING: {self.manifest_path}. Cannot verify anchors."
            )

        raw_bytes = self.manifest_path.read_bytes()

        # TODO:
        # Verify detached Ed25519 / Sigstore signature here.
        # The public verification key must be pinned outside the manifest.
        raw = json.loads(raw_bytes.decode("utf-8"))

        blobs: dict[str, BlobHash] = {}
        for item in raw.get("blobs", []):
            blob = BlobHash(**item)
            if blob.path in blobs:
                raise AnchorIntegrityError(f"Duplicate manifest entry: {blob.path}")
            blobs[blob.path] = blob

        if not blobs:
            raise AnchorIntegrityError("Manifest contains no protected blobs.")

        return blobs

    def verify_one(self, rel_path: str) -> AnchorIntegrityFinding | None:
        if rel_path not in self.known_blobs:
            return AnchorIntegrityFinding(
                id="P0-UNTRACKED-ANCHOR",
                path=rel_path,
                expected_sha256=None,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor path is not tracked in integrity manifest.",
            )

        expected = self.known_blobs[rel_path]
        target = self._resolve_inside_repo(self.repo_root / rel_path)

        if not target.exists():
            return AnchorIntegrityFinding(
                id="P0-MISSING-ANCHOR",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Tracked anchor file is missing.",
            )

        if target.is_symlink():
            return AnchorIntegrityFinding(
                id="P0-SYMLINK-ANCHOR",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Protected anchor path is a symlink.",
            )

        observed_hash = self._sha256_file(target)
        observed_size = target.stat().st_size

        if observed_hash != expected.sha256:
            return AnchorIntegrityFinding(
                id="P0-ANCHOR-HASH-MISMATCH",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=observed_hash,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor bytes differ from integrity manifest.",
            )

        if observed_size != expected.size:
            return AnchorIntegrityFinding(
                id="P0-ANCHOR-SIZE-MISMATCH",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=observed_hash,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor size differs from integrity manifest.",
            )

        return None

    def verify_all(self) -> list[AnchorIntegrityFinding]:
        findings: list[AnchorIntegrityFinding] = []
        for rel_path in sorted(self.known_blobs):
            finding = self.verify_one(rel_path)
            if finding is not None:
                findings.append(finding)
        return findings
```


---

## 32. Code Skeleton — Guard Runtime Integrity

```python
# guards/core/crypto_integrity.py

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import hashlib
import json


class Severity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"


@dataclass(frozen=True)
class IntegrityFinding:
    id: str
    guard_id: str
    path: str
    expected_sha256: str
    observed_sha256: str
    severity: Severity
    vector: str
    message: str
    ontology_authority: bool = False
    auto_fix_allowed: bool = False


@dataclass(frozen=True)
class GuardManifestEntry:
    guard_id: str
    path: str
    sha256: str
    perimeter: str
    vectors: tuple[str, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> list[GuardManifestEntry]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    entries: list[GuardManifestEntry] = []
    for item in raw["guards"]:
        entries.append(
            GuardManifestEntry(
                guard_id=item["guard_id"],
                path=item["path"],
                sha256=item["sha256"],
                perimeter=item["perimeter"],
                vectors=tuple(item.get("vectors", ())),
            )
        )

    return entries


def verify_guard_entry(repo_root: Path, entry: GuardManifestEntry) -> IntegrityFinding | None:
    target = repo_root / entry.path

    if not target.exists():
        return IntegrityFinding(
            id=f"EK-INTEGRITY-MISSING-{entry.guard_id}",
            guard_id=entry.guard_id,
            path=entry.path,
            expected_sha256=entry.sha256,
            observed_sha256="<missing>",
            severity=Severity.BLOCKER,
            vector="V15_guard_runtime_integrity",
            message="Guard file is missing from sealed manifest path.",
        )

    observed = sha256_file(target)

    if observed != entry.sha256:
        return IntegrityFinding(
            id=f"EK-INTEGRITY-DRIFT-{entry.guard_id}",
            guard_id=entry.guard_id,
            path=entry.path,
            expected_sha256=entry.sha256,
            observed_sha256=observed,
            severity=Severity.BLOCKER,
            vector="V15_guard_runtime_integrity",
            message="Guard runtime bytes differ from sealed manifest.",
        )

    return None
```


---

## 33. Code Skeleton — Hardened Negation Detector

```python
# guards/core/negation_parser.py

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class NegationResult:
    is_negated: bool
    confidence: float
    negation_span: tuple[int, int]
    method: str


class HardenedNegationDetector:
    NEGATION_PATTERN = re.compile(
        r"\b(is\s+not|isn't|does\s+not|don't|should\s+not|must\s+not|never|no\b)\b",
        re.IGNORECASE,
    )

    ASSIGNMENT_PATTERN = re.compile(
        r"(\b\w+\b\s*(=|:=|\+=|-=)|def\s+\w+|class\s+\w+|return\s+|yield\s+)"
    )

    OPERATIONAL_KEYWORDS = {
        "=", "+=", "-=", ":=", "return", "yield", "print(",
        "log(", "write(", "save(", "commit", "push", "deploy",
        "execute(", "run(", "call(", "send(", "export", "emit",
    }

    META_DISCUSSION_MARKERS = re.compile(r"[\"'`](.*?)[\"'`]")

    def check(self, line: str, forbidden_phrase: str, line_num: int) -> NegationResult:
        lower = line.lower()
        phrase_start = lower.find(forbidden_phrase.lower())

        if phrase_start == -1:
            return NegationResult(False, 1.0, (0, 0), "phrase_not_found")

        phrase_end = phrase_start + len(forbidden_phrase)

        before = line[max(0, phrase_start - 40):phrase_start]

        has_explicit_negation = self.NEGATION_PATTERN.search(before) is not None
        has_assignment_anywhere = self.ASSIGNMENT_PATTERN.search(line) is not None
        has_operational_anywhere = any(kw in line for kw in self.OPERATIONAL_KEYWORDS)
        is_in_meta_context = bool(self.META_DISCUSSION_MARKERS.search(line))

        if has_explicit_negation and is_in_meta_context and not has_assignment_anywhere:
            return NegationResult(True, 0.95, (phrase_start, phrase_end), "explicit_negation_meta")

        if has_explicit_negation and not has_assignment_anywhere and not has_operational_anywhere:
            return NegationResult(True, 0.80, (phrase_start, phrase_end), "explicit_negation_clean")

        if has_explicit_negation and (has_assignment_anywhere or has_operational_anywhere):
            return NegationResult(False, 0.70, (phrase_start, phrase_end), "negation_with_operation_WARN")

        return NegationResult(False, 0.90, (phrase_start, phrase_end), "no_valid_negation")
```

---

## 34. Code Skeleton — Incident Boundary

```python
# guards/core/incident_boundary.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentAction:
    action: str
    allowed_for_guard: bool
    requires_human: bool


INCIDENT_ACTIONS = [
    IncidentAction("emit_signed_incident_bundle", True, False),
    IncidentAction("refuse_ci_state", True, False),
    IncidentAction("recommend_quarantine", True, False),
    IncidentAction("produce_maintainer_checklist", True, False),
    IncidentAction("move_file_to_quarantine", False, True),
    IncidentAction("git_revert", False, True),
    IncidentAction("lock_repository", False, True),
    IncidentAction("notify_external_auditor", False, True),
    IncidentAction("publish_public_incident_report", False, True),
]


def is_action_allowed_for_guard(action: str) -> bool:
    for item in INCIDENT_ACTIONS:
        if item.action == action:
            return item.allowed_for_guard
    return False
```

---

## 35. Code Skeleton — External Sentinel Runner

```bash
#!/usr/bin/env bash
# run_guard.sh
# This script launches guards through external integrity verification.
# It is a skeleton, not a full sandbox.

set -euo pipefail

GUARD_FILE="${1:?missing guard file}"
shift || true

REPO_ROOT="$(pwd)"
GUARD_PATH="guards/${GUARD_FILE}"
EXPECTED_FILE="/secure/hsm/guard_hashes/${GUARD_FILE}.sha256"

if [[ ! -f "$EXPECTED_FILE" ]]; then
  echo "MISSING EXPECTED HASH: $EXPECTED_FILE"
  exit 2
fi

EXPECTED="$(cat "$EXPECTED_FILE" | tr -d '[:space:]')"
ACTUAL="$(sha256sum "$GUARD_PATH" | awk '{print $1}')"

if [[ "$EXPECTED" != "$ACTUAL" ]]; then
  echo "GUARD HASH MISMATCH. ABORTING."
  exit 2
fi

# Resource limits for current shell and child.
ulimit -f 100
ulimit -v 524288

# Better production hardening:
# - bubblewrap / container
# - network disabled
# - read-only mounts
# - tmpfs for reports
# - no secrets in env
# - pinned dependencies
timeout --signal=KILL 30s   python3 "$GUARD_PATH" "$@"
```


---

## 36. Contract Conflict Rule

If guards or contracts disagree:

```text
The conflict is emitted as a finding.
The conflict is not silently resolved.
The reporter may aggregate.
No guard becomes the verdict authority.
```

Conflict wording:

```text
Conflict detected between declared guard contracts.
```

Forbidden wording:

```text
Ontology conflict proven.
```

---

## 37. Contract Cannot Invent Ontology

Tests:

```text
test_contract_rule_requires_anchor_ref
test_contract_cannot_define_new_protected_object
test_contract_cannot_upgrade_draft_to_canonical
test_contract_cannot_replace_anchor
test_contract_without_trace_fails_closed
```

Rule:

```text
Anchor = semantic source
Contract = machine-readable projection
Guard = detection surface
Report = repository-state output
```

No layer may collapse into another.

---

## 38. Final Operating Principle

```text
Guard exposes drift.
Contract projects anchor constraints.
Manifest preserves byte identity.
Hash verifies bytes.
Signature verifies attestation.
EK exposes structural integrity drift.
CI refuses repository state.
Human governance decides repository mutation.
None of these becomes ontology.
```

Slovak:

```text
Guard exponuje drift.
Kontrakt projektuje hranice anchorov.
Manifest uchováva identitu bajtov.
Hash overuje bajty.
Podpis overuje atestáciu.
EK exponuje štrukturálny integritný drift.
CI odmieta stav repozitára.
Ľudská governance rozhoduje o mutácii repozitára.
Nič z toho sa nestáva ontológiou.
```

Final compressed sentence:

```text
Immutable anchor integrity protects bytes, not truth.
Guard sealing protects runtime identity, not ontology.
EK reports structural drift, not metaphysical failure.
CI refuses repository state, not reality.
```

Slovak:

```text
Integrita immutable anchorov chráni bajty, nie pravdu.
Zapečatenie guardov chráni runtime identitu, nie ontológiu.
EK hlási štrukturálny drift, nie metafyzické zlyhanie.
CI odmieta stav repozitára, nie realitu.
```

End of document.
