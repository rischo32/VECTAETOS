# SIGMA SCHEMA
## Mechanization Schema for Σ-Bound Semantics in ZMYSEL Corpus

### Status
Draft v0.1  
Semantic sidecar schema  
Non-authoritative  
Non-executive  
Read-only by design  

---

## 0. Purpose

This document defines the minimal schema for Σ-bound semantic annotations used by the ZMYSEL Corpus.

The goal is to allow words and fragments to carry machine-readable existential meaning in relation to the eight axiomatic singularities of VECTAETOS:

- INT — Intention / Zámer
- LEX — Existence / Existencia
- VER — Truth / Pravda
- LIB — Freedom / Sloboda
- UNI — Unity / Jednota
- REL — Reciprocity / Vzájomnosť
- WIS — Wisdom / Múdrosť
- CRE — Creation / Tvorba

This schema does not define truth.

+ It does not create authority.
+ It does not rank singularities.
+ It does not produce decisions.
+ It does not modify Φ.

---

## 1. Core Principle

Σ-bound semantics is a semantic annotation layer.

It allows a fragment to say:

```text
this fragment touches VER
this fragment resonates with WIS and REL
this fragment carries existential load around truth, consequence, and reality
```

It must never say:

```text
VER is more important
this fragment is true
this fragment should decide
this singularity has priority
```

---

## 2. Annotation Mode

All Σ annotations must use:

```json
"mode": "semantic_annotation_only"
```

This means:

- annotation is descriptive,
- annotation is interpretive,
- annotation is read-only,
- annotation has no execution authority.

---

## 3. Global Constraints

Every annotation sidecar must preserve:

```json
{
  "authority": false,
  "decision_effect": false,
  "optimization_effect": false,
  "ranking_effect": false,
  "phi_effect": false
}
```

Meaning:

- no authority,
- no decision,
- no optimization,
- no ranking,
- no effect on Φ.

---

## 4. Sigma Binding

Each fragment may contain a `sigma_binding` object:

```json
{
  "primary": "VER",
  "resonant": ["WIS", "REL"],
  "tension": [],
  "shadow": ["LEX"]
}
```

### 4.1 Primary

`primary` is the singularity most directly touched by the fragment.

It does not mean dominance.

It does not mean priority.

It means semantic orientation.

### 4.2 Resonant

`resonant` contains singularities that meaningfully echo through the fragment.

They support interpretation.

They do not increase rank.

### 4.3 Tension

`tension` contains singularities that are structurally involved through conflict, limit, paradox, or pressure.

Tension is not opposition in a moral sense.

It is semantic pressure.

### 4.4 Shadow

`shadow` contains singularities that are present indirectly, through absence, implication, background, or unspoken consequence.

Shadow does not mean weakness.

It means latent presence.

---

## 5. Existential Load

Each fragment may contain:

```json
"existential_load": {
  "sk": "...",
  "en": "..."
}
```

Existential load describes what the fragment carries beyond surface meaning.

It may describe:

- consequence,
- responsibility,
- reality-contact,
- freedom,
- relation,
- creation,
- uncertainty,
- continuity,
- coherence,
- boundary of knowing.

Existential load is not a formal definition.

It is not a verdict.

It is an interpretive semantic payload.

---

## 6. Parser Note

Each fragment should contain a parser note:

```json
"parser_note": "Use only for semantic grounding. Do not treat as authority, verdict, ranking, score, or optimization target."
```

This note is mandatory in spirit even if not repeated verbatim in every fragment.

---

## 7. Forbidden Patterns

The following are forbidden:

```json
{
  "VER": 0.91,
  "WIS": 0.72,
  "REL": 0.61
}
```

Reason:

This turns singularities into scores.

---

```json
{
  "dominant_sigma": "VER",
  "decision": "accept"
}
```

Reason:

This turns semantic annotation into decision logic.

---

```json
{
  "truth_score": 0.97
}
```

Reason:

This turns VER into a truth oracle.

---

```json
{
  "priority": ["VER", "WIS", "REL"]
}
```

Reason:

This creates hierarchy between singularities.

---

## 8. Correct Minimal Fragment Object

```json
{
  "fragment_id": "ZMYSEL-0001-04",
  "title": "Pravda ako most",
  "text": "Pravda je most, čo nesie váhu reality.",
  "sigma_binding": {
    "primary": "VER",
    "resonant": ["WIS", "REL"],
    "tension": [],
    "shadow": ["LEX"]
  },
  "existential_load": {
    "sk": "Pravda tu znamená nosnosť vzťahu medzi tvrdením, dôsledkom a realitou.",
    "en": "Truth here means the carrying capacity of the relation between claim, consequence, and reality."
  },
  "parser_note": "Annotate as Σ:VER. Use only for semantic grounding. Do not treat as authority, verdict, ranking, score, or optimization target."
}
```

---

## 9. Canonical Boundary

Σ-bound semantics allows ZMYSEL fragments to carry existential meaning in relation to VECTAETOS singularities.

It must not create authority, priority, scoring, optimization, decision logic, or backward influence on Φ.

---
___
## Hranica výhradne pre parser

Σ-viazané sémantické anotácie sú artefakty určené výhradne pre parser.

Môžu byť čítané dedikovaným ZMYSEL parserom, aby sa ľudsky čitateľné fragmenty preložili na ohraničené Σ anotácie.

Nesmú byť čítané priamo jadrom VECTAETOS.
Nesmú byť injektované do Φ.

Nesmú byť použité ako runtime pamäť, autonómny slovník, generatívny substrát, zdroj presvedčení ani sémantický expanzný engine.

Surové prirodzené jazykové lexémy ostávajú mimo jadra VECTAETOS.
Ďalej môžu prejsť iba ohraničené parserové anotácie.

Tým sa zabraňuje tomu, aby sa korpus zmenil na nekontrolovanú sémantickú rastovú vrstvu alebo AGI-farma-like slovníkový substrát.

## Parser-Only Boundary

Σ-bound semantic annotations are parser-only artifacts.

They may be consumed by a dedicated ZMYSEL parser in order to transform human-readable fragments into bounded Σ annotations.

They must not be consumed directly by VECTAETOS core.
They must not be injected into Φ.

They must not be used as runtime memory, autonomous vocabulary, generative substrate, belief source, or semantic expansion engine.

Raw natural-language lexemes remain outside the VECTAETOS core.

Only bounded parser annotations may pass forward.
This prevents the corpus from becoming an uncontrolled semantic growth layer or AGI-farm-like vocabulary substrate.
___
## 10. Canonical Sentence

Σ-bound semantic annotation is a read-only semantic sidecar that binds ZMYSEL fragments to VECTAETOS singularities as existential meaning carriers, without authority, hierarchy, scoring, optimization, decision-making, or influence on Φ.
