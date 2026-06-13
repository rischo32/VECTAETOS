# Theorem Draft — Boundary and QE

Status: Formal clarification  
Role: Prevent confusion between κ and QE.

---

## Definitions

Let:

```text
𝒟 ⊂ C²
```

be the admissible curvature domain.

Let:

```text
E = { Φ=(Σ,R) | d₁R ∈ 𝒟 }
```

Let:

```text
Ξ = E
```

Let:

```text
κ = ∂𝒟
```

or more precisely:

```text
κ = ∂_{𝒟_tri}𝒟
```

Define:

```text
QE ⇔ d₁R ∉ 𝒟
```

---

## Proposition 1

QE is not identical with κ.

### Proof

κ is the boundary of 𝒟.

QE is the condition:

```text
d₁R ∉ 𝒟
```

A boundary point may belong to closure of 𝒟 and may or may not belong to 𝒟 depending on whether 𝒟 is open, closed, or neither.

Therefore:

```text
κ ≠ QE
```

in general.

QED.

---

## Proposition 2

QE is the non-representability condition outside admissible curvature.

If:

```text
d₁R ∉ 𝒟
```

then:

```text
Φ ∉ E
```

Since:

```text
Ξ = E
```

then:

```text
Φ ∉ Ξ
```

Thus:

```text
QE ⇔ Φ ∉ Ξ
```

---

## Interpretation

κ is the boundary encountered at the limit of admissibility.

QE is the condition of being outside admissibility.

Recommended wording:

```text
κ is the boundary of representability.
QE is loss of representability.
```

Do not say:

```text
QE is the boundary.
```

Say:

```text
QE occurs beyond / outside the admissible representability domain.
```
