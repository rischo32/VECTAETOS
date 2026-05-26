# VECTAETOS / Core

## Status

`/Core/` contains technical projections and implementation-adjacent code for VECTAETOS.

This directory is **not** the ontological source of truth.

It is not an authority layer.

It is not a decision layer.

It is not an optimization layer.

It is not a deployment claim.

---

## Role of `/Core/`

The role of this directory is to hold bounded, deterministic, non-agentic technical components that may express parts of the VECTAETOS architecture in code.

Typical contents may include:

- Simulation Vortex prototypes
- field-shape utilities
- deterministic trajectory generators
- structural projection helpers
- audit-adjacent helpers
- experimental implementation sketches
- legacy or transitional core candidates

All code in this directory must remain downstream of canonical ontology.

---

## Canonical Boundary

Canonical meaning is defined outside this directory.

Priority order:

```text
canonical anchors
> master index
> formal specifications
> contracts
> guards
> Core implementation notes
> informal comments
```

If a file in `/Core/` conflicts with canonical anchors, the implementation is wrong.

The ontology must not be changed to fit code.

---

## Core Invariants

All code in `/Core/` must preserve the following invariants:

```text
Phi is not an agent.
Phi is not an optimizer.
Phi is not a controller.
Phi is not a planner.
Phi is not a decision subject.

K(Phi) is not a score.
K(Phi) is not a reward.
K(Phi) is not an optimization target.

kappa is not a numeric threshold.
kappa is not a tunable parameter.
kappa is not a deployment metric.

QE is not an error.
QE is not a fallback failure.
QE is an active epistemic aporia.

The Simulation Vortex does not decide.
The Simulation Vortex does not select.
The Simulation Vortex does not optimize.
The Simulation Vortex does not repair Phi.
The Simulation Vortex does not mutate epistemic ontology.

Audit layers observe only.
Projection layers expose only.
Memory layers describe only.
LLM layers render language only.
```

---

## Allowed Behavior

Code in `/Core/` may:

- generate candidate trajectories
- expose structural projections
- compute deterministic structural observables
- create local audit artifacts
- serialize non-authoritative traces
- support testing of non-agentic behavior
- fail closed when invariants are violated
- report boundary violations
- remain silent when no coherent projection exists

---

## Forbidden Behavior

Code in `/Core/` must not:

- select the "best" trajectory
- recommend an action
- optimize field state
- maximize coherence
- minimize risk as an objective function
- convert audit observables into authority
- convert projection into interpretation
- convert memory into truth source
- use feedback loops into Phi
- treat numeric observables as K(Phi), kappa, safety, truth, validity, or deployment readiness
- present VECTAETOS as an autonomous system
- present VECTAETOS as a military, regulatory, or operational decision engine

---

## Simulation Vortex Boundary

The Simulation Vortex, if present in `/Core/`, is a candidate trajectory generator only.

It may expose possible deformations or trajectory candidates.

It must not know or enforce kappa.

It must not define K(Phi).

It must not decide which trajectory is valid.

It must not rank candidate trajectories as preferred outcomes.

It must not repair, rescue, stabilize, or mutate Phi.

Correct posture:

```text
Vortex exposes candidate trajectories.
External coherence predicates classify representability.
QE marks non-representability.
Projection exposes structure.
Human interpretation remains outside the field.
```

Incorrect posture:

```text
Vortex chooses.
Vortex optimizes.
Vortex validates.
Vortex repairs.
Vortex controls.
Vortex recommends.
```

---

## Determinism

Core code should be deterministic by default.

If randomness is used, it must be:

- explicitly seeded
- documented
- reproducible
- isolated from ontology
- non-authoritative

Undocumented randomness is a boundary risk.

---

## Python Environment

Target Python:

```text
Python 3.11+
```

Recommended local setup from repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

If imports require repository root, use explicit `PYTHONPATH`:

```bash
PYTHONPATH=. python Core/<module>.py
```

Do not rely on implicit working-directory behavior.

---

## Testing

Run tests from repository root.

Example:

```bash
PYTHONPATH=. pytest
```

Static checks, if configured:

```bash
ruff check .
mypy .
```

Core tests should verify:

- no agency language in executable behavior
- no optimization operators over Phi
- no feedback into ontology
- deterministic output for identical input
- audit observables remain audit-only
- Vortex outputs remain candidate-only
- QE is treated as aporia, not error
- kappa is not treated as a numeric threshold
- K(Phi) is not treated as a score

---

## File Classification

Every substantial file in `/Core/` should be classifiable as one of:

```text
CURRENT_CORE
EXPERIMENTAL
LEGACY
RESEARCH_NOTE
DEPRECATED
TEST_FIXTURE
```

Recommended header:

```python
"""
VECTAETOS Core File

Status: EXPERIMENTAL
Role: candidate trajectory generation
Authority: none
Agency: none
Optimization: none
Feedback into Phi: none
"""
```

Files without a clear status should not be treated as canonical.

---

## Import Boundary

`/Core/` may depend on stable contracts and deterministic utilities.

`/Core/` must not import from downstream operational layers in a way that gives those layers authority over ontology.

Forbidden direction:

```text
ASI_MOD -> controls Core
ASIMULATOR -> redefines Core ontology
Audit -> commands Core
Projection -> mutates Core
Memory -> updates Phi
```

Allowed direction:

```text
Core -> reads constants/contracts
Core -> emits candidate structures
Core -> emits audit-safe traces
Core -> remains non-authoritative
```

---

## Security Posture

`/Core/` is not a security product.

It may support research into structural visibility, auditability, and invariant preservation.

It must not claim:

- real-world safety
- deployment readiness
- military readiness
- empirical validation
- autonomous reliability
- operational admissibility

Without replicated L4 evidence, all operational claims remain suspended.

---

## Branch and Permission Discipline

Recommended repository discipline:

```text
main branch protected
direct pushes disabled
pull requests required
status checks required
guard workflows required
CODEOWNERS review required for Core changes
```

Core changes should be reviewed as architectural changes, not only code changes.

---

## Failure Mode

When an invariant is violated, Core code should fail closed.

Preferred behavior:

```text
detect -> report -> stop
```

Not preferred:

```text
detect -> patch silently -> continue
detect -> reinterpret ontology -> continue
detect -> downgrade violation to warning
```

A hard ontological violation is not a runtime inconvenience.

It is a boundary breach.

---

## Canonical Sentence

`/Core/` contains technical projections of VECTAETOS behavior, not the authority to define VECTAETOS.

Code may expose structure.

Code may not become the field.
