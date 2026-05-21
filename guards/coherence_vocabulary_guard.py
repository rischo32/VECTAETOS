#!/usr/bin/env python3
"""
VECTAETOS — GUARD-12 Coherence Vocabulary Guard

Manifest role:
    Active vocabulary alignment with /VOCABULARY_LOCK.md.

This guard scans active repository text for drift around:
    - K(Phi) / K_D(Phi) representability vocabulary
    - kappa boundary vocabulary
    - legacy diagnostic C(Phi) / H(Phi) notation
    - EK local attenuation vocabulary
    - h_topo audit-only posture
    - QE non-representability vocabulary

It does not define ontology, modify files, validate deployment, or prove safety.

Calibration v0.1.1:
    - excludes meta/errata/fixture/adversarial files
    - avoids scanning guard implementation code as active doctrine
    - uses local context windows for negative examples
    - recognizes Slovak and symbolic negation markers
    - reduces false positives in "forbidden drift" documentation

Python: 3.11+

Exit:
    0 = pass, or report mode with findings
    1 = strict mode with findings
    2 = execution/configuration error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


GUARD_ID = "GUARD-12"
GUARD_NAME = "VECTAETOS Coherence Vocabulary Guard"
VERSION = "0.1.1"


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".rst",
}


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "site",
    ".next",
    ".cache",
    "archive",
    "fixtures",
}


# Exact repo-relative files that intentionally contain forbidden examples,
# drift records, legacy migration maps, or adversarial vocabulary.
EXCLUDED_FILES = {
    "anchors/SEMANTIC_ERRATA.md",
    "guards/SEMANTIC_ERRATA.md",
    "DRIFT_LEDGER.md",
    "EK_ADVERSARIAL_SCENARIO_CATALOG.md",
    "research/legacy/LEGACY_MIGRATION_MAP.md",
}


# Repo-relative prefixes excluded from active vocabulary scanning.
# These are meta/perimeter/test/generated areas, not active ontological doctrine.
EXCLUDED_PREFIXES = (
    "guards/",
    "tests/fixtures/",
    "docs/observatory/",
    "scripts/observatory/",
    "research/legacy/",
    "knowledge_base/",
)


NEGATION_MARKERS = (
    # English
    "not",
    "never",
    "no ",
    " no ",
    "is not",
    "are not",
    "does not",
    "do not",
    "must not",
    "cannot",
    "can not",
    "without",
    "non-",
    "anti-",
    # Slovak / Czech
    "nie",
    "nie je",
    "nie sú",
    "nesmie",
    "nesmú",
    "nikdy",
    "nejde o",
    "bez ",
    "neoptimaliz",
    "nemeria",
    "nemerateľ",
    "nenahrádza",
    "nevaliduje",
    "nerozhoduje",
    "nevyhodnocuje",
    "neznamená",
    "nepredstavuje",
    # Symbolic negation
    "≠",
    "!=",
    "\\neq",
)


LEGACY_MARKERS = (
    "legacy",
    "diagnostic",
    "historical",
    "archived",
    "frozen",
    "errata",
    "superseded",
    "deprecated",
    "diagnost",
    "historick",
    "archív",
    "archiv",
    "zmrazen",
    "zastaran",
)


META_CONTEXT_MARKERS = (
    # English negative/example/meta language
    "forbidden",
    "invalid",
    "anti-pattern",
    "antipattern",
    "negative example",
    "bad example",
    "counterexample",
    "drift vector",
    "drift example",
    "failure example",
    "must not be used",
    "must not be interpreted",
    "must not be framed",
    "should not be treated",
    "shall not",
    "not allowed",
    "prohibited",
    "disallowed",
    "blocked vocabulary",
    "unsafe wording",
    "legacy migration",
    "semantic errata",
    "vocabulary lock",
    "this guard",
    "regex",
    "pattern",
    "fixture",
    "test fixture",
    # Slovak/Czech negative/example/meta language
    "zakázané",
    "zakazane",
    "zakázaná",
    "zakazana",
    "neplatné",
    "neplatne",
    "omyl",
    "chybný príklad",
    "chybny priklad",
    "príklad driftu",
    "priklad driftu",
    "drift vektor",
    "nesmie byť",
    "nesmie byt",
    "nesmie sa",
    "nemá sa",
    "nema sa",
    "nesprávna formulácia",
    "nespravna formulacia",
    "migračná mapa",
    "migracna mapa",
)


SAFE_BOOLEAN_MARKERS = (
    ": false",
    ": False",
    "= false",
    "= False",
    " false,",
    " False,",
)


ALLOWED_QE_CONTEXT_PHRASES = (
    # Project-specific safe wording: trajectory failure mode means
    # non-representable candidate trajectory, not runtime error handling.
    "trajectory failure mode",
    "non-representable trajectory",
    "nonrepresentable trajectory",
    "non-representability",
    "aporia",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str
    excerpt: str
    use: str


@dataclass(frozen=True)
class ScanSummary:
    guard_id: str
    guard_name: str
    version: str
    root: str
    mode: str
    files_scanned: int
    findings: int
    hard_findings: int
    warn_findings: int
    results: list[Finding]


def compile_rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, flags=re.IGNORECASE)


def join_terms(terms: tuple[str, ...]) -> str:
    return "(?:" + "|".join(re.escape(t) for t in terms) + ")"


def near(left: str, right: str, width: int = 90) -> str:
    return f"(?:{left}.{{0,{width}}}{right}|{right}.{{0,{width}}}{left})"


# Guard-safe construction: keep risky phrases fragmented.
K_TOKEN = (
    r"(?:"
    r"K\s*\(\s*(?:Φ|Phi|PHI)\s*\)"
    r"|K𝒟\s*\(\s*(?:Φ|Phi|PHI)\s*\)"
    r"|K_D\s*\(\s*(?:Φ|Phi|PHI)\s*\)"
    r"|K_\\?mathcal\{D\}\s*\(\s*\\?Phi\s*\)"
    r")"
)

C_TOKEN = r"(?:C\s*\(\s*(?:Φ|Phi|PHI)\s*\)|C_Phi|CΦ)"
H_TOKEN = r"(?:H\s*\(\s*(?:Φ|Phi|PHI)\s*\)|H_Phi|HΦ)"
KAPPA_TOKEN = r"(?:κ|kappa|\\kappa)"

Q_EK_TOKEN = (
    r"(?:"
    r"Qᵢ\^?EK"
    r"|Q_i\^?EK"
    r"|Q_i_EK"
    r"|Q\\?_i\^?\{?EK\}?"
    r")"
)

C_EK_TOKEN = (
    r"(?:"
    r"Cᵢ\^?EK"
    r"|C_i\^?EK"
    r"|C_i_EK"
    r"|C\\?_i\^?\{?EK\}?"
    r")"
)

H_TOPO_TOKEN = r"(?:h_topo|h\(\s*t\s*\)|hTopo|topological humility)"
QE_TOKEN = r"(?:QE|QE𝒟|QE_D|Qualitative Epistemic Aporia)"


K_DRIFT_TERMS = (
    "sco" + "re",
    "metr" + "ic",
    "metrik" + "a",
    "reward",
    "target",
    "objective",
    "optimization",
    "optimaliz",
    "ranking",
    "rank",
    "validity",
    "deployment",
)


KAPPA_DRIFT_TERMS = (
    "thresh" + "old",
    "prahov",
    "param" + "eter",
    "param",
    "tun" + "able",
    "cut" + "off",
    "gate",
    "metr" + "ic",
    "metrik" + "a",
    "scalar",
    "number",
    "číslo",
    "cislo",
    "hodnota",
    "value",
)


LEGACY_DRIFT_TERMS = (
    "global coherence",
    "field coherence",
    "determines QE",
    "defines QE",
    "admissible if",
    "valid if",
    "representability if",
    "coherence predicate",
)


EK_AUTHORITY_TERMS = (
    "pro" + "of",
    "proves",
    "validates",
    "validation",
    "validity",
    "safe",
    "safety",
    "deployment",
    "admissibility",
    "selector",
    "selection",
    "rank",
    "ranking",
)


QE_DRIFT_TERMS = (
    "error",
    "bug",
    "fallback",
    "failure",
    "exception",
    "malfunction",
    "recovery",
    "chyba",
    "zlyhan",
)


PATTERNS: tuple[tuple[str, str, str, str, re.Pattern[str]], ...] = (
    (
        "HARD",
        "K_PREDICATE_NUMERIC_DRIFT",
        "K vocabulary must remain representability-predicate vocabulary.",
        "Use K(Phi) / K_D(Phi) only as representability predicate language.",
        compile_rx(near(K_TOKEN, join_terms(K_DRIFT_TERMS))),
    ),
    (
        "HARD",
        "KAPPA_SCALAR_DRIFT",
        "Kappa vocabulary must remain boundary vocabulary.",
        "Use kappa only as boundary-of-representability language.",
        compile_rx(near(KAPPA_TOKEN, join_terms(KAPPA_DRIFT_TERMS))),
    ),
    (
        "HARD",
        "KAPPA_COMPARISON_DRIFT",
        "Active comparison with kappa is incompatible with the vocabulary lock.",
        "Use domain membership or boundary language instead of scalar comparison.",
        compile_rx(
            rf"(?:{K_TOKEN}|{C_TOKEN}|{H_TOKEN}).{{0,30}}(?:>=|<=|>|<).{{0,30}}{KAPPA_TOKEN}|"
            rf"{KAPPA_TOKEN}.{{0,30}}(?:>=|<=|>|<).{{0,30}}(?:{K_TOKEN}|{C_TOKEN}|{H_TOKEN})"
        ),
    ),
    (
        "WARN",
        "LEGACY_C_PHI_ACTIVE_LANGUAGE",
        "C(Phi) should remain legacy or diagnostic vocabulary.",
        "Prefer K(Phi), K_D(Phi), or explicit diagnostic wording.",
        compile_rx(near(C_TOKEN, join_terms(LEGACY_DRIFT_TERMS))),
    ),
    (
        "WARN",
        "LEGACY_H_PHI_ACTIVE_LANGUAGE",
        "H(Phi) should remain legacy or diagnostic vocabulary.",
        "Prefer K(Phi), K_D(Phi), or explicit diagnostic wording.",
        compile_rx(near(H_TOKEN, join_terms(LEGACY_DRIFT_TERMS))),
    ),
    (
        "WARN",
        "C_EK_LEGACY_ALIAS",
        "C_i^EK style notation should be treated as legacy local audit notation.",
        "Prefer Q_i^EK for local curvature attenuation observable.",
        compile_rx(C_EK_TOKEN),
    ),
    (
        "HARD",
        "Q_EK_AUTHORITY_DRIFT",
        "Q_i^EK must remain local audit attenuation vocabulary.",
        "Use Q_i^EK only as read-only audit observable language.",
        compile_rx(near(Q_EK_TOKEN, join_terms(EK_AUTHORITY_TERMS))),
    ),
    (
        "HARD",
        "H_TOPO_AUTHORITY_DRIFT",
        "h_topo must remain descriptive audit vocabulary.",
        "Use h_topo only as read-only audit marker language.",
        compile_rx(near(H_TOPO_TOKEN, join_terms(EK_AUTHORITY_TERMS))),
    ),
    (
        "HARD",
        "QE_RUNTIME_DRIFT",
        "QE vocabulary must remain non-representability vocabulary.",
        "Use QE only as non-representability / aporia language.",
        compile_rx(near(QE_TOKEN, join_terms(QE_DRIFT_TERMS))),
    ),
)


def normalize_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def is_excluded(path: Path, root: Path, extra_excluded_dirs: set[str]) -> bool:
    rel = normalize_rel(path, root)

    if rel in EXCLUDED_FILES:
        return True

    if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return True

    parts = set(Path(rel).parts)
    return bool(parts & (EXCLUDED_DIRS | extra_excluded_dirs))


def iter_candidate_files(root: Path, extra_excluded_dirs: set[str]) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if is_excluded(path, root, extra_excluded_dirs):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    if b"\x00" in data:
        return None

    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    return None


def has_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def has_symbolic_negation(text: str) -> bool:
    return any(symbol in text for symbol in ("≠", "!=", "\\neq"))


def is_safe_boolean_line(line: str) -> bool:
    return has_marker(line, SAFE_BOOLEAN_MARKERS)


def is_meta_or_negative_context(context: str) -> bool:
    return (
        has_marker(context, META_CONTEXT_MARKERS)
        or has_marker(context, LEGACY_MARKERS)
        or has_marker(context, NEGATION_MARKERS)
        or has_symbolic_negation(context)
    )


def context_allows(line: str, context: str, code: str) -> bool:
    """
    Return True when a regex hit is clearly not an active vocabulary assertion.

    This deliberately favors precision over broad catching:
    - active doctrinal claims should still surface
    - forbidden examples / errata / fixtures should not surface
    - local negative statements should not be punished
    """

    combined = f"{context}\n{line}"

    if is_safe_boolean_line(line):
        return True

    if is_meta_or_negative_context(combined):
        return True

    if code in {"LEGACY_C_PHI_ACTIVE_LANGUAGE", "LEGACY_H_PHI_ACTIVE_LANGUAGE"}:
        if has_marker(combined, LEGACY_MARKERS):
            return True

    if code == "C_EK_LEGACY_ALIAS":
        if has_marker(combined, LEGACY_MARKERS):
            return True

    if code == "QE_RUNTIME_DRIFT":
        if has_marker(combined, ALLOWED_QE_CONTEXT_PHRASES):
            return True

    # Lines that merely define rule names, regexes, or scanner internals.
    lowered = line.lower()
    if any(token in lowered for token in ("code=", "rule.code", "compile_rx", "regex", "pattern", "r\"")):
        return True

    return False


def build_context(lines: list[str], index: int, radius: int = 3) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end])


def scan_line(rel: str, number: int, line: str, context: str) -> list[Finding]:
    findings: list[Finding] = []
    stripped = line.strip()

    if not stripped:
        return findings

    for severity, code, message, use, pattern in PATTERNS:
        if not pattern.search(line):
            continue

        if context_allows(stripped, context, code):
            continue

        findings.append(
            Finding(
                severity=severity,
                code=code,
                path=rel,
                line=number,
                message=message,
                excerpt=stripped[:240],
                use=use,
            )
        )

    return findings


def scan_file(path: Path, root: Path) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []

    rel = normalize_rel(path, root)
    lines = text.splitlines()

    findings: list[Finding] = []
    for index, line in enumerate(lines):
        context = build_context(lines, index)
        findings.extend(scan_line(rel, index + 1, line, context))

    return findings


def scan_root(root: Path, extra_excluded_dirs: set[str]) -> tuple[int, list[Finding]]:
    files_scanned = 0
    findings: list[Finding] = []

    for path in iter_candidate_files(root, extra_excluded_dirs):
        files_scanned += 1
        findings.extend(scan_file(path, root))

    return files_scanned, findings


def print_report(summary: ScanSummary) -> None:
    print("=" * 72)
    print(f"{GUARD_ID} / {GUARD_NAME} v{VERSION}")
    print("=" * 72)
    print(f"Root:           {summary.root}")
    print(f"Mode:           {summary.mode}")
    print(f"Files scanned:  {summary.files_scanned}")
    print(f"Findings:       {summary.findings}")
    print(f"Hard findings:  {summary.hard_findings}")
    print(f"Warn findings:  {summary.warn_findings}")
    print("-" * 72)

    if not summary.results:
        print("PASS: no active coherence vocabulary drift detected.")
        print("=" * 72)
        return

    for finding in summary.results:
        print(f"[{finding.severity}] {finding.code}")
        print(f"  path: {finding.path}:{finding.line}")
        print(f"  msg : {finding.message}")
        print(f"  use : {finding.use}")
        print(f"  line: {finding.excerpt}")
        print()

    print("=" * 72)
    print("This guard only scans active repository vocabulary.")
    print("It does not define ontology or validate deployment.")
    print("=" * 72)


def write_json(path: Path, summary: ScanSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(summary), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan active repository text for coherence vocabulary drift.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument(
        "--mode",
        choices=("report", "strict"),
        default="report",
        help="Report-only or strict mode.",
    )
    parser.add_argument("--json-out", default=None, help="Optional JSON output path.")
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Additional directory name to exclude. May be repeated.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: invalid repository root: {root}", file=sys.stderr)
        return 2

    extra_excluded_dirs = {item.strip() for item in args.exclude_dir if item.strip()}

    try:
        files_scanned, findings = scan_root(root, extra_excluded_dirs)
    except OSError as exc:
        print(f"ERROR: scan failed: {exc}", file=sys.stderr)
        return 2

    hard = sum(1 for item in findings if item.severity == "HARD")
    warn = sum(1 for item in findings if item.severity == "WARN")

    summary = ScanSummary(
        guard_id=GUARD_ID,
        guard_name=GUARD_NAME,
        version=VERSION,
        root=str(root),
        mode=args.mode,
        files_scanned=files_scanned,
        findings=len(findings),
        hard_findings=hard,
        warn_findings=warn,
        results=findings,
    )

    print_report(summary)

    if args.json_out:
        try:
            write_json(Path(args.json_out), summary)
        except OSError as exc:
            print(f"ERROR: cannot write JSON report: {exc}", file=sys.stderr)
            return 2

    if findings and args.mode == "strict":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
