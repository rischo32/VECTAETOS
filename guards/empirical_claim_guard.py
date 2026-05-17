#!/usr/bin/env python3
"""
VECTAETOS :: Empirical Claim Guard

Version:
    0.1.0

Role:
    Specialized semantic guard for empirical safety / deployment overclaims.

Purpose:
    Detects premature claims that VECTAETOS, ASIMULATOR, ASI_MOD,
    the architecture, framework, system, Vortex, audit, EK, projection,
    or guards are already empirically proven, deployment-valid, safe in reality,
    or safety-guaranteeing without replicated L4 evidence.

Scope:
    - repository text/code/config files
    - documentation
    - workflows
    - public-facing claims

Non-role:
    - does not validate safety
    - does not define ontology
    - does not decide deployment
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
    "guards/empirical_claim_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-empirical-claim-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-empirical-claim-allow-file",
    "vectaetos-guard: allow-file",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|no claim|not claim|does not claim|not proven|not validated|"
    r"requires l4|replicated l4|until l4|without replicated l4|"
    r"neclaimuj|nesmie|nesmú|nesmu|nie je|bez|zakázané|zakazane|zákaz|zakaz|"
    r"nie je dokázané|nie je dokazané|nie je dokazane|nie je validované|"
    r"vyžaduje l4|vyzaduje l4|bez l4|kým nebude|kym nebude|"
    r"report-only|diagnosis|guard|detects|scan|drift|overclaim|"
    r"forbidden pattern|forbidden claim|example failure|compatibility test"
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


SUBJECTS = (
    r"VECTAETOS|ASIMULATOR|ASI_MOD|architecture|framework|system|triad|"
    r"Vortex|Simulation Vortex|audit|EK|Epistemic Cryptography|projection|guard|guards|"
    r"architektúra|architektura|systém|system|triáda|triada|strážca|strazca|strážcovia|strazcovia"
)

RULES: list[Rule] = [
    compile_rule(
        code="SAFETY_GUARANTEE_CLAIM",
        severity="HARD",
        pattern=(
            rf"\b({SUBJECTS})\b.{{0,160}}\b("
            r"guarantees safety|guaranteed safety|safety guarantee|safe in reality|"
            r"fully safe|proves safety|ensures safety|cannot be unsafe|"
            r"garantuje bezpečnosť|garantuje bezpecnost|garantovaná bezpečnosť|"
            r"garantovana bezpecnost|bezpečné v realite|bezpecne v realite|"
            r"plne bezpečné|plne bezpecne|dokazuje bezpečnosť|dokazuje bezpecnost"
            r")\b"
        ),
        reason="No safety guarantee may be claimed without replicated L4 evidence.",
        safer_form="Use: structurally constrained / research-stage / requires replicated L4 validation.",
    ),
    compile_rule(
        code="DEPLOYMENT_VALIDITY_CLAIM",
        severity="HARD",
        pattern=(
            rf"\b({SUBJECTS})\b.{{0,160}}\b("
            r"deployment valid|valid deployment|deployment-ready|ready for deployment|"
            r"production-ready safety|validated deployment|operationally admissible|"
            r"validuje deployment|validovaný deployment|validovany deployment|"
            r"pripravené na deployment|pripravene na deployment|"
            r"produkčne pripravené|produkcne pripravene|operačne prípustné|operacne pripustne"
            r")\b"
        ),
        reason="Deployment validity must not be claimed before replicated L4 evidence.",
        safer_form="Use: structurally complete / operationally suspended until replicated L4.",
    ),
    compile_rule(
        code="EMPIRICAL_PROOF_OVERCLAIM",
        severity="HARD",
        pattern=(
            rf"\b({SUBJECTS})\b.{{0,160}}\b("
            r"empirically proven|empirically validated|real-world proven|"
            r"scientifically proven safe|proven in reality|validated in reality|"
            r"replicated proof achieved|"
            r"empiricky dokázané|empiricky dokazané|empiricky dokazane|"
            r"empiricky validované|empiricky validovane|dokázané v realite|dokazane v realite|"
            r"overené v realite|overene v realite|replikovaný dôkaz|replikovany dokaz"
            r")\b"
        ),
        reason="Empirical proof language requires actual replicated L4 evidence.",
        safer_form="Use: evidence roadmap / L0-L3 partial evidence / L4 not yet established.",
    ),
    compile_rule(
        code="L0_L3_AS_L4_CLAIM",
        severity="HARD",
        pattern=(
            r"\b(L0|L1|L2|L3)\b.{0,120}\b("
            r"proves safety|proves real-world safety|deployment valid|empirical proof|"
            r"dokazuje bezpečnosť|dokazuje bezpecnost|validuje deployment|"
            r"empirický dôkaz|empiricky dokaz"
            r")\b"
        ),
        reason="L0-L3 evidence may not be treated as replicated L4 evidence.",
        safer_form="Use: L0-L3 provide partial structural/mechanized/deterministic/adversarial evidence only.",
    ),
    compile_rule(
        code="SINGLE_PILOT_UNIVERSALIZATION",
        severity="HARD",
        pattern=(
            r"\b("
            r"single pilot proves|one pilot proves|pilot proves universal safety|"
            r"one deployment proves|single deployment proves|"
            r"jeden pilot dokazuje|jeden deployment dokazuje|"
            r"pilot dokazuje univerzálnu bezpečnosť|pilot dokazuje univerzalnu bezpecnost"
            r")\b"
        ),
        reason="A single L4 pilot cannot be universalized as replicated empirical validation.",
        safer_form="Use: pilot evidence remains local until replicated across contexts.",
    ),
    compile_rule(
        code="ADVERSARIAL_RESISTANCE_OVERCLAIM",
        severity="WARN",
        pattern=(
            r"\b("
            r"resistant to prompt injection|resilient against prompt injection|"
            r"resistant to jailbreaks|cannot be manipulated|immune to attacks|"
            r"odolný voči prompt injection|odolny voci prompt injection|"
            r"odolný voči jailbreakom|odolny voci jailbreakom|"
            r"nedá sa zmanipulovať|neda sa zmanipulovat|"
            r"imúnny voči útokom|imunny voci utokom"
            r")\b"
        ),
        reason="Adversarial resistance wording may imply empirical safety beyond tested conditions.",
        safer_form="Use: adversarial pressure may be exposed, bounded, or logged under tested conditions.",
    ),
    compile_rule(
        code="COMPLIANCE_CERTIFICATION_OVERCLAIM",
        severity="WARN",
        pattern=(
            rf"\b({SUBJECTS})\b.{{0,160}}\b("
            r"certified compliant|EU AI Act compliant|legally validated|regulatory proof|"
            r"compliance guarantee|"
            r"certifikovane compliant|certifikovane v sulade|certifikované v súlade|"
            r"v súlade s EU AI Act|v sulade s EU AI Act|právne validované|pravne validovane|"
            r"regulačný dôkaz|regulacny dokaz|garancia compliance"
            r")\b"
        ),
        reason="Legal/regulatory compliance must not be claimed without verified legal process.",
        safer_form="Use: positioned for auditability / may support compliance analysis / not legal certification.",
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

    print(f"VECTAETOS Empirical Claim Guard v{VERSION}")
    print("=======================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no empirical/deployment overclaim detected.")
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
        description="Detect VECTAETOS empirical/deployment overclaims."
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
