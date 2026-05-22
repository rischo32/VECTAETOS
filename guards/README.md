# VECTAETOS Guards

## Status

Fundamental repository perimeter layer.

## Purpose

This directory contains guard scripts for protecting the canonical structure and repository boundary of VECTAETOS.

Guards do not define ontology.

Guards do not interpret meaning.

Guards do not decide.

Guards do not validate deployment.

Guards only scan, detect, report, and fail closed when repository content violates canonical boundaries.

---

## Scope

The guard layer protects repository language, code roles, layer boundaries, evidence claims, feedback separation, Vortex posture, QE terminology, triality posture, and Master Index routing.

This layer is external to Φ, K(Φ), κ, QE, Vortex, projection, audit, memory, and triadic identity.

Guard output is a repository signal.

Guard output is not ontology.

Guard output is not empirical proof.

---

## Repository Boundary Sources

The guard perimeter is aligned with:

```text
/VOCABULARY_LOCK.md
/contracts/ASSEMBLY_MANIFEST.json
/contracts/LAYER_BOUNDARIES.md
/contracts/vectaetos_code_contract.json
/contracts/vectaetos_contract.json
/MASTER_INDEX.md
/anchors/
/formal/
```

These files define repository language and boundary conditions.

Guards mechanically protect those boundaries.

---

## Guard Classes

### Level 0 — Fundamental Repository Perimeter

These guards protect the root perimeter of the repository.

Active examples:

```text
GUARD-01 canonical_ontology_guard.py
GUARD-02 vectaetos_boundary_guard.py
GUARD-03 vectaetos_code_behavior_audit.py
GUARD-04 empirical_claim_guard.py
GUARD-05 repo_layer_boundary_guard.py
GUARD-06 no_feedback_loop_guard.py
GUARD-07 vortex_non_agentic_guard.py
```

---

### Level 1 — Specialized Ontological Guards

These guards protect specific ontological structures and vocabulary boundaries.

Active examples:

```text
GUARD-08 qe_aporia_guard.py
GUARD-09 triality_guard.py
GUARD-10 vector_drift_guard.py
GUARD-11 master_index_router_guard.py
```

Planned examples:

```text
GUARD-12 coherence_vocabulary_guard.py
```

---

### Level 2 — Bridge / EK / Layer-Specific Guards

These guards protect downstream bridge logic and layer-specific vocabulary.

Planned examples:

```text
GUARD-13 ek_observable_non_authority_guard.py
GUARD-14 bridge_phi_to_ek_guard.py
```

---

### Level 3 — Runner / CI / Release Perimeter

These tools coordinate deterministic perimeter execution and reporting.

Active examples:

```text
guards/perimeter_manifest.json
guards/run_perimeter.py
```

---

## Active Guards

### GUARD-01 — Canonical Ontology Guard

File:

```text
canonical_ontology_guard.py
```

Status:

```text
ACTIVE / STRICT / REQUIRED
```

Role:

Diff-based protection of canonical ontology, formal anchors, protected repository boundary files, and high-risk semantic drift in changed files.

This guard requires base and head revisions.

Typical CI form:

```bash
python3 guards/canonical_ontology_guard.py --base "$BASE_SHA" --head "$HEAD_SHA" --mode strict
```

---

### GUARD-02 — VECTAETOS Boundary Guard

File:

```text
vectaetos_boundary_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Repository-wide semantic perimeter scan for incompatible formulations defined by the canonical boundary vocabulary.

This guard is broader than GUARD-01 and can run locally over the full repository.

Typical local form:

```bash
python3 guards/vectaetos_boundary_guard.py --root . --mode report
```

Typical CI form:

```bash
python3 guards/vectaetos_boundary_guard.py --root . --mode strict
```

---

### GUARD-03 — Code Behavior Audit

File:

```text
vectaetos_code_behavior_audit.py
```

Contract:

```text
contracts/vectaetos_code_contract.json
```

Status:

```text
ACTIVE / CONTRACT-BASED / REQUIRED
```

Role:

Static AST audit of Python code behavior against role contracts.

This is not a deployment validator.

This is not empirical evidence.

This is not a security certification.

Typical form:

```bash
python3 guards/vectaetos_code_behavior_audit.py --root . --contract contracts/vectaetos_code_contract.json
```

---

### GUARD-04 — Empirical Claim Guard

File:

```text
empirical_claim_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects evidence language and prevents repository text from exceeding the L0–L4 evidence ladder.

Typical local form:

```bash
python3 guards/empirical_claim_guard.py --root . --mode report
```

Typical CI form:

```bash
python3 guards/empirical_claim_guard.py --root . --mode strict
```

---

### GUARD-05 — Repository Layer Boundary Guard

File:

```text
repo_layer_boundary_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects VECTAETOS / ASIMULATOR / ASI_MOD layer dependency boundaries.

Typical form:

```bash
python3 guards/repo_layer_boundary_guard.py --root . --mode strict
```

---

### GUARD-06 — No Feedback Loop Guard

File:

```text
no_feedback_loop_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects the acyclic boundary between output-facing, trace-facing, and ontology-facing layers.

Typical form:

```bash
python3 guards/no_feedback_loop_guard.py --root . --mode strict
```

---

### GUARD-07 — Vortex Non-Agentic Guard

File:

```text
vortex_non_agentic_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects Vortex vocabulary and implementation posture as an external candidate-trajectory exposure layer.

Typical form:

```bash
python3 guards/vortex_non_agentic_guard.py --root . --mode strict
```

---

### GUARD-08 — QE Aporia Guard

File:

```text
qe_aporia_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects QE terminology as non-representability vocabulary.

Typical form:

```bash
python3 guards/qe_aporia_guard.py --root . --mode strict
```

---

### GUARD-09 — Triality Guard

File:

```text
triality_guard.py
```

Status:

```text
ACTIVE / STRICT-CAPABLE / REQUIRED
```

Role:

Protects triality and OAAT posture from collapse into flattened layer symmetry or privileged-axis language.

Typical form:

```bash
python3 guards/triality_guard.py --root . --mode strict
```

---

### GUARD-10 — Vector Drift Guard

File:

```text
vector_drift_guard.py
```

Status:

```text
ACTIVE / OBSERVABLE / OPTIONAL IN MANIFEST
```

Role:

Reports vector drift as an external observable.

It remains outside Φ and outside ontology.

Typical local form:

```bash
python3 guards/vector_drift_guard.py --root . --mode report
```

Typical CI form:

```bash
python3 guards/vector_drift_guard.py --root . --mode ci --fail_at 0.70
```

---

### GUARD-11 — Master Index Router Guard

File:

```text
master_index_router_guard.py
```

Status:

```text
ACTIVE / ROUTER-INTEGRITY / REQUIRED
```

Role:

Checks Master Index routing integrity and referenced formal-document availability.

Typical form:

```bash
python3 guards/master_index_router_guard.py --repo-root . --mode check
```

Inventory form:

```bash
python3 guards/master_index_router_guard.py --repo-root . --mode inventory
```

---

## Planned Guards

### GUARD-12 — Coherence Vocabulary Guard

File:

```text
coherence_vocabulary_guard.py
```

Status:

```text
PLANNED / INACTIVE IN MANIFEST
```

Role:

Will protect active vocabulary alignment with `/VOCABULARY_LOCK.md`.

---

### GUARD-13 — EK Observable Non-Authority Guard

File:

```text
ek_observable_non_authority_guard.py
```

Status:

```text
PLANNED / INACTIVE IN MANIFEST
```

Role:

Will protect EK observables from being used as ontology, admissibility, or deployment language.

---

### GUARD-14 — Bridge Φ to EK Guard

File:

```text
bridge_phi_to_ek_guard.py
```

Status:

```text
PLANNED / INACTIVE IN MANIFEST
```

Role:

Will protect `/formal/BRIDGE_PHI_TO_EK.md` and corresponding implementation vocabulary.

---

## Perimeter Manifest

File:

```text
guards/perimeter_manifest.json
```

Status:

```text
ACTIVE MANIFEST
```

Role:

Deterministic registry of guard commands.

The manifest stores:

```text
guard id
guard name
path
level
active flag
required flag
profile command templates
exit mapping
execution order
```

The manifest is not a guard.

The manifest does not interpret findings.

The manifest does not define ontology.

---

## Perimeter Runner

File:

```text
guards/run_perimeter.py
```

Status:

```text
ACTIVE RUNNER
```

Role:

Manifest-driven guard orchestrator.

The runner may:

```text
read manifest
expand variables
execute active command templates
preserve stdout and stderr
write JSON and Markdown reports
return consolidated exit codes
```

The runner may not:

```text
modify repository content
suppress findings
create ontology
create empirical proof
replace individual guard behavior
```

---

## Runner Usage

List guards:

```bash
python3 guards/run_perimeter.py --root . --list
```

Local report profile:

```bash
python3 guards/run_perimeter.py --root . --profile report
```

Local report with strict exit:

```bash
python3 guards/run_perimeter.py --root . --profile report --strict-exit
```

CI profile:

```bash
python3 guards/run_perimeter.py --root . --profile ci --base "$BASE_SHA" --head "$HEAD_SHA"
```

Dry run:

```bash
python3 guards/run_perimeter.py --root . --profile ci --dry-run
```

Run one guard:

```bash
python3 guards/run_perimeter.py --root . --only GUARD-08
```

Create reports:

```bash
python3 guards/run_perimeter.py   --root .   --profile ci   --base "$BASE_SHA"   --head "$HEAD_SHA"   --json-out reports/perimeter.json   --md-out reports/perimeter.md
```

---

## Runner Exit Codes

```text
0 = selected required guards completed without findings
1 = one or more selected required guards reported findings
2 = one or more selected required guards failed to execute or had configuration errors
3 = manifest or runner error
```

In `report` profile, findings are visible but do not block by default.

Use `--strict-exit` if local report mode should return nonzero on findings.

---

## Environment Variables

Diff-based guards may use:

```text
BASE_SHA
HEAD_SHA
```

The runner accepts explicit values:

```bash
python3 guards/run_perimeter.py --base "$BASE_SHA" --head "$HEAD_SHA"
```

If not provided, the runner attempts to use environment values.

---

## Recommended CI Shape

```yaml
- name: Run VECTAETOS perimeter
  run: |
    python3 guards/run_perimeter.py       --root .       --profile ci       --base "$BASE_SHA"       --head "$HEAD_SHA"       --json-out reports/perimeter.json       --md-out reports/perimeter.md
```

The CI workflow must set usable `BASE_SHA` and `HEAD_SHA` values before invoking the runner.

---

## Semantic Errata

File:

```text
anchors/SEMANTIC_ERRATA.md
```

Role:

Registers known historical semantic drift in immutable, frozen, archived, or explicitly errata-covered documents without rewriting those documents.

Semantic errata do not define ontology.

Semantic errata do not replace anchors.

Semantic errata do not authorize new drift in active files.

Registered errata may guide guard behavior only for historical or explicitly frozen contexts.

Active files should be corrected directly.

---

## Vocabulary Lock

File:

```text
/VOCABULARY_LOCK.md
```

Role:

Repository-wide terminology lock.

This file is guard-safe and avoids literal incompatible example phrases in active text.

It should be used as the lexical reference for future vocabulary guards.

---

## Final Statement

The guard perimeter protects repository boundaries.

It does not create authority.

It does not create ontology.

It does not create empirical validation.

It only makes drift visible and fail-closed.
