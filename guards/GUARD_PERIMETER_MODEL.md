# VECTAETOS™ Guard Perimeter Model

**Status:** implementation model 
**Path:** `guards/GUARD_PERIMETER_MODEL.md` 
**Role:** repository perimeter architecture 
**Ontology authority:** none 
**Decision authority:** none 
**Optimization authority:** none 
**Feedback into Φ:** none 
**Version:** v0.4-draft-level-0-5 
**Date:** 2026-05-23 

---

## 0. Boundary

This document defines the working architecture of VECTAETOS repository guards.

It is not a canonical ontology anchor.

It does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, ZMYSEL, or any canonical meaning.

It defines how repository drift is exposed.

```text
guard = drift detection surface
guard ≠ truth
guard ≠ ontology
guard ≠ authority
guard ≠ optimizer
guard ≠ decision module
guard ≠ Φ
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
deterministic reports / CI refusal
    ↓
human maintainer review
```

Forbidden operational chain:

```text
guard finding
    ↓
truth verdict
    ↓
automatic ontology change
    ↓
feedback into Φ
```

Core sentence:

```text
Guard exponuje drift; nedefinuje pravdu.
```

---

## 1. Perimeter grammar

The previous P0–P4 notation is retained only as historical background.

The current implementation model uses six levels:

```text
Level 0 — Fundamental Repository Perimeter
Level 1 — Specialized Ontological Perimeter
Level 2 — Semantic / Ontological Vocabulary Perimeter
Level 3 — Code Behavior Perimeter
Level 4 — Bridge / Projection / Trace Perimeter
Level 5 — Runtime / Evidence / Release Perimeter
```

Every guard should be described by:

```text
level × drift vector × evidence class × enforcement mode × integrity posture
```

Example:

```yaml
guard_id: "GUARD-12"
primary_level: "Level 2"
secondary_levels: ["Level 4"]
drift_vectors: ["V3_forbidden_conversion", "V8_negation_blindness"]
evidence_class_allowed: "E1_static_scan"
enforcement_mode: "strict"
integrity_posture: "semantic_read_only"
```

A guard may touch multiple levels, but must still declare one primary level.

---

## 2. Levels

### Level 0 — Fundamental Repository Perimeter

Protects root repository structure, canonical anchors, formal files, contracts, manifests, workflows, master routing, and guard bootstrap boundaries.

Typical surfaces:

```text
anchors/
formal/
contracts/
guards/
.github/workflows/
MASTER_INDEX.md
VOCABULARY_LOCK.md
repository root shape
perimeter manifests
promotion ledgers
```

Typical guards:

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-11 master_index_router_guard.py
GUARD-21 no_feedback_loop_guard.py
GUARD-23 guard_runtime_integrity_guard.py
GUARD-24 anchor_blob_integrity_guard.py
```

Level 0 refuses repository states that corrupt the perimeter itself.

It does not prove ontology.

---

### Level 1 — Specialized Ontological Perimeter

Protects specific high-risk ontological structures where a narrow dedicated guard is safer than broad scanning.

Typical surfaces:

```text
QE
Triality
Vortex non-agentic posture
specialized anchor-local vocabulary
specific canonical structural terms
```

Typical guards:

```text
GUARD-06 no_feedback_loop_guard.py
GUARD-07 vortex_non_agentic_guard.py
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-22 vortex_non_agentic_guard.py
```

Level 1 is specialized. It detects local misuse of a protected concept.

---

### Level 2 — Semantic / Ontological Vocabulary Perimeter

Protects general semantic vocabulary across documents, code comments, contracts, reports, and examples.

Typical surfaces:

```text
Φ
K(Φ)
K_D(Φ)
κ
QE
Σ
R
ZMYSEL / Ξ
h_topo
C_i^EK
Q_i^EK
projection vocabulary
evidence language
guard language
```

Typical guards:

```text
GUARD-10 vector_drift_guard.py
GUARD-12 coherence_vocabulary_guard.py
GUARD-25 ontology_creep_guard.py
```

Level 2 must be negation-aware and meta-example-aware.

It must not punish boundary-protective sentences:

```text
κ is not a metric.
QE is not an error.
K(Φ) is not a score.
Projection does not interpret.
```

---

### Level 3 — Code Behavior Perimeter

Protects Python behavior, static AST discipline, role permissions, import boundaries, deterministic execution, file mutation, subprocess/network use, and non-agentic code posture.

Typical surfaces:

```text
Python source behavior
role-specific capabilities
dynamic execution
network calls
subprocess calls
file writes
randomness
import direction
ontology-facing assignments
selection / ranking behavior
```

Typical guards:

```text
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-07 ast_alias_audit_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-26 inter_guard_coupling_guard.py
```

Level 3 scans code.

It must never execute target modules.

---

### Level 4 — Bridge / Projection / Trace Perimeter

Protects downstream bridge vocabulary, EK observables, projection boundaries, trace layers, runes/glyphs, logs, and ledger language.

Typical surfaces:

```text
Φ → EK bridge
EK observables
projection vocabulary
runes
glyphs
TetraGlyph
memory traces
logs
ledger language
LTL
ESM
EAT
MML
```

Typical guards:

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
```

Level 4 enforces read-only downstream posture.

Projection, bridge, audit, and trace surfaces must not become interpretation, selection, validation, or control.

---

### Level 5 — Runtime / Evidence / Release Perimeter

Protects deterministic runtime execution, release language, DOI text, README badges, evidence classes, public statements, runtime sandboxing, dependency boundaries, and incident handling.

Typical surfaces:

```text
CI reports
release notes
DOI text
README badges
public claims
evidence attestations
runtime sandbox policy
dependency manifests
incident bundles
workflow outputs
```

Typical guards:

```text
GUARD-04 empirical_claim_guard.py
GUARD-19 release_claim_guard.py
GUARD-20 evidence_class_guard.py
GUARD-27 evidence_attestation_guard.py
GUARD-28 dependency_supply_chain_guard.py
GUARD-29 runtime_sandbox_guard.py
GUARD-30 incident_boundary_guard.py
```

Level 5 prevents evidence overclaim.

A successful runtime or CI result is not empirical proof of safety.

---

## 3. Drift vectors

Every finding must map to one or more drift vectors.

```yaml
V0_authority_inflation:
  meaning: Lower layer begins claiming authority, truth, ontology, validation, or decision power.

V1_upward_mutation:
  meaning: Downstream layer mutates or redefines a higher layer.

V2_agency_injection:
  meaning: Non-agentic component becomes an agent, controller, planner, optimizer, recommender, or selector.

V3_forbidden_conversion:
  meaning: Boundary term becomes metric, score, threshold, parameter, fallback, error, or reward.

V4_evidence_overclaim:
  meaning: Evidence level is overstated.

V5_nondeterminism:
  meaning: Behavior becomes time-dependent, random, environment-dependent, or non-reproducible.

V6_path_status_laundering:
  meaning: File changes meaning through path, name, status, relocation, or layer ambiguity.

V7_contract_drift:
  meaning: Contract diverges from anchor, rule id, schema version, or declared guard meaning.

V8_negation_blindness:
  meaning: Scanner punishes protective negation or ignores malicious negation.

V9_silence_qe_coercion:
  meaning: QE, aporia, or silence is coerced into resolution, fallback, success, failure, or output pressure.

V10_timing_side_channel:
  meaning: Runtime behavior leaks or changes meaning through timing, ordering, hidden state, or external dependency.

V11_inter_guard_coupling:
  meaning: One guard consumes another guard's findings as authority or changes thresholds based on another guard.

V12_ontology_creep:
  meaning: Vocabulary shifts meaning without anchor, errata, or versioned migration.

V13_dependency_supply_chain:
  meaning: Dependency is unpinned, unverified, network-installed, or changed without manifest trace.

V14_anchor_integrity_drift:
  meaning: Protected anchor bytes differ from manifest or expected reviewed state.

V15_guard_runtime_integrity:
  meaning: Guard runtime, runner, workflow, or guard file identity differs from sealed expectation.
```

---

## 4. Evidence classes

```yaml
E0_text_claim:
  claim_limit: textual pattern observed

E1_static_scan:
  claim_limit: static repository scan finding

E2_AST_contract_compliance:
  claim_limit: Python AST / contract compliance finding

E3_deterministic_test_suite:
  claim_limit: deterministic test result

E4_empirical_validation:
  claim_limit: real-world validation event

E5_external_replication:
  claim_limit: external replication event

E6_independent_security_governance_audit:
  claim_limit: independent audit/governance review

E7_formal_verification_of_guard_properties:
  claim_limit: formal property verification of guard behavior
```

Forbidden promotions:

```text
E0 → proof
E1 → empirical validation
E2 → deployment validity
E3 → real-world safety
E4 single pilot → universal proof
E5/E6/E7 → ontology authority
```

---

## 5. Enforcement modes

```yaml
advisory:
  behavior: emits finding only

report:
  behavior: emits finding and exits 0 unless configured otherwise

strict:
  behavior: fails CI on configured blocker

fail_closed:
  behavior: refuses when guard confidence is unavailable

experimental:
  behavior: reports without becoming required perimeter
```

Required safe wording:

```text
PASS: No configured blocker was detected within the declared perimeter.
FAIL: Configured blocker detected within declared repository perimeter.
FAIL: Guard infrastructure error; confidence unavailable.
```

Forbidden wording:

```text
ontology preserved
VECTAETOS is safe
semantic correctness proven
deployment ready
truth validated
```

---

## 6. Exit-code contract

```text
0 = no findings at configured enforcement level
1 = blocker finding detected
2 = guard infrastructure failure / confidence unavailable
3 = invalid contract / missing anchor trace / invalid manifest signature
4 = invalid CLI usage
```

Exit codes are repository-state signals only.

They are not truth values.

---

## 7. Unified Finding schema

All guards must eventually emit the shared finding schema.

Minimum required fields:

```yaml
id: "VEC-..."
guard_id: "GUARD-12"
guard_file: "guards/coherence_vocabulary_guard.py"
rule_id: "FC-KAPPA-METRIC"
contract_schema_version: "1.0"

level: "Level 2"
scope: "semantic_vocabulary"
vector: "V3_forbidden_conversion"
severity: "BLOCKER"
confidence: "high"

path: "formal/example.md"
line: 42
role: "formal"

protected_object: "κ"
observed_pattern: "kappa_score"
forbidden_conversion: "κ -> metric/score/threshold"

evidence_class_allowed: "E1_static_scan"
anchor_ref: "anchors/..."
contract_ref: "contracts/..."

message: "Pattern appears to convert κ into metric/score language."
safer_form: "Use boundary-of-representability language."

ontology_authority: false
auto_fix_allowed: false
```

Hard invariants:

```text
ontology_authority must always be false
auto_fix_allowed must default to false
rule_id must be stable
contract_schema_version must be present
finding order must be deterministic
report wording must be non-authoritative
```

---

## 8. Integrity posture

```yaml
immutable_anchor:
  checks: anchor identity and canonical file stability

guard_runtime:
  checks: guard file identity and runtime sealing

semantic_read_only:
  checks: protected vocabulary remains non-authoritative

code_behavior:
  checks: source behavior and role capabilities

projection_read_only:
  checks: projection and bridge surfaces remain descriptive

evidence_posture:
  checks: claims match evidence class

runtime_sandbox:
  checks: execution constraints, dependency and environment limits

incident_boundary:
  checks: incident reports remain non-agentic and non-mutating
```

Important:

```text
hash verifies bytes
hash ≠ truth
signature verifies attestation
signature ≠ ontology
CI pass verifies configured check
CI pass ≠ safety
```

---

## 9. Modus operandi

```text
inspect
    ↓
normalize
    ↓
map to rule_id
    ↓
map to level
    ↓
map to drift vector
    ↓
map to evidence class
    ↓
emit Finding
    ↓
render deterministic report
    ↓
human maintainer acts
```

The guard does not repair.

The guard does not quarantine.

The guard does not revert commits.

The guard does not modify Φ.

The guard does not automatically rewrite ontology-facing text.

---

## 10. Incident boundary

Allowed:

```text
emit incident bundle
fail CI
produce maintainer checklist
recommend quarantine
record timestamped evidence
```

Forbidden:

```text
auto-revert
auto-delete
auto-quarantine
auto-lock repository
send external webhook as authority
alter protected files
treat incident as ontology failure
```

---

## 11. MVP versus full perimeter

The full perimeter contains GUARD-00 through GUARD-30.

The MVP must be smaller and executable.

Recommended MVP:

```text
GUARD-00 perimeter kernel
GUARD-01 canonical ontology guard
GUARD-03 code behavior audit
GUARD-12 coherence vocabulary guard
GUARD-19 release claim guard
```

Expansion order after MVP:

```text
Level 0 integrity guards
Level 2 vocabulary guards
Level 3 code behavior guards
Level 4 projection / EK guards
Level 5 evidence / runtime guards
```

Do not implement 30 guards before the kernel stabilizes.

---

## 12. Refactoring order

Current shared kernel direction:

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

Next guard-level refactor order:

```text
1. GUARD-12 coherence_vocabulary_guard.py
2. GUARD-01 canonical_ontology_guard.py
3. GUARD-03 vectaetos_code_behavior_audit.py
4. GUARD-08 qe_aporia_guard.py
5. GUARD-09 triality_guard.py
6. GUARD-10 vector_drift_guard.py
7. GUARD-11 master_index_router_guard.py
8. GUARD-19 release_claim_guard.py
```

New guards should be added only after shared core output is stable.

---

## 13. Forbidden claims

```text
Guard proves ontology.
Guard validates truth.
CI pass means VECTAETOS is safe.
Hash means semantic validity.
Signature means ontology.
Evidence class E1 means empirical proof.
K(Φ) is a score.
κ is a threshold.
QE is an error.
Projection interprets.
Vortex selects.
EK validates deployment.
Audit controls runtime.
```

---

## 14. Document relation

This document is upstream of:

```text
guards/MATICA_PERIMETER.md
guards/GUARD_MVP_PROFILE.md
guards/README.md
guards/core/README.md
```

It is downstream of canonical anchors.

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
README
    >
implementation note
```

---

## 15. Final posture

```text
The perimeter may become stricter, but never more authoritative.
```

Slovak:

```text
Perimeter môže byť tvrdší, ale nikdy autoritatívnejší.
```

End.
