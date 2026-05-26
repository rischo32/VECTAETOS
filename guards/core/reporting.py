#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Reporting

Role:
    Deterministic report rendering and exit-code mapping for repository
    perimeter guards.

Boundary:
    Reports are repository-state diagnostics only.

    They do not define ontology, prove truth, validate safety, or authorize
    deployment.

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
    from guards.core.findings import (
        Finding,
        Severity,
        SEVERITY_ORDER,
        coerce_severity,
        finding_to_dict,
        schema_value,
    )
    from guards.core.perimeter import (
        SAFE_FAIL,
        SAFE_INFRA_FAIL,
        SAFE_PASS,
        contains_forbidden_report_claim,
    )
except ModuleNotFoundError:
    from findings import (  # type: ignore
        Finding,
        Severity,
        SEVERITY_ORDER,
        coerce_severity,
        finding_to_dict,
        schema_value,
    )
    from perimeter import (  # type: ignore
        SAFE_FAIL,
        SAFE_INFRA_FAIL,
        SAFE_PASS,
        contains_forbidden_report_claim,
    )


EXIT_OK = 0
EXIT_BLOCKER = 1
EXIT_INFRASTRUCTURE = 2
EXIT_INVALID_CONTRACT = 3
EXIT_USAGE = 4


def normalize_severity(value: Severity | str) -> Severity:
    return coerce_severity(value)


def assert_safe_report_fragment(value: str, *, field_name: str) -> None:
    """
    Reject report-control text that contains forbidden authority claims.

    This protects title/mode-like fields supplied by individual guards.
    Finding messages are still rendered as observations; they may quote unsafe
    source text through observed_pattern and must remain diagnostics.
    """

    if contains_forbidden_report_claim(value):
        raise ValueError(
            f"Report field {field_name!r} contains forbidden authoritative wording."
        )


def sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        list(findings),
        key=lambda item: (
            schema_value(item.level),
            str(item.path),
            item.line if item.line is not None else 0,
            item.column if item.column is not None else 0,
            str(item.guard_id),
            str(item.rule_id),
            str(item.id),
        ),
    )


def render_json(findings: Iterable[Finding]) -> str:
    data = [finding_to_dict(item) for item in sorted_findings(findings)]
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path | str, findings: Iterable[Finding]) -> None:
    """
    Write a deterministic JSON report.

    This is allowed only as an explicit report artifact write.
    It must not be used as auto-fix or repository mutation.
    """

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_json(findings), encoding="utf-8")


def severity_threshold(fail_on: Severity | str) -> int:
    return SEVERITY_ORDER[normalize_severity(fail_on)]


def has_findings_at_or_above(findings: Iterable[Finding], fail_on: Severity | str) -> bool:
    threshold = severity_threshold(fail_on)
    return any(SEVERITY_ORDER[normalize_severity(item.severity)] >= threshold for item in findings)


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
        severity = normalize_severity(finding.severity)
        counts[severity.value] += 1
    return counts


def finding_location(finding: Finding) -> str:
    location = str(finding.path)

    if finding.line is not None:
        location = f"{location}:{finding.line}"

    if finding.column is not None:
        location = f"{location}:{finding.column}"

    return location


def finding_vectors_label(finding: Finding) -> str:
    vectors = getattr(finding, "vectors", None) or (finding.vector,)
    return ",".join(str(schema_value(vector)) for vector in vectors)


def render_finding_text(finding: Finding) -> list[str]:
    lines: list[str] = []

    lines.append(f"[{finding.severity.value}] {finding.rule_id}")
    lines.append(f"  id:          {finding.id}")
    lines.append(f"  guard:       {finding.guard_id}")
    lines.append(f"  file:        {finding.guard_file}")
    lines.append(f"  path:        {finding_location(finding)}")
    lines.append(f"  level:       {finding.level.value}")
    lines.append(f"  scope:       {finding.scope.value}")
    lines.append(f"  vector:      {finding.vector.value}")
    lines.append(f"  vectors:     {finding_vectors_label(finding)}")
    lines.append(f"  evidence:    {finding.evidence_class_allowed.value}")
    lines.append(f"  enforcement: {finding.enforcement_mode.value}")
    lines.append(f"  integrity:   {finding.integrity_posture.value}")
    lines.append(f"  confidence:  {finding.confidence.value}")
    lines.append(f"  message:     {finding.message}")

    if finding.role:
        lines.append(f"  role:        {finding.role}")
    if finding.protected_object:
        lines.append(f"  protected:   {finding.protected_object}")
    if finding.observed_pattern:
        lines.append(f"  observed:    {finding.observed_pattern}")
    if finding.forbidden_conversion:
        lines.append(f"  conversion:  {finding.forbidden_conversion}")
    if finding.negated_context:
        lines.append("  context:     negated_context=true")
    if finding.anchor_ref:
        lines.append(f"  anchor_ref:  {finding.anchor_ref}")
    if finding.contract_ref:
        lines.append(f"  contract_ref:{finding.contract_ref}")
    if finding.safer_form:
        lines.append(f"  safer:       {finding.safer_form}")

    return lines


def render_text_report(
    findings: Iterable[Finding],
    *,
    title: str,
    mode: str,
    fail_on: Severity | str = Severity.BLOCKER,
    root: Path | str | None = None,
) -> str:
    assert_safe_report_fragment(title, field_name="title")
    assert_safe_report_fragment(mode, field_name="mode")

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
        lines.append("Repository-state result only.")
        lines.append("Not empirical validation.")
        lines.append("=" * 72)
        return "\n".join(lines) + "\n"

    for finding in ordered:
        lines.extend(render_finding_text(finding))
        lines.append("")

    if has_findings_at_or_above(ordered, threshold):
        lines.append(SAFE_FAIL)
    else:
        lines.append(SAFE_PASS)

    lines.append("This report does not define ontology.")
    lines.append("This report does not prove truth.")
    lines.append("This report does not validate safety.")
    lines.append("This report does not authorize deployment.")
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
    assert_safe_report_fragment(title, field_name="title")
    assert_safe_report_fragment(mode, field_name="mode")

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

    lines.append("## Findings")
    lines.append("")

    for finding in ordered:
        lines.append(f"### {finding.severity.value} — `{finding.rule_id}`")
        lines.append("")
        lines.append(f"- ID: `{finding.id}`")
        lines.append(f"- Guard: `{finding.guard_id}`")
        lines.append(f"- Path: `{finding_location(finding)}`")
        lines.append(f"- Level: `{finding.level.value}`")
        lines.append(f"- Scope: `{finding.scope.value}`")
        lines.append(f"- Vector: `{finding.vector.value}`")
        lines.append(f"- Evidence: `{finding.evidence_class_allowed.value}`")
        lines.append(f"- Enforcement: `{finding.enforcement_mode.value}`")
        lines.append(f"- Integrity: `{finding.integrity_posture.value}`")
        lines.append("")
        lines.append(finding.message)
        lines.append("")

        if finding.safer_form:
            lines.append(f"Safer form: {finding.safer_form}")
            lines.append("")

    if has_findings_at_or_above(ordered, threshold):
        lines.append(SAFE_FAIL)
    else:
        lines.append(SAFE_PASS)

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
    """
    Append a deterministic GitHub step summary.

    This is an explicit report artifact write, not an auto-fix.
    """

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


__all__ = [
    "SAFE_PASS",
    "SAFE_FAIL",
    "SAFE_INFRA_FAIL",
    "EXIT_OK",
    "EXIT_BLOCKER",
    "EXIT_INFRASTRUCTURE",
    "EXIT_INVALID_CONTRACT",
    "EXIT_USAGE",
    "normalize_severity",
    "assert_safe_report_fragment",
    "sorted_findings",
    "render_json",
    "write_json",
    "severity_threshold",
    "has_findings_at_or_above",
    "exit_code_for",
    "count_by_severity",
    "finding_location",
    "finding_vectors_label",
    "render_finding_text",
    "render_text_report",
    "print_text_report",
    "render_github_step_summary",
    "write_github_step_summary",
]
