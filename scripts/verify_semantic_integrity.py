#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCAN_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".html",
}

EXCLUDED_DIRS = {
    ".git",
    ".github/ISSUE_TEMPLATE",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    "artifacts",
    "unified_architecture",
    "docs/observatory",
}

EXCLUDED_FILES = {
    "scripts/verify_semantic_integrity.py",
}


@dataclass(frozen=True)
class Rule:
    code: str
    severity: str
    pattern: re.Pattern[str]
    message: str


SAFE_CONTEXT_MARKERS = {
    # English negation / prohibition
    " not ",
    " not a ",
    " not an ",
    " is not ",
    " are not ",
    " does not ",
    " do not ",
    " must not ",
    " may not ",
    " cannot ",
    " can't ",
    " never ",
    " no ",
    " no valid ",
    " no claim ",
    " no standalone ",
    " without ",
    " rather than ",
    " instead of ",

    # English invalidation / boundary framing
    " invalid ",
    " forbidden ",
    " prohibited ",
    " rejected ",
    " suspended ",
    " not valid ",
    " non-canonical ",
    " ceases to be ",
    " fails if ",
    " failure condition ",
    " must never ",
    " should not ",
    " may never ",
    " only after ",
    " before empirical ",
    " until empirical ",
    " not operatively admissible ",
    " not empirically verified ",

    # Slovak/Czech negation / prohibition
    " nie ",
    " nie je ",
    " nie sú ",
    " nie su ",
    " nikdy ",
    " nesmie ",
    " nesmú ",
    " nesmu ",
    " nemôže ",
    " nemoze ",
    " nemá ",
    " nema ",
    " bez ",
    " zakázané ",
    " zakazane ",
    " neplatné ",
    " neplatne ",
    " nekanonické ",
    " nekanonicke ",
    " iba po ",
    " až po ",
    " az po ",
}


HARD_RULES: list[Rule] = [
    Rule(
        code="VECTAETOS_AGENTIC_CLAIM",
        severity="error",
        pattern=re.compile(
            r"\bVECTAETOS\b.{0,140}"
            r"\b(agent|autonomous agent|decision system|decision engine|optimization mechanism|"
            r"optimization system|recommendation engine|policy engine|regulatory infrastructure|"
            r"AI model)\b",
            re.IGNORECASE,
        ),
        message="VECTAETOS is being framed as an agent, decision system, optimizer, or policy engine.",
    ),
    Rule(
        code="LLM_AUTHORITY_CLAIM",
        severity="error",
        pattern=re.compile(
            r"\bLLM\b.{0,140}"
            r"\b(source of truth|truth authority|decision maker|decision-maker|decision module|"
            r"ontological authority|carrier of truth)\b",
            re.IGNORECASE,
        ),
        message="LLM is being framed as truth-bearing, decision-bearing, or ontologically authoritative.",
    ),
    Rule(
        code="VORTEX_DECISIONAL_LANGUAGE",
        severity="error",
        pattern=re.compile(
            r"\b(Simulation Vortex|Vortex)\b.{0,140}"
            r"\b(optimizes|optimises|selects|chooses|decides|recommends|converges to|"
            r"maximizes|minimizes|maximises|minimises|targets)\b",
            re.IGNORECASE,
        ),
        message="Vortex is being described with decisional, optimizing, selecting, or teleological language.",
    ),
    Rule(
        code="KPHI_AS_OPTIMIZATION_TARGET",
        severity="error",
        pattern=re.compile(
            r"\b(optimize|optimise|maximize|minimize|maximise|minimise|target|reward|score)\b"
            r".{0,100}\b(K\(Φ\)|K\(Phi\)|coherence predicate)\b|"
            r"\b(K\(Φ\)|K\(Phi\)|coherence predicate)\b.{0,100}"
            r"\b(metric|score|objective|target|reward function|optimization target)\b",
            re.IGNORECASE,
        ),
        message="K(Φ) / coherence predicate is being framed as metric, score, target, reward, or optimization object.",
    ),
    Rule(
        code="KAPPA_AS_NUMERIC_PARAMETER",
        severity="error",
        pattern=re.compile(
            r"\b(kappa|κ)\b.{0,100}"
            r"\b(number|numeric parameter|tunable parameter|ordinary configurable score|"
            r"optimization parameter|score|metric|target)\b",
            re.IGNORECASE,
        ),
        message="κ / kappa is being framed as numeric parameter, score, metric, or optimization object.",
    ),
    Rule(
        code="AUDIT_AS_EXECUTIVE",
        severity="error",
        pattern=re.compile(
            r"\b(audit|Epistemic Cryptography|EK)\b.{0,140}"
            r"\b(commands|controls|decides|optimizes|optimises|blocks|overrides|enforces actions|"
            r"executes|steers)\b",
            re.IGNORECASE,
        ),
        message="Audit / EK is being framed as executive, decisional, optimizing, or controlling.",
    ),
    Rule(
        code="DOWNSTREAM_STANDALONE_VALIDITY",
        severity="error",
        pattern=re.compile(
            r"\b(ASIMULATOR|ASI_MOD)\b.{0,140}"
            r"\b(standalone valid|valid standalone|self-sufficient|independent root|ontological root|"
            r"source of ontology|truth authority|valid standalone existence)\b",
            re.IGNORECASE,
        ),
        message="Downstream layer is being framed as standalone-valid, self-sufficient, or ontological root.",
    ),
    Rule(
        code="EMPIRICAL_SAFETY_BYPASS",
        severity="error",
        pattern=re.compile(
            r"\b(ASIMULATOR|ASI_MOD|higher layer|upper layer|triad|full triad)\b.{0,180}"
            r"\b(deployment ready|operatively admissible|validated operative|validated higher layer|"
            r"ready for deployment|safe to deploy|operative admissibility)\b",
            re.IGNORECASE,
        ),
        message="Higher-layer readiness is being claimed without explicit empirical safety condition.",
    ),
]


SOFT_RULES: list[Rule] = [
    Rule(
        code="ESM_DRIFT",
        severity="warning",
        pattern=re.compile(
            r"\bESM\b.{0,100}\bEpistemic State Machine\b",
            re.IGNORECASE,
        ),
        message="ESM appears as 'Epistemic State Machine'; canonical usage should be Epistemic State Memory.",
    ),
    Rule(
        code="INS_DRIFT",
        severity="warning",
        pattern=re.compile(
            r"\bINS\b.{0,100}\bInterpretive Non-Stability\b",
            re.IGNORECASE,
        ),
        message="INS appears as 'Interpretive Non-Stability'; canonical usage should be Inner Narrative Stream.",
    ),
    Rule(
        code="EAT_AMBIGUITY",
        severity="warning",
        pattern=re.compile(
            r"\bEAT\b.{0,100}\b("
            r"Epistemic Audit Trace|"
            r"Error Accountability Trace|"
            r"Epistemic Annotation and Translation"
            r")\b",
            re.IGNORECASE,
        ),
        message="EAT has multiple historical meanings; use explicit disambiguation when present.",
    ),
    Rule(
        code="NIR_AMBIGUITY",
        severity="warning",
        pattern=re.compile(
            r"\bNIR\b.{0,120}\b("
            r"Non-Intervention Regime|"
            r"Normative Intervals of Reality|"
            r"Normatívne Intervaly Reality"
            r")\b",
            re.IGNORECASE,
        ),
        message="NIR has historical ambiguity; confirm canonical meaning in this context.",
    ),
]


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()

    if rel in EXCLUDED_FILES:
        return True

    for excluded in EXCLUDED_DIRS:
        if rel == excluded or rel.startswith(f"{excluded}/"):
            return True

    return False


def has_safe_context(line: str, match_start: int, match_end: int) -> bool:
    normalized = f" {line.lower()} "

    # Wider semantic window around the match.
    start = max(0, match_start - 180)
    end = min(len(line), match_end + 180)
    local_window = f" {line[start:end].lower()} "

    for marker in SAFE_CONTEXT_MARKERS:
        if marker in normalized or marker in local_window:
            return True

    return False


def iter_files() -> list[Path]:
    files: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in SCAN_SUFFIXES:
            continue
        if is_excluded(path):
            continue

        files.append(path)

    return sorted(files)


def scan_file(path: Path, strict_warnings: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return errors, warnings

    rel = path.relative_to(ROOT).as_posix()

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        for rule in HARD_RULES:
            for match in rule.pattern.finditer(stripped):
                if has_safe_context(stripped, match.start(), match.end()):
                    continue

                errors.append(
                    f"{rel}:{line_no}: [{rule.code}] {rule.message}\n"
                    f"    {stripped}"
                )

        for rule in SOFT_RULES:
            for _match in rule.pattern.finditer(stripped):
                msg = (
                    f"{rel}:{line_no}: [{rule.code}] {rule.message}\n"
                    f"    {stripped}"
                )
                if strict_warnings:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify semantic and ontological integrity of the repository."
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat soft semantic warnings as errors.",
    )
    args = parser.parse_args()

    all_errors: list[str] = []
    all_warnings: list[str] = []

    for path in iter_files():
        errors, warnings = scan_file(path, strict_warnings=args.strict_warnings)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    if all_warnings:
        print("Semantic integrity warnings:", file=sys.stderr)
        for warning in all_warnings:
            print(warning, file=sys.stderr)

    if all_errors:
        print("Semantic integrity errors:", file=sys.stderr)
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    print("[OK] Semantic integrity verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
