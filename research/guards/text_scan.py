#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Text Scan Core

Role:
    Shared text-scanning helpers for repository perimeter guards.

Boundary:
    This module exposes textual drift patterns for guard diagnostics.

    It does not define ontology, prove truth, validate safety, authorize
    deployment, resolve QE, estimate κ, evaluate K(Φ), interpret projection,
    or mutate Φ.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import enum
import re
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path
from typing import Any, Pattern

try:
    from guards.core.findings import (
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Scope,
        Severity,
        make_finding,
    )
    from guards.core.perimeter import EnforcementMode, normalize_vectors
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
        Scope,
        Severity,
        make_finding,
    )
    from perimeter import EnforcementMode, normalize_vectors  # type: ignore


DEFAULT_CONTEXT_RADIUS = 3
DEFAULT_NEGATION_WINDOW = 90


NEGATION_TOKENS: tuple[str, ...] = (
    # English
    "not",
    "no",
    "never",
    "does not",
    "do not",
    "is not",
    "are not",
    "must not",
    "should not",
    "cannot",
    "can not",
    "without",
    "non-",
    # Slovak / Czech
    "nie",
    "nie je",
    "nie sú",
    "nesmie",
    "nesmú",
    "nemá",
    "nemá sa",
    "nikdy",
    "nejde o",
    "bez",
    "neoptimalizuje",
    "neoptimalizovať",
    "nerozhoduje",
    "neinterpretuje",
    "nemení",
    "nemodifikuje",
    "nevaliduje",
    "nedokazuje",
    "neautorizuje",
    "nenahrádza",
    "nepredstavuje",
    "neznamená",
    # Symbols
    "≠",
    "!=",
    "\\neq",
)


META_CONTEXT_TOKENS: tuple[str, ...] = (
    # English
    "forbidden",
    "invalid",
    "anti-pattern",
    "antipattern",
    "negative example",
    "bad example",
    "counterexample",
    "drift vector",
    "drift example",
    "failure example",
    "must not be used",
    "must not be interpreted",
    "must not be framed",
    "not allowed",
    "prohibited",
    "disallowed",
    "blocked vocabulary",
    "unsafe wording",
    "legacy migration",
    "semantic errata",
    "vocabulary lock",
    "fixture",
    "test fixture",
    "must-fail",
    "must-warn",
    "must-pass",
    "example forbidden",
    "safe wording",
    "forbidden wording",
    # Slovak / Czech
    "zakázané",
    "zakazane",
    "zakázaná",
    "zakazana",
    "neplatné",
    "neplatne",
    "omyl",
    "chybný príklad",
    "chybny priklad",
    "príklad driftu",
    "priklad driftu",
    "drift vektor",
    "nesmie byť",
    "nesmie byt",
    "nesmie sa",
    "nemá sa",
    "nema sa",
    "nesprávna formulácia",
    "nespravna formulacia",
    "migračná mapa",
    "migracna mapa",
)


OPERATIONAL_TOKEN_PATTERN = re.compile(
    r"(?<![=!<>])=(?!=)"
    r"|\b(def|class|return|yield|raise|except|try|if|elif|else|for|while|import|from)\b"
    r"|\b(subprocess|requests|socket|urllib|open|write|eval|exec|compile|random)\b"
    r"|\b(argmax|argmin|select|choose|optimi[sz]e|optimaliz|handler|repair|fallback)\b"
    r"|\.(open|write|write_text|write_bytes|rename|replace|unlink|remove)\s*\("
    r"|\b(Path|os|sys|shutil)\s*\(",
    flags=re.IGNORECASE,
)


class ContextDecision(str, enum.Enum):
    ACTIVE = "active"
    NEGATED_SAFE = "negated_safe"
    META_EXAMPLE = "meta_example"
    NEGATED_OPERATIONAL_REVIEW = "negated_operational_review"
    META_OPERATIONAL_REVIEW = "meta_operational_review"


@dataclasses.dataclass(frozen=True, slots=True)
class ScanRule:
    """
    Contract-projected text scan rule.

    A ScanRule is not ontology. It is a detector definition used by a guard.
    """

    rule_id: str
    pattern: Pattern[str]
    pattern_text: str
    message: str
    scope: PerimeterScope | Scope | str
    vector: DriftVector | str
    severity: Severity | str
    level: PerimeterLevel | str | None = None
    vectors: tuple[DriftVector | str, ...] | None = None
    confidence: Confidence | str = Confidence.HIGH
    evidence_class_allowed: EvidenceClass | str = EvidenceClass.E1_STATIC_SCAN
    protected_object: str | None = None
    forbidden_conversion: str | None = None
    safer_form: str | None = None
    anchor_ref: str | None = None
    contract_ref: str | None = None
    enforcement_mode: EnforcementMode | str | None = EnforcementMode.STRICT
    integrity_posture: IntegrityPosture | str | None = IntegrityPosture.SEMANTIC_READ_ONLY
    role: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class TextMatch:
    rule_id: str
    path: str
    line: int
    column: int
    end_column: int
    excerpt: str
    context: str
    negated_context: bool
    meta_context: bool
    operational_context: bool
    decision: ContextDecision


def normalize_path(path: str | Path) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def compile_pattern(pattern: str) -> Pattern[str]:
    return re.compile(pattern, flags=re.IGNORECASE)


def make_rule(
    *,
    rule_id: str,
    pattern: str,
    message: str,
    scope: PerimeterScope | Scope | str,
    vector: DriftVector | str,
    severity: Severity | str,
    level: PerimeterLevel | str | None = None,
    vectors: tuple[DriftVector | str, ...] | None = None,
    confidence: Confidence | str = Confidence.HIGH,
    evidence_class_allowed: EvidenceClass | str = EvidenceClass.E1_STATIC_SCAN,
    protected_object: str | None = None,
    forbidden_conversion: str | None = None,
    safer_form: str | None = None,
    anchor_ref: str | None = None,
    contract_ref: str | None = None,
    enforcement_mode: EnforcementMode | str | None = EnforcementMode.STRICT,
    integrity_posture: IntegrityPosture | str | None = IntegrityPosture.SEMANTIC_READ_ONLY,
    role: str | None = None,
) -> ScanRule:
    normalized_vectors = normalize_vectors(vectors) if vectors is not None else None

    return ScanRule(
        rule_id=rule_id,
        pattern=compile_pattern(pattern),
        pattern_text=pattern,
        message=message,
        level=level,
        scope=scope,
        vector=vector,
        vectors=normalized_vectors,
        severity=severity,
        confidence=confidence,
        evidence_class_allowed=evidence_class_allowed,
        protected_object=protected_object,
        forbidden_conversion=forbidden_conversion,
        safer_form=safer_form,
        anchor_ref=anchor_ref,
        contract_ref=contract_ref,
        enforcement_mode=enforcement_mode,
        integrity_posture=integrity_posture,
        role=role,
    )


def scan_rules_from_contract_rule(
    contract_rule: Any,
    *,
    contract_ref: str | None = None,
) -> list[ScanRule]:
    """
    Convert a ContractRule-like object into one or more ScanRule objects.

    The function is duck-typed to avoid making text_scan.py depend on a specific
    contract implementation. No ontology is inferred here.
    """

    patterns = tuple(getattr(contract_rule, "patterns", ()) or ())
    single_pattern = getattr(contract_rule, "pattern", None)

    if single_pattern and single_pattern not in patterns:
        patterns = (single_pattern, *patterns)

    if not patterns:
        return []

    rules: list[ScanRule] = []
    for pattern in patterns:
        rules.append(
            make_rule(
                rule_id=str(getattr(contract_rule, "id")),
                pattern=pattern,
                message=str(getattr(contract_rule, "message")),
                level=getattr(contract_rule, "level", None),
                scope=getattr(contract_rule, "scope"),
                vector=getattr(contract_rule, "vector"),
                vectors=getattr(contract_rule, "vectors", None),
                severity=getattr(contract_rule, "severity"),
                confidence=Confidence.HIGH,
                evidence_class_allowed=getattr(contract_rule, "evidence_class_allowed"),
                protected_object=getattr(contract_rule, "protected_object", None),
                forbidden_conversion=getattr(contract_rule, "forbidden_conversion", None),
                safer_form=getattr(contract_rule, "safer_form", None),
                anchor_ref=getattr(contract_rule, "anchor_ref", None),
                contract_ref=contract_ref,
                enforcement_mode=getattr(contract_rule, "enforcement_mode", None),
                integrity_posture=getattr(contract_rule, "integrity_posture", None),
                role=getattr(contract_rule, "role", None),
            )
        )

    return rules


def normalize_text(value: str) -> str:
    return value.casefold()


def contains_any_token(text: str, tokens: Sequence[str]) -> bool:
    lowered = normalize_text(text)
    return any(normalize_text(token) in lowered for token in tokens)


def build_context(lines: Sequence[str], index: int, radius: int = DEFAULT_CONTEXT_RADIUS) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end])


def has_negation_near(
    line: str,
    start: int,
    end: int,
    *,
    window: int = DEFAULT_NEGATION_WINDOW,
    tokens: Sequence[str] = NEGATION_TOKENS,
) -> bool:
    left = max(0, start - window)
    right = min(len(line), end + window)
    context = line[left:right]
    return contains_any_token(context, tokens)


def has_meta_context(
    context: str,
    *,
    tokens: Sequence[str] = META_CONTEXT_TOKENS,
) -> bool:
    return contains_any_token(context, tokens)


def has_operational_context(context: str) -> bool:
    return OPERATIONAL_TOKEN_PATTERN.search(context) is not None


def classify_context(
    *,
    line: str,
    context: str,
    start: int,
    end: int,
) -> tuple[ContextDecision, bool, bool, bool]:
    negated = has_negation_near(line, start, end) or contains_any_token(
        context,
        ("≠", "!=", "\\neq"),
    )
    meta = has_meta_context(context)
    operational = has_operational_context(context)

    if meta and operational:
        return ContextDecision.META_OPERATIONAL_REVIEW, negated, meta, operational

    if meta:
        return ContextDecision.META_EXAMPLE, negated, meta, operational

    if negated and operational:
        return ContextDecision.NEGATED_OPERATIONAL_REVIEW, negated, meta, operational

    if negated:
        return ContextDecision.NEGATED_SAFE, negated, meta, operational

    return ContextDecision.ACTIVE, negated, meta, operational


def line_excerpt(line: str, *, limit: int = 240) -> str:
    stripped = line.strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 1] + "…"


def iter_text_matches(
    *,
    path: str | Path,
    text: str,
    rules: Iterable[ScanRule],
    context_radius: int = DEFAULT_CONTEXT_RADIUS,
) -> Iterator[tuple[ScanRule, TextMatch]]:
    repo_path = normalize_path(path)
    lines = text.splitlines()
    rule_list = list(rules)

    for index, line in enumerate(lines):
        context = build_context(lines, index, radius=context_radius)

        for rule in rule_list:
            for match in rule.pattern.finditer(line):
                decision, negated, meta, operational = classify_context(
                    line=line,
                    context=context,
                    start=match.start(),
                    end=match.end(),
                )
                yield rule, TextMatch(
                    rule_id=rule.rule_id,
                    path=repo_path,
                    line=index + 1,
                    column=match.start() + 1,
                    end_column=match.end() + 1,
                    excerpt=line_excerpt(line),
                    context=context,
                    negated_context=negated,
                    meta_context=meta,
                    operational_context=operational,
                    decision=decision,
                )


def decision_allows_skip(decision: ContextDecision) -> bool:
    return decision in {
        ContextDecision.NEGATED_SAFE,
        ContextDecision.META_EXAMPLE,
    }


def severity_for_decision(rule: ScanRule, decision: ContextDecision) -> Severity | str:
    if decision in {
        ContextDecision.NEGATED_OPERATIONAL_REVIEW,
        ContextDecision.META_OPERATIONAL_REVIEW,
    }:
        return Severity.WARN
    return rule.severity


def match_to_finding(
    *,
    rule: ScanRule,
    match: TextMatch,
    guard_id: str,
    guard_file: str,
    contract_schema_version: str = "1.0",
) -> Finding:
    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule.rule_id,
        contract_schema_version=contract_schema_version,
        level=rule.level,
        scope=rule.scope,
        vector=rule.vector,
        vectors=rule.vectors,
        severity=severity_for_decision(rule, match.decision),
        confidence=rule.confidence,
        path=match.path,
        line=match.line,
        column=match.column,
        end_column=match.end_column,
        role=rule.role,
        message=rule.message,
        protected_object=rule.protected_object,
        observed_pattern=match.excerpt,
        forbidden_conversion=rule.forbidden_conversion,
        negated_context=match.negated_context,
        evidence_class_allowed=rule.evidence_class_allowed,
        enforcement_mode=rule.enforcement_mode,
        integrity_posture=rule.integrity_posture,
        anchor_ref=rule.anchor_ref,
        contract_ref=rule.contract_ref,
        safer_form=rule.safer_form,
    )


def scan_text_to_findings(
    *,
    path: str | Path,
    text: str,
    rules: Iterable[ScanRule],
    guard_id: str,
    guard_file: str,
    contract_schema_version: str = "1.0",
    skip_safe_context: bool = True,
    context_radius: int = DEFAULT_CONTEXT_RADIUS,
) -> list[Finding]:
    findings: list[Finding] = []

    for rule, match in iter_text_matches(
        path=path,
        text=text,
        rules=rules,
        context_radius=context_radius,
    ):
        if skip_safe_context and decision_allows_skip(match.decision):
            continue

        findings.append(
            match_to_finding(
                rule=rule,
                match=match,
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
            )
        )

    return findings


def scan_file_to_findings(
    *,
    path: str | Path,
    rules: Iterable[ScanRule],
    guard_id: str,
    guard_file: str,
    contract_schema_version: str = "1.0",
    skip_safe_context: bool = True,
    context_radius: int = DEFAULT_CONTEXT_RADIUS,
) -> list[Finding]:
    text = read_text_file(path)
    if text is None:
        return []

    return scan_text_to_findings(
        path=path,
        text=text,
        rules=rules,
        guard_id=guard_id,
        guard_file=guard_file,
        contract_schema_version=contract_schema_version,
        skip_safe_context=skip_safe_context,
        context_radius=context_radius,
    )


def read_text_file(path: Path | str) -> str | None:
    """
    Read a text file safely for scanning.

    Returns None for unreadable or binary-looking files.
    """

    source = Path(path)
    try:
        data = source.read_bytes()
    except OSError:
        return None

    if b"\x00" in data:
        return None

    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    return None


__all__ = [
    "DEFAULT_CONTEXT_RADIUS",
    "DEFAULT_NEGATION_WINDOW",
    "NEGATION_TOKENS",
    "META_CONTEXT_TOKENS",
    "OPERATIONAL_TOKEN_PATTERN",
    "ContextDecision",
    "ScanRule",
    "TextMatch",
    "normalize_path",
    "compile_pattern",
    "make_rule",
    "scan_rules_from_contract_rule",
    "normalize_text",
    "contains_any_token",
    "build_context",
    "has_negation_near",
    "has_meta_context",
    "has_operational_context",
    "classify_context",
    "line_excerpt",
    "iter_text_matches",
    "decision_allows_skip",
    "severity_for_decision",
    "match_to_finding",
    "scan_text_to_findings",
    "scan_file_to_findings",
    "read_text_file",
    ]
