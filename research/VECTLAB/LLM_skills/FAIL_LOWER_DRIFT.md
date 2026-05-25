# FAIL_LOWER_DRIFT.md

**Project:** VECTAETOS Agentic Audit  
**Location:** `protocols/fail-lower-drift.md`  
**Status:** Draft v0.1  
**Document Type:** Working protocol / anti-drift failover procedure  

---

## 0. Purpose

This protocol defines how the project handles uncertainty, exhaustion, emotion, typos, naming conflicts, conversational ambiguity, and model drift.

The goal is simple:

```text
When drift appears, fall back to the lower, more stable canonical layer.
```

This protocol protects the project from accidental authority.

It applies to both humans and models.

---

## 1. Core Premise

Humans have emotions.

Models have drift.

Projects need procedures that account for both.

A human may write imprecisely because of:

```text
fatigue
emotion
speed
typo
pressure
context overload
associative thinking
```

A model may respond imprecisely because of:

```text
overgeneralization
pattern completion
premature synthesis
naming drift
false harmonization
context compression
authority misassignment
```

Therefore:

```text
chat statement is not automatically canonical
```

---

## 2. Canonical Principle

```text
FAIL_LOWER_DRIFT
```

Definition:

```text
When uncertainty, exhaustion, emotion, typo, model drift, naming conflict,
or conceptual ambiguity appears, the system must fall back to the lower,
more stable canonical layer.
```

Short form:

```text
If drift appears, go lower.
```

---

## 3. Canonical Layer Order

The project uses the following fallback hierarchy.

```text
temporary chat statement
    <
working hypothesis
    <
README.md
    <
CANONICAL_STATUS.md
    <
PHILOSOPHY.md / THEORY.md
    <
SECURITY_POLICY.md / TRADEMARKS.md / LICENSE.md
    <
non-drift canon
    <
VECTAETOS root constraints
```

Where `<` means:

```text
is less authoritative than
```

If two layers conflict, prefer the lower, more stable, more canonical layer.

---

## 4. Authority Rule

A statement becomes canonical only when it is aligned with:

```text
existing naming map
canonical status
anti-drift canon
repository architecture
relevant review documents
project constraints
```

A statement does not become canonical merely because:

```text
it appears in chat
it sounds plausible
it is repeated once
it is emotionally intense
it came from an assistant
it came from the user during fatigue
it appears in a temporary branch
it appears in a draft file
```

---

## 5. Typo Handling

Typos must not create new concepts by accident.

Example:

```text
ContractMash
```

is treated as a typo if the canonical naming map already contains:

```text
ContractMesh
```

Resolution:

```text
Do not create new term.
Do not rename architecture.
Correct to canonical term.
Record only if confusion repeats.
```

---

## 6. Human Emotion Handling

Human emotional statements may contain useful signal.

They must not be dismissed.

But they must not automatically override canonical structure.

Protocol:

```text
1. Preserve emotional signal.
2. Extract possible structural meaning.
3. Compare with existing canon.
4. If aligned, restate calmly.
5. If ambiguous, mark as hypothesis.
6. If conflicting, fail lower to canon.
```

Example:

```text
"peniaze, impérium, mačičky, infra"
```

Canonical extraction:

```text
Money is infrastructure metabolism, not project authority.
```

---

## 7. Model Drift Handling

If the model invents or overextends, apply:

```text
1. identify unsupported addition
2. compare against canonical files
3. downgrade to hypothesis
4. remove from active architecture
5. request source or review before promotion
```

Model outputs are not canonical unless reviewed.

---

## 8. Naming Conflict Procedure

When two possible names appear:

```text
1. Check CANONICAL_STATUS.md.
2. Check TRADEMARKS.md.
3. Check README.md.
4. Check repository naming map.
5. Check whether one form is a typo.
6. If unresolved, mark both as candidates.
7. Do not use either as final until review.
```

Allowed temporary statuses:

```text
accepted
reserved
candidate
hypothesis
suspended
rejected
typo
deprecated
```

---

## 9. Product Naming Freeze Rule

Do not create or finalize product names before the underlying object is understood.

Applies especially to:

```text
EAI-derived products
ContractMesh modules
audit packages
commercial layers
verification services
certification-like language
```

Rule:

```text
Object clarity before naming.
```

---

## 10. Repository Drift Procedure

If a file appears in the wrong place:

```text
1. Do not panic.
2. Treat it as staging.
3. Record in _REFACTORING_NOTE.md.
4. Move it during refactor.
5. Update CHANGELOG.md if the move changes structure.
```

Temporary root staging is allowed.

Root convenience must not become architecture.

---

## 11. EAI-Specific Failover

If EAI meaning becomes uncertain, fall back in this order:

```text
EAI_IMPORT_REVIEW.md
EAI_CORPUS_INVENTORY.md
upstream EAI README
CONSTRAINTS.md
DO_NOT_OPTIMIZE.md
PHILOSOPHY.md
THEORY.md
non-drift canon
```

Do not resolve EAI ambiguity by invention.

Resolve by import review.

---

## 12. Artifact / Report Failover

If there is ambiguity between artifact and report:

```text
artifact = machine-verifiable structural output
report = human-facing interpretation
```

Fallback rule:

```text
Artifact is lower and more structural.
Report is higher and interpretive.
```

Therefore:

```text
a report may interpret an artifact
an artifact must not interpret itself
```

---

## 13. kappa_trace Failover

If any language treats `kappa_trace` as a score:

```text
FAIL_LOWER_DRIFT
```

Return to:

```text
kappa_trace is a structural trace
kappa_trace is not a score
kappa_trace is not a KPI
kappa_trace is not a decision signal
kappa_trace is not truth
```

---

## 14. Hash / Ledger Failover

If hash, signature, ledger entry, or Merkle root is treated as truth:

```text
FAIL_LOWER_DRIFT
```

Return to:

```text
hash = integrity witness
signature = provenance witness
ledger = continuity witness
Merkle root = grouping / tamper-evidence witness
none of these are truth witnesses
```

---

## 15. Pull Request Use

This protocol should later be reflected in `.github/PULL_REQUEST_TEMPLATE.md`.

Suggested checklist:

```text
[ ] This change does not treat chat wording as canonical without review.
[ ] This change resolves naming conflicts through canonical files.
[ ] This change does not create a new concept from a typo.
[ ] This change does not turn kappa_trace into a score.
[ ] This change does not turn artifacts into recommendations.
[ ] This change does not turn reports into EAI.
[ ] This change fails lower when ambiguity appears.
```

---

## 16. Relation To Security

This protocol is part of conceptual security.

Technical security protects from attacks.

Conceptual security protects from false authority.

FAIL_LOWER_DRIFT protects from:

```text
accidental naming drift
model overreach
human fatigue
semantic compression
authority inflation
hype escalation
premature architecture
```

---

## 17. Minimal Operational Algorithm

```text
function handle_possible_drift(statement):
    classify statement:
        typo?
        emotion?
        hypothesis?
        candidate?
        canonical?
        conflict?

    if typo:
        correct to canonical naming map

    if emotion:
        preserve signal, do not canonize directly

    if hypothesis:
        mark as hypothesis

    if conflict:
        fall back to lower canonical layer

    if no supporting anchor:
        do not promote

    if aligned with canon:
        accept as working statement

    if repeated and useful:
        propose update to CANONICAL_STATUS.md
```

---

## 18. Examples

### Example 1: Typo

```text
Input:
ContractMash

Canonical:
ContractMesh

Action:
Correct silently or note as typo.
Do not create new architecture.
```

---

### Example 2: Model Overreach

```text
Input:
EAI Structural Audit should be a product line.

Status:
Hypothesis only.

Action:
Hold until EAI import review confirms object boundaries.
```

---

### Example 3: Emotional Signal

```text
Input:
We need money for infra and cats.

Extraction:
Money is infrastructure metabolism.

Action:
Allowed as commercial motivation.
Not allowed as authority over VECTAETOS.
```

---

### Example 4: Artifact Drift

```text
Input:
The artifact recommends human review.

Correction:
The report may recommend human review.
The artifact may only contain structural traces.
```

---

## 19. Canonical Sentence

```text
Conversational statements are not automatically canonical.
When drift appears, the project must fall back to the lower, more stable canonical layer.
```

Slovak form:

```text
Konverzačné vyjadrenia nie sú automaticky kanonické.
Keď vznikne drift, projekt sa musí vrátiť na nižšiu, stabilnejšiu kanonickú vrstvu.
```

---

## 20. Final Reminder

```text
Humans have emotions.
Models have drift.
The project must have procedures.
```

END
