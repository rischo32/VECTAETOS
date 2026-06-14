# VECTAETOS™ Guard Core Tests

**Path:** `tests/guards/core/`  
**Scope:** tests for `guards/core/` shared implementation kernel  
**Ontology authority:** none  
**Decision authority:** none  
**Optimization authority:** none  
**Feedback into Φ:** none  

---

## 0. Boundary

    This directory contains tests for the VECTAETOS guard shared core.
    It is a test surface.
    It is not part of the guard runtime kernel.

```text
tests/guards/core/ ≠ guards/core/
test finding ≠ truth
test pass ≠ ontology preserved
test pass ≠ empirical validation
test failure ≠ metaphysical proof
```

The implementation kernel lives in:

    guards/core/

1. Purpose

These tests verify that the shared guard core preserves repository-perimeter discipline.

They cover:

    import surface
    Finding schema invariants
    safe PASS / FAIL wording
    Level 0–5 perimeter coordinates
    negation-aware text scanning
    absence of pytest files inside guards/core/

The tests expose drift in the implementation surface.

They do not define canonical meaning.

2. Expected test files
   
    test_core_import_surface.py
    test_core_contract.py
    test_text_scan_negation.py
    test_no_tests_inside_guard_core.py

Additional tests may be added as the shared core stabilizes.

3. Run

From repository root:

    python -m pytest tests/guards/core

Do not run from inside tests/guards/core/ unless the import path is explicitly prepared.

4. Import rule

Allowed:

    from guards.core.findings import ...
    from guards.core.reporting import ...
    from guards.core.text_scan import ...

Forbidden:

    from Core import ...
    from core import ...
    from guards.Core import ...

/Core/ is a separate repository surface.

/guards/core/ is the guard shared implementation kernel.

5. Safe interpretation

Allowed language:

    core contract tests passed
    no configured blocker detected
    guard core import surface is stable

Forbidden language:

    ontology proven
    VECTAETOS is safe (nie preto žeby nemal byť, ale chzýba empiria evidence na urovni L0)
    guard core validates truth
    tests authorize deployment
    
6. Final posture
   
    Tests constrain implementation drift.
    Tests do not create ontology.
