#!/usr/bin/env python3
"""
VECTAETOS :: Vortex Non-Agentic Guard

Version:
    0.1.0

Guard Class:
    Level 0 — Fundamental Repository Perimeter

Role:
    Protects the non-agentic boundary of the Simulation Vortex.

Purpose:
    Detects repository drift where the Vortex is framed as an agent,
    optimizer, selector, recommender, decision system, coherence authority,
    κ-aware filter, QE generator, or feedback layer.

Canonical boundary:
    - Vortex generates candidate trajectories.
    - Vortex does not select, rank, optimize, recommend, or decide.
    - Vortex does not know K(Φ) or κ.
    - Vortex does not generate QE.
    - Vortex does not generate impulse.
    - Vortex does not write back into Φ.
    - Coherence filtering happens outside Vortex.

Non-role:
    - does not define ontology
    - does not validate deployment
    - does not prove safety
    - does not modify files
    - does not change Φ, K(Φ), κ, QE, audit, projection, or LLM role

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
    "guards/vortex_non_agentic_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-vortex-guard-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-vortex-guard-allow-file",
    "vectaetos-guard: allow-file",
}

VORTEX_PATH_MARKERS = {
    "vortex",
    "simulation_vortex",
    "vortex_core",
}

FORBIDDEN_AST_NAME_FRAGMENTS = {
    "select_best",
    "best_trajectory",
    "rank_trajectory",
    "rank_trajectories",
    "optimize",
    "optimizer",
    "optimization",
    "recommend",
    "recommender",
    "decision",
    "decide",
    "reward",
    "policy_update",
    "choose_path",
    "choose_trajectory",
    "select_trajectory",
    "score_trajectory",
    "trajectory_score",
}

FORBIDDEN_ASSIGNMENT_NAMES = {
    "best",
    "best_trajectory",
    "selected",
    "selected_trajectory",
    "ranked",
    "ranked_trajectories",
    "trajectory_score",
    "reward",
    "policy",
    "decision",
    "recommendation",
}

RANDOM_MODULES = {
    "random",
    "secrets",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|no claim|not claim|does not claim|"
    r"guard|detects|scan|drift|example failure|compatibility test|"
    r"canonical boundary|non-role|"
    r"nesmie|nesmú|nesmu|nie je|nie sú|nie su|bez|zakázané|zakazane|"
    r"zákaz|zakaz|neclaimuj|nepíš|nepis|"
    r"nie je rozhod|nie je agent|nie je optimal|nie je výber|nie je vyber|"
    r"report-only|diagnosis|forbidden pattern|forbidden claim"
    r")",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|bez|nie je|nie sú|nie su|"
    r"žiadny|ziadny|žiadna|ziadna"
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


VORTEX_SUBJECT = r"\b(Vortex|Simulation Vortex|Simulačný Vortex|Simulacny Vortex)\b"

RULES: list[Rule] = [
    compile_rule(
        code="VORTEX_AGENTIC_ENTITY",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,140}\b("
            r"agent|autonomous agent|planner|controller|executor|"
            r"agentný|agentny|autonómny agent|autonomny agent|plánovač|planovac|kontrolér|kontroler|vykonávateľ|vykonavatel"
            r")\b"
        ),
        reason="Vortex must not be framed as an agent, planner, controller, or executor.",
        safer_form="Use: Vortex is a non-agentic generator of candidate trajectories.",
    ),
    compile_rule(
        code="VORTEX_DECIDES",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,140}\b("
            r"decides|decision|chooses|determines what should happen|"
            r"rozhoduje|rozhodne|rozhodnutie|vyberá čo sa má stať|vybera co sa ma stat"
            r")\b"
        ),
        reason="Vortex must not be framed as decision authority.",
        safer_form="Use: Vortex emits candidate trajectories without decision authority.",
    ),
    compile_rule(
        code="VORTEX_RECOMMENDS",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,140}\b("
            r"recommends|recommendation|suggests the best|advises|"
            r"odporúča|odporuca|odporúčanie|odporucanie|radí|radi"
            r")\b"
        ),
        reason="Vortex must not be framed as recommendation authority.",
        safer_form="Use: Vortex exposes possible trajectories; interpretation remains outside Vortex.",
    ),
    compile_rule(
        code="VORTEX_OPTIMIZES",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,140}\b("
            r"optimizes|optimization|optimal trajectory|optimal path|"
            r"optimalizuje|optimalizácia|optimalizacia|optimálna trajektória|optimalna trajektoria|optimálna cesta|optimalna cesta"
            r")\b"
        ),
        reason="Vortex must not be framed as optimizer.",
        safer_form="Use: Vortex generates candidate trajectories without optimization objective.",
    ),
    compile_rule(
        code="VORTEX_SELECTS_BEST",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,160}\b("
            r"selects best|selects the best|best trajectory|best path|chooses best|"
            r"vyberá najlepš|vybera najleps|najlepšia trajektória|najlepsia trajektoria|najlepšia cesta|najlepsia cesta"
            r")\b"
        ),
        reason="Vortex must not select a best trajectory or path.",
        safer_form="Use: Vortex generates a set of candidate trajectories without ranking.",
    ),
    compile_rule(
        code="VORTEX_RANKS_TRAJECTORIES",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,160}\b("
            r"ranks trajectories|trajectory ranking|ranks candidates|scores trajectories|"
            r"rankuje trajektórie|rankuje trajektorie|ranking trajektórií|ranking trajektorii|skóruje trajektórie|skoruje trajektorie"
            r")\b"
        ),
        reason="Vortex must not rank or score trajectories.",
        safer_form="Use: Vortex output is an unordered candidate set or descriptive trace.",
    ),
    compile_rule(
        code="VORTEX_KAPPA_ACCESS",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,180}\b("
            r"knows|uses|applies|checks|filters by|compares against|thresholds against|"
            r"pozná|pozna|používa|pouziva|aplikuje|kontroluje|filtruje|porovnáva|porovnava"
            r")\b.{0,100}\b("
            r"κ|kappa|K\(Φ\)|K\(Phi\)|coherence predicate|koherenčný predikát|koherencny predikat"
            r")\b"
        ),
        reason="Vortex must not know or apply K(Φ) / κ; coherence filtering is outside Vortex.",
        safer_form="Use: coherence predicate is applied externally after candidate generation.",
    ),
    compile_rule(
        code="VORTEX_COHERENCE_FILTER",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,180}\b("
            r"filters coherent|filters incoherent|coherence filter|coherence filtering|"
            r"filtruje koherentné|filtruje koherentne|filtruje nekoherentné|filtruje nekoherentne|koherenčný filter|koherencny filter"
            r")\b"
        ),
        reason="Vortex must not be framed as the coherence filtering layer.",
        safer_form="Use: Vortex generates candidates; K(Φ) filters realizability outside Vortex.",
    ),
    compile_rule(
        code="QE_FROM_VORTEX",
        severity="HARD",
        pattern=(
            r"("
            + VORTEX_SUBJECT
            + r".{0,160}\b("
            r"generates|creates|produces|detects|signals|triggers|"
            r"generuje|vytvára|vytvara|produkuje|deteguje|signalizuje|spúšťa|spusta"
            r")\b.{0,80}\b(QE|aporia|apória|aporia)"
            r"|"
            r"\b(QE|aporia|apória|aporia)\b.{0,120}\b("
            r"inside|within|from|in the Vortex|vo Vortexe|z Vortexu"
            r")\b"
            r")"
        ),
        reason="QE must not be framed as originating inside the Vortex.",
        safer_form="Use: QE is an epistemic aporia identified outside Vortex when no trajectory preserves coherence.",
    ),
    compile_rule(
        code="IMPULSE_FROM_VORTEX",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,160}\b("
            r"generates impulse|creates impulse|produces impulse|emits impulse|"
            r"generuje impulz|vytvára impulz|vytvara impulz|produkuje impulz"
            r")\b"
        ),
        reason="Impulse must not be framed as generated by the Vortex.",
        safer_form="Use: impulse is identified as non-realizability outside the Vortex.",
    ),
    compile_rule(
        code="VORTEX_FEEDBACK_TO_PHI",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,180}\b("
            r"writes back|feeds back|updates|modifies|changes|rewrites|"
            r"píše späť|pise spat|vracia späť|vracia spat|updatuje|aktualizuje|mení|meni|prepisuje"
            r")\b.{0,100}\b(Φ|Phi|field|pole|ontology|ontológia|ontologia|K\(Φ\)|κ|kappa|QE)\b"
        ),
        reason="Vortex must not write back into Φ or modify ontology.",
        safer_form="Use: Vortex is external and non-intervening; no feedback into Φ.",
    ),
    compile_rule(
        code="VORTEX_MEMORY_AUTHORITY",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,160}\b("
            r"learns|adapts|remembers|updates from memory|trains|self-improves|"
            r"učí sa|uci sa|adaptuje|pamätá|pameta|trénuje|trenuje|seba-zlepšuje|seba-zlepsuje"
            r")\b"
        ),
        reason="Vortex must not be framed as learning, adaptive, or memory-authoritative.",
        safer_form="Use: Vortex remains non-agentic and memoryless with respect to authority.",
    ),
    compile_rule(
        code="VORTEX_REWARD_POLICY",
        severity="HARD",
        pattern=(
            VORTEX_SUBJECT
            + r".{0,180}\b("
            r"reward|reward function|policy|policy update|reinforcement|RLHF|"
            r"odmena|reward funkcia|politika|policy update|reinforcement"
            r")\b"
        ),
        reason="Vortex must not contain reward/policy semantics.",
        safer_form="Use: Vortex has no reward, policy, or optimization objective.",
    ),
]


def compile_internal_rule(code: str, reason: str, safer_form: str) -> Rule:
    return Rule(
        code=code,
        severity="HARD",
        pattern=re.compile(r"$^"),
        reason=reason,
        safer_form=safer_form,
    )


AST_FORBIDDEN_NAME_RULE = compile_internal_rule(
    code="VORTEX_FORBIDDEN_AST_NAME",
    reason="Vortex Python code must not encode selection, ranking, optimization, reward, recommendation, or decision semantics.",
    safer_form="Use descriptive names: generate_candidates, emit_trace, project_candidate_set.",
)

AST_FORBIDDEN_ASSIGNMENT_RULE = compile_internal_rule(
    code="VORTEX_FORBIDDEN_ASSIGNMENT_NAME",
    reason="Vortex Python code must not store best/selected/ranked/reward/decision semantics.",
    safer_form="Use candidate_set, trajectory_set, trace, or descriptive_output.",
)

AST_RANDOMNESS_RULE = Rule(
    code="VORTEX_RANDOMNESS_REVIEW",
    severity="WARN",
    pattern=re.compile(r"$^"),
    reason="Randomness in Vortex code may break determinism unless explicitly seeded and documented.",
    safer_form="Use deterministic generation or documented deterministic seed behavior.",
)


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


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr

    if isinstance(node, ast.Call):
        return dotted_name(node.func)

    return ""


def assigned_names(node: ast.AST) -> list[str]:
    names: list[str] = []

    def visit_target(target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Attribute):
            names.append(dotted_name(target))
        elif isinstance(target, (ast.Tuple, ast.List)):
            for item in target.elts:
                visit_target(item)

    if isinstance(node, ast.Assign):
        for target in node.targets:
            visit_target(target)
    elif isinstance(node, ast.AnnAssign):
        visit_target(node.target)
    elif isinstance(node, ast.AugAssign):
        visit_target(node.target)

    return names


def line_text(lines: list[str], line_no: int) -> str:
    if 0 < line_no <= len(lines):
        return lines[line_no - 1].strip()
    return ""


def is_vortex_file(path: Path, root: Path, text: str) -> bool:
    rel = normalize_repo_path(path, root).lower()

    if any(marker in rel for marker in VORTEX_PATH_MARKERS):
        return True

    head = "\n".join(text.splitlines()[:40]).lower()

    if '__vectaetos_role__ = "vortex"' in head or "__vectaetos_role__ = 'vortex'" in head:
        return True

    return False


def imports_from_node(node: ast.AST) -> list[str]:
    imports: list[str] = []

    if isinstance(node, ast.Import):
        for alias in node.names:
            imports.append(alias.name)

    if isinstance(node, ast.ImportFrom):
        if node.module:
            imports.append(node.module)

    return imports


def root_module(name: str) -> str:
    return name.split(".", 1)[0].lower()


def scan_python_ast(path: Path, root: Path, text: str) -> list[Finding]:
    if path.suffix.lower() != ".py":
        return []

    if not is_vortex_file(path, root, text):
        return []

    lines = text.splitlines()
    findings: list[Finding] = []

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        line_no = getattr(node, "lineno", 1)

        for imported in imports_from_node(node):
            if root_module(imported) in RANDOM_MODULES:
                findings.append(
                    Finding(
                        path=path,
                        line_no=line_no,
                        line=line_text(lines, line_no),
                        rule=AST_RANDOMNESS_RULE,
                    )
                )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            lowered = node.name.lower()

            for fragment in FORBIDDEN_AST_NAME_FRAGMENTS:
                if fragment in lowered:
                    findings.append(
                        Finding(
                            path=path,
                            line_no=line_no,
                            line=line_text(lines, line_no),
                            rule=AST_FORBIDDEN_NAME_RULE,
                        )
                    )

        if isinstance(node, ast.Call):
            call_name = dotted_name(node.func).lower()

            for fragment in FORBIDDEN_AST_NAME_FRAGMENTS:
                if fragment in call_name:
                    findings.append(
                        Finding(
                            path=path,
                            line_no=line_no,
                            line=line_text(lines, line_no),
                            rule=AST_FORBIDDEN_NAME_RULE,
                        )
                    )

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            for name in assigned_names(node):
                clean = name.split(".")[-1].lower()

                if clean in FORBIDDEN_ASSIGNMENT_NAMES:
                    findings.append(
                        Finding(
                            path=path,
                            line_no=line_no,
                            line=line_text(lines, line_no),
                            rule=AST_FORBIDDEN_ASSIGNMENT_RULE,
                        )
                    )

    return findings

def scan_file(path: Path, root: Path) -> list[Finding]:
    text = read_text(path)

    if text is None:
        return []

    if file_has_allow_marker(text):
        return []

    findings: list[Finding] = []

    findings.extend(scan_python_ast(path, root, text))

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

    print(f"VECTAETOS Vortex Non-Agentic Guard v{VERSION}")
    print("==========================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no Vortex non-agentic boundary drift detected.")
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
        description="Detect Simulation Vortex non-agentic boundary drift."
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
