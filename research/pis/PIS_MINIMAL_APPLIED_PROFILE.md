# VECTAETOS — Minimal Protected Surface Applied Profile

**Path:** `research/pis/PIS_MINIMAL_APPLIED_PROFILE.md`  
**Status:** current recommended minimal profile  
**Active enforcement:** proposal  
**Ontology authority:** none  

## Decision

Do not implement full PIS yet.

Implement a narrow protected surface first.

## Active Minimal Surface

```text
anchors/
formal/
contracts/
guards/core/
```

## Not Locked Yet

```text
.github/workflows/
CODEOWNERS
REQUIREMENTS*
pyproject.toml
ruff.toml
guards/canonical_ontology_guard.py
guards/run_perimeter.py
```

These remain future PIS candidates.

## Why This Minimum

`anchors/` and `formal/` protect canonical meaning.

`contracts/` protects machine-readable perimeter rules.

`guards/core/` protects the shared diagnostic kernel.

This is enough to reduce silent drift without creating maintenance deadlock.

## Solo Maintainer Unlock

Current unlock requires one maintainer signature.

```text
signed_by: Richard Fonfára
confirmation: I confirm solo-maintainer protected-surface unlock.
```

AI review may be recorded as advisory only.

AI is not an independent approver.

## Unlock Conditions

A protected change is allowed only when:

```text
unlock file exists
paths_allowed contains every protected changed path
reason is present
signed_by is present
confirmation phrase is exact
ontology_authority is false
auto_fix_allowed is false
```

## Recommended Unlock Location

```text
research/pis/unlocks/UNLOCK-YYYY-MM-DD-short-name.json
```

## Recommended Research Manifest

```text
research/pis/protected_surface_manifest.minimal.json
```

Later, after stabilization, the manifest may move to:

```text
contracts/protected_surface_manifest.json
```

## Failure Posture

If a protected path changes without a matching unlock record, the guard should fail closed.

Failure means repository-state blocker.

It does not mean metaphysical invalidity.

## Next Implementation Step

Create a minimal guard:

```text
guards/protected_surface_guard.py
```

It should read the manifest and compare changed files against the protected globs.
