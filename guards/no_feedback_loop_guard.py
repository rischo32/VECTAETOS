#!/usr/bin/env python3
"""
VECTAETOS :: No Feedback Loop Guard

Version:
    0.1.0

Guard Class:
    Level 0 — Fundamental Repository Perimeter

Role:
    Protects the acyclic architecture of VECTAETOS.

Purpose:
    Detects semantic or technical formulations where output, projection,
    audit, memory, observatory, LLM, reports, logs, or downstream layers
    are framed as writing back into Φ, ontology, K(Φ), κ, QE, Vortex,
    canonical anchors, or root meaning.

Detects:
    - feedback loops into Φ
    - output/write-back into ontology
    - audit command/control feedback
    - projection write-back
    - memory modifying root ontology
    - LLM or dialogue rewriting canonical state
    - observatory auto-PR / auto-commit patterns as warning signals

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
    "guards/no_feedback_loop_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-no-feedback-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-no-feedback-allow-file",
    "vectaetos-guard: allow-file",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|no feedback|no feedback loop|without feedback|no write-back|no writeback|"
    r"read-only|observe only|record only|hash only|descriptive only|"
    r"external to|not part of|not authority|not command|not control|"
    r"nesmie|nesmú|nesmu|nie je|bez|zakázané|zakazane|zákaz|zakaz|"
    r"bez spätnej slučky|bez spatnej slucky|bez spätného zápisu|bez spatneho zapisu|"
    r"nepíše späť|nepise spat|iba pozoruje|iba zapisuje|iba hashuje|"
    r"read only|readonly|report-only|diagnosis|guard|detects|scan|drift|"
    r"forbidden pattern|example failure|compatibility test"
    r")",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|bez|nie je|žiadny|ziadny|žiadna|ziadna|"
    r"nepíše|nepise|nemení|nemeni|neprepisuje|neriadi|nerozhoduje"
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


SOURCE_LAYER = (
    r"output|result|response|LLM|dialogue|dialog|projection|projections|projekcia|projekcie|"
    r"rune|runes|runa|runy|glyph|glyphs|TetraGlyph|audit|EK|Epistemic Cryptography|"
    r"observatory|report|log|ledger|memory|pamäť|pamat|ESM|LTL|MML|ASI_MOD|ASIMULATOR"
)

ROOT_TARGET = (
    r"Φ|Phi|field|pole|ontology|ontológia|ontologia|K\(Φ\)|K\(Phi\)|K\(\s*Φ\s*\)|"
    r"κ|kappa|QE|Vortex|canonical anchor|root anchor|anchor|formal meaning|root meaning"
)

WRITEBACK_VERBS = (
    r"writes back|write back|feeds back|feed back|loops back|updates|changes|modifies|"
    r"rewrites|redefines|controls|commands|governs|overrides|corrects|learns into|"
    r"píše späť|pise spat|spätne zapisuje|spatne zapisuje|vracia späť|vracia spat|"
    r"aktualizuje|mení|meni|modifikuje|prepisuje|redefinuje|riadi|prikazuje|"
    r"kontroluje|prebíja|prebija|opravuje|učí do|uci do"
)

RULES: list[Rule] = [
    compile_rule(
        code="GENERAL_FEEDBACK_INTO_ROOT",
        severity="HARD",
        pattern=rf"\b({SOURCE_LAYER})\b.{{0,160}}\b({WRITEBACK_VERBS})\b.{{0,120}}\b({ROOT_TARGET})\b",
        reason="No downstream/output/audit/projection/memory layer may write back into the root ontology.",
        safer_form="Use: acyclic descriptive flow; downstream layers may observe or render, not rewrite Φ or root meaning.",
    ),
    compile_rule(
        code="ROOT_FEEDBACK_ARROW",
        severity="HARD",
        pattern=(
            r"\b(output|response|projection|audit|memory|LLM|ASI_MOD|ASIMULATOR|observatory|report)\b"
            r"\s*(-?>|→|=>|-->)\s*"
            r"\b(Φ|Phi|ontology|K\(Φ\)|K\(Phi\)|κ|kappa|QE|Vortex|anchor)\b"
        ),
        reason="Arrow notation suggests a reverse flow into root structures.",
        safer_form="Use forward acyclic flow only; no downstream-to-root arrow.",
    ),
    compile_rule(
        code="AUDIT_COMMAND_FEEDBACK",
        severity="HARD",
        pattern=(
            r"\b(audit|EK|Epistemic Cryptography|ledger|log)\b.{0,160}\b("
            r"controls|commands|feeds back into|writes back into|updates|modifies|overrides|"
            r"riadi|prikazuje|vracia späť do|vracia spat do|píše späť do|pise spat do|"
            r"aktualizuje|modifikuje|prepisuje"
            r")\b.{0,100}\b(Φ|Phi|field|ontology|K\(Φ\)|κ|kappa|QE|Vortex)\b"
        ),
        reason="Audit/EK/logs may observe, record, hash, or report only.",
        safer_form="Use: audit observes / records / hashes / reports; ∂Φ/∂Audit = 0.",
    ),
    compile_rule(
        code="PROJECTION_WRITEBACK_FEEDBACK",
        severity="HARD",
        pattern=(
            r"\b(projection|projekcia|rune|runa|runy|glyph|TetraGlyph)\b.{0,160}\b("
            r"writes back|feeds back|updates|modifies|rewrites|changes|"
            r"píše späť|pise spat|vracia späť|vracia spat|aktualizuje|modifikuje|prepisuje|mení|meni"
            r")\b.{0,100}\b(Φ|Phi|field|ontology|K\(Φ\)|κ|kappa|QE|Vortex)\b"
        ),
        reason="Projection/rune/glyph layer must remain read-only and non-intervention.",
        safer_form="Use: projection exposes descriptive structural state without backward influence.",
    ),
    compile_rule(
        code="MEMORY_ROOT_WRITEBACK",
        severity="HARD",
        pattern=(
            r"\b(memory|pamäť|pamat|ESM|LTL|MML)\b.{0,160}\b("
            r"updates|changes|modifies|rewrites|redefines|feeds back into|writes back into|"
            r"aktualizuje|mení|meni|modifikuje|prepisuje|redefinuje|vracia späť do|vracia spat do"
            r")\b.{0,100}\b(Φ|Phi|ontology|K\(Φ\)|κ|kappa|QE|Vortex|canonical anchor|root anchor)\b"
        ),
        reason="Memory may provide controlled continuity but must not become ontological authority.",
        safer_form="Use: memory is descriptive/anchored continuity; it does not alter Φ, K(Φ), κ, QE, or anchors.",
    ),
    compile_rule(
        code="LLM_BACKWARD_AUTHORITY",
        severity="HARD",
        pattern=(
            r"\b(LLM|language adapter|jazykový adaptér|jazykovy adapter|dialogue|dialog)\b.{0,160}\b("
            r"updates ontology|rewrites ontology|defines Φ|defines Phi|changes K|changes kappa|changes QE|"
            r"aktualizuje ontológiu|aktualizuje ontologiu|prepisuje ontológiu|prepisuje ontologiu|"
            r"definuje Φ|definuje Phi|mení K|meni K|mení kappa|meni kappa|mení QE|meni QE"
            r")\b"
        ),
        reason="LLM is a language adapter, not a source of ontological authority.",
        safer_form="Use: LLM parses/renders language only; it does not modify root ontology.",
    ),
    compile_rule(
        code="OBSERVATORY_REPO_WRITEBACK",
        severity="WARN",
        pattern=(
            r"\b(observatory|projection update|runtime projection)\b.{0,200}\b("
            r"git commit|git push|gh pr create|pull request|auto branch|auto/observatory|"
            r"automaticky commit|automatický commit|automaticky push|otvára pull request|otvara pull request"
            r")\b"
        ),
        reason="Observatory auto-writeback may create a repository feedback loop.",
        safer_form="Use runtime-only output under .runtime/ unless a human explicitly persists documentation.",
    ),
    compile_rule(
        code="WORKFLOW_AUTOCOMMIT_PROJECTION",
        severity="WARN",
        pattern=(
            r"\b(git add|git commit|git push|gh pr create)\b.{0,200}\b("
            r"docs/observatory|runic_graph|projection|observatory_snapshot|OBSERVATORY_STATUS"
            r")\b"
        ),
        reason="Automated workflow committing generated projection outputs may create feedback-loop pressure.",
        safer_form="Use runtime-only CI outputs; persistent docs updates should be explicit human commits.",
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

    print(f"VECTAETOS No Feedback Loop Guard v{VERSION}")
    print("=========================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no feedback-loop drift detected.")
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
        description="Detect VECTAETOS feedback-loop drift."
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
