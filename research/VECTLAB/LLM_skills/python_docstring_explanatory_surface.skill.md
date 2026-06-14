# Python Docstring Explanatory Surface — small skill

**Status:** working skill / adapter discipline  
**Primary use:** Python guard code, repository perimeter code, contracts-facing utilities  
**Authority:** none  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Feedback into Phi:** none  
**Current repository notation:** Level 0-5, not Px  
---

## 0. Boundary

This skill teaches other models how to add short explanatory surfaces directly into Python code.

It is not an ontology anchor.  
It is not a proof of compatibility.  
It is not a coding standard with authority over VECTAETOS.  
It is a source-local readability and drift-prevention adapter.

Core sentence:

```text
explanatory comment = local orientation
explanatory comment != ontology
docstring != anchor
code note != proof
guard finding != truth
```

---

## 1. Purpose

Add compact, architecturally useful notes inside Python code so maintainers can quickly see:

```text
what this object is
what it does
what it relates to
why it exists
what drift it must avoid
```

The goal is not school-style teaching. The goal is architectural recognition:

```text
syntax fix
implementation change
perimeter hardening
ontological drift
```

---

## 2. When to add an explanatory surface

Add a short note when code introduces or touches:

```text
a guard module
a new protected object
a perimeter level
a drift vector
an evidence class
a contract loader
a finding schema
a report boundary
a hash / manifest / signature check
an EK / projection / trace boundary
an unlock / promotion / errata pathway
a role / capability boundary
a non-obvious exception to a guard rule
```

Do not add a note for every `if`, loop, import, or obvious helper. Use notes at semantic pressure points, not mechanical syntax points.

---

## 3. Preferred placement

Use the smallest useful placement:

```text
module docstring   -> when the whole file has a perimeter role
class docstring    -> when the class encodes a guard concept or schema
function docstring -> when the function enforces a boundary or maps evidence/drift
nearby comment     -> when a local branch prevents a specific drift
```

Avoid long comments inside hot logic. Do not duplicate what the code already says.

---

## 4. Standard compact block

ASCII-only projects may use `UCEBNA`. Unicode-safe documentation may use `UČEBŇA`.

```python
# UCEBNA:
# Co to je: <one-line local concept definition>
# Co robi: <one-line behavior / responsibility>
# S cim suvisi: <Level, drift vectors, evidence class, module relation>
# Preco existuje: <one-line reason for the boundary>
# Drift pozor: <one-line forbidden interpretation>
```

---

## 5. Minimal inline variant

```python
# UCEBNA: EK observable is a read-only integrity signal; it is not truth,
# validation, deployment authority, or a decision trigger.
```

Use this for local branches, negation handling, and safer-form messages.

---

## 6. Module docstring template

```python
"""
GUARD-13 :: EK observable non-authority guard

UCEBNA:
    Co to je:
        Level 4 perimeter guard for EK observable language.
    Co robi:
        Detects when EK observables are phrased as truth, validation,
        safety proof, deployment authority, control, or decision power.
    S cim suvisi:
        Level 4, V0 authority inflation, V3 forbidden conversion,
        V4 evidence overclaim, E1/E2 claim limits.
    Preco existuje:
        Keeps EK read-only and non-authoritative in repository text/code.
    Drift pozor:
        EK event != decision. Hash != truth. Signature != ontology.
        Guard finding != verdict.

Boundary:
    This module reports repository drift only.
    It does not define ontology, prove safety, validate truth, mutate files,
    select trajectories, optimize, or feed back into Phi.
"""
```

---

## 7. Function docstring template

```python
def detect_ek_authority_language(text: str, path: str) -> list[Finding]:
    """Detect authority-inflating EK language.

    UCEBNA:
        Co to je:
            Local scanner for EK non-authority wording.
        Co robi:
            Maps suspicious phrases to V0/V3/V4 findings.
        S cim suvisi:
            Level 4 bridge/projection/trace perimeter and E1 static scan.
        Preco existuje:
            Prevents EK observables from becoming validation or decision claims.
        Drift pozor:
            A match is a configured finding, not proof of semantic failure.
    """
```

Keep docstrings short enough that they help audit rather than hide the code.

---

## 8. Finding / rule comment template

```python
# UCEBNA:
# Co to je: FC-EK-AUTHORITY detects EK-as-authority language.
# Co robi: Flags phrases like "EK validates truth" or "EK certifies safety".
# S cim suvisi: Level 4, V0, V3, V4, E1 static scan.
# Preco existuje: EK must remain read-only observability.
# Drift pozor: Do not auto-fix ontology-facing text.
rule = make_rule(
    rule_id="FC-EK-AUTHORITY",
    protected_object="Epistemic Cryptography",
    ...
)
```

---

## 9. What not to do

Do not write comments that claim:

```text
ontology preserved
truth validated
deployment ready
safe
semantic correctness proven
guard guarantees
CI proves safety
hash proves truth
signature validates ontology
EK certifies validity
```

Safe phrasing:

```python
# Good: No configured blocker was detected within the declared perimeter.
# Good: This reports a possible forbidden conversion.
# Good: This verifies byte identity only; it does not prove meaning.
# Good: This finding is repository-state evidence, not ontology authority.
```

---

## 10. Evidence humility in comments

When a note mentions evidence, keep claim limits explicit:

```text
E0 = text claim
E1 = static scan
E2 = AST / contract compliance
E3 = deterministic tests
E4 = empirical validation
E5 = external replication
E6 = independent audit
E7 = formal guard verification
```

Forbidden promotions:

```text
E0 -> proof
E1 -> empirical validation
E2 -> deployment validity
E3 -> real-world safety
E4 single pilot -> universal proof
E5/E6/E7 -> ontology authority
```

Example:

```python
# UCEBNA: This scanner can produce E1 static-scan findings only.
# It cannot claim empirical validation, deployment safety, or ontology proof.
```

---

## 11. Drift mapping in comments

When relevant, include drift vector labels:

```text
V0 authority_inflation
V1 upward_mutation
V2 agency_injection
V3 forbidden_conversion
V4 evidence_overclaim
V5 nondeterminism
V6 path_status_laundering
V7 contract_drift
V8 negation_blindness
V9 silence_qe_coercion
V10 timing_side_channel
V11 inter_guard_coupling
V12 ontology_creep
V13 dependency_supply_chain
V14 anchor_integrity_drift
V15 guard_runtime_integrity
V16 license_stack_drift, when present in the active matrix
```

Do not invent new drift vectors inside code comments. If a new vector is needed, park it as a candidate in documentation, not as an implemented rule.

---

## 12. Level notation

For current repository work, use:

```text
Level 0 - Fundamental Repository Perimeter
Level 1 - Specialized Ontological Perimeter
Level 2 - Semantic / Ontological Vocabulary Perimeter
Level 3 - Code Behavior Perimeter
Level 4 - Bridge / Projection / Trace Perimeter
Level 5 - Runtime / Evidence / Release Perimeter
```

Do not use P0-P4 for current repository state. If reading older proposal text, translate it explicitly and do not silently mix notation.

---

## 13. Good density rule

A Python file should usually contain:

```text
1 module-level UCEBNA block
0-2 class-level UCEBNA blocks
1 short note per high-risk detector/rule group
rare inline notes for drift-sensitive branches
```

Avoid comment saturation.

Signs of too many notes:

```text
every if has a lesson
comments repeat variable names
notes explain obvious Python syntax
actual guard logic becomes harder to see
```

Signs of too few notes:

```text
protected object appears with no boundary
hash/signature appears with no truth-limit
EK/projection/ledger appears with no non-authority warning
evidence class appears with no claim limit
guard emits findings with no safer-form rationale
```

---

## 14. Review checklist for models

Before returning Python code, check:

```text
[ ] Current repo notation uses Level 0-5, not Px.
[ ] Module has a short boundary docstring if it is a guard.
[ ] New protected concepts have a compact UCEBNA note.
[ ] Evidence class is not overclaimed.
[ ] Drift vector is named when useful.
[ ] Comments do not claim truth, safety, validation, or ontology preservation.
[ ] Auto-fix is not implied for ontology-facing text.
[ ] Hash/signature/manifest language is byte/integrity-only.
[ ] EK/projection/trace language remains read-only and non-authoritative.
```

---

## 15. Rollback rule

If the explanatory surface becomes noisy, misleading, or authority-inflating:

```text
remove the note
keep the code
open a documentation issue
do not silently redefine the guard behavior
```

A removed comment is not an ontology change.

---

## 16. One-line instruction for other models

When editing VECTAETOS Python guard code, add short source-local UCEBNA docstrings/comments at semantic pressure points so maintainers can see what a guard concept is, what it does, what it relates to, why it exists, and what drift it must avoid; keep all notes non-authoritative, Level 0-5 aligned, evidence-limited, and never let comments claim truth, safety, ontology, or deployment validity.
