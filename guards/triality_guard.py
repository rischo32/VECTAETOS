#!/usr/bin/env python3
"""
VECTAETOS :: Triality Guard

Version:
    0.1.0

Guard Class:
    Level 1 — Specialized Ontological Guard

Role:
    Protects triality / OAAT semantics.

Purpose:
    Detects semantic drift where triality is framed as:
    - a selector of the best axis,
    - an optimizer,
    - a decision authority,
    - a symmetry/equality claim between non-equivalent layers,
    - a collapse into dyad, monad, or flat stack,
    - a mechanism that redefines Φ, K(Φ), κ, QE, Vortex, audit, projection, or LLM role.

Canonical boundary:
    Triality expresses irreducible plurality and ontological asymmetry.
    It does not choose, optimize, rank, decide, command, or collapse layers.

Non-role:
    - does not define ontology
    - does not validate deployment
    - does not prove safety
    - does not modify files
    - does not change Φ, K(Φ), κ, QE, Vortex, audit, projection, or LLM role

Python:
    3.11+

Run from:
    repository root

Modes:
    report = print findings and exit 0
    strict = exit 1 on HARD findings

Exit codes:
    0 = clean / report-only findings
    1 = hard findings in strict mode
    2 = execution/config error
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
from pathlib import Path
from typing import Iterable


VERSION = "0.1.0"

INCLUDE_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".html",
    ".css",
    ".js",
    ".ts",
}

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    "archive",
    ".runtime",
}

EXCLUDED_PATH_PARTS = {
    ("docs", "observatory"),
}

EXCLUDED_FILES = {
    "guards/triality_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-triality-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-triality-allow-file",
    "vectaetos-guard: allow-file",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|not a selector|not selector|not optimizer|not optimization|"
    r"not decision|does not decide|does not choose|does not select|"
    r"does not rank|not authority|not symmetrical|not equivalent|"
    r"ontologically asymmetric|non-equivalent|non equivalent|irreducible plurality|"
    r"nesmie|nesmú|nesmu|nie je|bez|zakázané|zakazane|zákaz|zakaz|"
    r"nerozhoduje|nevyberá|nevybera|neoptimalizuje|nerankuje|"
    r"nie je autorita|nie sú ekvivalentné|nie su ekvivalentne|"
    r"ontologicky asymetrick|neekvivalentn|iredukovateľn|iredukovateln|"
    r"report-only|diagnosis|guard|detects|scan|drift|"
    r"forbidden pattern|example failure|compatibility test"
    r")",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|bez|nie je|žiadny|ziadny|žiadna|ziadna|"
    r"nerozhoduje|nevyberá|nevybera|neoptimalizuje|nerankuje|nekolabuje"
    r")\b",
    re.IGNORECASE | re.UNICODE,
)


@dataclasses.dataclass(frozen=True)
class Rule:
    code: str
    severity: str
    pattern: re.Pattern[str]
    reason: str
    safer_form: str


@dataclasses.dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    line: str
    rule: Rule


def compile_rule(
    code: str,
    severity: str,
    pattern: str,
    reason: str,
    safer_form: str,
) -> Rule:
    return Rule(
        code=code,
        severity=severity,
        pattern=re.compile(pattern, re.IGNORECASE | re.UNICODE),
        reason=reason,
        safer_form=safer_form,
    )


TRIALITY_SUBJECTS = (
    r"triality|triadic architecture|triad|OAAT|Ontologically Asymmetric Architectural Triality|"
    r"trialita|triadická architektúra|triadicka architektura|triáda|triada|"
    r"ontologicky asymetrická architektonická trialita|ontologicky asymetricka architektonicka trialita"
)

ROOT_TERMS = (
    r"Φ|Phi|K\(Φ\)|K\(Phi\)|κ|kappa|QE|Vortex|audit|projection|projekcia|"
    r"ontology|ontológia|ontologia|LLM"
)

RULES: list[Rule] = [
    compile_rule(
        code="TRIALITY_AS_SELECTOR",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,180}}\b("
            r"selects|select|chooses|choose|picks|picks the best|best axis|preferred axis|"
            r"vyberá|vybera|vyberie|zvolí|zvoli|najlepšia os|najlepsia os|preferovaná os|preferovana os"
            r")\b"
        ),
        reason="Triality must not be framed as selecting or preferring one axis.",
        safer_form="Use: triality expresses absence of privileged representational axis.",
    ),
    compile_rule(
        code="TRIALITY_AS_OPTIMIZER",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,180}}\b("
            r"optimizes|optimize|optimization target|maximizes|minimizes|converges to|"
            r"optimal path|optimal axis|"
            r"optimalizuje|optimalizácia|optimalizacia|maximalizuje|minimalizuje|"
            r"konverguje k|optimálna cesta|optimalna cesta|optimálna os|optimalna os"
            r")\b"
        ),
        reason="Triality must not be framed as optimization.",
        safer_form="Use: triality is a structural invariance/asymmetry condition, not an optimizer.",
    ),
    compile_rule(
        code="TRIALITY_AS_DECISION_AUTHORITY",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,180}}\b("
            r"decides|decision authority|decides validity|decides truth|commands|controls|governs|"
            r"rozhoduje|autorita rozhodovania|rozhoduje platnosť|rozhoduje platnost|"
            r"rozhoduje pravdu|prikazuje|riadi|kontroluje"
            r")\b"
        ),
        reason="Triality must not become a decision or command authority.",
        safer_form="Use: triality exposes structural relation; it does not decide.",
    ),
    compile_rule(
        code="TRIALITY_FLATTENED_SYMMETRY",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,200}}\b("
            r"all layers are equal|layers are equivalent|symmetrical layers|same ontological status|"
            r"flat stack|equivalent roots|three roots|"
            r"všetky vrstvy sú rovnaké|vsetky vrstvy su rovnake|vrstvy sú ekvivalentné|"
            r"vrstvy su ekvivalentne|symetrické vrstvy|symetricke vrstvy|"
            r"rovnaký ontologický status|rovnaky ontologicky status|plochý stack|plochy stack|"
            r"ekvivalentné rooty|ekvivalentne rooty|tri rooty"
            r")\b"
        ),
        reason="OAAT requires ontological asymmetry; downstream layers are not equivalent roots.",
        safer_form="Use: one architecture, ontologically non-equivalent layers; VECTAETOS remains root.",
    ),
    compile_rule(
        code="TRIALITY_COLLAPSE_TO_DYAD_OR_MONAD",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,200}}\b("
            r"collapse into dyad|collapse into monad|reduce to dyad|reduce to monad|"
            r"only two layers|single layer architecture|one layer only|monolithic root|"
            r"kolaps do dyády|kolaps do dyady|kolaps do monády|kolaps do monady|"
            r"redukovať na dyádu|redukovat na dyadu|redukovať na monádu|redukovat na monadu|"
            r"iba dve vrstvy|jednovrstvová architektúra|jednovrstvova architektura|monolitický root|monoliticky root"
            r")\b"
        ),
        reason="Triality must preserve irreducible triadic plurality.",
        safer_form="Use: VECTAETOS / ASIMULATOR / ASI_MOD remain distinct and non-collapsed.",
    ),
    compile_rule(
        code="DOWNSTREAM_REDEFINES_TRIALITY_ROOT",
        severity="HARD",
        pattern=(
            r"\b(ASIMULATOR|ASI_MOD)\b.{0,180}\b("
            r"defines triality|redefines triality|defines OAAT|redefines OAAT|"
            r"defines VECTAETOS|redefines VECTAETOS|"
            r"definuje trialitu|redefinuje trialitu|definuje OAAT|redefinuje OAAT|"
            r"definuje VECTAETOS|redefinuje VECTAETOS"
            r")\b"
        ),
        reason="Downstream layers may reference triality but must not define the root architecture.",
        safer_form="Use: VECTAETOS defines the root; ASIMULATOR/ASI_MOD are downstream articulations.",
    ),
    compile_rule(
        code="TRIALITY_REDEFINES_CANONICAL_TERMS",
        severity="HARD",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,180}}\b("
            r"redefines|overrides|changes|modifies|rewrites|validates|"
            r"redefinuje|prepisuje|mení|meni|modifikuje|validuje"
            r")\b.{{0,120}}\b({ROOT_TERMS})\b"
        ),
        reason="Triality must not be framed as modifying canonical VECTAETOS terms.",
        safer_form="Use: triality is a structural relation; canonical terms remain anchored.",
    ),
    compile_rule(
        code="TRIALITY_AS_RUNTIME_MECHANISM",
        severity="WARN",
        pattern=(
            rf"\b({TRIALITY_SUBJECTS})\b.{{0,180}}\b("
            r"runtime mechanism|runtime selector|runtime validator|execution engine|"
            r"mechanizmus za behu|runtime mechanizmus|runtime selektor|runtime validator|vykonávací engine|vykonavaci engine"
            r")\b"
        ),
        reason="Triality should not be casually framed as a runtime mechanism.",
        safer_form="Use: triality is an architectural/ontological structural condition.",
    ),
]


def normalize_repo_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def has_allow_marker(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in ALLOW_MARKERS)


def file_has_allow_marker(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20]).lower()
    return any(marker in head for marker in FILE_ALLOW_MARKERS)


def is_path_excluded(path: Path, root: Path) -> bool:
    rel = normalize_repo_path(path, root)

    if rel in EXCLUDED_FILES:
        return True

    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts

    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return True

    for excluded_parts in EXCLUDED_PATH_PARTS:
        if len(rel_parts) < len(excluded_parts):
            continue

        for idx in range(0, len(rel_parts) - len(excluded_parts) + 1):
            if tuple(rel_parts[idx : idx + len(excluded_parts)]) == excluded_parts:
                return True

    return False


def iter_candidate_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue

        if is_path_excluded(path, root):
            continue

        if path.suffix.lower() not in INCLUDE_SUFFIXES:
            continue

        yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None
    except OSError as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}") from exc


def is_meta_or_negated_context(context: str, line: str) -> bool:
    if "≠" in line:
        return True

    if META_CONTEXT_PATTERN.search(context):
        return True

    if NEGATION_PATTERN.search(line):
        return True

    return False


def scan_file(path: Path, root: Path) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []

    if file_has_allow_marker(text):
        return []

    lines = text.splitlines()
    findings: list[Finding] = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        if has_allow_marker(stripped):
            continue

        window_start = max(0, idx - 20)
        context = "\n".join(lines[window_start:idx])

        for rule in RULES:
            if not rule.pattern.search(stripped):
                continue

            if is_meta_or_negated_context(context, stripped):
                continue

            findings.append(
                Finding(
                    path=path,
                    line_no=idx,
                    line=stripped,
                    rule=rule,
                )
            )

    return findings


def print_findings(findings: list[Finding], root: Path) -> None:
    hard_count = sum(1 for finding in findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in findings if finding.rule.severity == "WARN")

    print(f"VECTAETOS Triality Guard v{VERSION}")
    print("===================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no triality/OAAT drift detected.")
        return

    for finding in findings:
        rel = normalize_repo_path(finding.path, root)

        print(f"[{finding.rule.severity}] {finding.rule.code}")
        print(f"  file: {rel}:{finding.line_no}")
        print(f"  line: {finding.line}")
        print(f"  why:  {finding.rule.reason}")
        print(f"  use:  {finding.rule.safer_form}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect VECTAETOS triality / OAAT semantic drift."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current working directory.",
    )
    parser.add_argument(
        "--mode",
        choices=("report", "strict"),
        default="report",
        help="report exits 0; strict exits 1 on hard findings.",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Treat warnings as failures in strict mode.",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []

    try:
        for file_path in iter_candidate_files(root):
            findings.extend(scan_file(file_path, root))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    findings.sort(key=lambda item: (str(item.path), item.line_no, item.rule.code))
    print_findings(findings, root)

    if args.mode == "report":
        return 0

    hard_count = sum(1 for finding in findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in findings if finding.rule.severity == "WARN")

    if hard_count > 0:
        return 1

    if args.warnings_as_errors and warn_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
