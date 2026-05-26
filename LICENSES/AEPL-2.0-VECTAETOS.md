# AXIOMATIC EPISTEMIC PUBLIC LICENSE
## AEPL-2.0-VECTAETOS

**Status:** Draft for project and legal review  
**Version:** 2.0-draft  
**License type:** Custom software / tooling license with epistemic boundary conditions  
**Applies to:** code, guards, scripts, adapters, tools, tests, contracts, and repository automation  
**Legal note:** Not legal advice.

## 1. Purpose

This license governs the use, copying, modification, redistribution, and embedding of VECTAETOS™ software, tooling, guards, adapters, scripts, contracts, and implementation artefacts.

Its purpose is to permit research and implementation while preventing the software layer from being misrepresented as an ontology, decision authority, optimizer, deployment validator, or truth system.

## 2. Covered Software

Unless a file declares otherwise, this license applies to:

```text
source code
guard scripts
CLI audit tools
LSP diagnostics
contracts
test fixtures
reporting utilities
adapter code
parser code
projection tooling
repository automation
CI helper scripts
```

Canonical ontology and marks are governed separately by VCL-2.0 and VTP-1.0.

## 3. Permissions

Subject to the conditions below, you may use, copy, modify, redistribute, and run the covered software for research, study, experimentation, implementation, local CI, and compatible tooling.

## 4. Required Conditions

Redistribution or derivative software must:

1. retain this license or a clear reference to it;
2. preserve attribution;
3. state significant modifications;
4. avoid claiming official or canonical status unless authorized;
5. preserve non-authoritative output language;
6. preserve the distinction between guard, audit, report, ontology, and truth;
7. avoid auto-fix or semantic rewrite in ontology-facing spans unless explicitly allowed by a separate review protocol;
8. preserve safe PASS / FAIL wording;
9. preserve read-only behavior where the role is declared read-only;
10. avoid feedback into Φ or canonical anchors.

## 5. Behavioral Restrictions

Covered software must not be used or modified to:

1. make VECTAETOS™ act as an autonomous agent;
2. make VECTAETOS™ issue decisions;
3. make VECTAETOS™ optimize, rank, recommend, or select preferred states;
4. create reward-driven loops that collapse non-agentic structure;
5. mutate Φ, Σ, R, K(Φ), κ, QE, canonical anchors, or protected boundary documents;
6. turn audit findings into truth verdicts;
7. turn CI success into empirical validation;
8. turn guard output into deployment authorization;
9. suppress uncertainty where uncertainty is structurally required;
10. force output where QE, aporia, or silence is valid;
11. use structural observables as safety scores, truth scores, or deployment gates.

## 6. Guard and Audit Boundary

Guards may scan, detect, expose, report, refuse repository-state runs, emit findings, and emit incident bundles.

Guards must not define ontology, prove truth, authorize deployment, rewrite canonical meaning, auto-revert commits, auto-delete files, auto-quarantine canonical files, or lock maintainers out.

A guard finding means:

```text
A configured boundary appears to be violated.
```

It does not mean:

```text
Truth failed.
Ontology failed.
The system is unsafe.
Deployment is invalid.
```

## 7. Integrity and Cryptographic Boundary

Covered software may implement hash checks, manifest verification, signature verification, runtime sealing, EK integrity observables, and dependency locks.

These mechanisms must not be represented as proof of semantic truth, ontology validity, safety, correctness, or deployment readiness.

```text
hash verifies bytes
signature verifies attestation
manifest records expected identity
EK exposes structural drift
CI refuses repository state
```

## 8. Network, Subprocess, and Mutation

Unless explicitly declared by role and contract, covered software should remain deterministic and read-only.

The following behaviors require explicit role permission:

```text
network access
subprocess execution
filesystem mutation
dynamic execution
unseeded randomness
dependency installation during guard run
```

## 9. Derivative Naming

Modified software may not be named in a way that implies it is the official VECTAETOS™ implementation unless written permission is granted.

Acceptable:

```text
independent tool inspired by VECTAETOS™
unofficial guard compatible with selected VECTAETOS™ concepts
research prototype using VECTAETOS™ terminology
```

Not acceptable without permission:

```text
official VECTAETOS guard
VECTAETOS certified validator
VECTAETOS deployment checker
VECTAETOS safety score
VECTAETOS decision engine
```

## 10. Termination

Any violation of Sections 4, 5, 6, 7, 8, or 9 terminates the rights granted under this license until the violation is corrected.

## 11. No Warranty

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

No author, contributor, maintainer, or distributor shall be liable for any claim, damages, or other liability arising from use, misuse, modification, execution, interpretation, redistribution, or integration.

## 12. Final Clause

AEPL-2.0-VECTAETOS permits software experimentation.

It does not permit turning epistemic tools into hidden authority.

© 2026 Richard Fonfára / VECTAETOS Project.
