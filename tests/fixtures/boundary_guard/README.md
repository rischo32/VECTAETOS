# tests/textures/

## Status

`tests/textures/` is a non-canonical test fixture directory for VECTAETOS.

This directory may contain visual, textual, or metadata fixtures used for testing texture-related handling, asset hygiene, provenance checks, visual export checks, and guard compatibility.

It is not an ontology layer.  
It is not a formal layer.  
It is not a projection authority.  
It does not define Φ, K(Φ), κ, QE, Vortex, NIR, runes, glyphs, audit, or any canonical VECTAETOS concept.

---

## Purpose

The purpose of this directory is to store controlled test materials for:

- texture fixture validation,
- visual asset naming tests,
- provenance metadata tests,
- guard false-positive / false-negative tests,
- non-canonical visual export tests,
- repository hygiene checks.

Files here may intentionally include valid or invalid examples for testing.

---

## Test Fixture Boundary

Content in this directory is test material only.

A file in `tests/textures/` must not be interpreted as:

- a canonical anchor,
- a formal definition,
- a public projection,
- a proof,
- a deployment artefact,
- a validated visual representation of Φ,
- a real runic or glyphic projection.

If a fixture contains forbidden wording, it must be clearly framed as a test case.

---

## Suggested Structure

    tests/textures/
    ├── README.md
    ├── valid/
    │   └── accepted texture fixtures
    ├── invalid/
    │   └── intentionally invalid texture fixtures
    ├── metadata/
    │   └── provenance and metadata test cases
    └── expected/
    └── expected outputs or snapshots

Guard Compatibility

Guards may scan this directory differently from active repository documentation.

Allowed in tests/textures/invalid/:

forbidden language used as a test fixture,
invalid metadata examples,
intentionally broken provenance,
intentionally unsafe captions.

Not allowed:

presenting invalid fixtures as active documentation,
using fixtures as canonical evidence,
claiming that test textures validate Φ, K(Φ), κ, QE, Vortex, runes, audit, LLM, or deployment safety.
Final Boundary

tests/textures/ stores test fixtures.

It may help verify that texture handling and guard behavior remain stable.

It does not define, modify, validate, or authorize VECTAETOS.
