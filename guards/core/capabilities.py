#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Capability Core

Role:
    Shared role capability matrix for repository perimeter guards.

Boundary:
    Capabilities describe what a code role is allowed to do inside the
    repository perimeter.

    They do not define ontology, truth, safety, deployment validity,
    Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

    Capability denial is a repository-state diagnostic only.
    It is not metaphysical proof.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import enum
from collections.abc import Mapping
from pathlib import Path
from typing import Any

try:
    from guards.core.findings import (
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Severity,
        make_finding,
    )
    from guards.core.perimeter import EnforcementMode
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from findings import (  # type: ignore
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Severity,
        make_finding,
    )
    from perimeter import EnforcementMode  # type: ignore


SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"
DEFAULT_GUARD_ID = "GUARD-03"
DEFAULT_GUARD_FILE = "guards/vectaetos_code_behavior_audit.py"


class CodeRole(str, enum.Enum):
    GUARD = "guard"
    GIT_GUARD = "git_guard"
    REPORT_WRITER = "report_writer"
    VORTEX = "vortex"
    AUDIT_ADAPTER = "audit_adapter"
    CONTRACT_TOOL = "contract_tool"
    TEST = "test"
    SCRIPT = "script"
    UNKNOWN = "unknown"


class CapabilityName(str, enum.Enum):
    NETWORK = "network"
    SUBPROCESS = "subprocess"
    FILE_WRITE = "file_write"
    RANDOMNESS = "randomness"
    SELECTION_FUNCTIONS = "selection_functions"
    ONTOLOGY_ASSIGNMENTS = "ontology_assignments"


CAPABILITY_TO_VECTOR: dict[CapabilityName, DriftVector] = {
    CapabilityName.NETWORK: DriftVector.V2_AGENCY_INJECTION,
    CapabilityName.SUBPROCESS: DriftVector.V2_AGENCY_INJECTION,
    CapabilityName.FILE_WRITE: DriftVector.V1_UPWARD_MUTATION,
    CapabilityName.RANDOMNESS: DriftVector.V5_NONDETERMINISM,
    CapabilityName.SELECTION_FUNCTIONS: DriftVector.V2_AGENCY_INJECTION,
    CapabilityName.ONTOLOGY_ASSIGNMENTS: DriftVector.V12_ONTOLOGY_CREEP,
}


CAPABILITY_TO_OBJECT: dict[CapabilityName, str] = {
    CapabilityName.NETWORK: "network",
    CapabilityName.SUBPROCESS: "subprocess",
    CapabilityName.FILE_WRITE: "file_write",
    CapabilityName.RANDOMNESS: "randomness",
    CapabilityName.SELECTION_FUNCTIONS: "selection_functions",
    CapabilityName.ONTOLOGY_ASSIGNMENTS: "ontology_assignments",
}


@dataclasses.dataclass(frozen=True, slots=True)
class CapabilityPolicy:
    role: CodeRole
    allow_network: bool = False
    allow_subprocess: bool = False
    allow_file_write: bool = False
    allow_randomness: bool = False
    allow_selection_functions: bool = True
    protect_ontology_assignments: bool = True
    subprocess_allowlist: tuple[str, ...] = ()
    file_write_allowlist: tuple[str, ...] = ()
    notes: str | None = None


DEFAULT_CAPABILITY_MATRIX: dict[CodeRole, CapabilityPolicy] = {
    CodeRole.GUARD: CapabilityPolicy(
        role=CodeRole.GUARD,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=False,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        notes="ordinary read-only guard",
    ),
    CodeRole.GIT_GUARD: CapabilityPolicy(
        role=CodeRole.GIT_GUARD,
        allow_network=False,
        allow_subprocess=True,
        allow_file_write=False,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        subprocess_allowlist=("git",),
        notes="guard allowed to call git only for repository inspection",
    ),
    CodeRole.REPORT_WRITER: CapabilityPolicy(
        role=CodeRole.REPORT_WRITER,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=True,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        file_write_allowlist=("reports/", "artifacts/", ".guard_reports/"),
        notes="report writer may write explicit report artifacts only",
    ),
    CodeRole.VORTEX: CapabilityPolicy(
        role=CodeRole.VORTEX,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=False,
        allow_randomness=False,
        allow_selection_functions=False,
        protect_ontology_assignments=True,
        notes="vortex must not select, rank, optimize, or use uncontrolled IO",
    ),
    CodeRole.AUDIT_ADAPTER: CapabilityPolicy(
        role=CodeRole.AUDIT_ADAPTER,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=True,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        file_write_allowlist=("audit/", "reports/", "artifacts/", ".guard_reports/"),
        notes="audit adapter may write audit/report artifacts, not alter ontology",
    ),
    CodeRole.CONTRACT_TOOL: CapabilityPolicy(
        role=CodeRole.CONTRACT_TOOL,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=True,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        file_write_allowlist=("contracts/", "reports/", "artifacts/", ".guard_reports/"),
        notes="contract helper may generate files only under explicit human invocation",
    ),
    CodeRole.TEST: CapabilityPolicy(
        role=CodeRole.TEST,
        allow_network=False,
        allow_subprocess=True,
        allow_file_write=True,
        allow_randomness=True,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        notes="tests may exercise behavior but must not become runtime authority",
    ),
    CodeRole.SCRIPT: CapabilityPolicy(
        role=CodeRole.SCRIPT,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=False,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        notes="generic script defaults to restrictive posture",
    ),
    CodeRole.UNKNOWN: CapabilityPolicy(
        role=CodeRole.UNKNOWN,
        allow_network=False,
        allow_subprocess=False,
        allow_file_write=False,
        allow_randomness=False,
        allow_selection_functions=True,
        protect_ontology_assignments=True,
        notes="unknown protected role fails closed in strict audits",
    ),
}


CAPABILITY_ATTRS: dict[CapabilityName, str] = {
    CapabilityName.NETWORK: "allow_network",
    CapabilityName.SUBPROCESS: "allow_subprocess",
    CapabilityName.FILE_WRITE: "allow_file_write",
    CapabilityName.RANDOMNESS: "allow_randomness",
    CapabilityName.SELECTION_FUNCTIONS: "allow_selection_functions",
    CapabilityName.ONTOLOGY_ASSIGNMENTS: "protect_ontology_assignments",
}


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def coerce_role(value: CodeRole | str) -> CodeRole:
    if isinstance(value, CodeRole):
        return value

    raw = str(value).strip().replace("-", "_").lower()
    try:
        return CodeRole(raw)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in CodeRole)
        raise ValueError(f"invalid code role {value!r}; allowed values: {allowed}") from exc


def coerce_capability(value: CapabilityName | str) -> CapabilityName:
    if isinstance(value, CapabilityName):
        return value

    raw = str(value).strip().replace("-", "_").lower()
    try:
        return CapabilityName(raw)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in CapabilityName)
        raise ValueError(
            f"invalid capability {value!r}; allowed values: {allowed}"
        ) from exc


def get_capability_policy(
    role: CodeRole | str,
    *,
    matrix: Mapping[CodeRole, CapabilityPolicy] | None = None,
) -> CapabilityPolicy:
    selected_matrix = matrix or DEFAULT_CAPABILITY_MATRIX
    normalized = coerce_role(role)
    return selected_matrix.get(normalized, selected_matrix[CodeRole.UNKNOWN])


def capability_allowed(policy: CapabilityPolicy, capability: CapabilityName | str) -> bool:
    normalized = coerce_capability(capability)
    attr = CAPABILITY_ATTRS[normalized]
    value = getattr(policy, attr)

    if normalized == CapabilityName.ONTOLOGY_ASSIGNMENTS:
        # The policy field means "protect ontology assignments".
        # If protection is enabled, ontology-facing assignment is NOT allowed.
        return not bool(value)

    return bool(value)


def allowlist_matches(observed_pattern: str | None, allowlist: tuple[str, ...]) -> bool:
    if not allowlist:
        return True

    if not observed_pattern:
        return False

    lowered = observed_pattern.casefold()
    return any(item.casefold() in lowered for item in allowlist)


def capability_allowlist_ok(
    *,
    policy: CapabilityPolicy,
    capability: CapabilityName | str,
    observed_pattern: str | None,
) -> bool:
    normalized = coerce_capability(capability)

    if normalized == CapabilityName.SUBPROCESS:
        return allowlist_matches(observed_pattern, policy.subprocess_allowlist)

    if normalized == CapabilityName.FILE_WRITE:
        return allowlist_matches(observed_pattern, policy.file_write_allowlist)

    return True


def capability_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    role: CodeRole | str,
    capability: CapabilityName | str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    severity: Severity | str = Severity.BLOCKER,
    confidence: Confidence | str = Confidence.HIGH,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
    observed_pattern: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    normalized_role = coerce_role(role)
    normalized_capability = coerce_capability(capability)

    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=PerimeterLevel.LEVEL_3,
        scope=PerimeterScope.CODE_BEHAVIOR,
        vector=CAPABILITY_TO_VECTOR[normalized_capability],
        severity=severity,
        confidence=confidence,
        path=normalize_repo_path(path),
        message=message,
        role=normalized_role.value,
        protected_object=CAPABILITY_TO_OBJECT[normalized_capability],
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E2_AST_CONTRACT_COMPLIANCE,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.ROLE_CAPABILITY_READ_ONLY,
        safer_form=safer_form,
    )


def validate_capability_use(
    *,
    path: Path | str,
    role: CodeRole | str,
    capability: CapabilityName | str,
    observed_pattern: str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
) -> list[Finding]:
    policy = get_capability_policy(role)
    normalized_capability = coerce_capability(capability)
    normalized_role = coerce_role(role)

    if capability_allowed(policy, normalized_capability) and capability_allowlist_ok(
        policy=policy,
        capability=normalized_capability,
        observed_pattern=observed_pattern,
    ):
        return []

    if capability_allowed(policy, normalized_capability):
        message = (
            f"Role {normalized_role.value!r} may use capability "
            f"{normalized_capability.value!r}, but observed use is outside the declared allowlist."
        )
        safer_form = "Keep allowed behavior within declared bounded paths or commands."
    else:
        message = (
            f"Role {normalized_role.value!r} is not allowed to use "
            f"capability {normalized_capability.value!r}."
        )
        safer_form = "Move behavior behind explicit bounded contract or keep guard read-only."

    return [
        capability_finding(
            rule_id=f"CAPABILITY-DENIED-{normalized_capability.value.upper()}",
            path=path,
            role=normalized_role,
            capability=normalized_capability,
            message=message,
            observed_pattern=observed_pattern,
            guard_id=guard_id,
            guard_file=guard_file,
            safer_form=safer_form,
        )
    ]


def policy_to_dict(policy: CapabilityPolicy) -> dict[str, Any]:
    return {
        "role": policy.role.value,
        "allow_network": policy.allow_network,
        "allow_subprocess": policy.allow_subprocess,
        "allow_file_write": policy.allow_file_write,
        "allow_randomness": policy.allow_randomness,
        "allow_selection_functions": policy.allow_selection_functions,
        "protect_ontology_assignments": policy.protect_ontology_assignments,
        "subprocess_allowlist": list(policy.subprocess_allowlist),
        "file_write_allowlist": list(policy.file_write_allowlist),
        "notes": policy.notes,
    }


def matrix_to_dict(
    matrix: Mapping[CodeRole, CapabilityPolicy] | None = None,
) -> dict[str, dict[str, Any]]:
    selected_matrix = matrix or DEFAULT_CAPABILITY_MATRIX
    return {
        role.value: policy_to_dict(policy)
        for role, policy in sorted(selected_matrix.items(), key=lambda item: item[0].value)
    }


__all__ = [
    "SUPPORTED_CONTRACT_SCHEMA_VERSION",
    "DEFAULT_GUARD_ID",
    "DEFAULT_GUARD_FILE",
    "CodeRole",
    "CapabilityName",
    "CAPABILITY_TO_VECTOR",
    "CAPABILITY_TO_OBJECT",
    "CapabilityPolicy",
    "DEFAULT_CAPABILITY_MATRIX",
    "CAPABILITY_ATTRS",
    "normalize_repo_path",
    "coerce_role",
    "coerce_capability",
    "get_capability_policy",
    "capability_allowed",
    "allowlist_matches",
    "capability_allowlist_ok",
    "capability_finding",
    "validate_capability_use",
    "policy_to_dict",
    "matrix_to_dict",
]
