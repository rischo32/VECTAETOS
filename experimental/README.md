VECTAETOS :: experimental

This directory contains unstable, exploratory, and non-canonical implementations.

Nothing in this folder is part of the validated Vectaetos core (v1.0) or projection layer (v1.1).

---

Purpose

The "experimental" layer exists to:

- test new constructs before formalization
- explore implementation strategies
- validate feasibility of future modules
- bridge theory → executable artifacts

---

Scope

Typical contents:

- prototype engines (e.g. deterministic entropy, vortex variants)
- incomplete modules (AJE, MML, INS candidates)
- alternative formulations of Φ-derived structures
- performance experiments (canonicalization, EK pipeline)

---

Guarantees

None.

Artifacts here may:

- change without notice
- be incomplete or inconsistent
- violate performance constraints
- be replaced or deleted

---

Non-Goals

- no stability guarantees
- no backward compatibility
- no production readiness
- no formal correctness guarantees

---

Relationship to Core

core (v1.0)       → immutable ontology
projection (v1.1) → immutable mapping

experimental      → pre-formal layer

Nothing here modifies or overrides the core.

---

Promotion Rule

An artifact may move from "experimental" → core only if:

1. it is deterministic
2. it is non-agentic (no optimization / no feedback loops)
3. it is reproducible
4. it is formally expressible in Φ

---

Current Direction

Focus areas:

- Epistemic Cryptography (EK v2)
- canonical Δ̂ and invariant fingerprinting
- deterministic Vortex (state-space mapping, not simulation)
- audit pipeline for external systems

---

Warning

Do not treat outputs from this directory as authoritative.

They are intermediate states in the construction of a reference system.

---

Summary

experimental = where ideas are tested
core         = where ideas are frozen
