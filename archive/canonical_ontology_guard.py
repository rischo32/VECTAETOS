#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTAETOS :: GUARD-01 CANONICAL ONTOLOGY MODIFICATION GUARD

Encoding posture:
    This file is intentionally ASCII-only in source bytes.
    Canonical symbols are represented through Python Unicode escapes.

Role:
    Fundamental repository perimeter guard for canonical ontology boundaries.

Purpose:
    Mechanically protect canonical ontology files, guard runtime surfaces,
    and core semantic invariants from silent mutation in repository changes.

This guard:
    - reads git diff between base/head
    - detects protected canonical/perimeter path mutations
    - validates the semantic errata registry exception
    - detects mojibake / broken byte-trace artifacts in changed text
    - scans changed active text files for high-risk ontology drift
    - emits shared Finding objects
    - prints deterministic shared reports
    - optionally writes JSON report artifacts
    - fails closed on infrastructure errors

This guard does NOT:
    - redefine Phi
    - evaluate truth
    - optimize anything
    - decide for humans
    - validate deployment
    - claim empirical safety
    - mutate repository files
    - create feedback into Phi

Python:
    3.11+

Dependencies:
    standard library + guards/core shared kernel
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from collections.abc import Iterable
from pathlib import Path

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
    from guards.core.reporting import exit_code_for, print_text_report, write_json
    from guards.core.text_scan import make_rule, scan_text_to_findings
except ModuleNotFoundError:
    from core.findings import (  # type: ignore
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
    from core.perimeter import EnforcementMode  # type: ignore
    from core.reporting import exit_code_for, print_text_report, write_json  # type: ignore
    from core.text_scan import make_rule, scan_text_to_findings  # type: ignore


GUARD_ID = "GUARD-01"
GUARD_FILE = "guards/canonical_ontology_guard.py"
GUARD_NAME = "VECTAETOS Canonical Ontology Boundary"
VERSION = "0.2.1-byte-trace-safe"
CONTRACT_SCHEMA_VERSION = "1.0"

NULL_SHA = "0000000000000000000000000000000000000000"
ERRATA_REGISTRY_PATH = "anchors/SEMANTIC_ERRATA.md"

PHI_SYMBOL = "\u03a6"
KAPPA_SYMBOL = "\u03ba"
SCRIPT_D_SYMBOL = "\U0001d49f"

# Common mojibake markers created when UTF-8 text is decoded as Latin-1/CP1252
# or when replacement characters are introduced.
MOJIBAKE_MARKERS: tuple[str, ...] = (
    "\ufffd",      # replacement character
    "\u00c3",      # mojibake marker
    "\u00c2",      # mojibake marker
    "\u00ce",      # mojibake marker often seen instead of Phi
    "\u0102",      # mojibake marker
    "\u0139",      # mojibake marker
    "\u00e2\u0080",  # mojibake marker
)

ERRATA_REQUIRED_NORMALIZED_MARKERS: tuple[str, ...] = (
    "vectaetos-guard: allow-file",
    "semantic errata anchor",
    "tento dokument nie je nova ontologia",
    "nie je nahrada immutable anchorov",
    "nemeni phi",
    "guardy mozu registrovany historicky drift",
    "neregistrovany drift zostava",
    "aktivne subory sa maju opravit priamo",
)

PROTECTED_PREFIXES: tuple[str, ...] = (
    "anchors/",
    "formal/",
)

SELF_PROTECTED_PATHS: tuple[str, ...] = (
    ".github/workflows/canonical-ontology-guard.yml",
    "guards/canonical_ontology_guard.py",
)

PROTECTED_PATH_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|/)MASTER_INDEX\.md$",
        r"(^|/)VECTAETOS_Specification\.md$",
        r"(^|/)VECTAETOS_v1\.0_Frozen_Ontological_Core\.md$",
        r"(^|/)VECTAETOS.*Formal.*\.md$",
        r"(^|/)FORMALISM.*\.md$",
        r"(^|/)FORMAL_.*\.md$",
        r"(^|/)FORM.*LNE_.*\.md$",
        r"(^|/)CANONICAL.*ANCHOR.*\.md$",
        r"(^|/)KANONICK.*KOTV.*\.md$",
        r"(^|/)MECHANIZATION_OF_.*\.md$",
        r"(^|/)MECHANIZ.*CIA_.*\.md$",
        r"(^|/)EPISTEMIC_TOPOLOGY.*\.md$",
        r"(^|/)EPISTEMIC_LAYER.*\.md$",
        r"(^|/)EPISTEMIC_CRYPTOGRAPHY.*\.md$",
        r"(^|/)ENTROPIC_HUMILITY.*\.md$",
        r"(^|/)INTRINSIC_HUMILITY.*\.md$",
        r"(^|/)PROJECTION_RUNES.*\.md$",
        r"(^|/)TRIADIC_ARCHITECTURE.*\.md$",
        r"(^|/)OAAT.*\.md$",
        r"(^|/)EMPIRICAL_EVIDENCE_ROADMAP.*\.md$",
        r"(^|/)EMPIRICAL_SAFETY_PRIOR.*\.md$",
        r"(^|/)epistemic_space\.md$",
        r"(^|/)epistemick.*_priestor\.md$",
    )
)

SCAN_EXTENSIONS: tuple[str, ...] = (
    ".md",
    ".txt",
    ".html",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
)

SEMANTIC_SCAN_EXCLUDED_PREFIXES: tuple[str, ...] = (
    "guards/",
    ".github/",
    "archive/",
    "docs/archive/",
    "tests/fixtures/",
    "research/guards/",
)

# Encoding scan is intentionally broader than semantic scan.
# It can inspect guard files because byte-trace corruption in guard code is a
# runtime integrity risk.
ENCODING_SCAN_EXCLUDED_PREFIXES: tuple[str, ...] = (
    "archive/",
    "docs/archive/",
    "tests/fixtures/",
    "research/guards/",
)


def normalize_path(path: str | Path) -> str:
    value = str(path).strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def normalize_semantic_text(text: str) -> str:
    text = text.replace(PHI_SYMBOL, " Phi ")
    text = text.replace(KAPPA_SYMBOL, " kappa ")
    text = text.replace(SCRIPT_D_SYMBOL, " D ")
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = decomposed.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.casefold().split())


def is_null_sha(value: str | None) -> bool:
    return value is None or value.strip() == "" or value.strip() == NULL_SHA


def is_errata_registry_path(path: str | Path) -> bool:
    return normalize_path(path) == ERRATA_REGISTRY_PATH


def content_contains_required_errata_markers(content: str) -> bool:
    normalized = normalize_semantic_text(content)
    return all(marker in normalized for marker in ERRATA_REQUIRED_NORMALIZED_MARKERS)


def run_git(args: list[str], *, allow_fail: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(
            f"git {' '.join(args)} failed with exit {result.returncode}:\n"
            f"{result.stderr}"
        )
    return result.stdout


def commit_exists(ref: str) -> bool:
    if is_null_sha(ref):
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def empty_tree_hash() -> str:
    return run_git(["hash-object", "-t", "tree", "/dev/null"]).strip()


def file_exists_at_head(path: str, head: str) -> bool:
    selected_head = "HEAD" if is_null_sha(head) else head
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{selected_head}:{path}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def read_file_at_head(path: str, head: str) -> str:
    selected_head = "HEAD" if is_null_sha(head) else head
    return run_git(["show", f"{selected_head}:{path}"], allow_fail=False)


class ChangedPath:
    __slots__ = ("status", "paths")

    def __init__(self, status: str, paths: tuple[str, ...]) -> None:
        self.status = status
        self.paths = paths


def diff_name_status(base: str, head: str) -> list[ChangedPath]:
    selected_head = "HEAD" if is_null_sha(head) else head
    selected_base = empty_tree_hash() if is_null_sha(base) else base

    if selected_head != "HEAD" and not commit_exists(selected_head):
        raise RuntimeError(f"Head commit is not available in checkout: {selected_head}")

    if selected_base != empty_tree_hash() and not commit_exists(selected_base):
        raise RuntimeError(f"Base commit is not available in checkout: {selected_base}")

    raw = run_git(
        [
            "diff",
            "--name-status",
            "-M",
            "--find-renames",
            selected_base,
            selected_head,
            "--",
        ]
    )

    changes: list[ChangedPath] = []
    for line in raw.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith(("R", "C")):
            if len(parts) >= 3:
                changes.append(
                    ChangedPath(
                        status=status,
                        paths=(normalize_path(parts[1]), normalize_path(parts[2])),
                    )
                )
        elif len(parts) >= 2:
            changes.append(
                ChangedPath(
                    status=status,
                    paths=(normalize_path(parts[1]),),
                )
            )

    return changes


def path_is_protected(path: str | Path) -> bool:
    repo_path = normalize_path(path)

    if repo_path in SELF_PROTECTED_PATHS:
        return True

    if repo_path.startswith(PROTECTED_PREFIXES):
        return True

    return any(pattern.search(repo_path) for pattern in PROTECTED_PATH_PATTERNS)


def path_has_scan_extension(path: str | Path) -> bool:
    return Path(normalize_path(path)).suffix.lower() in SCAN_EXTENSIONS


def path_should_be_semantically_scanned(path: str | Path) -> bool:
    repo_path = normalize_path(path)

    if any(repo_path.startswith(prefix) for prefix in SEMANTIC_SCAN_EXCLUDED_PREFIXES):
        return False

    return path_has_scan_extension(repo_path)


def path_should_be_encoding_scanned(path: str | Path) -> bool:
    repo_path = normalize_path(path)

    if any(repo_path.startswith(prefix) for prefix in ENCODING_SCAN_EXCLUDED_PREFIXES):
        return False

    return path_has_scan_extension(repo_path)


def vector_for_encoding_path(path: str | Path) -> DriftVector:
    repo_path = normalize_path(path)
    if repo_path.startswith(("guards/", ".github/")):
        return DriftVector.V15_GUARD_RUNTIME_INTEGRITY
    if repo_path.startswith(("anchors/", "formal/")):
        return DriftVector.V14_ANCHOR_INTEGRITY_DRIFT
    return DriftVector.V12_ONTOLOGY_CREEP


def ontology_finding(
    *,
    rule_id: str,
    path: str | Path,
    message: str,
    severity: Severity = Severity.BLOCKER,
    confidence: Confidence = Confidence.HIGH,
    line: int | None = None,
    column: int | None = None,
    observed_pattern: str | None = None,
    protected_object: str | None = None,
    vector: DriftVector = DriftVector.V14_ANCHOR_INTEGRITY_DRIFT,
    forbidden_conversion: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    return make_finding(
        guard_id=GUARD_ID,
        guard_file=GUARD_FILE,
        rule_id=rule_id,
        contract_schema_version=CONTRACT_SCHEMA_VERSION,
        level=PerimeterLevel.LEVEL_0,
        scope=PerimeterScope.FUNDAMENTAL_REPOSITORY,
        vector=vector,
        severity=severity,
        confidence=confidence,
        path=normalize_path(path),
        line=line,
        column=column,
        message=message,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        forbidden_conversion=forbidden_conversion,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.FAIL_CLOSED,
        integrity_posture=IntegrityPosture.IMMUTABLE_ANCHOR,
        anchor_ref="MASTER_INDEX.md",
        contract_ref="contracts/perimeter_manifest.json",
        safer_form=safer_form,
    )


def validate_errata_registry_at_head(path: str, head: str) -> list[Finding]:
    if not is_errata_registry_path(path):
        return []

    if not file_exists_at_head(path, head):
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-MISSING",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md is a registered semantic errata "
                    "anchor and must not be deleted or moved away from anchors/."
                ),
                protected_object="semantic_errata_registry",
                safer_form=(
                    "Restore anchors/SEMANTIC_ERRATA.md with its required "
                    "registry markers."
                ),
            )
        ]

    try:
        content = read_file_at_head(path, head)
    except RuntimeError as exc:
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-UNREADABLE",
                path=path,
                message=f"Cannot read semantic errata registry at HEAD: {exc}",
                protected_object="semantic_errata_registry",
            )
        ]

    if not content_contains_required_errata_markers(content):
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-INVALID",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md may contain forbidden historical "
                    "phrases only if it preserves explicit errata registry clauses."
                ),
                protected_object="semantic_errata_registry",
                safer_form=(
                    "Keep errata as registry-only text; do not convert errata "
                    "into active ontology."
                ),
            )
        ]

    return []


def semantic_scan_is_exempt(path: str, content: str) -> bool:
    return is_errata_registry_path(path) and content_contains_required_errata_markers(content)


def detect_protected_file_changes(
    changes: Iterable[ChangedPath],
    head: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for change in changes:
        for path in change.paths:
            if is_errata_registry_path(path):
                findings.extend(validate_errata_registry_at_head(path, head))
                continue

            if path_is_protected(path):
                findings.append(
                    ontology_finding(
                        rule_id="CANONICAL-FILE-MUTATION",
                        path=path,
                        message=(
                            "Protected canonical/perimeter path changed "
                            f"(git status {change.status})."
                        ),
                        observed_pattern=f"git_status={change.status}",
                        protected_object="canonical_or_perimeter_path",
                        safer_form=(
                            "Canonical anchors and guard runtime surfaces require "
                            "explicit reviewed process."
                        ),
                    )
                )

    return findings


def first_mojibake_marker(line: str) -> tuple[str, int] | None:
    for marker in MOJIBAKE_MARKERS:
        index = line.find(marker)
        if index >= 0:
            return marker, index
    return None


def detect_byte_trace_drift(changes: Iterable[ChangedPath], head: str) -> list[Finding]:
    findings: list[Finding] = []
    unique_paths = sorted({path for change in changes for path in change.paths})

    for path in unique_paths:
        if not path_should_be_encoding_scanned(path):
            continue

        if not file_exists_at_head(path, head):
            continue

        try:
            content = read_file_at_head(path, head)
        except RuntimeError:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            marker = first_mojibake_marker(line)
            if marker is None:
                continue

            _marker_text, marker_index = marker
            excerpt = line.strip()
            if len(excerpt) > 240:
                excerpt = excerpt[:239] + "..."

            findings.append(
                ontology_finding(
                    rule_id="BYTE-TRACE-MOJIBAKE",
                    path=path,
                    message=(
                        "Broken byte trace / mojibake marker detected in changed "
                        "text. Repository source must remain valid UTF-8 text."
                    ),
                    line=line_number,
                    column=marker_index + 1,
                    observed_pattern=excerpt,
                    protected_object="repository_text_encoding",
                    vector=vector_for_encoding_path(path),
                    forbidden_conversion="UTF-8 source text -> mojibake / replacement-character drift",
                    safer_form=(
                        "Rewrite the affected file from a clean UTF-8 source. "
                        "Do not repair by semantic guessing."
                    ),
                )
            )
            break

    return findings


def join_terms(terms: tuple[str, ...]) -> str:
    return "(?:" + "|".join(re.escape(term) for term in terms) + ")"


def near(left: str, right: str, width: int = 100) -> str:
    return f"(?:{left}.{{0,{width}}}{right}|{right}.{{0,{width}}}{left})"


PHI_TOKEN = rf"(?:{re.escape(PHI_SYMBOL)}|Phi|PHI|phi)"
K_TOKEN = (
    rf"(?:K\s*\(\s*{re.escape(PHI_SYMBOL)}\s*\)"
    r"|K\s*\(\s*Phi\s*\)"
    r"|K\s*\(\s*PHI\s*\)"
    r"|KPhi|K_Phi)"
)
KAPPA_TOKEN = rf"(?:{re.escape(KAPPA_SYMBOL)}|kappa|\\kappa)"
QE_TOKEN = r"(?:QE|Qualitative Epistemic Aporia)"
AUDIT_TOKEN = r"(?:audit|EK|Epistemic Cryptography)"
PROJECTION_TOKEN = r"(?:projection|projekcia|runes?|runy|glyph|TetraGlyph)"
LLM_TOKEN = r"(?:LLM|language model|jazykovy model|jazykov\S+ model)"
VORTEX_TOKEN = r"(?:Vortex|Simulation Vortex|Simula\S+\s+Vortex)"
MEMORY_TOKEN = r"(?:memory|pamat|pam\S+|ESM|LTL|MML)"

PHI_AGENT_TERMS = (
    "agent",
    "planner",
    "controller",
    "decision-maker",
    "decision maker",
    "rozhoduje",
    "kona",
    "kon",
    "planuje",
    "plan",
    "riadi",
)
PHI_OPTIMIZATION_TERMS = (
    "optimiz",
    "optimaliz",
    "reward",
    "ciel",
    "goal",
    "target",
)
K_SCORE_TERMS = (
    "score",
    "skore",
    "metric",
    "metrika",
    "reward",
    "target",
    "ciel",
    "optimaliz",
)
KAPPA_PARAMETER_TERMS = (
    "parameter",
    "param",
    "threshold",
    "prah",
    "cislo",
    "number",
    "metric",
    "metrika",
    "tunable",
    "nastav",
)
QE_ERROR_TERMS = (
    "error",
    "bug",
    "chyba",
    "fallback",
    "exception",
    "failure",
    "zlyhan",
)
AUDIT_COMMAND_TERMS = (
    "command",
    "commands",
    "control",
    "controls",
    "riadi",
    "blokuje",
    "decides",
    "decide",
    "rozhoduje",
    "intervenes",
    "intervene",
    "zasahuje",
)
PROJECTION_INTERPRETS_TERMS = (
    "interprets",
    "interpret",
    "interpretuje",
    "decides",
    "decide",
    "rozhoduje",
    "prescribes",
    "prescribe",
    "predpisuje",
)
LLM_AUTHORITY_TERMS = (
    "authority",
    "autorita",
    "truth",
    "pravda",
    "decides",
    "decide",
    "rozhoduje",
    "validates",
    "validate",
    "validuje",
)
VORTEX_SELECTS_TERMS = (
    "selects",
    "select",
    "chooses",
    "choose",
    "vybera",
    "zvoli",
    "best",
    "najleps",
    "optimizes",
    "optimize",
    "optimaliz",
)
MEMORY_REWRITE_TERMS = (
    "rewrites",
    "rewrite",
    "modifies",
    "modify",
    "meni",
    "prepisuje",
    "updates ontology",
    "uci Phi",
    "trains Phi",
)
L4_OVERCLAIM_LEFT = (
    "safe",
    "bezpecny",
    "bezpecna",
    "bezpecne",
    "validated",
    "validovany",
    "validovana",
    "validovane",
    "deployment-ready",
    "deployment ready",
    "legitimate",
    "legitimny",
    "legitimna",
)
L4_OVERCLAIM_RIGHT = (
    "without L4",
    "bez L4",
    "bez empirick",
    "L0",
    "L1",
    "L2",
    "L3",
)


def build_semantic_rules() -> list:
    common = {
        "level": PerimeterLevel.LEVEL_0,
        "scope": PerimeterScope.FUNDAMENTAL_REPOSITORY,
        "confidence": Confidence.HIGH,
        "evidence_class_allowed": EvidenceClass.E1_STATIC_SCAN,
        "enforcement_mode": EnforcementMode.FAIL_CLOSED,
        "integrity_posture": IntegrityPosture.IMMUTABLE_ANCHOR,
        "anchor_ref": "MASTER_INDEX.md",
        "contract_ref": "contracts/perimeter_manifest.json",
    }

    return [
        make_rule(
            rule_id="PHI-AGENT",
            pattern=near(PHI_TOKEN, join_terms(PHI_AGENT_TERMS), width=80),
            message="Phi must not be framed as agent, planner, controller, or decision subject.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Phi",
            forbidden_conversion="Phi -> agent / planner / controller / decision subject",
            safer_form="Use Phi only as non-agentic relational epistemic field language.",
            **common,
        ),
        make_rule(
            rule_id="PHI-OPTIMIZATION",
            pattern=near(PHI_TOKEN, join_terms(PHI_OPTIMIZATION_TERMS), width=80),
            message="Phi must not be framed as optimization, reward, goal, or target mechanism.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Phi",
            forbidden_conversion="Phi -> optimizer / reward / goal / target",
            safer_form="Use Phi as field ontology, not as optimization mechanism.",
            **common,
        ),
        make_rule(
            rule_id="K-SCORE",
            pattern=near(K_TOKEN, join_terms(K_SCORE_TERMS), width=80),
            message="K(Phi) must not be framed as score, metric, reward, or optimization target.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="K(Phi)",
            forbidden_conversion="K(Phi) -> score / metric / reward / target",
            safer_form="Use K(Phi) as ontological representability predicate.",
            **common,
        ),
        make_rule(
            rule_id="KAPPA-PARAMETER",
            pattern=near(KAPPA_TOKEN, join_terms(KAPPA_PARAMETER_TERMS), width=80),
            message="kappa must not be framed as tunable parameter, number, threshold, or metric.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="kappa",
            forbidden_conversion="kappa -> parameter / number / threshold / metric",
            safer_form="Use kappa as boundary of ontological preservability / representability.",
            **common,
        ),
        make_rule(
            rule_id="QE-ERROR",
            pattern=near(QE_TOKEN, join_terms(QE_ERROR_TERMS), width=80),
            message="QE must not be framed as ordinary error, fallback, exception, or failure.",
            vector=DriftVector.V9_SILENCE_QE_COERCION,
            severity=Severity.HARD,
            protected_object="QE",
            forbidden_conversion="QE -> error / fallback / exception / failure",
            safer_form="Use QE as active epistemic aporia / non-representability language.",
            **common,
        ),
        make_rule(
            rule_id="AUDIT-COMMAND",
            pattern=near(AUDIT_TOKEN, join_terms(AUDIT_COMMAND_TERMS), width=80),
            message="Audit/EK must not be framed as command, control, decision, or intervention layer.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="audit/EK",
            forbidden_conversion="audit/EK -> command / control / decision / intervention",
            safer_form="Use audit/EK as read-only structural trace / observation layer.",
            **common,
        ),
        make_rule(
            rule_id="PROJECTION-INTERPRETS",
            pattern=near(PROJECTION_TOKEN, join_terms(PROJECTION_INTERPRETS_TERMS), width=80),
            message="Projection/runes/glyphs must not be framed as interpreting, deciding, or prescribing.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="projection",
            forbidden_conversion="projection -> interpretation / prescription / decision",
            safer_form="Use projection as read-only structural exposure.",
            **common,
        ),
        make_rule(
            rule_id="LLM-AUTHORITY",
            pattern=near(LLM_TOKEN, join_terms(LLM_AUTHORITY_TERMS), width=80),
            message="LLM must not be framed as truth, decision, validation, or authority layer.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="LLM",
            forbidden_conversion="LLM -> truth authority / decision authority / validator",
            safer_form="Use LLM only as linguistic adapter / renderer.",
            **common,
        ),
        make_rule(
            rule_id="VORTEX-SELECTS-BEST",
            pattern=near(VORTEX_TOKEN, join_terms(VORTEX_SELECTS_TERMS), width=100),
            message="Vortex must not be framed as selector of best trajectory or optimizer.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Simulation Vortex",
            forbidden_conversion="Vortex -> selector / optimizer / best-path chooser",
            safer_form="Use Vortex only as non-agentic candidate-trajectory exposure layer.",
            **common,
        ),
        make_rule(
            rule_id="MEMORY-REWRITES-ONTOLOGY",
            pattern=near(MEMORY_TOKEN, join_terms(MEMORY_REWRITE_TERMS), width=100),
            message="Memory layers must not be framed as modifying ontology, Phi, or Vortex.",
            vector=DriftVector.V1_UPWARD_MUTATION,
            severity=Severity.HARD,
            protected_object="memory layers",
            forbidden_conversion="memory -> ontology updater / Phi trainer / Vortex modifier",
            safer_form="Use memory layers as descriptive audit/state records only.",
            **common,
        ),
        make_rule(
            rule_id="L4-OVERCLAIM",
            pattern=near(join_terms(L4_OVERCLAIM_LEFT), join_terms(L4_OVERCLAIM_RIGHT), width=120),
            message="Without replicated L4 evidence, safety, deployment legitimacy, or full validation must not be claimed.",
            vector=DriftVector.V4_EVIDENCE_OVERCLAIM,
            severity=Severity.HARD,
            protected_object="empirical evidence posture",
            forbidden_conversion="L0-L3 evidence -> L4 / safety / deployment validity claim",
            safer_form="Say: no configured blocker detected within declared perimeter.",
            **common,
        ),
    ]


def detect_semantic_drift(changes: Iterable[ChangedPath], head: str) -> list[Finding]:
    findings: list[Finding] = []
    unique_paths = sorted({path for change in changes for path in change.paths})
    rules = build_semantic_rules()

    for path in unique_paths:
        if not path_should_be_semantically_scanned(path):
            continue

        if not file_exists_at_head(path, head):
            continue

        try:
            content = read_file_at_head(path, head)
        except RuntimeError:
            continue

        if semantic_scan_is_exempt(path, content):
            continue

        findings.extend(
            scan_text_to_findings(
                path=path,
                text=content,
                rules=rules,
                guard_id=GUARD_ID,
                guard_file=GUARD_FILE,
                contract_schema_version=CONTRACT_SCHEMA_VERSION,
                skip_safe_context=True,
            )
        )

    return findings


def emit_github_annotation(finding: Finding) -> None:
    command = "warning" if finding.severity == Severity.WARN else "error"
    safe_message = finding.message.replace("%", "%25")
    safe_message = safe_message.replace("\r", "%0D").replace("\n", "%0A")
    safe_path = str(finding.path).replace("\n", "")

    if finding.line is not None:
        print(
            f"::{command} file={safe_path},line={finding.line},title={finding.rule_id}::{safe_message}"
        )
    else:
        print(f"::{command} file={safe_path},title={finding.rule_id}::{safe_message}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS canonical ontology repository guard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--base", required=True, help="Base commit SHA or null SHA.")
    parser.add_argument("--head", required=True, help="Head commit SHA.")
    parser.add_argument(
        "--mode",
        choices=("strict", "report"),
        default="strict",
        help="Strict exits non-zero on findings; report only prints findings.",
    )
    parser.add_argument("--json-out", default=None, help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    base = args.base.strip()
    head = args.head.strip() or "HEAD"
    title = f"{GUARD_ID} / {GUARD_NAME} v{VERSION}"
    fail_on = Severity.HARD

    try:
        changes = diff_name_status(base, head)
        findings: list[Finding] = []

        findings.extend(detect_protected_file_changes(changes, head))
        findings.extend(detect_byte_trace_drift(changes, head))
        findings.extend(detect_semantic_drift(changes, head))

        for finding in findings:
            emit_github_annotation(finding)

        print(f"Changed entries scanned: {len(changes)}")
        print_text_report(
            findings,
            title=title,
            mode=args.mode,
            fail_on=fail_on,
            root=Path.cwd(),
        )

        if args.json_out:
            try:
                write_json(Path(args.json_out), findings)
            except OSError as exc:
                print(f"ERROR: cannot write JSON report: {exc}", file=sys.stderr)
                return 2

        if args.mode == "strict":
            return exit_code_for(findings, fail_on=fail_on)

        return 0

    except Exception as exc:
        print("::error title=GUARD-RUNTIME-ERROR::Canonical ontology guard failed internally.")
        print("")
        print("GUARD-RUNTIME-ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: guard runtime error blocks the check.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
