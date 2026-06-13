# Theorem Draft — Triality Compatibility

Status: Proof skeleton  
Role: Formalize triality as anti-dominance constraint.

---

## Setup

Let 𝒯 be a finite group action on C².

For each:

```text
τ ∈ 𝒯
```

define action on curvature:

```text
τ · Δ
```

Define projection:

```text
P𝒯 = (1/|𝒯|) Σ_{τ∈𝒯} τ
```

---

## Theorem 1 — Idempotence

```text
P𝒯² = P𝒯
```

### Proof Sketch

For finite group action:

```text
P𝒯²
= (1/|𝒯|²) Σ_{τ∈𝒯} Σ_{σ∈𝒯} τσ
```

Since 𝒯 is a group, for every η∈𝒯 there are |𝒯| pairs (τ,σ) such that τσ=η.

Thus:

```text
P𝒯²
= (1/|𝒯|²) Σ_{η∈𝒯} |𝒯| η
= (1/|𝒯|) Σ_{η∈𝒯} η
= P𝒯
```

QED.

---

## Theorem 2 — Fixed Space

```text
P𝒯Δ = Δ ⇔ Δ ∈ Fix(𝒯)
```

Where:

```text
Fix(𝒯) = {Δ | τΔ=Δ for all τ∈𝒯}
```

### Proof Sketch

If Δ is fixed by all τ:

```text
P𝒯Δ = (1/|𝒯|)ΣτΔ = Δ
```

Conversely, if P𝒯Δ=Δ, then Δ lies in the image of P𝒯, which is the invariant subspace of the group action.

---

## VECTAETOS Interpretation

Triality compatibility:

```text
P𝒯Δ = Δ
```

means Δ does not privilege one triality representation.

This supports the anti-dominance constraint.

---

## Critical Requirement

Define 𝒯 explicitly.

Needed:

- exact elements of 𝒯
- action on singularity indices
- sign convention on oriented triples
- relation to SO(8)/so(8) triality
- whether 𝒯 is S₃-like outer automorphism or declared finite structural action

Until then, the theorem is formal but not fully instantiated.
