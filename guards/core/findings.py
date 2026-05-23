#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Finding Model

Role:
    Shared non-authoritative finding schema for repository perimeter guards.

Boundary:
    This module does not define ontology, truth, safety, deployment validity,
    Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import enum
import hashlib
from pathlib import Path
from typing import Any, TypeVar


SCHEMA_BASELINE = "perimeter-finding-schema/1.0"
DEFAULT_CONTRACT_SCHEMA_VERSION = "1.0"

EnumT = TypeVar("EnumT", bound=enum.Enum)


class Severity(str, enum.Enum):
    INFO = "INFO"
    WARN = "WARN"
    HARD = "HARD"
    BLOCKER = "BLOCKER"


class Confidence(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EvidenceClass(str, enum.Enum):
    E0_TEXT_CLAIM = "E0_text_claim"
    E1_STATIC_SCAN = "E1_static_scan"
    E2_AST_CONTRACT_COMPLIANCE = "E2_AST_contract_compliance"
    E3_DETERMINISTIC_TEST_SUITE = "E3_deterministic_test_suite"
    E4_EMPIRICAL_VALIDATION = "E4_empirical_validation"
    E5_EXTERNAL_REPLICATION = "E5_external_replication"
    E6_INDEPENDENT_AUDIT = "E6_independent_security_governance_audit"
    E7_FORMAL_GUARD_VERIFICATION = "E7_formal_verification_of_guard_properties"


class DriftVector(str, enum.Enum):
    V0_AUTHORITY_INFLATION = "V0_authority_inflation"
    V1_UPWARD_MUTATION = "V1_upward_mutation"
    V2_AGENCY_INJECTION = "V2_agency_injection"
    V3_FORBIDDEN_CONVERSION = "V3_forbidden_conversion"
    V4_EVIDENCE_OVERCLAIM = "V4_evidence_overclaim"
    V5_NONDETERMINISM = "V5_nondeterminism"
    V6_PATH_STATUS_LAUNDERING = "V6_path_status_laundering"
    V7_CONTRACT_DRIFT = "V7_contract_drift"
    V8_NEGATION_BLINDNESS = "V8_negation_blindness"
    V9_SILENCE_QE_COERCION = "V9_silence_qe_coercion"
    V10_TIMING_SIDE_CHANNEL = "V10_timing_side_channel"
    V11_INTER_GUARD_COUPLING = "V11_inter_guard_coupling"
    V12_ONTOLOGY_CREEP = "V12_ontology_creep"
    V13_DEPENDENCY_SUPPLY_CHAIN = "V13_dependency_supply_chain"
    V14_ANCHOR_INTEGRITY_DRIFT = "V14_anchor_integrity_drift"
    V15_GUARD_RUNTIME_INTEGRITY = "V15_guard_runtime_integrity"


class Scope(str, enum.Enum):
    P0_REPOSITORY = "P0_repository"
    P1_SEMANTIC_VOCABULARY = "P1_semantic_vocabulary"
    P2_CODE_BEHAVIOR = "P2_code_behavior"
    P3_BRIDGE_PROJECTION_TRACE = "P3_bridge_projection_trace"
    P4_RUNTIME_EVIDENCE_RELEASE = "P4_runtime_evidence_release"


SEVERITY_ORDER: dict[Severity, int] = {
    Severity.INFO: 0,
    Severity.WARN: 1,
    Severity.HARD: 2,
    Severity.BLOCKER: 3,
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
    scope: Scope | str
    vector: DriftVector | str
    severity: Severity | str
    confidence: Confidence | str
    path: Path | str
    message: str

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
    enforcement_mode: str | None = None
    integrity_posture: str | None = None
    anchor_ref: str | None = None
    contract_ref: str | None = None
    safer_form: str | None = None
    ontology_authority: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        normalized_path = normalize_path(self.path)

        object.__setattr__(self, "path", normalized_path)
        object.__setattr__(
            self,
            "severity",
            coerce_enum(Severity, self.severity, "severity"),
        )
        object.__setattr__(
            self,
            "confidence",
            coerce_enum(Confidence, self.confidence, "confidence"),
        )
        object.__setattr__(
            self,
            "scope",
            coerce_enum(Scope, self.scope, "scope"),
        )
        object.__setattr__(
            self,
            "vector",
            coerce_enum(DriftVector, self.vector, "vector"),
        )

        if self.evidence_class_allowed is not None:
            object.__setattr__(
                self,
                "evidence_class_allowed",
                coerce_enum(
                    EvidenceClass,
                    self.evidence_class_allowed,
                    "evidence_class_allowed",
                ),
            )

        if self.evidence_class_claimed is not None:
            object.__setattr__(
                self,
                "evidence_class_claimed",
                coerce_enum(
                    EvidenceClass,
                    self.evidence_class_claimed,
                    "evidence_class_claimed",
                ),
            )

        validate_required_text("guard_id", self.guard_id)
        validate_required_text("guard_file", self.guard_file)
        validate_required_text("rule_id", self.rule_id)
        validate_required_text("contract_schema_version", self.contract_schema_version)
        validate_required_text("message", self.message)

        if self.ontology_authority:
            raise ValueError("Finding invariant violation: ontology_authority must be false.")

        if self.auto_fix_allowed:
            raise ValueError(
                "Finding invariant violation: auto_fix_allowed must be false by default."
            )

        if self.line is not None and self.line < 1:
            raise ValueError("Finding line must be >= 1 when provided.")

        if self.end_line is not None and self.end_line < 1:
            raise ValueError("Finding end_line must be >= 1 when provided.")

        if self.id is None:
            object.__setattr__(self, "id", deterministic_finding_id(self))


def validate_required_text(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Finding field {field_name!r} is required and must be non-empty."
        )


def coerce_enum(enum_type: type[EnumT], value: Any, field_name: str) -> EnumT:
    """
    Normalize enum values accepted by guard code.

    Accepted:
    - enum member, e.g. Severity.BLOCKER
    - schema value, e.g. "BLOCKER"

    Not accepted:
    - repr-like strings such as "Severity.BLOCKER"
    """

    if isinstance(value, enum_type):
        return value

    if isinstance(value, enum.Enum):
        raw_value = value.value
    else:
        raw_value = value

    try:
        return enum_type(str(raw_value))
    except ValueError as exc:
        allowed = ", ".join(str(item.value) for item in enum_type)
        raise ValueError(
            f"Finding field {field_name!r} has invalid value {raw_value!r}; "
            f"allowed values: {allowed}"
        ) from exc


def normalize_path(path: Path | str) -> str:
    return str(path).replace("\\", "/").strip()


def enum_value(value: Any) -> Any:
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, Path):
        return normalize_path(value)
    return value


def finding_to_dict(finding: Finding) -> dict[str, Any]:
    data = dataclasses.asdict(finding)
    return {key: enum_value(value) for key, value in data.items()}


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
            str(enum_value(finding.scope)),
            str(enum_value(finding.vector)),
            str(finding.path),
            str(finding.line or ""),
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
    scope: Scope | str,
    vector: DriftVector | str,
    severity: Severity | str,
    confidence: Confidence | str,
    path: Path | str,
    message: str,
    contract_schema_version: str = DEFAULT_CONTRACT_SCHEMA_VERSION,
    **kwargs: Any,
) -> Finding:
    return Finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        scope=scope,
        vector=vector,
        severity=severity,
        confidence=confidence,
        path=path,
        message=message,
        **kwargs,
    )
