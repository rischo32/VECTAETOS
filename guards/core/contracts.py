#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Contract Core

Role:
    Shared read-only contract loading and validation helpers for repository
    perimeter guards.

Boundary:
    Contracts project anchor constraints into machine-readable guard rules.

    This module does not define ontology, truth, safety, deployment validity,
    Φ, K(Φ), κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

    Invalid contracts produce repository-state diagnostics only.
    They are not metaphysical proof.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

try:
    from guards.core.findings import (
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        Scope,
        Severity,
        make_finding,
    )
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from findings import (  # type: ignore
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        Scope,
        Severity,
        make_finding,
    )


SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"
DEFAULT_CONTRACT_ROLE = "perimeter_contract"
DEFAULT_CONTRACT_GUARD_ID = "GUARD-22"
DEFAULT_CONTRACT_GUARD_FILE = "guards/contract_traceability_guard.py"

ALLOWED_ENFORCEMENT_MODES = frozenset(
    {
        "advisory",
        "report",
        "strict",
        "fail_closed",
        "experimental",
    }
)


class ContractError(RuntimeError):
    """
    Contract infrastructure error.

    This exception concerns repository contract integrity only.
    It is not ontology.
    """


@dataclasses.dataclass(frozen=True, slots=True)
class ContractRule:
    id: str
    anchor_ref: str
    vector: DriftVector
    scope: Scope
    evidence_class_allowed: EvidenceClass
    enforcement_mode: str
    severity: Severity
    message: str

    protected_object: str | None = None
    pattern: str | None = None
    forbidden_conversion: str | None = None
    safer_form: str | None = None
    role: str | None = None
    integrity_posture: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class ContractDocument:
    path: str
    schema_version: str
    contract_role: str
    rules: tuple[ContractRule, ...]

    def by_rule_id(self) -> dict[str, ContractRule]:
        return {rule.id: rule for rule in self.rules}


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def ensure_required_text(raw: Mapping[str, Any], key: str, *, context: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{context} missing required non-empty text field: {key}")
    return value.strip()


def optional_text(raw: Mapping[str, Any], key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ContractError(f"optional field {key!r} must be text when provided")
    stripped = value.strip()
    return stripped or None


def coerce_scope(value: str, *, context: str) -> Scope:
    try:
        return Scope(value)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in Scope)
        raise ContractError(
            f"{context} has invalid scope {value!r}; allowed values: {allowed}"
        ) from exc


def coerce_vector(value: str, *, context: str) -> DriftVector:
    try:
        return DriftVector(value)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in DriftVector)
        raise ContractError(
            f"{context} has invalid vector {value!r}; allowed values: {allowed}"
        ) from exc


def coerce_evidence_class(value: str, *, context: str) -> EvidenceClass:
    try:
        return EvidenceClass(value)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in EvidenceClass)
        raise ContractError(
            f"{context} has invalid evidence_class_allowed {value!r}; "
            f"allowed values: {allowed}"
        ) from exc


def coerce_severity(value: str, *, context: str) -> Severity:
    try:
        return Severity(value)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in Severity)
        raise ContractError(
            f"{context} has invalid severity {value!r}; allowed values: {allowed}"
        ) from exc


def validate_enforcement_mode(value: str, *, context: str) -> str:
    if value not in ALLOWED_ENFORCEMENT_MODES:
        allowed = ", ".join(sorted(ALLOWED_ENFORCEMENT_MODES))
        raise ContractError(
            f"{context} has invalid enforcement_mode {value!r}; allowed values: {allowed}"
        )
    return value


def rule_from_mapping(raw: Mapping[str, Any], *, index: int, contract_path: str) -> ContractRule:
    context = f"{contract_path}:rules[{index}]"

    rule_id = ensure_required_text(raw, "id", context=context)
    anchor_ref = ensure_required_text(raw, "anchor_ref", context=context)
    vector = coerce_vector(ensure_required_text(raw, "vector", context=context), context=context)
    scope = coerce_scope(ensure_required_text(raw, "scope", context=context), context=context)
    evidence = coerce_evidence_class(
        ensure_required_text(raw, "evidence_class_allowed", context=context),
        context=context,
    )
    enforcement_mode = validate_enforcement_mode(
        ensure_required_text(raw, "enforcement_mode", context=context),
        context=context,
    )
    severity = coerce_severity(
        str(raw.get("severity", Severity.BLOCKER.value)).strip(),
        context=context,
    )
    message = ensure_required_text(raw, "message", context=context)

    if enforcement_mode == "strict" and not anchor_ref:
        raise ContractError(f"{context} strict rule must have anchor_ref")

    return ContractRule(
        id=rule_id,
        anchor_ref=anchor_ref,
        vector=vector,
        scope=scope,
        evidence_class_allowed=evidence,
        enforcement_mode=enforcement_mode,
        severity=severity,
        message=message,
        protected_object=optional_text(raw, "protected_object"),
        pattern=optional_text(raw, "pattern"),
        forbidden_conversion=optional_text(raw, "forbidden_conversion"),
        safer_form=optional_text(raw, "safer_form"),
        role=optional_text(raw, "role"),
        integrity_posture=optional_text(raw, "integrity_posture"),
    )


def validate_unique_rule_ids(rules: Iterable[ContractRule], *, contract_path: str) -> None:
    seen: set[str] = set()
    for rule in rules:
        if rule.id in seen:
            raise ContractError(f"{contract_path} contains duplicate rule id: {rule.id}")
        seen.add(rule.id)


def document_from_mapping(raw: Mapping[str, Any], *, contract_path: str) -> ContractDocument:
    schema_version = ensure_required_text(raw, "schema_version", context=contract_path)
    if schema_version != SUPPORTED_CONTRACT_SCHEMA_VERSION:
        raise ContractError(
            f"{contract_path} schema_version must be "
            f"{SUPPORTED_CONTRACT_SCHEMA_VERSION!r}, got {schema_version!r}"
        )

    contract_role = str(raw.get("contract_role", DEFAULT_CONTRACT_ROLE)).strip()
    if not contract_role:
        raise ContractError(f"{contract_path} contract_role must not be empty")

    raw_rules = raw.get("rules")
    if not isinstance(raw_rules, list):
        raise ContractError(f"{contract_path} field 'rules' must be a list")

    rules: list[ContractRule] = []
    for index, raw_rule in enumerate(raw_rules):
        if not isinstance(raw_rule, dict):
            raise ContractError(f"{contract_path}:rules[{index}] must be an object")
        rules.append(rule_from_mapping(raw_rule, index=index, contract_path=contract_path))

    validate_unique_rule_ids(rules, contract_path=contract_path)

    return ContractDocument(
        path=contract_path,
        schema_version=schema_version,
        contract_role=contract_role,
        rules=tuple(rules),
    )


def load_contract(path: Path | str) -> ContractDocument:
    source = Path(path)
    contract_path = normalize_repo_path(source)

    if not source.exists():
        raise ContractError(f"contract missing: {contract_path}")

    if source.suffix.lower() not in {".json"}:
        raise ContractError(
            f"unsupported contract format for {contract_path}; "
            "current core supports JSON only"
        )

    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"contract invalid JSON: {contract_path}") from exc
    except OSError as exc:
        raise ContractError(f"contract unreadable: {contract_path}") from exc

    if not isinstance(raw, dict):
        raise ContractError(f"{contract_path} contract root must be a JSON object")

    return document_from_mapping(raw, contract_path=contract_path)


def load_contracts(paths: Iterable[Path | str]) -> tuple[ContractDocument, ...]:
    return tuple(load_contract(path) for path in paths)


def merge_rules(documents: Iterable[ContractDocument]) -> dict[str, ContractRule]:
    merged: dict[str, ContractRule] = {}

    for document in documents:
        for rule in document.rules:
            if rule.id in merged:
                raise ContractError(f"duplicate rule id across contracts: {rule.id}")
            merged[rule.id] = rule

    return merged


def contract_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    guard_id: str = DEFAULT_CONTRACT_GUARD_ID,
    guard_file: str = DEFAULT_CONTRACT_GUARD_FILE,
    severity: Severity | str = Severity.BLOCKER.value,
    confidence: Confidence | str = Confidence.HIGH.value,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
    observed_pattern: str | None = None,
    protected_object: str | None = "contract",
    safer_form: str | None = None,
) -> Finding:
    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        scope=Scope.P0_REPOSITORY.value,
        vector=DriftVector.V7_CONTRACT_DRIFT.value,
        severity=severity.value if isinstance(severity, Severity) else severity,
        confidence=confidence.value if isinstance(confidence, Confidence) else confidence,
        path=normalize_repo_path(path),
        message=message,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN.value,
        safer_form=safer_form,
        integrity_posture="contract_schema_read_only",
    )


def validate_contract_file(
    path: Path | str,
    *,
    guard_id: str = DEFAULT_CONTRACT_GUARD_ID,
    guard_file: str = DEFAULT_CONTRACT_GUARD_FILE,
) -> list[Finding]:
    try:
        load_contract(path)
    except ContractError as exc:
        return [
            contract_finding(
                rule_id="CONTRACT-INVALID",
                path=path,
                message=str(exc),
                guard_id=guard_id,
                guard_file=guard_file,
                safer_form=(
                    "Fix contract schema or rule traceability through "
                    "human-reviewed repository process."
                ),
            )
        ]

    return []


def validate_contract_files(
    paths: Iterable[Path | str],
    *,
    guard_id: str = DEFAULT_CONTRACT_GUARD_ID,
    guard_file: str = DEFAULT_CONTRACT_GUARD_FILE,
) -> list[Finding]:
    findings: list[Finding] = []

    for path in paths:
        findings.extend(
            validate_contract_file(
                path,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    try:
        documents = load_contracts(paths)
        merge_rules(documents)
    except ContractError as exc:
        findings.append(
            contract_finding(
                rule_id="CONTRACT-MERGE-INVALID",
                path="contracts/",
                message=str(exc),
                guard_id=guard_id,
                guard_file=guard_file,
                safer_form="Ensure rule ids are globally unique across loaded contracts.",
            )
        )

    return findings


def rule_to_dict(rule: ContractRule) -> dict[str, Any]:
    return {
        "id": rule.id,
        "anchor_ref": rule.anchor_ref,
        "vector": rule.vector.value,
        "scope": rule.scope.value,
        "evidence_class_allowed": rule.evidence_class_allowed.value,
        "enforcement_mode": rule.enforcement_mode,
        "severity": rule.severity.value,
        "message": rule.message,
        "protected_object": rule.protected_object,
        "pattern": rule.pattern,
        "forbidden_conversion": rule.forbidden_conversion,
        "safer_form": rule.safer_form,
        "role": rule.role,
        "integrity_posture": rule.integrity_posture,
    }


def contract_to_dict(document: ContractDocument) -> dict[str, Any]:
    return {
        "schema_version": document.schema_version,
        "contract_role": document.contract_role,
        "rules": [
            {key: value for key, value in rule_to_dict(rule).items() if value is not None}
            for rule in document.rules
        ],
    }
