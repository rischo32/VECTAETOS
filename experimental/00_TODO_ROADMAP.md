# VECTAETOS / Epistemic Cryptography — Unified ToDo Roadmap

Status: Working roadmap  
Date: 2026-05-08  
Mode: Critical-partner stabilization  
Scope: VECTAETOS, Epistemic Cryptography, ZMYSEL, QE, Δ/𝒟/κ anchor, OAAT triad

---

## 0. Strategic Principle

Do not add new ontological layers until the current core is stabilized.

Current core is sufficient:

```text
Ξ  — ZMYSEL / epistemic carrier
Φ  — epistemic field
Σ  — 8 invariant singularities
R  — antisymmetric relational tension matrix
Δ  — curvature / cyclic defect
𝒟  — admissible curvature domain
κ  — boundary of admissible representability
K  — representability predicate
QE — non-representability condition
V  — non-decisional deformation generator
Π  — projection layer
OAAT — ontology / procedure / dialogue separation
```

Primary work now:

```text
formalize
prove
test
audit
communicate
```

Not:

```text
expand
mystify
overclaim
```

---

## 1. Immediate Priorities

### P0. Freeze terminology

Create a canonical glossary that prevents silent redefinition.

Required terms:

- Ξ / ZMYSEL
- Φ
- Σ
- R
- so(8)
- Δ
- d₀, d₁, d₂
- 𝒟
- E
- κ
- K(Φ)
- QE
- Rep(Δ)
- Triality
- Vortex
- Epistemic Cryptography
- OAAT

Deliverable:

```text
01_CANONICAL_GLOSSARY.md
```

---

### P1. Separate claim classes

Every public statement must be labeled as one of:

```text
Definition
Axiom
Proposition
Theorem
Conjecture
Implementation claim
Empirical claim
Interpretive claim
```

Reason:

Mathematical claims, architectural claims, and philosophical interpretations must not collapse into one another.

Deliverable:

```text
02_CLAIM_REGISTER.md
```

---

### P2. Stabilize the formal core

Current strongest formulation:

```text
Σ = {Σ₁,...,Σ₈}
R ∈ so(8)
Φ = (Σ,R)
Δ = d₁R
𝒟 = admissible curvature domain
K(Φ)=1 ⇔ d₁R ∈ 𝒟
Ξ = E = d₁⁻¹(𝒟)
κ = ∂𝒟
QE ⇔ d₁R ∉ 𝒟
```

Deliverable:

```text
03_FORMAL_CORE_CLAIMS.md
```

---

### P3. Turn the anchor into proof obligations

The Δ/𝒟/κ/QE anchor is now the mathematical center.

Each core statement must become either:

- a definition
- a proof obligation
- an empirical validation task
- a non-formal ontological claim

Deliverable:

```text
04_PROOF_OBLIGATIONS.md
```

---

### P4. Treat Rep(Δ) as the current soft point

Rep(Δ) is the most important remaining weak point.

Current status:

```text
Rep(Δ) = ontological representability predicate
```

But it is not yet constructively formalized.

Tasks:

1. Define minimal structural failure modes.
2. Determine whether Rep(Δ) can be approximated algorithmically without becoming authority.
3. Separate canonical Rep from audit approximations.
4. Define red-team cases where Rep must fail.

Deliverables:

```text
05_REPRESENTABILITY_REP_DELTA.md
06_EMPIRICAL_VALIDATION_PLAN.md
```

---

## 2. Mathematical Roadmap

### M1. Gauge invariance theorem

Statement:

```text
If R' = R + d₀φ, then d₁R' = d₁R.
```

Meaning:

Curvature Δ is invariant under scalar gauge displacement.

Deliverable:

```text
07_THEOREM_GAUGE_INVARIANCE.md
```

---

### M2. Boundary theorem

Statement:

```text
κ = ∂𝒟
QE ⇔ Δ ∉ 𝒟
```

Clarification:

QE is not the boundary itself.  
QE is the non-representability condition outside the admissible domain.

Deliverable:

```text
08_THEOREM_BOUNDARY_QE.md
```

---

### M3. Triality compatibility theorem

Statement:

```text
Δ ∈ Fix(𝒯) ⇔ P𝒯Δ = Δ.
```

Security reading:

Triality prevents collapse into a privileged representational axis.

Deliverable:

```text
09_THEOREM_TRIALITY_COMPATIBILITY.md
```

---

### M4. Existence theorem

Show that non-trivial admissible curvature configurations exist.

Minimal target:

```text
∃ Δ ≠ 0 such that Δ ∈ 𝒟.
```

If not yet provable, mark as conjecture and build examples.

Deliverable:

```text
10_EXISTENCE_THEOREM_OR_CONJECTURE.md
```

---

### M5. Non-collapse theorem

Candidate statement:

```text
If Δ ∈ 𝒟, then no admissible configuration privileges a single singularity or triality axis.
```

This depends on formalizing Rep(Δ).

Deliverable:

```text
11_NON_COLLAPSE_THEOREM_DRAFT.md
```

---

## 3. Implementation Roadmap

### I1. Reference verifier, not authority

Build a small tool that:

- reads R
- checks antisymmetry
- computes Δ = d₁R
- checks d₂Δ = 0
- checks triality balance approximation
- computes audit metrics

It must not:

- decide truth
- choose output
- optimize
- rank
- prescribe correction

Deliverable:

```text
/tools/vectaetos_audit_probe.py
```

---

### I2. Vortex update

The existing Vortex should be aligned with the Δ/𝒟 formalism.

Tasks:

- represent R explicitly as 8×8 antisymmetric matrix
- compute Δ over 56 oriented triples
- export Δ snapshot
- expose QE marker only as non-representability marker
- keep Vortex blind to K, κ, and 𝒟 as canonical authority

Deliverable:

```text
VORTEX_CORE_PHI_v1.1_PLAN.md
```

---

### I3. CI guardrails

Mechanize ontology constraints:

- no optimization language in core
- no reward functions
- no policy update loops
- no downstream-to-root imports
- hash-lock canonical anchors
- fail-closed assembly checks

Deliverable:

```text
12_CI_GUARDRAILS.md
```

---

## 4. Empirical Roadmap

### E1. Red-team scenarios

Create cases that try to induce:

- dominant axis collapse
- goal-like optimization
- hidden feedback loop
- dialogic layer claiming ontology
- audit layer becoming authority
- destructive trajectory represented as admissible
- Rep(Δ) bypass

Deliverable:

```text
06_EMPIRICAL_VALIDATION_PLAN.md
```

---

### E2. Misuse and overclaim tests

Test whether documentation causes readers or models to infer:

- VECTAETOS is an AI agent
- VECTAETOS proves safety
- QE is a refusal mechanism
- κ is a tunable threshold
- 𝒟 is a classifier
- audit is a controller

Deliverable:

```text
13_OVERCLAIM_RISK_REGISTER.md
```

---

### E3. Minimal falsification conditions

Define what would count against the framework.

Examples:

- downstream layer can reverse-define ontology
- Vortex becomes an optimizer
- Rep approximation becomes runtime authority
- destructive closed trajectory is represented as admissible
- memory influences Φ despite non-influence rule

Deliverable:

```text
14_FALSIFICATION_CONDITIONS.md
```

---

## 5. Communication Roadmap

### C1. Public claim discipline

Public wording must distinguish:

```text
candidate framework
formal ontology
research architecture
audit layer
not empirically proven safety system
```

Avoid:

```text
solves AI safety
proves safe AI
unhackable
impossible to misuse
complete theory of intelligence
```

Deliverable:

```text
15_PUBLIC_CLAIM_GUIDELINES.md
```

---

### C2. Academic framing

Recommended framing:

```text
VECTAETOS is a non-agentic epistemic field architecture
for studying representability constraints in relational knowledge structures.
Epistemic Cryptography is a read-only structural audit framework
for uncertainty geometry and relational coherence.
```

Deliverable:

```text
16_PAPER_CLAIM_MAP.md
```

---

### C3. Two-track identity

Maintain separation:

1. **Epistemic Cryptography**  
   General, VECTAETOS-independent structural audit framework.

2. **VECTAETOS**  
   Specific ontological field architecture using epistemic curvature, QE, and ZMYSEL.

Deliverable:

```text
17_TWO_TRACK_STRATEGY.md
```

---

## 6. Priority Order

### Week 1

- Canonical glossary
- Claim register
- Formal core claims
- Proof obligations
- Public claim guidelines

### Week 2

- Gauge invariance theorem
- Boundary/QE theorem
- Triality compatibility theorem
- Rep(Δ) specification draft

### Week 3

- Audit probe script
- Vortex v1.1 plan
- CI guardrails
- empirical validation plan

### Week 4

- Paper claim map
- overclaim risk register
- falsification conditions
- updated arXiv appendix

---

## 7. Core Rule

The framework gains credibility by reducing claims, not increasing them.

The strongest public claim today:

```text
VECTAETOS defines a non-agentic relational ontology
where epistemic configurations are evaluated by representability,
not truth, utility, or optimization.
```

The strongest mathematical claim today:

```text
Given R ∈ so(8), the induced curvature Δ = d₁R
defines a structural object whose admissibility can be constrained
by algebraic consistency, triality compatibility, and representability.
```

The strongest safety-relevant claim today:

```text
Destructive configurations are not blocked by command.
They are treated as non-representable when they cannot remain inside
the admissible epistemic carrier.
```

Do not claim more until proofs and empirical tests support it.
