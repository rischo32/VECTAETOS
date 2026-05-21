# VECTAETOS Code Sentinel LSP

Research-only local editor diagnostic prototype.

## Purpose

This prototype explores whether a Python Language Server Protocol tool can expose early semantic drift signals while editing VECTAETOS-related Python code.

It analyzes Python source through AST inspection and emits advisory diagnostics for patterns such as:

- agentic language,
- decision authority,
- optimization semantics,
- protected ontology-name assignment,
- dynamic execution,
- role-boundary violations.

## Non-Authority Clause

This tool is not a canonical guard.

It is not a truth validator.

It is not a deployment validator.

It is not an optimizer.

It does not decide whether code is valid VECTAETOS.

It only exposes possible local diagnostic signals for human review.

## Current Status

Research prototype only.

Do not use this as a CI blocker, production validator, or compatibility authority.

## Files

- `vectaetos_lsp.py` — current prototype implementation
- `VECTAETOS_CODE_SENTINEL_LSP_PROPOSAL.md` — conceptual proposal
- `STATUS.md` — current repository status
- `requirements.txt` — prototype dependencies

## Ledger Constraint

The ledger helper is explicit-only.

No automatic ledger write may occur from ordinary diagnostics.

Ledger records are audit traces, not enforcement artifacts.

## Canonical Sentence

The VECTAETOS Code Sentinel LSP does not validate truth.

It exposes possible semantic drift for human review.
