#!/usr/bin/env python3#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Role Core

Role:
    Shared code-role declaration and inference helpers for repository perimeter
    guards.

Boundary:
    Role inference is a repository diagnostic helper only.

    It does not grant authority.
    It does not define ontology.
    It does not validate safety.
    It does not authorize deployment.
    It does not mutate files.
    It does not decide which layer is metaphysically valid.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from guards.core.capabilities import CodeRole
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
    from guards.core.paths import PathRole, describe_path
except ModuleNotFoundError:
    from capabilities import CodeRole  # type: ignore
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
    from paths import PathRole, describe_path  # type: ignore


SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"
DEFAULT_GUARD_ID = "GUARD-03"
DEFAULT_GUARD_FILE = "guards/vectaetos_code_behavior_audit.py"

ROLE_DECLARATION_PATTERN = re.compile(
    r"^\s*(?:#\s*)?(?:VECTAETOS_ROLE|Role)\s*:\s*([a-zA-Z0-9_\-]+)\s*$",
    flags=re.IGNORECASE,
)

ROLE_FILE_NAME_HINTS: tuple[tuple[str, CodeRole], ...] = (
    ("vortex", CodeRole.VORTEX),
    ("epistemic_cryptography", CodeRole.AUDIT_ADAPTER),
    ("ek_", CodeRole.AUDIT_ADAPTER),
    ("audit", CodeRole.AUDIT_ADAPTER),
    ("report", CodeRole.REPORT_WRITER),
    ("contract", CodeRole.CONTRACT_TOOL),
    ("git", CodeRole.GIT_GUARD),
)


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def coerce_code_role(value: CodeRole | str) -> CodeRole:
    if isinstance(value, CodeRole):
        return value

    raw = str(value).strip().replace("-", "_").lower()
    try:
        return CodeRole(raw)
    except ValueError:
        return CodeRole.UNKNOWN


def parse_declared_role(text: str, *, max_lines: int = 80) -> CodeRole | None:
    """
    Parse an explicit role declaration near the top of a source file.

    Supported forms:

    ```text
    # VECTAETOS_ROLE: guard
    Role: vortex
    ```
    """

    for line in text.splitlines()[:max_lines]:
        match = ROLE_DECLARATION_PATTERN.match(line)
        if not match:
            continue

        raw_role = match.group(1).strip()
        return coerce_code_role(raw_role)

    return None


def infer_role_from_path(path: Path | str) -> CodeRole:
    repo_path = normalize_repo_path(path)
    info = describe_path(repo_path)
    lowered = repo_path.casefold()

    if info.role == PathRole.GUARD_CORE:
        return CodeRole.GUARD

    if info.role == PathRole.GUARD:
        if "git" in lowered:
            return CodeRole.GIT_GUARD
        return CodeRole.GUARD

    if info.role in {PathRole.TEST, PathRole.FIXTURE}:
        return CodeRole.TEST

    if info.role == PathRole.CONTRACT:
        return CodeRole.CONTRACT_TOOL

    for needle, role in ROLE_FILE_NAME_HINTS:
        if needle in lowered:
            return role

    if info.role == PathRole.SOURCE:
        return CodeRole.SCRIPT

    return CodeRole.UNKNOWN


def resolve_code_role(
    *,
    path: Path | str,
    text: str | None = None,
    explicit_role: CodeRole | str | None = None,
) -> CodeRole:
    if explicit_role is not None:
        return coerce_code_role(explicit_role)

    if text is not None:
        declared = parse_declared_role(text)
        if declared is not None:
            return declared

    return infer_role_from_path(path)


def role_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    role: CodeRole | str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    severity: Severity | str = Severity.WARN,
    confidence: Confidence | str = Confidence.MEDIUM,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
    observed_pattern: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    normalized_role = coerce_code_role(role)

    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=PerimeterLevel.LEVEL_3,
        scope=PerimeterScope.CODE_BEHAVIOR,
        vector=DriftVector.V7_CONTRACT_DRIFT,
        severity=severity,
        confidence=confidence,
        path=normalize_repo_path(path),
        message=message,
        role=normalized_role.value,
        protected_object="code_role",
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E2_AST_CONTRACT_COMPLIANCE,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.ROLE_INFERENCE_READ_ONLY,
        safer_form=safer_form,
    )


def validate_role_known(
    *,
    path: Path | str,
    role: CodeRole,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
) -> list[Finding]:
    if role != CodeRole.UNKNOWN:
        return []

    return [
        role_finding(
            rule_id="ROLE-UNKNOWN",
            path=path,
            role=role,
            message="Code role could not be resolved for protected-path audit.",
            guard_id=guard_id,
            guard_file=guard_file,
            safer_form="Add explicit '# VECTAETOS_ROLE: <role>' declaration or path policy.",
        )
    ]


def role_to_dict(role: CodeRole | str) -> dict[str, str]:
    normalized = coerce_code_role(role)
    return {
        "role": normalized.value,
        "status": "known" if normalized != CodeRole.UNKNOWN else "unknown",
    }


__all__ = [
    "SUPPORTED_CONTRACT_SCHEMA_VERSION",
    "DEFAULT_GUARD_ID",
    "DEFAULT_GUARD_FILE",
    "ROLE_DECLARATION_PATTERN",
    "ROLE_FILE_NAME_HINTS",
    "normalize_repo_path",
    "coerce_code_role",
    "parse_declared_role",
    "infer_role_from_path",
    "resolve_code_role",
    "role_finding",
    "validate_role_known",
    "role_to_dict",
]
