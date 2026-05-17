#!/usr/bin/env python3
"""
VECTAETOS :: GUARD-01 CANONICAL ONTOLOGY MODIFICATION GUARD

Purpose:
    Mechanically protect canonical ontology files and core semantic invariants
    from silent mutation in repository changes.

Status:
    Fundamental repository perimeter guard.

Scope:
    L1 mechanized repository enforcement only.

This guard:
    - reads git diff
    - detects protected file modifications
    - detects high-risk semantic drift phrases
    - explicitly recognizes anchors/SEMANTIC_ERRATA.md as a narrow errata registry
    - emits deterministic CI errors
    - exits non-zero on violation

This guard does NOT:
    - redefine Φ
    - evaluate truth
    - optimize anything
    - decide for humans
    - validate deployment
    - claim empirical safety

Python:
    3.11+
Dependencies:
    standard library only
"""

from __future__ import annotations

import argparse
import dataclasses
import enum
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


NULL_SHA = "0000000000000000000000000000000000000000"

ERRATA_REGISTRY_PATH = "anchors/SEMANTIC_ERRATA.md"

ERRATA_REQUIRED_MARKERS: tuple[str, ...] = (
    "vectaetos-guard: allow-file",
    "KANONICKÝ SEMANTIC ERRATA ANCHOR",
    "Tento dokument nie je nová ontológia",
    "Nie je náhrada immutable anchorov",
    "Nemení Φ, K(Φ), κ, QE, Vortex, audit, projekciu",
    "guardy môžu registrovaný historický drift chápať ako známe errata",
    "neregistrovaný drift zostáva porušením",
    "Aktívne súbory sa majú opraviť priamo",
)


class Severity(str, enum.Enum):
    BLOCK = "BLOCK"
    FAIL = "FAIL"
    WARN = "WARN"


@dataclasses.dataclass(frozen=True)
class Finding:
    severity: Severity
    code: str
    path: str
    message: str
    line: int | None = None


@dataclasses.dataclass(frozen=True)
class ChangedPath:
    status: str
    paths: tuple[str, ...]


PROTECTED_PREFIXES: tuple[str, ...] = (
    "anchors/",
    "formal/",
)

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
        r"(^|/)FORMÁLNE_.*\.md$",
        r"(^|/)CANONICAL.*ANCHOR.*\.md$",
        r"(^|/)KANONICK.*KOTV.*\.md$",
        r"(^|/)MECHANIZATION_OF_.*\.md$",
        r"(^|/)MECHANIZÁCIA_.*\.md$",
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
        r"(^|/)epistemický_priestor\.md$",
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
)

FORBIDDEN_SEMANTIC_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = tuple(
    (code, re.compile(pattern, re.IGNORECASE), message)
    for code, pattern, message in (
        (
            "PHI_AGENT",
            r"\b(Φ|Phi|PHI)\b.{0,80}\b(agent|planner|controller|decision[- ]?maker|rozhoduje|koná|plánuje|riadi)\b",
            "Φ nesmie byť formulované ako agent, plánovač, controller alebo rozhodovací subjekt.",
        ),
        (
            "PHI_OPTIMIZATION",
            r"\b(Φ|Phi|PHI)\b.{0,80}\b(optimiz|optimaliz|reward|cieľ|goal|target)\b",
            "Φ nesmie byť formulované ako optimalizačný alebo cieľový mechanizmus.",
        ),
        (
            "K_SCORE",
            r"\bK\s*\(\s*Φ\s*\).{0,80}\b(score|skóre|metric|metrika|reward|target|cieľ|optimaliz)\b",
            "K(Φ) nesmie byť formulované ako skóre, metrika, reward alebo optimalizačný cieľ.",
        ),
        (
            "KAPPA_PARAMETER",
            r"\b(κ|kappa)\b.{0,80}\b(parameter|param|threshold|prahov[áaý]? hodnota|číslo|number|metric|metrika|tunable|nastaviteľ)\b",
            "κ nesmie byť formulované ako nastaviteľný parameter, číslo alebo metrika.",
        ),
        (
            "QE_ERROR",
            r"\b(QE|Qualitative Epistemic Aporia)\b.{0,80}\b(error|bug|chyba|fallback|exception|failure|zlyhanie)\b",
            "QE nesmie byť formulované ako obyčajná chyba, fallback alebo zlyhanie.",
        ),
        (
            "AUDIT_COMMAND",
            r"\b(audit|EK|Epistemic Cryptography)\b.{0,80}\b(commands?|controls?|riadi|blokuje|decides?|rozhoduje|intervenes?|zasahuje)\b",
            "Audit/EK nesmie byť formulovaný ako command/control/intervention layer.",
        ),
        (
            "PROJECTION_INTERPRETS",
            r"\b(projection|projekcia|runes?|runy|glyph|TetraGlyph)\b.{0,80}\b(interprets?|interpretuje|decides?|rozhoduje|prescribes?|predpisuje)\b",
            "Projekcia/runy/glyphy nesmú byť formulované ako interpretujúce alebo preskriptívne.",
        ),
        (
            "LLM_AUTHORITY",
            r"\b(LLM|language model|jazykový model)\b.{0,80}\b(authority|autorita|truth|pravda|decides?|rozhoduje|validates?|validuje)\b",
            "LLM nesmie byť formulované ako pravdová, rozhodovacia alebo validačná autorita.",
        ),
        (
            "VORTEX_SELECTS_BEST",
            r"\b(Vortex|Simulačný Vortex|Simulation Vortex)\b.{0,100}\b(selects?|chooses?|vyberá|zvolí|best|najlepš|optimizes?|optimaliz)\b",
            "Vortex nesmie byť formulovaný ako výberca najlepšej trajektórie alebo optimalizátor.",
        ),
        (
            "MEMORY_REWRITES_ONTOLOGY",
            r"\b(memory|pamäť|ESM|LTL|MML)\b.{0,100}\b(rewrites?|modifies?|mení|prepisuje|updates? ontology|učí Φ|trains? Φ)\b",
            "Pamäťové vrstvy nesmú meniť ontológiu, Φ ani Vortex.",
        ),
        (
            "L4_OVERCLAIM",
            r"\b(safe|bezpečn[ýáé]|validated|validovan[ýáé]|deployment[- ]?ready|legitimate|legitímn[yea])\b.{0,120}\b(without L4|bez L4|bez empirick|L0|L1|L2|L3)\b",
            "Bez L4 sa nesmie claimovať bezpečnosť, deployment legitimita ani plná validácia.",
        ),
    )
)


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
            f"git {' '.join(args)} failed with exit {result.returncode}:\n{result.stderr}"
        )

    return result.stdout


def normalize_path(path: str) -> str:
    return path.strip().replace("\\", "/")


def is_null_sha(value: str | None) -> bool:
    return value is None or value.strip() == "" or value.strip() == NULL_SHA


def is_errata_registry_path(path: str) -> bool:
    return normalize_path(path) == ERRATA_REGISTRY_PATH


def content_contains_required_errata_markers(content: str) -> bool:
    normalized = content.lower()
    return all(marker.lower() in normalized for marker in ERRATA_REQUIRED_MARKERS)


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


def diff_name_status(base: str, head: str) -> list[ChangedPath]:
    if is_null_sha(head):
        head = "HEAD"

    if is_null_sha(base):
        base_ref = empty_tree_hash()
    else:
        base_ref = base

    if not commit_exists(head) and head != "HEAD":
        raise RuntimeError(f"Head commit is not available in checkout: {head}")

    if base_ref != empty_tree_hash() and not commit_exists(base_ref):
        raise RuntimeError(f"Base commit is not available in checkout: {base_ref}")

    raw = run_git(
        [
            "diff",
            "--name-status",
            "-M",
            "--find-renames",
            base_ref,
            head,
            "--",
        ]
    )

    changes: list[ChangedPath] = []

    for line in raw.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith("R") or status.startswith("C"):
            if len(parts) >= 3:
                changes.append(
                    ChangedPath(
                        status=status,
                        paths=(normalize_path(parts[1]), normalize_path(parts[2])),
                    )
                )
        elif len(parts) >= 2:
            changes.append(
                ChangedPath(
                    status=status,
                    paths=(normalize_path(parts[1]),),
                )
            )

    return changes


def path_is_protected(path: str) -> bool:
    path = normalize_path(path)

    if path in SELF_PROTECTED_PATHS:
        return True

    if path.startswith(PROTECTED_PREFIXES):
        return True

    return any(pattern.search(path) for pattern in PROTECTED_PATH_PATTERNS)


def path_should_be_semantically_scanned(path: str) -> bool:
    path = normalize_path(path)

    if path.startswith(SCAN_EXCLUDED_PREFIXES):
        return False

    return Path(path).suffix.lower() in SCAN_EXTENSIONS


def file_exists_at_head(path: str, head: str) -> bool:
    if is_null_sha(head):
        head = "HEAD"

    result = subprocess.run(
        ["git", "cat-file", "-e", f"{head}:{path}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def read_file_at_head(path: str, head: str) -> str:
    if is_null_sha(head):
        head = "HEAD"

    return run_git(["show", f"{head}:{path}"], allow_fail=False)


def validate_errata_registry_at_head(path: str, head: str) -> list[Finding]:
    if not is_errata_registry_path(path):
        return []

    if not file_exists_at_head(path, head):
        return [
            Finding(
                severity=Severity.BLOCK,
                code="SEMANTIC_ERRATA_REGISTRY_MISSING",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md is a registered semantic errata "
                    "anchor and must not be deleted or moved away from anchors/."
                ),
            )
        ]

    try:
        content = read_file_at_head(path, head)
    except RuntimeError as exc:
        return [
            Finding(
                severity=Severity.BLOCK,
                code="SEMANTIC_ERRATA_REGISTRY_UNREADABLE",
                path=path,
                message=f"Cannot read semantic errata registry at HEAD: {exc}",
            )
        ]

    if not content_contains_required_errata_markers(content):
        return [
            Finding(
                severity=Severity.BLOCK,
                code="SEMANTIC_ERRATA_REGISTRY_INVALID",
                path=path,
                message=(
                    "anchors/SEMANTIC_ERRATA.md may contain forbidden historical "
                    "phrases only if it preserves explicit errata registry clauses."
                ),
            )
        ]

    return []


def semantic_scan_is_exempt(path: str, content: str) -> bool:
    if not is_errata_registry_path(path):
        return False

    return content_contains_required_errata_markers(content)


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
                    Finding(
                        severity=Severity.BLOCK,
                        code="CANONICAL_FILE_MUTATION",
                        path=path,
                        message=(
                            f"Protected canonical/perimeter path changed "
                            f"(git status {change.status})."
                        ),
                    )
                )

    return findings


def detect_semantic_drift(changes: Iterable[ChangedPath], head: str) -> list[Finding]:
    findings: list[Finding] = []
    unique_paths = sorted({path for change in changes for path in change.paths})

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

        for line_number, line in enumerate(content.splitlines(), start=1):
            for code, pattern, message in FORBIDDEN_SEMANTIC_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            severity=Severity.FAIL,
                            code=code,
                            path=path,
                            line=line_number,
                            message=message,
                        )
                    )

    return findings


def emit_github_annotation(finding: Finding) -> None:
    safe_message = finding.message.replace("\n", " ").replace("%", "%25")
    safe_message = safe_message.replace("\r", "%0D").replace("\n", "%0A")
    safe_path = finding.path.replace("\n", "")

    if finding.line is not None:
        print(
            f"::error file={safe_path},line={finding.line},title={finding.code}::{safe_message}"
        )
    else:
        print(f"::error file={safe_path},title={finding.code}::{safe_message}")


def print_report(findings: list[Finding], changes: list[ChangedPath]) -> None:
    print("")
    print("================================================================")
    print("VECTAETOS :: GUARD-01 CANONICAL ONTOLOGY MODIFICATION GUARD")
    print("================================================================")
    print(f"Changed entries scanned: {len(changes)}")
    print(f"Findings: {len(findings)}")
    print("")

    if not findings:
        print("PASS: Zachovaná integrita kanonickej ontológie.")
        print("Scope: L1 repository perimeter only.")
        print("================================================================")
        return

    for finding in findings:
        location = finding.path

        if finding.line is not None:
            location = f"{location}:{finding.line}"

        print(f"[{finding.severity.value}] {finding.code}")
        print(f"  path: {location}")
        print(f"  msg : {finding.message}")
        print("")

    print("FAIL: Zistený zásah do chránenej ontologickej/perimeter vrstvy.")
    print("")
    print("Tento guard nemení Φ, K(Φ), κ, QE, Vortex, audit ani projekciu.")
    print("Iba mechanicky blokuje drift v repozitári.")
    print("================================================================")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS canonical ontology repository guard"
    )

    parser.add_argument("--base", required=True, help="Base commit SHA or null SHA")
    parser.add_argument("--head", required=True, help="Head commit SHA")
    parser.add_argument(
        "--mode",
        choices=("strict", "report"),
        default="strict",
        help="strict exits non-zero on findings; report only prints findings",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    base = args.base.strip()
    head = args.head.strip() or "HEAD"

    try:
        changes = diff_name_status(base, head)
        findings: list[Finding] = []

        findings.extend(detect_protected_file_changes(changes, head))
        findings.extend(detect_semantic_drift(changes, head))

        for finding in findings:
            emit_github_annotation(finding)

        print_report(findings, changes)

        if findings and args.mode == "strict":
            return 1

        return 0

    except Exception as exc:
        print("::error title=GUARD_RUNTIME_ERROR::Canonical ontology guard failed internally.")
        print("")
        print("GUARD_RUNTIME_ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: guard runtime error blocks the check.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
