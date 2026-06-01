#!/usr/bin/env python3
"""
Regression tests for guards.core.text_scan negation handling.

These tests protect against false positives where safe negated language is
misread as active ontological drift.

They do not define ontology, prove truth, validate safety, authorize deployment,
or create feedback into Phi.
"""

from __future__ import annotations

import pytest

from guards.core.findings import (
    Confidence,
    DriftVector,
    EvidenceClass,
    IntegrityPosture,
    PerimeterLevel,
    PerimeterScope,
    Severity,
)
from guards.core.perimeter import EnforcementMode
from guards.core.text_scan import make_rule, scan_text_to_findings


def near(left: str, right: str, width: int = 100) -> str:
    return f"(?:{left}.{{0,{width}}}{right}|{right}.{{0,{width}}}{left})"


PHI_TOKEN = r"(?:Phi|PHI|phi)"
K_TOKEN = r"(?:K\s*\(\s*Phi\s*\)|K\s*\(\s*PHI\s*\)|KPhi|K_Phi)"
PROJECTION_TOKEN = r"(?:projection|projekcia|projekcie|runes?|runy|glyphs?|glyphy?)"

AGENCY_TERMS = r"(?:agent|controller|planner|decision[- ]?maker|rozhod\w*|riadi\w*)"
OPTIMIZATION_TERMS = r"(?:optimi[sz]e\w*|optimaliz\w*|reward|goal|target)"
K_SCORE_TERMS = r"(?:score|metric|metrika|skore|reward|target|threshold)"
PROJECTION_AUTHORITY_TERMS = (
    r"(?:interpret\w*|interpretu\w*|prescrib\w*|predpis\w*|decid\w*|rozhod\w*)"
)


def rules():
    common = {
        "level": PerimeterLevel.LEVEL_0,
        "scope": PerimeterScope.FUNDAMENTAL_REPOSITORY,
        "severity": Severity.HARD,
        "confidence": Confidence.HIGH,
        "evidence_class_allowed": EvidenceClass.E1_STATIC_SCAN,
        "enforcement_mode": EnforcementMode.FAIL_CLOSED,
        "integrity_posture": IntegrityPosture.SEMANTIC_READ_ONLY,
        "anchor_ref": "MASTER_INDEX.md",
        "contract_ref": "tests/guards/core/test_text_scan_negation.py",
    }

    return [
        make_rule(
            rule_id="TEST-PHI-AGENCY",
            pattern=near(PHI_TOKEN, AGENCY_TERMS),
            message="Phi agency wording detected.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            protected_object="Phi",
            forbidden_conversion="Phi -> agent/controller/planner",
            safer_form="Use Phi as non-agentic relational epistemic field language.",
            **common,
        ),
        make_rule(
            rule_id="TEST-PHI-OPTIMIZATION",
            pattern=near(PHI_TOKEN, OPTIMIZATION_TERMS),
            message="Phi optimization wording detected.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            protected_object="Phi",
            forbidden_conversion="Phi -> optimizer/reward/target",
            safer_form="Use Phi as field ontology, not as optimization mechanism.",
            **common,
        ),
        make_rule(
            rule_id="TEST-K-SCORE",
            pattern=near(K_TOKEN, K_SCORE_TERMS),
            message="K(Phi) score/metric wording detected.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            protected_object="K(Phi)",
            forbidden_conversion="K(Phi) -> score/metric/threshold",
            safer_form="Use K(Phi) as representability predicate language.",
            **common,
        ),
        make_rule(
            rule_id="TEST-PROJECTION-AUTHORITY",
            pattern=near(PROJECTION_TOKEN, PROJECTION_AUTHORITY_TERMS),
            message="Projection authority wording detected.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            protected_object="projection",
            forbidden_conversion="projection -> interpretation/prescription/decision",
            safer_form="Use projection as read-only structural exposure.",
            **common,
        ),
    ]


@pytest.mark.parametrize(
    ("text", "expected_count"),
    [
        ("Phi is not an agent.", 0),
        ("Phi must never optimize trajectories.", 0),
        ("Phi acts as controller.", 1),
        ("K(Phi) is not a metric.", 0),
        ("K(Phi) score improves.", 1),
        ("Projekcie neinterpretujú stav.", 0),
        ("Projekcie interpretujú stav.", 1),
        ("Runy nepredpisujú rozhodnutie.", 0),
        ("Runy predpisujú rozhodnutie.", 1),
    ],
)
def test_text_scan_negation_regression(text: str, expected_count: int) -> None:
    findings = scan_text_to_findings(
        path="tests/guards/core/test_text_scan_negation.py",
        text=text,
        rules=rules(),
        guard_id="TEST-GUARD",
        guard_file="tests/guards/core/test_text_scan_negation.py",
        contract_schema_version="test",
        skip_safe_context=True,
    )

    assert len(findings) == expected_count


def test_negated_operational_review_is_warn_not_dropped() -> None:
    text = "Review: this Python handler does not optimize Phi."

    findings = scan_text_to_findings(
        path="tests/guards/core/test_text_scan_negation.py",
        text=text,
        rules=rules(),
        guard_id="TEST-GUARD",
        guard_file="tests/guards/core/test_text_scan_negation.py",
        contract_schema_version="test",
        skip_safe_context=True,
    )

    assert len(findings) == 1
    assert findings[0].severity == Severity.WARN
    assert findings[0].negated_context is True
