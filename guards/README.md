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

- `VECTAETOS_BOUNDARY_GUARD.py`
- `REPO_LAYER_BOUNDARY_GUARD.py`
- `CANONICAL_ANCHOR_GUARD.py`
- `NO_FEEDBACK_LOOP_GUARD.py`
- `EMPIRICAL_CLAIM_GUARD.py`
- `LEGAL_POSITION_GUARD.py`
- `VORTEX_NON_AGENTIC_GUARD.py`

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

## Execution Rule

All guards are run from the repository root.

Example:

```bash
python guards/VECTAETOS_BOUNDARY_GUARD.py
