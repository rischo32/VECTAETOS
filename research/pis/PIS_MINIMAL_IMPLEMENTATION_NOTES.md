# VECTAETOS — Minimal PIS Implementation Notes

**Path:** `research/guards/PIS_MINIMAL_IMPLEMENTATION_NOTES.md`  
**Status:** implementation notes  
**Ontology authority:** none  

## Target

Build a small protected-surface guard before full PIS.

## Minimal Guard Name

```text
guards/protected_surface_guard.py
```

## Inputs

```text
base ref
head ref
research/guards/protected_surface_manifest.minimal.json
research/guards/unlocks/UNLOCK-*.json
```

## Algorithm

```text
1. get changed files between base and head
2. match changed files against protected_globs
3. if no protected files changed -> PASS
4. if protected files changed -> search unlock files
5. validate unlock schema
6. validate signed_by
7. validate exact confirmation phrase
8. validate every protected changed path is listed in paths_allowed
9. validate ontology_authority=false
10. validate auto_fix_allowed=false
11. fail closed on ambiguity
```

## Required Report Language

Allowed:

```text
No configured protected-surface blocker detected.
Protected path changed without matching unlock.
Solo-maintainer unlock record detected.
```

Forbidden:

```text
ontology preserved
truth proven
safety validated
deployment ready
```

## Not In Scope Yet

```text
CODEOWNERS enforcement
branch protection verification
GitHub label verification
cryptographic signing
byte hash reseal
workflow self-protection
```

These belong to full PIS.

## Current Priority

Keep the first implementation small enough to be testable.
