#!/usr/bin/env python3
"""
VECTAETOS :: GUARD-01 CANONICAL ONTOLOGY MODIFICATION GUARD

Role:
    Fundamental repository perimeter guard for canonical ontology boundaries.

Purpose:
    Mechanically protect canonical ontology files and core semantic invariants
    from silent mutation in repository changes.

This guard:
    - reads git diff between base/head
    - detects protected canonical/perimeter path mutations
    - validates the semantic errata registry exception
    - scans changed active text files for high-risk ontology drift
    - emits shared Finding objects
    - prints deterministic shared reports
    - optionally writes JSON report artifacts
    - fails closed on infrastructure errors

This guard does NOT:
    - redefine Î¦
    - evaluate truth
    - optimize anything
    - decide for humans
    - validate deployment
    - claim empirical safety
    - mutate repository files
    - create feedback into Î¦

Python:
    3.11+

Dependencies:
    standard library + guards/core shared kernel
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from collections.abc import Iterable

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
        make_finding,
    )
    from guards.core.perimeter import EnforcementMode
    from guards.core.reporting import exit_code_for, print_text_report, write_json
    from guards.core.text_scan import make_rule, scan_text_to_findings
except ModuleNotFoundError:
    from core.findings import (  # type: ignore
        Confidence,
        DriftVector,
        EvidenceClass,
        Finding,
        IntegrityPosture,
        PerimeterLevel,
        PerimeterScope,
        Severity,
        make_finding,
    )
    from core.perimeter import EnforcementMode  # type: ignore
    from core.reporting import exit_code_for, print_text_report, write_json  # type: ignore
    from core.text_scan import make_rule, scan_text_to_findings  # type: ignore


GUARD_ID = "GUARD-01"
GUARD_FILE = "guards/canonical_ontology_guard.py"
GUARD_NAME = "VECTAETOS Canonical Ontology Boundary"
VERSION = "0.2.0-core-refactor"
CONTRACT_SCHEMA_VERSION = "1.0"

NULL_SHA = "0000000000000000000000000000000000000000"
ERRATA_REGISTRY_PATH = "anchors/SEMANTIC_ERRATA.md"

ERRATA_REQUIRED_MARKERS: tuple[str, ...] = (
    "vectaetos-guard: allow-file",
    "KANONICKĂť SEMANTIC ERRATA ANCHOR",
    "Tento dokument nie je novĂˇ ontolĂłgia",
    "Nie je nĂˇhrada immutable anchorov",
    "NemenĂ­ Î¦, K(Î¦), Îş, QE, Vortex, audit, projekciu",
    "guardy mĂ´Ĺľu registrovanĂ˝ historickĂ˝ drift chĂˇpaĹĄ ako znĂˇme errata",
    "neregistrovanĂ˝ drift zostĂˇva poruĹˇenĂ­m",
    "AktĂ­vne sĂşbory sa majĂş opraviĹĄ priamo",
)

PROTECTED_PREFIXES: tuple[str, ...] = ("anchors/", "formal/")

SELF_PROTECTED_PATHS: tuple[str, ...] = (
    ".github/workflows/canonical-ontology-guard.yml",
    "guards/canonical_ontology_guard.py",
)

PROTECTED_PATH_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|/)MASTER_INDEX\.md$",
        r"(^|/)VECTAETOS_Specification\.md$",
        r"(^|/)VECTAETOS_v1\.0_Frozen_Ontological_Core\.md$",
        r"(^|/)VECTAETOS.*Formal.*\.md$",
        r"(^|/)FORMALISM.*\.md$",
        r"(^|/)FORMAL_.*\.md$",
        r"(^|/)FORMĂLNE_.*\.md$",
        r"(^|/)CANONICAL.*ANCHOR.*\.md$",
        r"(^|/)KANONICK.*KOTV.*\.md$",
        r"(^|/)MECHANIZATION_OF_.*\.md$",
        r"(^|/)MECHANIZĂCIA_.*\.md$",
        r"(^|/)EPISTEMIC_TOPOLOGY.*\.md$",
        r"(^|/)EPISTEMIC_LAYER.*\.md$",
        r"(^|/)EPISTEMIC_CRYPTOGRAPHY.*\.md$",
        r"(^|/)ENTROPIC_HUMILITY.*\.md$",
        r"(^|/)INTRINSIC_HUMILITY.*\.md$",
        r"(^|/)PROJECTION_RUNES.*\.md$",
        r"(^|/)TRIADIC_ARCHITECTURE.*\.md$",
        r"(^|/)OAAT.*\.md$",
        r"(^|/)EMPIRICAL_EVIDENCE_ROADMAP.*\.md$",
        r"(^|/)EMPIRICAL_SAFETY_PRIOR.*\.md$",
        r"(^|/)epistemic_space\.md$",
        r"(^|/)epistemickĂ˝_priestor\.md$",
    )
)

SCAN_EXTENSIONS: tuple[str, ...] = (
    ".md",
    ".txt",
    ".html",
    ".py",
    ".yml",
    ".yaml",
    ".json",
)

SCAN_EXCLUDED_PREFIXES: tuple[str, ...] = (
    "guards/",
    ".github/",
    "archive/",
    "docs/archive/",
    "tests/fixtures/",
    "research/guards/",
)


def normalize_path(path: str | Path) -> str:
    value = str(path).strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def is_null_sha(value: str | None) -> bool:
    return value is None or value.strip() == "" or value.strip() == NULL_SHA


def is_errata_registry_path(path: str | Path) -> bool:
    return normalize_path(path) == ERRATA_REGISTRY_PATH


def content_contains_required_errata_markers(content: str) -> bool:
    normalized = content.casefold()
    return all(marker.casefold() in normalized for marker in ERRATA_REQUIRED_MARKERS)


def run_git(args: list[str], *, allow_fail: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(
            f"git {' '.join(args)} failed with exit {result.returncode}:\n"
            f"{result.stderr}"
        )
    return result.stdout


def commit_exists(ref: str) -> bool:
    if is_null_sha(ref):
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def empty_tree_hash() -> str:
    return run_git(["hash-object", "-t", "tree", "/dev/null"]).strip()


def file_exists_at_head(path: str, head: str) -> bool:
    selected_head = "HEAD" if is_null_sha(head) else head
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{selected_head}:{path}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def read_file_at_head(path: str, head: str) -> str:
    selected_head = "HEAD" if is_null_sha(head) else head
    return run_git(["show", f"{selected_head}:{path}"], allow_fail=False)


class ChangedPath:
    __slots__ = ("status", "paths")

    def __init__(self, status: str, paths: tuple[str, ...]) -> None:
        self.status = status
        self.paths = paths


def diff_name_status(base: str, head: str) -> list[ChangedPath]:
    selected_head = "HEAD" if is_null_sha(head) else head
    selected_base = empty_tree_hash() if is_null_sha(base) else base

    if selected_head != "HEAD" and not commit_exists(selected_head):
        raise RuntimeError(f"Head commit is not available in checkout: {selected_head}")

    if selected_base != empty_tree_hash() and not commit_exists(selected_base):
        raise RuntimeError(f"Base commit is not available in checkout: {selected_base}")

    raw = run_git(
        [
            "diff",
            "--name-status",
            "-M",
            "--find-renames",
            selected_base,
            selected_head,
            "--",
        ]
    )

    changes: list[ChangedPath] = []
    for line in raw.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith(("R", "C")):
            if len(parts) >= 3:
                changes.append(
                    ChangedPath(
                        status=status,
                        paths=(normalize_path(parts[1]), normalize_path(parts[2])),
                    )
                )
        elif len(parts) >= 2:
            changes.append(ChangedPath(status=status, paths=(normalize_path(parts[1]),)))

    return changes


def path_is_protected(path: str | Path) -> bool:
    repo_path = normalize_path(path)
    if repo_path in SELF_PROTECTED_PATHS:
        return True
    if repo_path.startswith(PROTECTED_PREFIXES):
        return True
    return any(pattern.search(repo_path) for pattern in PROTECTED_PATH_PATTERNS)


def path_should_be_semantically_scanned(path: str | Path) -> bool:
    repo_path = normalize_path(path)
    if any(repo_path.startswith(prefix) for prefix in SCAN_EXCLUDED_PREFIXES):
        return False
    return Path(repo_path).suffix.lower() in SCAN_EXTENSIONS


def ontology_finding(
    *,
    rule_id: str,
    path: str | Path,
    message: str,
    severity: Severity = Severity.BLOCKER,
    confidence: Confidence = Confidence.HIGH,
    line: int | None = None,
    observed_pattern: str | None = None,
    protected_object: str | None = None,
    vector: DriftVector = DriftVector.V14_ANCHOR_INTEGRITY_DRIFT,
    forbidden_conversion: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    return make_finding(
        guard_id=GUARD_ID,
        guard_file=GUARD_FILE,
        rule_id=rule_id,
        contract_schema_version=CONTRACT_SCHEMA_VERSION,
        level=PerimeterLevel.LEVEL_0,
        scope=PerimeterScope.FUNDAMENTAL_REPOSITORY,
        vector=vector,
        severity=severity,
        confidence=confidence,
        path=normalize_path(path),
        line=line,
        message=message,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        forbidden_conversion=forbidden_conversion,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.FAIL_CLOSED,
        integrity_posture=IntegrityPosture.IMMUTABLE_ANCHOR,
        anchor_ref="MASTER_INDEX.md",
        contract_ref="contracts/perimeter_manifest.json",
        safer_form=safer_form,
    )


def validate_errata_registry_at_head(path: str, head: str) -> list[Finding]:
    if not is_errata_registry_path(path):
        return []

    if not file_exists_at_head(path, head):
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-MISSING",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md is a registered semantic errata "
                    "anchor and must not be deleted or moved away from anchors/."
                ),
                protected_object="semantic_errata_registry",
                safer_form="Restore anchors/SEMANTIC_ERRATA.md with its required registry markers.",
            )
        ]

    try:
        content = read_file_at_head(path, head)
    except RuntimeError as exc:
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-UNREADABLE",
                path=path,
                message=f"Cannot read semantic errata registry at HEAD: {exc}",
                protected_object="semantic_errata_registry",
            )
        ]

    if not content_contains_required_errata_markers(content):
        return [
            ontology_finding(
                rule_id="SEMANTIC-ERRATA-REGISTRY-INVALID",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md may contain forbidden historical "
                    "phrases only if it preserves explicit errata registry clauses."
                ),
                protected_object="semantic_errata_registry",
                safer_form="Keep errata as registry-only text; do not convert errata into active ontology.",
            )
        ]

    return []


def semantic_scan_is_exempt(path: str, content: str) -> bool:
    return is_errata_registry_path(path) and content_contains_required_errata_markers(content)


def detect_protected_file_changes(
    changes: Iterable[ChangedPath],
    head: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for change in changes:
        for path in change.paths:
            if is_errata_registry_path(path):
                findings.extend(validate_errata_registry_at_head(path, head))
                continue

            if path_is_protected(path):
                findings.append(
                    ontology_finding(
                        rule_id="CANONICAL-FILE-MUTATION",
                        path=path,
                        message=(
                            f"Protected canonical/perimeter path changed "
                            f"(git status {change.status})."
                        ),
                        observed_pattern=f"git_status={change.status}",
                        protected_object="canonical_or_perimeter_path",
                        safer_form=(
                            "Canonical anchors require explicit reviewed process. "
                            "Use versioned extension, errata registry, or controlled anchor update."
                        ),
                    )
                )

    return findings


def join_terms(terms: tuple[str, ...]) -> str:
    return "(?:" + "|".join(re.escape(term) for term in terms) + ")"


def near(left: str, right: str, width: int = 100) -> str:
    return f"(?:{left}.{{0,{width}}}{right}|{right}.{{0,{width}}}{left})"


PHI_TOKEN = r"(?:Î¦|Phi|PHI)"
K_TOKEN = r"(?:K\s*\(\s*Î¦\s*\)|K\s*\(\s*Phi\s*\)|K\s*\(\s*PHI\s*\))"
KAPPA_TOKEN = r"(?:Îş|kappa|\\kappa)"
QE_TOKEN = r"(?:QE|Qualitative Epistemic Aporia)"
AUDIT_TOKEN = r"(?:audit|EK|Epistemic Cryptography)"
PROJECTION_TOKEN = r"(?:projection|projekcia|runes?|runy|glyph|TetraGlyph)"
LLM_TOKEN = r"(?:LLM|language model|jazykovĂ˝ model)"
VORTEX_TOKEN = r"(?:Vortex|SimulaÄŤnĂ˝ Vortex|Simulation Vortex)"
MEMORY_TOKEN = r"(?:memory|pamĂ¤ĹĄ|ESM|LTL|MML)"

PHI_AGENT_TERMS = (
    "agent",
    "planner",
    "controller",
    "decision-maker",
    "decision maker",
    "rozhoduje",
    "konĂˇ",
    "kona",
    "plĂˇnuje",
    "planuje",
    "riadi",
)
PHI_OPTIMIZATION_TERMS = ("optimiz", "optimaliz", "reward", "cieÄľ", "ciel", "goal", "target")
K_SCORE_TERMS = ("score", "skĂłre", "skore", "metric", "metrika", "reward", "target", "cieÄľ", "ciel", "optimaliz")
KAPPA_PARAMETER_TERMS = (
    "parameter",
    "param",
    "threshold",
    "prahovĂˇ hodnota",
    "prahova hodnota",
    "ÄŤĂ­slo",
    "cislo",
    "number",
    "metric",
    "metrika",
    "tunable",
    "nastaviteÄľ",
    "nastavitel",
)
QE_ERROR_TERMS = ("error", "bug", "chyba", "fallback", "exception", "failure", "zlyhanie")
AUDIT_COMMAND_TERMS = (
    "command",
    "commands",
    "control",
    "controls",
    "riadi",
    "blokuje",
    "decides",
    "decide",
    "rozhoduje",
    "intervenes",
    "intervene",
    "zasahuje",
)
PROJECTION_INTERPRETS_TERMS = (
    "interprets",
    "interpret",
    "interpretuje",
    "decides",
    "decide",
    "rozhoduje",
    "prescribes",
    "prescribe",
    "predpisuje",
)
LLM_AUTHORITY_TERMS = (
    "authority",
    "autorita",
    "truth",
    "pravda",
    "decides",
    "decide",
    "rozhoduje",
    "validates",
    "validate",
    "validuje",
)
VORTEX_SELECTS_TERMS = (
    "selects",
    "select",
    "chooses",
    "choose",
    "vyberĂˇ",
    "vybera",
    "zvolĂ­",
    "zvoli",
    "best",
    "najlepĹˇ",
    "optimizes",
    "optimize",
    "optimaliz",
)
MEMORY_REWRITE_TERMS = (
    "rewrites",
    "rewrite",
    "modifies",
    "modify",
    "menĂ­",
    "meni",
    "prepisuje",
    "updates ontology",
    "uÄŤĂ­ Î¦",
    "uci Phi",
    "trains Î¦",
    "trains Phi",
)
L4_OVERCLAIM_LEFT = (
    "safe",
    "bezpeÄŤnĂ˝",
    "bezpeÄŤnĂˇ",
    "bezpeÄŤnĂ©",
    "bezpecny",
    "bezpecna",
    "bezpecne",
    "validated",
    "validovanĂ˝",
    "validovanĂˇ",
    "validovanĂ©",
    "deployment-ready",
    "deployment ready",
    "legitimate",
    "legitĂ­mny",
    "legitĂ­mna",
    "legitimny",
    "legitimna",
)
L4_OVERCLAIM_RIGHT = ("without L4", "bez L4", "bez empirick", "L0", "L1", "L2", "L3")


def build_semantic_rules() -> list:
    common = {
        "level": PerimeterLevel.LEVEL_0,
        "scope": PerimeterScope.FUNDAMENTAL_REPOSITORY,
        "confidence": Confidence.HIGH,
        "evidence_class_allowed": EvidenceClass.E1_STATIC_SCAN,
        "enforcement_mode": EnforcementMode.FAIL_CLOSED,
        "integrity_posture": IntegrityPosture.IMMUTABLE_ANCHOR,
        "anchor_ref": "MASTER_INDEX.md",
        "contract_ref": "contracts/perimeter_manifest.json",
    }

    return [
        make_rule(
            rule_id="PHI-AGENT",
            pattern=near(PHI_TOKEN, join_terms(PHI_AGENT_TERMS), width=80),
            message="Î¦ must not be framed as agent, planner, controller, or decision subject.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Î¦",
            forbidden_conversion="Î¦ -> agent / planner / controller / decision subject",
            safer_form="Use Î¦ only as non-agentic relational epistemic field language.",
            **common,
        ),
        make_rule(
            rule_id="PHI-OPTIMIZATION",
            pattern=near(PHI_TOKEN, join_terms(PHI_OPTIMIZATION_TERMS), width=80),
            message="Î¦ must not be framed as optimization, reward, goal, or target mechanism.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Î¦",
            forbidden_conversion="Î¦ -> optimizer / reward / goal / target",
            safer_form="Use Î¦ as field ontology, not as optimization mechanism.",
            **common,
        ),
        make_rule(
            rule_id="K-SCORE",
            pattern=near(K_TOKEN, join_terms(K_SCORE_TERMS), width=80),
            message="K(Î¦) must not be framed as score, metric, reward, or optimization target.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="K(Î¦)",
            forbidden_conversion="K(Î¦) -> score / metric / reward / target",
            safer_form="Use K(Î¦) as ontological representability predicate.",
            **common,
        ),
        make_rule(
            rule_id="KAPPA-PARAMETER",
            pattern=near(KAPPA_TOKEN, join_terms(KAPPA_PARAMETER_TERMS), width=80),
            message="Îş must not be framed as tunable parameter, number, threshold, or metric.",
            vector=DriftVector.V3_FORBIDDEN_CONVERSION,
            severity=Severity.HARD,
            protected_object="Îş",
            forbidden_conversion="Îş -> parameter / number / threshold / metric",
            safer_form="Use Îş as boundary of ontological preservability / representability.",
            **common,
        ),
        make_rule(
            rule_id="QE-ERROR",
            pattern=near(QE_TOKEN, join_terms(QE_ERROR_TERMS), width=80),
            message="QE must not be framed as ordinary error, fallback, exception, or failure.",
            vector=DriftVector.V9_SILENCE_QE_COERCION,
            severity=Severity.HARD,
            protected_object="QE",
            forbidden_conversion="QE -> error / fallback / exception / failure",
            safer_form="Use QE as active epistemic aporia / non-representability language.",
            **common,
        ),
        make_rule(
            rule_id="AUDIT-COMMAND",
            pattern=near(AUDIT_TOKEN, join_terms(AUDIT_COMMAND_TERMS), width=80),
            message="Audit/EK must not be framed as command, control, decision, or intervention layer.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="audit/EK",
            forbidden_conversion="audit/EK -> command / control / decision / intervention",
            safer_form="Use audit/EK as read-only structural trace / observation layer.",
            **common,
        ),
        make_rule(
            rule_id="PROJECTION-INTERPRETS",
            pattern=near(PROJECTION_TOKEN, join_terms(PROJECTION_INTERPRETS_TERMS), width=80),
            message="Projection/runes/glyphs must not be framed as interpreting, deciding, or prescribing.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="projection",
            forbidden_conversion="projection -> interpretation / prescription / decision",
            safer_form="Use projection as read-only structural exposure.",
            **common,
        ),
        make_rule(
            rule_id="LLM-AUTHORITY",
            pattern=near(LLM_TOKEN, join_terms(LLM_AUTHORITY_TERMS), width=80),
            message="LLM must not be framed as truth, decision, validation, or authority layer.",
            vector=DriftVector.V0_AUTHORITY_INFLATION,
            severity=Severity.HARD,
            protected_object="LLM",
            forbidden_conversion="LLM -> truth authority / decision authority / validator",
            safer_form="Use LLM only as linguistic adapter / renderer.",
            **common,
        ),
        make_rule(
            rule_id="VORTEX-SELECTS-BEST",
            pattern=near(VORTEX_TOKEN, join_terms(VORTEX_SELECTS_TERMS), width=100),
            message="Vortex must not be framed as selector of best trajectory or optimizer.",
            vector=DriftVector.V2_AGENCY_INJECTION,
            severity=Severity.HARD,
            protected_object="Simulation Vortex",
            forbidden_conversion="Vortex -> selector / optimizer / best-path chooser",
            safer_form="Use Vortex only as non-agentic candidate-trajectory exposure layer.",
            **common,
        ),
        make_rule(
            rule_id="MEMORY-REWRITES-ONTOLOGY",
            pattern=near(MEMORY_TOKEN, join_terms(MEMORY_REWRITE_TERMS), width=100),
            message="Memory layers must not be framed as modifying ontology, Î¦, or Vortex.",
            vector=DriftVector.V1_UPWARD_MUTATION,
            severity=Severity.HARD,
            protected_object="memory layers",
            forbidden_conversion="memory -> ontology updater / Î¦ trainer / Vortex modifier",
            safer_form="Use memory layers as descriptive audit/state records only.",
            **common,
        ),
        make_rule(
            rule_id="L4-OVERCLAIM",
            pattern=near(join_terms(L4_OVERCLAIM_LEFT), join_terms(L4_OVERCLAIM_RIGHT), width=120),
            message="Without replicated L4 evidence, safety, deployment legitimacy, or full validation must not be claimed.",
            vector=DriftVector.V4_EVIDENCE_OVERCLAIM,
            severity=Severity.HARD,
            protected_object="empirical evidence posture",
            forbidden_conversion="L0-L3 evidence -> L4 / safety / deployment validity claim",
            safer_form="Say: no configured blocker detected within declared perimeter.",
            **common,
        ),
    ]


def detect_semantic_drift(changes: Iterable[ChangedPath], head: str) -> list[Finding]:
    findings: list[Finding] = []
    unique_paths = sorted({path for change in changes for path in change.paths})
    rules = build_semantic_rules()

    for path in unique_paths:
        if not path_should_be_semantically_scanned(path):
            continue

        if not file_exists_at_head(path, head):
            continue

        try:
            content = read_file_at_head(path, head)
        except RuntimeError:
            continue

        if semantic_scan_is_exempt(path, content):
            continue

        findings.extend(
            scan_text_to_findings(
                path=path,
                text=content,
                rules=rules,
                guard_id=GUARD_ID,
                guard_file=GUARD_FILE,
                contract_schema_version=CONTRACT_SCHEMA_VERSION,
                skip_safe_context=True,
            )
        )

    return findings


def emit_github_annotation(finding: Finding) -> None:
    command = "warning" if finding.severity == Severity.WARN else "error"
    safe_message = finding.message.replace("%", "%25")
    safe_message = safe_message.replace("\r", "%0D").replace("\n", "%0A")
    safe_path = str(finding.path).replace("\n", "")

    if finding.line is not None:
        print(
            f"::{command} file={safe_path},line={finding.line},title={finding.rule_id}::{safe_message}"
        )
    else:
        print(f"::{command} file={safe_path},title={finding.rule_id}::{safe_message}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS canonical ontology repository guard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--base", required=True, help="Base commit SHA or null SHA.")
    parser.add_argument("--head", required=True, help="Head commit SHA.")
    parser.add_argument(
        "--mode",
        choices=("strict", "report"),
        default="strict",
        help="Strict exits non-zero on findings; report only prints findings.",
    )
    parser.add_argument("--json-out", default=None, help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    base = args.base.strip()
    head = args.head.strip() or "HEAD"
    title = f"{GUARD_ID} / {GUARD_NAME} v{VERSION}"
    fail_on = Severity.HARD

    try:
        changes = diff_name_status(base, head)
        findings: list[Finding] = []
        findings.extend(detect_protected_file_changes(changes, head))
        findings.extend(detect_semantic_drift(changes, head))

        for finding in findings:
            emit_github_annotation(finding)

        print(f"Changed entries scanned: {len(changes)}")
        print_text_report(
            findings,
            title=title,
            mode=args.mode,
            fail_on=fail_on,
            root=Path.cwd(),
        )

        if args.json_out:
            try:
                write_json(Path(args.json_out), findings)
            except OSError as exc:
                print(f"ERROR: cannot write JSON report: {exc}", file=sys.stderr)
                return 2

        if args.mode == "strict":
            return exit_code_for(findings, fail_on=fail_on)

        return 0

    except Exception as exc:
        print("::error title=GUARD-RUNTIME-ERROR::Canonical ontology guard failed internally.")
        print("")
        print("GUARD-RUNTIME-ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: guard runtime error blocks the check.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
