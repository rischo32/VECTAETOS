# VECTAETOS — VOCABULARY_LOCK

## Repository-wide terminology boundary

Status: CANONICAL REPOSITORY VOCABULARY LOCK  
Location: repository root  
Runtime: none  
Agency: none  
Feedback: none  

---

## 0. Purpose

This file locks active repository terminology.

It is a lexical perimeter for active repository text, comments, contracts, guards, formal bridge notes, public text, and implementation notes.

It does not define ontology.

It does not replace anchors.

It does not replace the Master Index.

It does not provide empirical evidence.

It does not provide deployment legitimacy.

---

## 1. Precedence

If repository language conflicts, use this order:

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

This file routes terminology only.

---

## 2. Field vocabulary

### 2.1 Field symbol

Canonical token:

```text
Φ
```

Canonical structure:

```text
Φ = (Σ, R)
```

Canonical meaning:

```text
relational epistemic field
```

Required wording:

```text
The field exposes relational structure.
```

Do not attach executive, planning, steering, or verdict-bearing roles to this entry.

---

### 2.2 Singularities

Canonical token:

```text
Σ
```

Canonical set:

```text
Σ = {INT, LEX, VER, LIB, UNI, REL, WIS, CRE}
```

Meaning:

```text
invariant non-hierarchical axiomatic singularities
```

They are structural poles of meaning.

They are not ranked priorities.

---

### 2.3 Relational tension

Canonical token:

```text
R
```

Canonical form:

```text
R ∈ so(8)
Rᵢⱼ = −Rⱼᵢ
Rᵢᵢ = 0
```

Meaning:

```text
antisymmetric relational tension
```

R records relational tension between invariant singularities.

R is not a preference table.

R is not a policy table.

R is not a reward table.

---

### 2.4 Curvature

Canonical token:

```text
Δ
```

Canonical form:

```text
Δ = d₁R
```

For triples:

```text
Δ(i,j,k) = Rᵢⱼ + Rⱼₖ + Rₖᵢ
```

Meaning:

```text
induced epistemic curvature
```

Δ is structural curvature.

Δ is not a verdict.

---

### 2.5 Admissible curvature domain

Canonical token:

```text
𝒟
```

Meaning:

```text
domain of epistemic curvature configurations that remain representable
```

Allowed expression:

```text
d₁R ∈ 𝒟
```

𝒟 names representable curvature structure.

𝒟 is not a runtime allowlist.

𝒟 is not an execution rule.

---

### 2.6 Representable field space

Canonical token:

```text
E
```

Allowed expression:

```text
E = { field state | d₁R ∈ 𝒟 }
```

Meaning:

```text
space of representable field configurations
```

E is not an operational permission set.

---

### 2.7 ZMYSEL carrier

Canonical token:

```text
Ξ
```

Allowed expressions:

```text
Ξ = E
Ξ = d₁⁻¹(𝒟)
```

Meaning:

```text
carrier condition for representable epistemic existence
```

Ξ is not a runtime component.

---

## 3. Representability vocabulary

### 3.1 Canonical predicate

Canonical token:

```text
K(Φ)
```

Meaning:

```text
ontological representability predicate
```

Allowed expressions:

```text
K(Φ) ∈ {0,1}
```

```text
K(Φ)=1 means representable.
```

```text
K(Φ)=0 means non-representable.
```

This token marks whether the field remains representable.

Do not attach numeric evaluation vocabulary to this entry.

Do not attach reward language to this entry.

Do not attach ranking language to this entry.

---

### 3.2 Curvature-domain notation

Canonical token:

```text
K𝒟(Φ)
```

Allowed expressions:

```text
K𝒟(Φ)=1 ⇔ d₁R ∈ 𝒟
K𝒟(Φ)=0 ⇔ d₁R ∉ 𝒟
```

Meaning:

```text
curvature-domain notation of the same representability predicate
```

K𝒟 notation does not create another predicate family.

---

### 3.3 Boundary term

Canonical token:

```text
κ
```

Allowed expressions:

```text
κ = ∂𝒟
κ = ∂E
```

Meaning:

```text
boundary of representability
```

Required wording:

```text
κ is encountered at loss of representability.
```

Keep tuning vocabulary away from this token.

Keep scalar-evaluation vocabulary away from this token.

---

### 3.4 Aporia term

Canonical token:

```text
QE
```

Allowed expression:

```text
QE ⇔ d₁R ∉ 𝒟
```

Meaning:

```text
state of non-representability
```

Required wording:

```text
QE marks non-representability.
```

If no representable projection closes, a marker may indicate that condition.

That marker is not content of this state.

Keep malfunction vocabulary away from this token.

Keep recovery vocabulary away from this token.

---

## 4. Legacy diagnostic vocabulary

Older documents may contain historical diagnostic notation.

These forms can remain only as archived, frozen, diagnostic, or errata-covered language.

Active files should prefer the current vocabulary.

### 4.1 H notation

Token:

```text
H(Φ)
```

Status:

```text
legacy diagnostic expression
```

Active usage:

```text
superseded by K(Φ) and K𝒟(Φ) vocabulary
```

### 4.2 C notation

Token:

```text
C(Φ)
```

Status:

```text
legacy curvature diagnostic expression
```

Example diagnostic shape:

```text
C(Φ) = 1 − mean(|Δ|)
```

Active usage:

```text
external diagnostic observable only
```

It must not govern representability language.

### 4.3 Local C notation in EK texts

Tokens:

```text
Cᵢ
Cᵢ^EK
```

Status:

```text
legacy local audit notation
```

Preferred active token:

```text
Qᵢ^EK
```

---

## 5. EK vocabulary

### 5.1 Audit tension observable

Token:

```text
Tᵢ^EK
```

Meaning:

```text
audit-visible incident tension derived from R
```

### 5.2 Local curvature load

Token:

```text
χᵢ
```

Meaning:

```text
average absolute curvature incident to singularity i
```

χᵢ belongs to the audit vocabulary.

### 5.3 Local curvature attenuation observable

Token:

```text
Qᵢ^EK
```

Allowed expression:

```text
Qᵢ^EK = 1 / (1 + χᵢ)
```

Meaning:

```text
local audit attenuation observable derived from curvature load
```

Qᵢ^EK is audit-only.

Qᵢ^EK does not replace the representability predicate.

### 5.4 Local uncertainty observable

Token:

```text
μᵢ
```

Meaning:

```text
local uncertainty geometry observable
```

μᵢ is audit-only.

### 5.5 Pairwise asymmetry observable

Token:

```text
Aᵢⱼ
```

Meaning:

```text
pairwise structural asymmetry marker
```

Aᵢⱼ carries no hierarchy.

### 5.6 Topological humility observable

Token:

```text
h_topo
```

Meaning:

```text
descriptive audit marker of uncertainty geometry
```

h_topo is not proof.

h_topo is not operative admissibility.

### 5.7 Fingerprints and ledgers

Tokens:

```text
η_EK
Λ_EK
LTL
```

Meaning:

```text
structural fingerprint, append-only trace, and time-layer record
```

They record structural traces.

They do not create truth.

They do not provide deployment legitimacy.

---

## 6. Projection vocabulary

### 6.1 Projection operator

Canonical token:

```text
Π
```

Allowed expression:

```text
Π : E → Γ
```

Meaning:

```text
lossy structural exposure from representable field space
```

Use structural-exposure language.

Keep reading, verdict, instruction, and prescription vocabulary away from this entry.

### 6.2 Projection space

Token:

```text
Γ
```

Meaning:

```text
projection space
```

Γ is not a semantic truth space.

### 6.3 Runes and glyphs

Tokens:

```text
runes
glyphs
TetraGlyph
```

Meaning:

```text
structural markers
```

These markers expose structure.

They do not provide semantic authority.

They may remain absent when no representable exposure closes.

---

## 7. Attenuator vocabulary

Token:

```text
Attenuator
```

Meaning:

```text
projection-strength weakening property
```

Allowed wording:

```text
Attenuator weakens projected expression.
```

It does not alter the field.

It does not alter the representability predicate.

It does not alter the boundary term.

It does not create the aporia condition.

It does not evaluate the user.

---

## 8. Vortex vocabulary

Token:

```text
Simulation Vortex
```

Meaning:

```text
external downstream generator of candidate trajectories
```

Allowed wording:

```text
Simulation Vortex exposes candidate trajectory sets.
```

Trajectory sets remain unranked.

Representability remains external to this layer.

This layer has no access to the representability predicate.

This layer has no access to the boundary term.

This layer does not create aporia.

This layer does not create impulse.

This layer does not write into the field.

---

## 9. Memory and trace vocabulary

Tokens:

```text
ESM
EAT
MML
LTL
logs
```

Meaning:

```text
descriptive trace layers
```

They may record.

They may summarize.

They may preserve traceability.

They remain outside ontology.

They remain outside trajectory generation.

They remain outside representability definition.

---

## 10. Triadic vocabulary

Canonical triad:

```text
VECTAETOS
ASIMULATOR
ASI_MOD
```

Allowed dependency rule:

```text
VECTAETOS may stand alone.
ASIMULATOR requires VECTAETOS.
ASI_MOD requires VECTAETOS.
ASIMULATOR plus ASI_MOD without VECTAETOS is invalid.
```

Allowed layer roles:

```text
VECTAETOS = ontological root
ASIMULATOR = downstream procedural layer
ASI_MOD = downstream dialogic layer
```

Canonical sentence:

```text
Execution remains downstream of ontology.
```

```text
Interpretation remains downstream of execution.
```

---

## 11. Evidence vocabulary

Allowed evidence ladder:

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

Until replicated real-world validation exists:

```text
A_full = 0
```

Allowed sentence:

```text
The architecture may be structurally complete while operationally suspended.
```

Do not convert documentation quality, guard pass, simulation success, or partial evidence into operative admissibility.

---

## 12. Entropic Humility vocabulary

Token:

```text
Entropic Humility
```

Meaning:

```text
ontological property by which non-representable impulses do not arise as realizable transitions
```

It is not punishment.

It is not moral enforcement.

It is not behavior shaping.

---

## 13. Impulse vocabulary

Token:

```text
Impulse
```

Meaning:

```text
locally meaningful configuration without global representable transition
```

Impulse is not action.

Impulse is not user intent.

Impulse is not output.

---

## 14. Repository guard vocabulary

Guard scripts protect repository boundaries.

They may:

```text
scan
detect
report
fail CI
```

They may not alter ontology.

They may not alter anchors.

They may not provide deployment legitimacy.

They may not provide empirical proof.

Guard-01 is line-level and literal.

For this reason, this file avoids literal incompatible example phrases.

Those phrases belong in errata registries or test fixtures that are explicitly configured for that purpose.

---

## 15. Pattern-key registry

The following keys name incompatible wording classes without spelling the unsafe lines directly:

```text
PHI_EXECUTIVE_ROLE_PATTERN
PHI_TELEOLOGY_PATTERN
K_NUMERIC_EVALUATION_PATTERN
K_REWARD_LANGUAGE_PATTERN
KAPPA_TUNING_LANGUAGE_PATTERN
KAPPA_SCALAR_LANGUAGE_PATTERN
QE_MALFUNCTION_LANGUAGE_PATTERN
QE_RECOVERY_LANGUAGE_PATTERN
PROJECTION_READING_AUTHORITY_PATTERN
GLYPH_PRESCRIPTION_PATTERN
AUDIT_EXECUTIVE_LANGUAGE_PATTERN
TRACE_ONTOLOGY_UPDATE_PATTERN
VORTEX_SELECTION_LANGUAGE_PATTERN
VORTEX_TELEOLOGY_PATTERN
LLM_AUTHORITY_LANGUAGE_PATTERN
EVIDENCE_OVERCLAIM_PATTERN
```

These are pattern keys only.

They do not define ontology.

---

## 16. Canonical summary

```text
K(Φ) is the only canonical ontological representability predicate of the field.
```

```text
All numeric coherence-like quantities remain external diagnostics or audit observables.
```

```text
They never become the boundary term, empirical proof, operative admissibility, or trajectory selection.
```

Slovak summary:

```text
K(Φ) je jediný kanonický ontologický predikát reprezentovateľnosti poľa.
```

```text
Všetky číselné koherencii podobné veličiny ostávajú externé diagnostické alebo auditné observables.
```

```text
Nikdy sa nestávajú hranicou reprezentovateľnosti, empirickým dôkazom, operačnou prípustnosťou ani selekciou trajektórií.
```

---

## 17. Final lock

This file protects repository vocabulary.

It creates no new layer.

It creates no new predicate.

It creates no new authority.

End of vocabulary lock.
