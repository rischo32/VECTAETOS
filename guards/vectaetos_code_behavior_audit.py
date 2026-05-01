#!/usr/bin/env python3
"""
VECTAETOS_CODE_BEHAVIOR_AUDIT.py

Version:
    0.1.0

Purpose:
    Ontological production-code behavior audit for VECTAETOS Python code.

Scope:
    - Static AST audit.
    - Checks whether code behavior matches its declared or inferred VECTAETOS role.
    - Does not perform security audit.
    - Does not perform integrity audit.
    - Does not modify files.
    - Does not validate deployment.

Python:
    3.11+

Run from:
    repository root

Command:
    python3 guards/VECTAETOS_CODE_BEHAVIOR_AUDIT.py

Exit codes:
    0 = clean / warnings only
    1 = hard violation found
    2 = execution/config error
"""

from __future__ import annotations

import argparse
import ast
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Iterable


VERSION = "0.1.0"
DEFAULT_CONTRACT_PATH = Path("contracts/vectaetos_code_contract.json")

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}

EXCLUDED_FILE_NAMES = {
    "__init__.py",
}

DANGEROUS_CALL_NAMES = {
    "eval",
    "exec",
    "compile",
    "__import__",
}

NETWORK_MODULE_PREFIXES = (
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "aiohttp",
    "ftplib",
    "smtplib",
    "paramiko",
)

SUBPROCESS_MODULE_PREFIXES = (
    "subprocess",
    "pty",
)

RANDOM_MODULE_PREFIXES = (
    "random",
    "secrets",
)

WRITE_METHODS = {
    "write",
    "write_text",
    "write_bytes",
    "writelines",
    "unlink",
    "rename",
    "replace",
    "mkdir",
    "rmdir",
    "touch",
}

ONTOLOGY_FORBIDDEN_NAME_FRAGMENTS = (
    "decide",
    "decision",
    "recommend",
    "recommendation",
    "optimize",
    "optimization",
    "reward",
    "policy_update",
    "select_best",
    "best_trajectory",
    "rank_trajectories",
    "truth_authority",
)

VORTEX_FORBIDDEN_CALL_FRAGMENTS = (
    "argmax",
    "argmin",
    "select_best",
    "best_trajectory",
    "rank",
    "reward",
    "optimize",
    "policy_update",
)

PROTECTED_ONTOLOGY_NAMES = {
    "PHI",
    "Phi",
    "K",
    "K_PHI",
    "KPhi",
    "KAPPA",
    "kappa",
    "QE",
}


@dataclasses.dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: Path
    line_no: int
    message: str
    detail: str
    safer_form: str


@dataclasses.dataclass(frozen=True)
class FileAudit:
    path: Path
    role: str
    findings: list[Finding]


def load_contract(root: Path, contract_path: Path) -> dict[str, Any]:
    full_path = (root / contract_path).resolve()

    if not full_path.exists():
        raise RuntimeError(f"contract file not found: {full_path}")

    try:
        data = json.loads(full_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON contract {full_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError("contract root must be a JSON object")

    return data


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if path.is_dir():
            continue

        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            rel_parts = path.parts

        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue

        if path.name in EXCLUDED_FILE_NAMES:
            continue

        yield path


def parse_python(path: Path) -> ast.AST:
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = path.read_text(encoding="utf-8-sig")

    try:
        return ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise RuntimeError(f"syntax error in {path}: {exc}") from exc


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr

    if isinstance(node, ast.Call):
        return dotted_name(node.func)

    if isinstance(node, ast.Subscript):
        return dotted_name(node.value)

    return ""


def is_prefixed(name: str, prefixes: tuple[str, ...]) -> bool:
    normalized = name.lower()
    return any(
        normalized == prefix or normalized.startswith(prefix + ".")
        for prefix in prefixes
    )


def get_declared_role(tree: ast.AST) -> str | None:
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__vectaetos_role__":
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    return node.value.value.strip()

    return None


def infer_role(path: Path, root: Path, tree: ast.AST, contract: dict[str, Any]) -> str:
    declared = get_declared_role(tree)

    if declared:
        return declared

    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path

    rel_text = str(rel).replace("\\", "/").lower()
    role_patterns = contract.get("role_inference", {})

    if isinstance(role_patterns, dict):
        for role, patterns in role_patterns.items():
            if not isinstance(patterns, list):
                continue

            for pattern in patterns:
                if isinstance(pattern, str) and pattern.lower() in rel_text:
                    return str(role)

    name = path.name.lower()

    if "guard" in rel_text:
        return "guard"
    if "vortex" in rel_text:
        return "vortex"
    if "audit" in rel_text or "cryptograph" in rel_text:
        return "audit"
    if "projection" in rel_text or "rune" in rel_text or "glyph" in rel_text:
        return "projection"
    if "adapter" in rel_text or "llm" in rel_text:
        return "adapter"
    if "parser" in rel_text or "gate" in rel_text:
        return "parser"
    if "test_" in name or rel_text.startswith("tests/"):
        return "test"

    return "utility"


def role_policy(contract: dict[str, Any], role: str) -> dict[str, Any]:
    roles = contract.get("roles", {})

    if isinstance(roles, dict) and isinstance(roles.get(role), dict):
        return roles[role]

    if isinstance(roles, dict) and isinstance(roles.get("utility"), dict):
        return roles["utility"]

    return {}


def add_finding(
    findings: list[Finding],
    *,
    severity: str,
    code: str,
    path: Path,
    line_no: int,
    message: str,
    detail: str,
    safer_form: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            path=path,
            line_no=max(line_no, 1),
            message=message,
            detail=detail,
            safer_form=safer_form,
        )
    )


def imports_from_node(node: ast.AST) -> list[str]:
    imports: list[str] = []

    if isinstance(node, ast.Import):
        for alias in node.names:
            imports.append(alias.name)

    if isinstance(node, ast.ImportFrom):
        if node.module:
            imports.append(node.module)

    return imports


def open_mode_is_write(call: ast.Call) -> bool:
    mode_node: ast.AST | None = None

    if len(call.args) >= 2:
        mode_node = call.args[1]

    for keyword in call.keywords:
        if keyword.arg == "mode":
            mode_node = keyword.value

    if isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
        mode = mode_node.value
        return any(flag in mode for flag in ("w", "a", "x", "+"))

    return False


def assigned_names(node: ast.AST) -> list[str]:
    names: list[str] = []

    def visit_target(target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Attribute):
            names.append(dotted_name(target))
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                visit_target(element)
        elif isinstance(target, ast.Subscript):
            names.append(dotted_name(target.value))

    if isinstance(node, ast.Assign):
        for target in node.targets:
            visit_target(target)
    elif isinstance(node, ast.AnnAssign):
        visit_target(node.target)
    elif isinstance(node, ast.AugAssign):
        visit_target(node.target)

    return names


def function_or_class_name(node: ast.AST) -> str | None:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return node.name

    return None


def audit_file(path: Path, root: Path, contract: dict[str, Any]) -> FileAudit:
    tree = parse_python(path)
    role = infer_role(path, root, tree, contract)
    policy = role_policy(contract, role)
    findings: list[Finding] = []

    allow_network = bool(policy.get("allow_network", False))
    allow_subprocess = bool(policy.get("allow_subprocess", False))
    allow_file_write = bool(policy.get("allow_file_write", False))
    allow_randomness = bool(policy.get("allow_randomness", False))
    allow_selection = bool(policy.get("allow_selection_functions", False))
    protect_ontology_assignments = bool(policy.get("protect_ontology_assignments", True))

    for node in ast.walk(tree):
        line_no = getattr(node, "lineno", 1)

        for imported in imports_from_node(node):
            if is_prefixed(imported, NETWORK_MODULE_PREFIXES) and not allow_network:
                add_finding(
                    findings,
                    severity="HARD",
                    code="NETWORK_IMPORT",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' imports network module '{imported}'",
                    detail="Network access is outside deterministic VECTAETOS production-code audit.",
                    safer_form="Move network behavior outside ontology/perimeter code.",
                )

            if is_prefixed(imported, SUBPROCESS_MODULE_PREFIXES) and not allow_subprocess:
                add_finding(
                    findings,
                    severity="HARD",
                    code="SUBPROCESS_IMPORT",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' imports subprocess module '{imported}'",
                    detail="Subprocess execution expands behavior beyond static deterministic audit.",
                    safer_form="Use pure Python deterministic checks or isolate subprocess use explicitly.",
                )

            if is_prefixed(imported, RANDOM_MODULE_PREFIXES) and not allow_randomness:
                add_finding(
                    findings,
                    severity="WARN",
                    code="RANDOMNESS_IMPORT",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' imports randomness module '{imported}'",
                    detail="Randomness may break deterministic production behavior.",
                    safer_form="Use deterministic seeds or remove randomness from this role.",
                )

        name = function_or_class_name(node)

        if name:
            lowered = name.lower()
            for fragment in ONTOLOGY_FORBIDDEN_NAME_FRAGMENTS:
                if fragment in lowered:
                    add_finding(
                        findings,
                        severity="HARD",
                        code="FORBIDDEN_BEHAVIOR_NAME",
                        path=path,
                        line_no=line_no,
                        message=f"role '{role}' declares behavior-like name '{name}'",
                        detail="Production code should not encode agency, recommendation, reward, optimization, or truth-authority semantics.",
                        safer_form="Rename to scan, detect, project, render, report, expose, or another descriptive verb.",
                    )

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and protect_ontology_assignments:
            for target_name in assigned_names(node):
                clean_target = target_name.split(".")[-1]

                if clean_target in PROTECTED_ONTOLOGY_NAMES and role not in {"test"}:
                    add_finding(
                        findings,
                        severity="WARN",
                        code="PROTECTED_ONTOLOGY_ASSIGNMENT",
                        path=path,
                        line_no=line_no,
                        message=f"role '{role}' assigns to protected ontology-like name '{target_name}'",
                        detail="Assignments to Φ/K/κ/QE-like names may be legitimate in formal math modules but require review.",
                        safer_form="Production code should reference ontology; canonical anchors define ontology.",
                    )

        if isinstance(node, ast.Call):
            call_name = dotted_name(node.func)
            call_lower = call_name.lower()
            method = call_name.split(".")[-1]

            if call_name in DANGEROUS_CALL_NAMES:
                add_finding(
                    findings,
                    severity="HARD",
                    code="DYNAMIC_EXECUTION",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls '{call_name}'",
                    detail="Dynamic execution prevents deterministic ontology-conformance audit.",
                    safer_form="Remove dynamic execution from production ontology/perimeter code.",
                )

            if call_lower in {"open", "io.open"} and open_mode_is_write(node) and not allow_file_write:
                add_finding(
                    findings,
                    severity="HARD",
                    code="FILE_WRITE",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' opens file in write/append mode",
                    detail="This role is expected to be read-only.",
                    safer_form="Emit stdout report only or move writing into an explicitly contracted reporting utility.",
                )

            if method in WRITE_METHODS and not allow_file_write:
                add_finding(
                    findings,
                    severity="HARD",
                    code="FILESYSTEM_MUTATION",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls filesystem mutation '{call_name}'",
                    detail="This role is expected to be read-only.",
                    safer_form="Use read-only scan/report behavior.",
                )

            if is_prefixed(call_name, NETWORK_MODULE_PREFIXES) and not allow_network:
                add_finding(
                    findings,
                    severity="HARD",
                    code="NETWORK_CALL",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls network function '{call_name}'",
                    detail="Network behavior is outside deterministic ontology production audit.",
                    safer_form="Remove network calls from this role.",
                )

            if (is_prefixed(call_name, SUBPROCESS_MODULE_PREFIXES) or call_lower == "os.system") and not allow_subprocess:
                add_finding(
                    findings,
                    severity="HARD",
                    code="SUBPROCESS_CALL",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls subprocess/shell function '{call_name}'",
                    detail="Subprocess execution is outside this role contract.",
                    safer_form="Use deterministic Python-only behavior.",
                )

            if is_prefixed(call_name, RANDOM_MODULE_PREFIXES) and not allow_randomness:
                add_finding(
                    findings,
                    severity="WARN",
                    code="RANDOMNESS_CALL",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls randomness function '{call_name}'",
                    detail="Randomness may break deterministic behavior.",
                    safer_form="Use deterministic seed or remove randomness.",
                )

            if method in {"min", "max", "sorted"} and not allow_selection:
                add_finding(
                    findings,
                    severity="WARN",
                    code="SELECTION_FUNCTION",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls selection/sorting function '{call_name}'",
                    detail="Selection functions are allowed in guards for technical findings; other roles require review.",
                    safer_form="Ensure this does not select truth, best trajectory, or ontology.",
                )

            if method in {"argmin", "argmax"} and not allow_selection:
                add_finding(
                    findings,
                    severity="HARD",
                    code="ARG_SELECTION_FUNCTION",
                    path=path,
                    line_no=line_no,
                    message=f"role '{role}' calls arg-selection function '{call_name}'",
                    detail="argmin/argmax must not appear as ontology, Vortex, or projection selection authority.",
                    safer_form="Restrict argmin/argmax to external guard/report mechanics only.",
                )

            if role == "vortex":
                for fragment in VORTEX_FORBIDDEN_CALL_FRAGMENTS:
                    if fragment in call_lower:
                        add_finding(
                            findings,
                            severity="HARD",
                            code="VORTEX_SELECTION_OR_OPTIMIZATION",
                            path=path,
                            line_no=line_no,
                            message=f"Vortex role calls forbidden function '{call_name}'",
                            detail="Vortex may generate candidate trajectories, but must not rank, select, optimize, or reward them.",
                            safer_form="Use candidate generation and descriptive export only.",
                        )

    return FileAudit(path=path, role=role, findings=findings)


def print_report(file_audits: list[FileAudit], root: Path) -> None:
    all_findings = [finding for audit in file_audits for finding in audit.findings]
    hard_count = sum(1 for finding in all_findings if finding.severity == "HARD")
    warn_count = sum(1 for finding in all_findings if finding.severity == "WARN")

    print(f"VECTAETOS Code Behavior Audit v{VERSION}")
    print("=====================================")
    print(f"Files audited:    {len(file_audits)}")
    print(f"Hard violations: {hard_count}")
    print(f"Warnings:         {warn_count}")
    print()

    role_counts: dict[str, int] = {}

    for audit in file_audits:
        role_counts[audit.role] = role_counts.get(audit.role, 0) + 1

    print("Role map:")

    for role in sorted(role_counts):
        print(f"  {role}: {role_counts[role]}")

    print()

    if not all_findings:
        print("OK: no code behavior drift detected.")
        return

    for finding in sorted(all_findings, key=lambda item: (str(item.path), item.line_no, item.code)):
        try:
            rel = finding.path.relative_to(root)
        except ValueError:
            rel = finding.path

        print(f"[{finding.severity}] {finding.code}")
        print(f"  file: {rel}:{finding.line_no}")
        print(f"  msg:  {finding.message}")
        print(f"  why:  {finding.detail}")
        print(f"  use:  {finding.safer_form}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static ontological behavior audit for VECTAETOS Python code."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current working directory.",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=DEFAULT_CONTRACT_PATH,
        help="Path to behavior contract JSON relative to root.",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Treat warnings as CI failures.",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        contract = load_contract(root, args.contract)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    file_audits: list[FileAudit] = []

    try:
        for py_file in iter_python_files(root):
            file_audits.append(audit_file(py_file, root, contract))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print_report(file_audits, root)

    all_findings = [finding for audit in file_audits for finding in audit.findings]
    hard_count = sum(1 for finding in all_findings if finding.severity == "HARD")
    warn_count = sum(1 for finding in all_findings if finding.severity == "WARN")

    if hard_count > 0:
        return 1

    if args.warnings_as_errors and warn_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
