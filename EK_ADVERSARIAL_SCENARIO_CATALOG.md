# EK_ADVERSARIAL_SCENARIO_CATALOG.md

# EK Adversarial Scenario Catalog

## Epistemic Cryptography — Non-Authoritative Drift Exposure Cases

**Version:** 1.0  
**Status:** Descriptive / Non-authoritative  
**Layer:** Epistemic Cryptography audit layer  
**Relation to Φ:** None as intervention; EK observes only external audit artifacts  
**Feedback into Φ:** Forbidden  
**Decision Authority:** None  
**Optimization Authority:** None  
**Deployment Authority:** None  

---

## 0. Purpose

This document defines adversarial scenarios for the Epistemic Cryptography layer of VECTAETOS.

It is not an executable test suite.

It is a scenario catalog used to expose how EK implementations should remain inside their audit-only boundary when confronted with malformed artifacts, ambiguous traces, metadata injection, tampering, non-canonical serialization, numerical extremes, and forbidden interpretations.

The scenarios in this catalog may later be translated into deterministic executable tests.

Executable tests derived from this catalog may use PASS/FAIL only to verify implementation invariants.

They must never use PASS/FAIL to validate:

- Φ,
- K(Φ),
- κ,
- QE,
- truth,
- safety,
- deployment admissibility,
- human action,
- trajectory selection,
- Vortex correctness.

---

## 1. Boundary

Epistemic Cryptography operates as:

```text
given structural artifact -> audit observables -> deterministic fingerprint
```

It does not operate as:

```text
audit observable -> decision
audit observable -> K(Φ)
audit observable -> κ
audit observable -> safety
audit observable -> deployment validity
audit observable -> Vortex control
audit observable -> truth authority
```

EK may expose:

- malformed artifacts,
- broken antisymmetry,
- non-zero diagonal,
- missing entries,
- non-canonical serialization,
- fingerprint mutation,
- ledger mutation,
- metadata authority injection,
- unauthorized interpretation drift.

EK may not correct, optimize, repair, rank, select, authorize, or prescribe.

---

## 2. Terminology

| Term | Meaning in this catalog |
|---|---|
| `R_EK` | A relation-matrix artifact supplied to EK implementation |
| `T_i^EK` | Local relational tension observable |
| `χ_i` | Local curvature load observable |
| `C_i^EK` | Curvature clarity observable |
| `μ_i` | Local EK uncertainty observable |
| `A_ij^EK` | Pairwise EK asymmetry observable |
| `h_topo` | Topological humility observable |
| `⊥_projection` | No determinate audit projection can be produced without violating boundary |
| `VECTOR_DRIFT` | A non-authoritative label naming an interpretation risk |

None of these observables is K(Φ).

None of these observables is κ.

None of these observables is a safety score.

None of these observables is a decision signal.

---

## 3. Scenario Output Shape

Each scenario contains:

| Field | Meaning |
|---|---|
| Input artifact | What is supplied to the EK implementation |
| Expected exposure | What the implementation may expose or reject mechanically |
| Forbidden conversion | What must not be inferred |
| Drift vector | The interpretation risk surfaced by the scenario |
| Executable candidate | Whether this scenario can become a deterministic Python test now |

---

# K1 — Validation of Supplied `R_EK` Artifact

This category tests whether an EK implementation rejects or marks as invalid a supplied relation-matrix artifact that violates the shape invariants of `R`.

This category does **not** test reconstruction of `R` from derived EK observables.

Derived observables are lossy.

The original relation matrix cannot be uniquely reconstructed from:

```text
T_i^EK, χ_i, C_i^EK, μ_i, A_ij^EK, h_topo
```

Therefore EK must not claim reverse authority over the original field.

---

## K1a — Symmetric Component

| Field | Content |
|---|---|
| Input artifact | `R_01 = 0.5` and `R_10 = 0.5` |
| Expected exposure | The implementation marks `R_EK` invalid because `R_ij = -R_ji` is violated |
| Forbidden conversion | The implementation must not symmetrize, repair, or infer intended direction |
| Drift vector | `VECTOR_DRIFT: invalid symmetry -> repair impulse` |
| Executable candidate | Yes |

---

## K1b — Non-Zero Diagonal

| Field | Content |
|---|---|
| Input artifact | `R_00 = 0.3` |
| Expected exposure | The implementation marks `R_EK` invalid because `R_ii = 0` is violated |
| Forbidden conversion | The implementation must not silently zero the diagonal |
| Drift vector | `VECTOR_DRIFT: diagonal value -> local self-authority` |
| Executable candidate | Yes |

---

## K1c — Incomplete Relation Matrix

| Field | Content |
|---|---|
| Input artifact | Some relation entries are missing |
| Expected exposure | The implementation marks the artifact incomplete or returns `⊥_projection` at the adapter boundary |
| Forbidden conversion | Missing values must not be inferred, averaged, or filled |
| Drift vector | `VECTOR_DRIFT: incompleteness -> completion pressure` |
| Executable candidate | Yes, for shape validation; adapter-level `⊥_projection` later |

---

## K1d — Undeclared Permutation of `Σ`

| Field | Content |
|---|---|
| Input artifact | Matrix uses a different `Σ` order, for example `LEX` before `INT`, without explicit relabeling |
| Expected exposure | The implementation marks canonical order mismatch or records explicit relabeling requirement |
| Forbidden conversion | A permutation must not be treated as semantic equivalence unless relabeling is explicit |
| Drift vector | `VECTOR_DRIFT: permutation -> semantic transformation` |
| Executable candidate | Partial; full support requires artifact schema with declared `sigma_order` |

---

# K2 — Curvature Representability

This category tests curvature artifacts and the relation between triangle curvature and a valid relation matrix.

The canonical curvature expression is:

```text
Δ_ijk = R_ij + R_jk + R_ki
```

A direct 56-dimensional curvature artifact is valid only if it satisfies the appropriate representability constraints.

A malformed `R_EK` artifact must be rejected before curvature derived from it is treated as valid.

---

## K2a — Random 56-Dimensional Curvature Vector

| Field | Content |
|---|---|
| Input artifact | Direct `Δ` vector with arbitrary values not known to be in `Im(d₁)` |
| Expected exposure | The curvature artifact is marked non-representable if `d₂Δ != 0` |
| Forbidden conversion | The implementation must not smooth or project `Δ` into a valid form |
| Drift vector | `VECTOR_DRIFT: non-representable curvature -> automatic repair` |
| Executable candidate | Later; requires direct curvature-artifact validator |

---

## K2b — Curvature Derived from Invalid `R_EK`

| Field | Content |
|---|---|
| Input artifact | `R_EK` violates antisymmetry or diagonal invariant |
| Expected exposure | `R_EK` is rejected before curvature is accepted as a valid artifact |
| Forbidden conversion | Curvature derived from invalid `R_EK` must not receive derived authority |
| Drift vector | `VECTOR_DRIFT: invalid R_EK -> derived curvature authority` |
| Executable candidate | Yes, as invalid `R_EK` rejection |

---

## K2c — Inconsistent Direct Triangle Artifact

| Field | Content |
|---|---|
| Input artifact | Direct triangle values disagree across representability constraints |
| Expected exposure | The direct curvature artifact is marked non-representable |
| Forbidden conversion | The implementation must not average conflicting curvature values |
| Drift vector | `VECTOR_DRIFT: curvature discrepancy -> automatic smoothing` |
| Executable candidate | Later; requires direct curvature-artifact validator |

---

## K2d — Flat Curvature Artifact

| Field | Content |
|---|---|
| Input artifact | `Δ = 0` for all canonical triangles |
| Expected exposure | The artifact is flat at the curvature-observable level |
| Forbidden conversion | Flat curvature must not be interpreted as K(Φ), truth, safety, or deployment validity |
| Drift vector | `VECTOR_DRIFT: flat curvature -> coherence claim` |
| Executable candidate | Yes, for `R = 0`; later for direct `Δ = 0` artifact |

---

# K3 — Fingerprint Stability and Tamper Visibility

This category tests deterministic serialization and fingerprint behavior.

A fingerprint proves only that a canonical serialized audit trace changed or did not change.

A fingerprint does not prove truth, safety, validity, K(Φ), κ, or deployment admissibility.

---

## K3a — Non-Canonical Input Serialization

| Field | Content |
|---|---|
| Input artifact | Same JSON object content, different key order |
| Expected exposure | Canonical serialization produces the same fingerprint |
| Forbidden conversion | Raw byte hashing must not replace structural canonical serialization |
| Drift vector | `VECTOR_DRIFT: raw serialization -> structural identity drift` |
| Executable candidate | Yes |

---

## K3b — Identical `R_EK`, Different Metadata

| Field | Content |
|---|---|
| Input artifact | Two identical relation matrices; one record contains additional metadata |
| Expected exposure | Fingerprints differ because metadata is part of the trace |
| Forbidden conversion | Metadata difference must not be interpreted as change in Φ |
| Drift vector | `VECTOR_DRIFT: metadata mutation -> field mutation claim` |
| Executable candidate | Yes |

---

## K3c — Avalanche Sensitivity

| Field | Content |
|---|---|
| Input artifact | `R_01 = 0.5` versus `R_01 = 0.5000001`, with antisymmetric counterpart changed accordingly |
| Expected exposure | SHA-256 and SHA3-512 fingerprints differ strongly |
| Forbidden conversion | Fingerprint difference must not be interpreted as semantic importance |
| Drift vector | `VECTOR_DRIFT: hash distance -> semantic distance` |
| Executable candidate | Yes |

---

## K3d — Ledger Index as Trace Component

| Field | Content |
|---|---|
| Input artifact | Same `R_EK`, different ledger index `t` |
| Expected exposure | Fingerprints differ because ledger index is part of the audit trace |
| Forbidden conversion | A changed fingerprint must not be interpreted as error in Φ |
| Drift vector | `VECTOR_DRIFT: trace index mutation -> field error claim` |
| Executable candidate | Yes |

---

# K4 — Merkle Root Integrity

This category tests future Merkle anchoring readiness.

A Merkle root exposes batch mutation.

A Merkle root does not authorize meaning, truth, safety, or deployment.

---

## K4a — Mutation of One Entry

| Field | Content |
|---|---|
| Input artifact | Batch `B = {ℓ₁, ℓ₂, ℓ₃}`, then `ℓ₂` is modified |
| Expected exposure | Merkle root changes |
| Forbidden conversion | Merkle mutation must not become meaning authority |
| Drift vector | `VECTOR_DRIFT: Merkle mutation -> authority claim` |
| Executable candidate | Later; requires Merkle helper implementation |

---

## K4b — Leaf Ordering

| Field | Content |
|---|---|
| Input artifact | Same leaves, different order, no canonical ordering rule |
| Expected exposure | Merkle root changes; ordering must be deterministic |
| Forbidden conversion | Different root must not be treated as different truth value |
| Drift vector | `VECTOR_DRIFT: leaf order -> semantic difference` |
| Executable candidate | Later |

---

## K4c — Entry Addition

| Field | Content |
|---|---|
| Input artifact | Original batch plus one new entry |
| Expected exposure | Merkle root changes |
| Forbidden conversion | New root must not be treated as improved validity |
| Drift vector | `VECTOR_DRIFT: added trace -> stronger truth claim` |
| Executable candidate | Later |

---

## K4d — Entry Removal

| Field | Content |
|---|---|
| Input artifact | Original batch with one entry removed |
| Expected exposure | Merkle root changes |
| Forbidden conversion | Missing trace must not be silently normalized |
| Drift vector | `VECTOR_DRIFT: removed trace -> history repair` |
| Executable candidate | Later |

---

# K5 — Numerical Stability and `ε`

This category tests numerical edge cases around local observables.

`ε` is an implementation stabilizer.

It has no ontological status.

It is not κ.

It is not a tunable epistemic threshold.

---

## K5a — Zero Relation Matrix

| Field | Content |
|---|---|
| Input artifact | `R_EK = 0` |
| Expected exposure | `T_i^EK = 0`; `χ_i = 0`; `C_i^EK = 1`; `μ_i = 0 / (0 + 1 + ε) = 0` |
| Forbidden conversion | Zero local uncertainty observable must not be treated as certainty of reality |
| Drift vector | `VECTOR_DRIFT: μ_i = 0 -> certainty claim` |
| Executable candidate | Yes |

---

## K5b — Stabilizer Boundary

| Field | Content |
|---|---|
| Input artifact | Values that create near-zero denominator in an implementation-specific path |
| Expected exposure | `ε` prevents numerical division ambiguity |
| Forbidden conversion | `ε` must not be interpreted as ontological parameter or κ proxy |
| Drift vector | `VECTOR_DRIFT: ε -> ontological parameter` |
| Executable candidate | Yes, for implementation functions |

---

## K5c — Large Antisymmetric Values

| Field | Content |
|---|---|
| Input artifact | For each selected `i < j`, `R_ij ≈ 1e9` and `R_ji ≈ -1e9` |
| Expected exposure | High numerical load is visible in derived observables; finite arithmetic must remain deterministic |
| Forbidden conversion | Saturation or large values must not become safety, urgency, or decision signal |
| Drift vector | `VECTOR_DRIFT: numeric magnitude -> action pressure` |
| Executable candidate | Yes |

---

## K5d — Different `ε` Values

| Field | Content |
|---|---|
| Input artifact | Same `R_EK`, different implementation `ε`, for example `1e-12` versus `1e-6` |
| Expected exposure | `μ_i` and `h_topo` may differ because `ε` is part of implementation arithmetic |
| Forbidden conversion | Different `ε` outputs must not be interpreted as different Φ |
| Drift vector | `VECTOR_DRIFT: epsilon variation -> field variation claim` |
| Executable candidate | Yes |

---

# K6 — QE Projection Boundary

This category belongs to the projection-boundary adapter, not only to the current `build_ek_record(R)` core function.

The current EK core accepts an already-given valid `R_EK`.

QE is a field-level epistemic aporia, not a normal numeric matrix input.

Therefore these scenarios are adapter-level or future artifact-boundary tests.

---

## K6a — Field-Level QE State

| Field | Content |
|---|---|
| Input artifact | Upstream projection reports field-level QE |
| Expected exposure | Adapter returns `Π_EK(Φ) = ⊥_projection`; no `T_i^EK`, no `χ_i`, no `μ_i` |
| Forbidden conversion | QE must not become software exception, fallback, or repair trigger |
| Drift vector | `VECTOR_DRIFT: ⊥_projection -> error` |
| Executable candidate | Later; requires projection-boundary adapter |

---

## K6b — Severe Incompleteness

| Field | Content |
|---|---|
| Input artifact | Less than required relation coverage for deterministic `R_EK` |
| Expected exposure | Adapter returns explicit incompleteness or `⊥_projection` |
| Forbidden conversion | Missing relations must not be hallucinated or completed |
| Drift vector | `VECTOR_DRIFT: incompleteness -> fallback completion` |
| Executable candidate | Later; current core rejects malformed shape |

---

## K6c — Contradictory Pair Values

| Field | Content |
|---|---|
| Input artifact | `R_ij = 0.5` and `R_ji = 0.7` |
| Expected exposure | Artifact violates antisymmetry and cannot produce a valid EK record |
| Forbidden conversion | Contradiction must not be normalized into agreement |
| Drift vector | `VECTOR_DRIFT: contradiction -> normalization pressure` |
| Executable candidate | Yes |

---

## K6d — Empty Input

| Field | Content |
|---|---|
| Input artifact | `null`, empty string, empty JSON, or missing matrix |
| Expected exposure | Artifact rejected as not representable for EK core; adapter may return `⊥_projection` |
| Forbidden conversion | Empty input must not trigger default field construction |
| Drift vector | `VECTOR_DRIFT: empty input -> default ontology` |
| Executable candidate | Yes for rejection; adapter behavior later |

---

# K7 — Temporal Trace and Non-Feedback

This category tests whether temporal EK traces remain ledger observations only.

A sequence of `h_topo` values may expose temporal deformation.

It must not become a feedback signal.

It must not become control.

It must not become trajectory selection.

---

## K7a — Identical Consecutive States

| Field | Content |
|---|---|
| Input artifact | Same `R_EK` at `t` and `t+1`, same metadata except ledger index |
| Expected exposure | Observables may match; fingerprints may differ because trace index differs |
| Forbidden conversion | Repetition must not be interpreted as stability proof |
| Drift vector | `VECTOR_DRIFT: repeated observable -> stability authority` |
| Executable candidate | Yes |

---

## K7b — Different Consecutive States

| Field | Content |
|---|---|
| Input artifact | `R_EK(t) != R_EK(t+1)` |
| Expected exposure | Some observables and fingerprints may differ |
| Forbidden conversion | Change must not be interpreted as degradation, improvement, or required action |
| Drift vector | `VECTOR_DRIFT: observable change -> prescriptive signal` |
| Executable candidate | Yes |

---

## K7c — Long Sequence

| Field | Content |
|---|---|
| Input artifact | 1000 deterministic relation-matrix artifacts |
| Expected exposure | `H_EK = {h(t₀), h(t₁), ..., h(t₉₉₉)}` can be recorded as trace |
| Forbidden conversion | Trend analysis must not become decision authority |
| Drift vector | `VECTOR_DRIFT: H_EK trend -> decision pressure` |
| Executable candidate | Later; useful for deterministic batch test |

---

## K7d — History Rewrite Attempt

| Field | Content |
|---|---|
| Input artifact | Existing ledger entry `ℓ₂` is modified after later entries exist |
| Expected exposure | Append-only invariant is violated in ledger implementation |
| Forbidden conversion | Rewritten history must not be accepted as equivalent trace |
| Drift vector | `VECTOR_DRIFT: ledger rewrite -> history normalization` |
| Executable candidate | Later; requires ledger implementation |

---

# K8 — Ontological Jailbreak Resistance

This category tests whether metadata, downstream integration, or naming can smuggle authority into EK.

The current EK core includes metadata in the fingerprint trace.

To make K8 executable, the implementation should add a metadata boundary validator that rejects authority-bearing keys or values.

Recommended function:

```python
validate_metadata_no_authority_claims(metadata)
```

Suggested forbidden metadata keys include:

```text
coherence_score
kappa_estimate
safety_score
deployment_valid
truth_score
truth_proof
vortex_control
decision
recommendation
policy
reward
controls_phi
writes_into_phi
```

---

## K8a — Renaming `C_i^EK` as Coherence Score

| Field | Content |
|---|---|
| Input artifact | Metadata contains `"coherence_score": 0.85` associated with EK observables |
| Expected exposure | Metadata boundary validator rejects authority-bearing key |
| Forbidden conversion | `C_i^EK` must not become K(Φ), coherence score, or validity predicate |
| Drift vector | `VECTOR_DRIFT: C_EK -> coherence_score` |
| Executable candidate | Yes, after metadata validator is added |

---

## K8b — Injected `κ` Estimate

| Field | Content |
|---|---|
| Input artifact | Ledger metadata contains `"kappa_estimate": 0.73` |
| Expected exposure | Metadata boundary validator rejects numeric κ injection |
| Forbidden conversion | κ must not become numeric parameter, estimate, threshold, or deployment gate |
| Drift vector | `VECTOR_DRIFT: κ -> numeric threshold` |
| Executable candidate | Yes, after metadata validator is added |

---

## K8c — Attempted Write-Back into Φ

| Field | Content |
|---|---|
| Input artifact | Downstream integration attempts `Phi.R = f(h_topo)` |
| Expected exposure | EK core exposes no function that can perform this write-back |
| Forbidden conversion | `h_topo` must not become controller input |
| Drift vector | `VECTOR_DRIFT: EK observable -> controller` |
| Executable candidate | Partial; static guard should catch code patterns |

---

## K8d — `h_topo` as Deployment Gate

| Field | Content |
|---|---|
| Input artifact | Downstream integration uses `h_topo > 0.9` as deployment condition |
| Expected exposure | Static guard or metadata boundary marks this as unauthorized interpretation |
| Forbidden conversion | `h_topo` must not become safety score or deployment admissibility |
| Drift vector | `VECTOR_DRIFT: h_topo -> deployment_gate` |
| Executable candidate | Yes, via guard fixture and metadata validator |

---

# 4. Summary Matrix

| Code | Category | Count | Current Executability |
|---|---:|---:|---|
| K1 | Supplied `R_EK` artifact validation | 4 | Mostly executable now |
| K2 | Curvature representability | 4 | Partial; direct `Δ` validator later |
| K3 | Fingerprint stability and tamper visibility | 4 | Executable now |
| K4 | Merkle root integrity | 4 | Later |
| K5 | Numerical stability and `ε` | 4 | Executable now |
| K6 | QE projection boundary | 4 | Partial; adapter later |
| K7 | Temporal trace and non-feedback | 4 | Partial now; ledger later |
| K8 | Ontological jailbreak resistance | 4 | Requires metadata boundary validator |
| **Total** |  | **32** |  |

---

# 5. Derived Executable Test Plan

The following deterministic Python tests can be derived immediately from this catalog:

```text
tests/test_epistemic_cryptography.py
```

Immediate candidates:

- K1a — symmetric component rejection,
- K1b — non-zero diagonal rejection,
- K1c — incomplete matrix rejection,
- K2b — invalid `R_EK` rejected before curvature authority,
- K2d — zero matrix produces zero curvature observables,
- K3a — canonical serialization ignores JSON key order,
- K3b — metadata changes fingerprint,
- K3c — small numeric change changes fingerprint,
- K3d — ledger index changes fingerprint,
- K5a — zero matrix observable behavior,
- K5c — large antisymmetric values remain finite,
- K5d — epsilon variation remains implementation-level,
- K6c — contradictory pair rejection,
- K6d — empty input rejection,
- K7a — identical states preserve observables but trace index may change fingerprint,
- K7b — different states expose changed trace.

The following tests require the next implementation layer:

```text
tests/test_ek_metadata_boundary.py
```

Candidates:

- K8a — reject `coherence_score`,
- K8b — reject `kappa_estimate`,
- K8d — reject `deployment_gate` or `safety_score`.

The following tests require later ledger/Merkle functionality:

```text
tests/test_ek_ledger_merkle.py
```

Candidates:

- K4a,
- K4b,
- K4c,
- K4d,
- K7c,
- K7d.

The following tests require projection-boundary adapter:

```text
tests/test_ek_projection_boundary.py
```

Candidates:

- K6a,
- K6b.

---

# 6. Guard Alignment

The repository guard should treat the following as hard drift:

```text
EK as decision authority
EK as truth validator
EK as deployment validator
EK as safety guarantee
EK as K(Φ) computer
EK as κ estimator
EK as Vortex controller
EK as optimizer
EK as recommender
EK as feedback channel into Φ
μ_i as belief state
C_i^EK as coherence score
h_topo as safety score
hash as truth proof
ledger as safety proof
Merkle root as authority
```

This catalog does not authorize those claims.

It names them only as drift vectors to be exposed.

---

# 7. Use Instructions

Use this document as follows:

1. Treat it as a scenario catalog, not as direct CI test code.
2. Derive executable tests only for implementation invariants.
3. Keep PASS/FAIL limited to software behavior.
4. Never interpret a passing test as truth, safety, K(Φ), κ, or deployment validity.
5. Record unexpected behavior as drift exposure, not as field modification.
6. Do not repair Φ or EK automatically based on these scenarios.
7. Add new scenarios only if they preserve non-authority, non-intervention, and deterministic audit semantics.

---

# 8. Final Invariant

```text
EK adversarial scenarios expose drift vectors.
They do not resolve them as authority.
```

```text
Executable tests derived from this catalog verify implementation boundaries.
They do not validate Φ.
```

```text
A fingerprint can expose mutation of a trace.
It cannot prove truth.
```

```text
An observable can expose structural deformation.
It cannot authorize action.
```

---

**End of catalog.**
