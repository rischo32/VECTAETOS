#  CI/CD and Governance Infrastructure
 
## Overview
 
The VECTAETOS CI/CD infrastructure enforces **ontological constraints**,
**non-agentic boundaries**, and **structural immutability**. It ensures
the system remains a descriptive relational structure rather than evolving
into an optimizing agent.
 
Three primary layers:
1. **Ontology Guard** -- integrity enforcement
2. **Canonical Anchors** -- immutability verification
3. **Epistemic Observatory** -- visibility and drift monitoring
 
Reference: [UNIFIED_ARCHITECTURE.md Section 4](/UNIFIED_ARCHITECTURE.md) (CI Guardrails diagram)
 
## Complete Workflow List
 
| Workflow | File | Purpose |
|----------|------|---------|
| Ontology Guard | `ontology_guard.yml` | Hash, language, and governance verification of core ontology |
| Canonical Guard | `canonical_guard.yml` | Protects formal definitions from unauthorized modification |
| Canonical Anchor | `canonical-anchor.yml` | SHA-256 verification of `CANONICAL_ANCHOR.md` |
| Anchor Hash | `anchor-hash.yml` | Secondary SHA-256 verification path for canonical anchor |
| **Root Canonical Anchor** | `root-canonical-anchor.yml` | **SHA-256 verification of `ROOT_CANONICAL_ANCHOR.md`** |
| Phi Integrity | `phi_integrity.yml` | Integrity check of the Phi field state |
| Phi State | `phi_state.yml` | Guarded state-sync mechanism (currently no-op placeholder) |
| Phi State PR | `phi_state_pr.yml` | PR-triggered Phi state verification |
| Determinism | `determinism.yml` | Phi determinism verification |
| Vortex Determinism | `vortex_determinism.yml` | Vortex simulation determinism check |
| Repo Boundaries | `repo-boundaries.yml` | Detects forbidden downstream imports |
| Observatory | `observatory.yml` | Hourly drift monitoring and visual projection |
| Release | `release.yml` | Release + EK Notarization pipeline |
| Static | `static.yml` | GitHub Pages deployment |
| Summary | `summary.yml` | Summary generation |
 
##  Ontology Guard (`ontology_guard.yml`)
 
Primary gatekeeper for the repository. Triggers on modifications to core
ontology files in `/formal`, `/Core`, or `/governance`.
 
Executes a triadic audit sequence:
1. **Hash Guard:** Verifies structural fingerprint via `check_ontology_hash.py`
2. **Language Guard:** Enforces prohibited agentic terminology via `check_ontology_language.py`
3. **Governance Guard:** Validates non-intervention regime via `check_governance_rules.py`
 
##  Canonical Anchor Workflows
 
### canonical-anchor.yml & anchor-hash.yml
 
Two redundant workflows verify SHA-256 hash of `anchors/CANONICAL_ANCHOR.md`:
1. Manual checkout of specific commit/PR ref
2. Recompute SHA-256 hash via `hash_anchor.py`
3. Compare against versioned `anchors/CANONICAL_ANCHOR.sha256`
 
### root-canonical-anchor.yml (NEW)
 
Verifies SHA-256 hash of `ROOT_CANONICAL_ANCHOR.md` on push/PR.
 
Triggers on changes to:
- `anchors/ROOT_CANONICAL_ANCHOR.md`
- `anchors/ROOT_CANONICAL_ANCHOR.sha256`
- `.github/workflows/root-canonical-anchor.yml`
 
Verification steps:
1. Manual checkout (shallow fetch)
2. Verify file existence (`ROOT_CANONICAL_ANCHOR.md` and `.sha256`)
3. Run `sha256sum -c anchors/ROOT_CANONICAL_ANCHOR.sha256`
 
### canonical_guard.yml
 
Protects formal definitions from unauthorized modification.
Monitors patterns: `FORMAL_`, `CANONICAL_ANCHORS.md`, `MECHANIZATION_OF_`,
`ZMYSEL.md`, `epistemic_space.md`.
 
##  Repo Boundary Enforcement (`repo-boundaries.yml`)
 
Executes `verify_repo_boundaries.py` to detect "reverse imports."
 
Forbidden import patterns:
- `asimulator` (Procedural possibilities repository)
- `asi_mod` or `asi-mod` (Dialogue/Interaction repository)
 
Recursively scans all `.py` files while excluding environment/cache directories.
 
##  Observatory Pipeline (`observatory.yml`)
 
See [Section 8: Epistemic Observatory](08_observatory.md) for detailed coverage.
 
Hourly cron schedule:
1. Vortex projection via `vortex_runner.py`
2. Visual generation via `generate_visuals.py`
3. Observatory scan via `epistemic_observatory.py`
4. Metric aggregation via `observatory_metrics.py`
5. Automated PR with updated snapshots
 
##  Governance Layer
 
The `/governance` directory contains:
- `NON_AGENTIC_POLICY.md` -- core non-agentic policy
- `ONTOLOGY_RULES.md` -- ontology modification rules
- `LANGUAGE_CONSTRAINTS.md` -- prohibited terminology
 
## Contracts
 
See [Section 9: Contracts](09_contracts.md) for the `/contracts` directory.
 
Structural constraints are also enforced through:
- `importlinter.ini` -- "Vectaetos One-Way Architecture" contract ensuring
  dependencies flow downward through triadic layers
- `ASSEMBLY_MANIFEST.json` -- assembly manifest defining valid system boot requirements
