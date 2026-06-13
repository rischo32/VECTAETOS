#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTAETOS :: MINIMAL PROTECTED SURFACE GUARD

Role:
    Minimal repository protected-surface guard for the first PIS layer.

Purpose:
    Detect changes to a narrow protected surface unless an explicit
    solo-maintainer unlock record covers those paths.

Boundary:
    This guard does not define ontology, prove truth, validate safety,
    authorize deployment, mutate files, auto-fix text, or create feedback into Phi.

Minimal protected surface:
    anchors/**
    formal/**
    contracts/**
    guards/core/**

Current manifest:
    research/pis/protected_surface_manifest.minimal.json

Python:
    3.11+

Dependencies:
    standard library only + guards.core shared kernel
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _bootstrap_repo_import_path() -> Path:
    cwd = Path.cwd().resolve()
    script_path = Path(__file__).resolve()

    candidates = [
        cwd,
        cwd.parent,
        script_path.parent.parent,
        script_path.parent,
    ]

    for candidate in candidates:
        if (candidate / "guards" / "core" / "findings.py").is_file():
            candidate_str = str(candidate)
            if candidate_str in sys.path:
                sys.path.remove(candidate_str)
            sys.path.insert(0, candidate_str)
            return candidate

    return cwd


REPO_ROOT = _bootstrap_repo_import_path()

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
except ModuleNotFoundError as exc:
    print("::error title=PIS-GUARD-IMPORT-ERROR::Cannot import guards.core shared kernel.")
    print("")
    print("PIS-GUARD-IMPORT-ERROR")
    print(str(exc))
    print("")
    print(f"cwd: {Path.cwd()}")
    print(f"script: {Path(__file__).resolve()}")
    print(f"repo_root_candidate: {REPO_ROOT}")
    print("")
    print("Fail-closed: shared guard kernel is unavailable.")
    raise SystemExit(2)


GUARD_ID = "GUARD-PIS-01"
GUARD_FILE = "guards/protected_surface_guard.py"
GUARD_NAME = "Minimal Protected Surface Guard"
VERSION = "0.1.1-pinned-minimal-globs"
CONTRACT_SCHEMA_VERSION = "0.1"

DEFAULT_MANIFEST_PATH = "research/pis/protected_surface_manifest.minimal.json"
NULL_SHA = "0000000000000000000000000000000000000000"

DEFAULT_REQUIRED_SIGNED_BY = "Richard Fonfara"
DEFAULT_REQUIRED_CONFIRMATION = "I confirm solo-maintainer protected-surface unlock."

REQUIRED_MINIMAL_PROTECTED_GLOBS: tuple[str, ...] = (
    "anchors/**",
    "formal/**",
    "contracts/**",
    "guards/core/**",
)

# Research PIS files are intentionally not part of the active protected surface
# yet, but the manifest is still shape-checked against the pinned baseline above.
RESEARCH_PROFILE_EXCLUDED_GLOBS: tuple[str, ...] = (
    "research/pis/**",
    "tests/fixtures/**",
    "docs/archive/**",
)

GLOB_META_CHARS = frozenset("*?[]")


class ChangedPath:
    __slots__ = ("status", "paths")

    def __init__(self, status: str, paths: tuple[str, ...]) -> None:
        self.status = status
        self.paths = paths


class UnlockRecord:
    __slots__ = ("path", "data")

    def __init__(self, path: str, data: dict[str, Any]) -> None:
        self.path = path
        self.data = data


def normalize_path(path: str | Path) -> str:
    value = str(path).strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def is_null_sha(value: str | None) -> bool:
    return value is None or value.strip() == "" or value.strip() == NULL_SHA


def run_git(args: list[str], *, allow_fail: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
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

        if status.startswith(("R", "C")) and len(parts) >= 3:
            changes.append(
                ChangedPath(
                    status=status,
                    paths=(normalize_path(parts[1]), normalize_path(parts[2])),
                )
            )
        elif len(parts) >= 2:
            changes.append(ChangedPath(status=status, paths=(normalize_path(parts[1]),)))

    return changes


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Manifest file missing: {normalize_path(path)}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {normalize_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"JSON root must be an object: {normalize_path(path)}")

    return data


def path_matches_glob(path: str, glob_pattern: str) -> bool:
    normalized_path = normalize_path(path)
    normalized_glob = normalize_path(glob_pattern)

    if fnmatch.fnmatchcase(normalized_path, normalized_glob):
        return True

    if normalized_glob.endswith("/**"):
        prefix = normalized_glob[:-3]
        return normalized_path == prefix or normalized_path.startswith(prefix + "/")

    return False


def path_in_patterns(path: str, patterns: list[str] | tuple[str, ...]) -> bool:
    return any(path_matches_glob(path, pattern) for pattern in patterns)


def contains_glob_meta(path: str) -> bool:
    return any(char in path for char in GLOB_META_CHARS)


def protected_vector_for_path(path: str) -> DriftVector:
    repo_path = normalize_path(path)

    if repo_path.startswith("contracts/"):
        return DriftVector.V7_CONTRACT_DRIFT
    if repo_path.startswith("guards/core/"):
        return DriftVector.V15_GUARD_RUNTIME_INTEGRITY
    if repo_path.startswith(("anchors/", "formal/")):
        return DriftVector.V14_ANCHOR_INTEGRITY_DRIFT

    return DriftVector.V6_PATH_STATUS_LAUNDERING


def protected_object_for_path(path: str) -> str:
    repo_path = normalize_path(path)

    if repo_path.startswith("anchors/"):
        return "anchors"
    if repo_path.startswith("formal/"):
        return "formal"
    if repo_path.startswith("contracts/"):
        return "contracts"
    if repo_path.startswith("guards/core/"):
        return "guards/core"

    return "protected_surface"


def changed_paths(changes: list[ChangedPath]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for change in changes:
        for path in change.paths:
            entries.append((path, change.status))
    return entries


def protected_changed_paths(
    changes: list[ChangedPath],
    *,
    protected_paths: list[str],
    protected_globs: list[str],
    excluded_globs: list[str],
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []

    normalized_protected_paths = {normalize_path(path) for path in protected_paths}
    normalized_protected_globs = [normalize_path(item) for item in protected_globs]
    normalized_excluded_globs = [normalize_path(item) for item in excluded_globs]

    for path, status in changed_paths(changes):
        repo_path = normalize_path(path)

        # Pinned baseline is evaluated before manifest-provided exclusions.
        # A PR must not be able to weaken the minimal PIS surface by editing
        # research/pis/protected_surface_manifest.minimal.json.
        if path_in_patterns(repo_path, REQUIRED_MINIMAL_PROTECTED_GLOBS):
            result.append((repo_path, status))
            continue

        if path_in_patterns(repo_path, normalized_excluded_globs):
            continue

        if repo_path in normalized_protected_paths or path_in_patterns(
            repo_path,
            normalized_protected_globs,
        ):
            result.append((repo_path, status))

    return sorted(set(result), key=lambda item: (item[0], item[1]))


def load_unlock_records(glob_pattern: str) -> tuple[list[UnlockRecord], list[str]]:
    normalized_glob = normalize_path(glob_pattern)
    root = Path.cwd()

    records: list[UnlockRecord] = []
    errors: list[str] = []

    for path in sorted(root.glob(normalized_glob)):
        if not path.is_file():
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{normalize_path(path)}: invalid JSON: {exc}")
            continue
        except OSError as exc:
            errors.append(f"{normalize_path(path)}: unreadable unlock record: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{normalize_path(path)}: unlock root must be an object")
            continue

        records.append(UnlockRecord(normalize_path(path), data))

    return records, errors


def parse_expiry(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None

    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)

    return parsed.astimezone(UTC)


def validate_unlock_record(
    record: UnlockRecord,
    *,
    required_signed_by: str,
    required_confirmation: str,
) -> list[str]:
    data = record.data
    errors: list[str] = []

    if data.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        errors.append("schema_version mismatch")

    if data.get("mode") != "solo_maintainer":
        errors.append("mode must be solo_maintainer")

    if not isinstance(data.get("paths_allowed"), list) or not all(
        isinstance(item, str) and item.strip() for item in data.get("paths_allowed", [])
    ):
        errors.append("paths_allowed must be a non-empty string list")
    else:
        for item in data["paths_allowed"]:
            normalized_item = normalize_path(item)
            if contains_glob_meta(normalized_item):
                errors.append(
                    f"paths_allowed entry must be an exact path, not a glob: {normalized_item}"
                )

    if not isinstance(data.get("reason"), str) or not data["reason"].strip():
        errors.append("reason is required")

    if data.get("signed_by") != required_signed_by:
        errors.append("signed_by does not match required maintainer")

    if data.get("confirmation") != required_confirmation:
        errors.append("confirmation phrase does not match exactly")

    if data.get("ontology_authority") is not False:
        errors.append("ontology_authority must be false")

    if data.get("auto_fix_allowed") is not False:
        errors.append("auto_fix_allowed must be false")

    expiry = parse_expiry(data.get("expires_utc"))
    if expiry is None:
        errors.append("expires_utc must be a valid ISO UTC timestamp")
    elif expiry < datetime.now(UTC):
        errors.append("unlock record is expired")

    ai_review = data.get("ai_review")
    if ai_review is not None:
        if not isinstance(ai_review, dict):
            errors.append("ai_review must be an object when present")
        elif ai_review.get("advisory_only") is not True:
            errors.append("ai_review.advisory_only must be true")

    return errors


def unlock_covers_path(record: UnlockRecord, path: str) -> bool:
    allowed = record.data.get("paths_allowed", [])
    if not isinstance(allowed, list):
        return False

    repo_path = normalize_path(path)
    for item in allowed:
        if not isinstance(item, str):
            continue

        allowed_path = normalize_path(item)
        if contains_glob_meta(allowed_path):
            continue

        if repo_path == allowed_path:
            return True

    return False


def find_covering_unlocks(
    records: list[UnlockRecord],
    path: str,
    *,
    required_signed_by: str,
    required_confirmation: str,
) -> tuple[list[UnlockRecord], list[str]]:
    covering: list[UnlockRecord] = []
    invalid_messages: list[str] = []

    for record in records:
        if not unlock_covers_path(record, path):
            continue

        errors = validate_unlock_record(
            record,
            required_signed_by=required_signed_by,
            required_confirmation=required_confirmation,
        )
        if errors:
            invalid_messages.append(f"{record.path}: " + "; ".join(errors))
            continue

        covering.append(record)

    return covering, invalid_messages


def pis_finding(
    *,
    rule_id: str,
    path: str | Path,
    message: str,
    severity: Severity = Severity.BLOCKER,
    confidence: Confidence = Confidence.HIGH,
    observed_pattern: str | None = None,
    protected_object: str | None = None,
    vector: DriftVector = DriftVector.V6_PATH_STATUS_LAUNDERING,
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
        message=message,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.FAIL_CLOSED,
        integrity_posture=IntegrityPosture.PATH_POLICY_READ_ONLY,
        anchor_ref="research/pis/PIS_MINIMAL_APPLIED_PROFILE.md",
        contract_ref=DEFAULT_MANIFEST_PATH,
        safer_form=safer_form,
    )


def validate_manifest_shape(manifest: dict[str, Any], manifest_path: str) -> list[Finding]:
    findings: list[Finding] = []

    def add(rule_id: str, message: str) -> None:
        findings.append(
            pis_finding(
                rule_id=rule_id,
                path=manifest_path,
                message=message,
                protected_object="protected_surface_manifest",
                observed_pattern=manifest_path,
                vector=DriftVector.V7_CONTRACT_DRIFT,
                severity=Severity.BLOCKER,
                safer_form="Keep the minimal PIS manifest explicit, non-authoritative, and fail-closed.",
            )
        )

    if manifest.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        add(
            "PIS-MANIFEST-SCHEMA-VERSION",
            f"Minimal PIS manifest must use schema_version={CONTRACT_SCHEMA_VERSION!r}.",
        )

    if manifest.get("manifest_role") != "minimal_protected_immutable_surface":
        add("PIS-MANIFEST-ROLE", "Minimal PIS manifest has invalid or missing manifest_role.")

    if manifest.get("active_enforcement") is not False:
        add(
            "PIS-MANIFEST-RESEARCH-MODE",
            "Research manifest must keep active_enforcement=false until promoted to contracts/.",
        )

    protected_globs_raw = manifest.get("protected_globs")
    if not isinstance(protected_globs_raw, list):
        add("PIS-MANIFEST-PROTECTED-GLOBS", "Minimal PIS manifest must define protected_globs as a list.")
    else:
        normalized_manifest_globs = {
            normalize_path(item)
            for item in protected_globs_raw
            if isinstance(item, str)
        }
        for required_glob in REQUIRED_MINIMAL_PROTECTED_GLOBS:
            if normalize_path(required_glob) not in normalized_manifest_globs:
                add(
                    "PIS-MANIFEST-MISSING-REQUIRED-GLOB",
                    f"Minimal PIS manifest must include pinned protected glob: {required_glob}",
                )

    unlock = manifest.get("unlock")
    if not isinstance(unlock, dict):
        add("PIS-MANIFEST-UNLOCK", "Minimal PIS manifest must define unlock as an object.")
    else:
        if unlock.get("mode") != "solo_maintainer":
            add("PIS-MANIFEST-UNLOCK-MODE", "Minimal PIS manifest currently supports only solo_maintainer unlock mode.")
        if not unlock.get("required_unlock_file_glob"):
            add("PIS-MANIFEST-UNLOCK-GLOB", "Minimal PIS manifest must define required_unlock_file_glob.")

    claims = manifest.get("claims")
    if not isinstance(claims, dict):
        add("PIS-MANIFEST-CLAIMS", "Minimal PIS manifest must define claims as an object.")
    else:
        for key in (
            "ontology_authority",
            "auto_fix_allowed",
            "truth_claim_allowed",
            "safety_claim_allowed",
        ):
            if claims.get(key) is not False:
                add(f"PIS-MANIFEST-CLAIM-{key.upper()}", f"Minimal PIS manifest must keep claims.{key}=false.")

    failure_mode = manifest.get("failure_mode")
    if not isinstance(failure_mode, dict) or failure_mode.get("fail_closed") is not True:
        add("PIS-MANIFEST-FAIL-CLOSED", "Minimal PIS manifest must define failure_mode.fail_closed=true.")

    return findings


def analyze_protected_surface(
    *,
    changes: list[ChangedPath],
    manifest: dict[str, Any],
    manifest_path: str,
) -> list[Finding]:
    findings: list[Finding] = []

    findings.extend(validate_manifest_shape(manifest, manifest_path))
    if findings:
        return findings

    protected_paths = [
        normalize_path(item)
        for item in manifest.get("protected_paths", [])
        if isinstance(item, str)
    ]
    protected_globs = sorted(
        {
            *(normalize_path(item) for item in REQUIRED_MINIMAL_PROTECTED_GLOBS),
            *(
                normalize_path(item)
                for item in manifest.get("protected_globs", [])
                if isinstance(item, str)
            ),
        }
    )
    excluded_globs = [
        normalize_path(item)
        for item in manifest.get("excluded_globs", [])
        if isinstance(item, str)
    ]

    protected_changes = protected_changed_paths(
        changes,
        protected_paths=protected_paths,
        protected_globs=protected_globs,
        excluded_globs=excluded_globs,
    )

    if not protected_changes:
        return []

    unlock = manifest.get("unlock", {})
    required_unlock_glob = str(unlock.get("required_unlock_file_glob", "")).strip()
    required_signed_by = str(unlock.get("required_signed_by", DEFAULT_REQUIRED_SIGNED_BY)).strip()
    required_confirmation = str(unlock.get("required_confirmation", DEFAULT_REQUIRED_CONFIRMATION))

    if not required_unlock_glob:
        return [
            pis_finding(
                rule_id="PIS-UNLOCK-GLOB-MISSING",
                path=manifest_path,
                message="Protected paths changed, but manifest does not declare required unlock glob.",
                protected_object="unlock_policy",
                vector=DriftVector.V7_CONTRACT_DRIFT,
                safer_form="Declare research/pis/unlocks/UNLOCK-*.json as the unlock glob.",
            )
        ]

    records, unlock_errors = load_unlock_records(required_unlock_glob)

    for error in unlock_errors:
        findings.append(
            pis_finding(
                rule_id="PIS-UNLOCK-INVALID-JSON",
                path=error.split(":", 1)[0],
                message=f"Unlock record could not be loaded: {error}",
                protected_object="unlock_record",
                vector=DriftVector.V7_CONTRACT_DRIFT,
                safer_form="Keep unlock records as valid JSON with solo-maintainer fields.",
            )
        )

    for protected_path, status in protected_changes:
        covering, invalid_messages = find_covering_unlocks(
            records,
            protected_path,
            required_signed_by=required_signed_by,
            required_confirmation=required_confirmation,
        )

        if covering:
            continue

        if invalid_messages:
            observed = " | ".join(invalid_messages)
            rule_id = "PIS-PROTECTED-PATH-INVALID-UNLOCK"
            message = "Protected path changed, but matching unlock record is invalid or expired."
        else:
            observed = f"git_status={status}"
            rule_id = "PIS-PROTECTED-PATH-WITHOUT-UNLOCK"
            message = "Protected path changed without matching solo-maintainer unlock record."

        findings.append(
            pis_finding(
                rule_id=rule_id,
                path=protected_path,
                message=message,
                observed_pattern=observed,
                protected_object=protected_object_for_path(protected_path),
                vector=protected_vector_for_path(protected_path),
                safer_form=(
                    "Create research/pis/unlocks/UNLOCK-*.json with exact protected paths only, "
                    "reason, maintainer signature, exact confirmation, expiry, "
                    "ontology_authority=false, and auto_fix_allowed=false."
                ),
            )
        )

    return findings


def emit_github_annotation(finding: Finding) -> None:
    command = "warning" if finding.severity == Severity.WARN else "error"
    safe_message = finding.message.replace("%", "%25")
    safe_message = safe_message.replace("\r", "%0D").replace("\n", "%0A")
    safe_path = str(finding.path).replace("\n", "")

    if finding.line is not None:
        print(f"::{command} file={safe_path},line={finding.line},title={finding.rule_id}::{safe_message}")
    else:
        print(f"::{command} file={safe_path},title={finding.rule_id}::{safe_message}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS minimal protected surface guard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--base", required=True, help="Base commit SHA or null SHA.")
    parser.add_argument("--head", required=True, help="Head commit SHA.")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST_PATH, help="Minimal PIS manifest path.")
    parser.add_argument(
        "--mode",
        choices=("strict", "report"),
        default="strict",
        help="Strict exits non-zero on protected-surface findings.",
    )
    parser.add_argument("--json-out", default=None, help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    base = args.base.strip()
    head = args.head.strip() or "HEAD"
    manifest_path = normalize_path(args.manifest)
    title = f"{GUARD_ID} / {GUARD_NAME} v{VERSION}"
    fail_on = Severity.BLOCKER

    try:
        manifest = load_json_file(Path(manifest_path))
        changes = diff_name_status(base, head)

        findings = analyze_protected_surface(
            changes=changes,
            manifest=manifest,
            manifest_path=manifest_path,
        )

        for finding in findings:
            emit_github_annotation(finding)

        print(f"Changed entries scanned: {len(changes)}")
        print_text_report(findings, title=title, mode=args.mode, fail_on=fail_on, root=Path.cwd())

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
        print("::error title=PIS-GUARD-RUNTIME-ERROR::Protected surface guard failed internally.")
        print("")
        print("PIS-GUARD-RUNTIME-ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: guard runtime error blocks the check.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
