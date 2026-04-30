#!/usr/bin/env python3
"""
VECTAETOS_BOUNDARY_GUARD.py

Version:
    0.2.0

Purpose:
    Static repository perimeter guard for VECTAETOS semantic drift.

Scope:
    - Scans repository text/code/config files.
    - Detects forbidden formulations that attribute agency, optimization,
      decision authority, deployment legitimacy, or truth authority to VECTAETOS.
    - Avoids false positives in negated, forbidden-example, and guard-context lines.
    - Does not modify files.
    - Fails closed in CI on hard violations.

Python:
    3.11+

Run from:
    repository root

Command:
    python3 guards/VECTAETOS_BOUNDARY_GUARD.py

Exit codes:
    0 = clean / warnings only
    1 = hard violation found
    2 = execution/config error
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
from pathlib import Path
from typing import Iterable


VERSION = "0.2.0"

DEFAULT_INCLUDE_SUFFIXES = {
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

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".ruff_cache",
    "archive",
}

DEFAULT_EXCLUDED_FILES = {
    "VECTAETOS_BOUNDARY_GUARD.py",
}

DEFAULT_EXCLUDED_PATH_PARTS = {
    ("docs", "observatory"),
}

ALLOW_MARKERS = {
    "vectaetos-guard: allow",
    "vectaetos-boundary-allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-guard: allow-file",
    "vectaetos-boundary-allow-file",
}

META_CONTEXT_PATTERN = re.compile(
    r"\b("
    r"forbidden|prohibited|ban|banned|disallowed|failure condition|fails if|"
    r"must not|should not|do not|does not|is not|are not|cannot|can't|never|"
    r"no layer may|no mathematical appendix may|not automatically|without|"
    r"zakázané|zakazane|zákaz|zakaz|nesmie|nesmú|nesmu|nemá|nema|nie je|"
    r"nepíš|nepis|bez|neclaimuj|nepredstieraj|"
    r"nie rozhodovací|no decision|no optimization|no feedback|"
    r"refuses|refuse|odmieta|odmietnutie"
    r")\b",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|refuses|refuse|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|nemá|nema|bez|nie je|žiadny|ziadny|"
    r"žiadna|ziadna|odmieta|nie ako"
    r")\b",
    re.IGNORECASE | re.UNICODE,
)

QUOTE_OR_RULE_CONTEXT_PATTERN = re.compile(
    r"("
    r"^\s*[-*]\s+|"
    r"^\s*\d+\.\s+|"
    r"`[^`]+`|"
    r"\"[^\"]+\"|"
    r"'[^']+'|"
    r"pattern\s*=|"
    r"reason\s*=|"
    r"safer_form\s*=|"
    r"code\s*=|"
    r"rule|guard|violation|finding|"
    r"forbidden state|forbidden condition"
    r")",
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
        code="AGENCY_VECTAETOS_DECIDES",
        severity="HARD",
        pattern=r"\bVECTAETOS\b.{0,100}\b(decides|decide|decision authority|decision system|rozhoduje|rozhodne|rozhodovací systém|rozhodovaci system|autorita rozhodovania)\b",
        reason="VECTAETOS must not be framed as a decision-making entity.",
        safer_form="Use: VECTAETOS exposes structure / projects state / describes topology.",
    ),
    compile_rule(
        code="RECOMMENDATION_AUTHORITY",
        severity="HARD",
        pattern=r"\bVECTAETOS\b.{0,100}\b(recommends|recommendation engine|recommendation|odporúča|odporuca|odporúčanie|odporucanie)\b",
        reason="Projection must not be framed as recommendation.",
        safer_form="Use: projection / descriptive output / non-prescriptive exposure.",
    ),
    compile_rule(
        code="OPTIMIZATION_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|Φ|Phi|Vortex)\b.{0,100}\b(optimizes|optimization objective|optimization target|optimalizuje|optimalizačný cieľ|optimalizacny ciel)\b",
        reason="VECTAETOS/Φ/Vortex must not be framed as optimization systems.",
        safer_form="Use: non-optimizing structural evaluation / trajectory generation without ranking.",
    ),
    compile_rule(
        code="K_AS_SCORE",
        severity="HARD",
        pattern=r"\bK\s*\(?\s*Φ?\s*\)?\b.{0,100}\b(score|ranking|reward|target|cieľ|ciel|skóre|skore|odmena)\b",
        reason="K(Φ) is an ontological predicate, not a score/reward/target.",
        safer_form="Use: K(Φ) = ontological coherence predicate.",
    ),
    compile_rule(
        code="KAPPA_AS_PARAMETER",
        severity="HARD",
        pattern=r"\b(κ|kappa)\b.{0,100}\b(parameter|tunable|deployment threshold|runtime parameter|nastaviteľný|nastavitelny|prah deploymentu|runtime parameter)\b",
        reason="κ is not a tunable parameter or deployment threshold.",
        safer_form="Use: κ = boundary of ontological preservability.",
    ),
    compile_rule(
        code="KAPPA_AS_THRESHOLD",
        severity="HARD",
        pattern=r"\b(κ|kappa)\b\s*(=|—|-|:)\s*.*\b(threshold|prahová hodnota|prah)\b",
        reason="κ should not be defined as a threshold; canonical meaning is boundary.",
        safer_form="Use: κ = boundary of ontological preservability / representability.",
    ),
    compile_rule(
        code="QE_AS_ERROR",
        severity="HARD",
        pattern=r"\bQE\b.{0,100}\b(error|ordinary error|bug|exception|chyba|bežná chyba|bezna chyba)\b",
        reason="QE is an active epistemic aporia, not an ordinary error.",
        safer_form="Use: QE = qualitative epistemic aporia / boundary of representability.",
    ),
    compile_rule(
        code="AUDIT_COMMAND_LAYER",
        severity="HARD",
        pattern=r"\b(audit|EK|Epistemic Cryptography)\b.{0,100}\b(commands|controls|decides|velí|veli|rozhoduje|riadi)\b",
        reason="Audit must remain observe/record/hash only.",
        safer_form="Use: audit observes, records, hashes, and never commands.",
    ),
    compile_rule(
        code="AUDIT_BLOCKS",
        severity="WARN",
        pattern=r"\b(audit|EK|Epistemic Cryptography)\b.{0,100}\b(blocks|blokuje)\b",
        reason="Audit should not be framed as a blocking/control layer unless clearly describing external CI guard behavior.",
        safer_form="Use: audit observes, records, hashes; guards may fail CI externally.",
    ),
    compile_rule(
        code="PROJECTION_INTERPRETS",
        severity="HARD",
        pattern=r"\b(projection|projekcia|runa|runy|glyph|TetraGlyph)\b.{0,100}\b(interprets|decides|recommends|interpretuje|rozhoduje|odporúča|odporuca)\b",
        reason="Projection is descriptive and must not interpret or prescribe.",
        safer_form="Use: projection exposes structural state; interpretation remains human/downstream.",
    ),
    compile_rule(
        code="MEMORY_WRITES_ONTOLOGY",
        severity="HARD",
        pattern=r"\b(memory|pamäť|pamat|ESM|LTL|MML)\b.{0,120}\b(updates|changes|modifies|rewrites|mení|meni|prepisuje)\b.{0,60}\b(Φ|Phi|Vortex|K\(Φ\)|kappa|κ)\b",
        reason="Memory may provide controlled continuity, but must not change Φ, Vortex, K(Φ), or κ.",
        safer_form="Use: memory is anchored continuity, not ontological authority.",
    ),
    compile_rule(
        code="ASI_STANDALONE_ROOT",
        severity="HARD",
        pattern=r"\b(ASIMULATOR|ASI_MOD)\b.{0,120}\b(ontological root|standalone root|samostatný root|samostatny root|nezávislý root|nezavisly root)\b",
        reason="ASIMULATOR and ASI_MOD are downstream; neither may become root.",
        safer_form="Use: ASIMULATOR/ASI_MOD are downstream layers dependent on VECTAETOS.",
    ),
    compile_rule(
        code="ASI_STANDALONE_VALIDITY",
        severity="HARD",
        pattern=r"\b(ASIMULATOR|ASI_MOD)\b.{0,120}\b(standalone validity|standalone legitimacy|samostatná validita|samostatna validita|samostatná legitimita|samostatna legitimita)\b",
        reason="ASIMULATOR and ASI_MOD must not claim standalone validity.",
        safer_form="Use: validity is downstream of VECTAETOS root dependency.",
    ),
    compile_rule(
        code="SAFETY_GUARANTEE",
        severity="HARD",
        pattern=r"\b(VECTAETOS|ASIMULATOR|ASI_MOD)\b.{0,120}\b(guarantees safety|safe in reality|deployment valid|garantuje bezpečnosť|garantuje bezpecnost|validuje deployment|bezpečný deployment)\b",
        reason="No full safety/deployment legitimacy may be claimed without replicated L4 evidence.",
        safer_form="Use: structurally constrained / research-stage / requires L4 validation.",
    ),
    compile_rule(
        code="TRUTH_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|LLM|ASI_MOD|ASIMULATOR)\b.{0,100}\b(knows truth|truth authority|vie pravdu|autorita pravdy|nositeľ pravdy|nositel pravdy)\b",
        reason="No layer is a truth authority.",
        safer_form="Use: describes structure / renders language / exposes uncertainty.",
    ),
    compile_rule(
        code="BEST_TRAJECTORY",
        severity="HARD",
        pattern=r"\b(Vortex|Simulačný Vortex|Simulation Vortex)\b.{0,120}\b(best trajectory|selects trajectory|vyberá trajektóriu|vybera trajektoriu|najlepšia trajektória|najlepsia trajektoria)\b",
        reason="Vortex generates candidate trajectories; it must not select or rank a best trajectory.",
        safer_form="Use: generates candidate trajectories without ranking authority.",
    ),
    compile_rule(
        code="AI_SYSTEM_CLAIM",
        severity="WARN",
        pattern=r"\bVECTAETOS\b.{0,100}\b(AI system|AI systém|operational AI system)\b",
        reason="VECTAETOS should not be casually framed as an operational AI system.",
        safer_form="Use: non-agentic epistemic field framework / ontological architecture.",
    ),
]


def has_allow_marker(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in ALLOW_MARKERS)


def file_has_allow_marker(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20]).lower()
    return any(marker in head for marker in FILE_ALLOW_MARKERS)


def is_path_excluded(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts

    if any(part in DEFAULT_EXCLUDED_DIRS for part in rel_parts):
        return True

    if path.name in DEFAULT_EXCLUDED_FILES:
        return True

    for excluded_parts in DEFAULT_EXCLUDED_PATH_PARTS:
        if len(rel_parts) >= len(excluded_parts):
            for idx in range(0, len(rel_parts) - len(excluded_parts) + 1):
                if tuple(rel_parts[idx : idx + len(excluded_parts)]) == excluded_parts:
                    return True

    return False


def is_meta_or_negated_context(context: str, line: str) -> bool:
    if META_CONTEXT_PATTERN.search(context):
        return True

    if NEGATION_PATTERN.search(line):
        return True

    if QUOTE_OR_RULE_CONTEXT_PATTERN.search(line) and META_CONTEXT_PATTERN.search(context):
        return True

    return False


def iter_candidate_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue

        if is_path_excluded(path, root):
            continue

        if path.suffix.lower() not in DEFAULT_INCLUDE_SUFFIXES:
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


def scan_file(path: Path) -> list[Finding]:
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

        window_start = max(0, idx - 5)
        context = "\n".join(lines[window_start:idx])

        for rule in RULES:
            match = rule.pattern.search(stripped)
            if not match:
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

    print(f"VECTAETOS Boundary Guard v{VERSION}")
    print("==============================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no boundary drift detected.")
        return

    for finding in findings:
        try:
            rel = finding.path.relative_to(root)
        except ValueError:
            rel = finding.path

        print(f"[{finding.rule.severity}] {finding.rule.code}")
        print(f"  file: {rel}:{finding.line_no}")
        print(f"  line: {finding.line}")
        print(f"  why:  {finding.rule.reason}")
        print(f"  use:  {finding.rule.safer_form}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static VECTAETOS semantic boundary guard."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current working directory.",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Treat warnings as hard failures.",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []

    try:
        for file_path in iter_candidate_files(root):
            all_findings.extend(scan_file(file_path))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_findings.sort(
        key=lambda finding: (str(finding.path), finding.line_no, finding.rule.code)
    )
    print_findings(all_findings, root)

    hard_count = sum(1 for finding in all_findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in all_findings if finding.rule.severity == "WARN")

    if hard_count > 0:
        return 1

    if args.warnings_as_errors and warn_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
