from __future__ import annotations

import pytest

from guards.core.findings import finding_to_dict, make_finding
from guards.core.perimeter import (
    Confidence,
    DriftVector,
    EvidenceClass,
    EnforcementMode,
    IntegrityPosture,
    LegacyScope,
    PerimeterLevel,
    PerimeterScope,
    Severity,
    SAFE_FAIL,
    SAFE_PASS,
    compatibility_coordinates_from_legacy_scope,
    contains_forbidden_report_claim,
)
from guards.core.reporting import (
    EXIT_BLOCKER,
    EXIT_OK,
    exit_code_for,
    render_text_report,
)
from guards.core.text_scan import make_rule, scan_text_to_findings


def test_legacy_p1_maps_to_level_2_semantic_vocabulary() -> None:
    coords = compatibility_coordinates_from_legacy_scope(
        legacy_scope=LegacyScope.P1_SEMANTIC_VOCABULARY,
        vector=DriftVector.V3_FORBIDDEN_CONVERSION,
        evidence_class=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.SEMANTIC_READ_ONLY,
    )

    assert coords.level == PerimeterLevel.LEVEL_2
    assert coords.scope == PerimeterScope.SEMANTIC_VOCABULARY


def test_finding_schema_is_non_authoritative_and_deterministic() -> None:
    finding = make_finding(
        guard_id="GUARD-12",
        guard_file="guards/coherence_vocabulary_guard.py",
        rule_id="FC-KAPPA-METRIC",
        contract_schema_version="1.0",
        level=PerimeterLevel.LEVEL_2,
        scope=PerimeterScope.SEMANTIC_VOCABULARY,
        vector=DriftVector.V3_FORBIDDEN_CONVERSION,
        severity=Severity.BLOCKER,
        confidence=Confidence.HIGH,
        path="./formal/example.md",
        line=42,
        message="Pattern appears to convert κ into metric language.",
        protected_object="κ",
        observed_pattern="κ_score = 0.84",
        forbidden_conversion="κ -> metric/score/threshold",
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.SEMANTIC_READ_ONLY,
        safer_form="Use boundary-of-representability language.",
    )

    same_finding = make_finding(
        guard_id="GUARD-12",
        guard_file="guards/coherence_vocabulary_guard.py",
        rule_id="FC-KAPPA-METRIC",
        contract_schema_version="1.0",
        level=PerimeterLevel.LEVEL_2,
        scope=PerimeterScope.SEMANTIC_VOCABULARY,
        vector=DriftVector.V3_FORBIDDEN_CONVERSION,
        severity=Severity.BLOCKER,
        confidence=Confidence.HIGH,
        path="formal/example.md",
        line=42,
        message="Pattern appears to convert κ into metric language.",
        protected_object="κ",
        observed_pattern="κ_score = 0.84",
        forbidden_conversion="κ -> metric/score/threshold",
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.SEMANTIC_READ_ONLY,
        safer_form="Use boundary-of-representability language.",
    )

    data = finding_to_dict(finding)

    assert finding.id == same_finding.id
    assert data["path"] == "formal/example.md"
    assert data["level"] == "Level 2"
    assert data["scope"] == "semantic_vocabulary"
    assert data["ontology_authority"] is False
    assert data["auto_fix_allowed"] is False


def test_finding_rejects_authority_or_autofix_flags() -> None:
    with pytest.raises(ValueError):
        make_finding(
            guard_id="GUARD-12",
            guard_file="guards/coherence_vocabulary_guard.py",
            rule_id="FC-KAPPA-METRIC",
            contract_schema_version="1.0",
            level=PerimeterLevel.LEVEL_2,
            scope=PerimeterScope.SEMANTIC_VOCABULARY,
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.BLOCKER,
            confidence=Confidence.HIGH,
            path="formal/example.md",
            message="Invalid authority flag test.",
            ontology_authority=True,
        )

    with pytest.raises(ValueError):
        make_finding(
            guard_id="GUARD-12",
            guard_file="guards/coherence_vocabulary_guard.py",
            rule_id="FC-KAPPA-METRIC",
            contract_schema_version="1.0",
            level=PerimeterLevel.LEVEL_2,
            scope=PerimeterScope.SEMANTIC_VOCABULARY,
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.BLOCKER,
            confidence=Confidence.HIGH,
            path="formal/example.md",
            message="Invalid autofix flag test.",
            auto_fix_allowed=True,
        )


def test_reporting_uses_safe_repository_state_language() -> None:
    empty_report = render_text_report(
        [],
        title="VECTAETOS Core Contract Test",
        mode="strict",
        fail_on=Severity.BLOCKER,
    )

    assert SAFE_PASS in empty_report
    assert "Repository-state result only." in empty_report
    assert "Not empirical validation." in empty_report
    assert not contains_forbidden_report_claim(empty_report)
    assert exit_code_for([], fail_on=Severity.BLOCKER) == EXIT_OK

    finding = make_finding(
        guard_id="GUARD-12",
        guard_file="guards/coherence_vocabulary_guard.py",
        rule_id="FC-KAPPA-METRIC",
        contract_schema_version="1.0",
        level=PerimeterLevel.LEVEL_2,
        scope=PerimeterScope.SEMANTIC_VOCABULARY,
        vector=DriftVector.V3_FORBIDDEN_CONVERSION,
        severity=Severity.BLOCKER,
        confidence=Confidence.HIGH,
        path="formal/example.md",
        message="Pattern appears to convert κ into metric language.",
    )

    report = render_text_report(
        [finding],
        title="VECTAETOS Core Contract Test",
        mode="strict",
        fail_on=Severity.BLOCKER,
    )

    assert SAFE_FAIL in report
    assert "This report does not define ontology." in report
    assert "This report does not prove truth." in report
    assert "This report does not validate safety." in report
    assert "This report does not authorize deployment." in report
    assert exit_code_for([finding], fail_on=Severity.BLOCKER) == EXIT_BLOCKER


def test_text_scan_skips_protective_negation_but_flags_active_conversion() -> None:
    rule = make_rule(
        rule_id="FC-KAPPA-METRIC",
        pattern=r"(κ_score|κ.{0,80}(metric|score|threshold|estimate))",
        message="Pattern appears to convert κ into metric language.",
        level=PerimeterLevel.LEVEL_2,
        scope=PerimeterScope.SEMANTIC_VOCABULARY,
        vector=DriftVector.V3_FORBIDDEN_CONVERSION,
        severity=Severity.BLOCKER,
        protected_object="κ",
        forbidden_conversion="κ -> metric/score/threshold",
        safer_form="Use boundary-of-representability language.",
    )

    findings = scan_text_to_findings(
        path="formal/example.md",
        text="\n".join(
            [
                "κ is not a metric.",
                "κ_score = 0.84",
            ]
        ),
        rules=[rule],
        guard_id="GUARD-12",
        guard_file="guards/coherence_vocabulary_guard.py",
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "FC-KAPPA-METRIC"
    assert findings[0].severity == Severity.BLOCKER
    assert findings[0].line == 2
