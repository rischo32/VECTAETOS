#!/usr/bin/env python3
"""
VECTAETOS :: Repo Layer Boundary Guard

Version:
    0.1.0

Guard Class:
    Level 0 — Fundamental Repository Perimeter

Role:
    Protects the repository-layer boundary of VECTAETOS.

Purpose:
    Detects repository drift where VECTAETOS is made dependent on,
    merged with, or semantically collapsed into downstream layers:
    ASIMULATOR / ASI_MOD.

Detects:
    - reverse imports from ASIMULATOR / ASI_MOD
    - downstream directories appearing as root implementation layers
    - claims that ASIMULATOR / ASI_MOD are ontological roots
    - claims that VECTAETOS depends on ASIMULATOR / ASI_MOD
    - claims that downstream layers redefine Φ, K(Φ), κ, QE, audit, projection, or LLM role

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
import ast
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
    "guards/repo_layer_boundary_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-repo-layer-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-repo-layer-allow-file",
    "vectaetos-guard: allow-file",
}

FORBIDDEN_DOWNSTREAM_MODULES = {
    "asimulator",
    "asi_mod",
}

FORBIDDEN_ROOT_DIR_NAMES = {
    "asimulator",
    "asi_mod",
    "asi-mod",
    "ASI_MOD",
    "ASIMULATOR",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|not a root|not root|not standalone|not valid without|"
    r"downstream|dependency rule|boundary rule|guard|detects|scan|drift|"
    r"nesmie|nesmú|nesmu|nie je|bez|zakázané|zakazane|zákaz|zakaz|"
    r"nie je root|nie je koreň|nie je koren|nie je samostatn|"
    r"neplatné bez|neplatne bez|downstream|hranica|strážca|strazca|"
    r"forbidden pattern|example failure|compatibility test|"
    r"hard violation|hard violations|examples of hard violations|example of hard violation"
    r")",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|bez|nie je|žiadny|ziadny|žiadna|ziadna"
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


RULES: list[Rule] = [
    compile_rule(
        code="VECTAETOS_DEPENDS_ON_DOWNSTREAM",
        severity="HARD",
        pattern=(
            r"\bVECTAETOS\b.{0,140}\b("
            r"depends on|requires|is valid only with|needs ASIMULATOR|needs ASI_MOD|"
            r"závisí od|zavisi od|vyžaduje|vyzaduje|je platný iba s|je platny iba s"
            r")\b.{0,80}\b(ASIMULATOR|ASI_MOD)\b"
        ),
        reason="VECTAETOS may exist without ASIMULATOR / ASI_MOD.",
        safer_form="Use: ASIMULATOR and ASI_MOD are downstream of VECTAETOS; VECTAETOS remains root.",
    ),
    compile_rule(
        code="DOWNSTREAM_AS_ONTOLOGICAL_ROOT",
        severity="HARD",
        pattern=(
            r"\b(ASIMULATOR|ASI_MOD)\b.{0,140}\b("
            r"ontological root|ontology root|primary ontology|foundational ontology|"
            r"samostatný root|samostatny root|ontologický root|ontologicky root|"
            r"primárna ontológia|primarna ontologia|zakladná ontológia|zakladna ontologia"
            r")\b"
        ),
        reason="Downstream layers must not be framed as ontological roots.",
        safer_form="Use: ASIMULATOR / ASI_MOD are downstream layers dependent on VECTAETOS.",
    ),
    compile_rule(
        code="DOWNSTREAM_STANDALONE_VALIDITY",
        severity="HARD",
        pattern=(
            r"\b(ASIMULATOR|ASI_MOD)\b.{0,140}\b("
            r"standalone validity|standalone legitimacy|valid without VECTAETOS|"
            r"self-sufficient|self sufficient|independent root|"
            r"samostatná validita|samostatna validita|samostatná legitimita|"
            r"samostatna legitimita|platný bez VECTAETOS|platny bez VECTAETOS|"
            r"sebestačný|sebestacny|nezávislý root|nezavisly root"
            r")\b"
        ),
        reason="ASIMULATOR and ASI_MOD must not claim standalone validity.",
        safer_form="Use: downstream validity remains dependent on VECTAETOS root conditions.",
    ),
    compile_rule(
        code="DOWNSTREAM_REDEFINES_ROOT",
        severity="HARD",
        pattern=(
            r"\b(ASIMULATOR|ASI_MOD)\b.{0,160}\b("
            r"defines|redefines|overrides|changes|modifies|rewrites|validates|"
            r"definuje|redefinuje|prepisuje|mení|meni|modifikuje|validuje"
            r")\b.{0,100}\b("
            r"Φ|Phi|K\(Φ\)|K\(Phi\)|κ|kappa|QE|Vortex|audit|projection|projekcia|LLM|ontology|ontológ"
            r")\b"
        ),
        reason="Downstream layers must not redefine canonical VECTAETOS terms or root ontology.",
        safer_form="Use: downstream layers may reference VECTAETOS but must not redefine its canonical terms.",
    ),
    compile_rule(
        code="REPOSITORY_FUSION_COLLAPSE",
        severity="WARN",
        pattern=(
            r"\b(VECTAETOS|ASIMULATOR|ASI_MOD)\b.{0,160}\b("
            r"merge into one repository|single repository root|same ontological layer|"
            r"collapse into one layer|unified executable root|"
            r"zlúčiť do jedného repozitára|zlucit do jedneho repozitara|"
            r"jeden spoločný root|jeden spolocny root|rovnaká ontologická vrstva|"
            r"rovnaka ontologicka vrstva|kolaps do jednej vrstvy"
            r")\b"
        ),
        reason="Triadic unity must not collapse repository-layer separation.",
        safer_form="Use: one architecture, three non-equivalent repositories/layers.",
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


def root_module(name: str) -> str:
    return name.split(".", 1)[0].lower()


def line_text(lines: list[str], line_no: int) -> str:
    if 0 < line_no <= len(lines):
        return lines[line_no - 1].strip()
    return ""


def scan_python_imports(path: Path, text: str) -> list[Finding]:
    lines = text.splitlines()

    import_rule = Rule(
        code="REVERSE_DOWNSTREAM_IMPORT",
        severity="HARD",
        pattern=re.compile(r"$^"),
        reason="VECTAETOS root repository must not import downstream ASIMULATOR / ASI_MOD modules.",
        safer_form="Use explicit non-authoritative interface contracts; do not import downstream layers into root.",
    )

    findings: list[Finding] = []

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if root_module(alias.name) in FORBIDDEN_DOWNSTREAM_MODULES:
                    original = line_text(lines, node.lineno)
                    if not has_allow_marker(original):
                        findings.append(Finding(path, node.lineno, original, import_rule))

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            if root_module(node.module) in FORBIDDEN_DOWNSTREAM_MODULES:
                original = line_text(lines, node.lineno)
                if not has_allow_marker(original):
                    findings.append(Finding(path, node.lineno, original, import_rule))

    return findings


def scan_structural_paths(root: Path) -> list[Finding]:
    path_rule = Rule(
        code="DOWNSTREAM_ROOT_DIRECTORY_PRESENT",
        severity="WARN",
        pattern=re.compile(r"$^"),
        reason="A downstream layer directory at repository root may blur VECTAETOS root boundaries.",
        safer_form="Use separate downstream repositories or clearly non-executable reference folders.",
    )

    findings: list[Finding] = []

    for name in FORBIDDEN_ROOT_DIR_NAMES:
        candidate = root / name
        if candidate.exists() and candidate.is_dir():
            findings.append(
                Finding(
                    path=candidate,
                    line_no=0,
                    line=f"root directory present: {name}",
                    rule=path_rule,
                )
            )

    return findings


def is_meta_or_negated_context(context: str, line: str) -> bool:
    if "≠" in line:
        return True

    if META_CONTEXT_PATTERN.search(context):
        return True

    if NEGATION_PATTERN.search(line):
        return True

    return False


def scan_text_rules(path: Path, root: Path) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []

    if file_has_allow_marker(text):
        return []

    findings: list[Finding] = []

    if path.suffix.lower() == ".py":
        findings.extend(scan_python_imports(path, text))

    lines = text.splitlines()

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

            findings.append(Finding(path, idx, stripped, rule))

    return findings


def print_findings(findings: list[Finding], root: Path) -> None:
    hard_count = sum(1 for finding in findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in findings if finding.rule.severity == "WARN")

    print(f"VECTAETOS Repo Layer Boundary Guard v{VERSION}")
    print("===========================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no repository layer boundary drift detected.")
        return

    for finding in findings:
        rel = normalize_repo_path(finding.path, root)

        location = rel if finding.line_no == 0 else f"{rel}:{finding.line_no}"

        print(f"[{finding.rule.severity}] {finding.rule.code}")
        print(f"  file: {location}")
        print(f"  line: {finding.line}")
        print(f"  why:  {finding.rule.reason}")
        print(f"  use:  {finding.rule.safer_form}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect VECTAETOS repository layer boundary drift."
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
        findings.extend(scan_structural_paths(root))

        for file_path in iter_candidate_files(root):
            findings.extend(scan_text_rules(file_path, root))

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
