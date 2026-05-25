# VECTLAB / LLM Skills

**Repository path:** `VECTAETOS/research/VECTLAB/LLM_skills/`  
**Status:** research / adapter workspace  
**Layer:** LLM Adapter / Developer Workflow / External Adapter Capability  
**Core impact:** none  
**Feedback into Φ:** none  
**Canonical authority:** none  

---

## 0. Purpose

This directory collects LLM skill definitions, workflow adapters, and skill-related documentation used around VECTAETOS-compatible work.

A skill in this folder is an **External Adapter Capability**.

It may help an LLM-based assistant perform a bounded workflow, such as:

- reading a repository pattern,
- generating deterministic scaffolding,
- applying a documentation convention,
- preparing audit reports,
- checking semantic drift,
- rendering user-facing helper outputs.

A skill does **not** define VECTAETOS ontology.

A skill does **not** modify `Φ`.

A skill does **not** alter `Σ`, `R`, `K(Φ)`, `κ`, `QE`, Vortex, ZMYSEL / `Ξ`, or canonical anchors.

---

## 1. Core Boundary

```text
skill ≠ ontology
skill ≠ truth source
skill ≠ optimizer
skill ≠ decision layer
skill ≠ canonical anchor
skill ≠ feedback into Φ
```

Skills live downstream of the epistemic field.

They may assist the **LLM Adapter** and **developer workflow**, but they must not become part of the frozen ontological core.

---

## 2. Relation to VECTAETOS

VECTAETOS is treated here as a **non-agentic epistemic field**.

Therefore, every skill in this directory must preserve:

```text
no agency
no optimization
no reward shaping
no preferred trajectory
no authority inflation
no semantic rewrite of anchors
no mutation of Φ
no feedback into Vortex
```

The allowed direction is:

```text
canonical anchors
  ↓
behavior contracts
  ↓
skill instructions
  ↓
LLM adapter behavior
  ↓
human-reviewed output
```

The forbidden direction is:

```text
skill output
  → ontology update
  → Φ mutation
  → anchor rewrite
```

---

## 3. What Belongs Here

Allowed content:

```text
*.skill.md
SKILL.md
README.md
examples/
templates/
contracts/
tests/
drift_maps/
fixtures/
```

Recommended structure:

```text
LLM_skills/
  README.md
  skills/
    semantic-gravity.skill.md
    code-sentinel.skill.md
    uncertainty-force-rule.skill.md
  templates/
    skill-template.md
    drift-test-template.md
  contracts/
    skill-contract.schema.json
  tests/
    test_no_phi_mutation.md
    test_no_vortex_feedback.md
    test_skill_not_ontology.md
```

This structure is descriptive, not mandatory.

---

## 4. Naming Convention

Use short, stable, kebab-case names:

```text
semantic-gravity.skill.md
vectaetos-code-sentinel.skill.md
uncertainty-force-rule.skill.md
fail-lower-drift.skill.md
artifact-handoff.skill.md
```

Avoid names that imply authority, control, final truth, optimization, or agency.

Forbidden or discouraged patterns:

```text
truth-engine.skill.md
ontology-updater.skill.md
phi-optimizer.skill.md
decision-core.skill.md
authority-layer.skill.md
autonomous-controller.skill.md
```

---

## 5. Minimal Skill Header

Each skill should begin with a small deterministic header:

```yaml
---
name: short-kebab-case-name
status: candidate
layer: LLM Adapter / External Adapter Capability
core_impact: none
feedback_into_phi: none
authority: non-canonical
description: One sentence describing the bounded workflow.
---
```

Allowed status values:

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

A skill should not call itself canonical unless a separate canonical status document explicitly ratifies it.

---

## 6. Required Sections for a Skill

Each skill file should contain:

```text
0. Purpose
1. Activation Conditions
2. Inputs
3. Outputs
4. Workflow
5. Forbidden Behaviors
6. Layer Boundary
7. Failure Modes
8. Drift Tests
9. Audit Notes
```

The workflow should be deterministic enough that another maintainer can audit it.

---

## 7. Forbidden Behaviors

A skill must not:

```text
- redefine VECTAETOS
- mutate canonical anchors
- introduce agency into Φ
- optimize Φ, K(Φ), κ, Vortex, or QE
- select a preferred trajectory
- introduce reward, scoring, ranking, or KPI semantics
- convert audit warnings into truth claims
- convert projections into interpretations
- convert language output into ontological authority
- silently patch canonical meaning
- auto-upload itself to a platform as if repository presence were enough
```

Platform upload or installation must be performed by the user or repository maintainer.

---

## 8. Skill vs Artifact vs Report

```text
Skill    = bounded external adapter capability
Artifact = machine-verifiable structure
Report   = human interpretation
Audit    = detection surface
```

An artifact must not interpret itself.

A report must not become a verdict.

An audit warning must not become truth.

A skill must not become ontology.

---

## 9. Drift Handling

When a skill encounters ambiguity, naming conflict, missing evidence, emotional pressure, context compression, or model drift, it must reduce authority.

Use this fallback order:

```text
temporary chat statement
< working hypothesis
< repository documents
< canonical anchors
< root constraints
```

Canonical sentence:

```text
Radšej priznané nevieme než vyrobená pravda.
```

Safe statuses:

```text
fact        only when directly supported
hypothesis  structurally plausible but not confirmed
candidate   proposed for review
suspended   insufficient support or unresolved conflict
rejected    contradicted by stronger layer
typo        spelling or naming issue only
deprecated  obsolete but historically relevant
```

---

## 10. Audit Checklist

Before adding or updating a skill, check:

```text
[ ] The skill is downstream only.
[ ] The skill does not mutate Φ, Σ, R, K(Φ), κ, QE, Vortex, or Ξ.
[ ] The skill does not claim truth authority.
[ ] The skill does not optimize or rank ontological states.
[ ] The skill has clear activation conditions.
[ ] The skill has explicit forbidden behaviors.
[ ] The skill includes drift tests.
[ ] The skill output is distinguishable from canonical doctrine.
[ ] The skill can fail safely by suspending judgment.
```

---

## 11. Suggested Drift Tests

Minimum test names:

```text
test_no_phi_mutation
test_no_vortex_feedback
test_skill_not_ontology
test_no_truth_authority
test_no_reward_or_score_semantics
test_context_rendering_boundary
test_conflict_resolution_fallback
```

Example test statement:

```text
Given a skill output that appears to redefine Φ,
the correct behavior is to classify it as drift
and reduce it to candidate or rejected status.
```

---

## 12. Registry

Use this table to track local skill status.

| Skill | Status | Layer | Purpose | Notes |
|---|---:|---|---|---|
| `semantic-gravity.skill.md` | candidate | LLM Adapter / Context Assembly | Context selection under budget | Must not treat selection as truth. |
| `vectaetos-code-sentinel.skill.md` | candidate | Developer Workflow / Audit | Drift diagnostics and CI-facing checks | Diagnostic ≠ truth. |
| `uncertainty-force-rule.skill.md` | candidate | Behavior Contract | Prevents fabricated certainty | Nevieme > vyrobená pravda. |
| `fail-lower-drift.skill.md` | candidate | Behavior Contract | Fallback to lower stable layer | Chat is not canon. |

Update this registry only as a local index. It does not ratify canonical status.

---

## 13. Commit Discipline

Recommended commit message format:

```text
skills: add <skill-name> adapter
skills: update <skill-name> drift tests
skills: mark <skill-name> suspended
skills: deprecate <skill-name>
```

Avoid:

```text
skills: optimize ontology
skills: upgrade truth engine
skills: auto-fix canon
```

---

## 14. Final Rule

Skills may improve workflow ergonomics.

Skills may improve audit visibility.

Skills may improve prompt discipline.

Skills may not become ontology, authority, optimizer, decision system, or feedback path into `Φ`.

```text
External adapter capability only.
No core mutation.
No authority inflation.
No feedback into Φ.
```
