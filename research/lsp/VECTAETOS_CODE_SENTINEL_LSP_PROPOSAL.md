# VECTAETOS — Code Sentinel LSP Proposal

## Status

RESEARCH PROTOTYPE

## Scope

Local editor diagnostics for semantic and ontological drift in VECTAETOS-related Python code.

## Non-Authority Clause

This prototype is not a canonical guard.

It is not a truth validator.

It is not a deployment validator.

It is not an optimizer.

It does not decide whether code is valid VECTAETOS.

It only exposes local diagnostic signals for human review.

## Purpose

The VECTAETOS Code Sentinel LSP explores whether Language Server Protocol diagnostics can help detect early semantic drift during development.

The prototype analyzes Python files through AST inspection and emits editor diagnostics when code appears to introduce:

- agentic language
- decision authority
- optimization semantics
- protected ontology mutation
- dynamic execution
- role-boundary violations

## Intended Location

Prototype source:

```text
research/lsp/vectaetos_lsp.py
```

Optional future location after hardening:

```text
guards/lsp/vectaetos_lsp.py
```

Only after tests, contract schema, deterministic behavior review, and non-authority wording are complete.

## Current Prototype Capabilities

The prototype currently provides:

- local AST parsing
- forbidden fragment detection
- protected ontology name assignment checks
- dynamic execution detection
- pygls-based diagnostics
- Jedi-based completions
- optional append-only ledger helper
- SHA-256 and SHA3-512 dual fingerprinting

## Protected Concepts

The prototype treats the following as protected ontology names:

```text
PHI
Phi
K
K_PHI
KPhi
KAPPA
kappa
QE
```

These names must not be assigned inside roles such as:

```text
vortex
projection
adapter
```

unless future contract rules explicitly allow safe local shadowing.

## Forbidden Semantic Fragments

The prototype flags names containing fragments such as:

```text
decide
decision
recommend
optimize
reward
policy_update
best_trajectory
select_best
rank
argmax
argmin
```

These diagnostics are warnings unless a future contract escalates them.

## Ledger Constraint

The ledger helper is research-only.

No automatic ledger write may occur from ordinary LSP diagnostics.

A ledger commit requires explicit user/editor action.

The ledger is an audit trace, not an enforcement mechanism.

## Determinism Note

The serializer is deterministic with respect to object structure.

However, ledger events contain timestamps.

Therefore, ledger records are time-bound audit fingerprints, not deterministic replay artifacts.

## Contract Status

The prototype loads:

```text
contracts/vectaetos_code_contract.json
```

but the current embedded rule engine does not yet fully externalize behavior through this contract.

Future work should move protected names, role rules, and severity levels into the contract.

## Known Limitations

- URI handling is improved with `urllib.parse`, but role inference remains heuristic.
- pygls API compatibility must be pinned and tested.
- diagnostics must remain non-authoritative.
- ledger write operations must remain opt-in.
- lexical fragment matching may produce false positives.
- contract schema is not yet enforced.
- no CI role yet.
- no production guard role yet.

## Invariants

This LSP must never:

- define VECTAETOS truth
- decide code validity
- select trajectories
- optimize Φ
- modify Φ
- modify K(Φ)
- modify κ
- redefine QE
- write back into Vortex
- act as deployment validation
- replace human review

## Research Value

This prototype moves semantic drift detection closer to the moment of writing code.

Instead of waiting for CI, the editor can show early local warnings.

This supports human review without giving the tool authority.

## Promotion Criteria

This prototype may be promoted from research to guard only if:

- deterministic tests pass
- pygls compatibility is pinned
- contract schema is implemented
- false-positive fixtures are added
- no automatic ledger writes occur
- severity levels are documented
- non-authority language is preserved
- CI integration remains external and human-maintained

## Canonical Sentence

The VECTAETOS Code Sentinel LSP does not validate truth.

It exposes possible semantic drift for human review.
