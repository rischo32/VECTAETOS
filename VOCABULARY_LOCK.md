# VECTAETOS — VOCABULARY LOCK
## Repository-Wide Canonical Terminology Boundary

### Status
CANONICAL REPOSITORY VOCABULARY LOCK

### Location
Repository root: `/VOCABULARY_LOCK.md`

### Scope
All active repository documents, code comments, guards, contracts, README files, public-facing text, formal bridge documents, audit descriptions, projection descriptions, and Vortex-related descriptions.

### Authority
Terminology only.

### Ontology
None.

### Runtime
None.

### Agency
None.

### Optimization
None.

### Feedback
None.

---

## 0. Purpose

This document locks the active vocabulary of VECTAETOS.

It prevents semantic drift where canonical terms are silently redefined across repository layers.

This document does not define new ontology.

This document does not replace anchors.

This document does not replace formal specifications.

This document does not validate deployment.

This document does not prove empirical safety.

Its only role is to preserve the canonical language used by the repository.

---

## 1. Precedence Rule

If a conflict occurs, the following order applies:

```text
canonical anchor
> formal specification
> VOCABULARY_LOCK.md
> contracts
> README
> implementation note
> informal explanation
```

VOCABULARY_LOCK.md is a repository-wide terminology router.

It is not an ontological source.

2. Canonical Core Terms

2.1 Φ — Epistemic Field

Φ denotes the VECTAETOS epistemic field.
Canonical form:

Φ = (Σ, R)

Where:

Σ = invariant axiomatic singularities
R = antisymmetric relational tension structure
R ∈ so(8)

Φ is not:
an agent
a planner
a controller
a decision subject
a runtime system
an optimizer
a recommendation engine
a truth authority
Canonical sentence:

    Φ is a relational epistemic field, not an agent or decision system.

2.2 Σ — Axiomatic Singularities
Σ denotes the invariant set of eight axiomatic singularities:

Σ = {INT, LEX, VER, LIB, UNI, REL, WIS, CRE}
They are not:
modules
agents
values to maximize
ranked priorities
decision criteria
They are non-hierarchical singularities of relational meaning.

2.3 R — Relational Tension
R denotes the antisymmetric relational tension matrix:

R ∈ so(8)
Rᵢⱼ = −Rⱼᵢ
Rᵢᵢ = 0
R is not:
a preference matrix
a policy matrix
a reward matrix
a decision matrix
a ranking system
R encodes relational tension between invariant singularities.
2.4 Δ — Curvature
Δ denotes induced epistemic curvature:

Δ = d₁R
For triples:

Δ(i,j,k) = Rᵢⱼ + Rⱼₖ + Rₖᵢ

Δ is not:
a score
a verdict
a decision signal
an optimization gradient
a safety metric
Δ is the curvature induced by the relational configuration R.

2.5 𝒟 — Admissible Curvature Domain
𝒟 denotes the admissible curvature domain.
Canonical meaning:

𝒟 = domain of epistemic curvature configurations that can exist as representable field states
𝒟 is not:
an algorithm
a classifier
a scoring space
a safety filter
a decision boundary
an optimization target
a runtime validator
𝒟 defines representability.
It does not decide.

2.6 K(Φ) — Coherence / Representability Predicate
K(Φ) is the canonical ontological predicate of field representability / preservability.

Canonical meaning:
K(Φ) tells whether the field configuration can exist as a meaningful configuration.

K(Φ) is not:
a number
a metric
a score
a reward
a target
a ranking
a safety score
a deployment score
an optimization function

K(Φ) must never be written as:

coherence_score
coherence_metric
K_score
K_value
K_reward
K_target

    K(Φ) is the ontological predicate that marks whether Φ remains representable.
    
