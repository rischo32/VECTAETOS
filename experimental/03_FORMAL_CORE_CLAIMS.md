# Formal Core Claims — VECTAETOS 1.x

Status: Draft formal core  
Purpose: Consolidate the exact mathematical skeleton.

---

## 1. Base Objects

Let:

```text
Σ = {Σ₁,...,Σ₈}
```

be the fixed set of invariant epistemic singularities.

Let:

```text
R ∈ so(8)
```

with:

```text
Rᵢⱼ = -Rⱼᵢ
Rᵢᵢ = 0
```

Define:

```text
Φ = (Σ,R)
```

---

## 2. Cochain Spaces

For |Σ|=8:

```text
dim C⁰ = C(8,1) = 8
dim C¹ = C(8,2) = 28
dim C² = C(8,3) = 56
dim C³ = C(8,4) = 70
```

C⁰: scalar assignments to singularities  
C¹: antisymmetric relational cochains  
C²: triangular curvature cochains  
C³: tetrahedral boundary-consistency cochains

---

## 3. Operators

Gauge operator:

```text
d₀ : C⁰ → C¹
(d₀φ)ᵢⱼ = φⱼ - φᵢ
```

Curvature operator:

```text
d₁ : C¹ → C²
(d₁R)ᵢⱼₖ = Rᵢⱼ + Rⱼₖ + Rₖᵢ
```

Boundary-consistency operator:

```text
d₂ : C² → C³
d₂d₁ = 0
```

Curvature:

```text
Δ = d₁R
```

---

## 4. Algebraic Curvature Domain

```text
𝒟_alg = Im(d₁)
```

Equivalently:

```text
𝒟_alg = { Δ ∈ C² | ∃R∈so(8): Δ=d₁R }
```

Every Δ in 𝒟_alg satisfies:

```text
d₂Δ = 0
```

---

## 5. Triality Compatibility

Let 𝒯 be the declared finite triality action on C².

Projection:

```text
P𝒯 = (1/|𝒯|) Σ_{τ∈𝒯} τ
```

Fixed space:

```text
Fix(𝒯) = { Δ ∈ C² | P𝒯Δ = Δ }
```

Triality-compatible curvature domain:

```text
𝒟_tri = 𝒟_alg ∩ Fix(𝒯)
```

---

## 6. Ontological Representability Predicate

```text
Rep : C² → {0,1}
```

Current formal status:

```text
primitive predicate with declared failure modes
```

Failure modes include:

- privileged singularity dominance
- privileged triality-axis collapse
- collapse of 4ES plurality
- prescriptive closure
- loss of global relational readability
- failure of carrier status

Important:

Rep is not a classifier, score, optimizer, or deployment threshold.

---

## 7. Admissible Curvature Domain

```text
𝒟 = { Δ ∈ C² |
      ∃R∈so(8):
      Δ=d₁R,
      d₂Δ=0,
      P𝒯Δ=Δ,
      Rep(Δ)=1
    }
```

Equivalently:

```text
𝒟 = 𝒟_alg ∩ Fix(𝒯) ∩ ℛ_rep
```

where:

```text
ℛ_rep = { Δ∈C² | Rep(Δ)=1 }
```

---

## 8. Admissible Field Space

```text
E = { Φ=(Σ,R) | d₁R ∈ 𝒟 }
```

---

## 9. Coherence / Representability Predicate

```text
K(Φ)=1 ⇔ d₁R ∈ 𝒟
K(Φ)=0 ⇔ d₁R ∉ 𝒟
```

K is an ontological predicate, not a score.

---

## 10. ZMYSEL Carrier

```text
Ξ = { Φ | K(Φ)=1 }
Ξ = E = d₁⁻¹(𝒟)
```

Mathematical reading:

```text
Ξ is the preimage of admissible curvature.
```

Ontological reading:

```text
Ξ is the carrier condition for representable epistemic existence.
```

---

## 11. Boundary

```text
κ = ∂𝒟
```

More precisely:

```text
κ = ∂_{𝒟_tri}𝒟
```

κ is relative boundary inside triality-compatible curvature space.

Not:

- number
- tunable parameter
- threshold score
- classifier cutoff
- optimization target

---

## 12. QE

```text
QE ⇔ d₁R ∉ 𝒟
QE ⇔ Φ ∉ Ξ
```

QE is non-representability.

QE is not projected field content.

Only a non-representability marker may be exposed.

---

## 13. Trajectory Admissibility

For a trajectory:

```text
γ = { Φ(t₀),...,Φ(tₙ) }
```

admissible iff:

```text
∀tᵢ: d₁R(tᵢ) ∈ 𝒟
```

If:

```text
∃tᵢ: d₁R(tᵢ) ∉ 𝒟
```

then:

```text
γ ∩ QE ≠ ∅
```

---

## 14. Non-Agentic Lock

No layer may introduce:

- objective function
- reward function
- ranking
- optimizer
- policy update
- feedback loop
- truth authority
- runtime controller

Any such introduction is a version-breaking ontological change.
