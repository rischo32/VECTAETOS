# VECTAETOS Contracts

## Status

Repository-level behavioral contracts for VECTAETOS production code.

## Purpose

Contracts define readable and machine-readable boundary conditions for downstream repositories.

They do **not** replace ontology.
They do **not** redefine anchors.
They do **not** create authority.

This directory defines machine-readable contracts used by guard scripts.

Contracts do not define ontology.  
Contracts do not validate truth.  
Contracts do not validate deployment.  
Contracts only describe allowed and forbidden behavior for repository code roles.

---

## Current Contract

```text
contracts/vectaetos_code_contract.json
## Rules

1. Contracts are downstream-facing.
2. Contracts must remain compatible with canonical anchors.
3. If an anchor changes, the contract must be reviewed.
4. Contracts may be versioned, but may not contradict canonical anchors.

## Boundary

Anchors define identity.
Contracts define interface and boundary.
