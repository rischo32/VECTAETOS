#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Perimeter Registry

Role:
    Shared non-authoritative vocabulary registry for repository perimeter guards.

Boundary:
    This module defines stable labels used by guard diagnostics.

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
import enum
from collections.abc import Iterable
from typing import Any, TypeVar


EnumT = TypeVar("EnumT", bound=enum.Enum)


SCHEMA_VERSION = "perimeter-registry/1.0"
DEFAULT_CONTRACT_SCHEMA_VERSION = "1.0"


class PerimeterLevel(str, enum.Enum):
    LEVEL_0 = "Level 0"
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"
    LEVEL_4 = "Level 4"
    LEVEL_5 = "Level 5"


LEVEL_TITLES: dict[PerimeterLevel, str] = {
    PerimeterLevel.LEVEL_0: "Fundamental Repository Perimeter",
    PerimeterLevel.LEVEL_1: "Specialized Ontological Perimeter",
    PerimeterLevel.LEVEL_2: "Semantic / Ontological Vocabulary Perimeter",
    PerimeterLevel.LEVEL_3: "Code Behavior Perimeter",
    PerimeterLevel.LEVEL_4: "Bridge / Projection / Trace Perimeter",
    PerimeterLevel.LEVEL_5: "Runtime / Evidence / Release Perimeter",
}


class PerimeterScope(str, enum.Enum):
    FUNDAMENTAL_REPOSITORY = "fundamental_repository"
    SPECIALIZED_ONTOLOGICAL = "specialized_ontological"
    SEMANTIC_VOCABULARY = "semantic_vocabulary"
    CODE_BEHAVIOR = "code_behavior"
    BRIDGE_PROJECTION_TRACE = "bridge_projection_trace"
    RUNTIME_EVIDENCE_RELEASE = "runtime_evidence_release"


class LegacyScope(str, enum.Enum):
    """
    Backward-compatible scope labels used by older core modules.

    These labels are retained only for migration compatibility.
    New documentation should use PerimeterLevel plus PerimeterScope.
    """

    P0_REPOSITORY = "P0_repository"
    P1_SEMANTIC_VOCABULARY = "P1_semantic_vocabulary"
    P2_CODE_BEHAVIOR = "P2_code_behavior"
    P3_BRIDGE_PROJECTION_TRACE = "P3_bridge_projection_trace"
    P4_RUNTIME_EVIDENCE_RELEASE = "P4_runtime_evidence_release"


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


DRIFT_VECTOR_DESCRIPTIONS: dict[DriftVector, str] = {
    DriftVector.V0_AUTHORITY_INFLATION: "A lower layer claims authority, truth, ontology, validation, or decision power.",
    DriftVector.V1_UPWARD_MUTATION: "A downstream layer mutates or redefines a higher layer.",
    DriftVector.V2_AGENCY_INJECTION: "A non-agentic component becomes an agent, controller, planner, optimizer, recommender, or selector.",
    DriftVector.V3_FORBIDDEN_CONVERSION: "A protected boundary term becomes metric, score, threshold, parameter, fallback, error, or reward.",
    DriftVector.V4_EVIDENCE_OVERCLAIM: "Evidence level is overstated.",
    DriftVector.V5_NONDETERMINISM: "Behavior becomes time-dependent, random, environment-dependent, or non-reproducible.",
    DriftVector.V6_PATH_STATUS_LAUNDERING: "File meaning changes through path, name, status, relocation, or layer ambiguity.",
    DriftVector.V7_CONTRACT_DRIFT: "Contract diverges from anchor, rule id, schema version, or declared guard meaning.",
    DriftVector.V8_NEGATION_BLINDNESS: "Scanner punishes protective negation or ignores malicious negation.",
    DriftVector.V9_SILENCE_QE_COERCION: "QE, aporia, or silence is coerced into resolution, fallback, success, failure, or output pressure.",
    DriftVector.V10_TIMING_SIDE_CHANNEL: "Runtime behavior leaks or changes meaning through timing, ordering, hidden state, or external dependency.",
    DriftVector.V11_INTER_GUARD_COUPLING: "One guard consumes another guard's findings as authority or changes thresholds based on another guard.",
    DriftVector.V12_ONTOLOGY_CREEP: "Vocabulary shifts meaning without anchor, errata, or versioned migration.",
    DriftVector.V13_DEPENDENCY_SUPPLY_CHAIN: "Dependency is unpinned, unverified, network-installed, or changed without manifest trace.",
    DriftVector.V14_ANCHOR_INTEGRITY_DRIFT: "Protected anchor bytes differ from manifest or expected reviewed state.",
    DriftVector.V15_GUARD_RUNTIME_INTEGRITY: "Guard runtime, runner, workflow, or guard file identity differs from sealed expectation.",
}


class EvidenceClass(str, enum.Enum):
    E0_TEXT_CLAIM = "E0_text_claim"
    E1_STATIC_SCAN = "E1_static_scan"
    E2_AST_CONTRACT_COMPLIANCE = "E2_AST_contract_compliance"
    E3_DETERMINISTIC_TEST_SUITE = "E3_deterministic_test_suite"
    E4_EMPIRICAL_VALIDATION = "E4_empirical_validation"
    E5_EXTERNAL_REPLICATION = "E5_external_replication"
    E6_INDEPENDENT_AUDIT = "E6_independent_security_governance_audit"
    E7_FORMAL_GUARD_VERIFICATION = "E7_formal_verification_of_guard_properties"


EVIDENCE_CLASS_CLAIM_LIMITS: dict[EvidenceClass, str] = {
    EvidenceClass.E0_TEXT_CLAIM: "textual pattern observed",
    EvidenceClass.E1_STATIC_SCAN: "static repository scan finding",
    EvidenceClass.E2_AST_CONTRACT_COMPLIANCE: "Python AST / contract compliance finding",
    EvidenceClass.E3_DETERMINISTIC_TEST_SUITE: "deterministic test result",
    EvidenceClass.E4_EMPIRICAL_VALIDATION: "real-world validation event",
    EvidenceClass.E5_EXTERNAL_REPLICATION: "external replication event",
    EvidenceClass.E6_INDEPENDENT_AUDIT: "independent audit / governance review",
    EvidenceClass.E7_FORMAL_GUARD_VERIFICATION: "formal property verification of guard behavior",
}


class EnforcementMode(str, enum.Enum):
    ADVISORY = "advisory"
    REPORT = "report"
    STRICT = "strict"
    FAIL_CLOSED = "fail_closed"
    EXPERIMENTAL = "experimental"


class IntegrityPosture(str, enum.Enum):
    IMMUTABLE_ANCHOR = "immutable_anchor"
    GUARD_RUNTIME = "guard_runtime"
    SEMANTIC_READ_ONLY = "semantic_read_only"
    CODE_BEHAVIOR = "code_behavior"
    PROJECTION_READ_ONLY = "projection_read_only"
    EVIDENCE_POSTURE = "evidence_posture"
    RUNTIME_SANDBOX = "runtime_sandbox"
    INCIDENT_BOUNDARY = "incident_boundary"
    BYTE_INTEGRITY_READ_ONLY = "byte_integrity_read_only"
    CONTRACT_SCHEMA_READ_ONLY = "contract_schema_read_only"
    PATH_POLICY_READ_ONLY = "path_policy_read_only"
    ROLE_INFERENCE_READ_ONLY = "role_inference_read_only"
    ROLE_CAPABILITY_READ_ONLY = "role_capability_read_only"
    AST_SCAN_READ_ONLY = "ast_scan_read_only"


class Severity(str, enum.Enum):
    INFO = "INFO"
    WARN = "WARN"
    HARD = "HARD"
    BLOCKER = "BLOCKER"


SEVERITY_ORDER: dict[Severity, int] = {
    Severity.INFO: 0,
    Severity.WARN: 1,
    Severity.HARD: 2,
    Severity.BLOCKER: 3,
}


class Confidence(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


LEGACY_SCOPE_TO_LEVEL: dict[LegacyScope, PerimeterLevel] = {
    LegacyScope.P0_REPOSITORY: PerimeterLevel.LEVEL_0,
    LegacyScope.P1_SEMANTIC_VOCABULARY: PerimeterLevel.LEVEL_2,
    LegacyScope.P2_CODE_BEHAVIOR: PerimeterLevel.LEVEL_3,
    LegacyScope.P3_BRIDGE_PROJECTION_TRACE: PerimeterLevel.LEVEL_4,
    LegacyScope.P4_RUNTIME_EVIDENCE_RELEASE: PerimeterLevel.LEVEL_5,
}


LEGACY_SCOPE_TO_SCOPE: dict[LegacyScope, PerimeterScope] = {
    LegacyScope.P0_REPOSITORY: PerimeterScope.FUNDAMENTAL_REPOSITORY,
    LegacyScope.P1_SEMANTIC_VOCABULARY: PerimeterScope.SEMANTIC_VOCABULARY,
    LegacyScope.P2_CODE_BEHAVIOR: PerimeterScope.CODE_BEHAVIOR,
    LegacyScope.P3_BRIDGE_PROJECTION_TRACE: PerimeterScope.BRIDGE_PROJECTION_TRACE,
    LegacyScope.P4_RUNTIME_EVIDENCE_RELEASE: PerimeterScope.RUNTIME_EVIDENCE_RELEASE,
}


LEVEL_TO_SCOPE: dict[PerimeterLevel, PerimeterScope] = {
    PerimeterLevel.LEVEL_0: PerimeterScope.FUNDAMENTAL_REPOSITORY,
    PerimeterLevel.LEVEL_1: PerimeterScope.SPECIALIZED_ONTOLOGICAL,
    PerimeterLevel.LEVEL_2: PerimeterScope.SEMANTIC_VOCABULARY,
    PerimeterLevel.LEVEL_3: PerimeterScope.CODE_BEHAVIOR,
    PerimeterLevel.LEVEL_4: PerimeterScope.BRIDGE_PROJECTION_TRACE,
    PerimeterLevel.LEVEL_5: PerimeterScope.RUNTIME_EVIDENCE_RELEASE,
}


SCOPE_TO_LEVEL: dict[PerimeterScope, PerimeterLevel] = {
    scope: level for level, scope in LEVEL_TO_SCOPE.items()
}


def coerce_enum(enum_type: type[EnumT], value: Any, field_name: str) -> EnumT:
    """
    Normalize stable schema values into enum members.

    Accepted:
    - enum member, e.g. DriftVector.V3_FORBIDDEN_CONVERSION
    - enum value, e.g. "V3_forbidden_conversion"

    Rejected:
    - repr-like strings, e.g. "DriftVector.V3_FORBIDDEN_CONVERSION"
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
            f"Perimeter field {field_name!r} has invalid value {raw_value!r}; "
            f"allowed values: {allowed}"
        ) from exc


def enum_value(value: Any) -> Any:
    if isinstance(value, enum.Enum):
        return value.value
    return value


def coerce_level(value: PerimeterLevel | str) -> PerimeterLevel:
    return coerce_enum(PerimeterLevel, value, "level")


def coerce_scope(value: PerimeterScope | LegacyScope | str) -> PerimeterScope:
    if isinstance(value, LegacyScope):
        return LEGACY_SCOPE_TO_SCOPE[value]

    if isinstance(value, str):
        try:
            legacy = LegacyScope(value)
        except ValueError:
            pass
        else:
            return LEGACY_SCOPE_TO_SCOPE[legacy]

    return coerce_enum(PerimeterScope, value, "scope")


def coerce_legacy_scope(value: LegacyScope | str) -> LegacyScope:
    return coerce_enum(LegacyScope, value, "legacy_scope")


def coerce_drift_vector(value: DriftVector | str) -> DriftVector:
    return coerce_enum(DriftVector, value, "vector")


def coerce_evidence_class(value: EvidenceClass | str) -> EvidenceClass:
    return coerce_enum(EvidenceClass, value, "evidence_class")


def coerce_enforcement_mode(value: EnforcementMode | str) -> EnforcementMode:
    return coerce_enum(EnforcementMode, value, "enforcement_mode")


def coerce_integrity_posture(value: IntegrityPosture | str) -> IntegrityPosture:
    return coerce_enum(IntegrityPosture, value, "integrity_posture")


def level_from_scope(scope: PerimeterScope | LegacyScope | str) -> PerimeterLevel:
    if isinstance(scope, LegacyScope):
        return LEGACY_SCOPE_TO_LEVEL[scope]

    if isinstance(scope, str):
        try:
            legacy = LegacyScope(scope)
        except ValueError:
            pass
        else:
            return LEGACY_SCOPE_TO_LEVEL[legacy]

    normalized_scope = coerce_scope(scope)
    return SCOPE_TO_LEVEL[normalized_scope]


def default_scope_for_level(level: PerimeterLevel | str) -> PerimeterScope:
    normalized_level = coerce_level(level)
    return LEVEL_TO_SCOPE[normalized_level]


def level_label(level: PerimeterLevel | str) -> str:
    normalized = coerce_level(level)
    return f"{normalized.value} — {LEVEL_TITLES[normalized]}"


def evidence_claim_limit(evidence_class: EvidenceClass | str) -> str:
    normalized = coerce_evidence_class(evidence_class)
    return EVIDENCE_CLASS_CLAIM_LIMITS[normalized]


def drift_vector_description(vector: DriftVector | str) -> str:
    normalized = coerce_drift_vector(vector)
    return DRIFT_VECTOR_DESCRIPTIONS[normalized]


def normalize_vectors(vectors: Iterable[DriftVector | str]) -> tuple[DriftVector, ...]:
    normalized = tuple(coerce_drift_vector(vector) for vector in vectors)
    if not normalized:
        raise ValueError("At least one drift vector is required.")
    return normalized


@dataclasses.dataclass(frozen=True, slots=True)
class PerimeterCoordinates:
    """
    Non-authoritative guard finding coordinates.

    Coordinates classify where and how a repository-state finding occurred.
    They are not truth values and not ontology.
    """

    level: PerimeterLevel | str
    scope: PerimeterScope | LegacyScope | str
    vectors: tuple[DriftVector | str, ...]
    evidence_class: EvidenceClass | str
    enforcement_mode: EnforcementMode | str
    integrity_posture: IntegrityPosture | str

    def __post_init__(self) -> None:
        normalized_level = coerce_level(self.level)
        normalized_scope = coerce_scope(self.scope)

        object.__setattr__(self, "level", normalized_level)
        object.__setattr__(self, "scope", normalized_scope)
        object.__setattr__(self, "vectors", normalize_vectors(self.vectors))
        object.__setattr__(
            self,
            "evidence_class",
            coerce_evidence_class(self.evidence_class),
        )
        object.__setattr__(
            self,
            "enforcement_mode",
            coerce_enforcement_mode(self.enforcement_mode),
        )
        object.__setattr__(
            self,
            "integrity_posture",
            coerce_integrity_posture(self.integrity_posture),
        )

        expected_scope = default_scope_for_level(normalized_level)
        if normalized_scope != expected_scope:
            raise ValueError(
                "Perimeter level/scope mismatch: "
                f"level={normalized_level.value!r}, "
                f"scope={normalized_scope.value!r}, "
                f"expected_scope={expected_scope.value!r}"
            )


def coordinates_to_dict(coordinates: PerimeterCoordinates) -> dict[str, Any]:
    return {
        "level": enum_value(coordinates.level),
        "scope": enum_value(coordinates.scope),
        "vectors": [enum_value(vector) for vector in coordinates.vectors],
        "evidence_class": enum_value(coordinates.evidence_class),
        "enforcement_mode": enum_value(coordinates.enforcement_mode),
        "integrity_posture": enum_value(coordinates.integrity_posture),
    }


def make_coordinates(
    *,
    level: PerimeterLevel | str,
    scope: PerimeterScope | LegacyScope | str | None = None,
    vectors: Iterable[DriftVector | str],
    evidence_class: EvidenceClass | str,
    enforcement_mode: EnforcementMode | str,
    integrity_posture: IntegrityPosture | str,
) -> PerimeterCoordinates:
    normalized_level = coerce_level(level)
    normalized_scope = coerce_scope(scope) if scope is not None else default_scope_for_level(normalized_level)

    return PerimeterCoordinates(
        level=normalized_level,
        scope=normalized_scope,
        vectors=tuple(vectors),
        evidence_class=evidence_class,
        enforcement_mode=enforcement_mode,
        integrity_posture=integrity_posture,
    )


def compatibility_coordinates_from_legacy_scope(
    *,
    legacy_scope: LegacyScope | str,
    vector: DriftVector | str,
    evidence_class: EvidenceClass | str,
    enforcement_mode: EnforcementMode | str = EnforcementMode.STRICT,
    integrity_posture: IntegrityPosture | str = IntegrityPosture.SEMANTIC_READ_ONLY,
) -> PerimeterCoordinates:
    """
    Convert old P0–P4 scope coordinates into Level 0–5 coordinates.

    This is migration compatibility only.
    It must not be used to redefine the perimeter model.
    """

    normalized_legacy = coerce_legacy_scope(legacy_scope)

    return PerimeterCoordinates(
        level=LEGACY_SCOPE_TO_LEVEL[normalized_legacy],
        scope=LEGACY_SCOPE_TO_SCOPE[normalized_legacy],
        vectors=(coerce_drift_vector(vector),),
        evidence_class=coerce_evidence_class(evidence_class),
        enforcement_mode=coerce_enforcement_mode(enforcement_mode),
        integrity_posture=coerce_integrity_posture(integrity_posture),
    )


SAFE_PASS = "PASS: No configured blocker was detected within the declared perimeter."
SAFE_FAIL = "FAIL: Configured blocker detected within declared repository perimeter."
SAFE_INFRA_FAIL = "FAIL: Guard infrastructure error; confidence unavailable."

FORBIDDEN_REPORT_CLAIMS: tuple[str, ...] = (
    "ontology preserved",
    "truth proven",
    "truth validated",
    "semantic correctness proven",
    "vectaetos is safe",
    "deployment ready",
    "deployment validated",
    "safety validated",
    "guard-certified ontology",
    "hash proves meaning",
    "hash-proven meaning",
    "signature proves ontology",
    "manifest-certified ontology",
    "ci proves safety",
)


SAFE_WORDING_REGISTRY: dict[str, str] = {
    "validated safe": "no configured blocker detected within declared perimeter",
    "safety validated": "no configured blocker detected within declared perimeter",
    "ontology preserved": "protected anchor bytes matched configured manifest",
    "canonical integrity proven": "configured byte-integrity check passed",
    "hash proves meaning": "hash matched configured byte manifest",
    "hash-proven meaning": "hash matched configured byte manifest",
    "signature proves ontology": "signature verified configured attestation",
    "manifest-certified ontology": "manifest entry matched configured repository state",
    "ek certified validity": "EK observable recorded structural trace",
    "ci proves safety": "CI perimeter checks passed",
}


def safe_replacement_for_claim(claim: str) -> str | None:
    lowered = claim.casefold().strip()
    return SAFE_WORDING_REGISTRY.get(lowered)


def contains_forbidden_report_claim(text: str) -> bool:
    lowered = text.casefold()
    return any(claim in lowered for claim in FORBIDDEN_REPORT_CLAIMS)


def assert_non_authoritative_flags(
    *,
    ontology_authority: bool,
    auto_fix_allowed: bool,
) -> None:
    if ontology_authority:
        raise ValueError("ontology_authority must be false for guard diagnostics.")

    if auto_fix_allowed:
        raise ValueError("auto_fix_allowed must be false by default for guard diagnostics.")


__all__ = [
    "SCHEMA_VERSION",
    "DEFAULT_CONTRACT_SCHEMA_VERSION",
    "PerimeterLevel",
    "LEVEL_TITLES",
    "PerimeterScope",
    "LegacyScope",
    "DriftVector",
    "DRIFT_VECTOR_DESCRIPTIONS",
    "EvidenceClass",
    "EVIDENCE_CLASS_CLAIM_LIMITS",
    "EnforcementMode",
    "IntegrityPosture",
    "Severity",
    "SEVERITY_ORDER",
    "Confidence",
    "LEGACY_SCOPE_TO_LEVEL",
    "LEGACY_SCOPE_TO_SCOPE",
    "LEVEL_TO_SCOPE",
    "SCOPE_TO_LEVEL",
    "PerimeterCoordinates",
    "coerce_enum",
    "enum_value",
    "coerce_level",
    "coerce_scope",
    "coerce_legacy_scope",
    "coerce_drift_vector",
    "coerce_evidence_class",
    "coerce_enforcement_mode",
    "coerce_integrity_posture",
    "level_from_scope",
    "default_scope_for_level",
    "level_label",
    "evidence_claim_limit",
    "drift_vector_description",
    "normalize_vectors",
    "coordinates_to_dict",
    "make_coordinates",
    "compatibility_coordinates_from_legacy_scope",
    "SAFE_PASS",
    "SAFE_FAIL",
    "SAFE_INFRA_FAIL",
    "FORBIDDEN_REPORT_CLAIMS",
    "SAFE_WORDING_REGISTRY",
    "safe_replacement_for_claim",
    "contains_forbidden_report_claim",
    "assert_non_authoritative_flags",
]
