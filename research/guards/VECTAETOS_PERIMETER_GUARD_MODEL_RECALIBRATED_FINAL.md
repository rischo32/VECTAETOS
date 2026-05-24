# VECTAETOS™ PERIMETER GUARD MODEL
## Hardened Reference Architecture + MVP Operational Baseline

**Status:** HARDENED REFERENCE ARCHITECTURE WITH MVP PROFILE  
**Reference Version:** `0.4-recalibrated`  
**MVP Version:** `0.1-operational-baseline`  
**Document role:** implementation proposal, not canonical ontology anchor  
**Scope:** VECTAETOS repository perimeter only  
**Execution Power:** repository-state protection only  
**Feedback into Φ:** none  
**Ontology Authority:** none  
**Optimization Authority:** none  
**Decision Authority:** none  
**Deployment Authority:** none  
**Recommended path:** `guards/GUARD_PERIMETER_MODEL.md`  
**MVP companion path:** `guards/GUARD_MVP_PROFILE.md`  
**Companion review path:** `guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md`

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

The perimeter guard system exposes possible drift relative to canonical anchors, machine-readable contracts, signed manifests, and declared repository boundaries.

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
signed or hash-pinned manifests
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

The full model is not a plain Level 0–3 hierarchy.

```text
Perimeter = scope layer × drift vector × evidence class × enforcement mode × integrity posture
```

The old Level 0–3 reading remains useful for humans, but implementation must use:

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

## 2. Recalibrated Implementation Profile

The hardened perimeter model is a **reference architecture**, not the required first implementation.

For a solo developer or constrained environment, implementation must begin with the **MVP perimeter**.

```text
Reference Architecture = complete hardened model
MVP Perimeter = smallest operational baseline
```

A smaller guard system that actually runs is stronger than a complete perimeter that remains theoretical.

Slovak:

```text
Menší guard systém, ktorý reálne beží, je silnejší než úplný perimeter, ktorý zostane teoretický.
```

### MVP Principle

Implement the smallest guard set that protects the highest-risk invariants:

```text
1. no authority inflation
2. no silent canonical anchor mutation
3. no forbidden conversion of protected vocabulary
4. no protected-layer mutation in Python code
5. no release/evidence overclaim
```

---

## 3. MVP Guard Set

The minimum viable perimeter contains five guards:

```text
GUARD-MVP-00 perimeter_kernel_guard.py
GUARD-MVP-01 anchor_and_manifest_integrity_guard.py
GUARD-MVP-02 semantic_vocabulary_guard.py
GUARD-MVP-03 code_behavior_ast_guard.py
GUARD-MVP-04 release_and_evidence_claim_guard.py
```

### MVP Risk Coverage Matrix

| Risk | Covered by | MVP status |
|---|---|---|
| Guard claims authority | `GUARD-MVP-00` | active |
| Unsafe PASS/FAIL wording | `GUARD-MVP-00` | active |
| Anchor modified silently | `GUARD-MVP-01` | active |
| Guard runtime modified | `GUARD-MVP-01` | active |
| Protected file not in manifest | `GUARD-MVP-01` | active |
| κ becomes metric | `GUARD-MVP-02` | active |
| QE becomes exception/fallback | `GUARD-MVP-02` / `GUARD-MVP-03` | active |
| Vortex becomes optimizer | `GUARD-MVP-02` / `GUARD-MVP-03` | active |
| EK becomes authority | `GUARD-MVP-02` / `GUARD-MVP-04` | active |
| Python mutates protected layer | `GUARD-MVP-03` | active |
| `eval` / `exec` / subprocess introduced | `GUARD-MVP-03` | active |
| CI/release claims safety | `GUARD-MVP-04` | active |
| Dependency attack | `GUARD-MVP-03` basic, full later | partial |
| Ontology creep over months | `GUARD-MVP-02` snapshot only, V12 later | partial |
| Timing side channel | out of MVP | deferred |
| Multi-guard collusion | out of MVP | deferred |

---

## 4. MVP Kernel

Minimal kernel:

```text
guards/core/
  findings.py
  reporting.py
  paths.py
  contracts.py
  integrity.py
  text_scan.py
  ast_scan.py
```

Deferred modules:

```text
semantic_drift.py       # V12, requires git history
sandbox.py              # production hardening
dependency_lock.py      # supply-chain hardening
incident_bundle.py      # signed forensic output
temporal_isolation.py   # not MVP
consensus.py            # not MVP
inter_guard_coupling.py # not MVP
collateral_damage.py    # not MVP
```

Deferred does not mean rejected.  
It means not required for the first operational baseline.

---

## 5. MVP Repository Tree

```text
guards/
  GUARD_PERIMETER_MODEL.md
  GUARD_MVP_PROFILE.md
  GUARD_TABLE.md

  perimeter_kernel_guard.py
  anchor_and_manifest_integrity_guard.py
  semantic_vocabulary_guard.py
  code_behavior_ast_guard.py
  release_and_evidence_claim_guard.py

  core/
    findings.py
    reporting.py
    paths.py
    contracts.py
    integrity.py
    text_scan.py
    ast_scan.py

  config/
    anchor_manifest.json
    guard_runtime_manifest.json

contracts/
  mvp_policy.yaml
  forbidden_conversions.yaml
  evidence_classes.yaml

tests/
  fixtures/
    must_pass/
    must_warn/
    must_fail/
```

---

## 6. Perimeter Rings — Reference Architecture

### P0 — Canonical Repository Perimeter

Protects root repository boundary, canonical anchors, formal files, status files, guard files, signed or hash-pinned manifests, semantic errata registry, and canonical routing.

Protected surfaces:

```text
anchors/
formal/
MASTER_INDEX.md
CANONICAL_STATUS.md
canonical status files
guard files
anchor manifests
guard runtime manifests
semantic errata registry
promotion paths
root repository shape
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

---

### P1 — Semantic / Ontological Vocabulary Perimeter

Protects canonical language around ZMYSEL / Ξ, Φ, Σ, R, K(Φ), κ, QE, Vortex, Triality, OAAT, silence, aporia, and related boundary terms.

Primary vectors:

```text
V2_agency_injection
V3_forbidden_conversion
V8_negation_blindness
V9_silence_qe_coercion
V12_ontology_creep
```

---

### P2 — Code Behavior Perimeter

Protects Python source behavior, role-specific permissions, read-only guard behavior, runtime sealing, and non-agentic execution discipline.

Primary vectors:

```text
V1_upward_mutation
V2_agency_injection
V3_forbidden_conversion
V5_nondeterminism
V11_inter_guard_coupling
V15_guard_runtime_integrity
```

---

### P3 — Bridge / Projection / Trace Perimeter

Protects downstream read-only bridge vocabulary, projection boundaries, EK observables, memory traces, logs, glyph/rune language, and ledger semantics.

Primary vectors:

```text
V0_authority_inflation
V1_upward_mutation
V3_forbidden_conversion
V4_evidence_overclaim
V14_anchor_integrity_drift
V15_guard_runtime_integrity
```

---

### P4 — Runtime / Evidence / Release Perimeter

Protects deterministic execution, evidence posture, public claims, release text, DOI language, README badges, CI-report boundaries, dependency integrity, sandbox behavior, and incident output.

Primary vectors:

```text
V0_authority_inflation
V4_evidence_overclaim
V5_nondeterminism
V6_path_status_laundering
V10_runtime_resource_anomaly
V13_dependency_supply_chain
V15_guard_runtime_integrity
```

---

## 7. Drift Vector Taxonomy

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

  V10_runtime_resource_anomaly:
    detects: "guard run exceeds declared CPU, memory, file-count, or wall-time budget"
    note: "Replaces timing-side-channel ambition in MVP. Timing side-channel detection is deferred research."

  V11_inter_guard_coupling:
    detects: "one guard changes thresholds, severity, rule set, or interpretation based on another guard output"
    alias: "guard_collusion"

  V12_ontology_creep:
    detects: "slow semantic drift across commits without explicit version, errata, or promotion trail"
    limit: "Requires git history analysis; in MVP only snapshot vocabulary checks are active."

  V13_dependency_supply_chain:
    detects: "third-party dependency introduces unpinned, unaudited, or behavior-changing code path"

  V14_anchor_integrity_drift:
    detects: "protected anchor bytes differ from registered manifest without authorized promotion path"

  V15_guard_runtime_integrity:
    detects: "guard source, contract, runtime core, or manifest differs from registered sealed identity"
```

---

## 8. Evidence Classes

```text
E0 text claim
E1 static text scan
E2 AST / contract / manifest compliance
E3 deterministic test suite
E4 empirical validation
E5 external replication / deployment evidence
E6 independent security / governance audit
E7 formal verification of selected guard properties
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

## 9. Enforcement Modes

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

## 10. Exit Code Contract

```text
0  = no configured findings at enforcement level
1  = blocker finding detected
2  = guard runtime failure / confidence unavailable
3  = invalid contract schema
4  = missing anchor trace
5  = invalid manifest signature
6  = manifest/hash mismatch
7  = dependency lock failure
64 = invalid CLI usage
```

Exit code = run diagnosis.  
Exit code ≠ truth.

---

## 11. Unified Finding Format

All guards must emit one shared finding shape.

```yaml
finding:
  id: "VEC-P1-CONV-001"
  guard_id: "GUARD-MVP-02"
  guard_file: "guards/semantic_vocabulary_guard.py"
  rule_id: "FC-KAPPA-METRIC"
  contract_schema_version: "1.0"
  scope: "P1_semantic_vocabulary"
  vector: "V3_forbidden_conversion"
  severity: "BLOCKER"
  confidence: "structural"
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
  contract_ref: "contracts/forbidden_conversions.yaml"
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

## 12. Confidence Levels

Do not use arbitrary numeric confidence scores.

Use discrete classes:

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

## 13. Text Scan vs. AST Scan

Regex-based negation detection is allowed only for documentation and prose-like files.

```text
P1/P3 documentation text:
  text_scan + negation parser allowed

P2 Python code:
  AST scan primary
  text scan only fallback / warning layer
```

For Python code, AST rules dominate.

Examples that must be handled by AST, not prose negation:

```python
κ_score = 0.84
def optimize_phi(...): ...
return deployment_valid
subprocess.run(...)
eval(source)
```

Negation class enum:

```yaml
negation_class:
  NEGATED_META_EXAMPLE:
    action: "PASS"

  NEGATED_CLEAN_TEXT:
    action: "PASS"

  NEGATED_WITH_OPERATIONAL_PATTERN:
    action: "WARN"

  ACTIVE_IMPLEMENTATION:
    action: "BLOCKER"

  UNCLEAR:
    action: "WARN"
```

Rule:

```text
If a line contains negation and an implementation pattern, never treat it as a clean pass.
```

---

## 14. Forbidden Conversion Table

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

## 15. Integrity Profiles

Do not assume enterprise HSM for local development.

```yaml
integrity_profiles:
  local:
    trust_root: "repo-pinned manifest + local public key"
    hsm_required: false
    sigstore_optional: true
    target_environment: "Termux / laptop / solo developer"

  ci:
    trust_root: "CI-pinned public key + signed manifest"
    hsm_required: false
    sigstore_recommended: true
    target_environment: "GitHub Actions / local CI"

  production:
    trust_root: "HSM/KMS/Sigstore-backed signing"
    hsm_required: true
    sigstore_required: true
    target_environment: "hardened release pipeline"
```

Any `/secure/hsm/...` example is production-profile pseudocode, not local deployment code.

---

## 16. Immutable Canonical Anchor Integrity

Canonical anchors and guard runtime files may be protected by manifests, hashes, signatures, and verify-before-import execution.

Cryptographic integrity verifies:

```text
byte identity
path binding
manifest inclusion
attested change history
```

It does not prove:

```text
ontology
semantic truth
safety
correctness
deployment readiness
```

### Anchor Manifest

Recommended local MVP files:

```text
guards/config/anchor_manifest.json
guards/config/guard_runtime_manifest.json
```

Production may add:

```text
guards/config/anchor_manifest.sig
guards/config/guard_runtime_manifest.sig
guards/config/trusted_keys.json
```

Example:

```json
{
  "schema_version": "1.0",
  "manifest_id": "vectaetos-anchor-integrity-manifest",
  "hash_algorithm": "sha256",
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

### Safe Language

Allowed:

```text
Protected bytes match the manifest.
Protected bytes differ from the manifest.
```

Forbidden:

```text
The manifest proves ontology.
The hash proves truth.
The signature validates meaning.
```

---

## 17. Guard Runtime Sealing and EK Integrity Observable

Guard files may be sealed before execution.

The runner should verify:

```text
manifest identity
file hash
path role
contract binding
dependency lock where available
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

### Verify-Before-Import Rule

Allowed flow:

```text
read bytes
verify path
verify manifest
verify hash
verify contract binding
load exact verified bytes
execute
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

---

## 18. Runtime Sandbox Policy

MVP local profile:

```yaml
runtime_sandbox_local:
  network_policy: "avoid network by default"
  filesystem_policy:
    read_only_targets:
      - "anchors/"
      - "formal/"
      - "contracts/"
    write_targets:
      - "reports/"
      - "logs/"
  forbidden:
    - "eval"
    - "exec"
    - "subprocess unless explicitly allowed"
    - "secret-like env variables in report"
```

Production profile:

```yaml
runtime_sandbox_production:
  network_policy: "disabled_by_default"
  process_policy:
    subprocess: "forbidden_by_default"
    dynamic_execution: "forbidden"
    threading: "forbidden_by_default"
    multiprocessing: "forbidden_by_default"
    max_memory_mb: 512
    max_cpu_seconds_per_file: 30
```

Special note:

```text
.git/HEAD may be readable for commit binding.
.git/objects must not be directly traversable unless integrity role is declared.
```

---

## 19. Incident Boundary and Non-Autonomous Enforcement

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
emit_incident_bundle
refuse_ci_state
recommend_quarantine
produce_maintainer_checklist
```

Maintainer-governed actions:

```text
move files to quarantine
revert commits
lock protected branch
notify external auditors
publish public incident report
```

Clean boundary:

```text
guard may refuse the run
guard may emit incident evidence
guard must not rewrite repository history
guard must not move canonical files
```

---

## 20. Evidence Attestation Boundary

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

---

## 21. Safe PASS / FAIL Wording

Allowed PASS wording:

```text
PASS: No configured blocker was detected within the declared perimeter.
PASS: Repository-state check completed without configured blockers.
PASS: Static scan produced no findings at or above the configured enforcement level.
PASS: Protected bytes match manifest.
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
FAIL: protected bytes differ from manifest.
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

## 22. Canonical Repo Sentence

English:

```text
The VECTAETOS perimeter guard system exposes semantic, architectural,
behavioral, runtime, integrity, supply-chain, and release-claim drift relative
to canonical anchors, machine-readable contracts, and manifests. It protects
repository state only. It does not define ontology, prove truth, validate
safety, optimize behavior, authorize deployment, or mutate Φ.
```

Slovak:

```text
Perimeter guard systém VECTAETOS exponuje sémantický, architektonický,
behaviorálny, runtime, integritný, supply-chain a release-claim drift voči
kanonickým anchorom, strojovo čitateľným kontraktom a manifestom. Chráni iba
stav repozitára. Nedefinuje ontológiu, nedokazuje pravdu, nevaliduje bezpečnosť,
neoptimalizuje správanie, neautorizuje deployment a nemutuje Φ.
```

---

## 23. Non-Goals

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

## 24. Recalibrated Build Order

```text
0. guards/GUARD_PERIMETER_MODEL.md
1. guards/GUARD_MVP_PROFILE.md
2. guards/GUARD_TABLE.md

3. guards/core/findings.py
4. guards/core/reporting.py
5. guards/core/paths.py
6. guards/core/contracts.py
7. guards/core/integrity.py
8. guards/core/text_scan.py
9. guards/core/ast_scan.py

10. guards/perimeter_kernel_guard.py
11. guards/anchor_and_manifest_integrity_guard.py
12. guards/semantic_vocabulary_guard.py
13. guards/code_behavior_ast_guard.py
14. guards/release_and_evidence_claim_guard.py

15. contracts/perimeter_kernel.yaml
16. contracts/mvp_policy.yaml
17. contracts/forbidden_conversions.yaml
18. contracts/evidence_classes.yaml

19. guards/config/anchor_manifest.json
20. guards/config/guard_runtime_manifest.json

21. tests/fixtures/must_pass/
22. tests/fixtures/must_warn/
23. tests/fixtures/must_fail/
```

After MVP is stable, optionally add:

```text
semantic_drift.py
dependency_lock.py
sandbox.py
incident_bundle.py
signed manifests
Sigstore / KMS / HSM production profile
```

---

## 25. Testing Hardening

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

Best red-team metric:

```text
Every discovered bypass becomes a regression fixture.
```

---

## 26. Success Metrics

```yaml
success_metrics:
  protected_surface_coverage:
    target: "100% declared MVP protected surfaces mapped to at least one guard"
    measurement: "contract coverage report"

  blocker_detection_latency:
    target: "< 500ms median for E1/E2 scans on standard fixture set"
    measurement: "CI benchmark"

  false_blocker_rate:
    target: "< 0.5% on golden clean dataset"
    measurement: "rolling CI history"

  red_team_learning_rate:
    target: "100% discovered bypasses converted into regression fixtures"
    measurement: "red-team review"

  incident_bundle_completeness:
    target: "100% blocker incidents include finding JSON, contract ref, anchor ref, file hash, git commit, and safe wording"
    measurement: "incident drill"

  manifest_integrity:
    target: "100% MVP protected anchors and guard runtime files present in manifests"
    measurement: "manifest audit"

  authority_language_suppression:
    target: "0 allowed PASS/FAIL messages claim truth, safety, deployment, or ontology"
    measurement: "release claim guard"
```

---

## 27. Full Reference Backlog

The full hardened reference architecture may later add:

```text
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

But these are not required for MVP.

---

## 28. Final Operating Principle

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
