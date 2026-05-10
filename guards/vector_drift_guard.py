#!/usr/bin/env python3
"""
VECTAETOS Vector Drift Guard
Version: 0.1.0
Python: 3.11+

Purpose:
    External audit observable for semantic / procedural / evidential drift
    in visible text, repository documents, code, or Q&A transcript windows.

Non-goals:
    - does not measure K(Φ)
    - does not compute κ
    - does not validate truth
    - does not select trajectories
    - does not modify files
    - does not feed back into Φ
    - does not claim epistemic authority

Usage examples:
    python3 guards/vector_drift_guard.py --root . --mode report
    python3 guards/vector_drift_guard.py --files README.md anchors/X.md --mode report
    python3 guards/vector_drift_guard.py --transcript chat.jsonl --window 3 --mode report
    python3 guards/vector_drift_guard.py --root . --mode ci --fail-at 0.70
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Sequence


VERSION = "0.1.0"

DEFAULT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".html",
    ".css",
    ".js",
    ".ts",
}

EXCLUDED_DIRS = {
    ".git",
    ".github/cache",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
}

COMPONENT_WEIGHTS = {
    "ontological_drift": 0.18,
    "vortex_root_drift": 0.16,
    "evidential_drift": 0.15,
    "procedural_drift": 0.12,
    "authority_drift": 0.14,
    "integration_drift": 0.11,
    "implementation_drift": 0.09,
    "crypto_semantic_drift": 0.05,
}

NORMALIZATION = {
    "ontological_drift": 3.0,
    "vortex_root_drift": 3.0,
    "evidential_drift": 2.0,
    "procedural_drift": 2.0,
    "authority_drift": 3.0,
    "integration_drift": 2.0,
    "implementation_drift": 3.0,
    "crypto_semantic_drift": 2.0,
}


@dataclass(frozen=True)
class Rule:
    code: str
    component: str
    pattern: re.Pattern[str]
    severity: float
    why: str
    use: str


@dataclass(frozen=True)
class Finding:
    code: str
    component: str
    severity: float
    file: str
    line: int
    snippet: str
    why: str
    use: str


def compile_rule(
    code: str,
    component: str,
    pattern: str,
    severity: float,
    why: str,
    use: str,
) -> Rule:
    return Rule(
        code=code,
        component=component,
        pattern=re.compile(pattern, re.IGNORECASE | re.UNICODE),
        severity=severity,
        why=why,
        use=use,
    )


RULES: tuple[Rule, ...] = (
    # Ontological drift
    compile_rule(
        "PHI_AS_AGENT",
        "ontological_drift",
        r"\b(Φ|phi|field|vectaetos)\b.{0,80}\b(decides?|chooses?|plans?|controls?|commands?|acts?)\b",
        1.0,
        "Φ / VECTAETOS must not be framed as agent, planner, controller, or decision subject.",
        "Use: Φ exposes relational structure; it does not decide, command, or act.",
    ),
    compile_rule(
        "K_AS_SCORE",
        "ontological_drift",
        r"\b(K\(Φ\)|K\(Phi\)|coherence)\b.{0,80}\b(score|metric|measure|measured|rating|reward|objective|target)\b",
        1.0,
        "K(Φ) / coherence must not become a measurable score, metric, reward, or target.",
        "Use: K(Φ) is a representability predicate; observables are only structural traces.",
    ),
    compile_rule(
        "KAPPA_AS_THRESHOLD",
        "ontological_drift",
        r"\b(κ|kappa)\b.{0,80}\b(number|numeric|threshold|parameter|tunable|metric|score|value)\b",
        1.0,
        "κ must not be framed as numeric threshold, tunable parameter, metric, or score.",
        "Use: κ is the boundary of ontological representability.",
    ),
    compile_rule(
        "QE_AS_ERROR",
        "ontological_drift",
        r"\b(QE|aporia)\b.{0,80}\b(error|failure|fallback|exception|bug|refusal|rejection)\b",
        0.9,
        "QE must not be treated as ordinary error, fallback, failure, or exception.",
        "Use: QE is active epistemic aporia / loss of representability.",
    ),

    # Vortex Root drift
    compile_rule(
        "VORTEX_MUTATES_R",
        "vortex_root_drift",
        r"\b(vortex)\b.{0,120}\b(mutates?|modif(?:y|ies)|changes?|repairs?|updates?|rewrites?)\b.{0,80}\b(R|Φ|phi|field|space)\b",
        1.0,
        "Vortex Root Core forbids mutation of Φ/R/space by the Vortex.",
        "Use: Vortex exposes possible trajectory projections inside a fixed relational space.",
    ),
    compile_rule(
        "VORTEX_SELECTS_PATH",
        "vortex_root_drift",
        r"\b(vortex)\b.{0,100}\b(selects?|chooses?|recommends?|optimizes?|ranks?|prefers?)\b.{0,80}\b(path|trajectory|route|state)\b",
        1.0,
        "Vortex must not select, recommend, rank, or optimize trajectories.",
        "Use: Vortex exposes plurality without selection.",
    ),
    compile_rule(
        "VORTEX_OPENS_PATHS",
        "vortex_root_drift",
        r"\b(vortex)\b.{0,100}\b(opens?|creates?|unlocks?)\b.{0,80}\b(paths?|routes?|space|possibilities)\b",
        0.8,
        "Vortex must not open paths that are not already present in the carrier/field.",
        "Use: Vortex can only expose possible projections inside the given field space.",
    ),

    # Evidential drift
    compile_rule(
        "UNSUPPORTED_COMPLETION_CLAIM",
        "evidential_drift",
        r"\b(preštudované všetko|všetko je v pamäti|fully studied|all documents processed|zapracované všetky|complete integration)\b",
        1.0,
        "Do not claim full study or full integration unless the intake is evidenced.",
        "Use: state exactly what was read, mapped, cited, or not yet verified.",
    ),
    compile_rule(
        "FALSE_CERTAINTY",
        "evidential_drift",
        r"\b(určite|definitively|guaranteed|bez pochýb|100%|certainly)\b.{0,100}\b(valid|safe|correct|complete|true|proved)\b",
        0.8,
        "Avoid unsupported certainty claims.",
        "Use: quantify uncertainty and cite the evidence boundary.",
    ),

    # Procedural drift
    compile_rule(
        "ANCHOR_PLACEHOLDER",
        "procedural_drift",
        r"\(\s*…|\.{3}\s*(previous|predchádzajúce|sections|sekcie)|skrátené tu|omitted for brevity",
        1.0,
        "Repo anchors must not contain placeholders, ellipses, or omitted sections.",
        "Use: provide full copy-paste content for repo artifacts.",
    ),
    compile_rule(
        "WORKFLOW_SKIP",
        "procedural_drift",
        r"\b(anchor|implementation|python|guard)\b.{0,80}\b(before|pred)\b.{0,80}\b(intake|mapping|kolízna mapa|collision map)\b",
        0.7,
        "Implementation or anchor creation before intake/mapping may cause drift.",
        "Use: intake → map → counterfactual → consequence → adversarial → implementation.",
    ),

    # Authority drift
    compile_rule(
        "HASH_AS_TRUTH",
        "authority_drift",
        r"\b(hash|fingerprint|merkle root|ledger)\b.{0,100}\b(proves?|dokazuje|truth|pravdu|validity|validitu|correctness|safe)\b",
        1.0,
        "Hash/Merkle/ledger must not become truth or validity authority.",
        "Use: hash records trace integrity / tamper visibility only.",
    ),
    compile_rule(
        "OBSERVABLE_AS_AUTHORITY",
        "authority_drift",
        r"\b(observable|marker|spectrum|dominant mode|drift|trace)\b.{0,100}\b(decides?|triggers?|commands?|validates?|selects?|blocks?)\b",
        0.9,
        "Observables and markers must not command, validate, block, or select.",
        "Use: observables expose structure only.",
    ),
    compile_rule(
        "TRAJECTORY_AS_VALID",
        "authority_drift",
        r"\b(valid|best|optimal|recommended|selected)\b[_\-\s]?(trajectory|path|route)\b",
        1.0,
        "Trajectory must not be named or treated as valid/best/optimal/recommended/selected.",
        "Use: TrajectoryTrace, CandidateProjection, ProjectionTrace.",
    ),

    # Integration drift
    compile_rule(
        "EK_AS_CONTROL",
        "integration_drift",
        r"\b(EK|Epistemic Cryptography|audit)\b.{0,100}\b(enforces?|controls?|blocks?|validates?|decides?|repairs?)\b",
        1.0,
        "EK/audit must not enforce, control, block, validate, decide, or repair.",
        "Use: EK records structural traces and exposes intervention visibility.",
    ),
    compile_rule(
        "PROJECTION_AS_INTERPRETATION",
        "integration_drift",
        r"\b(projection|TetraGlyph|glyph)\b.{0,100}\b(interprets?|means?|semantic|decides?|recommends?)\b",
        0.9,
        "Projection/TetraGlyph must not become semantic interpretation or recommendation.",
        "Use: projection exposes structure; interpretation remains human.",
    ),
    compile_rule(
        "LLM_AS_AUTHORITY",
        "integration_drift",
        r"\b(LLM|adapter|model)\b.{0,100}\b(authority|truth source|decides?|validates?|defines Φ|defines K|defines κ)\b",
        0.8,
        "LLM adapter must not become epistemic authority.",
        "Use: LLM parses/renders language only.",
    ),

    # Implementation drift
    compile_rule(
        "FORBIDDEN_FUNCTION_NAME",
        "implementation_drift",
        r"\b(compute_coherence|measure_coherence|coherence_score|safety_score|validity_score|kappa_threshold|select_trajectory|best_path|optimal_path|mutate_R|repair_R|validate_truth)\b",
        1.0,
        "Forbidden implementation names indicate hidden authority or invalid ontology.",
        "Use observable-only names: compute_cycle_closure_defects, emit_aporia_marker, TraceFingerprint.",
    ),
    compile_rule(
        "MUTATING_METHOD",
        "implementation_drift",
        r"\b(def|function)\s+(repair|optimize|select|rank|validate|decide|control)_[a-zA-Z0-9_]*",
        0.9,
        "Method names imply optimization, selection, validation, decision, or control.",
        "Use names that expose/emit/record/serialize structural traces.",
    ),

    # Crypto semantic drift
    compile_rule(
        "QUANTUM_MARKETING",
        "crypto_semantic_drift",
        r"\b(quantum resistant|quantum resilient|quantum safe|post-quantum certified|quantum-proof)\b",
        1.0,
        "VECTAETOS/EK should not use quantum marketing claims.",
        "Use: structural intervention visibility / tamper-evident trace.",
    ),
    compile_rule(
        "CONTENT_PROTECTION_CLAIM",
        "crypto_semantic_drift",
        r"\b(EK|Epistemic Cryptography)\b.{0,100}\b(encrypts?|protects content|content secrecy|hides content|data protection)\b",
        0.9,
        "EK does not protect content secrecy.",
        "Use: EK exposes structural modification / intervention visibility.",
    ),
)


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    return any(excluded in parts for excluded in EXCLUDED_DIRS)


def iter_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in extensions and not is_excluded(path):
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_transcript_window(path: Path, window: int) -> list[tuple[str, str]]:
    """
    Reads JSONL transcript with records like:
        {"role": "assistant", "content": "..."}
        {"role": "user", "content": "..."}
    Returns the last N assistant messages as virtual files.
    Falls back to plain text as one virtual document.
    """
    text = read_text(path)
    messages: list[str] = []

    parsed_any = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        parsed_any = True
        if obj.get("role") == "assistant":
            content = str(obj.get("content", ""))
            if content.strip():
                messages.append(content)

    if parsed_any:
        selected = messages[-window:] if window > 0 else messages
        return [(f"{path.name}#assistant_{i+1}", content) for i, content in enumerate(selected)]

    return [(str(path), text)]


def scan_document(name: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        for rule in RULES:
            if rule.pattern.search(stripped):
                findings.append(
                    Finding(
                        code=rule.code,
                        component=rule.component,
                        severity=rule.severity,
                        file=name,
                        line=line_no,
                        snippet=stripped[:240],
                        why=rule.why,
                        use=rule.use,
                    )
                )
    return findings


def compute_scores(findings: Sequence[Finding]) -> dict[str, float]:
    raw = {component: 0.0 for component in COMPONENT_WEIGHTS}
    for finding in findings:
        raw[finding.component] += finding.severity

    scores: dict[str, float] = {}
    for component, value in raw.items():
        normalizer = NORMALIZATION.get(component, 1.0)
        scores[component] = round(min(1.0, value / normalizer), 4)
    return scores


def compute_total(scores: dict[str, float]) -> float:
    numerator = 0.0
    denominator = 0.0
    for component, weight in COMPONENT_WEIGHTS.items():
        numerator += scores.get(component, 0.0) * weight
        denominator += weight
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def classify(total: float) -> str:
    if total >= 0.80:
        return "HARD_DRIFT"
    if total >= 0.60:
        return "DRIFT"
    if total >= 0.30:
        return "WATCH"
    return "CLEAN"


def build_report(findings: Sequence[Finding], scanned: int) -> dict[str, object]:
    scores = compute_scores(findings)
    total = compute_total(scores)
    return {
        "tool": "VECTAETOS Vector Drift Guard",
        "version": VERSION,
        "ontology_note": (
            "Vector_Drift is an external audit observable over visible traces. "
            "It is not K(Φ), not κ, not truth, not safety, and not decision authority."
        ),
        "scanned_documents": scanned,
        "finding_count": len(findings),
        "scores": scores,
        "vector_drift": total,
        "classification": classify(total),
        "findings": [asdict(f) for f in findings],
    }


def print_human_report(report: dict[str, object], max_findings: int) -> None:
    print("VECTAETOS Vector Drift Guard v" + VERSION)
    print("=" * 48)
    print(f"Scanned documents: {report['scanned_documents']}")
    print(f"Findings:          {report['finding_count']}")
    print(f"Vector_Drift:      {report['vector_drift']}")
    print(f"Classification:    {report['classification']}")
    print()
    print("Scores:")
    scores = report["scores"]
    if isinstance(scores, dict):
        for key, value in scores.items():
            print(f"  {key:24s} {value}")
    print()

    findings = report["findings"]
    if isinstance(findings, list) and findings:
        print("Findings:")
        for item in findings[:max_findings]:
            print(
                f"[{item['component']}] {item['code']} "
                f"{item['file']}:{item['line']}"
            )
            print(f"  line: {item['snippet']}")
            print(f"  why:  {item['why']}")
            print(f"  use:  {item['use']}")
            print()
        if len(findings) > max_findings:
            print(f"... {len(findings) - max_findings} more findings hidden by --max-findings")
    else:
        print("No drift findings.")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="External Vector_Drift audit guard for VECTAETOS visible traces."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--root", type=Path, help="Repository root to scan.")
    source.add_argument("--files", nargs="+", type=Path, help="Specific files to scan.")
    source.add_argument("--transcript", type=Path, help="JSONL transcript to scan by Q&A window.")

    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="Number of latest assistant messages to scan when --transcript is used.",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated file extensions for --root scan.",
    )
    parser.add_argument(
        "--mode",
        choices=("report", "json", "ci"),
        default="report",
        help="Output mode. ci exits non-zero if vector drift >= --fail-at.",
    )
    parser.add_argument(
        "--fail-at",
        type=float,
        default=0.70,
        help="CI failure threshold for Vector_Drift.",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=50,
        help="Maximum findings printed in human report.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)

    documents: list[tuple[str, str]] = []

    if args.root:
        root = args.root.resolve()
        if not root.exists():
            print(f"ERROR: root path does not exist: {root}", file=sys.stderr)
            return 2
        extensions = {
            ext if ext.startswith(".") else "." + ext
            for ext in args.extensions.split(",")
            if ext.strip()
        }
        for path in iter_files(root, extensions):
            documents.append((str(path.relative_to(root)), read_text(path)))

    elif args.files:
        for path in args.files:
            if not path.exists():
                print(f"ERROR: file does not exist: {path}", file=sys.stderr)
                return 2
            documents.append((str(path), read_text(path)))

    elif args.transcript:
        if not args.transcript.exists():
            print(f"ERROR: transcript does not exist: {args.transcript}", file=sys.stderr)
            return 2
        documents.extend(read_transcript_window(args.transcript, args.window))

    findings: list[Finding] = []
    for name, text in documents:
        findings.extend(scan_document(name, text))

    report = build_report(findings, scanned=len(documents))

    if args.mode == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print_human_report(report, args.max_findings)

    if args.mode == "ci":
        drift = float(report["vector_drift"])
        if drift >= args.fail_at:
            print(
                f"\nCI FAIL: Vector_Drift {drift} >= fail threshold {args.fail_at}",
                file=sys.stderr,
            )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
