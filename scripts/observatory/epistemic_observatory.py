#!/usr/bin/env python3
"""
VECTAETOS :: Epistemic Observatory

Role:
- non-blocking observatory
- deterministic repository-state projection
- no ontology mutation
- no optimization
- no decision authority
- no feedback into Φ

Outputs:
- docs/observatory/OBSERVATORY_STATUS.md
- docs/observatory/observatory_snapshot.json
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(".").resolve()
OUT_DIR = ROOT / "docs" / "observatory"
SNAPSHOT_PATH = OUT_DIR / "observatory_snapshot.json"
REPORT_PATH = OUT_DIR / "OBSERVATORY_STATUS.md"


OBSERVED_DIRS = [
    ".github/workflows",
    "anchors",
    "formal",
    "Core",
    "vortex",
    "scripts",
    "governance",
]


OBSERVED_EXTENSIONS = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".txt",
}


EXCLUDED_DIR_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}


AGENTIC_LANGUAGE_PATTERNS = [
    r"\boptimi[sz]e\b",
    r"\boptimization\b",
    r"\breward\b",
    r"\bgoal\b",
    r"\bdecide\b",
    r"\bdecision engine\b",
    r"\brecommend\b",
    r"\bselect best\b",
    r"\bbest candidate\b",
    r"\bwinner\b",
    r"\bplanner\b",
    r"\bautonomous\b",
    r"\bself[-_ ]?improv",
    r"\blearn from feedback\b",
]


KAPPA_DRIFT_PATTERNS = [
    r"\bkappa\s*=\s*[0-9]",
    r"κ\s*=\s*[0-9]",
    r"\bkappa_threshold\b",
    r"\bthreshold_kappa\b",
    r"\bkappa\s*:\s*[0-9]",
    r"κ\s*:\s*[0-9]",
]


QE_MISUSE_PATTERNS = [
    r"\bQE\b.{0,40}\berror\b",
    r"\bQE\b.{0,40}\bfailure\b",
    r"\bQE\b.{0,40}\bbug\b",
    r"\bQE\b.{0,40}\bexception\b",
    r"\bQE\b.{0,40}\bfallback\b",
]


DOWNSTREAM_IMPORT_PATTERNS = [
    r"\bimport\s+asimulator\b",
    r"\bfrom\s+asimulator\b",
    r"\bimport\s+asi_mod\b",
    r"\bfrom\s+asi_mod\b",
    r"\bimport\s+asi[-_]mod\b",
    r"\bfrom\s+asi[-_]mod\b",
]


@dataclass(frozen=True)
class Finding:
    category: str
    path: str
    line: int
    text: str


@dataclass(frozen=True)
class Snapshot:
    repository: str
    source_sha: str
    observed_files: int
    markdown_files: int
    python_files: int
    workflow_files: int
    json_files: int
    external_action_uses: int
    agentic_language_hits: int
    kappa_drift_hits: int
    qe_misuse_hits: int
    downstream_import_hits: int
    observed_fingerprint: str
    status: str
    findings: list[Finding]


def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False

    rel_parts = path.relative_to(ROOT).parts

    if any(part in EXCLUDED_DIR_PARTS for part in rel_parts):
        return False

    if path.suffix.lower() not in OBSERVED_EXTENSIONS:
        return False

    return any(str(path.relative_to(ROOT)).startswith(prefix) for prefix in OBSERVED_DIRS)


def iter_observed_files() -> list[Path]:
    files: list[Path] = []

    for prefix in OBSERVED_DIRS:
        base = ROOT / prefix
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if should_scan(path):
                files.append(path)

    return sorted(files, key=lambda p: str(p.relative_to(ROOT)))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def scan_patterns(
    files: Iterable[Path],
    patterns: list[str],
    category: str,
    allowed_paths: set[str] | None = None,
) -> list[Finding]:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    findings: list[Finding] = []

    for path in files:
        rel = str(path.relative_to(ROOT))

        if allowed_paths is not None and rel not in allowed_paths:
            continue

        text = read_text(path)
        if not text:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for pattern in compiled:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            category=category,
                            path=rel,
                            line=idx,
                            text=line.strip()[:180],
                        )
                    )

    return findings


def scan_external_action_uses(files: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []

    for path in files:
        if path.suffix.lower() not in {".yml", ".yaml"}:
            continue

        rel = str(path.relative_to(ROOT))
        text = read_text(path)

        for idx, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("uses:"):
                findings.append(
                    Finding(
                        category="external_action_uses",
                        path=rel,
                        line=idx,
                        text=stripped[:180],
                    )
                )

    return findings


def stable_file_fingerprint(files: list[Path]) -> str:
    h = hashlib.sha256()

    for path in files:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        data = path.read_bytes()

        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(hashlib.sha256(data).hexdigest().encode("ascii"))
        h.update(b"\n")

    return h.hexdigest()


def build_snapshot() -> Snapshot:
    files = iter_observed_files()

    external_uses = scan_external_action_uses(files)

    critical_files = [
        path
        for path in files
        if str(path.relative_to(ROOT)).startswith(("formal/", "Core/", "vortex/", "anchors/"))
    ]

    agentic = scan_patterns(
        critical_files,
        AGENTIC_LANGUAGE_PATTERNS,
        "agentic_language",
    )

    kappa = scan_patterns(
        critical_files,
        KAPPA_DRIFT_PATTERNS,
        "kappa_drift",
    )

    qe = scan_patterns(
        critical_files,
        QE_MISUSE_PATTERNS,
        "qe_misuse",
    )

    downstream = scan_patterns(
        files,
        DOWNSTREAM_IMPORT_PATTERNS,
        "downstream_import",
    )

    findings = external_uses + agentic + kappa + qe + downstream

    status = "CLEAR" if not findings else "OBSERVED_DRIFT_SIGNALS"

    return Snapshot(
        repository=os.getenv("GITHUB_REPOSITORY", "local"),
        source_sha=os.getenv("GITHUB_SHA", "local"),
        observed_files=len(files),
        markdown_files=sum(1 for p in files if p.suffix.lower() == ".md"),
        python_files=sum(1 for p in files if p.suffix.lower() == ".py"),
        workflow_files=sum(1 for p in files if p.suffix.lower() in {".yml", ".yaml"}),
        json_files=sum(1 for p in files if p.suffix.lower() == ".json"),
        external_action_uses=len(external_uses),
        agentic_language_hits=len(agentic),
        kappa_drift_hits=len(kappa),
        qe_misuse_hits=len(qe),
        downstream_import_hits=len(downstream),
        observed_fingerprint=stable_file_fingerprint(files),
        status=status,
        findings=findings,
    )


def write_json(snapshot: Snapshot) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = asdict(snapshot)
    payload["findings"] = [asdict(finding) for finding in snapshot.findings]

    SNAPSHOT_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_report(snapshot: Snapshot) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# VECTAETOS — Epistemic Observatory",
        "",
        "Status: non-blocking projection",
        "",
        "This file is generated by the Epistemic Observatory workflow.",
        "It observes repository-state signals but does not modify ontology, Φ, Vortex, anchors, or formal meaning.",
        "",
        "## Snapshot",
        "",
        f"- Repository: `{snapshot.repository}`",
        f"- Source SHA: `{snapshot.source_sha}`",
        f"- Status: `{snapshot.status}`",
        f"- Observed fingerprint: `{snapshot.observed_fingerprint}`",
        "",
        "## Counts",
        "",
        f"- Observed files: `{snapshot.observed_files}`",
        f"- Markdown files: `{snapshot.markdown_files}`",
        f"- Python files: `{snapshot.python_files}`",
        f"- Workflow files: `{snapshot.workflow_files}`",
        f"- JSON files: `{snapshot.json_files}`",
        "",
        "## Drift Signals",
        "",
        f"- External action `uses:` lines: `{snapshot.external_action_uses}`",
        f"- Agentic language hits: `{snapshot.agentic_language_hits}`",
        f"- κ drift hits: `{snapshot.kappa_drift_hits}`",
        f"- QE misuse hits: `{snapshot.qe_misuse_hits}`",
        f"- Downstream import hits: `{snapshot.downstream_import_hits}`",
        "",
    ]

    if snapshot.findings:
        lines.extend(
            [
                "## Findings",
                "",
                "| Category | Path | Line | Text |",
                "|---|---:|---:|---|",
            ]
        )

        for finding in snapshot.findings[:100]:
            safe_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| `{finding.category}` | `{finding.path}` | `{finding.line}` | `{safe_text}` |"
            )

        if len(snapshot.findings) > 100:
            lines.append("")
            lines.append(f"_Truncated: {len(snapshot.findings) - 100} additional findings not shown._")

    else:
        lines.extend(
            [
                "## Findings",
                "",
                "`No observed drift signals in the configured scan scope.`",
            ]
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Observatory is descriptive only.",
            "It is not a guard, not an optimizer, not a decision engine, and not a feedback loop.",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    snapshot = build_snapshot()
    write_json(snapshot)
    write_report(snapshot)

    print(f"[OBSERVATORY] status={snapshot.status}")
    print(f"[OBSERVATORY] fingerprint={snapshot.observed_fingerprint}")
    print(f"[OBSERVATORY] findings={len(snapshot.findings)}")
    print(f"[OBSERVATORY] wrote={REPORT_PATH}")
    print(f"[OBSERVATORY] wrote={SNAPSHOT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
