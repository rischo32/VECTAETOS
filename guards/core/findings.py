#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Finding Model

Role:
    Shared non-authoritative finding schema for repository perimeter guards.

Boundary:
    This module defines diagnostic records for repository-state findings.

    It does not define ontology, truth, safety, deployment validity,
    Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

    It does not decide.
    It does not optimize.
    It does not validate deployment.
    It does not modify repository files.
    It does not create feedback into Φ.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import hashlib
from pathlib import Path
from typing import Any

try:
    from guards.core.perimeter import (
        DEFAULT_CONTRACT_SCHEMA_VERSION,
        Confidence,
        DriftVector,
        EnforcementMode,
        EvidenceClass,
        IntegrityPosture,
        LegacyScope,
        PerimeterLevel,
        PerimeterScope,
        SEVERITY_ORDER,
        Severity,
        assert_non_authoritative_flags,
        coerce_drift_vector,
        coerce_enforcement_mode,
        coerce_evidence_class,
        coerce_integrity_posture,
        coerce_level,
        coerce_scope,
        default_scope_for_level,
        enum_value,
        level_from_scope,
        normalize_vectors,
    )
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from perimeter import (  # type: ignore
        DEFAULT_CONTRACT_SCHEMA_VERSION,
        Confidence,
        DriftVector,
        EnforcementMode,
        EvidenceClass,
        IntegrityPosture,
        LegacyScope,
        PerimeterLevel,
        PerimeterScope,
        SEVERITY_ORDER,
        Severity,
        assert_non_authoritative_flags,
        coerce_drift_vector,
        coerce_enforcement_mode,
        coerce_evidence_class,
        coerce_integrity_posture,
        coerce_level,
        coerce_scope,
        default_scope_for_level,
        enum_value,
        level_from_scope,
        normalize_vectors,
    )


SCHEMA_BASELINE = "perimeter-finding-schema/1.1"

# Backward-compatible export name.
# Older modules import `Scope` from findings.py.
# New code should prefer PerimeterScope plus PerimeterLevel.
Scope = LegacyScope


DEFAULT_INTEGRITY_BY_LEVEL: dict[PerimeterLevel, IntegrityPosture] = {
    PerimeterLevel.LEVEL_0: IntegrityPosture.IMMUTABLE_ANCHOR,
    PerimeterLevel.LEVEL_1: IntegrityPosture.SEMANTIC_READ_ONLY,
    PerimeterLevel.LEVEL_2: IntegrityPosture.SEMANTIC_READ_ONLY,
    PerimeterLevel.LEVEL_3: IntegrityPosture.CODE_BEHAVIOR,
    PerimeterLevel.LEVEL_4: IntegrityPosture.PROJECTION_READ_ONLY,
    PerimeterLevel.LEVEL_5: IntegrityPosture.EVIDENCE_POSTURE,
}


@dataclasses.dataclass(frozen=True, slots=True)
class Finding:
    """
    Shared repository-perimeter finding.

    A Finding is a diagnostic record, not a truth claim.
    """

    guard_id: str
    guard_file: str
    rule_id: str
    contract_schema_version: str
    scope: PerimeterScope | LegacyScope | str
    vector: DriftVector | str
    severity: Severity | str
    confidence: Confidence | str
    path: Path | str
    message: str

    level: PerimeterLevel | str | None = None
    vectors: tuple[DriftVector | str, ...] | None = None

    id: str | None = None
    line: int | None = None
    end_line: int | None = None
    column: int | None = None
    end_column: int | None = None
    role: str | None = None
    protected_object: str | None = None
    observed_pattern: str | None = None
    forbidden_conversion: str | None = None
    negated_context: bool = False

    evidence_class_claimed: EvidenceClass | str | None = None
    evidence_class_allowed: EvidenceClass | str | None = None
    enforcement_mode: EnforcementMode | str | None = None
    integrity_posture: IntegrityPosture | str | None = None

    anchor_ref: str | None = None
    contract_ref: str | None = None
    safer_form: str | None = None

    ontology_authority: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        normalized_path = normalize_path(self.path)
        normalized_scope = coerce_scope(self.scope)

        if self.level is None:
            normalized_level = level_from_scope(self.scope)
        else:
            normalized_level = coerce_level(self.level)
            expected_scope = default_scope_for_level(normalized_level)
            if normalized_scope != expected_scope:
                raise ValueError(
                    "Finding level/scope mismatch: "
                    f"level={normalized_level.value!r}, "
                    f"scope={normalized_scope.value!r}, "
                    f"expected_scope={expected_scope.value!r}"
                )

        normalized_vector = coerce_drift_vector(self.vector)

        if self.vectors is None:
            normalized_vectors = (normalized_vector,)
        else:
            normalized_vectors = normalize_vectors(self.vectors)
            if normalized_vector not in normalized_vectors:
                normalized_vectors = (normalized_vector, *normalized_vectors)

        normalized_evidence_allowed = (
            coerce_evidence_class(self.evidence_class_allowed)
            if self.evidence_class_allowed is not None
            else EvidenceClass.E1_STATIC_SCAN
        )

        normalized_evidence_claimed = (
            coerce_evidence_class(self.evidence_class_claimed)
            if self.evidence_class_claimed is not None
            else None
        )

        normalized_enforcement_mode = (
            coerce_enforcement_mode(self.enforcement_mode)
            if self.enforcement_mode is not None
            else EnforcementMode.STRICT
        )

        normalized_integrity_posture = (
            coerce_integrity_posture(self.integrity_posture)
            if self.integrity_posture is not None
            else DEFAULT_INTEGRITY_BY_LEVEL[normalized_level]
        )

        object.__setattr__(self, "path", normalized_path)
        object.__setattr__(self, "level", normalized_level)
        object.__setattr__(self, "scope", normalized_scope)
        object.__setattr__(self, "vector", normalized_vector)
        object.__setattr__(self, "vectors", normalized_vectors)
        object.__setattr__(self, "severity", coerce_severity(self.severity))
        object.__setattr__(self, "confidence", coerce_confidence(self.confidence))
        object.__setattr__(self, "evidence_class_allowed", normalized_evidence_allowed)
        object.__setattr__(self, "evidence_class_claimed", normalized_evidence_claimed)
        object.__setattr__(self, "enforcement_mode", normalized_enforcement_mode)
        object.__setattr__(self, "integrity_posture", normalized_integrity_posture)

        validate_required_text("guard_id", self.guard_id)
        validate_required_text("guard_file", self.guard_file)
        validate_required_text("rule_id", self.rule_id)
        validate_required_text("contract_schema_version", self.contract_schema_version)
        validate_required_text("message", self.message)

        assert_non_authoritative_flags(
            ontology_authority=self.ontology_authority,
            auto_fix_allowed=self.auto_fix_allowed,
        )

        validate_position("line", self.line)
        validate_position("end_line", self.end_line)
        validate_position("column", self.column)
        validate_position("end_column", self.end_column)

        if self.end_line is not None and self.line is not None and self.end_line < self.line:
            raise ValueError("Finding end_line must be >= line when both are provided.")

        if self.end_column is not None and self.column is not None and self.end_column < self.column:
            raise ValueError("Finding end_column must be >= column when both are provided.")

        if self.id is None:
            object.__setattr__(self, "id", deterministic_finding_id(self))


def coerce_severity(value: Severity | str) -> Severity:
    if isinstance(value, Severity):
        return value

    if hasattr(value, "value"):
        raw_value = value.value
    else:
        raw_value = value

    try:
        return Severity(str(raw_value))
    except ValueError as exc:
        allowed = ", ".join(item.value for item in Severity)
        raise ValueError(
            f"Finding field 'severity' has invalid value {raw_value!r}; "
            f"allowed values: {allowed}"
        ) from exc


def coerce_confidence(value: Confidence | str) -> Confidence:
    if isinstance(value, Confidence):
        return value

    if hasattr(value, "value"):
        raw_value = value.value
    else:
        raw_value = value

    try:
        return Confidence(str(raw_value))
    except ValueError as exc:
        allowed = ", ".join(item.value for item in Confidence)
        raise ValueError(
            f"Finding field 'confidence' has invalid value {raw_value!r}; "
            f"allowed values: {allowed}"
        ) from exc


def validate_required_text(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Finding field {field_name!r} is required and must be non-empty."
        )


def validate_position(field_name: str, value: int | None) -> None:
    if value is None:
        return

    if not isinstance(value, int) or value < 1:
        raise ValueError(f"Finding {field_name} must be an integer >= 1 when provided.")


def normalize_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def schema_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [schema_value(item) for item in value]

    if isinstance(value, list):
        return [schema_value(item) for item in value]

    if isinstance(value, dict):
        return {key: schema_value(item) for key, item in value.items()}

    if isinstance(value, Path):
        return normalize_path(value)

    return enum_value(value)


def finding_to_dict(finding: Finding) -> dict[str, Any]:
    data = dataclasses.asdict(finding)
    return {key: schema_value(value) for key, value in data.items()}


def deterministic_finding_id(finding: Finding) -> str:
    """
    Produce a stable id from non-authoritative finding coordinates.

    The id is only a repository diagnostic identifier.
    It is not a truth proof, safety proof, or ontology marker.
    """

    base = "|".join(
        [
            str(finding.guard_id),
            str(finding.rule_id),
            str(schema_value(finding.level)),
            str(schema_value(finding.scope)),
            ",".join(str(schema_value(vector)) for vector in (finding.vectors or ())),
            str(schema_value(finding.vector)),
            str(finding.path),
            str(finding.line or ""),
            str(finding.column or ""),
            str(finding.observed_pattern or ""),
            str(finding.protected_object or ""),
            str(finding.message),
        ]
    )
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:12]
    return f"VEC-{digest}"


def make_finding(
    *,
    guard_id: str,
    guard_file: str,
    rule_id: str,
    scope: PerimeterScope | LegacyScope | str,
    vector: DriftVector | str,
    severity: Severity | str,
    confidence: Confidence | str,
    path: Path | str,
    message: str,
    contract_schema_version: str = DEFAULT_CONTRACT_SCHEMA_VERSION,
    level: PerimeterLevel | str | None = None,
    vectors: tuple[DriftVector | str, ...] | None = None,
    **kwargs: Any,
) -> Finding:
    return Finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=level,
        scope=scope,
        vector=vector,
        vectors=vectors,
        severity=severity,
        confidence=confidence,
        path=path,
        message=message,
        **kwargs,
    )


def make_finding_from_coordinates(
    *,
    guard_id: str,
    guard_file: str,
    rule_id: str,
    coordinates: Any,
    severity: Severity | str,
    confidence: Confidence | str,
    path: Path | str,
    message: str,
    contract_schema_version: str = DEFAULT_CONTRACT_SCHEMA_VERSION,
    **kwargs: Any,
) -> Finding:
    """
    Build a Finding from a perimeter coordinates-like object.

    The object is expected to expose:
    level, scope, vectors, evidence_class, enforcement_mode, integrity_posture.
    """

    vectors = tuple(getattr(coordinates, "vectors"))
    if not vectors:
        raise ValueError("coordinates.vectors must contain at least one drift vector.")

    return Finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=getattr(coordinates, "level"),
        scope=getattr(coordinates, "scope"),
        vector=vectors[0],
        vectors=vectors,
        severity=severity,
        confidence=confidence,
        path=path,
        message=message,
        evidence_class_allowed=getattr(coordinates, "evidence_class"),
        enforcement_mode=getattr(coordinates, "enforcement_mode"),
        integrity_posture=getattr(coordinates, "integrity_posture"),
        **kwargs,
    )


__all__ = [
    "SCHEMA_BASELINE",
    "DEFAULT_CONTRACT_SCHEMA_VERSION",
    "Scope",
    "LegacyScope",
    "PerimeterLevel",
    "PerimeterScope",
    "DriftVector",
    "EvidenceClass",
    "EnforcementMode",
    "IntegrityPosture",
    "Severity",
    "SEVERITY_ORDER",
    "Confidence",
    "DEFAULT_INTEGRITY_BY_LEVEL",
    "Finding",
    "coerce_severity",
    "coerce_confidence",
    "validate_required_text",
    "validate_position",
    "normalize_path",
    "schema_value",
    "enum_value",
    "finding_to_dict",
    "deterministic_finding_id",
    "make_finding",
    "make_finding_from_coordinates",
]
