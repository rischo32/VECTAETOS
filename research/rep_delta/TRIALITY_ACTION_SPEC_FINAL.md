# VECTAETOS — TRIALITY ACTION SPEC

## Finite Triality Action over Curvature Configurations

### Status
CANONICAL CANDIDATE — ACTION DECLARATION REQUIRED

### Lock Boundary
This document is a lock-safe specification of the required structure of a finite triality action.

It is not yet a canonical lock unless a concrete finite action `𝒯` is declared.

Canonical lock requires:

```text
1. explicit finite group or finite action 𝒯,
2. explicit generators or elements of 𝒯,
3. explicit action on C²,
4. declared orientation convention,
5. proof or declaration that the action commutes with d₁ and d₂,
6. declaration that 𝒟₀ is invariant under 𝒯,
7. explicit statement of representational-axis non-privilege.
```

If any item is missing, `A_{\mathcal T}(Δ)` is `DEPENDENCY_UNRESOLVED`, not `TRIALITY_BROKEN`.

### Layer
Meta-mathematical / Triality / Curvature-domain specification

### Scope
Σ / R / Δ / C² / 𝒯 / P_𝒯 / 𝒟₀ / 𝒟_rep / Rep(Δ)

### Authority
Descriptive only

### Agency
None

### Optimization
None

### Runtime decision authority
None

### Feedback into Φ
None

---

## 0. Purpose

This specification defines the admissible structure of a finite triality action:

```math
\mathcal T
```

over curvature configurations:

```math
\Delta \in C^2
```

for use by:

```math
A_{\mathcal T}(\Delta)
```

inside the `Rep(Δ)` formalism.

This document does not define ontology by itself.

This document does not select trajectories.

This document does not optimize curvature.

This document does not create a preferred representational axis.

This document does not repair curvature configurations.

This document does not authorize replacement of `Δ` by `P_{\mathcal T}Δ`.

It only defines the structural requirements required to evaluate triality compatibility once a concrete action `𝒯` is declared.

---

## 1. Base Curvature Space

Let:

```math
\Sigma = \{\Sigma_1,\ldots,\Sigma_8\}
```

be the invariant set of eight singularities.

Let:

```math
C^2 = C^2(K_{\Sigma};\mathbb R)
```

be the real-valued oriented triangular cochain space over the complete simplicial complex on `Σ`.

For eight singularities:

```math
\dim C^2 = \binom{8}{3}=56
```

A curvature configuration is:

```math
\Delta \in C^2
```

with components:

```math
\Delta_{ijk}
```

for oriented triples of distinct indices.

Orientation convention:

```math
\Delta_{\pi(i)\pi(j)\pi(k)}
=
\operatorname{sgn}(\pi)
\Delta_{ijk}
```

for any permutation `π` of the triple.

---

## 2. Declared Triality Action

A canonical triality action must be a finite structural action:

```math
\mathcal T \curvearrowright C^2
```

where each:

```math
\tau \in \mathcal T
```

acts linearly on `C²`.

For canonical lock, `𝒯` must be declared either as:

```text
finite group representation on C²
```

or as:

```text
finite action closed under composition with identity and inverses explicitly handled
```

If `𝒯` is only a finite list without group/action closure, then:

```text
P_𝒯 = |𝒯|⁻¹ Σ_{τ∈𝒯} τ
```

is only an averaging operator, not necessarily a projection.

Therefore, for the phrase "triality-invariant projection" to be valid, `𝒯` must be a finite group action or an explicitly idempotent finite averaging action.

This specification declares the boundary of admissible `𝒯`.

It does not itself supply the missing concrete action.

It is not a trajectory generator.

It is not a policy.

It is not an optimizer.

It is not a selector.

It is not a semantic interpreter.

---

## 3. Minimal Action Requirements

A lock-ready triality action must specify:

```text
1. the finite group or finite closed action underlying 𝒯,
2. the generators or elements of 𝒯,
3. the action of each τ ∈ 𝒯 on C²,
4. the orientation convention,
5. whether the action is left-action or right-action,
6. whether the action commutes with d₁,
7. whether the action commutes with d₂,
8. whether 𝒟₀ is invariant under 𝒯,
9. the meaning of representational-axis non-privilege.
```

If any item is missing, triality compatibility remains unresolved.

Unresolved triality is not proof of non-representability.

It is a dependency suspension condition.

---

## 4. Signed Cochain Action

For a left action on indices:

```math
\tau : \{1,\ldots,8\}\to\{1,\ldots,8\}
```

the induced left action on oriented 2-cochains should be read as pullback by inverse:

```math
(\tau\cdot\Delta)_{ijk}
=
\operatorname{sgn}(\tau^{-1}|_{ijk})
\Delta_{\tau^{-1}(i)\tau^{-1}(j)\tau^{-1}(k)}
```

where:

```math
\operatorname{sgn}(\tau^{-1}|_{ijk})
```

is the sign induced by the reordering of the oriented triple.

This convention preserves the usual left-action composition law:

```math
(\tau_1\tau_2)\cdot\Delta
=
\tau_1\cdot(\tau_2\cdot\Delta)
```

If an implementation or formalization uses:

```math
(\tau\cdot\Delta)_{ijk}
=
\operatorname{sgn}(\tau|_{ijk})
\Delta_{\tau(i)\tau(j)\tau(k)}
```

then it must explicitly declare a right-action or opposite-composition convention.

The action is structural.

It does not assign value.

It does not assign preference.

It does not assign semantic meaning.

---

## 5. Triality-Invariant Projection

Assuming `𝒯` is a finite group action or explicitly idempotent finite averaging action, define:

```math
P_{\mathcal T}
=
\frac{1}{|\mathcal T|}
\sum_{\tau\in\mathcal T}\tau
```

For any:

```math
\Delta\in C^2
```

the projection:

```math
P_{\mathcal T}\Delta
```

is the triality-symmetrized curvature configuration.

This projection is not an optimization.

This projection is not a repair mechanism.

This projection must not be used to replace `Δ` during runtime.

This projection must not be used to generate an accepted state.

It exists only to define the fixed-space condition.

---

## 6. Fixed Space

Define:

```math
\operatorname{Fix}(\mathcal T)
=
\{
\Delta\in C^2
\mid
P_{\mathcal T}\Delta=\Delta
\}
```

A curvature configuration is triality-compatible iff:

```math
\Delta\in\operatorname{Fix}(\mathcal T)
```

Equivalently:

```math
A_{\mathcal T}(\Delta)=1
\iff
P_{\mathcal T}\Delta=\Delta
```

`A_{\mathcal T}(Δ)` is a boolean structural condition.

It is not a score.

It is not a closeness measure.

It is not a distance to symmetry.

It is not an instruction to symmetrize `Δ`.

It does not provide a nearest triality-compatible curvature.

---

## 7. Compatibility with `d₁` and `d₂`

For canonical lock, the declared triality action must satisfy:

```math
d_1(\tau\cdot R)
=
\tau\cdot(d_1R)
```

whenever the action is also declared on `C^1`.

It must also satisfy:

```math
d_2(\tau\cdot\Delta)
=
\tau\cdot(d_2\Delta)
```

on `C^2`.

These are compatibility conditions.

They do not create a computation target.

They do not create a preferred action.

If these compatibility conditions are not proven or declared, the triality action remains:

```text
CANONICAL CANDIDATE — ACTION DECLARATION REQUIRED
```

and `A_{\mathcal T}(Δ)` must be treated as:

```text
DEPENDENCY_UNRESOLVED
```

---

## 8. Invariance of `𝒟₀`

For canonical lock, the primitive admissible curvature carrier-domain:

```math
\mathcal D_0
```

must be invariant under the triality action:

```math
\Delta\in\mathcal D_0
\Rightarrow
\tau\cdot\Delta\in\mathcal D_0
```

for all:

```math
\tau\in\mathcal T
```

Equivalently:

```math
\mathcal T\cdot\mathcal D_0=\mathcal D_0
```

This expresses that the primitive domain does not privilege a representational axis.

It does not say that every symmetrized point is representable.

It does not define `𝒟₀`.

It does not define `𝒟_rep`.

It does not define `Rep(Δ)`.

It only states invariance of the primitive domain under the declared action.

---

## 9. Relation to `Rep(Δ)`

Inside `REP_DELTA_FORMALISM`, triality compatibility is the component condition:

```math
A_{\mathcal T}(\Delta)=1
\iff
P_{\mathcal T}\Delta=\Delta
```

and `Rep(Δ)` includes:

```math
A_{\mathcal T}(\Delta)
```

as one of its representability requirements.

This specification defines the structural requirements for the action used by that condition.

It does not define the whole of `Rep(Δ)`.

It does not define `𝒟₀`.

It does not define `K_𝒟(Φ)`.

It does not override `ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN`.

---

## 10. Non-Privilege Meaning

Triality compatibility means:

```text
no representational axis is privileged by the curvature configuration under the declared action 𝒯
```

It does not mean:

```text
all axes are identical in semantic meaning
```

It does not mean:

```text
the system chooses the most balanced state
```

It does not mean:

```text
curvature is optimized toward symmetry
```

It does not mean:

```text
Vortex should repair imbalance
```

It means only that the curvature configuration does not collapse into a privileged representational axis under the declared triality action.

---

## 11. Failure and Suspension

If a concrete, canonical `𝒯` is declared and:

```math
P_{\mathcal T}\Delta\ne\Delta
```

then:

```math
A_{\mathcal T}(\Delta)=0
```

and `Rep(Δ)` cannot return `1`.

If the triality action itself is missing, ambiguous, incomplete, or unverified, the failure reason must be:

```text
DEPENDENCY_UNRESOLVED
```

not:

```text
TRIALITY_BROKEN
```

Dependency unresolved is a suspension marker.

It is not proof of non-representability.

It is not `QE_𝒟`.

It is not a runtime error.

---

## 12. Forbidden Transformations

The following are forbidden:

```text
Triality becomes a score.
Triality becomes a ranking function.
Triality becomes a repair mechanism.
Triality becomes a Vortex selector.
Triality becomes a policy target.
Triality becomes semantic interpretation.
P_𝒯Δ replaces Δ as runtime state.
Distance to Fix(𝒯) becomes a safety metric.
Projection to Fix(𝒯) becomes automatic correction.
Unresolved triality becomes TRIALITY_BROKEN.
Unresolved triality becomes QE_𝒟.
```

Allowed phrasing:

```text
Triality defines a structural fixed-space condition over curvature configurations once a concrete finite action 𝒯 is declared.
```

---

## 13. Implementation Projection

A technical projection may expose:

```text
apply_triality_action(delta, tau) -> delta
project_triality(delta) -> delta_projected
is_triality_compatible(delta) -> bool
```

But implementation must preserve:

```text
no score
no ranking
no optimization
no repair
no trajectory selection
no feedback into Φ
```

`project_triality(delta)` must not be used as automatic repair.

It may be used only for structural comparison or proof checking.

If `𝒯` is unresolved, implementation should return:

```text
DEPENDENCY_UNRESOLVED
```

rather than a boolean failure.

---

## 14. Required Action Declaration Template

A future lock patch may complete this document by adding:

```md
## Declared Triality Action

### Underlying finite group or closed action

...

### Generators / elements

...

### Action on indices

...

### Induced action on C¹

...

### Induced action on C²

...

### Orientation convention

left-action pullback by inverse / right-action opposite convention

### Compatibility with d₁

proof or declared lemma

### Compatibility with d₂

proof or declared lemma

### Invariance of 𝒟₀

proof, declaration, or upstream anchor reference

### Non-privilege reading

exact representational-axis interpretation
```

Until such declaration exists, this document remains:

```text
CANONICAL CANDIDATE — ACTION DECLARATION REQUIRED
```

---

## 15. Canonical Sentence

Triality action is the finite structural action over curvature configurations whose fixed space expresses non-privilege of representational axes. It defines the condition `A_{\mathcal T}(Δ)` used by `Rep(Δ)`, but it does not select, optimize, repair, interpret, or authorize any trajectory. Until the concrete finite action `𝒯` is declared, triality compatibility is dependency-unresolved, not broken.

Slovak:

Trialitná akcia je konečná štrukturálna akcia nad krivostnými konfiguráciami, ktorej fixný priestor vyjadruje neprivilegovanie reprezentačných osí. Definuje podmienku `A_{\mathcal T}(Δ)` používanú v `Rep(Δ)`, ale nevyberá, neoptimalizuje, neopravuje, neinterpretuje ani neautorizuje žiadnu trajektóriu. Kým nie je deklarovaná konkrétna konečná akcia `𝒯`, trialitná kompatibilita je dependency-unresolved, nie broken.
