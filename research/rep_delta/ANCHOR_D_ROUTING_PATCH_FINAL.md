# PATCH — ANCHOR_D ROUTING FOR REP(Δ)

## Target

```text
anchors/ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md
```

## Status

FINAL PATCH — APPLY BEFORE CANONICAL LOCK OF `REP_DELTA_FORMALISM`

## Purpose

Add a routing clarification so `REP_DELTA_FORMALISM_FINAL_ROUTED.md` can introduce `𝒟₀` and `𝒟_rep` without redefining `ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN`.

This patch protects the distinction between:

```text
primitive admissible curvature carrier-domain
derived representable curvature domain induced by Rep(Δ)
```

It prevents circularity between `Rep(Δ)` and `𝒟`.

---

## Insert Location

Recommended location:

```text
After section 0. Purpose
```

or immediately before the current section:

```text
## 9. Ontological Representability Predicate
```

---

## Patch Text

```md
## Routing Note — Primitive and Derived Curvature Domains

`𝒟` in this anchor names the admissible curvature domain of the VECTAETOS epistemic field.

For the purpose of the separate `REP_DELTA_FORMALISM` document, this domain is read through two non-conflicting layers:

```text
𝒟₀      primitive admissible curvature carrier-domain
𝒟_rep   derived representable curvature domain induced by Rep(Δ)
```

`𝒟₀` is the primitive-domain reading of the admissible curvature domain defined here.

`𝒟_rep` is the derived subset of curvature configurations for which:

```math
\mathrm{Rep}(\Delta)=1
```

Thus:

```math
\mathcal D_{\mathrm{rep}}
\subseteq
\mathrm{Int}(\mathcal D_0)
\subseteq
\mathcal D_0
```

This routing does not redefine `𝒟`.

It only separates the primitive carrier-domain from the derived representability domain in order to avoid circularity.

`ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN` remains the upstream domain anchor.

`REP_DELTA_FORMALISM` does not define `ANCHOR_D`.

`REP_DELTA_FORMALISM` only introduces a non-circular reading of primitive and derived domain layers.

`κ` remains:

```math
\kappa = \partial\mathcal D_0
```

and must not be interpreted as a numeric threshold, tunable parameter, score, optimization objective, safety metric, or deployment metric.
```

---

## Minimal Alternative

If only one paragraph is permitted:

```md
`𝒟₀` is the primitive-domain reading of the admissible curvature domain defined by `ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN`. `REP_DELTA_FORMALISM` does not redefine `ANCHOR_D`; it separates the primitive carrier-domain `𝒟₀` from the derived representable domain `𝒟_rep` only to avoid circularity. `ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN` remains upstream and must not be treated as derived from `Rep(Δ)`. `κ` remains the non-numeric boundary `∂𝒟₀`.
```

---

## Guard Notes

Future guards should reject:

```text
ANCHOR_D as derived from Rep(Δ)
𝒟₀ as score
𝒟₀ as threshold
𝒟_rep as primitive domain
κ as numeric threshold
κ as deployment metric
Rep(Δ) as defining the upstream admissible domain
```

Allowed:

```text
ANCHOR_D defines the upstream admissible curvature domain.
𝒟₀ is the primitive-domain reading used to avoid circularity.
𝒟_rep is the derived representable subset induced by Rep(Δ).
κ is the non-numeric boundary ∂𝒟₀.
```
