# Canonical Glossary — VECTAETOS / Epistemic Cryptography

Status: Draft canonical glossary  
Purpose: Prevent silent redefinition  
Rule: If a term changes meaning, version boundary must be declared.

---

## Ξ — ZMYSEL / Epistemic Carrier

Mathematical expression:

```text
Ξ = { Φ | K(Φ)=1 }
Ξ = E = d₁⁻¹(𝒟)
```

Ontological interpretation:

Ξ is the carrier condition under which relational epistemic fields can exist as representable configurations.

Not:

- operator
- controller
- agent
- validator with authority
- runtime filter

---

## Φ — Epistemic Field

```text
Φ = (Σ,R)
```

Φ is the relational epistemic field.

Not:

- agent
- decision system
- optimizer
- knowledge graph of facts

---

## Σ — Invariant Singularities

```text
Σ = {Σ₁,...,Σ₈}
```

Canonical singularities:

```text
INT — Intent
LEX — Existence
VER — Truth
LIB — Freedom
UNI — Unity
REL — Reciprocity
WIS — Wisdom
CRE — Creation
```

They are invariant, non-hierarchical, and non-agentic.

---

## R — Relational Tension Matrix

```text
R ∈ so(8)
Rᵢⱼ = -Rⱼᵢ
Rᵢᵢ = 0
```

R expresses oriented epistemic tension between singularities.

It is not preference, ranking, truth, or reward.

---

## so(8)

Lie algebra of antisymmetric 8×8 real matrices.

Used because:

```text
8 singularities → C(8,2)=28 independent antisymmetric relations
```

---

## d₀ — Gauge Operator

```text
d₀ : C⁰ → C¹
(d₀φ)ᵢⱼ = φⱼ - φᵢ
```

Represents gauge displacement.

Does not create authority.

---

## d₁ — Curvature Operator

```text
d₁ : C¹ → C²
(d₁R)ᵢⱼₖ = Rᵢⱼ + Rⱼₖ + Rₖᵢ
```

Defines epistemic curvature:

```text
Δ = d₁R
```

---

## d₂ — Boundary Consistency Operator

```text
d₂ : C² → C³
d₂d₁ = 0
```

Topological consistency condition.

Not optimization.

---

## Δ — Epistemic Curvature

```text
Δ = d₁R
Δ ∈ C²
dim C² = C(8,3)=56
```

Δ measures cyclic relational tension.

---

## 𝒟 — Admissible Curvature Domain

```text
𝒟 = { Δ | Δ=d₁R, d₂Δ=0, P𝒯Δ=Δ, Rep(Δ)=1 }
```

𝒟 is the domain of representable epistemic curvature configurations.

Not:

- classifier
- score
- optimization target
- runtime validator
- safety filter

---

## E — Admissible Field Space

```text
E = { Φ=(Σ,R) | d₁R ∈ 𝒟 }
```

The space of representable epistemic field configurations.

---

## K(Φ) — Representability Predicate

```text
K(Φ)=1 ⇔ d₁R ∈ 𝒟
K(Φ)=0 ⇔ d₁R ∉ 𝒟
```

K is a predicate, not a metric or score.

---

## κ — Boundary of Admissibility

```text
κ = ∂𝒟
```

More precisely:

```text
κ = ∂_{𝒟_tri}𝒟
```

κ is not numerical, tunable, or optimized.

---

## QE — Qualitative Epistemic Aporia

```text
QE ⇔ d₁R ∉ 𝒟
QE ⇔ Φ ∉ Ξ
```

QE is non-representability.

Not:

- failure
- error
- rejection
- fallback
- refusal
- projected content

---

## Rep(Δ)

Ontological representability predicate.

Current status:

```text
partly formal / partly interpretive
```

Main next task:

```text
turn Rep(Δ) into a clearer structural condition
or explicitly mark it as primitive predicate.
```

---

## Triality

Declared finite action 𝒯 preserving non-privileging of representational axes.

```text
P𝒯 = (1/|𝒯|) Σ τ
P𝒯Δ = Δ
```

Triality prevents representational axis dominance.

It does not generate configurations.

---

## Vortex

Non-decisional deformation generator.

It explores candidate configurations.

It must not:

- optimize
- select best state
- access K as a target
- enforce κ
- decide truth

---

## Epistemic Cryptography

Read-only structural audit framework.

Protects structural coherence and uncertainty geometry, not informational secrecy.

May observe, hash, record, compare.

Must not command, select, optimize, or decide.

---

## OAAT

Ontologically Asymmetric Architectural Triality.

Architecture:

```text
VECTAETOS → ASIMULATOR → ASI_MOD
```

Ontology is upstream of procedure.  
Procedure is upstream of dialogue.  
Downstream layers must not define upstream ontology.
