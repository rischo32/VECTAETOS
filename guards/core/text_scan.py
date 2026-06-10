#!/usr/bin/env python3
"""
VECTAETOS - Shared Guard Text Scan Core

Role:
    Shared text-scanning helpers for repository perimeter guards.

Boundary:
    This module exposes textual drift patterns for guard diagnostics.

    It does not define ontology, prove truth, validate safety, authorize
    deployment, resolve QE, estimate kappa, evaluate K(Phi), interpret
    projection, or mutate Phi.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import enum
import re
import unicodedata
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
DEFAULT_NEGATION_WINDOW = 160


NEGATION_TOKENS: tuple[str, ...] = (
    # English. Keep these relational; avoid broad tokens such as "non-".
    "not",
    "no",
    "never",
    "does not",
    "do not",
    "is not",
    "are not",
    "must not",
    "should not",
    "shall not",
    "may not",
    "cannot",
    "can not",
    "without",
    # Slovak / Czech, accentless forms are intentional; normalize_text()
    # removes diacritics before matching.
    "nie",
    "nie je",
    "nie su",
    "nie je to",
    "nejde o",
    "bez",
    "nikdy",
    "nesmie",
    "nesmu",
    "nesmie byt",
    "nesmu byt",
    "nesmie sa",
    "nesmu sa",
    "nema",
    "nema sa",
    "nemaju",
    "nemaju sa",
    "nepozna",
    "nepoznaju",
    "nevykonava",
    "nevykonavaju",
    "nevytvara",
    "nevytvaraju",
    "neoptimalizuje",
    "neoptimalizuju",
    "neoptimalizovat",
    "nerozhoduje",
    "nerozhoduju",
    "neinterpretuje",
    "neinterpretuju",
    "nepredpisuje",
    "nepredpisuju",
    "neodporuca",
    "neodporucaju",
    "nepise",
    "nepisu",
    "nepise spat",
    "nepisu spat",
    "nemeni",
    "nemenia",
    "nemodifikuje",
    "nemodifikuju",
    "nevaliduje",
    "nevaliduju",
    "nedokazuje",
    "nedokazuju",
    "neautorizuje",
    "neautorizuju",
    "nenahradza",
    "nenahradzaju",
    "nepredstavuje",
    "nepredstavuju",
    "neznamena",
    "neznamenaju",
    "nezasahuje",
    "nezasahuju",
    "neriadi",
    "neriadia",
    "nevybera",
    "nevyberaju",
    "neselektuje",
    "neselektuji",
    "netrenuje",
    "netrenuju",
    "neuci",
    "neucia",
    # Symbols
    "\u2260",
    "!=",
    "\\neq",
)


# Morphological negation detector for Slovak/Czech verbs with "ne-" prefix.
# This exists because protective sentences often use words like
# "neinterpretuju", "nepredpisuju", "nerozhoduju", "neodporucaju".
NEGATED_MORPHOLOGY_PATTERN = re.compile(
    r"(?<![a-z0-9_])ne(?:"
    r"interpret\w*"
    r"|predpis\w*"
    r"|rozhod\w*"
    r"|odporuc\w*"
    r"|optimaliz\w*"
    r"|valid\w*"
    r"|autoriz\w*"
    r"|dokaz\w*"
    r"|modifik\w*"
    r"|men\w*"
    r"|pis\w*"
    r"|nahradz\w*"
    r"|predstav\w*"
    r"|znamena\w*"
    r"|zasah\w*"
    r"|riad\w*"
    r"|vyber\w*"
    r"|selekt\w*"
    r"|trenu\w*"
    r"|uc\w*"
    r"|vytvar\w*"
    r"|pozn\w*"
    r"|vykonav\w*"
    r")(?![a-z0-9_])",
    flags=re.IGNORECASE,
)


META_CONTEXT_TOKENS: tuple[str, ...] = (
    # English
    "forbidden",
    "forbidden conversion",
    "forbidden transformation",
    "invalid",
    "invalid claim",
    "incompatible transformation",
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
    "must never",
    "not allowed",
    "not permitted",
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
    "safer wording",
    "guard pattern",
    "pattern declaration",
    "pattern registry",
    "forbidden phrase",
    "forbidden phrases",
    "forbidden examples",
    "forbidden claims",
    "claim limit",
    "boundary clause",
    "boundary clauses",
    "license restriction",
    "license restrictions",
    "restrictions",
    "shall not",
    "may not",
    # Slovak / Czech, accentless forms are intentional.
    "zakazane",
    "zakazana",
    "neplatne",
    "omyl",
    "chybny priklad",
    "priklad driftu",
    "drift vektor",
    "nesmie byt",
    "nesmie sa",
    "nema sa",
    "nespravna formulacia",
    "migracna mapa",
    "zakazana formulacia",
    "hranica slovnika",
    "bezpecna formulacia",
)


# Pattern declarations and machine-readable guard vocabulary. These should not
# be interpreted as active repository doctrine.
PATTERN_DECLARATION_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"[A-Z][A-Z0-9_]*(?:"
    r"_PATTERN|_PATTERNS|_RULE|_RULES|_TOKEN|_TOKENS|_DRIFT|_LANGUAGE|_TERMS"
    r")"
    r"(?![A-Za-z0-9_])"
)

GUARD_DECLARATION_PATTERN = re.compile(
    r"\b("
    r"rule_id|pattern|patterns|pattern_text|forbidden_conversion|safer_form|"
    r"observed_pattern|protected_object|anchor_ref|contract_ref|message"
    r")\b\s*[:=]",
    flags=re.IGNORECASE,
)


# Explicit negative machine-readable assertions.
BOOLEAN_FALSE_CONTEXT_PATTERN = re.compile(
    r"(?:(?:uses|is|has|allows|enables|validates|proves|authorizes|decides|selects)"
    r"[A-Za-z0-9_]*|[A-Za-z0-9_]*(?:safety|deployment|validity|truth|score|metric|threshold)[A-Za-z0-9_]*)"
    r"\s*(?::|=|==)\s*(?:False|false|0)\b"
)


# Strong operational context markers. These indicate code or runtime surfaces.
# Avoid overly broad keywords such as plain "if", because prose often contains
# "if" in explanatory text and that should not turn safe negation into a WARN.
OPERATIONAL_TOKEN_PATTERN = re.compile(
    r"(?<![=!<>])=(?!=)"
    r"|\b(def|class|return|yield|raise|except|import|from)\b"
    r"|\b(subprocess|requests|socket|urllib|open|write|eval|exec|compile|random)\b"
    r"|\b(argmax|argmin|handler|repair)\b"
    r"|\.(open|write|write_text|write_bytes|rename|replace|unlink|remove)\s*\("
    r"|\b(Path|os|sys|shutil)\s*\(",
    flags=re.IGNORECASE,
)


# Weak operational verbs are not enough by themselves. They are common in
# protective prose such as "Phi must never optimize trajectories." They become
# operational only when a nearby review/code cue is also present.
REVIEW_CONTEXT_PATTERN = re.compile(
    r"\b("
    r"review|code|function|method|handler|implementation|runtime|scanner|guard|"
    r"test|fixture|commit|diff|pr|pull request|workflow|ci|runner|pytest"
    r")\b",
    flags=re.IGNORECASE,
)

WEAK_OPERATIONAL_VERB_PATTERN = re.compile(
    r"\b(select|choose|optimi[sz]e|optimaliz|fallback)\w*\b",
    flags=re.IGNORECASE,
)


SAFE_RELATION_PATTERN = re.compile(
    r"\b("
    r"is\s+not|are\s+not|does\s+not|do\s+not|must\s+not|should\s+not|shall\s+not|"
    r"may\s+not|cannot|can\s+not|never|without|"
    r"nie\s+je|nie\s+su|nejde\s+o|nesmie|nesmu|nema\s+sa|nemaju\s+sa|"
    r"nevalid\w*|nedokaz\w*|neautoriz\w*|nerozhod\w*|neoptimaliz\w*|"
    r"nepredstav\w*|neznamen\w*|nepozn\w*|nevykonav\w*"
    r")\b"
    r".{0,120}\b("
    r"score|skore|metric|metrika|threshold|prahov|parameter|scalar|number|"
    r"value|objective|target|reward|optimization|optimaliz|fitness|loss|"
    r"accuracy|performance|benchmark|validity|deployment|safety|safe|proof|"
    r"proves|validates|validation|selector|ranking|error|bug|fallback|failure|"
    r"exception|recovery|chyba|zlyhan"
    r")\b",
    flags=re.IGNORECASE | re.DOTALL,
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


def strip_diacritics(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return decomposed.encode("ascii", "ignore").decode("ascii")


def normalize_text(value: str) -> str:
    """
    Normalize text for token checks.

    This is not semantic interpretation. It is a scanner utility that makes
    Slovak/Czech negation robust against diacritics.
    """

    return strip_diacritics(value).casefold()


def token_is_word_like(token: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9_ ]+", token, flags=re.IGNORECASE))


def token_in_normalized_text(normalized_text: str, normalized_token: str) -> bool:
    if not normalized_token:
        return False

    if normalized_token.endswith("-"):
        return normalized_token in normalized_text

    if token_is_word_like(normalized_token):
        pattern = r"(?<![a-z0-9_])" + re.escape(normalized_token) + r"(?![a-z0-9_])"
        return re.search(pattern, normalized_text, flags=re.IGNORECASE) is not None

    return normalized_token in normalized_text


def contains_any_token(text: str, tokens: Sequence[str]) -> bool:
    normalized = normalize_text(text)
    for token in tokens:
        normalized_token = normalize_text(token)
        if token_in_normalized_text(normalized, normalized_token):
            return True
    return False


def has_negated_morphology(text: str) -> bool:
    normalized = normalize_text(text)
    return NEGATED_MORPHOLOGY_PATTERN.search(normalized) is not None


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
    region = line[left:right]
    return contains_any_token(region, tokens) or has_negated_morphology(region)


def has_safe_relation_negation(line: str, context: str) -> bool:
    compact = " ".join((line + "\n" + context).split())
    normalized = normalize_text(compact)

    if "!=" in compact or "\u2260" in compact or "\\neq" in compact:
        return True

    if SAFE_RELATION_PATTERN.search(normalized):
        return True

    if BOOLEAN_FALSE_CONTEXT_PATTERN.search(line):
        return True

    return False


def has_meta_context(
    context: str,
    *,
    tokens: Sequence[str] = META_CONTEXT_TOKENS,
) -> bool:
    return contains_any_token(context, tokens)


def is_pattern_declaration(line: str, context: str) -> bool:
    if PATTERN_DECLARATION_PATTERN.search(line):
        return True

    if GUARD_DECLARATION_PATTERN.search(line):
        return True

    lowered = normalize_text(line)
    return (
        ("pattern" in lowered or "rule_id" in lowered)
        and ("drift" in lowered or "forbidden" in lowered or "language" in lowered)
    )


def is_forbidden_example_context(line: str, context: str) -> bool:
    normalized_line = normalize_text(line)
    normalized_context = normalize_text(context)

    if has_meta_context(context):
        return True

    if ("->" in line or "\u2192" in line or "becomes" in normalized_line) and (
        "forbidden" in normalized_context
        or "invalid" in normalized_context
        or "drift" in normalized_context
        or "must not" in normalized_context
        or "nesmie" in normalized_context
        or "vocabulary lock" in normalized_context
    ):
        return True

    if "convert" in normalized_line and (
        "must not" in normalized_context
        or "shall not" in normalized_context
        or "may not" in normalized_context
        or "forbidden" in normalized_context
        or "prohibited" in normalized_context
        or "license" in normalized_context
        or "nesmie" in normalized_context
        or "zakazane" in normalized_context
    ):
        return True

    return False


def has_operational_context(context: str) -> bool:
    if OPERATIONAL_TOKEN_PATTERN.search(context):
        # Avoid treating Markdown tables / prose with "=" as code unless there
        # is a stronger code cue nearby.
        if REVIEW_CONTEXT_PATTERN.search(context) is not None:
            return True
        if re.search(
            r"^\s*(def|class|return|yield|raise|except|import|from)\b",
            context,
            flags=re.IGNORECASE | re.MULTILINE,
        ):
            return True
        if re.search(r"\.(open|write|write_text|write_bytes|rename|replace|unlink|remove)\s*\(", context):
            return True
        if re.search(r"\b(subprocess|requests|socket|urllib|eval|exec|compile|random)\b", context):
            return True
        if BOOLEAN_FALSE_CONTEXT_PATTERN.search(context):
            return False
        return False

    return (
        REVIEW_CONTEXT_PATTERN.search(context) is not None
        and WEAK_OPERATIONAL_VERB_PATTERN.search(context) is not None
    )


def classify_context(
    *,
    line: str,
    context: str,
    start: int,
    end: int,
) -> tuple[ContextDecision, bool, bool, bool]:
    negated = (
        has_negation_near(line, start, end)
        or contains_any_token(context, ("\u2260", "!=", "\\neq"))
        or has_safe_relation_negation(line, context)
    )
    meta = has_meta_context(context) or is_pattern_declaration(line, context) or is_forbidden_example_context(line, context)
    operational = has_operational_context(context)

    if is_pattern_declaration(line, context):
        return ContextDecision.META_EXAMPLE, negated, True, operational

    if BOOLEAN_FALSE_CONTEXT_PATTERN.search(line):
        return ContextDecision.NEGATED_SAFE, True, meta, operational

    if has_safe_relation_negation(line, context):
        return ContextDecision.NEGATED_SAFE, True, meta, operational

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
    stripped = " ".join(line.strip().split())
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 1] + "..."


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
    "NEGATED_MORPHOLOGY_PATTERN",
    "META_CONTEXT_TOKENS",
    "PATTERN_DECLARATION_PATTERN",
    "GUARD_DECLARATION_PATTERN",
    "BOOLEAN_FALSE_CONTEXT_PATTERN",
    "OPERATIONAL_TOKEN_PATTERN",
    "REVIEW_CONTEXT_PATTERN",
    "WEAK_OPERATIONAL_VERB_PATTERN",
    "SAFE_RELATION_PATTERN",
    "ContextDecision",
    "ScanRule",
    "TextMatch",
    "normalize_path",
    "compile_pattern",
    "make_rule",
    "scan_rules_from_contract_rule",
    "strip_diacritics",
    "normalize_text",
    "token_is_word_like",
    "token_in_normalized_text",
    "contains_any_token",
    "has_negated_morphology",
    "build_context",
    "has_negation_near",
    "has_safe_relation_negation",
    "has_meta_context",
    "is_pattern_declaration",
    "is_forbidden_example_context",
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
