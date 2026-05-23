#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Role Core

Role:
    Shared code-role declaration and inference helpers for repository perimeter
    guards.

Boundary:
    Role inference is a repository diagnostic helper only.

    It does not grant authority, define ontology, validate safety, authorize
    deployment, mutate files, or decide which layer is metaphysically valid.

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
        Scope,
        Severity,
        make_finding,
    )
    from guards.core.paths import PathRole, describe_path
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from capabilities import CodeRole  # type: ignore
    from findings import (  # type: ignore
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        Scope,
        Severity,
        make_finding,
    )
    from paths import PathRole, describe_path  # type: ignore


SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"
DEFAULT_GUARD_ID = "GUARD-03"
DEFAULT_GUARD_FILE = "guards/vectaetos_code_behavior_audit.py"

ROLE_DECLARATION_PATTERN = re.compile(
    r"^\s*(?:#\s*)?(?:VECTAETOS_ROLE|Role)\s*:\s*([a-zA-Z0-9_\-]+)\s*$",
    flags=re.IGNORECASE,
)


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


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

        raw_role = match.group(1).strip().replace("-", "_").lower()
        try:
            return CodeRole(raw_role)
        except ValueError:
            return CodeRole.UNKNOWN

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

    if "vortex" in lowered:
        return CodeRole.VORTEX

    if "audit" in lowered or "ek_" in lowered or "epistemic_cryptography" in lowered:
        return CodeRole.AUDIT_ADAPTER

    if "report" in lowered:
        return CodeRole.REPORT_WRITER

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
        if isinstance(explicit_role, CodeRole):
            return explicit_role
        try:
            return CodeRole(str(explicit_role))
        except ValueError:
            return CodeRole.UNKNOWN

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
    severity: Severity | str = Severity.WARN.value,
    confidence: Confidence | str = Confidence.MEDIUM.value,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
    observed_pattern: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    normalized_role = role if isinstance(role, CodeRole) else CodeRole(str(role))

    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        scope=Scope.P2_CODE_BEHAVIOR.value,
        vector=DriftVector.V7_CONTRACT_DRIFT.value,
        severity=severity.value if isinstance(severity, Severity) else severity,
        confidence=confidence.value if isinstance(confidence, Confidence) else confidence,
        path=normalize_repo_path(path),
        message=message,
        role=normalized_role.value,
        protected_object="code_role",
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E2_AST_CONTRACT_COMPLIANCE.value,
        safer_form=safer_form,
        integrity_posture="role_inference_read_only",
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
