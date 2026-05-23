#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Reporting

Role:
    Deterministic report rendering and exit-code mapping for repository
    perimeter guards.

Boundary:
    Reports are repository-state diagnostics only.
    They do not define ontology, prove truth, validate safety, or authorize deployment.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TextIO

try:
    from guards.core.findings import Finding, Severity, finding_to_dict, SEVERITY_ORDER
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from findings import Finding, Severity, finding_to_dict, SEVERITY_ORDER  # type: ignore


SAFE_PASS = "PASS: No configured blocker was detected within the declared perimeter."
SAFE_FAIL = "FAIL: Configured blocker detected within declared repository perimeter."
INFRA_FAIL = "FAIL: Guard infrastructure error; confidence unavailable."

EXIT_OK = 0
EXIT_BLOCKER = 1
EXIT_INFRASTRUCTURE = 2
EXIT_INVALID_CONTRACT = 3
EXIT_USAGE = 4


def normalize_severity(value: Severity | str) -> Severity:
    if isinstance(value, Severity):
        return value
    return Severity(str(value))


def sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        list(findings),
        key=lambda item: (
            str(item.path),
            item.line if item.line is not None else 0,
            str(item.guard_id),
            str(item.rule_id),
            str(item.id),
        ),
    )


def render_json(findings: Iterable[Finding]) -> str:
    data = [finding_to_dict(item) for item in sorted_findings(findings)]
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path | str, findings: Iterable[Finding]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_json(findings), encoding="utf-8")


def severity_threshold(fail_on: Severity | str) -> int:
    return SEVERITY_ORDER[normalize_severity(fail_on)]


def has_findings_at_or_above(findings: Iterable[Finding], fail_on: Severity | str) -> bool:
    threshold = severity_threshold(fail_on)
    return any(SEVERITY_ORDER[item.severity] >= threshold for item in findings)


def exit_code_for(
    findings: Sequence[Finding],
    *,
    fail_on: Severity | str = Severity.BLOCKER,
    infrastructure_error: bool = False,
    invalid_contract: bool = False,
    usage_error: bool = False,
) -> int:
    if usage_error:
        return EXIT_USAGE
    if invalid_contract:
        return EXIT_INVALID_CONTRACT
    if infrastructure_error:
        return EXIT_INFRASTRUCTURE
    if has_findings_at_or_above(findings, fail_on):
        return EXIT_BLOCKER
    return EXIT_OK


def count_by_severity(findings: Iterable[Finding]) -> dict[str, int]:
    counts = {severity.value: 0 for severity in Severity}
    for finding in findings:
        counts[finding.severity.value] += 1
    return counts


def render_text_report(
    findings: Iterable[Finding],
    *,
    title: str,
    mode: str,
    fail_on: Severity | str = Severity.BLOCKER,
    root: Path | str | None = None,
) -> str:
    ordered = sorted_findings(findings)
    counts = count_by_severity(ordered)
    threshold = normalize_severity(fail_on)

    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(title)
    lines.append("=" * 72)
    if root is not None:
        lines.append(f"Root:              {root}")
    lines.append(f"Mode:              {mode}")
    lines.append(f"Fail on:           {threshold.value}")
    lines.append(f"Findings:          {len(ordered)}")
    lines.append(f"INFO:              {counts[Severity.INFO.value]}")
    lines.append(f"WARN:              {counts[Severity.WARN.value]}")
    lines.append(f"HARD:              {counts[Severity.HARD.value]}")
    lines.append(f"BLOCKER:           {counts[Severity.BLOCKER.value]}")
    lines.append("-" * 72)

    if not ordered:
        lines.append(SAFE_PASS)
        lines.append("This is a repository-state result, not empirical validation.")
        lines.append("=" * 72)
        return "\n".join(lines) + "\n"

    for finding in ordered:
        location = str(finding.path)
        if finding.line is not None:
            location = f"{location}:{finding.line}"

        lines.append(f"[{finding.severity.value}] {finding.rule_id}")
        lines.append(f"  id:        {finding.id}")
        lines.append(f"  guard:     {finding.guard_id}")
        lines.append(f"  path:      {location}")
        lines.append(f"  scope:     {finding.scope.value}")
        lines.append(f"  vector:    {finding.vector.value}")
        lines.append(f"  evidence:  {finding.evidence_class_allowed.value if finding.evidence_class_allowed else 'not_declared'}")
        lines.append(f"  message:   {finding.message}")

        if finding.protected_object:
            lines.append(f"  protected: {finding.protected_object}")
        if finding.observed_pattern:
            lines.append(f"  observed:  {finding.observed_pattern}")
        if finding.forbidden_conversion:
            lines.append(f"  conversion:{finding.forbidden_conversion}")
        if finding.negated_context:
            lines.append("  context:   negated_context=true")
        if finding.safer_form:
            lines.append(f"  safer:     {finding.safer_form}")

        lines.append("")

    if has_findings_at_or_above(ordered, threshold):
        lines.append(SAFE_FAIL)
    else:
        lines.append("PASS: Static scan produced no findings at or above the configured enforcement level.")

    lines.append("This report does not define ontology, prove truth, validate safety, or authorize deployment.")
    lines.append("=" * 72)
    return "\n".join(lines) + "\n"


def print_text_report(
    findings: Iterable[Finding],
    *,
    title: str,
    mode: str,
    fail_on: Severity | str = Severity.BLOCKER,
    root: Path | str | None = None,
    file: TextIO = sys.stdout,
) -> None:
    file.write(
        render_text_report(
            findings,
            title=title,
            mode=mode,
            fail_on=fail_on,
            root=root,
        )
    )


def render_github_step_summary(
    findings: Iterable[Finding],
    *,
    title: str,
    mode: str,
    fail_on: Severity | str = Severity.BLOCKER,
) -> str:
    ordered = sorted_findings(findings)
    counts = count_by_severity(ordered)
    threshold = normalize_severity(fail_on)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Mode: `{mode}`")
    lines.append(f"- Fail on: `{threshold.value}`")
    lines.append(f"- Findings: `{len(ordered)}`")
    lines.append(f"- INFO: `{counts[Severity.INFO.value]}`")
    lines.append(f"- WARN: `{counts[Severity.WARN.value]}`")
    lines.append(f"- HARD: `{counts[Severity.HARD.value]}`")
    lines.append(f"- BLOCKER: `{counts[Severity.BLOCKER.value]}`")
    lines.append("")

    if not ordered:
        lines.append(SAFE_PASS)
        lines.append("")
        lines.append("_Repository-state result only. Not empirical validation._")
        return "\n".join(lines) + "\n"

    lines.append("| Severity | Rule | Path | Message |")
    lines.append("|---|---|---|---|")
    for finding in ordered:
        location = str(finding.path)
        if finding.line is not None:
            location = f"{location}:{finding.line}"
        message = finding.message.replace("|", "\\|")
        lines.append(
            f"| {finding.severity.value} | `{finding.rule_id}` | `{location}` | {message} |"
        )

    lines.append("")
    if has_findings_at_or_above(ordered, threshold):
        lines.append(SAFE_FAIL)
    else:
        lines.append("PASS: Static scan produced no findings at or above the configured enforcement level.")
    lines.append("")
    lines.append("_This report does not define ontology, prove truth, validate safety, or authorize deployment._")
    return "\n".join(lines) + "\n"


def write_github_step_summary(
    path: Path | str,
    findings: Iterable[Finding],
    *,
    title: str,
    mode: str,
    fail_on: Severity | str = Severity.BLOCKER,
) -> None:
    target = Path(path)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(
            render_github_step_summary(
                findings,
                title=title,
                mode=mode,
                fail_on=fail_on,
            )
        )
