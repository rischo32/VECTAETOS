# VECTAETOS™ — Immutable Surfaces Policy

**Path:** `guards/IMMUTABLE_SURFACES_POLICY.md`  
**Status:** implementation policy / repository perimeter discipline  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Auto-fix authority:** none  
**Feedback into Φ:** none  

---

## 0. Boundary Statement

This document defines repository protection discipline for **Protected Immutable Surfaces**.

It does not define Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, ZMYSEL, or any canonical ontology.

It does not prove truth.

It does not validate safety.

It does not authorize deployment.

It defines a fail-closed repository perimeter for sensitive files whose silent mutation could alter how VECTAETOS is represented, checked, reported, or released.

```text
Immutable surface = locked by default, unlockable by explicit protocol, auditable after unlock.
```

---

## 1. Core Principle

A protected immutable surface is not “unchangeable forever”.

It is a repository surface that ordinary PRs must not modify silently.

A protected surface may change only through an explicit unlock protocol that is visible, reviewed, scoped, time-bounded, and auditable.

```text
No ordinary PR may change the protected object and the checker protecting it in the same untrusted tree.
```

---

## 2. Three-Layer Model

Protected immutable surfaces are governed by three layers.

```text
1. Human-readable policy
2. Machine-readable manifest
3. External trusted enforcement
```

### 2.1 Human-readable policy

The human-readable policy explains what is protected and why.

Primary file:

```text
guards/IMMUTABLE_SURFACES_POLICY.md
```

This file is itself part of the protected surface.

### 2.2 Machine-readable manifest

The manifest lists protected paths, protected globs, optional hashes, unlock labels, workflow names, and fail-closed settings.

Primary file:

```text
contracts/immutable_surfaces_manifest.json
```

The manifest is itself part of the protected surface.

Any manifest modification requires unlock.

### 2.3 External trusted enforcement

The external root of trust must exist outside the modified PR tree.

Examples:

```text
GitHub branch protection
CODEOWNERS
required reviews
required checks
trusted base-ref workflow execution
no direct push to main
```

A guard must not pretend to verify what only GitHub governance can enforce.

---

## 3. Threat Model

A normal PR must not be able to modify all of these together:

```text
the protected object
the checker protecting it
the manifest defining the protection
the workflow enforcing the protection
```

If one PR can change all of them at once and make the check trust the changed versions, the guard is self-bypassable.

The repository must therefore evaluate protected surface changes against the trusted base branch, not only against files supplied by the PR.

---

## 4. Initial Protected Surface

The initial protected immutable surface includes:

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

Maintainers may extend this list through the unlock protocol.

---

## 5. Why These Surfaces Are Protected

### 5.1 `anchors/`

Anchors contain canonical project meaning.

Silent mutation of anchors is ontology drift.

### 5.2 `formal/`

Formal documents expose or mechanize canonical meaning.

Silent mutation can alter formal representation.

### 5.3 `ontology/` and `governance/`

These directories may contain high-trust policy, routing, release, or governance artifacts.

Silent mutation can alter repository authority structure.

### 5.4 `guards/core/`

`guards/core/` defines shared Finding shape, reporting behavior, text scanning, AST scanning, path classification, role inference, capability rules, and byte-integrity helpers.

Changing it changes how guard findings are seen.

### 5.5 `guards/canonical_ontology_guard.py`

This is the root ontology boundary guard.

It must not be weakened by the same PR it evaluates.

### 5.6 `contracts/`

Contracts are machine-readable projections of policy and anchor constraints.

They are not ontology, but they can influence enforcement.

### 5.7 `.github/workflows/`

Guard workflows decide which checks run.

A PR must not weaken the workflow that evaluates that same PR.

### 5.8 `CODEOWNERS`

CODEOWNERS defines required ownership and review surfaces.

Changing it can change who is allowed to approve protected changes.

### 5.9 Requirements and tool config

Dependency and tooling files influence what code runs in CI.

They belong to the runtime perimeter.

---

## 6. Enforcement Rule

Ordinary PRs must fail if they modify protected paths.

Protected paths may be changed only through explicit unlock.

The immutable surface check must compare PR changed files against the protected surface defined on the trusted base branch.

The check must not rely solely on files modified by the PR.

If the checker cannot determine whether a protected change is admissible, it must fail closed.

---

## 7. Unlock Protocol

A protected-path change is admissible only when all required conditions are satisfied.

Minimum required conditions:

```text
PR has label: immutable-surface-unlock
PR body contains explicit reason
CODEOWNERS approval is present
approving reviewer is not the PR author
CI immutable check passes
manifest diff is visible
no silent autofix is used
no direct push to main is used
trusted base-ref policy is used for evaluation
```

The unlock protocol does not mean “the ontology approves the change”.

It means:

```text
Repository maintainers declared and reviewed a bounded protected-surface modification.
```

---

## 8. Unlock Request File

A protected-surface unlock should include an explicit unlock request file.

Recommended path:

```text
governance/unlocks/UNLOCK-YYYY-MM-DD-<short-name>.json
```

Example:

```json
{
  "schema_version": "1.0",
  "unlock_id": "UNLOCK-2026-05-GUARD-CORE-001",
  "scope": "guards/core/",
  "paths_allowed": [
    "guards/core/findings.py",
    "guards/core/reporting.py"
  ],
  "reason": "Shared guard kernel refactor correction.",
  "expires_utc": "2026-05-27T23:59:00Z",
  "requires_review": true,
  "ontology_authority": false,
  "auto_fix_allowed": false
}
```

Unlock files are audit artifacts.

They do not create ontology.

They do not validate safety.

---

## 9. Manifest Rule

The immutable surfaces manifest is machine-readable policy.

Recommended path:

```text
contracts/immutable_surfaces_manifest.json
```

The manifest may list:

```text
protected_paths
protected_globs
protected_hashes
allowed_unlock_labels
required_unlock_file_glob
required_owners
workflow_names
fail_closed_mode
base_ref_required
trusted_runtime_required
ontology_authority
auto_fix_allowed
```

The manifest is protected by the immutable surface itself.

Any manifest modification requires unlock.

---

## 10. Suggested Manifest Shape

```json
{
  "schema_version": "1.0",
  "manifest_role": "protected_immutable_surface",
  "protected_paths": [
    "guards/canonical_ontology_guard.py",
    "guards/run_perimeter.py",
    "guards/IMMUTABLE_SURFACES_POLICY.md",
    "contracts/perimeter_manifest.json",
    "contracts/immutable_surfaces_manifest.json",
    "CODEOWNERS"
  ],
  "protected_globs": [
    "anchors/**",
    "formal/**",
    "ontology/**",
    "governance/**",
    "guards/core/**",
    "contracts/*.schema.json",
    "contracts/*contract*.json",
    ".github/workflows/*guard*.yml"
  ],
  "protected_hashes": [],
  "allowed_unlock_labels": [
    "immutable-surface-unlock"
  ],
  "required_unlock_file_glob": "governance/unlocks/UNLOCK-*.json",
  "workflow_names": [
    "immutable-surface",
    "canonical-ontology-guard"
  ],
  "fail_closed_mode": true,
  "base_ref_required": true,
  "trusted_runtime_required": true,
  "ontology_authority": false,
  "auto_fix_allowed": false
}
```

---

## 11. Protection Modes

Protected surfaces may use several protection modes.

```text
path_locked
byte_sealed
workflow_locked
contract_locked
review_locked
release_locked
```

### 11.1 `path_locked`

The path cannot be changed by an ordinary PR.

### 11.2 `byte_sealed`

Tracked bytes must match the configured manifest hash.

Hash match means byte integrity only.

Hash match does not prove semantic truth.

### 11.3 `workflow_locked`

Workflow logic cannot be weakened by the same PR it evaluates.

### 11.4 `contract_locked`

Contracts and manifests cannot be silently changed.

### 11.5 `review_locked`

Human review is required through CODEOWNERS or equivalent branch protection.

### 11.6 `release_locked`

Release or deployment claims cannot be altered without release-specific checks.

---

## 12. Workflow Rule

Guard workflows are protected objects.

A PR modifying guard workflows must not be allowed to weaken the same check that evaluates that PR.

Trusted enforcement must come from:

```text
trusted base-ref workflow
branch protection
required checks
CODEOWNERS
non-author review
```

Workflows must not run trusted guard code from `/tmp`.

Trusted guard execution should use a workspace-local trusted base tree.

Recommended pattern:

```bash
TRUSTED_TREE=".trusted/base"
TRUSTED_GUARD="${TRUSTED_TREE}/guards/canonical_ontology_guard.py"

rm -rf "${TRUSTED_TREE}"
mkdir -p "${TRUSTED_TREE}"

git archive "${TRUSTED_REF}" \
  guards/canonical_ontology_guard.py \
  guards/core \
  | tar -x -C "${TRUSTED_TREE}"

PYTHONPATH="${PWD}/${TRUSTED_TREE}:${PWD}" \
python3 "${TRUSTED_GUARD}" \
  --base "${BASE}" \
  --head "${HEAD}" \
  --mode strict
```

This creates:

```text
trusted guard = base ref
trusted core = base ref
scanned content = PR head
runtime path = workspace, not /tmp
```

---

## 13. No `/tmp` Trusted Runtime Rule

`/tmp` must not be used as the trusted runtime location for guard execution.

Reason:

```text
/tmp is outside repository structure
/tmp breaks package import assumptions
/tmp hides trust boundaries
/tmp makes runtime provenance harder to audit
```

Allowed:

```text
.trusted/base/
```

Forbidden for trusted guard execution:

```text
/tmp/canonical_ontology_guard.py
/tmp/immutable_surface_guard.py
```

Temporary files may exist for ordinary shell mechanics, but trusted guard code must not execute from `/tmp`.

---

## 14. Failure Behavior

If the checker cannot determine whether a change is admissible, it must fail closed.

Fail closed cases include:

```text
missing trusted base manifest
unreadable manifest
invalid manifest schema
changed protected path without unlock
unlock label missing
unlock file missing
unlock expired
unlock scope mismatch
manifest modified without unlock
workflow modified without unlock
CODEOWNERS modified without unlock
ambiguous file rename across protected boundary
broken UTF-8 / mojibake in protected text
```

Failure language must remain repository-state language.

Allowed:

```text
Configured blocker detected within declared repository perimeter.
```

Forbidden:

```text
ontology proven safe
truth preserved
deployment validated
guard certified ontology
```

---

## 15. Auto-Fix Rule

Auto-fix is forbidden for protected semantic or ontological surfaces.

A guard may report.

A guard may fail CI.

A guard may write explicit report artifacts.

A guard must not silently rewrite:

```text
anchors
formal ontology text
protected contracts
guard core
workflow logic
CODEOWNERS
unlock files
```

Autofix may be considered only for non-semantic formatting after separate approval.

---

## 16. Emergency Bypass

Emergency bypass must be rare and recorded.

Minimum record:

```text
who authorized it
why it was needed
what files changed
what checks were bypassed
when it happened
what follow-up audit is required
```

Recommended location:

```text
governance/events/EMERGENCY-BYPASS-YYYY-MM-DD.md
```

Emergency bypass is a governance event.

It is not ontology.

It is not validation.

---

## 17. Required Claims Discipline

Allowed claims:

```text
Protected path changed.
Unlock protocol missing.
Unlock protocol present.
Configured blocker detected.
No configured protected-surface blocker detected.
Repository-state result only.
```

Forbidden claims:

```text
safe
validated
truth proven
ontology certified
deployment-ready
semantically correct
empirically proven
```

---

## 18. Relation to Existing Guard Core

This policy aligns with the shared guard kernel:

```text
guards/core/findings.py
guards/core/reporting.py
guards/core/contracts.py
guards/core/text_scan.py
guards/core/ast_scan.py
guards/core/paths.py
guards/core/roles.py
guards/core/capabilities.py
guards/core/immutable_blob.py
```

The shared kernel must remain non-authoritative.

It standardizes diagnostics.

It does not define VECTAETOS.

---

## 19. Implementation Order

Recommended order:

```text
1. stop trusted guard execution from /tmp
2. add guards/IMMUTABLE_SURFACES_POLICY.md
3. add contracts/immutable_surfaces_manifest.json
4. add guards/immutable_surface_guard.py
5. add .github/workflows/immutable-surface.yml
6. add or update CODEOWNERS
7. configure branch protection / required checks
8. add byte-seal manifest for anchors and guards/core
9. add unlock fixtures and tests
```

Do not implement the full lock before the unlock path exists.

A lock without unlock becomes maintenance deadlock.

An unlock without external review becomes bypass.

Both are invalid.

---

## 20. Final Boundary Sentence

```text
Protected Immutable Surfaces protect repository trust boundaries.
They do not decide ontology.
```

Slovak:

```text
Protected Immutable Surfaces chránia dôveryhodné hranice repozitára.
Nerozhodujú, čo je VECTAETOS.
```

End.
