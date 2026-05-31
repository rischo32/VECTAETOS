# VECTAETOS — Research Guard Notes

**Path:** `research/guards/`  
**Status:** research / review / design notes  
**Active enforcement:** none  
**Ontology authority:** none  
**Runtime authority:** none  

## Role

`research/guards/` contains exploratory notes, external review outputs, guard design drafts, audit observations, and improvement proposals for the VECTAETOS guard perimeter.

This directory is not the active guard runtime.

It does not define ontology, prove truth, validate safety, authorize deployment, or replace canonical anchors.

## What Belongs Here

```text
guard review notes
Codex / AI review summaries
weakness reports
refactoring proposals
perimeter design drafts
historical guard model variants
adversarial observations
research-only implementation notes
```

## What Does Not Belong Here

```text
active guard scripts
active contracts
canonical anchors
workflow enforcement logic
runtime unlock records
production policy manifests
```

Active guard scripts belong in:

```text
guards/
guards/core/
```

Active machine-readable contracts belong in:

```text
contracts/
```

Minimal PIS research belongs in:

```text
research/pis/
```

## Boundary

Files in this directory may describe risks and possible guard behavior.

They must not be treated as executable authority.

They may inform implementation, but every implementation must be reviewed against the canonical anchors, `GUARD_PERIMETER_MODEL.md`, active contracts, and the shared guard kernel.

## Modus Operandi

```text
1. collect observation
2. classify drift vector
3. map to affected perimeter layer
4. decide whether it is research-only or implementation-ready
5. promote only through an explicit reviewed change
6. keep final active rules outside research/guards/
```

## Promotion Rule

A research note may be promoted only by creating or changing an active file in one of the proper runtime locations.

Promotion targets:

```text
guards/*.py
guards/core/*.py
contracts/*.json
.github/workflows/*.yml
```

A note is not promoted merely because it exists here.

## Non-Authority Statement

The presence of a claim, recommendation, or draft in `research/guards/` means only:

```text
this was observed or proposed for review
```

It does not mean:

```text
ontology changed
system is safe
claim is validated
guard behavior is active
human judgment is replaced
```

## Relation to PIS

`research/guards/` may contain broad guard research.

PIS-specific research should live in:

```text
research/pis/
```

This separation prevents protected-surface design from being mixed with general guard review notes.

## Safe Language

Preferred wording:

```text
proposal
review note
observed risk
candidate rule
research-only draft
non-authoritative diagnostic
```

Avoid wording:

```text
validated
proven
certified
safe
deployment-ready
ontology-preserving
```

## Učebňa

Research guard note is a review artefact. It records a possible weakness, design option, or audit observation. It relates to guard implementation, but it is not itself a guard, contract, anchor, or CI rule. It exists so we can preserve reasoning without silently turning drafts into authority.
