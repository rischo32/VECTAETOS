# VECTAETOS Guards

## Status

    Fundamental repository perimeter layer.

## Purpose

    This directory contains guard scripts for protecting the canonical structure of VECTAETOS.

The guards do not define ontology.
They do not interpret meaning.
They do not decide.
They do not validate deployment.

They only scan, detect, report, and fail closed when repository content violates canonical boundaries.

---

## Scope

    The first guard layer protects the repository perimeter.

It checks for forbidden transformations such as:

- VECTAETOS framed as an agent
- VECTAETOS framed as a decision system
- VECTAETOS framed as a recommendation engine
- K(Φ) framed as a score, target, or reward
- κ framed as a tunable parameter or deployment threshold
- QE framed as an ordinary error
- audit framed as command or control
- projection framed as interpretation or prescription
- memory framed as ontology-modifying authority
- ASIMULATOR or ASI_MOD framed as standalone root
- safety or deployment legitimacy claimed without replicated L4 evidence

---

## Guard Classes

### Level 0 — Fundamental Repository Perimeter

These guards protect the root boundary of the repository.

Planned examples:
- GUARD-01 canonical_ontology_guard.py
- GUARD-02 vectaetos_boundary_guard.py
- GUARD-03 vectaetos_code_behavior_audit.py
- GUARD-04 empirical_claim_guard.py
- GUARD-05 repo_layer_boundary_guard.py
- GUARD-06 no_feedback_loop_guard.py
- GUARD-07 vortex_non_agentic_guard.py

## Level 1 — Specialized Ontological Guards

These guards protect specific ontological structures and phenomena.

Planned examples:

- Triality Guard
- QE Aporia Guard
- Kappa Integrity Guard
- K(Φ) Predicate Guard
- Projection Non-Prescription Guard
- Audit Non-Intervention Guard

### Level 2 — Layer-Specific Guards

These guards protect downstream layers and architectural boundaries.

Planned examples:

- 3Gate Guard
- Epistemic Cryptography Guard
- Rune / TetraGlyph Guard
- Memory Continuity Guard
- ASIMULATOR Dependency Guard
- ASI_MOD Authority Guard

### Level 3 — Runtime / CI / Release Guards

These guards protect deterministic execution, CI behavior, and release claims.

Planned examples:

- Determinism Guard
- Import Boundary Guard
- Path / Repo Structure Guard
- Release Claim Guard
- Documentation Drift Guard

---

## Active Guards

### GUARD-01 — Canonical Ontology Guard

File:

`canonical_ontology_guard.py`

Status:

`ACTIVE / STRICT / REQUIRED`

Role:

Detects modification of canonical ontology, formal anchors, protected repository boundary files, and high-risk semantic drift in changed files.

This guard is diff-based.

---

### GUARD-02 — VECTAETOS Boundary Guard

File:

`vectaetos_boundary_guard.py`

Status:

`REPORT-ONLY / CALIBRATION`

Role:

Scans active repository files for forbidden semantic formulations such as agency, optimization, decision authority, truth authority, audit command authority, projection prescription, or L4 overclaim.

This guard excludes `archive/` by default.

---

### GUARD-03 — Code Behavior Audit

File:

`vectaetos_code_behavior_audit.py`

Contract:

`contracts/vectaetos_code_contract.json`

Status:

`REPORT-ONLY / CALIBRATION`

Role:

Performs static AST audit of Python code behavior against role contracts.

It does not validate deployment.
It does not perform security audit.
It does not prove empirical safety.

## Semantic Errata

File:

`SEMANTIC_ERRATA.md`

Role:

Registers known historical semantic drift in immutable, frozen, or archived documents without rewriting those documents.

Semantic errata do not define ontology.
They do not replace anchors.
They do not authorize new drift in active files.

Registered errata may guide guard behavior only for historical or explicitly frozen contexts.
Active files should be corrected directly.
