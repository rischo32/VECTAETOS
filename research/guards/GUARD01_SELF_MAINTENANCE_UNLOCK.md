# VECTAETOS — GUARD-01 Self-Maintenance Unlock

**Path:** `research/guards/GUARD01_SELF_MAINTENANCE_UNLOCK.md`  
**Status:** research / design proposal  
**Active enforcement:** none  
**Ontology authority:** none  
**Runtime authority:** none  

## Purpose

This document defines a research-stage unlock protocol for maintaining GUARD-01:

```text
guards/canonical_ontology_guard.py
.github/workflows/canonical-ontology-guard.yml
```

GUARD-01 protects canonical ontology boundaries and also protects its own runtime surface.

That self-protection is correct, but without an explicit maintenance protocol it can create an operational deadlock.

This document is not the unlock implementation.

It is the design boundary before implementation.

## Non-Authority Statement

This document does not define ontology.

It does not modify Phi.

It does not modify K(Phi), kappa, QE, Vortex, projection, audit, LLM role, anchors, or canonical meaning.

It does not authorize deployment, prove truth, validate safety, or replace human review.

It only describes a possible repository maintenance protocol.

## Problem

GUARD-01 currently marks these paths as self-protected:

```text
guards/canonical_ontology_guard.py
.github/workflows/canonical-ontology-guard.yml
```

A normal change to either path triggers:

```text
CANONICAL-FILE-MUTATION
```

This protects the guard from silent modification.

But it also means a valid maintenance change can be blocked by the same guard it is trying to repair.

## Threat Model

A normal pull request must not be able to modify all of these silently:

```text
the protected guard
the workflow that runs the guard
the unlock rule
the evidence record used for unlock
```

If one change can weaken the lock and change the locked object at the same time, the protection becomes self-bypassable.

## Design Goal

Create a minimal self-maintenance unlock path for GUARD-01 that is:

```text
explicit
exact-path only
time-limited
human-signed
non-authoritative
auditable
fail-closed
```

The unlock must allow maintenance.

It must not become a reusable bypass.

## Proposed Unlock Location

```text
governance/unlocks/GUARD01/UNLOCK-GUARD01-YYYY-MM-DD-short-name.json
```

Alternative research-only staging path:

```text
research/guards/unlocks/GUARD01/UNLOCK-GUARD01-YYYY-MM-DD-short-name.json
```

Recommended final active location:

```text
governance/unlocks/GUARD01/
```

Reason: GUARD-01 maintenance is repository governance, not guard research and not PIS runtime.

## Unlock Scope

The unlock may allow only exact paths.

Allowed examples:

```text
guards/canonical_ontology_guard.py
.github/workflows/canonical-ontology-guard.yml
```

Forbidden examples:

```text
guards/**
guards/*.py
.github/workflows/**
*.yml
```

No glob unlocks.

No directory unlocks.

No implicit path expansion.

## Required Unlock Fields

A valid GUARD-01 self-maintenance unlock record must contain:

```json
{
  "schema_version": "0.1",
  "unlock_id": "UNLOCK-GUARD01-YYYY-MM-DD-short-name",
  "mode": "guard01_self_maintenance",
  "paths_allowed": [
    "guards/canonical_ontology_guard.py"
  ],
  "reason": "Describe the exact maintenance reason.",
  "signed_by": "Richard Fonfára",
  "confirmation": "I confirm GUARD-01 self-maintenance unlock.",
  "expires_utc": "YYYY-MM-DDT23:59:00Z",
  "ontology_authority": false,
  "auto_fix_allowed": false,
  "ai_review": {
    "used": true,
    "advisory_only": true,
    "notes": "AI review is advisory only and is not an independent approver."
  }
}
```

## Required Validation Rules

GUARD-01 should allow a self-protected path change only when all checks pass:

```text
schema_version matches
mode is guard01_self_maintenance
paths_allowed is a non-empty list
every changed self-protected path is listed exactly
no paths_allowed entry contains glob metacharacters
reason is present
signed_by is present and matches configured maintainer
confirmation phrase is exact
expires_utc is valid and not expired
ontology_authority is false
auto_fix_allowed is false
ai_review.advisory_only is true when ai_review exists
```

If any check is ambiguous, missing, malformed, expired, or unreadable, GUARD-01 must fail closed.

## Required Confirmation Phrase

```text
I confirm GUARD-01 self-maintenance unlock.
```

The phrase must match exactly.

The phrase is not a proof of correctness.

It is a traceable human maintenance marker.

## Minimal Implementation Behaviour

When GUARD-01 detects a changed self-protected path, it should do this:

```text
1. collect changed paths
2. identify self-protected changed paths
3. search configured unlock records
4. validate unlock records
5. verify exact path coverage
6. allow only covered self-protected paths
7. report any uncovered or invalid path as BLOCKER
```

Ordinary canonical anchors and formal files remain protected by existing GUARD-01 logic.

This unlock applies only to GUARD-01 self-maintenance paths unless explicitly extended later.

## Failure Behaviour

If no valid unlock exists:

```text
BLOCKER: GUARD01-SELF-PROTECTED-PATH-WITHOUT-UNLOCK
```

If an unlock exists but is malformed, broad, expired, or mismatched:

```text
BLOCKER: GUARD01-SELF-PROTECTED-PATH-INVALID-UNLOCK
```

If the unlock parser fails unexpectedly:

```text
exit code 2
fail closed
```

## Allowed Report Language

Allowed:

```text
Self-protected GUARD-01 path changed with valid maintenance unlock.
Self-protected GUARD-01 path changed without matching unlock.
GUARD-01 self-maintenance unlock record is invalid or expired.
```

Forbidden:

```text
ontology preserved
truth proven
system safe
deployment validated
guard is correct
human review replaced
```

## Relationship to PIS

PIS protects broader repository surfaces such as:

```text
anchors/**
formal/**
contracts/**
guards/core/**
```

GUARD-01 self-maintenance unlock is narrower.

It only addresses maintenance of:

```text
guards/canonical_ontology_guard.py
.github/workflows/canonical-ontology-guard.yml
```

These two mechanisms may coexist, but they must not silently replace each other.

## Relationship to Branch Protection

This protocol is not a substitute for GitHub branch protection.

The intended final posture is:

```text
GUARD-01 detects
workflow fails on blocker
branch protection blocks merge
human maintainer uses explicit unlock when maintenance is legitimate
```

Without branch protection, the protocol is an alarm and audit trace.

With branch protection, it becomes part of the repository gate.

## Promotion Path

Research stage:

```text
research/guards/GUARD01_SELF_MAINTENANCE_UNLOCK.md
```

Implementation stage:

```text
guards/canonical_ontology_guard.py
governance/unlocks/GUARD01/UNLOCK-GUARD01-*.json
```

Future contract stage, if needed:

```text
contracts/guard01_self_maintenance_unlock.schema.json
```

## Not In Scope

This proposal does not implement:

```text
CODEOWNERS enforcement
GitHub label verification
cryptographic signing
multi-maintainer approval
workflow identity sealing
Merkle anchoring
automatic branch protection configuration
```

These may be future hardening layers.

## Minimal Next Step

Implement only this first:

```text
exact-path JSON unlock validation for GUARD-01 self-protected paths
```

Do not over-engineer.

Do not add labels, CODEOWNERS checks, signatures, or multi-reviewer logic until the minimal path is proven.

## Učebňa

Self-maintenance unlock is a maintenance key for the guard that protects itself.  
It does not weaken ontology; it defines when a guarded file may be changed deliberately.  
It relates to perimeter hardening, not semantic truth.  
What is still missing is external enforcement through branch protection and required checks.
