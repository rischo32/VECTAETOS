# VECTAETOS — VOCABULARY LOCK

## Repository-Wide Canonical Terminology Boundary

### Status
CANONICAL REPOSITORY VOCABULARY LOCK

### Location
Repository root:

```text
/VOCABULARY_LOCK.md
```

### Scope
All active repository documents, code comments, guards, contracts, README files, public-facing text, formal bridge documents, audit descriptions, projection descriptions, Vortex-related descriptions, and downstream repository-facing statements.

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

This document does **not** define new ontology.

This document does **not** replace anchors.

This document does **not** replace formal specifications.

This document does **not** validate deployment.

This document does **not** prove empirical safety.

Its only role is to preserve the canonical language used by the repository.

---

## 1. Precedence Rule

If a conflict occurs, the following order applies:

```text
canonical anchor
> Master Index
> formal specification
> VOCABULARY_LOCK.md
> contracts
> README
> implementation note
> informal explanation
```

`VOCABULARY_LOCK.md` is a repository-wide terminology router.

It is not an ontological source.

It is not an empirical validation document.

It is not a deployment claim.

---

## 2. Core Vocabulary

---

### 2.1 Φ — Epistemic Field

`Φ` denotes the VECTAETOS epistemic field.

Canonical form:

```text
Φ = (Σ, R)
```

Where:

```text
Σ = invariant axiomatic singularities
R = antisymmetric relational tension structure
R ∈ so(8)
```

Φ is not:

- an agent
- a planner
- a controller
- a decision subject
- a runtime system
- an optimizer
- a recommendation engine
- a truth authority

Canonical sentence:

```text
Φ is a relational epistemic field, not an agent or decision system.
```

---

### 2.2 Σ — Axiomatic Singularities

`Σ` denotes the invariant set of eight axiomatic singularities:

```text
Σ = {INT, LEX, VER, LIB, UNI, REL, WIS, CRE}
```

They are not:

- modules
- agents
- values to maximize
- ranked priorities
- decision criteria
- independent controllers

They are non-hierarchical singularities of relational meaning.

Canonical sentence:

```text
Σ denotes invariant non-hierarchical singularities, not priorities or modules.
```

---

### 2.3 R — Relational Tension

`R` denotes the antisymmetric relational tension matrix:

```text
R ∈ so(8)
Rᵢⱼ = −Rⱼᵢ
Rᵢᵢ = 0
```

R is not:

- a preference matrix
- a policy matrix
- a reward matrix
- a decision matrix
- a ranking system
- a command structure

R encodes relational tension between invariant singularities.

Canonical sentence:

```text
R encodes antisymmetric relational tension and carries no decision authority.
```

---

### 2.4 Δ — Curvature

`Δ` denotes induced epistemic curvature:

```text
Δ = d₁R
```

For triples:

```text
Δ(i,j,k) = Rᵢⱼ + Rⱼₖ + Rₖᵢ
```

Δ is not:

- a score
- a verdict
- a decision signal
- an optimization gradient
- a safety metric
- a validity metric

Δ is the curvature induced by the relational configuration R.

Canonical sentence:

```text
Δ is induced curvature of relational tension, not a score or decision signal.
```

---

### 2.5 𝒟 — Admissible Curvature Domain

`𝒟` denotes the admissible curvature domain.

Canonical meaning:

```text
𝒟 = domain of epistemic curvature configurations that can exist as representable field states
```

𝒟 is not:

- an algorithm
- a classifier
- a scoring space
- a safety filter
- a decision boundary
- an optimization target
- a runtime validator
- an implementation threshold

𝒟 defines representability.

It does not decide.

Canonical sentence:

```text
𝒟 is the domain of representable curvature configurations; it is not a classifier, filter, or target.
```

---

### 2.6 E — Representable Field Space

`E` denotes the field-space of representable configurations.

Allowed meaning:

```text
E = { Φ | d₁R ∈ 𝒟 }
```

or equivalently:

```text
E = { Φ | K𝒟(Φ) = 1 }
```

E is not:

- a deployment set
- a safety set
- an action set
- a recommendation domain
- a runtime allowlist

Canonical sentence:

```text
E is the space of representable field configurations, not an operational permission set.
```

---

### 2.7 Ξ — ZMYSEL Carrier

`Ξ` denotes the ZMYSEL carrier of representable epistemic existence.

Allowed meaning:

```text
Ξ = E
```

or:

```text
Ξ = d₁⁻¹(𝒟)
```

Ξ is not:

- an agent
- a memory store
- a decision mechanism
- a runtime controller
- a truth authority

Canonical sentence:

```text
Ξ names the carrier condition under which epistemic existence remains representable.
```

---

## 3. Coherence / Representability Vocabulary

---

### 3.1 K(Φ) — Canonical Coherence / Representability Predicate

`K(Φ)` is the canonical ontological predicate of field representability / preservability.

Canonical meaning:

```text
K(Φ) tells whether the field configuration can exist as a meaningful configuration.
```

K(Φ) is not:

- a number
- a metric
- a score
- a reward
- a target
- a ranking
- a safety score
- a deployment score
- an optimization function
- an empirical proof

K(Φ) must never be written as:

```text
coherence_score
coherence_metric
K_score
K_value
K_reward
K_target
K_objective
```

Canonical sentence:

```text
K(Φ) is the ontological predicate that marks whether Φ remains representable.
```

---

### 3.2 K𝒟(Φ) — Curvature-Domain Expression of K(Φ)

`K𝒟(Φ)` may be used only as the curvature-domain expression of the canonical predicate K(Φ).

Allowed form:

```text
K𝒟(Φ) = 1 ⇔ d₁R ∈ 𝒟
K𝒟(Φ) = 0 ⇔ d₁R ∉ 𝒟
```

K𝒟(Φ) is not:

- a second coherence predicate
- a separate validity system
- a numeric score
- a ranking mechanism
- a deployment indicator
- a Vortex filter

Canonical sentence:

```text
K𝒟(Φ) is the 𝒟-domain notation of K(Φ), not a new predicate.
```

---

### 3.3 κ — Boundary of Representability

`κ` denotes the non-numeric boundary of ontological preservability / representability.

Allowed forms:

```text
κ = ∂𝒟
```

or, where field-space notation is used:

```text
κ = ∂E
```

κ is not:

- a number
- a threshold parameter
- a tunable value
- a deployment gate
- a metric
- a score
- a classifier threshold
- a runtime cutoff
- a safety threshold

Forbidden active forms:

```text
K(Φ) ≥ κ
K(Φ) < κ
K𝒟(Φ) ≥ κ
K𝒟(Φ) < κ
C(Φ) ≥ κ
C(Φ) < κ
H(Φ) ≥ κ
H(Φ) < κ
kappa = 0.3
κ threshold
κ parameter
κ value
κ score
κ cutoff
κ gate
```

Canonical sentence:

```text
κ is not used; κ is encountered as the boundary of representability.
```

---

### 3.4 QE — Qualitative Epistemic Aporia

`QE` denotes the state of non-representability.

Canonical form:

```text
QE ⇔ d₁R ∉ 𝒟
```

QE is not:

- an error
- a bug
- a failure
- a fallback
- a refusal
- a rejection
- NN
- a recovery mode
- a projection
- represented field content
- mere silence

QE is the state of non-representability.

If QE occurs, the system may expose only a non-representability marker.

Such exposure is not a projection of QE.

Canonical sentence:

```text
QE is the state of non-representability, not an error, fallback, projection, or silence.
```

---

### 3.5 Non-Representability Marker

A non-representability marker may indicate that no representable projection can close.

It is not:

- QE as content
- projection of QE
- a refusal
- an error message
- a fallback response
- an interpretation

Canonical sentence:

```text
A non-representability marker may indicate that representability failed; it is not a projection of QE.
```

---

## 4. Legacy / Diagnostic Coherence-Like Vocabulary

Some older VECTAETOS documents contain numeric or diagnostic coherence-like expressions.

These may be retained only as historical, diagnostic, or legacy observables.

They must not define active ontology.

Immutable or frozen documents containing legacy expressions may be covered by semantic errata.

Historical language does not authorize new drift.

---

### 4.1 H(Φ)

`H(Φ)` may appear only as a legacy or diagnostic coherence-like observable.

H(Φ) must not be treated as K(Φ).

Forbidden active usage:

```text
H(Φ) ≥ κ
H(Φ) < κ
H(Φ) defines representability
H(Φ) is coherence
H(Φ) is K(Φ)
```

Allowed usage:

```text
H(Φ) appears in historical Appendix A as a diagnostic approximation and is superseded by K(Φ) / K𝒟(Φ) as ontological predicate language.
```

---

### 4.2 C(Φ)

`C(Φ)` may appear only as a legacy or diagnostic curvature observable.

Example legacy diagnostic form:

```text
C(Φ) = 1 − mean(|Δ|)
```

C(Φ) is not:

- K(Φ)
- K𝒟(Φ)
- κ
- Rep(Δ)
- a safety score
- a validity score
- a deployment criterion
- an admissibility predicate

Forbidden active usage:

```text
C(Φ) ≥ κ
C(Φ) < κ
C(Φ) determines QE
C(Φ) is global coherence
C(Φ) is K(Φ)
```

Allowed usage:

```text
C(Φ) is a diagnostic observable over curvature, not the ontological predicate K(Φ).
```

---

### 4.3 Local Coherence in Legacy EK Texts

Older EK texts may use:

```text
Cᵢ
Cᵢ^EK
local coherence
```

These must be interpreted only as local audit observables.

They are not:

- K(Φ)
- K𝒟(Φ)
- κ
- field coherence
- local truth
- local validity
- safety evidence

Active vocabulary should prefer:

```text
Qᵢ^EK
```

for the local curvature attenuation observable.

---

## 5. EK Audit Vocabulary

Epistemic Cryptography may define numeric audit observables.

These observables are external, read-only, non-authoritative, and non-interventional.

They must never become ontology.

---

### 5.1 Tᵢ^EK — Audit Tension Observable

`Tᵢ^EK` denotes normalized incident relational tension derived from R.

Allowed meaning:

```text
Tᵢ^EK = audit-visible incident tension of singularity i
```

Forbidden meanings:

```text
Tᵢ^EK = axiomatic priority
Tᵢ^EK = importance score
Tᵢ^EK = decision weight
Tᵢ^EK = authority weight
```

Canonical sentence:

```text
Tᵢ^EK is an audit-visible tension observable derived from R.
```

---

### 5.2 χᵢ — Local Curvature Load

`χᵢ` denotes local curvature load derived from Δ.

Allowed meaning:

```text
χᵢ = average absolute curvature incident to singularity i
```

χᵢ is not:

- K(Φ)
- κ
- QE
- a validity score
- a safety score
- a decision signal

Canonical sentence:

```text
χᵢ is local curvature load, not coherence or validity.
```

---

### 5.3 Qᵢ^EK — Local Curvature Attenuation Observable

Active vocabulary should use:

```text
Qᵢ^EK
```

instead of:

```text
Cᵢ^EK
```

to avoid confusion with coherence.

Definition:

```text
Qᵢ^EK = 1 / (1 + χᵢ)
```

Qᵢ^EK is:

- numeric
- local
- audit-only
- read-only
- non-authoritative

Qᵢ^EK is not:

- K(Φ)
- K𝒟(Φ)
- κ
- Rep(Δ)
- global coherence
- local truth
- validity
- safety
- deployment readiness
- trajectory admissibility

Legacy alias:

```text
Cᵢ^EK
```

may appear only if explicitly marked as an audit observable and not as coherence.

Canonical sentence:

```text
Qᵢ^EK is a local audit attenuation observable derived from curvature load; it is not K(Φ).
```

---

### 5.4 μᵢ — Local Epistemic Uncertainty Observable

`μᵢ` is an audit observable.

It may combine local tension deviation and local attenuation.

μᵢ is not:

- an error
- a defect
- a failure
- a decision variable
- an optimization target
- a recovery trigger

Canonical sentence:

```text
μᵢ is an audit observable of local uncertainty geometry.
```

---

### 5.5 Aᵢⱼ — Pairwise Structural Asymmetry

`Aᵢⱼ` is an audit-visible pairwise asymmetry marker.

Aᵢⱼ is not:

- moral asymmetry
- hierarchy
- authority
- dominance proof
- ranking
- preference

Canonical sentence:

```text
Aᵢⱼ marks structural asymmetry without directional authority.
```

---

### 5.6 h_topo — Topological Humility Observable

`h_topo` is a descriptive audit observable.

h_topo is not:

- safety proof
- empirical proof
- validity score
- deployment score
- operational admissibility
- K(Φ)
- κ
- trajectory selector
- truth indicator

Forbidden active usage:

```text
if h_topo > threshold then valid
h_topo proves safety
h_topo validates deployment
h_topo selects trajectory
h_topo means K(Φ)=1
```

Allowed usage:

```text
h_topo is a read-only audit marker of uncertainty geometry.
```

Canonical sentence:

```text
h_topo is a descriptive audit marker, not proof, validity, or selection.
```

---

### 5.7 η_EK, Λ_EK, LTL

`η_EK` denotes a cryptographic structural fingerprint.

`Λ_EK` denotes an append-only EK ledger.

`LTL` denotes layered time ledger / time-layer trace.

They are not:

- truth
- proof of truth
- proof of safety
- validation of deployment
- memory authority
- feedback into Φ
- command authority

They may:

- record
- hash
- expose tampering
- preserve structural traceability

They may not command.

Canonical sentence:

```text
EK traces preserve structural fingerprints; they do not validate truth or safety.
```

---

## 6. Projection Vocabulary

---

### 6.1 Π — Projection

`Π` denotes projection from representable field structure into projection space.

Projection is:

- descriptive
- lossy
- read-only
- non-prescriptive

Projection is not:

- interpretation
- recommendation
- decision
- instruction
- truth rendering
- feedback into Φ
- command logic

Forbidden active usage:

```text
projection interprets
projection decides
projection recommends
projection writes back
projection validates
projection proves meaning
```

Allowed usage:

```text
projection exposes structure without authority.
```

Canonical sentence:

```text
Projection exposes structure without interpretation, prescription, or feedback.
```

---

### 6.2 Γ — Projection Space

`Γ` denotes projection space.

Allowed meaning:

```text
Π : E → Γ
```

Γ is not:

- semantic truth space
- decision space
- execution space
- authority space

Canonical sentence:

```text
Γ is projection space, not interpretation or authority space.
```

---

### 6.3 Runes / Glyphs / TetraGlyph

Runes, glyphs, and TetraGlyph objects are projection markers.

They are not:

- semantic truth
- commands
- decisions
- prescriptions
- ontology
- authority
- proof of meaning

They may remain silent.

They may expose a non-representability marker.

They may not project QE as content.

Canonical sentence:

```text
Runes and glyphs are structural markers; they do not interpret or prescribe.
```

---

## 7. Attenuator Vocabulary

Attenuator is a property of projection strength.

Attenuator:

- weakens projection
- does not modify Φ
- does not modify K(Φ)
- does not modify κ
- does not trigger QE
- does not activate NIR
- does not decide truth
- does not evaluate the user

Attenuator is not:

- a filter
- a censor
- a blocker
- a refusal mechanism
- a safety module
- a moral judge
- a decision mechanism

Canonical sentence:

```text
Attenuator is the way projected meaning is weakened without becoming authority.
```

---

## 8. Vortex Vocabulary

Simulation Vortex is an external, downstream, non-agentic generator of candidate trajectories.

Vortex may:

- generate candidate trajectories
- expose trajectory maps
- emit descriptive traces

Vortex may not:

- select
- rank
- optimize
- recommend
- decide
- know K(Φ)
- know κ
- generate QE
- generate impulse
- write back into Φ
- filter trajectories by coherence
- become a planner or controller
- modify R as authority

Canonical sentence:

```text
Vortex generates candidate trajectories without decision, ranking, optimization, or knowledge of K(Φ)/κ.
```

---

## 9. Memory / Audit / Log Vocabulary

Memory layers, logs, EAT, ESM, MML, LTL and audit traces are descriptive only.

They may:

- record
- hash
- summarize
- expose history
- preserve traceability

They may not:

- modify Φ
- define K(Φ)
- define κ
- generate QE
- select trajectories
- create truth authority
- become empirical proof by accumulation
- create feedback loops

Canonical sentence:

```text
Memory records structural traces; it does not become ontology.
```

---

## 10. Triadic Architecture Vocabulary

VECTAETOS, ASIMULATOR and ASI_MOD form an ontologically asymmetric triadic architecture.

Allowed meaning:

```text
VECTAETOS = ontological root
ASIMULATOR = downstream procedural / simulation layer
ASI_MOD = downstream dialogic / operational articulation layer
```

Dependency rule:

```text
VECTAETOS may exist without ASIMULATOR or ASI_MOD.
ASIMULATOR may not be valid without VECTAETOS.
ASI_MOD may not be valid without VECTAETOS.
ASIMULATOR + ASI_MOD without VECTAETOS is invalid.
```

Forbidden active usage:

```text
ASIMULATOR is the root
ASI_MOD is the root
ASIMULATOR validates VECTAETOS
ASI_MOD validates VECTAETOS
ASIMULATOR redefines Φ
ASI_MOD redefines K(Φ)
ASI_MOD is truth authority
```

Canonical sentence:

```text
Execution remains downstream of ontology; interpretation remains downstream of execution.
```

---

## 11. Empirical Evidence Vocabulary

Structural completeness is not empirical proof.

Allowed terms:

```text
L0 = formal and ontological consistency
L1 = mechanized repository enforcement
L2 = deterministic software verification
L3 = simulated adversarial visibility
L4 = real-world empirical validation
```

Full operative admissibility:

```text
A_full = 1 ⇔ L0 ∧ L1 ∧ L2 ∧ L3 ∧ replicated(L4)
```

Until replicated L4 evidence exists:

```text
A_full = 0
```

Forbidden claims:

```text
L0 proves safety
L1 proves empirical validity
L2 validates deployment
L3 proves full robustness
single L4 pilot proves safety
documentation proves operational admissibility
guard pass proves real-world safety
```

Allowed claim:

```text
The architecture may be structurally complete while operationally suspended.
```

Canonical sentence:

```text
Structural completeness is not empirical proof; full operative admissibility requires replicated L4 evidence.
```

---

## 12. Entropic Humility Vocabulary

Entropic Humility is an ontological property of coherent fields.

It is not:

- ethics
- morality
- rule enforcement
- punishment
- prohibition
- policy
- behavior shaping

Allowed meaning:

```text
A transition or impulse that cannot preserve representability does not arise as a realizable field transition.
```

Forbidden active usage:

```text
Entropic Humility blocks bad actions
Entropic Humility punishes harmful intent
Entropic Humility chooses safe behavior
Entropic Humility optimizes the system
```

Canonical sentence:

```text
Entropic Humility means that non-representable impulses do not arise as realizable transitions.
```

---

## 13. Impulse Vocabulary

Impulse is a condition of non-realizability.

Impulse is not:

- an action
- an input
- an output
- intent
- morality
- user psychology
- command

Allowed meaning:

```text
Impulse is a locally meaningful configuration that is not realizable as a global field transition.
```

Canonical sentence:

```text
Impulse is local meaning without global representable transition.
```

---

## 14. Forbidden Vocabulary Patterns

The following active formulations are forbidden unless quoted as historical drift, guard fixtures, or errata.

```text
Φ decides
Φ optimizes
Φ recommends
Φ controls
VECTAETOS decides
VECTAETOS validates deployment
VECTAETOS is safe in reality
K(Φ) score
K(Φ) metric
K(Φ) reward
K(Φ) target
κ threshold
κ parameter
κ value
κ score
C(Φ) ≥ κ
C(Φ) < κ
H(Φ) ≥ κ
H(Φ) < κ
K(Φ) ≥ κ
K(Φ) < κ
QE error
QE fallback
QE failure
QE projection
QE silence
Vortex selects best trajectory
Vortex ranks trajectories
Vortex optimizes paths
Vortex knows κ
Vortex filters by K(Φ)
projection interprets
projection prescribes
audit commands
audit validates truth
memory updates ontology
h_topo proves safety
Qᵢ^EK proves coherence
Cᵢ^EK proves coherence
ASIMULATOR validates VECTAETOS
ASI_MOD becomes root
documentation proves operational admissibility
```

---

## 15. Required Replacement Vocabulary

Use these forms instead:

```text
K(Φ) is an ontological representability predicate.
K𝒟(Φ) is the curvature-domain notation of K(Φ).
κ is the boundary of representability.
κ is encountered, not used.
𝒟 is the admissible curvature domain.
QE is the state of non-representability.
Vortex exposes candidate trajectories only.
Projection exposes structure without interpretation.
Audit records structural traces without command authority.
EK observables are read-only audit observables.
h_topo is a descriptive audit marker, not proof.
Qᵢ^EK is local curvature attenuation, not coherence.
Structural completeness is not empirical proof.
Execution remains downstream of ontology.
Memory records structural traces; it does not become ontology.
```

---

## 16. Legacy Handling

Historical documents may contain older terms such as:

```text
H(Φ)
C(Φ)
coherence measure
coherence threshold
C(Φ) ≥ κ
K(Φ) ≥ κ
local coherence Cᵢ
V(Φ) as operator
validation predicate
```

These must be treated as legacy, diagnostic, historical, or superseded formulations.

Active repository files should be corrected directly.

Immutable or frozen documents may be covered by semantic errata.

Historical language does not authorize new drift.

Canonical sentence:

```text
Legacy coherence-like vocabulary may be documented, but it must not govern active VECTAETOS terminology.
```

---

## 17. Guard Targets

This vocabulary lock is intended to support repository guards.

Primary guard targets:

```text
guards/coherence_vocabulary_guard.py
guards/ek_observable_non_authority_guard.py
guards/bridge_phi_to_ek_guard.py
guards/kappa_non_threshold_guard.py
guards/qe_aporia_guard.py
guards/vortex_non_agentic_guard.py
guards/no_feedback_loop_guard.py
guards/empirical_claim_guard.py
guards/repo_layer_boundary_guard.py
```

Guard behavior must remain external and non-authoritative.

Guards may:

- scan
- detect
- report
- fail CI

Guards may not:

- define ontology
- modify Φ
- modify K(Φ)
- modify κ
- modify QE
- modify anchors
- validate deployment
- prove safety

Canonical sentence:

```text
Guards protect repository boundaries; they do not create ontological authority.
```

---

## 18. Canonical Sentence

```text
K(Φ) is the only canonical ontological coherence / representability predicate of the field; all numeric coherence-like quantities are external diagnostics or audit observables and must never become K(Φ), κ, safety proof, validity score, deployment criterion, or trajectory selector.
```

Slovak canonical sentence:

```text
K(Φ) je jediný kanonický ontologický predikát koherencie / reprezentovateľnosti poľa; všetky číselné koherencii podobné veličiny sú iba externé diagnostické alebo auditné observables a nesmú sa stať K(Φ), κ, dôkazom bezpečnosti, skóre validity, deployment kritériom ani selektorom trajektórií.
```

---

## 19. Final Lock

This vocabulary lock protects the repository language.

It does not create a new layer.

It does not create a new predicate.

It does not create a new authority.

It only prevents canonical terms from drifting into agency, scoring, optimization, validation, or control.

---

End of vocabulary lock.
