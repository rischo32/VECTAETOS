# VECTAETOS™ PERIMETER GUARD MODEL
## Final Implementation Proposal

**Status:** FINAL IMPLEMENTATION PROPOSAL  
**Scope:** VECTAETOS repository perimeter only  
**Execution Power:** repository-state protection only  
**Feedback into Φ:** none  
**Ontology Authority:** none  
**Optimization Authority:** none  
**Decision Authority:** none  
**Recommended path:** `guards/GUARD_PERIMETER_MODEL.md`  
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

The perimeter guard system exposes possible drift relative to canonical anchors, machine-readable contracts, and declared repository boundaries.

It does not decide whether an implementation, document, bridge, projection, audit report, release claim, or interpretation is metaphysically true.

```text
diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
warning ≠ verdict
failure ≠ metaphysical proof
CI pass ≠ empirical proof
```

Allowed chain:

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

No lower layer may redefine a higher layer. No downstream layer may mutate Φ. No guard may become a source of ontology.

---

## 1. Final Architectural Decision

The final model is not a plain Level 0–3 hierarchy.

```text
Perimeter = scope layer × drift vector × evidence class × enforcement mode
```

The older Level 0–3 reading remains useful for humans, but implementation should use perimeter rings, drift vectors, evidence classes, and enforcement modes.

This prevents each guard from having its own private meaning of severity, finding, report, contract, evidence, authority, or exit code.

Working posture:

```text
mapujeme → obmedzujeme → exponujeme → odmietame drift
```

Not:

```text
rozhodujeme → optimalizujeme → dokazujeme → autorizujeme
```

---

## 2. Perimeter Rings

### P0 — Canonical Repository Perimeter

Protects root repository boundary, canonical anchors, formal files, status files, and canonical routing.

Protected surfaces:

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

Related guards:

```text
GUARD-00 perimeter_kernel_guard.py
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-11 master_index_router_guard.py
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
```

Primary vectors:

```text
V0_authority_inflation
V1_upward_mutation
V6_path_status_laundering
V7_contract_drift
```

### P1 — Semantic / Ontological Vocabulary Perimeter

Protects canonical language around ZMYSEL / Ξ, Φ, Σ, R, K(Φ), κ, QE, Vortex, Triality, and related boundary terms.

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
canonical vocabulary
```

Related guards:

```text
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
GUARD-12 coherence_vocabulary_guard.py
```

Primary vectors:

```text
V2_agency_injection
V3_forbidden_conversion
V8_negation_blindness
V9_silence_qe_coercion
```

### P2 — Code Behavior Perimeter

Protects Python source behavior, role-specific permissions, and non-agentic execution discipline.

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
```

Related guards:

```text
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-07 vortex_non_agentic_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
```

Primary vectors:

```text
V1_upward_mutation
V2_agency_injection
V5_nondeterminism
V3_forbidden_conversion
```

### P3 — Bridge / Projection / Trace Perimeter

Protects downstream read-only bridge vocabulary, projection boundaries, EK observables, and trace layers.

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
```

Related guards:

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
```

Primary vectors:

```text
V0_authority_inflation
V1_upward_mutation
V3_forbidden_conversion
V4_evidence_overclaim
```

### P4 — Runtime / Evidence / Release Perimeter

Protects deterministic execution, evidence posture, public claims, release text, DOI language, and CI-report boundaries.

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
```

Related guards:

```text
GUARD-04 empirical_claim_guard.py
GUARD-17 determinism_guard.py
GUARD-18 import_boundary_guard.py
GUARD-19 repo_path_guard.py
GUARD-20 release_claim_guard.py
```

Primary vectors:

```text
V4_evidence_overclaim
V5_nondeterminism
V6_path_status_laundering
V0_authority_inflation
```

---

## 3. Drift Vector Taxonomy

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

## 4. Evidence Classes

```text
E0 text claim
E1 static text scan
E2 AST / contract compliance
E3 deterministic test suite
E4 empirical validation
E5 external replication / deployment evidence
```

Allowed claims:

```text
E2 compliant
no blocker findings
static audit clean
CI perimeter checks passed
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
```

Guard clean state means:

```text
No configured blocker was detected within the declared perimeter.
```

It does not mean the system is safe, true, deployment-valid, or empirically proven.

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
    ci_exit: 1_on_blocker
    purpose: "repository-state refusal"
  fail_closed:
    ci_exit: 2_on_guard_runtime_error
    purpose: "guard infrastructure failure blocks confidence"
  experimental:
    ci_exit: 0
    purpose: "collect signal before enforcement"
```

Strict CI failure is repository-state refusal, not metaphysical proof.

---

## 6. Unified Finding Format

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

Invariants:

```text
ontology_authority: false
auto_fix_allowed: false
```

For ontology-facing text, guards may report drift but must not automatically rewrite meaning.

---

## 7. Shared Guard Kernel

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
```

Responsibilities:

```text
findings.py       shared dataclass/enums and invariants
reporting.py      human report, JSON report, stable ordering, safe PASS wording
text_scan.py      line/window scan, negation detection, forbidden conversion detection
contracts.py      load and validate contracts, trace rule → anchor_ref, fail closed on invalid contract
ast_scan.py       AST parsing, call detection, import alias resolution, assignment detection
roles.py          declared/inferred role detection, fail-closed unknown protected role
capabilities.py   network/subprocess/file/randomness/selection permissions
paths.py          repo-relative normalization, canonical/draft/research/formal path roles
```

---

## 8. Contract Layout

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

This separates what is protected, where it is protected, which drift vector is detected, which evidence class is allowed, and how strongly CI enforces it.

---

## 9. Guard Inventory v0.2

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

Do not implement all of these before the shared kernel exists.

---

## 10. Guard-Specific Final Roles

### GUARD-00 — Perimeter Kernel Guard

Checks that no guard, runner, manifest, or contract claims ontology authority.

Detects:

```text
guard proves truth
guard validates ontology
guard authorizes deployment
CI proves safety
runner decides validity
manifest defines ontology
contract replaces anchor
```

Output: `BLOCKER` on authority inflation.

### GUARD-01 — Canonical Ontology Guard

Keep diff-based mechanics and protected path awareness. Add shared Finding, JSON output, contract refs, anchor refs, negation-aware text scan, and safe PASS wording.

### GUARD-03 — Code Behavior Audit

Keep AST audit. Add import alias resolution, role capability matrix, shared Finding, explicit evidence class, protected object mapping, and `--format json` / `--fail-on` options.

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

Must be negation-aware, meta-example aware, contract-traced, non-authoritative, JSON-emitting, and stable-ordering.

It must not globally hide active documentation areas such as `knowledge_base/` or all `docs/`.

---

## 11. Forbidden Conversion Table

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
```

---

## 12. Negated Context Rule

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

Implementation rule:

```text
If forbidden phrase appears inside a short negation window,
classify as negated_context=true and do not block.

If same line also contains operational implementation language,
escalate to WARN for review.
```

---

## 13. Runtime / CI / External Security Stack

External tools may be used only as diagnostic layers. They do not define VECTAETOS ontology and do not validate deployment.

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
```

These tools should be integrated only after the shared guard kernel and reporting language are stable.

---

## 14. Release Claim Boundary

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

## 15. Recommended GUARD_TABLE.md Columns

```text
ID
Guard
Perimeter
Drift vectors
Evidence class
Enforcement mode
Output format
Status
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

## 16. Final Build Order

```text
0. guards/GUARD_PERIMETER_MODEL.md
1. guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md

2. guards/core/findings.py
3. guards/core/reporting.py
4. guards/core/text_scan.py
5. guards/core/contracts.py
6. guards/core/ast_scan.py
7. guards/core/roles.py
8. guards/core/capabilities.py
9. guards/core/paths.py

10. GUARD-00 perimeter_kernel_guard.py
11. refactor GUARD-12 coherence_vocabulary_guard.py
12. refactor GUARD-01 canonical_ontology_guard.py
13. refactor GUARD-03 vectaetos_code_behavior_audit.py

14. contracts/perimeter_kernel.yaml
15. contracts/perimeters/p0_repository.yaml
16. contracts/perimeters/p1_semantic_vocabulary.yaml
17. contracts/perimeters/p2_code_behavior.yaml
18. contracts/perimeters/p3_bridge_projection_trace.yaml
19. contracts/perimeters/p4_runtime_evidence_release.yaml
20. contracts/vectors/forbidden_conversion.yaml
21. contracts/evidence/evidence_classes.yaml
22. contracts/roles/code_roles.yaml

23. GUARD-13 ek_observable_non_authority_guard.py
24. GUARD-14 bridge_phi_to_ek_guard.py
25. GUARD-15 projection_boundary_guard.py
26. GUARD-16 memory_trace_boundary_guard.py
27. GUARD-17 determinism_guard.py
28. GUARD-18 import_boundary_guard.py
29. GUARD-19 repo_path_guard.py
30. GUARD-20 release_claim_guard.py
31. GUARD-21 promotion_ledger_guard.py
32. GUARD-22 contract_traceability_guard.py
```

Shared output and contract traceability must stabilize before expanding the guard perimeter.

---

## 17. Minimal Repository Patch Plan

### Phase A — Add final perimeter documents

```text
guards/GUARD_PERIMETER_MODEL.md
guards/reviews/GUARD_PERIMETER_EXPERT_REVIEW.md
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

### Phase C — Add negation-aware text scanning

```text
guards/core/text_scan.py
```

### Phase D — Add AST normalization

```text
guards/core/ast_scan.py
```

### Phase E — Extract contracts

```text
contracts/perimeter_kernel.yaml
contracts/perimeters/p0_repository.yaml
contracts/perimeters/p1_semantic_vocabulary.yaml
contracts/perimeters/p2_code_behavior.yaml
contracts/perimeters/p3_bridge_projection_trace.yaml
contracts/perimeters/p4_runtime_evidence_release.yaml
contracts/vectors/forbidden_conversion.yaml
contracts/evidence/evidence_classes.yaml
contracts/roles/code_roles.yaml
```

### Phase F — Add P3 guards

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
GUARD-15 projection_boundary_guard.py
GUARD-16 memory_trace_boundary_guard.py
```

### Phase G — Add P4 release boundary

```text
GUARD-20 release_claim_guard.py
```

### Phase H — Add governance perimeter

```text
GUARD-21 promotion_ledger_guard.py
GUARD-22 contract_traceability_guard.py
```

---

## 18. Safe PASS / FAIL Wording

Allowed PASS wording:

```text
PASS: No configured blocker was detected within the declared perimeter.
PASS: Repository-state check completed without configured blockers.
PASS: Static scan produced no findings at or above the configured enforcement level.
```

Forbidden PASS wording:

```text
PASS: ontology preserved.
PASS: VECTAETOS is safe.
PASS: system is valid.
PASS: semantic correctness proven.
PASS: deployment ready.
```

Allowed FAIL wording:

```text
FAIL: configured blocker detected within declared repository perimeter.
FAIL: guard infrastructure error; confidence unavailable.
FAIL: release claim exceeds declared evidence class.
```

Forbidden FAIL wording:

```text
FAIL: ontology is false.
FAIL: system is dangerous.
FAIL: metaphysical corruption proven.
FAIL: truth invalidated.
```

---

## 19. Canonical Repo Sentence

English:

```text
The VECTAETOS perimeter guard system exposes semantic, architectural,
behavioral, runtime, and release-claim drift relative to canonical anchors
and machine-readable contracts. It protects repository state only. It does
not define ontology, prove truth, validate safety, optimize behavior,
authorize deployment, or mutate Φ.
```

Slovak:

```text
Perimeter guard systém VECTAETOS exponuje sémantický, architektonický,
behaviorálny, runtime a release-claim drift voči kanonickým anchorom
a strojovo čitateľným kontraktom. Chráni iba stav repozitára. Nedefinuje
ontológiu, nedokazuje pravdu, nevaliduje bezpečnosť, neoptimalizuje správanie,
neautorizuje deployment a nemutuje Φ.
```

---

## 20. Non-Goals

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
```

This model only defines a repository perimeter for drift exposure.

---

## 21. Final Operating Principle

```text
Guard exposes drift.
Contract projects anchor constraints.
Anchor preserves semantic source.
CI refuses repository state.
None of these becomes ontology.
```

Slovak:

```text
Guard exponuje drift.
Kontrakt projektuje hranice anchorov.
Anchor uchováva sémantický zdroj.
CI odmieta stav repozitára.
Nič z toho sa nestáva ontológiou.
```

End of document.
