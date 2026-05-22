#!/usr/bin/env python3
"""
VECTAETOS — Perimeter Guard Runner
==================================

Role:
    Deterministic manifest-driven runner for repository perimeter guards.

This runner:
    - reads guards/perimeter_manifest.json
    - expands explicit variables
    - executes active guard command templates in deterministic order
    - preserves stdout/stderr
    - writes optional JSON / Markdown reports
    - returns a consolidated exit code

This runner does not:
    - define ontology
    - interpret guard findings
    - suppress guard findings
    - modify repository content
    - retry guards automatically
    - decide which findings matter semantically

Python:
    3.11+

Exit codes:
    0 = all selected required guards OK
    1 = one or more selected required guards reported findings
    2 = execution/configuration error in one or more required guards
    3 = manifest/runner error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


RUNNER_NAME = "VECTAETOS Perimeter Guard Runner"
RUNNER_VERSION = "0.1.0"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GuardResult:
    guard_id: str
    name: str
    path: str
    active: bool
    required: bool
    selected: bool
    skipped: bool
    skip_reason: str
    command: list[str]
    status: str
    raw_exit_code: int | None
    mapped_exit_level: int
    duration_seconds: float
    stdout: str
    stderr: str


@dataclass(frozen=True)
class RunnerSummary:
    runner: str
    version: str
    profile: str
    root: str
    manifest: str
    started_at_utc: str
    finished_at_utc: str
    duration_seconds: float
    selected_guards: int
    executed_guards: int
    skipped_guards: int
    ok: int
    findings: int
    errors: int
    runner_exit_code: int
    results: list[GuardResult]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class RunnerError(Exception):
    """Manifest or runner-level error."""


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def utc_now_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"Manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"Manifest is not valid JSON: {path}: {exc}") from exc
    except OSError as exc:
        raise RunnerError(f"Cannot read manifest: {path}: {exc}") from exc


def ensure_repo_root(root: Path) -> Path:
    resolved = root.resolve()
    if not resolved.exists():
        raise RunnerError(f"Repository root does not exist: {resolved}")
    if not resolved.is_dir():
        raise RunnerError(f"Repository root is not a directory: {resolved}")
    return resolved


def normalize_guard_id(value: str) -> str:
    return value.strip()


def split_csv(values: Iterable[str] | None) -> set[str]:
    if not values:
        return set()
    out: set[str] = set()
    for item in values:
        for part in item.split(","):
            part = part.strip()
            if part:
                out.add(part)
    return out


def substitute_template(value: str, variables: dict[str, str]) -> str:
    """Substitute ${VAR} placeholders in a string using variables dict, then env."""
    out = value
    # One-pass replacement for explicit manifest style placeholders.
    for key, repl in variables.items():
        out = out.replace("${" + key + "}", repl)
    # Environment fallback for any remaining ${VAR}
    # No shell expansion is performed.
    import re

    pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return os.environ.get(key, match.group(0))

    return pattern.sub(replace, out)


def substitute_command(command: list[Any], variables: dict[str, str]) -> list[str]:
    return [substitute_template(str(part), variables) for part in command]


def has_unresolved_placeholders(command: list[str]) -> list[str]:
    unresolved: list[str] = []
    for part in command:
        if "${" in part and "}" in part:
            unresolved.append(part)
    return unresolved


def map_exit_code(raw_exit: int, exit_mapping: dict[str, str] | None) -> tuple[str, int]:
    """
    Convert a guard exit code to status and runner level.

    Level:
        0 ok
        1 finding
        2 error
    """
    if exit_mapping is None:
        exit_mapping = {"0": "ok", "1": "finding", "2": "error"}

    status = exit_mapping.get(str(raw_exit))
    if status is None:
        return "error", 2

    normalized = str(status).lower().strip()
    if normalized == "ok":
        return "ok", 0
    if normalized in {"finding", "findings", "policy_failure", "finding_or_policy_failure"}:
        return "finding", 1
    if normalized in {"error", "execution_error", "configuration_error"}:
        return "error", 2

    # Unknown mapping value is a manifest error class at guard result level.
    return "error", 2


def should_select_guard(
    guard: dict[str, Any],
    only: set[str],
    skip: set[str],
    include_inactive: bool,
) -> tuple[bool, bool, str]:
    guard_id = normalize_guard_id(str(guard.get("id", "")))
    name = str(guard.get("name", ""))
    active = bool(guard.get("active", True))

    if only and guard_id not in only and name not in only:
        return False, True, "not selected by --only"

    if guard_id in skip or name in skip:
        return False, True, "excluded by --skip"

    if not active and not include_inactive:
        return False, True, str(guard.get("reason_inactive", "inactive guard"))

    return True, False, ""


def guard_path_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def print_human_summary(summary: RunnerSummary, show_output: bool) -> None:
    print()
    print("=" * 72)
    print(f"{RUNNER_NAME} v{RUNNER_VERSION}")
    print("=" * 72)
    print(f"Profile:          {summary.profile}")
    print(f"Root:             {summary.root}")
    print(f"Manifest:         {summary.manifest}")
    print(f"Selected guards:  {summary.selected_guards}")
    print(f"Executed guards:  {summary.executed_guards}")
    print(f"Skipped guards:   {summary.skipped_guards}")
    print(f"OK:               {summary.ok}")
    print(f"Findings:         {summary.findings}")
    print(f"Errors:           {summary.errors}")
    print(f"Exit:             {summary.runner_exit_code}")
    print("=" * 72)

    for result in summary.results:
        if result.skipped:
            marker = "SKIP"
        elif result.status == "ok":
            marker = "OK"
        elif result.status == "finding":
            marker = "FINDING"
        else:
            marker = "ERROR"

        print(f"[{marker}] {result.guard_id} {result.name}")
        if result.skipped:
            print(f"  reason: {result.skip_reason}")
        else:
            print(f"  exit:   {result.raw_exit_code}")
            print(f"  time:   {result.duration_seconds:.3f}s")
            print(f"  cmd:    {shlex.join(result.command)}")

        if show_output and not result.skipped:
            if result.stdout:
                print("  stdout:")
                print(indent_block(result.stdout, "    "))
            if result.stderr:
                print("  stderr:")
                print(indent_block(result.stderr, "    "))

    print("=" * 72)


def indent_block(text: str, prefix: str) -> str:
    return "\n".join(prefix + line for line in text.rstrip("\n").splitlines())


def summary_to_json(summary: RunnerSummary) -> dict[str, Any]:
    data = asdict(summary)
    data["results"] = [asdict(item) for item in summary.results]
    return data


def write_json_report(path: Path, summary: RunnerSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary_to_json(summary), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_markdown_report(path: Path, summary: RunnerSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# VECTAETOS — Perimeter Guard Report")
    lines.append("")
    lines.append(f"- Runner: `{summary.runner}`")
    lines.append(f"- Version: `{summary.version}`")
    lines.append(f"- Profile: `{summary.profile}`")
    lines.append(f"- Root: `{summary.root}`")
    lines.append(f"- Manifest: `{summary.manifest}`")
    lines.append(f"- Started UTC: `{summary.started_at_utc}`")
    lines.append(f"- Finished UTC: `{summary.finished_at_utc}`")
    lines.append(f"- Duration: `{summary.duration_seconds:.3f}s`")
    lines.append(f"- Exit: `{summary.runner_exit_code}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Selected | Executed | Skipped | OK | Findings | Errors |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    lines.append(
        f"| {summary.selected_guards} | {summary.executed_guards} | {summary.skipped_guards} | "
        f"{summary.ok} | {summary.findings} | {summary.errors} |"
    )
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Guard | Status | Exit | Required | Duration |")
    lines.append("|---|---|---:|---:|---:|")
    for result in summary.results:
        status = "SKIPPED" if result.skipped else result.status.upper()
        raw = "" if result.raw_exit_code is None else str(result.raw_exit_code)
        lines.append(
            f"| `{result.guard_id} {result.name}` | `{status}` | {raw} | "
            f"{str(result.required).lower()} | {result.duration_seconds:.3f}s |"
        )
    lines.append("")
    lines.append("## Commands")
    lines.append("")
    for result in summary.results:
        lines.append(f"### {result.guard_id} — {result.name}")
        lines.append("")
        if result.skipped:
            lines.append(f"Skipped: `{result.skip_reason}`")
            lines.append("")
            continue
        lines.append("```bash")
        lines.append(shlex.join(result.command))
        lines.append("```")
        lines.append("")
        if result.stdout:
            lines.append("<details><summary>stdout</summary>")
            lines.append("")
            lines.append("```text")
            lines.append(result.stdout.rstrip("\n"))
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")
        if result.stderr:
            lines.append("<details><summary>stderr</summary>")
            lines.append("")
            lines.append("```text")
            lines.append(result.stderr.rstrip("\n"))
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------


def build_variables(
    manifest: dict[str, Any],
    root: Path,
    base_sha: str | None,
    head_sha: str | None,
    python_bin: str | None,
) -> dict[str, str]:
    raw = manifest.get("variables", {})
    if not isinstance(raw, dict):
        raise RunnerError("manifest.variables must be an object")

    variables: dict[str, str] = {}
    for key, value in raw.items():
        variables[str(key)] = str(value)

    variables["ROOT"] = str(root)

    if python_bin:
        variables["PYTHON"] = python_bin

    # CLI > environment > manifest literal
    base = base_sha or os.environ.get("BASE_SHA") or os.environ.get("GITHUB_BASE_SHA")
    head = head_sha or os.environ.get("HEAD_SHA") or os.environ.get("GITHUB_SHA")

    if base:
        variables["BASE_SHA"] = base
    if head:
        variables["HEAD_SHA"] = head

    # Expand variables that reference other variables once.
    for key, value in list(variables.items()):
        variables[key] = substitute_template(value, variables)

    return variables


def validate_manifest(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest.get("guards"), list):
        raise RunnerError("manifest.guards must be a list")
    if "execution_order" in manifest and not isinstance(manifest["execution_order"], list):
        raise RunnerError("manifest.execution_order must be a list when present")

    ids: set[str] = set()
    for idx, guard in enumerate(manifest["guards"]):
        if not isinstance(guard, dict):
            raise RunnerError(f"manifest.guards[{idx}] must be an object")

        guard_id = guard.get("id")
        name = guard.get("name")
        path = guard.get("path")

        if not guard_id:
            raise RunnerError(f"manifest.guards[{idx}] missing id")
        if not name:
            raise RunnerError(f"manifest.guards[{idx}] missing name")
        if not path:
            raise RunnerError(f"manifest.guards[{idx}] missing path")

        guard_id_s = str(guard_id)
        if guard_id_s in ids:
            raise RunnerError(f"Duplicate guard id: {guard_id_s}")
        ids.add(guard_id_s)

        templates = guard.get("command_templates")
        if not isinstance(templates, dict):
            raise RunnerError(f"{guard_id_s} missing command_templates object")


def order_guards(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    guards = manifest["guards"]
    by_id = {str(item["id"]): item for item in guards}

    order = manifest.get("execution_order")
    if not order:
        return guards

    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()

    for guard_id in order:
        guard_id_s = str(guard_id)
        guard = by_id.get(guard_id_s)
        if guard is None:
            raise RunnerError(f"execution_order references unknown guard: {guard_id_s}")
        ordered.append(guard)
        seen.add(guard_id_s)

    # Append guards not in explicit order deterministically by id.
    for guard in sorted(guards, key=lambda item: str(item.get("id", ""))):
        guard_id_s = str(guard["id"])
        if guard_id_s not in seen:
            ordered.append(guard)

    return ordered


def run_guard(
    guard: dict[str, Any],
    profile: str,
    root: Path,
    variables: dict[str, str],
    timeout_seconds: int,
    dry_run: bool,
) -> GuardResult:
    guard_id = str(guard["id"])
    name = str(guard["name"])
    rel_path = str(guard["path"])
    active = bool(guard.get("active", True))
    required = bool(guard.get("required", True))

    if not active:
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=True,
            skip_reason=str(guard.get("reason_inactive", "inactive guard")),
            command=[],
            status="skipped",
            raw_exit_code=None,
            mapped_exit_level=0,
            duration_seconds=0.0,
            stdout="",
            stderr="",
        )

    if not guard_path_exists(root, rel_path):
        status = "error" if required else "skipped"
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=not required,
            skip_reason=f"guard file not found: {rel_path}",
            command=[],
            status=status,
            raw_exit_code=2 if required else None,
            mapped_exit_level=2 if required else 0,
            duration_seconds=0.0,
            stdout="",
            stderr=f"guard file not found: {rel_path}" if required else "",
        )

    templates = guard.get("command_templates", {})
    template = templates.get(profile)
    if not template:
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=[],
            status="error",
            raw_exit_code=2,
            mapped_exit_level=2,
            duration_seconds=0.0,
            stdout="",
            stderr=f"missing command template for profile: {profile}",
        )

    if not isinstance(template, list):
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=[],
            status="error",
            raw_exit_code=2,
            mapped_exit_level=2,
            duration_seconds=0.0,
            stdout="",
            stderr=f"command template for {profile} must be a list",
        )

    command = substitute_command(template, variables)
    unresolved = has_unresolved_placeholders(command)
    if unresolved:
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=command,
            status="error",
            raw_exit_code=2,
            mapped_exit_level=2,
            duration_seconds=0.0,
            stdout="",
            stderr="unresolved placeholders: " + ", ".join(unresolved),
        )

    if dry_run:
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=command,
            status="ok",
            raw_exit_code=0,
            mapped_exit_level=0,
            duration_seconds=0.0,
            stdout="DRY RUN: command not executed\n",
            stderr="",
        )

    started = time.perf_counter()
    try:
        proc = subprocess.run(
            command,
            cwd=str(root),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration = time.perf_counter() - started
        status, level = map_exit_code(proc.returncode, guard.get("exit_mapping"))
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=command,
            status=status,
            raw_exit_code=proc.returncode,
            mapped_exit_level=level,
            duration_seconds=duration,
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - started
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        stderr = (stderr + "\n" if stderr else "") + f"timeout after {timeout_seconds}s"
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=command,
            status="error",
            raw_exit_code=2,
            mapped_exit_level=2,
            duration_seconds=duration,
            stdout=stdout,
            stderr=stderr,
        )
    except OSError as exc:
        duration = time.perf_counter() - started
        return GuardResult(
            guard_id=guard_id,
            name=name,
            path=rel_path,
            active=active,
            required=required,
            selected=True,
            skipped=False,
            skip_reason="",
            command=command,
            status="error",
            raw_exit_code=2,
            mapped_exit_level=2,
            duration_seconds=duration,
            stdout="",
            stderr=f"execution failed: {exc}",
        )


def compute_runner_exit(
    results: list[GuardResult],
    profile: str,
    strict_exit: bool,
) -> int:
    required_results = [item for item in results if item.required and not item.skipped]

    has_error = any(item.mapped_exit_level >= 2 for item in required_results)
    has_finding = any(item.mapped_exit_level == 1 for item in required_results)

    if has_error:
        return 2
    if has_finding:
        # In report mode, default is visibility without blocking unless strict exit is requested.
        if profile == "report" and not strict_exit:
            return 0
        return 1
    return 0


def build_summary(
    profile: str,
    root: Path,
    manifest_path: Path,
    started_at: str,
    started_perf: float,
    results: list[GuardResult],
    runner_exit: int,
) -> RunnerSummary:
    finished = utc_now_iso()
    duration = time.perf_counter() - started_perf

    selected = [item for item in results if item.selected]
    executed = [item for item in selected if not item.skipped]
    skipped = [item for item in selected if item.skipped]

    ok = sum(1 for item in executed if item.status == "ok")
    findings = sum(1 for item in executed if item.status == "finding")
    errors = sum(1 for item in executed if item.status == "error")

    return RunnerSummary(
        runner=RUNNER_NAME,
        version=RUNNER_VERSION,
        profile=profile,
        root=str(root),
        manifest=str(manifest_path),
        started_at_utc=started_at,
        finished_at_utc=finished,
        duration_seconds=duration,
        selected_guards=len(selected),
        executed_guards=len(executed),
        skipped_guards=len(skipped),
        ok=ok,
        findings=findings,
        errors=errors,
        runner_exit_code=runner_exit,
        results=results,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run VECTAETOS perimeter guards from guards/perimeter_manifest.json.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument(
        "--manifest",
        default="guards/perimeter_manifest.json",
        help="Path to perimeter manifest, relative to root unless absolute.",
    )
    parser.add_argument(
        "--profile",
        choices=["report", "ci"],
        default="report",
        help="Execution profile.",
    )
    parser.add_argument(
        "--only",
        action="append",
        help="Comma-separated guard IDs or names to run. May be repeated.",
    )
    parser.add_argument(
        "--skip",
        action="append",
        help="Comma-separated guard IDs or names to skip. May be repeated.",
    )
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include inactive planned guards.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print/report commands without executing them.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List guards and exit.",
    )
    parser.add_argument(
        "--base",
        dest="base_sha",
        help="Base SHA for diff-based guards.",
    )
    parser.add_argument(
        "--head",
        dest="head_sha",
        help="Head SHA for diff-based guards.",
    )
    parser.add_argument(
        "--python",
        dest="python_bin",
        default=None,
        help="Python executable used for guard commands.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout per guard in seconds.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional JSON report path.",
    )
    parser.add_argument(
        "--md-out",
        default=None,
        help="Optional Markdown report path.",
    )
    parser.add_argument(
        "--show-output",
        action="store_true",
        help="Print guard stdout/stderr in terminal summary.",
    )
    parser.add_argument(
        "--strict-exit",
        action="store_true",
        help="In report profile, return nonzero on findings.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop after the first required guard with finding/error.",
    )
    return parser.parse_args(argv)


def list_guards(manifest: dict[str, Any]) -> None:
    print("ID        ACTIVE  REQUIRED  LEVEL  NAME")
    print("-" * 72)
    for guard in order_guards(manifest):
        print(
            f"{str(guard.get('id', '')):<9} "
            f"{str(bool(guard.get('active', True))).lower():<7} "
            f"{str(bool(guard.get('required', True))).lower():<9} "
            f"{str(guard.get('level', '')):<6} "
            f"{guard.get('name', '')}"
        )


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    started_at = utc_now_iso()
    started_perf = time.perf_counter()

    try:
        root = ensure_repo_root(Path(args.root))
        manifest_path = Path(args.manifest)
        if not manifest_path.is_absolute():
            manifest_path = root / manifest_path
        manifest_path = manifest_path.resolve()

        manifest = load_json(manifest_path)
        validate_manifest(manifest)

        if args.list:
            list_guards(manifest)
            return 0

        variables = build_variables(
            manifest=manifest,
            root=root,
            base_sha=args.base_sha,
            head_sha=args.head_sha,
            python_bin=args.python_bin,
        )

        only = split_csv(args.only)
        skip = split_csv(args.skip)

        results: list[GuardResult] = []
        for guard in order_guards(manifest):
            selected, skipped, reason = should_select_guard(
                guard=guard,
                only=only,
                skip=skip,
                include_inactive=args.include_inactive,
            )

            if not selected:
                results.append(
                    GuardResult(
                        guard_id=str(guard.get("id", "")),
                        name=str(guard.get("name", "")),
                        path=str(guard.get("path", "")),
                        active=bool(guard.get("active", True)),
                        required=bool(guard.get("required", True)),
                        selected=True,
                        skipped=True,
                        skip_reason=reason,
                        command=[],
                        status="skipped",
                        raw_exit_code=None,
                        mapped_exit_level=0,
                        duration_seconds=0.0,
                        stdout="",
                        stderr="",
                    )
                )
                continue

            result = run_guard(
                guard=guard,
                profile=args.profile,
                root=root,
                variables=variables,
                timeout_seconds=args.timeout,
                dry_run=args.dry_run,
            )
            results.append(result)

            if args.fail_fast and result.required and result.mapped_exit_level > 0:
                break

        runner_exit = compute_runner_exit(
            results=results,
            profile=args.profile,
            strict_exit=args.strict_exit,
        )
        summary = build_summary(
            profile=args.profile,
            root=root,
            manifest_path=manifest_path,
            started_at=started_at,
            started_perf=started_perf,
            results=results,
            runner_exit=runner_exit,
        )

        if args.json_out:
            write_json_report(Path(args.json_out), summary)
        if args.md_out:
            write_markdown_report(Path(args.md_out), summary)

        print_human_summary(summary, show_output=args.show_output)

        return runner_exit

    except RunnerError as exc:
        print(f"RUNNER ERROR: {exc}", file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        print("RUNNER ERROR: interrupted", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
