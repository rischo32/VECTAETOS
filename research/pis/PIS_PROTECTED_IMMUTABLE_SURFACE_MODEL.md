# VECTAETOS — Protected Immutable Surface Research Model

**Path:** `research/guards/PIS_PROTECTED_IMMUTABLE_SURFACE_MODEL.md`  
**Status:** research / design model  
**Active enforcement:** no  
**Ontology authority:** none  

## Boundary

Protected Immutable Surface is a repository trust-boundary model.

It does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

It does not prove truth, safety, correctness, or deployment validity.

## Core Definition

```text
PIS = locked by default + explicit unlock + auditable reseal
```

A protected surface is not immutable forever.

It is protected against silent mutation.

## Three-Layer Model

```text
1. Policy
2. Manifest
3. External trusted enforcement
```

Policy is human-readable.

Manifest is machine-readable.

External enforcement is branch protection, required checks, CODEOWNERS, or trusted base-ref execution.

## Threat Model

A normal PR must not be able to modify all of these together:

```text
protected object
checker protecting it
manifest defining protection
workflow enforcing protection
```

If all four can change in one untrusted tree, the guard is self-bypassable.

## Full Protected Surface Candidate

```text
anchors/
formal/
ontology/
governance/

guards/core/
guards/canonical_ontology_guard.py
guards/run_perimeter.py
guards/IMMUTABLE_SURFACES_POLICY.md

contracts/perimeter_manifest.json
contracts/immutable_surfaces_manifest.json
contracts/*.schema.json
contracts/*contract*.json

.github/workflows/*guard*.yml
.github/workflows/immutable-surface.yml
.github/CODEOWNERS
CODEOWNERS

REQUIREMENTS.txt
REQUIREMENTS-dev.txt
pyproject.toml
ruff.toml
```

## Unlock Principle

Unlock is not approval by VECTAETOS.

Unlock is a visible human maintenance event.

Required future conditions:

```text
declared reason
declared path scope
expiry
review
manifest diff visibility
no autofix
reseal
```

## Solo Maintainer Adaptation

Current repository reality:

```text
one human maintainer
AI tools are advisory only
no independent human reviewer yet
```

Therefore the active model should not pretend to enforce second-human review.

Use solo signature plus audit friction until a second maintainer exists.

## No `/tmp` Trusted Runtime

Trusted guard execution should not run from `/tmp`.

Use a workspace-local trusted base tree:

```text
.trusted/base/
```

## Final Research Posture

This model is a design horizon.

The active implementation should start smaller.
