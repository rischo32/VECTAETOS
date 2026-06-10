#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTAETOS :: GUARD-13 EK OBSERVABLE NON-AUTHORITY GUARD

Role:
    Level 4 perimeter guard for EK / audit / hash / ledger / observable
    non-authority boundaries.

Purpose:
    Expose textual drift where Epistemic Cryptography, audit, hashes,
    signatures, manifests, ledgers, Merkle roots, EK events, or observables
    are framed as truth, ontology, validation, decision, command, enforcement,
    deployment authorization, or safety proof.

Boundary:
    This guard does not define EK.
    This guard does not define ontology.
    This guard does not prove truth.
    This guard does not validate safety.
    This guard does not authorize deployment.
    This guard does not mutate Φ.
    This guard does not modify repository files.
    This guard does not auto-fix ontology-facing text.

    It only scans repository text against a machine-readable contract and emits
    repository-state findings.

Expected contract:
    contracts/guard13_ek_observable_rules.json

Python:
    3.11+

Dependencies:
    standard library only + guards.core shared kernel
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


GUARD_ID = "GUARD-13"
GUARD_FILE = "guards/ek_observable_non_authority_guard.py"
GUARD_NAME = "EK observable non-authority guard"
VERSION = "0.1.0"
CONTRACT_SCHEMA_VERSION = "1.0"

DEFAULT_CONTRACT_PATH = "contracts/guard13_ek_observable_rules.json"


def _prepend_import_root(root: Path) -> None:
    """Put a single import root at sys.path[0]."""
    root_str = str(root)
    sys.path[:] = [entry for entry in sys.path if entry != root_str]
    sys.path.insert(0, root_str)


def _bootstrap_repo_import_path() -> Path:
    """
    Ensure guards.core is imported from the repository root or trusted runtime.
    """
    script_path = Path(__file__).resolve()
    cwd = Path.cwd().resolve()

    candidates = [
        cwd,
        script_path.parent.parent,
        script_path.parent.parent.parent,
    ]

    for candidate in candidates:
        if (candidate / "guards" / "core" / "findings.py").is_file():
            _prepend_import_root(candidate)
            return candidate

    return cwd


REPO_ROOT = _bootstrap_repo_import_path()

try:
    from guards.core.contracts import ContractError, load_contract, validate_contract_file
    from guards.core.findings import Finding, Severity
    from guards.core.paths import iter_repo_files, normalize_repo_path
    from guards.core.reporting import (
        EXIT_INVALID_CONTRACT,
        exit_code_for,
        print_text_report,
        write_json,
    )
    from guards.core.text_scan import (
        ScanRule,
        read_text_file,
        scan_rules_from_contract_rule,
        scan_text_to_findings,
    )
except ModuleNotFoundError as exc:
    print("::error title=GUARD-IMPORT-ERROR::Cannot import guards.core shared kernel.")
    print("")
    print("GUARD-IMPORT-ERROR")
    print(str(exc))
    print("")
    print(f"cwd: {Path.cwd()}")
    print(f"script: {Path(__file__).resolve()}")
    print(f"repo_root_candidate: {REPO_ROOT}")
    print("")
    print("Fail-closed: shared guard kernel is unavailable.")
    raise SystemExit(2)


def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return normalize_repo_path(path)


def load_scan_rules(contract_path: Path) -> list[ScanRule]:
    """
    Load contract and convert contract rules into text scan rules.

    Contract rules are projections of anchors. They are not ontology.
    """
    document = load_contract(contract_path)

    rules: list[ScanRule] = []
    for contract_rule in document.rules:
        rules.extend(
            scan_rules_from_contract_rule(
                contract_rule,
                contract_ref=normalize_repo_path(contract_path),
            )
        )

    if not rules:
        raise ContractError(
            f"{normalize_repo_path(contract_path)} produced no scan rules"
        )

    return rules


def iter_candidate_text_files(root: Path) -> Iterable[Path]:
    """
    Iterate repository text files deterministically.

    Heavy/generated technical directories are skipped by paths.iter_repo_files.
    Semantic inclusion/exclusion remains governed by the contract and scanner.
    """
    yield from iter_repo_files(
        root,
        text_only=True,
        include_binary=False,
        skip_heavy_dirs=True,
    )


def scan_repository(
    *,
    root: Path,
    rules: list[ScanRule],
) -> list[Finding]:
    findings: list[Finding] = []

    for file_path in iter_candidate_text_files(root):
        rel_path = repo_relative(root, file_path)
        text = read_text_file(file_path)

        if text is None:
            continue

        findings.extend(
            scan_text_to_findings(
                path=rel_path,
                text=text,
                rules=rules,
                guard_id=GUARD_ID,
                guard_file=GUARD_FILE,
                contract_schema_version=CONTRACT_SCHEMA_VERSION,
                skip_safe_context=True,
            )
        )

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VECTAETOS GUARD-13 EK observable non-authority guard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan.",
    )
    parser.add_argument(
        "--contract",
        default=DEFAULT_CONTRACT_PATH,
        help="Machine-readable GUARD-13 rule contract.",
    )
    parser.add_argument(
        "--mode",
        choices=("report", "strict"),
        default="report",
        help="Report mode exits 0; strict exits 1 on configured blocker findings.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional JSON report output path.",
    )
    parser.add_argument(
        "--fail-on",
        choices=("INFO", "WARN", "HARD", "BLOCKER"),
        default="BLOCKER",
        help="Severity threshold for strict mode.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    root = Path(args.root).resolve()
    contract_path = Path(args.contract)
    if not contract_path.is_absolute():
        contract_path = root / contract_path

    title = f"{GUARD_ID} / {GUARD_NAME} v{VERSION}"
    fail_on = Severity(args.fail_on)

    try:
        contract_findings = validate_contract_file(
            contract_path,
            guard_id=GUARD_ID,
            guard_file=GUARD_FILE,
        )

        if contract_findings:
            print_text_report(
                contract_findings,
                title=title,
                mode=args.mode,
                fail_on=fail_on,
                root=root,
            )
            if args.json_out:
                write_json(Path(args.json_out), contract_findings)
            return EXIT_INVALID_CONTRACT

        rules = load_scan_rules(contract_path)
        findings = scan_repository(root=root, rules=rules)

        print_text_report(
            findings,
            title=title,
            mode=args.mode,
            fail_on=fail_on,
            root=root,
        )

        if args.json_out:
            write_json(Path(args.json_out), findings)

        if args.mode == "strict":
            return exit_code_for(findings, fail_on=fail_on)

        return 0

    except ContractError as exc:
        print("::error title=GUARD-CONTRACT-ERROR::GUARD-13 contract is invalid.")
        print("")
        print("GUARD-CONTRACT-ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: contract confidence unavailable.")
        return 3

    except Exception as exc:
        print("::error title=GUARD-RUNTIME-ERROR::GUARD-13 failed internally.")
        print("")
        print("GUARD-RUNTIME-ERROR")
        print(str(exc))
        print("")
        print("Fail-closed: guard runtime error blocks the check.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
