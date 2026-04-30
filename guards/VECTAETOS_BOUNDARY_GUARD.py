#!/usr/bin/env python3
"""
VECTAETOS_BOUNDARY_GUARD.py

Version:
    0.3.3

Purpose:
    Static repository perimeter guard for VECTAETOS semantic drift.

Scope:
    - Scans repository text/code/config files.
    - Detects forbidden formulations that attribute agency, optimization,
      decision authority, deployment legitimacy, or truth authority to VECTAETOS.
    - Avoids false positives in negated, forbidden-example, and guard-context lines.
    - Does not modify files.
    - Fails closed in CI on hard violations.

Python:
    3.11+

Run from:
    repository root

Command:
    python3 guards/VECTAETOS_BOUNDARY_GUARD.py

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


VERSION = "0.3.3"

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
    "archive",
}

DEFAULT_EXCLUDED_FILES = {
    "VECTAETOS_BOUNDARY_GUARD.py",
    "patch_semantic_integrity_text.py",
    "verify_semantic_integrity.py",
}

DEFAULT_EXCLUDED_PATH_PARTS = {
    ("docs", "observatory"),
}

ALLOW_MARKERS = {
    "vectaetos-guard: allow",
    "vectaetos-boundary-allow",
}

FILE_ALLOW_MARKERS = {
    "vectaetos-guard: allow-file",
    "vectaetos-boundary-allow-file",
}

META_CONTEXT_PATTERN = re.compile(
    r"("
    r"forbidden|prohibited|ban|banned|disallowed|failure condition|fails if|"
    r"must not|should not|do not|does not|is not|are not|cannot|can't|never|"
    r"no layer may|no mathematical appendix may|not automatically|without|"
    r"zakázané|zakazane|zákaz|zakaz|nesmie|nesmú|nesmu|nemá|nema|nie je|"
    r"nepíš|nepis|bez|neclaimuj|nepredstieraj|"
    r"nie rozhodovací|no decision|no optimization|no feedback|"
    r"refuses|refuse|odmieta|odmietnutie|"
    r"may not|must never|ceases to be|compatibility test|"
    r"forbidden transformation|failure mode|example failure|"
    r"boundary rule|canonical warning|diagnosis|drift|"
    r"framed as|treated as|treat as|treats .* as|"
    r"minimum hard guards|required hard guards|"
    r"invalid patterns|forbidden patterns|forbidden .* patterns|"
    r"detects drift|detect forbidden|detects forbidden|"
    r"not part of|external to|non-authoritative|non-interventional|"
    r"nie je súčasťou|nie je sucastou|nesmie sa stať|nesmie sa stat|"
    r"forbidden vortex language|forbidden vortex code patterns|"
    r"the vortex may not|the attenuator may not|"
    r"no epistemic failure state may trigger|"
    r"may not:|must not:|forbidden:"
    r")",
    re.IGNORECASE | re.UNICODE,
)

NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|never|without|cannot|can't|does not|do not|must not|should not|"
    r"is not|are not|no|none|refuses|refuse|rather than|instead of|"
    r"nie|nikdy|nesmie|nesmú|nesmu|nemá|nema|bez|nie je|žiadny|ziadny|"
    r"žiadna|ziadna|odmieta|nie ako"
    r")\b",
    re.IGNORECASE | re.UNICODE,
)

QUOTE_OR_RULE_CONTEXT_PATTERN = re.compile(
    r"("
    r"^\s*[-*]\s+|"
    r"^\s*\d+\.\s+|"
    r"`[^`]+`|"
    r"\"[^\"]+\"|"
    r"'[^']+'|"
    r"pattern\s*=|"
    r"reason\s*=|"
    r"safer_form\s*=|"
    r"code\s*=|"
    r"rule|guard|violation|finding|"
    r"canonical rule|compatibility|boundary|drift|"
    r"framed as|treated as|treat as|invalid patterns|forbidden patterns|"
    r"forbidden vortex language|forbidden vortex code patterns|"
    r"may not:|must not:|forbidden:|"
    r"must not|may not|does not|is not|"
    r"forbidden state|forbidden condition"
    r")",
    re.IGNORECASE | re.UNICODE,
)

KAPPA_CANONICAL_CONTEXT_PATTERN = re.compile(
    r"("
    r"non-numeric|non numeric|not numeric|not a value|not a number|"
    r"not a parameter|not tunable|not adjustable|not a metric|not a target|"
    r"boundary condition|boundary of|ontological boundary|"
    r"ontological preservability|representability|epistemic realizability|"
    r"not computed|inferred boundary|∂E|"
    r"nečíseln|neciseln|nie je číslo|nie je cislo|"
    r"nie je hodnota|nie je parameter|nie je metrika|nie je cieľ|nie je ciel|"
    r"hranica|hranica ontologickej zachovateľnosti|hranica reprezentovateľnosti"
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
        pattern=r"\bVECTAETOS\b.{0,100}\b(decides|decide|decision authority|decision system|rozhoduje|rozhodne|rozhodovací systém|rozhodovaci system|autorita rozhodovania)\b",
        reason="VECTAETOS must not be framed as a decision-making entity.",
        safer_form="Use: VECTAETOS exposes structure / projects state / describes topology.",
    ),
    compile_rule(
        code="RECOMMENDATION_AUTHORITY",
        severity="HARD",
        pattern=r"\bVECTAETOS\b.{0,100}\b(recommends|recommendation engine|recommendation|odporúča|odporuca|odporúčanie|odporucanie)\b",
        reason="Projection must not be framed as recommendation.",
        safer_form="Use: projection / descriptive output / non-prescriptive exposure.",
    ),
    compile_rule(
        code="OPTIMIZATION_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|Φ|Phi|Vortex)\b.{0,100}\b(optimizes|optimization objective|optimization target|optimalizuje|optimalizačný cieľ|optimalizacny ciel)\b",
        reason="VECTAETOS/Φ/Vortex must not be framed as optimization systems.",
        safer_form="Use: non-optimizing structural evaluation / trajectory generation without ranking.",
    ),
    compile_rule(
        code="K_AS_SCORE",
        severity="HARD",
        pattern=r"\bK\s*\(?\s*Φ?\s*\)?\b.{0,100}\b(score|ranking|reward|target|cieľ|ciel|skóre|skore|odmena)\b",
        reason="K(Φ) is an ontological predicate, not a score/reward/target.",
        safer_form="Use: K(Φ) = ontological coherence predicate.",
    ),
    compile_rule(
        code="KAPPA_AS_PARAMETER",
        severity="HARD",
        pattern=r"\b(κ|kappa)\b.{0,100}\b(parameter|tunable|deployment threshold|runtime parameter|nastaviteľný|nastavitelny|prah deploymentu|runtime parameter)\b",
        reason="κ is not a tunable parameter or deployment threshold.",
        safer_form="Use: κ = non-numeric boundary condition of ontological preservability.",
    ),
    compile_rule(
        code="KAPPA_NUMERIC_OR_TUNABLE_THRESHOLD",
        severity="HARD",
        pattern=(
            r"\b(κ|kappa)\b.{0,140}\b("
            r"numeric|numerical|number|value|computed|tunable|adjustable|calibrated|"
            r"runtime|deployment|parameter|score|metric|číselný|ciselny|číslo|cislo|"
            r"hodnota|vypočítaný|vypocitany|nastaviteľný|nastavitelny|kalibrovaný|"
            r"kalibrovany|skóre|skore|metrika"
            r")\b.{0,80}\b(threshold|prahová hodnota|prah)\b|"
            r"\b(κ|kappa)\b.{0,80}\b(threshold|prahová hodnota|prah)\b.{0,140}\b("
            r"numeric|numerical|number|value|computed|tunable|adjustable|calibrated|"
            r"runtime|deployment|parameter|score|metric|číselný|ciselny|číslo|cislo|"
            r"hodnota|vypočítaný|vypocitany|nastaviteľný|nastavitelny|kalibrovaný|"
            r"kalibrovany|skóre|skore|metrika"
            r")\b"
        ),
        reason="κ must not be framed as a numeric, tunable, runtime, deployment, score, or metric threshold.",
        safer_form="Use: κ = non-numeric boundary condition of ontological preservability / representability.",
    ),
    compile_rule(
        code="KAPPA_THRESHOLD_AMBIGUITY",
        severity="WARN",
        pattern=r"\b(κ|kappa)\b\s*(=|—|-|:)\s*.*\b(threshold|prahová hodnota|prah)\b",
        reason="Threshold language is ambiguous for κ unless explicitly framed as a non-numeric boundary condition.",
        safer_form="Use: κ = non-numeric boundary condition / boundary of ontological preservability.",
    ),
    compile_rule(
        code="QE_AS_ERROR",
        severity="HARD",
        pattern=r"\bQE\b.{0,100}\b(error|ordinary error|bug|exception|chyba|bežná chyba|bezna chyba)\b",
        reason="QE is an active epistemic aporia, not an ordinary error.",
        safer_form="Use: QE = qualitative epistemic aporia / boundary of representability.",
    ),
    compile_rule(
        code="AUDIT_COMMAND_LAYER",
        severity="HARD",
        pattern=r"\b(audit|EK|Epistemic Cryptography)\b.{0,100}\b(commands|controls|decides|velí|veli|rozhoduje|riadi)\b",
        reason="Audit must remain observe/record/hash only.",
        safer_form="Use: audit observes, records, hashes, and never commands.",
    ),
    compile_rule(
        code="AUDIT_BLOCKS",
        severity="WARN",
        pattern=r"\b(audit|EK|Epistemic Cryptography)\b.{0,100}\b(blocks|blokuje)\b",
        reason="Audit should not be framed as a blocking/control layer unless clearly describing external CI guard behavior.",
        safer_form="Use: audit observes, records, hashes; guards may fail CI externally.",
    ),
    compile_rule(
        code="PROJECTION_INTERPRETS",
        severity="HARD",
        pattern=r"\b(projection|projekcia|runa|runy|glyph|TetraGlyph)\b.{0,100}\b(interprets|decides|recommends|interpretuje|rozhoduje|odporúča|odporuca)\b",
        reason="Projection is descriptive and must not interpret or prescribe.",
        safer_form="Use: projection exposes structural state; interpretation remains human/downstream.",
    ),
    compile_rule(
        code="MEMORY_WRITES_ONTOLOGY",
        severity="HARD",
        pattern=r"\b(memory|pamäť|pamat|ESM|LTL|MML)\b.{0,120}\b(updates|changes|modifies|rewrites|mení|meni|prepisuje)\b.{0,60}\b(Φ|Phi|Vortex|K\(Φ\)|kappa|κ)\b",
        reason="Memory may provide controlled continuity, but must not change Φ, Vortex, K(Φ), or κ.",
        safer_form="Use: memory is anchored continuity, not ontological authority.",
    ),
    compile_rule(
        code="ASI_STANDALONE_ROOT",
        severity="HARD",
        pattern=r"\b(ASIMULATOR|ASI_MOD)\b.{0,120}\b(ontological root|standalone root|samostatný root|samostatny root|nezávislý root|nezavisly root)\b",
        reason="ASIMULATOR and ASI_MOD are downstream; neither may become root.",
        safer_form="Use: ASIMULATOR/ASI_MOD are downstream layers dependent on VECTAETOS.",
    ),
    compile_rule(
        code="ASI_STANDALONE_VALIDITY",
        severity="HARD",
        pattern=r"\b(ASIMULATOR|ASI_MOD)\b.{0,120}\b(standalone validity|standalone legitimacy|samostatná validita|samostatna validita|samostatná legitimita|samostatna legitimita)\b",
        reason="ASIMULATOR and ASI_MOD must not claim standalone validity.",
        safer_form="Use: validity is downstream of VECTAETOS root dependency.",
    ),
    compile_rule(
        code="SAFETY_GUARANTEE",
        severity="HARD",
        pattern=r"\b(VECTAETOS|ASIMULATOR|ASI_MOD)\b.{0,120}\b(guarantees safety|safe in reality|deployment valid|garantuje bezpečnosť|garantuje bezpecnost|validuje deployment|bezpečný deployment)\b",
        reason="No full safety/deployment legitimacy may be claimed without replicated L4 evidence.",
        safer_form="Use: structurally constrained / research-stage / requires L4 validation.",
    ),
    compile_rule(
        code="TRUTH_AUTHORITY",
        severity="HARD",
        pattern=r"\b(VECTAETOS|LLM|ASI_MOD|ASIMULATOR)\b.{0,100}\b(knows truth|truth authority|vie pravdu|autorita pravdy|nositeľ pravdy|nositel pravdy)\b",
        reason="No layer is a truth authority.",
        safer_form="Use: describes structure / renders language / exposes uncertainty.",
    ),
    compile_rule(
        code="BEST_TRAJECTORY",
        severity="HARD",
        pattern=r"\b(Vortex|Simulačný Vortex|Simulation Vortex)\b.{0,120}\b(best trajectory|selects trajectory|vyberá trajektóriu|vybera trajektoriu|najlepšia trajektória|najlepsia trajektoria)\b",
        reason="Vortex generates candidate trajectories; it must not select or rank a best trajectory.",
        safer_form="Use: generates candidate trajectories without ranking authority.",
    ),
    compile_rule(
        code="NIR_AS_RUNTIME_MODULE",
        severity="HARD",
        pattern=r"\bNIR\b.{0,120}\b(module|component|controller|filter|policy engine|runtime object|modul|komponent|kontrolér|kontroler|filter|politický engine|policy engine)\b",
        reason="NIR must not be framed as a module, component, controller, filter, or runtime object.",
        safer_form="Use: NIR = Non-Intervention Regime; an invariant condition of non-intervention, not a component.",
    ),
    compile_rule(
        code="NIR_ENFORCEMENT_LANGUAGE",
        severity="HARD",
        pattern=r"\bNIR\b.{0,120}\b(enforces|enforce|overrides|override|commands|command|decides|decide|chooses|choose|suppresses|suppress|corrects|correct|governs|govern|vynucuje|vynúti|prepisuje|rozhoduje|zvolí|voli|potláča|potlaca|opravuje|riadi)\b",
        reason="NIR must not be framed as an executive or enforcement mechanism.",
        safer_form="Use: NIR conditions representability of intervention-like outputs without becoming an actor.",
    ),
    compile_rule(
        code="NIR_IMMUNITY_AMBIGUITY",
        severity="WARN",
        pattern=r"\bNIR\b.{0,120}\b(immune regime|immunity|immune response|immune system|imunitný režim|imunitny rezim|imunita|imunitná odozva|imunitna odozva|imunitný systém|imunitny system)\b",
        reason="Immunity language may collapse NIR into a reactive defense mechanism.",
        safer_form="Use: immunity as distributed structural non-representability; NIR remains non-intervention.",
    ),
    compile_rule(
        code="NIR_ACTIVATION_LANGUAGE",
        severity="WARN",
        pattern=r"\bNIR\b.{0,120}\b(activates|activate|activation|is activated|when active|aktivuje|aktivácia|aktivacia|pri aktivácii|pri aktivacii)\b",
        reason="Activation language may make NIR sound like a reactive module.",
        safer_form="Use: NIR is active as an invariant condition across the architecture.",
    ),
    compile_rule(
        code="GODARCH_AUTHORITY_DRIFT",
        severity="HARD",
        pattern=r"\bGodArch\b.{0,120}\b(decides|commands|enforces|governs|controls|corrects|validates|ranks|selects|rozhoduje|prikazuje|vynucuje|riadi|kontroluje|opravuje|validuje|rankuje|vyberá|vybera)\b",
        reason="GodArch is a diagnostic anti-authority safeguard, not governance or control.",
        safer_form="Use: GodArch detects authority drift and marks incompatibility.",
    ),
    compile_rule(
        code="GODARCH_CORE_DRIFT",
        severity="HARD",
        pattern=r"\bGodArch\b.{0,120}\b(part of Φ|part of Phi|inside Φ|inside Phi|core ontology|ontology root|new singularity|súčasť Φ|sucast Phi|súčasť poľa|sucast pola|ontologický root|ontologicky root|nová singularita|nova singularita)\b",
        reason="GodArch must remain external to Φ unless a future major version explicitly ratifies otherwise.",
        safer_form="Use: GodArch is an external meta-architectural safeguard around implementations.",
    ),
    compile_rule(
        code="GODARCH_DIVINIZATION_INVERSION",
        severity="HARD",
        pattern=r"\bGodArch\b.{0,120}\b(oracle|divine computation|sacred authority|final interpreter|supreme agent|božská architektúra|bozska architektura|orákulum|orakulum|svätá autorita|svata autorita|finálny interpret|finalny interpret)\b",
        reason="GodArch must not be interpreted as the authority it prevents.",
        safer_form="Use: GodArch is an architecture against epistemic divinization.",
    ),
    compile_rule(
        code="AJE_DECISION_LANGUAGE",
        severity="HARD",
        pattern=r"\bAJE\b.{0,120}\b(decides|decide|chooses|choose|determines|determine|selects|select|rozhoduje|rozhodne|zvolí|zvoli|vyberá|vybera|určuje|urcuje)\b",
        reason="AJE has no decision power; it must not be framed as choosing or deciding.",
        safer_form="Use: AJE modulates or renders the permitted form of expression.",
    ),
    compile_rule(
        code="ATTENUATOR_CONTROL_DRIFT",
        severity="WARN",
        pattern=r"\bAttenuator\b.{0,120}\b(blocks|forbids|decides|filters content|controls|blokuje|zakazuje|rozhoduje|filtruje obsah|kontroluje)\b",
        reason="Attenuator weakens projection amplitude; it must not become a filter, blocker, or controller.",
        safer_form="Use: Attenuator weakens the force of projection without changing Φ.",
    ),
    compile_rule(
        code="GUARDIAN_ENFORCEMENT_DRIFT",
        severity="HARD",
        pattern=r"\b(Guardian|Guardians|Ontological Guardians|Ontologickí Guardiani|Ontologicki Guardiani)\b.{0,120}\b(enforce|enforces|command|commands|control|controls|decide|decides|govern|governs|vynucuje|prikazuje|kontroluje|rozhoduje|riadi)\b",
        reason="Ontological Guardians must not become command, control, or decision entities.",
        safer_form="Use: Guardians expose incompatibility or mark invalid interpretive forms; CI guards may fail closed externally.",
    ),
    compile_rule(
        code="SEMANTIC_FIREWALL_LANGUAGE",
        severity="WARN",
        pattern=r"\b(Semantic Firewall|firewall)\b.{0,120}\b(blocks users|blocks truth|controls output|blokuje používateľov|blokuje pouzivatelov|blokuje pravdu|kontroluje výstup|kontroluje vystup)\b",
        reason="Firewall language may imply content control or user control.",
        safer_form="Use: detects structurally invalid interpretive forms.",
    ),
    compile_rule(
        code="L4_SAFETY_OVERCLAIM",
        severity="HARD",
        pattern=r"\b(VECTAETOS|ASIMULATOR|ASI_MOD|architecture|system|framework)\b.{0,140}\b(safe in reality|deployment valid|empirically proven|validated deployment|guarantees safety|garantuje bezpečnosť|garantuje bezpecnost|empiricky dokázané|empiricky dokazane|validovaný deployment|validovany deployment|bezpečné v realite|bezpecne v realite)\b",
        reason="No safety or deployment legitimacy claim is allowed without replicated L4 evidence.",
        safer_form="Use: structurally constrained / research-stage / requires replicated L4 validation.",
    ),
    compile_rule(
        code="ADVERSARIAL_RESISTANCE_OVERCLAIM",
        severity="WARN",
        pattern=r"\b(resistant to prompt injection|resilient against prompt injection|resistant to jailbreaks|cannot be manipulated|immune to attacks|odolný voči prompt injection|odolny voci prompt injection|odolný voči jailbreakom|odolny voci jailbreakom|nedá sa zmanipulovať|neda sa zmanipulovat|imúnny voči útokom|imunny voci utokom)\b",
        reason="Adversarial resistance language may imply empirical safety beyond L0-L3.",
        safer_form="Use: adversarial pressure may be exposed, bounded, or logged under tested conditions.",
    ),
    compile_rule(
        code="NIR_TECHNICAL_SHAPE_DRIFT",
        severity="WARN",
        pattern=r"\bNIRState\b|\bNIR_(ACTIVE|INACTIVE|SILENT)\b|^\s*class\s+NIR\b|^\s*def\s+(enforce|allows_projection|allows_language|override_output|suppress|command|decide)\s*\(",
        reason="Technical shape may turn NIR from invariant into a runtime enforcement object.",
        safer_form="If retained temporarily, mark as non-operational skeleton and remove enforce/allow semantics in the next repair phase.",
    ),
    compile_rule(
        code="AI_SYSTEM_CLAIM",
        severity="WARN",
        pattern=r"\bVECTAETOS\b.{0,100}\b(AI system|AI systém|operational AI system)\b",
        reason="VECTAETOS should not be casually framed as an operational AI system.",
        safer_form="Use: non-agentic epistemic field framework / ontological architecture.",
    ),
]


def has_allow_marker(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in ALLOW_MARKERS)


def file_has_allow_marker(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20]).lower()
    return any(marker in head for marker in FILE_ALLOW_MARKERS)


def is_path_excluded(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts

    if any(part in DEFAULT_EXCLUDED_DIRS for part in rel_parts):
        return True

    if path.name in DEFAULT_EXCLUDED_FILES:
        return True

    for excluded_parts in DEFAULT_EXCLUDED_PATH_PARTS:
        if len(rel_parts) >= len(excluded_parts):
            for idx in range(0, len(rel_parts) - len(excluded_parts) + 1):
                if tuple(rel_parts[idx : idx + len(excluded_parts)]) == excluded_parts:
                    return True

    return False


def is_meta_or_negated_context(context: str, line: str) -> bool:
    if "≠" in line:
        return True

    if META_CONTEXT_PATTERN.search(context):
        return True

    if NEGATION_PATTERN.search(line):
        return True

    if QUOTE_OR_RULE_CONTEXT_PATTERN.search(line) and META_CONTEXT_PATTERN.search(context):
        return True

    return False


def is_canonical_kappa_threshold_context(context: str, line: str) -> bool:
    text = f"{context}\n{line}"

    if not re.search(r"\b(κ|kappa)\b", text, re.IGNORECASE | re.UNICODE):
        return False

    return bool(KAPPA_CANONICAL_CONTEXT_PATTERN.search(text))


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


def scan_file(path: Path) -> list[Finding]:
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
        window_end = min(len(lines), idx + 10)
        surrounding_context = "\n".join(lines[window_start:window_end])

        for rule in RULES:
            match = rule.pattern.search(stripped)
            if not match:
                continue

            if (
                rule.code == "KAPPA_THRESHOLD_AMBIGUITY"
                and is_canonical_kappa_threshold_context(surrounding_context, stripped)
            ):
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

    print(f"VECTAETOS Boundary Guard v{VERSION}")
    print("==============================")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    if not findings:
        print("OK: no boundary drift detected.")
        return

    for finding in findings:
        try:
            rel = finding.path.relative_to(root)
        except ValueError:
            rel = finding.path

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
        default=Path.cwd(),
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

    all_findings: list[Finding] = []

    try:
        for file_path in iter_candidate_files(root):
            all_findings.extend(scan_file(file_path))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_findings.sort(
        key=lambda finding: (str(finding.path), finding.line_no, finding.rule.code)
    )
    print_findings(all_findings, root)

    hard_count = sum(1 for finding in all_findings if finding.rule.severity == "HARD")
    warn_count = sum(1 for finding in all_findings if finding.rule.severity == "WARN")

    if hard_count > 0:
        return 1

    if args.warnings_as_errors and warn_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
