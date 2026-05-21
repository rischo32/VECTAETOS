# Claim Register — VECTAETOS / Epistemic Cryptography

Status: Draft  
Purpose: Keep definitions, theorems, conjectures, implementation claims, and empirical claims separate.

---

## Claim Classification

| Type | Meaning |
|---|---|
| Definition | Introduces formal object or term |
| Axiom | Accepted structural constraint |
| Proposition | Derivable statement, proof desirable |
| Theorem | Proven statement |
| Conjecture | Plausible but unproven |
| Implementation claim | Claim about code behavior |
| Empirical claim | Requires experimental evidence |
| Interpretive claim | Philosophical reading, not proof |

---

## Core Definitions

### D1. Field definition

```text
Φ = (Σ,R)
```

Type: Definition  
Status: Stable

---

### D2. Singularities

```text
Σ = {INT, LEX, VER, LIB, UNI, REL, WIS, CRE}
```

Type: Definition / Ontological axiom  
Status: Frozen for 1.x

---

### D3. Antisymmetry

```text
R ∈ so(8)
Rᵢⱼ = -Rⱼᵢ
Rᵢᵢ = 0
```

Type: Axiom  
Status: Stable

---

### D4. Curvature

```text
Δ = d₁R
(d₁R)ᵢⱼₖ = Rᵢⱼ + Rⱼₖ + Rₖᵢ
```

Type: Definition  
Status: Stable

---

### D5. Admissible curvature domain

```text
𝒟 = { Δ | Δ=d₁R, d₂Δ=0, P𝒯Δ=Δ, Rep(Δ)=1 }
```

Type: Definition  
Status: Stable structure, Rep needs refinement

---

### D6. Carrier

```text
Ξ = E = d₁⁻¹(𝒟)
```

Type: Definition  
Status: Stable

---

### D7. QE

```text
QE ⇔ d₁R ∉ 𝒟
```

Type: Definition  
Status: Stable

---

## Propositions / Theorem Candidates

### P1. Gauge invariance

```text
R' = R + d₀φ ⇒ d₁R' = d₁R
```

Type: Theorem candidate  
Status: Proof straightforward

---

### P2. Boundary relation

```text
κ = ∂𝒟
QE occurs outside 𝒟, not at κ itself.
```

Type: Proposition  
Status: Needs formal statement

---

### P3. Triality fixed-point condition

```text
P𝒯Δ = Δ ⇔ Δ ∈ Fix(𝒯)
```

Type: Theorem candidate  
Status: Standard projection property if 𝒯 is finite group action

---

### P4. Non-collapse

```text
Δ ∈ 𝒟 ⇒ no privileged singularity / no privileged triality axis
```

Type: Conjecture / theorem candidate  
Status: Depends on formal Rep(Δ)

---

### P5. Non-representability principle

```text
Δ ∉ 𝒟 ⇒ no representable field state exists inside Ξ.
```

Type: Definition consequence  
Status: Stable if Ξ=d₁⁻¹(𝒟)

---

## Implementation Claims

### I1. Vortex is non-optimizing

Claim:

```text
Vortex generates candidate trajectories without objective function.
```

Type: Implementation claim  
Evidence required:

- code audit
- no reward function
- no argmax/argmin
- no feedback into Φ
- no optimizer import / training loop

---

### I2. Epistemic Cryptography is read-only

Claim:

```text
Audit layer observes and records but does not write to Φ or V.
```

Type: Implementation claim  
Evidence required:

- call graph
- dependency graph
- no write access
- tests proving audit cannot alter state

---

### I3. CI prevents ontological drift

Claim:

```text
Repository guardrails prevent forbidden architectural changes.
```

Type: Implementation claim  
Evidence required:

- CI logs
- negative tests
- hash locks
- dependency-boundary tests

---

## Empirical Claims

### E1. Framework improves AI safety

Type: Empirical claim  
Status: Not proven

Allowed wording:

```text
candidate safety-relevant architecture
```

Forbidden wording until evidence:

```text
solves AI safety
guarantees safe AI
prevents all harmful behavior
```

---

### E2. QE prevents destructive trajectories

Type: Empirical / formal hybrid  
Status: Not proven globally

Allowed wording:

```text
Within the defined ontology, destructive configurations that violate representability are mapped to QE.
```

Need:

- formal destructive-configuration class
- red-team tests
- counterexample search

---

## Interpretive Claims

### IC1. VECTAETOS as epistemic field ontology

Type: Interpretive claim  
Status: Acceptable if clearly labeled

---

### IC2. Meaning as carrier condition

Type: Interpretive / ontological claim  
Status: Acceptable in ZMYSEL documents, not a mathematical theorem

---

## Claim Discipline Rule

Every paper, README, website, or diagram must label strong statements by class.

Never present:

```text
interpretive claim
```

as:

```text
mathematical theorem
```

Never present:

```text
candidate safety architecture
```

as:

```text
validated safe system
```
