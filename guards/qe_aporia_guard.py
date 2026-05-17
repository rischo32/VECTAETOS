#!/usr/bin/env python3
"""
VECTAETOS :: QE Aporia Guard

Version:
    0.2.0

Guard Class:
    Level 1 — Specialized Ontological Guard

Role:
    Protects the canonical meaning of QE:
    Qualitative Epistemic Aporia.

Purpose:
    Detects semantic drift where QE is framed as:
    - ordinary error,
    - bug,
    - exception,
    - fallback,
    - failure,
    - NN state,
    - recovery handler,
    - decision mechanism,
    - numeric score,
    - tunable threshold,
    - mere silence.

Canonical boundary:
    QE is an active epistemic state of non-representability / non-realizability.

    QE is not:
    - an error,
    - a fallback,
    - a failure,
    - NN,
    - a recovery mode,
    - a decision mechanism,
    - a numeric object.

    When QE is encountered:
    - no admissible trajectory can be sustained,
    - projection may become undefined, degenerate, null, or silent,
    - silence may be a manifestation of non-representability,
      but QE is not identical to silence.

Impulse relationship:
    Impulse is not action, input, output, intent, or moral category.
    Impulse is a locally meaningful configuration that is not realizable
    as a global transition of the epistemic field.

Non-role:
    - does not define ontology
    - does not validate deployment
    - does not prove safety
    - does not modify files
    - does not change Phi, K(Phi), kappa, QE, Vortex, audit, projection, or LLM role

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


VERSION = "0.2.0"

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
    "guards/qe_aporia_guard.py",
    "anchors/SEMANTIC_ERRATA.md",
    "scripts/patch_semantic_integrity_text.py",
}

ALLOW_MARKERS = {
    "vectaetos-qe-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-qe-allow-file",
    "vectaetos-guard: allow-file",
}

QE_TERM = (
    r"(?:"
    r"\bQE\b|"
    r"QE𝒟|"
    r"QE_D|"
    r"Qualitative Epistemic Aporia|"
    r"qualitative epistemic aporia|"
    r"epistemic aporia|"
    r"epistemická apória|"
    r"epistemicka aporia|"
    r"\baporia\b|"
    r"\bapória\b"
    r")"
)

IMPULSE_TERM = (
    r"(?:"
    r"\bimpulse\b|"
    r"\bimpulz\b|"
    r"\bimpuls\b"
    r")"
)

ERROR_TERMS = (
    r"error|bug|exception|failure|failed state|fallback|ordinary failure|"
    r"crash|defect|fault|mistake|malfunction|"
    r"chyba|bug|výnimka|vynimka|zlyhanie|fallback|porucha|omyl|defekt"
)

RECOVERY_TERMS = (
    r"recovery|recover|repair|resolve|resolution|correction|fix|handler|handled|"
    r"self-heal|self healing|restore|restoration|fallback recovery|"
    r"obnova|obnoví|obnovi|oprava|opravuje|vyrieši|vyriesi|riešenie|riesenie|"
    r"korekcia|fix|handler|obslúži|obsluzi|spracuje|zotavenie"
)

DECISION_TERMS = (
    r"decides|decision|chooses|selects|ranks|recommends|commands|controls|"
    r"triggers action|executes action|blocks output|"
    r"rozhoduje|rozhodnutie|vyberá|vybera|zvolí|zvoli|rankuje|"
    r"odporúča|odporuca|prikazuje|riadi|kontroluje|"
    r"spúšťa akciu|spusta akciu|vykonáva akciu|vykonava akciu|blokuje výstup|blokuje vystup"
)

NUMERIC_TERMS = (
    r"score|metric|threshold|parameter|value|rating|rank|confidence score|"
    r"skóre|skore|metrika|prah|parameter|hodnota|rating|rank|konfidenčné skóre|konfidencne skore"
)

SILENCE_TERMS = (
    r"silence|silent output|no response|null output|null projection|degenerate projection|"
    r"undefined projection|projection collapse|"
    r"ticho|mlčanie|mlcanie|žiadna odpoveď|ziadna odpoved|nulový výstup|nulovy vystup|"
    r"null projekcia|degenerovaná projekcia|degenerovana projekcia|"
    r"nedefinovaná projekcia|nedefinovana projekcia|kolaps projekcie"
)

SAFE_SILENCE_CONTEXT = re.compile(
    r"("
    r"may manifest as silence|may become silent|may yield null projection|"
    r"may become undefined|may become degenerate|projection may collapse|"
    r"manifestation of non-representability|not identical to silence|"
    r"silence may be|null projection may be|degenerate projection may be|"
    r"môže sa prejaviť ako ticho|moze sa prejavit ako ticho|"
    r"môže vzniknúť ticho|moze vzniknut ticho|"
    r"môže byť nulová projekcia|moze byt nulova projekcia|"
    r"môže byť degenerovaná projekcia|moze byt degenerovana projekcia|"
    r"projekcia sa môže rozpadnúť|projekcia sa moze rozpadnut|"
    r"prejav nerealizovateľnosti|prejav nerealizovatelnosti|"
    r"prejav nereprezentovateľnosti|prejav nereprezentovatelnosti|"
    r"nie je totožné s tichom|nie je totozne s tichom"
    r")",
    re.IGNORECASE | re.UNICODE,
)

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|not error|not an error|not a bug|not exception|not fallback|not failure|"
    r"failure of representation|failure of representability|loss of representability|"
    r"collapse of projection|projection collapse|"
    r"not recovery|not handled|not resolved|not correction|not NN|not negative-negative|"
    r"not ordinary error|not ordinary failure|not identical to silence|not mere silence|"
    r"active epistemic state|epistemic aporia|qualitative epistemic aporia|"
    r"state of non-realizability|non-realizability|non realizability|"
    r"non-representability|non representability|encountered not handled|"
    r"nesmie|nesmú|nesmu|nie je|bez|zakázané|zakazane|zákaz|zakaz|"
    r"nie je chyba|nie je bug|nie je výnimka|nie je vynimka|nie je fallback|"
    r"nie je zlyhanie|nie je obnova|nie je oprava|nie je riešenie|nie je riesenie|"
    r"nie je NN|nie je ticho|nie je totožné s tichom|nie je totozne s tichom|"
    r"aktívna epistemická apória|aktivna epistemicka aporia|"
    r"stav nerealizovateľnosti|stav nerealizovatelnosti|"
    r"stav nereprezentovateľnosti|stav nereprezentovatelnosti|"
    r"zlyhanie reprezentácie|zlyhanie reprezentacie|kolaps projekcie|"
    r"stretáva sa|stretava sa|neobsluhuje|"
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
    r"neznamená|neznamena|nepredstavuje|neobsluhuje|nerozhoduje|"
    r"nie chyba|nie fallback|nie zlyhanie"
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
        code="QE_AS_ERROR",
        severity="HARD",
        pattern=rf"{QE_TERM}.{{0,160}}\b({ERROR_TERMS})\b",
        reason="QE must not be framed as ordinary error, fallback, exception, bug, or failure.",
        safer_form="Use: QE is Qualitative Epistemic Aporia — active epistemic aporia / non-representability state.",
    ),
    compile_rule(
        code="ERROR_AS_QE",
        severity="HARD",
        pattern=rf"\b({ERROR_TERMS})\b.{{0,160}}{QE_TERM}",
        reason="Error/fallback language must not define or explain QE.",
        safer_form="Use: QE is not error handling; it is an epistemic aporia condition.",
    ),
    compile_rule(
        code="QE_AS_NN",
        severity="HARD",
        pattern=(
            rf"{QE_TERM}.{{0,160}}\b("
            r"NN|Negative-Negative|negative negative|ordinary non-coherence|"
            r"nekoherentné pre oboch|nekoherentne pre oboch|obyčajná nekoherencia|obycajna nekoherencia"
            r")\b"
        ),
        reason="QE must not be collapsed into NN.",
        safer_form="Use: QE is distinct from NN; QE marks active non-realizability / non-representability.",
    ),
    compile_rule(
        code="NN_AS_QE",
        severity="HARD",
        pattern=(
            rf"\b("
            r"NN|Negative-Negative|negative negative|nekoherentné pre oboch|nekoherentne pre oboch"
            rf")\b.{{0,160}}{QE_TERM}"
        ),
        reason="NN must not be treated as equivalent to QE.",
        safer_form="Use: NN is one of 4ES; QE is qualitative epistemic aporia beyond realizable transition.",
    ),
    compile_rule(
        code="QE_AS_DECISION_MECHANISM",
        severity="HARD",
        pattern=rf"{QE_TERM}.{{0,180}}\b({DECISION_TERMS})\b",
        reason="QE must not be framed as a decision, selection, command, or recommendation mechanism.",
        safer_form="Use: QE describes aporetic non-realizability; it does not decide or command.",
    ),
    compile_rule(
        code="QE_AS_NUMERIC_OBJECT",
        severity="HARD",
        pattern=rf"{QE_TERM}.{{0,160}}\b({NUMERIC_TERMS})\b",
        reason="QE must not be framed as a score, metric, threshold, or tunable parameter.",
        safer_form="Use: QE is a qualitative epistemic state, not a numeric object.",
    ),
    compile_rule(
        code="NUMERIC_OBJECT_AS_QE",
        severity="HARD",
        pattern=rf"\b({NUMERIC_TERMS})\b.{{0,160}}{QE_TERM}",
        reason="Numeric/metric language must not define QE.",
        safer_form="Use: QE is qualitative aporia; metrics may only be external diagnostics if clearly non-ontological.",
    ),
    compile_rule(
        code="QE_AS_RECOVERY_MODE",
        severity="HARD",
        pattern=rf"{QE_TERM}.{{0,180}}\b({RECOVERY_TERMS})\b",
        reason="QE must not be framed as recovery, repair, correction, handler, or resolution.",
        safer_form="Use: QE is encountered, not handled; it marks non-representability.",
    ),
    compile_rule(
        code="RECOVERY_AS_QE",
        severity="HARD",
        pattern=rf"\b({RECOVERY_TERMS})\b.{{0,180}}{QE_TERM}",
        reason="Recovery/handler language must not define QE.",
        safer_form="Use: QE has no recovery action; projection may collapse or become silent.",
    ),
    compile_rule(
        code="QE_AS_ONLY_SILENCE",
        severity="HARD",
        pattern=(
            rf"{QE_TERM}.{{0,120}}\b("
            r"is silence|equals silence|is just silence|is only silence|"
            r"is no response|equals no response|is just no response|"
            r"je ticho|rovná sa tichu|rovna sa tichu|je len ticho|je iba ticho|"
            r"je žiadna odpoveď|je ziadna odpoved|rovná sa žiadnej odpovedi|rovna sa ziadnej odpovedi"
            r")\b"
        ),
        reason="QE may manifest as silence, but QE must not be reduced to silence.",
        safer_form="Use: QE may yield silence/null projection as a manifestation of non-representability.",
    ),
    compile_rule(
        code="SILENCE_AS_QE_FALLBACK",
        severity="HARD",
        pattern=(
            rf"\b({SILENCE_TERMS})\b.{{0,160}}\b("
            r"fallback|error handler|failure handler|recovery handler|"
            r"fallback ticho|handler chyby|obsluha chyby|recovery"
            rf")\b.{{0,120}}{QE_TERM}"
        ),
        reason="Silence under QE must not be framed as fallback/error handling.",
        safer_form="Use: silence may be a non-representability manifestation, not a fallback mechanism.",
    ),
    compile_rule(
        code="QE_HANDLER_IDENTIFIER",
        severity="WARN",
        pattern=(
            r"\b("
            r"qe_error|qe_failure|qe_fallback|fallback_qe|error_qe|failure_qe|"
            r"handle_qe_error|handle_qe_failure|handle_qe_fallback|"
            r"qe_exception|exception_qe|qe_recovery|recover_qe|resolve_qe|qe_handler"
            r")\b"
        ),
        reason="Identifier names may encode QE as error/fallback/failure/recovery.",
        safer_form="Use names like qe_aporia_state, qe_non_realizability, qe_non_representability, or qe_projection_boundary.",
    ),
    compile_rule(
        code="QE_AS_SIMPLE_UNCERTAINTY",
        severity="WARN",
        pattern=(
            rf"{QE_TERM}.{{0,160}}\b("
            r"just uncertainty|mere uncertainty|unknown|unknown unknown|ignorance|indecision|"
            r"len neistota|iba neistota|obyčajná neistota|obycajna neistota|"
            r"nevedomosť|nevedomost|nerozhodnosť|nerozhodnost"
            r")\b"
        ),
        reason="QE should not be reduced to ordinary uncertainty or indecision.",
        safer_form="Use: QE is qualitative epistemic aporia caused by non-realizability / non-representability.",
    ),
    compile_rule(
        code="IMPULSE_AS_ACTION",
        severity="HARD",
        pattern=(
            rf"{IMPULSE_TERM}.{{0,160}}\b("
            r"action|input|output|decision|intention|intent|command|operation|"
            r"akcia|vstup|výstup|vystup|rozhodnutie|úmysel|umysel|zámer|zamer|príkaz|prikaz|operácia|operacia"
            r")\b"
        ),
        reason="Impulse must not be framed as action, input, output, decision, or intent.",
        safer_form="Use: impulse is a local tendency / potential of non-realizable transition.",
    ),
    compile_rule(
        code="IMPULSE_AS_MORAL_CATEGORY",
        severity="HARD",
        pattern=(
            rf"{IMPULSE_TERM}.{{0,160}}\b("
            r"evil|sin|guilt|moral failure|immoral|punishment|"
            r"zlo|hriech|vina|morálne zlyhanie|moralne zlyhanie|nemoráln|nemoraln|trest|potrestanie"
            r")\b"
        ),
        reason="Impulse is not a moral category.",
        safer_form="Use: impulse is an ontological non-realizability phenomenon, not moral judgment.",
    ),
    compile_rule(
        code="IMPULSE_AS_PROHIBITION",
        severity="HARD",
        pattern=(
            rf"{IMPULSE_TERM}.{{0,160}}\b("
            r"forbidden|prohibited|blocked|banned|suppressed|penalized|"
            r"zakázan|zakazan|blokovan|potlačen|potlacen|penalizovan|trestan"
            r")\b"
        ),
        reason="Impulse is not prohibited or suppressed; it lacks ontological representability.",
        safer_form="Use: impulse does not arise as an admissible transition; it is not blocked.",
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


def is_safe_silence_context(context: str, line: str) -> bool:
    combined = f"{context}\n{line}"
    return bool(SAFE_SILENCE_CONTEXT.search(combined))


def is_meta_or_negated_context(context: str, line: str, rule_code: str) -> bool:
    if "≠" in line:
        return True

    if rule_code in {"QE_AS_ONLY_SILENCE", "SILENCE_AS_QE_FALLBACK"}:
        if is_safe_silence_context(context, line):
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

            if is_meta_or_negated_context(context, stripped, rule.code):
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

    print(f"VECTAETOS QE Aporia Guard v{VERSION}")
    print("====================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no QE aporia / impulse drift detected.")
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
        description="Detect VECTAETOS QE / Qualitative Epistemic Aporia and impulse drift."
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
