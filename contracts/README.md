# /contracts

This directory contains repository-facing contracts exported by VECTAETOS.

## Purpose

Contracts define readable and machine-readable boundary conditions for downstream repositories.

They do **not** replace ontology.
They do **not** redefine anchors.
They do **not** create authority.

## Files

- `LAYER_BOUNDARIES.md`  
  Human-readable definition of repository layer boundaries.

- `vectaetos_contract.json`  
  Machine-readable export of repository boundaries, allowed flows, forbidden reverse flows,
  and shared invariants.

## Rules

1. Contracts are downstream-facing.
2. Contracts must remain compatible with canonical anchors.
3. If an anchor changes, the contract must be reviewed.
4. Contracts may be versioned, but may not contradict canonical anchors.

## Boundary

Anchors define identity.
Contracts define interface and boundary.
