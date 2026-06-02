#!/usr/bin/env python3
"""
VECTAETOS :: EK Observable Non-Authority Guard
GUARD-13 / v0.1.1

Role:
    Deterministic semantic guard for Epistemic Cryptography observable drift.

Detects claims that:
    - h_topo / EK observables are scores, metrics, truth, safety, deployment validity, K(Phi), or kappa.
    - hash / fingerprint / ledger prove truth, safety, ontology, or deployment validity.
    - EK / audit / ledger / hash / fingerprint control, decide, optimize, or act as an agent.
    - audit / EK / ledger / hash / fingerprint mutate Phi or write back into Phi.
    - Phi is a mutable runtime state.

Correct reading:
    h_topo = observable, not score.
    ledger = provenance, not truth.
    hash = integrity, not ontological verdict.
    EK = audit layer, not control layer.
    Phi = untouchable field, not runtime state.

Modes:
    report = print findings and exit 0
    strict = exit 1 on HARD findings
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
from pathlib import Path
from typing import Iterable

VERSION = "0.1.1"

DEFAULT_INCLUDE_SUFFIXES = {
    ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".toml",
    ".html", ".css", ".js", ".ts",
}

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", "node_modules", "dist", "build",
    "archive", ".runtime",
}

EXCLUDED_PATH_PARTS = {
    ("audit",),
}

EXCLUDED_FILES = {
    "guards/ek_observable_non_authority_guard.py",
    "tests/test_guard13_ek_observable_non_authority.py",
}

ALLOW_MARKERS = {
    "vectaetos-ek-observable-allow",
    "vectaetos-guard: allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-ek-observable-allow-file",
    "vectaetos-guard: allow-file",
}

# Line-local only. Do not use a wide previous-context window: it can hide drift
# immediately after a correct sentence such as "h_topo is not a score".
LINE_META_OR_NEGATION_PATTERN = re.compile(
    r"("
    r"must not|should not|do not|does not|is not|are not|never|without|"
    r"forbidden|prohibited|ban|banned|disallowed|invalid|failure condition|"
    r"fails if|no claim|not claim|does not claim|not a score|not score|"
    r"not truth|not authority|not control|not command|not proof|not verdict|not ontological verdict|not a control layer|not control layer|"
    r"correct reading|forbidden reading|drift guard|semantic guard|guard|detects|"
    r"forbidden pattern|forbidden claim|example failure|compatibility test|"
    r"nesmie|nesmú|nesmu|nie je|nie sú|nie su|bez|zakázané|zakazane|zákaz|zakaz|"
    r"nie je skóre|nie je skore|nie je pravda|nie je autorita|nie je dôkaz|nie je dokaz|"
    r"správne čítanie|spravne citanie|zakázané čítanie|zakazane citanie"
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


def compile_rule(code: str, severity: str, pattern: str, reason: str, safer_form: str) -> Rule:
    return Rule(
        code=code,
        severity=severity,
        pattern=re.compile(pattern, re.IGNORECASE | re.UNICODE),
        reason=reason,
        safer_form=safer_form,
    )


OBSERVABLES = (
    r"h_topo|h[-_\s]?topo|H_topo|C_EK|T_EK|A_EK|mu|μ|mu_total|"
    r"EK observable|EK observables|audit observable|audit observables|"
    r"topological humility|topologická pokora|topologicka pokora"
)

INTEGRITY_ARTIFACTS = (
    r"hash|fingerprint|sha-?256|sha3-?512|merkle|ledger|jsonl|"
    r"odtlačok|odtlacok|provenance"
)

EK_SUBJECTS = (
    r"EK|Epistemic Cryptography|epistemická kryptografia|epistemicka kryptografia|"
    r"audit|audit layer|auditná vrstva|auditna vrstva|ledger|hash|fingerprint"
)

FIELD_SUBJECTS = r"Phi|Φ|field|pole"

AUTHORITY_TERMS = (
    r"truth|true state|ontological truth|pravda|pravdivý stav|pravdivy stav|"
    r"proof|proves|prove|dokazuje|dôkaz|dokaz|verdict|gives verdict|verdikt|"
    r"authority|authoritative|autorita|autoritatívny|autoritarivny|"
    r"validity|validita|validates|validate|validuje|validation|validácia|validacia|"
    r"safety|bezpečnosť|bezpecnost|safe|bezpečný|bezpecny|"
    r"deployment|nasadenie|operative admissibility|operačná prípustnosť|operacna pripustnost"
)

CONTROL_TERMS = (
    r"control layer|command layer|runtime controller|controller|control signal|"
    r"riadiaca vrstva|kontrolná vrstva|kontrolna vrstva|príkazová vrstva|prikazova vrstva|"
    r"riadi|kontroluje|commands|blocks|blokuje|decides|decide|rozhoduje|"
    r"selects trajectories|selects trajectory|vyberá trajektórie|vybera trajektorie|"
    r"optimizes|optimize|optimalizuje|optimizer|optimalizér|optimalizer|"
    r"agent|AI agent|agentic|agentný|agentny"
)

SCORE_TERMS = (
    r"score|scoring|rank|ranking|rating|metric|threshold|parameter|"
    r"skóre|skore|hodnotenie|rebríček|rebricek|metrika|prah|parameter|"
    r"coherence score|coherence_score|safety score|validity score|deployment metric|"
    r"bezpečnostné skóre|bezpecnostne skore|skóre koherencie|skore koherencie|"
    r"metrika bezpečnosti|metrika bezpecnosti|metrika deploymentu"
)

KAPPA_K_TERMS = (
    r"K\(Φ\)|K\(Phi\)|K_phi|KPhi|K\(\\Phi\)|kappa|κ|\\kappa|"
    r"coherence predicate|koherenčný predikát|koherencny predikat"
)

MUTATION_VERBS = (
    r"changes|change|updates|update|mutates|mutate|modifies|modify|"
    r"writes back|write back|writes to|write to|affects|affect|"
    r"controls|control|feeds back|feedback into|"
    r"mení|meni|zmení|zmeni|aktualizuje|mutuje|modifikuje|"
    r"zapisuje|píše späť|pise spat|ovplyvňuje|ovplyvnuje|kontroluje|riadi"
)

MUTABLE_STATE_TERMS = (
    r"runtime state|mutable runtime state|mutable state|"
    r"runtime stav|meniteľný runtime stav|menitelny runtime stav|mutovateľný stav|mutovatelny stav"
)

RULES: list[Rule] = [
    compile_rule(
        "OBSERVABLE_AS_AUTHORITY", "HARD",
        rf"\b({OBSERVABLES})\b.{{0,180}}\b({AUTHORITY_TERMS})\b",
        "EK observables must not be framed as truth, safety, deployment, validity, proof, verdict, or authority.",
        "Use: h_topo / C_EK / T_EK / mu are structural audit observables only.",
    ),
    compile_rule(
        "AUTHORITY_AS_OBSERVABLE", "HARD",
        rf"\b({AUTHORITY_TERMS})\b.{{0,180}}\b({OBSERVABLES})\b",
        "Truth/safety/deployment/validity vocabulary must not attach to EK observables.",
        "Use: observable / trace / structural marker; never authority, proof, or verdict.",
    ),
    compile_rule(
        "OBSERVABLE_AS_CONTROL_OR_AGENT", "HARD",
        rf"\b({OBSERVABLES})\b.{{0,180}}\b({CONTROL_TERMS})\b",
        "EK observables must not be framed as control, decision, optimization, command, or agency.",
        "Use: external audit observable only; no control and no trajectory selection.",
    ),
    compile_rule(
        "CONTROL_OR_AGENT_AS_OBSERVABLE", "HARD",
        rf"\b({CONTROL_TERMS})\b.{{0,180}}\b({OBSERVABLES})\b",
        "Control/agent vocabulary near EK observables collapses audit into intervention.",
        "Use: non-interventional audit trace; no command, no decision, no optimization.",
    ),
    compile_rule(
        "OBSERVABLE_AS_SCORE", "HARD",
        rf"\b({OBSERVABLES})\b.{{0,180}}\b({SCORE_TERMS})\b",
        "EK observables must not be framed as scores, ranks, thresholds, metrics, or parameters.",
        "Use: h_topo / C_EK / T_EK / mu are structural audit observables only.",
    ),
    compile_rule(
        "SCORE_AS_OBSERVABLE_AUTHORITY", "HARD",
        rf"\b({SCORE_TERMS})\b.{{0,180}}\b({OBSERVABLES})\b",
        "Scoring vocabulary near EK observables risks turning audit traces into authority.",
        "Use: observable / trace / structural marker; never score, rank, threshold, or metric for authority.",
    ),
    compile_rule(
        "OBSERVABLE_AS_K_OR_KAPPA", "HARD",
        rf"\b({OBSERVABLES})\b.{{0,180}}\b({KAPPA_K_TERMS})\b",
        "No EK observable may be treated as K(Phi), kappa, or a proxy for either.",
        "Use: audit observable only; K(Phi) and kappa remain ontological notions outside EK.",
    ),
    compile_rule(
        "K_OR_KAPPA_AS_OBSERVABLE", "HARD",
        rf"\b({KAPPA_K_TERMS})\b.{{0,180}}\b({OBSERVABLES})\b",
        "K(Phi)/kappa vocabulary must not collapse into numeric EK observables.",
        "Use: K(Phi) as predicate and kappa as boundary; EK values remain external traces.",
    ),
    compile_rule(
        "INTEGRITY_ARTIFACT_AS_TRUTH_OR_VALIDITY", "HARD",
        rf"\b({INTEGRITY_ARTIFACTS})\b.{{0,180}}\b({AUTHORITY_TERMS})\b",
        "Hashes, fingerprints, ledgers, and provenance records show integrity, not truth or validity.",
        "Use: hash = integrity; ledger = provenance; neither is ontological verdict.",
    ),
    compile_rule(
        "AUTHORITY_AS_INTEGRITY_ARTIFACT", "HARD",
        rf"\b({AUTHORITY_TERMS})\b.{{0,180}}\b({INTEGRITY_ARTIFACTS})\b",
        "Truth/safety/deployment language must not be grounded in hashes or ledgers.",
        "Use: integrity/provenance only; do not claim truth, safety, or deployment validity from artifacts.",
    ),
    compile_rule(
        "EK_AS_CONTROL_OR_AGENT", "HARD",
        rf"\b({EK_SUBJECTS})\b.{{0,180}}\b({CONTROL_TERMS})\b",
        "EK/audit must not be framed as control, command, blocking, decision, optimization, or agency.",
        "Use: EK observes, records, fingerprints, and exposes traces without intervention.",
    ),
    compile_rule(
        "CONTROL_OR_AGENT_AS_EK", "HARD",
        rf"\b({CONTROL_TERMS})\b.{{0,180}}\b({EK_SUBJECTS})\b",
        "Control/agent vocabulary near EK/audit collapses audit into intervention.",
        "Use: non-interventional audit layer; no command, no decision, no optimization.",
    ),
    compile_rule(
        "AUDIT_ARTIFACT_MUTATES_PHI", "HARD",
        rf"\b({EK_SUBJECTS}|{INTEGRITY_ARTIFACTS})\b.{{0,120}}\b({MUTATION_VERBS})\b.{{0,120}}\b({FIELD_SUBJECTS})\b",
        "Audit/EK/ledger/hash/fingerprint must not be described as changing, updating, controlling, or writing back into Phi.",
        "Use: audit records external traces only; ∂Phi/∂Audit = 0.",
    ),
    compile_rule(
        "PHI_MUTATED_BY_AUDIT_ARTIFACT", "HARD",
        rf"\b({FIELD_SUBJECTS})\b.{{0,120}}\b({MUTATION_VERBS})\b.{{0,120}}\b({EK_SUBJECTS}|{INTEGRITY_ARTIFACTS})\b",
        "Phi must not be framed as affected by audit/EK/ledger/hash/fingerprint.",
        "Use: Phi is untouchable; audit has no write-back.",
    ),
    compile_rule(
        "PHI_AS_MUTABLE_RUNTIME_STATE", "HARD",
        rf"\b({FIELD_SUBJECTS})\b.{{0,180}}\b({MUTABLE_STATE_TERMS})\b",
        "Phi must not be framed as mutable runtime state.",
        "Use: Phi is an untouchable field, not runtime state.",
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


def is_line_meta_or_negated(line: str) -> bool:
    return "≠" in line or bool(LINE_META_OR_NEGATION_PATTERN.search(line))


def scan_file(path: Path, root: Path) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []
    if file_has_allow_marker(text):
        return []

    findings: list[Finding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if has_allow_marker(stripped):
            continue
        if is_line_meta_or_negated(stripped):
            continue

        for rule in RULES:
            if rule.pattern.search(stripped):
                findings.append(Finding(path=path, line_no=idx, line=stripped, rule=rule))

    return findings


def print_findings(findings: list[Finding], root: Path) -> None:
    hard_count = sum(1 for finding in findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in findings if finding.rule.severity == "WARN")

    print(f"VECTAETOS EK Observable Non-Authority Guard v{VERSION}")
    print("======================================================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no EK observable authority drift detected.")
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
        description="Detect VECTAETOS EK observable / audit authority drift."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=("report", "strict"), default="report")
    parser.add_argument("--warnings-as-errors", action="store_true")
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
