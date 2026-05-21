# Theorem Draft — Gauge Invariance of Epistemic Curvature

Status: Proof draft  
Role: Foundational theorem candidate

---

## Theorem

Let:

```text
R ∈ C¹
φ ∈ C⁰
R' = R + d₀φ
```

where:

```text
(d₀φ)ᵢⱼ = φⱼ - φᵢ
```

Then:

```text
d₁R' = d₁R
```

Equivalently:

```text
Δ' = Δ
```

---

## Proof

By definition:

```text
(d₁R')ᵢⱼₖ = R'ᵢⱼ + R'ⱼₖ + R'ₖᵢ
```

Substitute:

```text
R' = R + d₀φ
```

Therefore:

```text
(d₁R')ᵢⱼₖ
= (Rᵢⱼ + φⱼ - φᵢ)
+ (Rⱼₖ + φₖ - φⱼ)
+ (Rₖᵢ + φᵢ - φₖ)
```

Group terms:

```text
= Rᵢⱼ + Rⱼₖ + Rₖᵢ
+ (φⱼ - φᵢ + φₖ - φⱼ + φᵢ - φₖ)
```

The scalar displacement terms cancel:

```text
φⱼ - φᵢ + φₖ - φⱼ + φᵢ - φₖ = 0
```

Thus:

```text
(d₁R')ᵢⱼₖ = Rᵢⱼ + Rⱼₖ + Rₖᵢ = (d₁R)ᵢⱼₖ
```

Therefore:

```text
d₁R' = d₁R
```

QED.

---

## Epistemic Interpretation

Curvature Δ does not depend on absolute scalar displacement of singularities.

Therefore Δ does not encode absolute relational authority.

It encodes cyclic relational tension only.

---

## Safety Relevance

A local re-labeling or scalar shift of singularities cannot create a new curvature state.

This supports the non-authoritative reading of relational tension.
