# Existence Theorem / Conjecture — Non-Trivial Admissible Curvature

Status: Open  
Role: Show that the admissible domain is not empty or trivial.

---

## Minimal Existence

### Claim

```text
𝒟 ≠ ∅
```

### Candidate witness

```text
R = 0
Δ = d₁R = 0
```

If:

```text
Rep(0)=1
```

and:

```text
P𝒯0 = 0
d₂0 = 0
```

then:

```text
0 ∈ 𝒟
```

### Status

Likely theorem if Rep(0)=1 is declared.

---

## Non-Trivial Existence

### Stronger Claim

```text
∃ Δ ≠ 0 such that Δ ∈ 𝒟
```

### Needed

Construct R∈so(8) such that:

```text
Δ = d₁R ≠ 0
d₂Δ = 0
P𝒯Δ = Δ
Rep(Δ)=1
```

### Current status

Conjecture until explicit example.

---

## Example Construction Strategy

1. Choose small antisymmetric R with balanced pattern.
2. Compute Δ=d₁R.
3. Apply triality projection:

```text
Δ_tri = P𝒯Δ
```

4. Check whether Δ_tri remains in Im(d₁).
5. Evaluate Rep assumptions.

---

## Important Risk

Projection P𝒯 on Δ may move Δ outside Im(d₁) unless the group action commutes with d₁ or preserves Im(d₁).

Required condition:

```text
P𝒯(Im(d₁)) ⊂ Im(d₁)
```

This must be proven or declared.

---

## Proof Obligation

Show:

```text
τ d₁R = d₁(τ R)
```

for τ∈𝒯.

If true, triality preserves algebraic curvature.

---

## Research Task

Create explicit sample matrices:

```text
examples/R_balanced_01.json
examples/Delta_balanced_01.json
```

Then compute:

- Δ
- d₂Δ
- P𝒯Δ
- ||Δ-P𝒯Δ||
- dominance measures
