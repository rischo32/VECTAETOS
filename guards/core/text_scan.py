#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Text Scan Core

Role:
    Shared text-scanning helpers for repository perimeter guards.

Boundary:
    This module exposes textual drift patterns for guard diagnostics.
    It does not define ontology, prove truth, validate safety, authorize deployment,
    resolve QE, estimate κ, evaluate K(Φ), interpret projection, or mutate Φ.

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
from typing import Pattern

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


OPERATIONAL_TOKENS: tuple[str, ...] = (
    "def ",
    "class ",
    "return ",
    "raise ",
    "except ",
    "try:",
    "if ",
    "elif ",
    "else:",
    "for ",
    "while ",
    "import ",
    "from ",
    "subprocess",
    "requests",
    "socket",
    "open(",
    ".open(",
    "write(",
    ".write(",
    "eval(",
    "exec(",
    "compile(",
    "random",
    "argmax",
    "argmin",
    "sort(",
    "sorted(",
    "select",
    "choose",
    "optimize",
    "optimaliz",
    "handler",
    "repair",
    "fallback",
)


class ContextDecision(str, enum.Enum):
    ACTIVE = "active"
    NEGATED_SAFE = "negated_safe"
    META_EXAMPLE = "meta_example"
    NEGATED_OPERATIONAL_REVIEW = "negated_operational_review"


@dataclasses.dataclass(frozen=True, slots=True)
class ScanRule:
    """
    Contract-projected text scan rule.

    A ScanRule is not ontology. It is a detector definition used by a guard.
    """

    rule_id: str
    pattern: Pattern[str]
    message: str
    scope: Scope | str
    vector: DriftVector | str
    severity: Severity | str
    confidence: Confidence | str = Confidence.HIGH
    evidence_class_allowed: EvidenceClass | str = EvidenceClass.E1_STATIC_SCAN
    protected_object: str | None = None
    forbidden_conversion: str | None = None
    safer_form: str | None = None
    anchor_ref: str | None = None
    contract_ref: str | None = None
    enforcement_mode: str | None = None
    integrity_posture: str | None = None


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


def compile_pattern(pattern: str) -> Pattern[str]:
    return re.compile(pattern, flags=re.IGNORECASE)


def make_rule(
    *,
    rule_id: str,
    pattern: str,
    message: str,
    scope: Scope | str,
    vector: DriftVector | str,
    severity: Severity | str,
    confidence: Confidence | str = Confidence.HIGH,
    evidence_class_allowed: EvidenceClass | str = EvidenceClass.E1_STATIC_SCAN,
    protected_object: str | None = None,
    forbidden_conversion: str | None = None,
    safer_form: str | None = None,
    anchor_ref: str | None = None,
    contract_ref: str | None = None,
    enforcement_mode: str | None = None,
    integrity_posture: str | None = None,
) -> ScanRule:
    return ScanRule(
        rule_id=rule_id,
        pattern=compile_pattern(pattern),
        message=message,
        scope=scope,
        vector=vector,
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
    )


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


def has_operational_context(
    context: str,
    *,
    tokens: Sequence[str] = OPERATIONAL_TOKENS,
) -> bool:
    return contains_any_token(context, tokens)


def classify_context(
    *,
    line: str,
    context: str,
    start: int,
    end: int,
) -> tuple[ContextDecision, bool, bool, bool]:
    negated = has_negation_near(line, start, end) or contains_any_token(context, ("≠", "!=", "\\neq"))
    meta = has_meta_context(context)
    operational = has_operational_context(context)

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
    repo_path = str(path).replace("\\", "/")
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
    if decision == ContextDecision.NEGATED_OPERATIONAL_REVIEW:
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
        scope=rule.scope,
        vector=rule.vector,
        severity=severity_for_decision(rule, match.decision),
        confidence=rule.confidence,
        path=match.path,
        line=match.line,
        column=match.column,
        end_column=match.end_column,
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
