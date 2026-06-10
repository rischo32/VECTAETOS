# /anchors

This directory contains canonical anchor documents of the VECTAETOS repository.

## Purpose

Anchors define frozen semantic or ontological reference points.
They are not runtime code, not product documentation, and not procedural logic.

## Files

- `TRIADIC_REPOSITORY_ANCHOR.md`  
  Canonical supra-repository anchor defining the relation and separation between:
  - VECTAETOS
  - ASIMULATOR
  - ASI_MOD

- `TRIADIC_REPOSITORY_ANCHOR.sha256`  
  SHA-256 digest of the canonical anchor file.
  This hash is used for repository-integrity verification only.
  It is **not** the Epistemic Cryptography layer.

## Rules

1. Anchor documents are semantically prior to downstream repository interpretation.
2. Hash files verify textual identity, not ontological truth.
3. No downstream repository may redefine an anchor locally.
4. Changes to anchor documents require explicit review and hash regeneration.

## Boundary

Anchors describe what the architecture is.
Contracts describe how repositories may relate to it.
