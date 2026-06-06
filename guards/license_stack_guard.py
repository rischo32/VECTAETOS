#!/usr/bin/env python3
"""
VECTAETOS — License Stack Guard
===============================

Repository-aligned location:
    guards/license_stack_guard.py

Registry location:
    contracts/LICENSE_REGISTRY.json

Purpose:
    Detect configured license-stack boundary drift:
    - configured file missing
    - license moved or renamed
    - DOI missing from a configured license file
    - expected boundary marker missing
    - optional SHA-256 manifest mismatch

This guard does not:
    - decide legal validity
    - define ontology
    - define canonical truth
    - modify files
    - auto-fix licenses
    - update README
    - modify Φ, K(Φ), κ, QE, Vortex, projection, audit, memory, or evidence status

Python:
    3.11+

Exit:
    0 = PASS, or report mode with findings
    1 = strict mode with hard findings
    2 = execution/configuration error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


GUARD_NAME = "VECTAETOS License Stack Guard"
GUARD_VERSION = "0.3.0"
DEFAULT_REGISTRY_PATH = "contracts/LICENSE_REGISTRY.json"


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class Summary:
    guard: str
    version: str
    repo_root: str
    registry_path: str
    hash_manifest_path: str
    mode: str
    files_checked: int
    findings: int
    hard_findings: int
    warn_findings: int
    results: list[Finding]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_registry(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(path))
    except FileNotFoundError as exc:
        raise RuntimeError(f"registry not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"registry is invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError("registry root must be a JSON object")
    return data


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sha_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    text = read_text(path)
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        match = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$", raw)
        if not match:
            raise RuntimeError(f"invalid SHA-256 manifest line {line_no}: {raw!r}")

        digest, rel_path = match.groups()
        rel_path = rel_path.strip()
        if rel_path.startswith("./"):
            rel_path = rel_path[2:]
        entries[rel_path] = digest.lower()
    return entries


def add_finding(
    findings: list[Finding],
    severity: str,
    code: str,
    path: str,
    message: str,
) -> None:
    findings.append(Finding(severity=severity, code=code, path=path, message=message))


def check_registry_shape(registry: dict[str, Any], registry_path: str) -> list[Finding]:
    findings: list[Finding] = []

    if registry.get("schema") not in {
        "vectaetos-license-registry-v0.1",
        "vectaetos-license-registry-v0.2",
    }:
        add_finding(
            findings,
            "HARD",
            "REGISTRY_SCHEMA_INVALID",
            registry_path,
            "schema must be vectaetos-license-registry-v0.1 or vectaetos-license-registry-v0.2",
        )

    expected_none = {
        "execution_power": "none",
        "feedback_into_phi": "none",
        "ontology_authority": "none",
        "legal_validity_claim": "none",
    }
    for key, expected in expected_none.items():
        value = registry.get(key)
        if value != expected:
            add_finding(
                findings,
                "HARD",
                "REGISTRY_BOUNDARY_FIELD_INVALID",
                registry_path,
                f"{key} must be {expected!r}, got {value!r}",
            )

    licenses = registry.get("licenses")
    if not isinstance(licenses, list) or not licenses:
        add_finding(
            findings,
            "HARD",
            "REGISTRY_LICENSES_INVALID",
            registry_path,
            "licenses must be a non-empty list",
        )
        return findings

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()

    for index, item in enumerate(licenses):
        where = f"licenses[{index}]"
        if not isinstance(item, dict):
            add_finding(findings, "HARD", "REGISTRY_ENTRY_INVALID", registry_path, f"{where} must be an object")
            continue

        for key in ("id", "role", "path", "doi", "status"):
            if not item.get(key):
                add_finding(findings, "HARD", "REGISTRY_FIELD_MISSING", registry_path, f"{where}.{key} is required")

        license_id = str(item.get("id", ""))
        license_path = str(item.get("path", ""))

        if license_id and license_id in seen_ids:
            add_finding(findings, "HARD", "REGISTRY_DUPLICATE_ID", registry_path, f"duplicate id: {license_id}")
        seen_ids.add(license_id)

        if license_path and license_path in seen_paths:
            add_finding(findings, "HARD", "REGISTRY_DUPLICATE_PATH", registry_path, f"duplicate path: {license_path}")
        seen_paths.add(license_path)

    return findings


def required_hash_paths(registry: dict[str, Any], registry_path: str) -> list[str]:
    out = [registry_path]
    for item in registry.get("licenses", []):
        if isinstance(item, dict):
            rel = item.get("path")
            if isinstance(rel, str) and rel:
                out.append(rel)

    seen: set[str] = set()
    deduped: list[str] = []
    for rel in out:
        if rel not in seen:
            deduped.append(rel)
            seen.add(rel)
    return deduped


def check_license_file(root: Path, item: dict[str, Any], findings: list[Finding]) -> bool:
    rel = str(item.get("path", ""))
    path = root / rel

    if not path.exists():
        add_finding(findings, "HARD", "LICENSE_FILE_MISSING", rel, "configured license file does not exist")
        return False

    if not path.is_file():
        add_finding(findings, "HARD", "LICENSE_PATH_NOT_FILE", rel, "configured license path is not a file")
        return False

    try:
        text = read_text(path)
    except UnicodeDecodeError:
        add_finding(findings, "HARD", "LICENSE_NOT_UTF8", rel, "license file must be UTF-8 text")
        return False
    except OSError as exc:
        add_finding(findings, "HARD", "LICENSE_READ_ERROR", rel, f"cannot read license file: {exc}")
        return False

    license_id = str(item.get("id", ""))
    if license_id and license_id not in text:
        add_finding(findings, "HARD", "LICENSE_ID_MISSING", rel, f"license id not found: {license_id}")

    doi = str(item.get("doi", ""))
    if doi and doi not in text:
        add_finding(findings, "HARD", "LICENSE_DOI_MISSING", rel, f"DOI not found: {doi}")

    for marker in item.get("required_markers", []) or []:
        if not isinstance(marker, str) or not marker:
            continue
        if marker not in text:
            add_finding(findings, "HARD", "LICENSE_MARKER_MISSING", rel, f"required marker not found: {marker!r}")

    return True


def check_hash_manifest(
    root: Path,
    registry: dict[str, Any],
    registry_path: str,
    manifest_path: str,
    findings: list[Finding],
    require_hashes: bool,
) -> None:
    manifest_file = root / manifest_path
    required = required_hash_paths(registry, registry_path)

    if not manifest_file.exists():
        severity = "HARD" if require_hashes else "WARN"
        add_finding(
            findings,
            severity,
            "HASH_MANIFEST_MISSING",
            manifest_path,
            "SHA-256 manifest is missing. Generate it after license files are final.",
        )
        return

    try:
        entries = parse_sha_manifest(manifest_file)
    except (OSError, UnicodeDecodeError, RuntimeError) as exc:
        add_finding(findings, "HARD", "HASH_MANIFEST_INVALID", manifest_path, str(exc))
        return

    required_set = set(required)

    for rel in required:
        path = root / rel
        if rel not in entries:
            add_finding(findings, "HARD", "HASH_ENTRY_MISSING", rel, "path is missing from SHA-256 manifest")
            continue
        if not path.exists():
            add_finding(findings, "HARD", "HASHED_FILE_MISSING", rel, "hash-required file does not exist")
            continue

        expected = entries[rel]
        actual = sha256_file(path)
        if actual != expected:
            add_finding(
                findings,
                "HARD",
                "HASH_MISMATCH",
                rel,
                f"sha256 mismatch: expected {expected}, got {actual}",
            )

    for rel in sorted(entries):
        if rel not in required_set:
            add_finding(findings, "WARN", "HASH_ENTRY_UNREGISTERED", rel, "manifest contains a path not listed by registry")


def run(
    root: Path,
    registry_rel: str,
    mode: str,
    require_hashes_arg: bool | None,
) -> Summary:
    registry_path = root / registry_rel
    registry = load_registry(registry_path)

    findings: list[Finding] = []
    findings.extend(check_registry_shape(registry, registry_rel))

    files_checked = 0
    for item in registry.get("licenses", []):
        if isinstance(item, dict):
            files_checked += 1
            check_license_file(root, item, findings)

    manifest_rel = str(registry.get("hash_manifest") or "LICENSES/LICENSE_INTEGRITY_MANIFEST.sha256")
    registry_requires_hashes = bool(registry.get("hash_manifest_required", False))
    require_hashes = registry_requires_hashes if require_hashes_arg is None else require_hashes_arg

    check_hash_manifest(
        root=root,
        registry=registry,
        registry_path=registry_rel,
        manifest_path=manifest_rel,
        findings=findings,
        require_hashes=require_hashes,
    )

    hard = sum(1 for item in findings if item.severity == "HARD")
    warn = sum(1 for item in findings if item.severity == "WARN")

    return Summary(
        guard=GUARD_NAME,
        version=GUARD_VERSION,
        repo_root=str(root),
        registry_path=registry_rel,
        hash_manifest_path=manifest_rel,
        mode=mode,
        files_checked=files_checked,
        findings=len(findings),
        hard_findings=hard,
        warn_findings=warn,
        results=findings,
    )


def print_text(summary: Summary) -> None:
    print("=" * 72)
    print(f"{summary.guard} v{summary.version}")
    print("=" * 72)
    print(f"Repo root:       {summary.repo_root}")
    print(f"Registry:        {summary.registry_path}")
    print(f"Hash manifest:   {summary.hash_manifest_path}")
    print(f"Mode:            {summary.mode}")
    print(f"Files checked:   {summary.files_checked}")
    print(f"Findings:        {summary.findings}")
    print(f"Hard findings:   {summary.hard_findings}")
    print(f"Warnings:        {summary.warn_findings}")
    print("-" * 72)

    if not summary.results:
        print("PASS: license stack boundary matched configured registry and integrity state.")
    else:
        for finding in summary.results:
            print(f"[{finding.severity}] {finding.code}")
            print(f"  path: {finding.path}")
            print(f"  msg : {finding.message}")
            print()

    print("=" * 72)
    print("This guard is tamper-evidence only.")
    print("It does not decide legal validity, truth, safety, or deployment admissibility.")
    print("=" * 72)


def write_report(path: Path, summary: Summary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(summary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS license-stack boundary and integrity guard.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--repo-root", "--root", dest="repo_root", default=".", help="Repository root.")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_PATH, help="License registry path.")
    parser.add_argument("--strict", action="store_true", help="Return exit 1 on hard findings.")
    parser.add_argument("--mode", choices=("report", "strict"), default=None, help="Alternative mode selector.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Console output format.")
    parser.add_argument("--report", "--json-out", dest="report", default=None, help="Optional JSON report path.")
    parser.add_argument(
        "--require-hashes",
        action="store_true",
        help="Treat missing SHA-256 manifest as a hard finding.",
    )
    parser.add_argument(
        "--no-require-hashes",
        action="store_true",
        help="Treat missing SHA-256 manifest as a warning.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.repo_root).resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: invalid repo root: {root}", file=sys.stderr)
        return 2

    if args.mode is not None:
        mode = args.mode
    else:
        mode = "strict" if args.strict else "report"

    if args.require_hashes and args.no_require_hashes:
        print("ERROR: cannot use --require-hashes and --no-require-hashes together", file=sys.stderr)
        return 2

    require_hashes_arg: bool | None
    if args.require_hashes:
        require_hashes_arg = True
    elif args.no_require_hashes:
        require_hashes_arg = False
    else:
        require_hashes_arg = None

    try:
        summary = run(root=root, registry_rel=args.registry, mode=mode, require_hashes_arg=require_hashes_arg)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))
    else:
        print_text(summary)

    if args.report:
        try:
            write_report(Path(args.report), summary)
        except OSError as exc:
            print(f"ERROR: cannot write report: {exc}", file=sys.stderr)
            return 2

    if mode == "strict" and summary.hard_findings > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
