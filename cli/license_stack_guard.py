#!/usr/bin/env python3
"""
VECTAETOS™ License Stack Guard

Level mapping:
  - Level 0: Fundamental Repository Perimeter
  - Level 5: Runtime / Evidence / Release Perimeter

Purpose:
  Detect repository-state drift in the VECTAETOS™ license stack.

Boundary:
  This guard does not define ontology, prove truth, validate safety,
  authorize deployment, or mutate Φ. It only emits repository-state findings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class Severity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"


class Level(StrEnum):
    LEVEL_0 = "Level 0 — Fundamental Repository Perimeter"
    LEVEL_5 = "Level 5 — Runtime / Evidence / Release Perimeter"


@dataclass(frozen=True)
class Finding:
    id: str
    level: str
    severity: str
    rule_id: str
    path: str
    line: int | None
    message: str
    safer_form: str
    ontology_authority: bool = False
    auto_fix_allowed: bool = False


REQUIRED_FILES = (
    "LICENSE.md",
    "LICENSES/README.md",
    "LICENSES/LICENSE_STACK.md",
    "LICENSES/VCL-2.0.md",
    "LICENSES/AEPL-2.0-VECTAETOS.md",
    "LICENSES/VNAL-1.1.md",
    "LICENSES/VPL-1.0.md",
    "LICENSES/VTP-1.0.md",
    "LICENSES/LICENSE_LINEAGE_AND_SUPERSESSION.md",
    "LICENSES/ZENODO_RELEASE_MINIGUIDE.md",
)

FILES_TO_SCAN = (
    "LICENSE.md",
    "LICENSES/README.md",
    "LICENSES/LICENSE_STACK.md",
    "LICENSES/VCL-2.0.md",
    "LICENSES/AEPL-2.0-VECTAETOS.md",
    "LICENSES/VNAL-1.1.md",
    "LICENSES/VPL-1.0.md",
    "LICENSES/VTP-1.0.md",
    "LICENSES/LICENSE_LINEAGE_AND_SUPERSESSION.md",
    "LICENSES/ZENODO_RELEASE_MINIGUIDE.md",
    "README.md",
)

REQUIRED_ROOT_LICENSE_REFERENCES = (
    "LICENSES/README.md",
    "LICENSES/VCL-2.0.md",
    "LICENSES/AEPL-2.0-VECTAETOS.md",
    "LICENSES/VNAL-1.1.md",
    "LICENSES/VPL-1.0.md",
    "LICENSES/VTP-1.0.md",
)

REQUIRED_LICENSE_README_BOUNDARIES = (
    "license ≠ ontology",
    "policy ≠ truth",
    "trademark ≠ Φ",
    "guard ≠ authority",
    "hash ≠ semantic truth",
    "projection ≠ interpretation",
    "EK ≠ decision",
)

DEPRECATED_PERIMETER_LABELS = ("P0", "P1", "P2", "P3", "P4")

FORBIDDEN_AUTHORITY_PATTERNS = (
    r"\bproves?\s+ontology\b",
    r"\bproves?\s+truth\b",
    r"\bproves?\s+safety\b",
    r"\bvalidates?\s+deployment\b",
    r"\bauthorizes?\s+deployment\b",
    r"\bcertifies?\s+truth\b",
    r"\bcertifies?\s+safety\b",
    r"\bcertifies?\s+ontology\b",
    r"\bEK\s+decides?\b",
    r"\bEK\s+validates?\b",
    r"\bEK\s+certifies?\b",
    r"\bhash\s+proves?\b",
    r"\bsignature\s+proves?\b",
    r"\bDOI\s+proves?\b",
    r"\blicense\s+defines?\s+Φ\b",
    r"\blicense\s+defines?\s+ontology\b",
    r"\bpolicy\s+defines?\s+truth\b",
    r"\bguard\s+defines?\s+ontology\b",
    r"\bguard\s+proves?\b",
    r"\bCI\s+proves?\b",
)

SAFE_CONTEXT_MARKERS = (
    "forbidden",
    "not allowed",
    "prohibited",
    "must not",
    "may not",
    "does not",
    "do not",
    "≠",
    "not ",
    "no ",
    "non-goals",
    "strict prohibitions",
    "forbidden statement",
    "forbidden wording",
    "forbidden doi wording",
    "forbidden without",
    "must never",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_safe_context(lines: list[str], index: int) -> bool:
    start = max(0, index - 5)
    window = "\n".join(lines[start : index + 1]).lower()
    return any(marker.lower() in window for marker in SAFE_CONTEXT_MARKERS)


def required_files_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for rel in REQUIRED_FILES:
        path = repo_root / rel
        if not path.exists():
            findings.append(
                Finding(
                    id="VEC-LIC-REQ-001",
                    level=Level.LEVEL_0.value,
                    severity=Severity.BLOCKER.value,
                    rule_id="LICENSE-REQUIRED-FILE",
                    path=rel,
                    line=None,
                    message=f"Required license stack file is missing: {rel}",
                    safer_form="Create the required file or update the license stack policy intentionally.",
                )
            )
        elif path.is_dir():
            findings.append(
                Finding(
                    id="VEC-LIC-REQ-002",
                    level=Level.LEVEL_0.value,
                    severity=Severity.BLOCKER.value,
                    rule_id="LICENSE-FILE-IS-DIRECTORY",
                    path=rel,
                    line=None,
                    message=f"Expected a file but found a directory: {rel}",
                    safer_form="Replace the directory with the required Markdown file.",
                )
            )

    return findings


def root_license_links_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    root_license = repo_root / "LICENSE.md"

    if not root_license.exists():
        return findings

    text = read_text(root_license)

    for required_ref in REQUIRED_ROOT_LICENSE_REFERENCES:
        if required_ref not in text:
            findings.append(
                Finding(
                    id="VEC-LIC-LINK-001",
                    level=Level.LEVEL_0.value,
                    severity=Severity.ERROR.value,
                    rule_id="ROOT-LICENSE-MISSING-REFERENCE",
                    path="LICENSE.md",
                    line=None,
                    message=f"Root LICENSE.md does not reference {required_ref}.",
                    safer_form=f"Add an explicit reference to `{required_ref}` in root LICENSE.md.",
                )
            )

    return findings


def license_readme_boundary_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    readme = repo_root / "LICENSES" / "README.md"

    if not readme.exists():
        return findings

    text = read_text(readme)

    for boundary in REQUIRED_LICENSE_README_BOUNDARIES:
        if boundary not in text:
            findings.append(
                Finding(
                    id="VEC-LIC-BOUNDARY-001",
                    level=Level.LEVEL_5.value,
                    severity=Severity.WARNING.value,
                    rule_id="LICENSE-README-MISSING-BOUNDARY",
                    path="LICENSES/README.md",
                    line=None,
                    message=f"LICENSES/README.md is missing boundary statement: {boundary}",
                    safer_form=f"Add `{boundary}` to the Core Boundary section.",
                )
            )

    return findings


def deprecated_perimeter_label_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for rel in FILES_TO_SCAN:
        path = repo_root / rel
        if not path.exists() or not path.is_file():
            continue

        lines = read_text(path).splitlines()
        for index, line in enumerate(lines):
            for label in DEPRECATED_PERIMETER_LABELS:
                if re.search(rf"\b{re.escape(label)}\b", line):
                    if "deprecated" in line.lower() or "historical" in line.lower():
                        continue

                    findings.append(
                        Finding(
                            id="VEC-LIC-LEVEL-001",
                            level=Level.LEVEL_0.value,
                            severity=Severity.WARNING.value,
                            rule_id="DEPRECATED-PERIMETER-LABEL",
                            path=rel,
                            line=index + 1,
                            message=f"Deprecated perimeter label `{label}` found. Current model uses Level 0–5.",
                            safer_form="Replace P-labels with Level 0–5 terminology unless this is an explicitly historical note.",
                        )
                    )

    return findings


def authority_language_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in FORBIDDEN_AUTHORITY_PATTERNS]

    for rel in FILES_TO_SCAN:
        path = repo_root / rel
        if not path.exists() or not path.is_file():
            continue

        lines = read_text(path).splitlines()

        for index, line in enumerate(lines):
            for pattern in compiled:
                if not pattern.search(line):
                    continue

                if is_safe_context(lines, index):
                    continue

                findings.append(
                    Finding(
                        id="VEC-LIC-AUTH-001",
                        level=Level.LEVEL_5.value,
                        severity=Severity.BLOCKER.value,
                        rule_id="AUTHORITY-INFLATION-LANGUAGE",
                        path=rel,
                        line=index + 1,
                        message="Possible authority inflation language found in license or release-facing text.",
                        safer_form="Use repository-state wording: detects, exposes, records, refuses run. Do not claim truth, ontology, safety, certification, or deployment authority.",
                    )
                )

    return findings


def readme_license_block_guard(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    readme = repo_root / "README.md"

    if not readme.exists():
        return findings

    text = read_text(readme)

    if "## Licensing" not in text and "## License" not in text:
        findings.append(
            Finding(
                id="VEC-LIC-README-001",
                level=Level.LEVEL_0.value,
                severity=Severity.WARNING.value,
                rule_id="README-MISSING-LICENSING-BLOCK",
                path="README.md",
                line=None,
                message="README.md does not appear to contain a Licensing section.",
                safer_form="Add a short licensing section pointing to LICENSE.md and LICENSES/README.md.",
            )
        )
        return findings

    if "LICENSES/README.md" not in text:
        findings.append(
            Finding(
                id="VEC-LIC-README-002",
                level=Level.LEVEL_0.value,
                severity=Severity.WARNING.value,
                rule_id="README-MISSING-LICENSE-STACK-LINK",
                path="README.md",
                line=None,
                message="README.md Licensing section does not reference LICENSES/README.md.",
                safer_form="Add a link to `LICENSES/README.md` in the README licensing section.",
            )
        )

    return findings


def run_guards(repo_root: Path) -> list[Finding]:
    repo_root = repo_root.resolve()

    findings: list[Finding] = []
    findings.extend(required_files_guard(repo_root))
    findings.extend(root_license_links_guard(repo_root))
    findings.extend(license_readme_boundary_guard(repo_root))
    findings.extend(deprecated_perimeter_label_guard(repo_root))
    findings.extend(authority_language_guard(repo_root))
    findings.extend(readme_license_block_guard(repo_root))

    return sorted(
        findings,
        key=lambda f: (
            f.severity,
            f.path,
            f.line if f.line is not None else -1,
            f.rule_id,
            f.message,
        ),
    )


def has_blocker(findings: Iterable[Finding]) -> bool:
    return any(f.severity == Severity.BLOCKER.value for f in findings)


def format_text(findings: list[Finding]) -> str:
    if not findings:
        return "\n".join(
            [
                "PASS: No configured license-stack blocker was detected within the declared Level 0 / Level 5 perimeter.",
                "This is a repository-state check only.",
                "It does not prove truth, ontology, safety, deployment validity, or semantic correctness.",
            ]
        )

    lines = [
        "VECTAETOS™ License Stack Guard Report",
        "",
        "Boundary:",
        "  This report protects repository state only.",
        "  It does not define ontology, prove truth, validate safety, or authorize deployment.",
        "",
        f"Findings: {len(findings)}",
        "",
    ]

    for finding in findings:
        location = finding.path
        if finding.line is not None:
            location = f"{location}:{finding.line}"

        lines.extend(
            [
                f"[{finding.severity}] {finding.id} {finding.rule_id}",
                f"  level: {finding.level}",
                f"  path: {location}",
                f"  message: {finding.message}",
                f"  safer_form: {finding.safer_form}",
                f"  ontology_authority: {str(finding.ontology_authority).lower()}",
                f"  auto_fix_allowed: {str(finding.auto_fix_allowed).lower()}",
                "",
            ]
        )

    return "\n".join(lines).rstrip()


def format_json(findings: list[Finding]) -> str:
    payload = {
        "schema_version": "1.0",
        "guard": "license_stack_guard",
        "levels": [Level.LEVEL_0.value, Level.LEVEL_5.value],
        "summary": {
            "finding_count": len(findings),
            "blocker_count": sum(1 for f in findings if f.severity == Severity.BLOCKER.value),
            "error_count": sum(1 for f in findings if f.severity == Severity.ERROR.value),
            "warning_count": sum(1 for f in findings if f.severity == Severity.WARNING.value),
        },
        "authority_boundary": {
            "ontology_authority": False,
            "deployment_authority": False,
            "truth_authority": False,
        },
        "findings": [asdict(f) for f in findings],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS™ License Stack Guard — Level 0 / Level 5 repository-state check."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root. Default: current directory.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format. Default: text.")
    parser.add_argument("--report", type=Path, default=None, help="Optional path for JSON report.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 when BLOCKER findings are present.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        findings = run_guards(args.repo_root)

        if args.report is not None:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(format_json(findings) + "\n", encoding="utf-8")

        output = format_json(findings) if args.format == "json" else format_text(findings)
        print(output)

        if args.strict and has_blocker(findings):
            return 1

        return 0

    except KeyboardInterrupt:
        print("FAIL: guard interrupted; confidence unavailable.", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"FAIL: guard runtime error; confidence unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
  
