# VORTEX — SCORING MODEL v1.0

Status: Projection Layer  
Scope: Vortex Only  
Ontological Authority: None  
Affects Φ: No  

---

## 0. Purpose

This document defines the structural scoring model used inside the Vortex projection layer.

This model:

- Does NOT modify Φ
- Does NOT redefine 3Gate
- Does NOT perform interpretation
- Does NOT evaluate moral content
- Does NOT store user data

It provides structural decomposition only.

---

# 1. 3Gate Projection Axes

Each input question is decomposed along three structural axes:

W — Width  
H — Height  
D — Depth  

All values are normalized to:

0 ≤ axis ≤ 1

---

## 1.1 Width (W)

Represents horizontal scope expansion.

Approximation heuristic:
- Word count ratio
- Concept dispersion (basic token spread)

Example heuristic:
W = min(1, word_count / 12)

High W → broad, diffuse question  
Low W → narrow, focused question

---

## 1.2 Height (H)

Represents abstraction polarity.

Binary vs explanatory structure detection.

Heuristic:
- Presence of "?"
- Presence of causal markers ("why", "how", "explain")
- Declarative vs interrogative pattern

Example approximation:
H = 0.8 if explicit question mark  
H = 0.6 if causal marker  
H = 0.4 otherwise  

---

## 1.3 Depth (D)

Represents structural load / assumption density.

Heuristic:
- Character length ratio
- Clause nesting
- Conditional phrasing

Example:
D = min(1, character_length / 100)

---

# 2. Gate Pass

Gate pass is defined as:

gate_pass = min(W, H, D)

Interpretation:

Low gate_pass → structural imbalance  
High gate_pass → balanced projection

---

# 3. Sigma (σ)

Sigma represents structural tension.

Defined as:

σ = 1 − gate_pass

Range:

0 ≤ σ ≤ 1

High σ → high deformation  
Low σ → stable structure  

Sigma is not truth.  
Sigma is not confidence.  
Sigma is not correctness.

---

# 4. Delta-Type Classification

Dominant deformation axis is determined by the lowest axis value.

If:

W is minimal → ΔW  
H is minimal → ΔH  
D is minimal → ΔD  

If all three are approximately equal (within tolerance ε):

Δ0 (balanced)

---

# 5. Stability Bands

Based on gate_pass:

0.00 – 0.25 → NON_REPRESENTABLE  
0.26 – 0.50 → LOW_COHERENCE  
0.51 – 0.75 → MEDIUM_COHERENCE  
0.76 – 1.00 → HIGH_COHERENCE  

These are projection bands only.

They do not reflect ontological representability of Φ.

---

# 6. Intensity

Intensity is derived from input length buffer.

intensity = min(1, character_length / 100)

Used for visual modulation only.

Does not affect scoring logic.

---

# 7. Determinism

Given identical input text:

The scoring model must produce identical output.

No randomness permitted in scoring.

---

# 8. Boundary Condition

This scoring model:

∂Φ / ∂Scoring = 0

It does not influence:
- 3Gate ontological mechanism
- Core anchors
- Epistemic topology
- Vectaetos canonical definitions

It is strictly a projection layer for Vortex.

---

# 9. Versioning

Current version: delta_v1  
Future modifications must increment version identifier.
