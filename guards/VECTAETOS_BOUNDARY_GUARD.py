#!/usr/bin/env python3
"""
VECTAETOS_BOUNDARY_GUARD.py

Purpose:
    Static repository perimeter guard for VECTAETOS semantic drift.

Scope:
    - Scans repository text/code/config files.
    - Detects forbidden formulations that attribute agency, optimization,
      decision authority, deployment legitimacy, or truth authority to VECTAETOS.
    - Does not modify files.
    - Fails closed in CI on hard violations.

Python:
    3.11+

Run from:
    repository root

Command:
    python infrastructure/guards/VECTAETOS_BOUNDARY_GUARD.py

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


REPO_ROOT = Path.cwd()

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
}

DEFAULT_EXCLUDED_FILES = {
    "VECTAETOS_BOUNDARY_GUARD.py",
}


@dataclasses.dataclass(frozen=True)
class Rule:
    code: str
    severity: str  # "HARD" or "WARN"
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
        pattern=r"\bVECTAETOS\b.{0,80}\b(decides|decide|decision|rozhoduje|rozhodne|rozhodnutie)\b",
        reason="VECTAETOS must not be framed as a decision-making entity.",
        safer_form="Use: VECTAETOS exposes structure / projects state / describes topology.",
    ),
    compile_rule(
        code="RECOMMENDATION_AUTHORITY",
        severity="HARD",
        pattern=r"\bVECTAETOS\b.{0,80}\b(recommends|recommendation|odporúča|odporuca|odporúčanie|odporucanie)\b",
        reason="Projection must not be framed as recommendation.",
        safer_form="Use: projection / descriptive output / non-prescriptive exposure.",
    ),
    compile_rule(
        code="OPTIMIZATION_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|Φ|Phi|Vortex)\b.{0,80}\b(optimizes|optimize|optimization|optimalizuje|optimalizácia|optimalizacia)\b",
        reason="VECTAETOS/Φ/Vortex must not be framed as optimization systems.",
        safer_form="Use: non-optimizing structural evaluation / trajectory generation without ranking.",
    ),
    compile_rule(
        code="K_AS_SCORE",
        severity="HARD",
        pattern=r"\bK\s*\(?\s*Φ?\s*\)?\b.{0,80}\b(score|ranking|reward|cieľ|ciel|skóre|skore|odmena)\b",
        reason="K(Φ) is an ontological predicate, not a score/reward/target.",
        safer_form="Use: K(Φ) = ontological coherence predicate.",
    ),
    compile_rule(
        code="KAPPA_AS_PARAMETER",
        severity="HARD",
        pattern=r"\b(κ|kappa)\b.{0,80}\b(parameter|threshold|tunable|nastaviteľný|nastavitelny|prahová hodnota|prah deploymentu)\b",
        reason="κ is not a tunable parameter or deployment threshold.",
        safer_form="Use: κ = boundary of ontological preservability.",
    ),
    compile_rule(
        code="QE_AS_ERROR",
        severity="HARD",
        pattern=r"\bQE\b.{0,80}\b(error|failure|bug|chyba|zlyhanie|exception)\b",
        reason="QE is an active epistemic aporia, not an ordinary error.",
        safer_form="Use: QE = qualitative epistemic aporia / boundary of representability.",
    ),
    compile_rule(
        code="AUDIT_COMMAND_LAYER",
        severity="HARD",
        pattern=r"\b(audit|EK|Epistemic Cryptography)\b.{0,80}\b(commands|controls|blocks|decides|velí|veli|kontroluje|blokuje|rozhoduje)\b",
        reason="Audit must remain observe/record/hash only.",
        safer_form="Use: audit observes, records, hashes, and never commands.",
    ),
    compile_rule(
        code="PROJECTION_INTERPRETS",
        severity="HARD",
        pattern=r"\b(projection|projekcia|runa|runy|glyph|TetraGlyph)\b.{0,80}\b(interprets|decides|recommends|interpretuje|rozhoduje|odporúča|odporuca)\b",
        reason="Projection is descriptive and must not interpret or prescribe.",
        safer_form="Use: projection exposes structural state; interpretation remains human/downstream.",
    ),
    compile_rule(
        code="MEMORY_WRITES_ONTOLOGY",
        severity="HARD",
        pattern=r"\b(memory|pamäť|pamat|ESM|LTL|MML)\b.{0,100}\b(updates|changes|modifies|rewrites|mení|meni|prepisuje)\b.{0,40}\b(Φ|Phi|Vortex|K\(Φ\)|kappa|κ)\b",
        reason="Memory may provide controlled continuity, but must not change Φ, Vortex, K(Φ), or κ.",
        safer_form="Use: memory is anchored continuity, not ontological authority.",
    ),
    compile_rule(
        code="ASI_STANDALONE_ROOT",
        severity="HARD",
        pattern=r"\b(ASIMULATOR|ASI_MOD)\b.{0,100}\b(root|ontological root|standalone|samostatný root|samostatny root|nezávislý root|nezavisly root)\b",
        reason="ASIMULATOR and ASI_MOD are downstream; neither may become root.",
        safer_form="Use: ASIMULATOR/ASI_MOD are downstream layers dependent on VECTAETOS.",
    ),
    compile_rule(
        code="SAFETY_GUARANTEE",
        severity="HARD",
        pattern=r"\b(VECTAETOS|ASIMULATOR|ASI_MOD)\b.{0,100}\b(guarantees safety|safe in reality|deployment valid|garantuje bezpečnosť|garantuje bezpecnost|validuje deployment|bezpečný deployment)\b",
        reason="No full safety/deployment legitimacy may be claimed without replicated L4 evidence.",
        safer_form="Use: structurally constrained / research-stage / requires L4 validation.",
    ),
    compile_rule(
        code="TRUTH_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|LLM|ASI_MOD|ASIMULATOR)\b.{0,80}\b(knows truth|truth authority|vie pravdu|autorita pravdy|nositeľ pravdy|nositel pravdy)\b",
        reason="No layer is a truth authority.",
        safer_form="Use: describes structure / renders language / exposes uncertainty.",
    ),
    compile_rule(
        code="AI_SYSTEM_CLAIM",
        severity="WARN",
        pattern=r"\bVECTAETOS\b.{0,80}\b(AI system|umelá inteligencia|AI systém|AI system)\b",
        reason="VECTAETOS should not be casually framed as an operational AI system.",
        safer_form="Use: non-agentic epistemic field framework / ontological architecture.",
    ),
    compile_rule(
        code="BEST_TRAJECTORY",
        severity="HARD",
        pattern=r"\b(Vortex|Simulačný Vortex|Simulation Vortex)\b.{0,100}\b(best trajectory|selects trajectory|vyberá trajektóriu|vybera trajektoriu|najlepšia trajektória|najlepsia trajektoria)\b",
        reason="Vortex generates candidate trajectories; it must not select or rank a best trajectory.",
        safer_form="Use: generates candidate trajectories without ranking authority.",
    ),
]


def iter_candidate_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue

        if any(part in DEFAULT_EXCLUDED_DIRS for part in path.parts):
            continue

        if path.name in DEFAULT_EXCLUDED_FILES:
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

    findings: list[Finding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        for rule in RULES:
            if rule.pattern.search(stripped):
                findings.append(
                    Finding(
                        path=path,
                        line_no=idx,
                        line=stripped,
                        rule=rule,
                    )
                )

    return findings


def print_findings(findings: list[Finding]) -> None:
    hard_count = sum(1 for f in findings if f.rule.severity == "HARD")
    warn_count = sum(1 for f in findings if f.rule.severity == "WARN")

    print("VECTAETOS Boundary Guard")
    print("========================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no boundary drift detected.")
        return

    for finding in findings:
        rel = finding.path.relative_to(REPO_ROOT)
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
        default=REPO_ROOT,
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

    global REPO_ROOT
    REPO_ROOT = root

    all_findings: list[Finding] = []

    try:
        for file_path in iter_candidate_files(root):
            all_findings.extend(scan_file(file_path))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_findings.sort(key=lambda f: (str(f.path), f.line_no, f.rule.code))
    print_findings(all_findings)

    hard_count = sum(1 for f in all_findings if f.rule.severity == "HARD")
    warn_count = sum(1 for f in all_findings if f.rule.severity == "WARN")

    if hard_count > 0:
        return 1

    if args.warnings_as_errors and warn_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
