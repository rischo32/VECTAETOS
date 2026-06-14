# VECTAETOS GUARDS
## Status

Fundamental repository perimeter / MATICA_PERIMETER implementation layer.

```text
Perimeter môže byť tvrdší, ale nikdy autoritatívnejší.
```

## Purpose

This directory contains guard scripts and guard-facing implementation notes for protecting the repository boundary of VECTAETOS.

Guards do not define ontology.

Guards do not interpret meaning.

Guards do not decide.

Guards do not validate deployment.

Guards only scan, detect, report, and fail closed when repository content violates declared repository boundaries.

---

## Scope

The guard layer protects:

```text
repository language
code roles
layer boundaries
evidence claims
feedback separation
Vortex posture
QE terminology
triality posture
Master Index routing
EK / audit observable boundaries
license stack integrity
```

This layer is external to:

```text
Φ
K(Φ)
κ
QE
Vortex
projection
audit
memory
triadic identity
```

Guard output is a repository signal.

Guard output is not ontology.

Guard output is not empirical proof.

---

## Repository Boundary Sources

The guard perimeter is aligned with canonical and machine-readable boundary sources.

Current known sources:

```text
/VOCABULARY_LOCK.md
/MASTER_INDEX.md
/anchors/
/formal/
/contracts/perimeter_manifest.json
/contracts/vectaetos_code_contract.json
/contracts/LICENSE_REGISTRY.json
/contracts/guard13_ek_observable_rules.json
/guards/MATICA_PERIMETER.md
/guards/GUARD_PERIMETER_MODEL.md
```

If one of these files is missing in the current repository state, it is a repository alignment issue, not an ontological issue.

These files define repository language, guard execution boundaries, or machine-readable guard contracts.

Guards mechanically protect those boundaries.

They do not create those boundaries.

---

## Directory Roles

```text
guards/
    guard scripts
    guard README
    perimeter implementation model
    shared guard core
    optional/staged runner

contracts/
    machine-readable contracts
    rule registries
    perimeter manifest
    license registry
    guard-specific rule files

.github/workflows/
    CI entrypoints invoking guards or the staged runner

tests/guards/
    guard tests and fixtures
```

Important boundary:

```text
manifest ∈ contracts/
runner ∈ guards/
guard scripts ∈ guards/
guard contracts ∈ contracts/
guard tests ∈ tests/guards/
```

---

## Current Perimeter Map

The working implementation matrix is:

```text
guards/MATICA_PERIMETER.md
```

It maps guards to:

```text
level × drift vector × evidence class × enforcement mode × integrity posture
```

Core invariant:

```text
Guard exponuje drift; nedefinuje pravdu.
```

This README follows `guards/MATICA_PERIMETER.md` as the current human-readable perimeter map.

If this README and the machine-readable manifest disagree, the repository must be realigned.

This README does not override the manifest.

The manifest does not override canonical anchors.

---

## Level Index

```text
Level 0 — Fundamental Repository Perimeter
Level 1 — Specialized Ontological Perimeter
Level 2 — Semantic / Ontological Vocabulary Perimeter
Level 3 — Code Behavior Perimeter
Level 4 — Bridge / Projection / Trace Perimeter
Level 5 — Runtime / Evidence / Release Perimeter
```

---

## Guard Matrix Summary

| ID | Guard file | Level | Status | Role |
|---|---|---:|---|---|
| GUARD-00 | `perimeter_kernel_guard.py` | 0 | PLANNED,MVP | perimeter kernel |
| GUARD-01 | `canonical_ontology_guard.py` | 0 | ACTIVE,REFAC,MVP | canonical boundary |
| GUARD-02 | `vectaetos_boundary_guard.py` | 0 | PLANNED | repository boundary |
| GUARD-03 | `vectaetos_code_behavior_audit.py` | 3 | ACTIVE,REFAC,MVP | code behavior |
| GUARD-04 | `empirical_claim_guard.py` | 5 | PLANNED | claim boundary |
| GUARD-05 | `repo_layer_boundary_guard.py` | 0 | PLANNED | layer shape |
| GUARD-06 | `no_feedback_loop_guard.py` | 1 | PLANNED | feedback block |
| GUARD-07 | `vortex_non_agentic_guard.py` | 1 | ACTIVE,REFAC | Vortex non-agentic |
| GUARD-08 | `qe_aporia_guard.py` | 1 | ACTIVE,REFAC | QE aporia |
| GUARD-09 | `triality_guard.py` | 1 | ACTIVE,REFAC | triality boundary |
| GUARD-10 | `vector_drift_guard.py` | 2 | ACTIVE,REFAC | vector terms |
| GUARD-11 | `master_index_router_guard.py` | 0 | ACTIVE,REFAC | index router |
| GUARD-12 | `coherence_vocabulary_guard.py` | 2 | ACTIVE,REFAC,MVP,REPORT | coherence terms |
| GUARD-13 | `ek_observable_non_authority_guard.py` | 4 | PLANNED | EK observables |
| GUARD-14 | `bridge_phi_to_ek_guard.py` | 4 | PLANNED | Φ→EK bridge |
| GUARD-15 | `projection_boundary_guard.py` | 4 | PLANNED | projection boundary |
| GUARD-16 | `memory_trace_boundary_guard.py` | 4 | PLANNED | memory traces |
| GUARD-17 | `determinism_guard.py` | 3 | PLANNED | deterministic tests |
| GUARD-18 | `import_boundary_guard.py` | 3 | PLANNED | import direction |
| GUARD-19 | `repo_path_guard.py` | 0 | CORE_READY | path policy |
| GUARD-20 | `release_claim_guard.py` | 5 | PLANNED,MVP | release claims |
| GUARD-21 | `promotion_ledger_guard.py` | 5 | PLANNED | promotion ledger |
| GUARD-22 | `contract_traceability_guard.py` | 0 | CORE_READY | contract trace |
| GUARD-23 | `guard_runtime_integrity_guard.py` | 0 | PLANNED | runtime identity |
| GUARD-24 | `anchor_blob_integrity_guard.py` | 0 | CORE_READY | anchor hashes |
| GUARD-25 | `ontology_creep_guard.py` | 2 | PLANNED | slow drift |
| GUARD-26 | `inter_guard_coupling_guard.py` | 3 | PLANNED | guard isolation |
| GUARD-27 | `evidence_attestation_guard.py` | 5 | PLANNED | evidence wording |
| GUARD-28 | `dependency_supply_chain_guard.py` | 5 | PLANNED | dependency lock |
| GUARD-29 | `runtime_sandbox_guard.py` | 5 | PLANNED | runtime sandbox |
| GUARD-30 | `incident_boundary_guard.py` | 5 | PLANNED | incident limits |
| GUARD-31 | `license_stack_guard.py` | 5 | ACTIVE,MVP,REPORT | license stack integrity |

---

## Level-to-Guard View

### Level 0 — Fundamental Repository Perimeter

```text
GUARD-00 perimeter kernel
GUARD-01 canonical ontology boundary
GUARD-02 repository boundary
GUARD-05 repository layer boundary
GUARD-11 master index router
GUARD-19 repository path policy
GUARD-22 contract traceability
GUARD-23 guard runtime integrity
GUARD-24 anchor blob integrity
```

### Level 1 — Specialized Ontological Perimeter

```text
GUARD-06 no feedback loop
GUARD-07 Vortex non-agentic boundary
GUARD-08 QE aporia boundary
GUARD-09 Triality boundary
```

### Level 2 — Semantic / Ontological Vocabulary Perimeter

```text
GUARD-10 vector drift
GUARD-12 coherence vocabulary
GUARD-25 ontology creep
```

### Level 3 — Code Behavior Perimeter

```text
GUARD-03 code behavior audit
GUARD-17 determinism
GUARD-18 import boundary
GUARD-26 inter-guard coupling
```

### Level 4 — Bridge / Projection / Trace Perimeter

```text
GUARD-13 EK observable non-authority
GUARD-14 Φ to EK bridge
GUARD-15 projection boundary
GUARD-16 memory trace boundary
```

### Level 5 — Runtime / Evidence / Release Perimeter

```text
GUARD-04 empirical claim guard
GUARD-20 release claim guard
GUARD-21 promotion ledger guard
GUARD-27 evidence attestation guard
GUARD-28 dependency supply-chain guard
GUARD-29 runtime sandbox guard
GUARD-30 incident boundary guard
GUARD-31 license stack integrity
```

---

## MVP Perimeter

The first executable perimeter should remain smaller than the full matrix.

Recommended MVP:

```text
GUARD-00 perimeter kernel
GUARD-01 canonical ontology guard
GUARD-03 code behavior audit
GUARD-12 coherence vocabulary guard
GUARD-20 release claim guard
GUARD-31 license stack guard
```

MVP purpose:

```text
block root authority drift
block canonical ontology mutation
block code behavior mutation
block vocabulary conversion
block release/evidence overclaim
block license-stack DOI / path / boundary drift
```

Do not implement all guards before shared core stabilizes.

---

## Perimeter Manifest

File:

```text
contracts/perimeter_manifest.json
```

Status:

```text
ACTIVE MACHINE-READABLE MANIFEST
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

The manifest does not validate safety.

The manifest belongs in `/contracts/` because it is a machine-readable perimeter contract.

---

## Perimeter Runner

File:

```text
guards/run_perimeter.py
```

Status:

```text
STAGED / MECHANICAL RUNNER
```

Role:

Manifest-driven guard command runner.

The runner may:

```text
read the manifest
expand explicit variables
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
decide which findings matter semantically
```

Current alignment note:

```text
The runner must use contracts/perimeter_manifest.json as the manifest path.
If the runner default still points to guards/perimeter_manifest.json, that is a runner alignment bug.
```

Until the runner default is corrected, invoke it explicitly with:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --profile report
```

---

## Runner Usage

List guards:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --list
```

Local report profile:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --profile report
```

Local report with strict exit:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --profile report --strict-exit
```

CI profile:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --profile ci --base "$BASE_SHA" --head "$HEAD_SHA"
```

Dry run:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --profile ci --dry-run
```

Run one guard:

```bash
python3 guards/run_perimeter.py --root . --manifest contracts/perimeter_manifest.json --only GUARD-08
```

Create reports:

```bash
python3 guards/run_perimeter.py   --root .   --manifest contracts/perimeter_manifest.json   --profile ci   --base "$BASE_SHA"   --head "$HEAD_SHA"   --json-out reports/perimeter.json   --md-out reports/perimeter.md
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
python3 guards/run_perimeter.py   --manifest contracts/perimeter_manifest.json   --base "$BASE_SHA"   --head "$HEAD_SHA"
```

If not provided, the runner may attempt to use environment values.

---

## Recommended CI Shape

```yaml
- name: Run VECTAETOS perimeter
  run: |
    python3 guards/run_perimeter.py       --root .       --manifest contracts/perimeter_manifest.json       --profile ci       --base "$BASE_SHA"       --head "$HEAD_SHA"       --json-out reports/perimeter.json       --md-out reports/perimeter.md
```

The CI workflow must set usable `BASE_SHA` and `HEAD_SHA` values before invoking the runner.

---

## Shared Guard Core

Planned or existing shared modules:

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

Shared core exists to reduce duplicate guard logic.

It must not become an ontology source.

---

## Current Contract Files

Known machine-readable contract files:

```text
contracts/perimeter_manifest.json
contracts/vectaetos_code_contract.json
contracts/LICENSE_REGISTRY.json
contracts/guard13_ek_observable_rules.json
```

Contract boundary:

```text
contract ≠ ontology
contract ≠ truth
contract ≠ empirical proof
contract ≠ deployment validity
```

Contracts define repository-facing behavior and machine-readable boundaries.

Anchors define identity.

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

It should be used as the lexical reference for vocabulary guards.

---

## Forbidden Transformations

No guard, contract, runner, manifest, report, workflow, or hash may become:

```text
truth authority
ontology source
optimizer
planner
decision system
recommendation engine
runtime controller
feedback loop into Φ
auto-fix layer for ontology-facing text
auto-revert mechanism
auto-quarantine mechanism
deployment validator
empirical proof
```

---

## Safe Claim Language

Allowed:

```text
configured blocker detected
repository-state drift exposed
static scan finding
AST compliance finding
byte integrity mismatch
evidence class mismatch
license stack boundary mismatch
DOI marker missing
hash mismatch
guard infrastructure error
```

Forbidden:

```text
truth invalidated
ontology proven
VECTAETOS safe
deployment valid
hash proves meaning
CI proves safety
guard decides
license guard proves legal validity
```

---

## Conflict Order

If repository perimeter files disagree, use this order:

```text
canonical anchor
    >
MASTER_INDEX
    >
GUARD_PERIMETER_MODEL
    >
MATICA_PERIMETER
    >
contracts/perimeter_manifest.json
    >
contracts/LICENSE_REGISTRY.json
    >
GUARD_MVP_PROFILE
    >
GUARD_TABLE
    >
README
    >
implementation note
```

This README is a guide.

It is not the final authority.

---

## Final Statement

The guard perimeter protects repository boundaries.

It does not create authority.

It does not create ontology.

It does not create empirical validation.

It only makes drift visible and fail-closed.

```text
Matica mapuje zodpovednosť guardov.
Nevytvára autoritu guardov.
```
