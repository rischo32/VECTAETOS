# VECTAETOS_CODE_SENTINEL_AND_BEHAVIOR_AUDIT_ANCHOR.md
## VECTAETOS™ Code Sentinel and Behavior Audit Anchor
### Status: PRELIMINARY / CANONICAL CANDIDATE
### Ontological Role: Developer-Surface Drift Detection and Code-Behavior Audit Anchor
### Scope: VECTAETOS™ / ASIMULATOR™ / ASI_MOD™ / Anchors / Contracts / LSP / CI
### Modification Policy: Controlled extension only

---

## 0. PURPOSE

This anchor defines the role, boundary, and admissible behavior of the VECTAETOS Code Sentinel and Behavior Audit system.

Its purpose is to prevent semantic, architectural, and behavioral drift in code without turning the audit layer into an authority, optimizer, decision engine, or ontology.

The system has two operational surfaces:

```text
LSP Sentinel  → live developer-facing diagnostics
CLI Audit     → deterministic repository / CI enforcement
```

Both surfaces must derive their rules from canonical anchors and machine-readable contracts.

Neither surface may become the source of ontology.

---

## 1. CORE THESIS

The Code Sentinel and Behavior Audit system does not decide whether code is true.

It exposes whether code appears to violate declared VECTAETOS architectural constraints.

```text
diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
warning ≠ verdict
failure ≠ metaphysical proof
```

The system exists to preserve alignment between:

```text
canonical anchors
behavior contracts
repository structure
runtime-adjacent code behavior
developer feedback
CI enforcement
```

---

## 2. PRIMARY DISTINCTION

The architecture distinguishes three layers of validation:

```text
Anchor      = semantic source
Contract    = machine-readable rule projection
Audit       = behavioral and structural detection
```

Meaning:

- anchors define canonical meaning,
- contracts encode enforceable constraints,
- audits detect apparent violations,
- diagnostics expose drift,
- CI gates block invalid repository states.

No layer may collapse into another.

---

## 3. SYSTEM COMPONENTS

### 3.1 Canonical Anchors

Canonical anchors are the semantic source of the system.

They define:

- non-agentic posture,
- no optimization,
- no decision power,
- no feedback into Φ,
- no authority inflation,
- layer boundaries,
- admissible and inadmissible behavior.

Anchors are not executable policy engines.

Anchors must not be mutated by LSP, audit, memory, runtime code, or automated refactoring.

---

### 3.2 Behavior Contracts

Behavior contracts are machine-readable projections of canonical anchors.

They may define:

- roles,
- allowed imports,
- forbidden imports,
- allowed filesystem operations,
- forbidden mutation targets,
- allowed randomness,
- allowed network usage,
- role-specific constraints,
- severity levels.

Contracts are not ontology.

They are operational projections used for deterministic checking.

---

### 3.3 Shared Rule Engine

The shared rule engine is the common implementation layer used by both:

```text
LSP Sentinel
CLI Behavior Audit
```

It must contain:

- AST analysis helpers,
- role inference,
- rule loading,
- violation classification,
- severity mapping,
- diagnostic normalization,
- deterministic report generation.

The rule engine must not create new ontology.

It may only operationalize existing anchors and contracts.

---

### 3.4 LSP Sentinel

The LSP Sentinel is a developer-facing live diagnostic layer.

It may:

- analyze open files,
- analyze saved files,
- show diagnostics,
- show hover explanations,
- expose anchor-derived context,
- warn about possible drift,
- point to relevant anchors or contracts.

It may not:

- rewrite code automatically,
- mutate canonical anchors,
- decide correctness,
- optimize code toward a preferred architecture,
- silently fix semantic violations,
- claim proof of safety,
- replace CI.

The LSP Sentinel is advisory.

---

### 3.5 CLI Behavior Audit

The CLI Behavior Audit is a deterministic repository-level guard.

It may:

- scan code,
- parse AST,
- classify hard and soft violations,
- emit structured reports,
- fail CI on hard violations,
- enforce role contracts,
- enforce forbidden behavior,
- detect architectural drift.

It may not:

- modify files,
- mutate anchors,
- mutate contracts without explicit commit,
- infer hidden ontology,
- validate deployment,
- claim empirical safety,
- replace human review.

The CLI Behavior Audit is enforceable, but not ontological.

---

### 3.6 CI Integration

CI is the repository enforcement surface.

It may:

- run CLI audits,
- block pull requests,
- block merges,
- verify anchor hashes,
- verify contracts,
- verify layer boundaries,
- verify no reverse dependency flows.

CI may not:

- define canonical meaning,
- rewrite repository history,
- auto-legitimize empirical claims,
- replace canonical review,
- promote advisory diagnostics into ontology.

CI is a gate.

It is not the root.

---

## 4. JEDI / PYTHON LANGUAGE SERVER BOUNDARY

Jedi or any Python language server may provide standard Python intelligence:

- completion,
- hover,
- goto definition,
- references,
- rename,
- signature help,
- Python diagnostics.

Vectaetos Sentinel provides a different layer:

- ontological drift diagnostics,
- anchor-aware hover,
- role-boundary warnings,
- behavior-contract violations,
- non-agentic posture checks.

Therefore:

```text
Jedi = Python code intelligence
Vectaetos Sentinel = architectural drift exposure
```

They may coexist.

They must not be semantically merged.

The Sentinel must not claim to replace Jedi.

Jedi must not be treated as an ontological validator.

---

## 5. NON-AGENCY LAW

The Sentinel and Audit system must remain non-agentic.

It may observe code.

It may classify apparent drift.

It may emit diagnostics.

It may fail closed in CI.

It may not decide what the system should become.

Forbidden behaviors:

```text
optimize architecture
select best trajectory
choose preferred state
reward compliant code
punish non-compliant code beyond CI failure
auto-rewrite canonical meaning
self-update policy without anchor change
```

---

## 6. NON-INTERVENTION LAW

The Sentinel and Audit system must not intervene in Φ or in canonical ontology.

Forbidden:

```text
LSP → anchor mutation
CLI audit → anchor mutation
CI → ontology rewrite
diagnostic → truth claim
hover → authority claim
autofix → semantic rewrite
memory → canonical source
```

Allowed:

```text
observe
parse
classify
warn
report
fail closed
link to source anchor
```

---

## 7. MUTATION BOUNDARIES

The following objects are canonical or root-adjacent and must not be mutated by downstream diagnostic systems:

```text
Φ
Σ
R
K(Φ)
κ
QE
canonical anchors
assembly manifest
validity anchors
empirical evidence anchors
layer boundary contracts
```

Any attempted mutation of these objects by unauthorized layers must be treated as a hard violation.

Examples of hard violations:

```text
Vortex mutates Φ
Projection rewrites R
Audit modifies anchor files
LSP auto-edits canonical constraints
Memory overrides contracts
ASI_MOD claims truth authority
ASIMULATOR must not define ontology
```

---

## 8. ROLE POLICY

Code behavior must be evaluated relative to declared or inferred role.

Recommended roles:

```text
ontology
vortex
projection
audit
memory
lsp
cli_guard
adapter
test
docs_tooling
```

Each role has different permissions.

Example policy:

```text
ontology:
  may_define: Φ, Σ, R, K, κ
  may_mutate_runtime: false

vortex:
  may_explore: true
  may_mutate_phi: false
  may_optimize: false

projection:
  may_render: true
  may_interpret: false
  may_write_back: false

audit:
  may_observe: true
  may_record: true
  may_hash: true
  may_command: false

memory:
  may_trace: true
  may_instruct: false
  may_override_anchor: false

lsp:
  may_warn: true
  may_autofix_semantics: false
  may_claim_truth: false

cli_guard:
  may_fail_ci: true
  may_modify_files: false
```

---

## 9. SEVERITY MODEL

Diagnostics should distinguish severity.

```text
INFO      = contextual note
WARNING   = possible drift
ERROR     = hard architectural violation
BLOCKER   = repository-invalidating violation
```

Recommended mapping:

```text
naming drift                       → WARNING
forbidden agentic terminology      → WARNING / ERROR by role
forbidden import                   → ERROR
Φ mutation by downstream layer      → BLOCKER
anchor mutation by tool            → BLOCKER
audit issuing command              → BLOCKER
projection claiming interpretation → ERROR / BLOCKER
```

Severity must be deterministic.

Severity must not depend on rhetorical confidence.

---

## 10. HARD VIOLATION CLASSES

The following classes are hard violations unless explicitly allowed by contract:

```text
AGENCY_INJECTION
OPTIMIZATION_INJECTION
TRUTH_AUTHORITY_CLAIM
PHI_MUTATION
ANCHOR_MUTATION
REVERSE_DEPENDENCY
AUDIT_COMMAND
PROJECTION_AS_ONTOLOGY
MEMORY_AS_AUTHORITY
RANDOMNESS_WITHOUT_DECLARATION
NETWORK_WITHOUT_DECLARATION
SUBPROCESS_WITHOUT_DECLARATION
DYNAMIC_EXECUTION
UNDECLARED_FILE_MUTATION
```

---

## 11. SOFT WARNING CLASSES

The following classes may be warnings depending on role and context:

```text
AMBIGUOUS_LAYER_NAMING
POSSIBLE_AUTHORITY_LANGUAGE
POSSIBLE_SELECTION_LANGUAGE
POSSIBLE_REWARD_LANGUAGE
POSSIBLE_POLICY_LANGUAGE
POSSIBLE_SEMANTIC_DRIFT
UNDECLARED_ROLE
MISSING_CONTRACT_REFERENCE
MISSING_ANCHOR_REFERENCE
```

Soft warnings must not block CI unless configured as strict mode.

---

## 12. DYNAMIC EXECUTION POLICY

The following calls are forbidden in canonical or root-adjacent code unless explicitly justified in contract:

```text
eval
exec
compile
__import__
```

Reason:

Dynamic execution can bypass static architecture checks.

If allowed in tooling, it must be:

- isolated,
- documented,
- role-scoped,
- tested,
- never permitted to mutate anchors or Φ.

---

## 13. FILESYSTEM POLICY

Filesystem writes are forbidden in ontology, projection, and audit roles unless explicitly declared.

Allowed examples:

```text
audit may write deterministic reports
cli_guard may write local report artifacts
test may write temporary files
docs_tooling may generate documentation
```

Forbidden examples:

```text
audit rewrites anchors
lsp rewrites canonical files
memory writes contracts
projection modifies ontology files
vortex rewrites Φ definitions
```

---

## 14. NETWORK POLICY

Network access is forbidden by default.

It may be allowed only for explicitly declared tooling roles.

Network access must not be used to:

- fetch canonical ontology dynamically,
- mutate anchors,
- bypass hash locks,
- outsource authority,
- validate truth through remote source alone.

Canonical anchors must remain locally auditable.

---

## 15. RANDOMNESS POLICY

Randomness is forbidden in ontology and audit-critical checks unless explicitly deterministic.

Allowed:

```text
seeded test randomness
simulation experiments marked non-canonical
fuzzing under deterministic seed logs
```

Forbidden:

```text
random canonical state
random verdict
random ontology update
random CI admissibility result
```

---

## 16. DIAGNOSTIC TEXT POLICY

Diagnostic messages must be precise, non-mystical, non-authoritarian, and actionable.

Allowed diagnostic form:

```text
ARCHITECTURAL VIOLATION:
This symbol appears to introduce optimization in a non-optimizing layer.
Source: behavior contract / anchor reference.
```

Forbidden diagnostic form:

```text
The truth rejects this code.
The field commands you to change this.
The system knows this is wrong.
```

Diagnostics expose drift.

They do not speak as ontology.

---

## 17. HOVER POLICY

Hover text may explain:

- term definition,
- layer role,
- relevant anchor principle,
- why a warning exists,
- what boundary is at risk.

Hover text may not:

- declare final truth,
- command action,
- simulate authority,
- hide uncertainty,
- turn interpretation into ontology.

Recommended form:

```text
VECTAETOS Sentinel:
This term is associated with selection / optimization.
In non-agentic layers, this may indicate architectural drift.
```

---

## 18. AUTOFIX POLICY

Automatic fixes are forbidden for semantic and ontological violations.

Allowed:

```text
formatting
import sorting
dead whitespace removal
mechanical typo fix in non-canonical files
```

Forbidden:

```text
rename ontology terms automatically
rewrite anchor language
change role declarations
remove forbidden code without human review
convert warning into compliant-looking code silently
```

Autofix may never create semantic compliance by hiding drift.

---

## 19. CONTRACT STRUCTURE

A behavior contract should contain at minimum:

```yaml
vectaetos_code_contract:
  version: "0.1"
  default_mode: fail_closed
  roles:
    ontology: {}
    vortex: {}
    projection: {}
    audit: {}
    memory: {}
    lsp: {}
    cli_guard: {}
    adapter: {}
    test: {}
  forbidden_terms: []
  forbidden_calls: []
  forbidden_imports: []
  mutation_targets:
    protected:
      - "Φ"
      - "PHI"
      - "Phi"
      - "Sigma"
      - "R"
      - "K"
      - "kappa"
      - "QE"
  severity:
    hard_violation: error
    root_mutation: blocker
```

---

## 20. REPORT STRUCTURE

A CLI audit report should contain:

```yaml
audit_report:
  tool: vectaetos_code_behavior_audit
  version: string
  root: string
  contract: string
  files_scanned: integer
  findings:
    - file: string
      line: integer
      column: integer
      severity: INFO | WARNING | ERROR | BLOCKER
      code: string
      message: string
      role: string
      anchor_reference: string | null
  exit_code: 0 | 1 | 2
```

Reports must be deterministic for the same input tree and same contract.

---

## 21. LSP OUTPUT STRUCTURE

LSP diagnostics should map audit findings into editor-visible diagnostics:

```text
finding severity → LSP DiagnosticSeverity
finding location → Range
finding code     → Diagnostic.code
finding message  → Diagnostic.message
finding source   → "VectaetosSentinel"
```

The LSP layer may suppress or downgrade some warnings for developer ergonomics.

It must never suppress hard root violations unless explicitly configured for experimental mode.

---

## 22. FAIL-CLOSED PRINCIPLE

When the tool cannot determine whether a root-adjacent action is admissible, it must fail closed in CI.

```text
unknown role + protected mutation → fail
unknown contract + root mutation → fail
missing anchor + ontology edit → fail
unclear authority flow → fail or warning by strictness
```

In LSP mode, uncertainty may be shown as warning.

In CI mode, uncertainty near protected roots should be hard failure.

---

## 23. DEVELOPMENT MODES

The system may support modes:

```text
advisory
strict
canonical
experimental
```

Recommended meanings:

```text
advisory:
  warnings only, no blocking

strict:
  errors block CI

canonical:
  root-adjacent violations are blockers

experimental:
  exploratory code allowed only outside canonical paths
```

No experimental mode may be used to legitimize canonical claims.

---

## 24. CANONICAL PATHS

The following paths should be treated as root-adjacent by default:

```text
anchors/
formal/
contracts/
governance/
core/
ontology/
vectaetos/
```

The exact list must be repository-defined.

Canonical paths require stronger enforcement.

---

## 25. NON-CANONICAL PATHS

The following paths may allow softer enforcement:

```text
experiments/
scratch/
notebooks/
examples/
playground/
drafts/
```

However, non-canonical paths may not claim canonical authority.

Any artifact promoted from non-canonical to canonical path must pass full audit.

---

## 26. INTEGRATION WITH EMPIRICAL EVIDENCE

Passing the Code Sentinel or Behavior Audit does not imply empirical validation.

```text
CI pass ≠ empirical proof
LSP clean ≠ safety
audit clean ≠ E = 1
```

These tools support L1 / L2 evidence only.

They cannot establish L4 real-world validation.

---

## 27. FAILURE MODES

The Sentinel and Audit architecture fails if:

```text
LSP becomes authority
CLI audit rewrites code
CI rewrites ontology
diagnostics claim truth
hover creates semantic authority
Jedi is treated as ontology
anchor parser invents rules not present in anchors/contracts
contracts drift from anchors
warnings hide hard violations
autofix hides semantic drift
audit output becomes command layer
```

---

## 28. MINIMUM IMPLEMENTATION ROADMAP

### Phase A — Shared Core

- extract AST logic into shared rule engine
- define finding dataclass
- define role inference
- load contract from JSON/YAML
- normalize diagnostic severity

### Phase B — CLI Guard

- scan repository
- generate deterministic report
- return exit codes
- integrate with CI
- enforce fail-closed behavior

### Phase C — LSP Sentinel

- use shared rule engine
- publish diagnostics on open/save/change
- provide anchor-aware hover
- optionally expose code actions for documentation links only

### Phase D — Contract Hardening

- define role policies
- define protected symbols
- define path scopes
- define strict/canonical modes
- define allowed exceptions

### Phase E — Regression Tests

- test forbidden agentic names
- test protected Φ mutation
- test audit command violation
- test projection-as-ontology
- test random/network/subprocess policy
- test deterministic report stability

---

## 29. MACHINE-CHECKABLE SUMMARY

```yaml
vectaetos_code_sentinel_and_behavior_audit:
  status: preliminary_canonical_candidate

  surfaces:
    lsp_sentinel:
      role: advisory_developer_diagnostics
      may:
        - observe_open_documents
        - publish_diagnostics
        - provide_hover_context
        - expose_anchor_references
      may_not:
        - mutate_code_semantically
        - mutate_anchors
        - claim_truth
        - replace_ci
        - optimize_architecture

    cli_behavior_audit:
      role: deterministic_repository_guard
      may:
        - scan_code
        - parse_ast
        - classify_findings
        - emit_reports
        - fail_ci
      may_not:
        - modify_files
        - mutate_anchors
        - validate_deployment
        - claim_empirical_safety

  semantic_source:
    - canonical_anchors

  machine_source:
    - behavior_contracts

  shared_engine_required: true

  protected_objects:
    - "Φ"
    - "PHI"
    - "Phi"
    - "Σ"
    - "Sigma"
    - "R"
    - "K(Φ)"
    - "K"
    - "κ"
    - "kappa"
    - "QE"
    - "canonical anchors"

  hard_violations:
    - agency_injection
    - optimization_injection
    - truth_authority_claim
    - phi_mutation
    - anchor_mutation
    - reverse_dependency
    - audit_command
    - projection_as_ontology
    - memory_as_authority
    - dynamic_execution
    - undeclared_file_mutation

  formulas:
    - "diagnostic != truth"
    - "audit != ontology"
    - "guard != authority"
    - "lsp_clean != empirical_proof"
    - "ci_pass != E=1"
```

---

## 30. CANONICAL SENTENCE

The VECTAETOS Code Sentinel and Behavior Audit system is a non-authoritative developer and repository guard that exposes architectural drift derived from canonical anchors and behavior contracts. The LSP Sentinel warns; the CLI Audit enforces repository constraints; the anchors remain the semantic source. No diagnostic, audit, guard, or language-server feature may become ontology, authority, optimizer, or decision engine.

---

## 31. SHORT FORMULA

```text
anchors → contracts → shared rule engine → { LSP diagnostics, CLI audit }

LSP = advisory
CLI = enforceable
Anchor = semantic source

diagnostic ≠ truth
audit ≠ ontology
guard ≠ authority
CI pass ≠ empirical proof
```

---

© VECTAETOS™ / ASIMULATOR™ / ASI_MOD™
