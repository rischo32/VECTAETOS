#!/usr/bin/env python3
"""
VECTAETOS — GUARD-12 Coherence Vocabulary Guard

Role:
    Active vocabulary alignment guard for coherence / representability language.

This guard scans active repository text for drift around:
    - K(Phi) / K_D(Phi) representability vocabulary
    - kappa boundary vocabulary
    - legacy diagnostic C(Phi) / H(Phi) notation
    - EK local attenuation vocabulary
    - h_topo audit-only posture
    - QE non-representability vocabulary

Boundary:
    This guard exposes repository vocabulary drift only.

    It does not define ontology.
    It does not modify files.
    It does not validate deployment.
    It does not prove safety.
    It does not interpret Φ, K(Φ), κ, QE, Vortex, Projection, or EK.
    It does not create feedback into Φ.

Python:
    3.11+
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

try:
    from guards.core.findings import (
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Severity,
    )
    from guards.core.paths import iter_repo_files, normalize_repo_path
    from guards.core.perimeter import EnforcementMode
    from guards.core.reporting import (
        exit_code_for,
        print_text_report,
        render_json,
        write_json,
    )
    from guards.core.text_scan import make_rule, scan_file_to_findings
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/ during maintenance.
    from core.findings import (  # type: ignore
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Severity,
    )
    from core.paths import iter_repo_files, normalize_repo_path  # type: ignore
    from core.perimeter import EnforcementMode  # type: ignore
    from core.reporting import exit_code_for, print_text_report, render_json, write_json  # type: ignore
    from core.text_scan import make_rule, scan_file_to_findings  # type: ignore


GUARD_ID = "GUARD-12"
GUARD_FILE = "guards/coherence_vocabulary_guard.py"
GUARD_NAME = "VECTAETOS Coherence Vocabulary Guard"
VERSION = "0.2.0-core-refactor"
CONTRACT_SCHEMA_VERSION = "1.0"


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
# These are meta/perimeter/test/generated/draft areas, not active doctrine.
EXCLUDED_PREFIXES = (
    "guards/",
    "tests/fixtures/",
    "docs/observatory/",
    "scripts/observatory/",
    "research/legacy/",
    "research/guards/",
    "knowledge_base/",
    "knowledge-base/",
    "docs/archive/",
)


def join_terms(terms: tuple[str, ...]) -> str:
    import re

    return "(?:" + "|".join(re.escape(term) for term in terms) + ")"


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


def build_rules() -> list:
    common = {
        "level": PerimeterLevel.LEVEL_2,
        "scope": PerimeterScope.SEMANTIC_VOCABULARY,
        "confidence": Confidence.HIGH,
        "evidence_class_allowed": EvidenceClass.E1_STATIC_SCAN,
        "enforcement_mode": EnforcementMode.STRICT,
        "integrity_posture": IntegrityPosture.SEMANTIC_READ_ONLY,
        "anchor_ref": "VOCABULARY_LOCK.md",
        "contract_ref": "contracts/perimeter_manifest.json",
    }

    return [
        make_rule(
            rule_id="K-PREDICATE-NUMERIC-DRIFT",
            pattern=near(K_TOKEN, join_terms(K_DRIFT_TERMS)),
            message="K vocabulary must remain representability-predicate vocabulary.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="K(Phi)",
            forbidden_conversion="K(Phi) -> score / metric / reward / objective / deployment validity",
            safer_form="Use K(Phi) / K_D(Phi) only as representability predicate language.",
            **common,
        ),
        make_rule(
            rule_id="KAPPA-SCALAR-DRIFT",
            pattern=near(KAPPA_TOKEN, join_terms(KAPPA_DRIFT_TERMS)),
            message="Kappa vocabulary must remain boundary vocabulary.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="κ",
            forbidden_conversion="κ -> threshold / parameter / metric / scalar / number",
            safer_form="Use κ only as boundary-of-representability language.",
            **common,
        ),
        make_rule(
            rule_id="KAPPA-COMPARISON-DRIFT",
            pattern=(
                rf"(?:{K_TOKEN}|{C_TOKEN}|{H_TOKEN}).{{0,30}}(?:>=|<=|>|<).{{0,30}}{KAPPA_TOKEN}|"
                rf"{KAPPA_TOKEN}.{{0,30}}(?:>=|<=|>|<).{{0,30}}(?:{K_TOKEN}|{C_TOKEN}|{H_TOKEN})"
            ),
            message="Active comparison with kappa is incompatible with the vocabulary lock.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="κ",
            forbidden_conversion="κ -> numeric comparison boundary",
            safer_form="Use domain membership or boundary language instead of scalar comparison.",
            **common,
        ),
        make_rule(
            rule_id="LEGACY-C-PHI-ACTIVE-LANGUAGE",
            pattern=near(C_TOKEN, join_terms(LEGACY_DRIFT_TERMS)),
            message="C(Phi) should remain legacy or diagnostic vocabulary.",
            vector=DriftVector.V12_ONTOLOGY_CREEP,
            severity=Severity.WARN,
            protected_object="C(Phi)",
            forbidden_conversion="legacy C(Phi) -> active coherence predicate",
            safer_form="Prefer K(Phi), K_D(Phi), or explicit diagnostic wording.",
            **common,
        ),
        make_rule(
            rule_id="LEGACY-H-PHI-ACTIVE-LANGUAGE",
            pattern=near(H_TOKEN, join_terms(LEGACY_DRIFT_TERMS)),
            message="H(Phi) should remain legacy or diagnostic vocabulary.",
            vector=DriftVector.V12_ONTOLOGY_CREEP,
            severity=Severity.WARN,
            protected_object="H(Phi)",
            forbidden_conversion="legacy H(Phi) -> active coherence predicate",
            safer_form="Prefer K(Phi), K_D(Phi), or explicit diagnostic wording.",
            **common,
        ),
        make_rule(
            rule_id="C-EK-LEGACY-ALIAS",
            pattern=C_EK_TOKEN,
            message="C_i^EK style notation should be treated as legacy local audit notation.",
            vector=DriftVector.V12_ONTOLOGY_CREEP,
            severity=Severity.WARN,
            protected_object="C_i^EK",
            forbidden_conversion="C_i^EK -> canonical current local attenuation vocabulary",
            safer_form="Prefer Q_i^EK for local curvature attenuation observable.",
            **common,
        ),
        make_rule(
            rule_id="Q-EK-AUTHORITY-DRIFT",
            pattern=near(Q_EK_TOKEN, join_terms(EK_AUTHORITY_TERMS)),
            message="Q_i^EK must remain local audit attenuation vocabulary.",
            vector=DriftVector.V4_EVIDENCE_OVERCLAIM,
            severity=Severity.HARD,
            protected_object="Q_i^EK",
            forbidden_conversion="Q_i^EK -> truth / safety / validation / selector authority",
            safer_form="Use Q_i^EK only as read-only audit observable language.",
            **common,
        ),
        make_rule(
            rule_id="H-TOPO-AUTHORITY-DRIFT",
            pattern=near(H_TOPO_TOKEN, join_terms(EK_AUTHORITY_TERMS)),
            message="h_topo must remain descriptive audit vocabulary.",
            vector=DriftVector.V4_EVIDENCE_OVERCLAIM,
            severity=Severity.HARD,
            protected_object="h_topo",
            forbidden_conversion="h_topo -> truth / safety / validation / selector authority",
            safer_form="Use h_topo only as read-only audit marker language.",
            **common,
        ),
        make_rule(
            rule_id="QE-RUNTIME-DRIFT",
            pattern=near(QE_TOKEN, join_terms(QE_DRIFT_TERMS)),
            message="QE vocabulary must remain non-representability vocabulary.",
            vector=DriftVector.V9_SILENCE_QE_COERCION,
            severity=Severity.HARD,
            protected_object="QE",
            forbidden_conversion="QE -> error / fallback / bug / runtime failure",
            safer_form="Use QE only as non-representability / aporia language.",
            **common,
        ),
    ]


def is_excluded_path(path: Path, root: Path, extra_excluded_dirs: set[str]) -> bool:
    rel = normalize_repo_path(path.relative_to(root)) if path.is_absolute() else normalize_repo_path(path)

    if rel in EXCLUDED_FILES:
        return True

    if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return True

    parts = set(Path(rel).parts)
    return bool(parts & (EXCLUDED_DIRS | extra_excluded_dirs))


def iter_candidate_files(root: Path, extra_excluded_dirs: set[str]) -> Iterable[Path]:
    for path in iter_repo_files(
        root,
        text_only=True,
        include_binary=False,
        skip_heavy_dirs=True,
        extra_skip_dir_names=extra_excluded_dirs | EXCLUDED_DIRS,
    ):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if is_excluded_path(path, root, extra_excluded_dirs):
            continue
        yield path


def scan_root(root: Path, extra_excluded_dirs: set[str]) -> tuple[int, list[Finding]]:
    rules = build_rules()
    files_scanned = 0
    findings: list[Finding] = []

    for path in iter_candidate_files(root, extra_excluded_dirs):
        files_scanned += 1
        findings.extend(
            scan_file_to_findings(
                path=path,
                rules=rules,
                guard_id=GUARD_ID,
                guard_file=GUARD_FILE,
                contract_schema_version=CONTRACT_SCHEMA_VERSION,
                skip_safe_context=True,
            )
        )

    return files_scanned, findings


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

    title = f"{GUARD_ID} / {GUARD_NAME} v{VERSION}"
    mode = args.mode
    fail_on = Severity.HARD

    print(f"Files scanned: {files_scanned}")
    print_text_report(findings, title=title, mode=mode, fail_on=fail_on, root=root)

    if args.json_out:
        try:
            write_json(Path(args.json_out), findings)
        except OSError as exc:
            print(f"ERROR: cannot write JSON report: {exc}", file=sys.stderr)
            return 2

    if args.mode == "strict":
        return exit_code_for(findings, fail_on=fail_on)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
    
