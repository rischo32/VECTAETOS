#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard AST Scan Core

Role:
    Shared Python AST scanning helpers for code-behavior perimeter guards.

Boundary:
    This module reads Python source and exposes repository-state diagnostics.

    It does not execute source code.
    It does not import target modules.
    It does not mutate files.
    It does not define ontology, truth, safety, deployment validity, Φ, K(Φ),
    κ, QE, Vortex, Projection, EK, ASIMULATOR, ASI_MOD, or ZMYSEL.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import ast
import dataclasses
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

try:
    from guards.core.capabilities import (
        CapabilityName,
        CodeRole,
        validate_capability_use,
    )
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
    from guards.core.roles import resolve_code_role
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
    from capabilities import CapabilityName, CodeRole, validate_capability_use  # type: ignore
    from findings import (  # type: ignore
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
    from perimeter import EnforcementMode  # type: ignore
    from roles import resolve_code_role  # type: ignore


SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"
DEFAULT_GUARD_ID = "GUARD-03"
DEFAULT_GUARD_FILE = "guards/vectaetos_code_behavior_audit.py"


NETWORK_ROOTS = frozenset(
    {
        "socket",
        "requests",
        "urllib",
        "urllib.request",
        "http",
        "http.client",
        "ftplib",
        "smtplib",
        "imaplib",
        "poplib",
        "telnetlib",
        "webbrowser",
    }
)

SUBPROCESS_ROOTS = frozenset(
    {
        "subprocess",
        "os.system",
        "os.popen",
        "pty.spawn",
    }
)

RANDOMNESS_ROOTS = frozenset(
    {
        "random",
        "secrets",
        "uuid.uuid4",
        "uuid.uuid1",
        "numpy.random",
    }
)

DYNAMIC_EXEC_ROOTS = frozenset(
    {
        "eval",
        "exec",
        "compile",
        "__import__",
        "importlib.import_module",
        "runpy.run_module",
        "runpy.run_path",
    }
)

FILE_MUTATION_METHODS = frozenset(
    {
        "write",
        "writelines",
        "write_text",
        "write_bytes",
        "touch",
        "mkdir",
        "rename",
        "replace",
        "unlink",
        "rmdir",
        "remove",
        "removedirs",
        "rmtree",
        "copy",
        "copy2",
        "copyfile",
        "copytree",
        "move",
    }
)

SELECTION_FUNCTIONS = frozenset(
    {
        "max",
        "min",
        "sorted",
        "sort",
        "argmax",
        "argmin",
        "choose",
        "select",
        "rank",
    }
)

ONTOLOGY_NAMES = frozenset(
    {
        "Phi",
        "PHI",
        "phi",
        "Φ",
        "K_Phi",
        "KPhi",
        "K_D",
        "K_D_Phi",
        "K",
        "kappa",
        "κ",
        "QE",
        "Vortex",
        "Projection",
        "EK",
        "h_topo",
        "C_i_EK",
        "Q_i_EK",
    }
)


@dataclasses.dataclass(frozen=True, slots=True)
class AstCall:
    name: str
    line: int
    column: int
    excerpt: str


@dataclasses.dataclass(frozen=True, slots=True)
class AstAssignment:
    target: str
    line: int
    column: int
    excerpt: str


@dataclasses.dataclass(frozen=True, slots=True)
class AstImport:
    name: str
    alias: str
    line: int
    column: int
    excerpt: str


@dataclasses.dataclass(frozen=True, slots=True)
class AstScanResult:
    path: str
    role: CodeRole
    imports: dict[str, str]
    calls: tuple[AstCall, ...]
    assignments: tuple[AstAssignment, ...]
    findings: tuple[Finding, ...]


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def source_segment(source: str, node: ast.AST, *, limit: int = 180) -> str:
    try:
        segment = ast.get_source_segment(source, node) or ""
    except Exception:
        segment = ""
    segment = " ".join(segment.strip().split())
    if len(segment) > limit:
        return segment[: limit - 1] + "…"
    return segment


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"
        return node.attr

    if isinstance(node, ast.Call):
        return dotted_name(node.func)

    if isinstance(node, ast.Subscript):
        return dotted_name(node.value)

    return None


def target_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        if base:
            return f"{base}.{node.attr}"
        return node.attr

    if isinstance(node, ast.Subscript):
        return dotted_name(node.value)

    if isinstance(node, ast.Tuple):
        return ",".join(item for item in (target_name(elt) for elt in node.elts) if item)

    if isinstance(node, ast.List):
        return ",".join(item for item in (target_name(elt) for elt in node.elts) if item)

    return None


def build_import_aliases(tree: ast.AST) -> dict[str, str]:
    aliases: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local_name = alias.asname or alias.name.split(".")[0]
                aliases[local_name] = alias.name

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                local_name = alias.asname or alias.name
                full_name = f"{module}.{alias.name}" if module else alias.name
                aliases[local_name] = full_name

    return aliases


def collect_imports(tree: ast.AST, source: str) -> tuple[AstImport, ...]:
    imports: list[AstImport] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    AstImport(
                        name=alias.name,
                        alias=alias.asname or alias.name.split(".")[0],
                        line=getattr(node, "lineno", 1),
                        column=getattr(node, "col_offset", 0) + 1,
                        excerpt=source_segment(source, node),
                    )
                )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                name = f"{module}.{alias.name}" if module else alias.name
                imports.append(
                    AstImport(
                        name=name,
                        alias=alias.asname or alias.name,
                        line=getattr(node, "lineno", 1),
                        column=getattr(node, "col_offset", 0) + 1,
                        excerpt=source_segment(source, node),
                    )
                )

    return tuple(sorted(imports, key=lambda item: (item.line, item.column, item.alias)))


def resolve_call_name(name: str, aliases: Mapping[str, str]) -> str:
    parts = name.split(".")
    if not parts:
        return name

    first = parts[0]
    if first not in aliases:
        return name

    resolved_first = aliases[first]
    if len(parts) == 1:
        return resolved_first

    return ".".join([resolved_first, *parts[1:]])


def starts_with_any(name: str, roots: Iterable[str]) -> bool:
    return any(name == root or name.startswith(f"{root}.") for root in roots)


def call_name_for_node(node: ast.Call, aliases: Mapping[str, str]) -> str | None:
    raw = dotted_name(node.func)
    if raw is None:
        return None
    return resolve_call_name(raw, aliases)


def is_write_mode(mode: str | None) -> bool:
    if mode is None:
        return False

    normalized = mode.replace("t", "").replace("b", "")
    if any(flag in normalized for flag in ("w", "a", "x")):
        return True

    # r+ is readable and writable.
    return "+" in normalized


def is_open_write_call(node: ast.Call, name: str) -> bool:
    if name not in {"open", "io.open", "pathlib.Path.open", "Path.open"} and not name.endswith(".open"):
        return False

    mode: str | None = None

    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
        if isinstance(node.args[1].value, str):
            mode = node.args[1].value

    for keyword in node.keywords:
        if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
            if isinstance(keyword.value.value, str):
                mode = keyword.value.value

    return is_write_mode(mode)


def is_file_mutation_call(node: ast.Call, resolved_name: str) -> bool:
    if is_open_write_call(node, resolved_name):
        return True

    method = resolved_name.split(".")[-1]
    return method in FILE_MUTATION_METHODS


def is_selection_call(resolved_name: str) -> bool:
    method = resolved_name.split(".")[-1]
    return resolved_name in SELECTION_FUNCTIONS or method in SELECTION_FUNCTIONS


def is_ontology_assignment(target: str) -> bool:
    leaf = target.split(".")[-1]
    return target in ONTOLOGY_NAMES or leaf in ONTOLOGY_NAMES


def ast_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    line: int,
    column: int,
    role: CodeRole | str,
    observed_pattern: str,
    vector: DriftVector | str,
    severity: Severity | str = Severity.BLOCKER,
    confidence: Confidence | str = Confidence.HIGH,
    protected_object: str | None = None,
    safer_form: str | None = None,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
) -> Finding:
    normalized_role = role.value if isinstance(role, CodeRole) else str(role)

    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=PerimeterLevel.LEVEL_3,
        scope=PerimeterScope.CODE_BEHAVIOR,
        vector=vector,
        severity=severity,
        confidence=confidence,
        path=normalize_repo_path(path),
        line=line,
        column=column,
        message=message,
        role=normalized_role,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E2_AST_CONTRACT_COMPLIANCE,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.AST_SCAN_READ_ONLY,
        safer_form=safer_form,
    )


def parse_python_source(path: Path | str, source: str) -> tuple[ast.AST | None, list[Finding]]:
    try:
        return ast.parse(source), []
    except SyntaxError as exc:
        finding = ast_finding(
            rule_id="AST-PARSE-ERROR",
            path=path,
            message=f"Python source could not be parsed: {exc.msg}",
            line=exc.lineno or 1,
            column=exc.offset or 1,
            role=CodeRole.UNKNOWN,
            observed_pattern=exc.text.strip() if exc.text else "",
            vector=DriftVector.V7_CONTRACT_DRIFT,
            severity=Severity.HARD,
            confidence=Confidence.HIGH,
            protected_object="python_ast",
            safer_form="Fix syntax before AST-based guard confidence can be established.",
        )
        return None, [finding]


def collect_calls(tree: ast.AST, source: str, aliases: Mapping[str, str]) -> tuple[AstCall, ...]:
    calls: list[AstCall] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        name = call_name_for_node(node, aliases)
        if name is None:
            continue

        calls.append(
            AstCall(
                name=name,
                line=getattr(node, "lineno", 1),
                column=getattr(node, "col_offset", 0) + 1,
                excerpt=source_segment(source, node),
            )
        )

    return tuple(sorted(calls, key=lambda item: (item.line, item.column, item.name)))


def collect_assignments(tree: ast.AST, source: str) -> tuple[AstAssignment, ...]:
    assignments: list[AstAssignment] = []

    for node in ast.walk(tree):
        targets: list[ast.AST] = []

        if isinstance(node, ast.Assign):
            targets.extend(node.targets)
        elif isinstance(node, ast.AnnAssign):
            targets.append(node.target)
        elif isinstance(node, ast.AugAssign):
            targets.append(node.target)
        else:
            continue

        for target in targets:
            name = target_name(target)
            if not name:
                continue

            assignments.append(
                AstAssignment(
                    target=name,
                    line=getattr(node, "lineno", 1),
                    column=getattr(node, "col_offset", 0) + 1,
                    excerpt=source_segment(source, node),
                )
            )

    return tuple(sorted(assignments, key=lambda item: (item.line, item.column, item.target)))


def findings_for_call(
    *,
    path: Path | str,
    role: CodeRole,
    call: AstCall,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
) -> list[Finding]:
    findings: list[Finding] = []

    if starts_with_any(call.name, NETWORK_ROOTS):
        findings.extend(
            validate_capability_use(
                path=path,
                role=role,
                capability=CapabilityName.NETWORK,
                observed_pattern=call.excerpt or call.name,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    if starts_with_any(call.name, SUBPROCESS_ROOTS):
        findings.extend(
            validate_capability_use(
                path=path,
                role=role,
                capability=CapabilityName.SUBPROCESS,
                observed_pattern=call.excerpt or call.name,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    if starts_with_any(call.name, RANDOMNESS_ROOTS):
        findings.extend(
            validate_capability_use(
                path=path,
                role=role,
                capability=CapabilityName.RANDOMNESS,
                observed_pattern=call.excerpt or call.name,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    if starts_with_any(call.name, DYNAMIC_EXEC_ROOTS):
        findings.append(
            ast_finding(
                rule_id="AST-DYNAMIC-EXECUTION",
                path=path,
                message="Dynamic execution/import call detected in protected code scan.",
                line=call.line,
                column=call.column,
                role=role,
                observed_pattern=call.excerpt or call.name,
                vector=DriftVector.V1_UPWARD_MUTATION,
                protected_object="dynamic_execution",
                safer_form="Avoid eval/exec/compile/dynamic import in guard-protected code.",
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    if is_selection_call(call.name):
        findings.extend(
            validate_capability_use(
                path=path,
                role=role,
                capability=CapabilityName.SELECTION_FUNCTIONS,
                observed_pattern=call.excerpt or call.name,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    return findings


def findings_for_file_mutations(
    *,
    tree: ast.AST,
    source: str,
    aliases: Mapping[str, str],
    path: str,
    role: CodeRole,
    guard_id: str,
    guard_file: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        name = call_name_for_node(node, aliases)
        if name is None:
            continue

        if is_file_mutation_call(node, name):
            findings.extend(
                validate_capability_use(
                    path=path,
                    role=role,
                    capability=CapabilityName.FILE_WRITE,
                    observed_pattern=source_segment(source, node) or name,
                    guard_id=guard_id,
                    guard_file=guard_file,
                )
            )

    return findings


def findings_for_ontology_assignments(
    *,
    path: str,
    role: CodeRole,
    assignments: Iterable[AstAssignment],
    guard_id: str,
    guard_file: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for assignment in assignments:
        if not is_ontology_assignment(assignment.target):
            continue

        findings.append(
            ast_finding(
                rule_id="AST-ONTOLOGY-ASSIGNMENT",
                path=path,
                message="Assignment to ontology-facing symbol detected in protected code scan.",
                line=assignment.line,
                column=assignment.column,
                role=role,
                observed_pattern=assignment.excerpt,
                vector=DriftVector.V12_ONTOLOGY_CREEP,
                protected_object=assignment.target,
                safer_form="Do not assign to Φ/K(Φ)/κ/QE/Vortex/Projection/EK symbols in runtime code.",
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    return findings


def scan_python_source(
    *,
    path: Path | str,
    source: str,
    role: CodeRole | str | None = None,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
) -> AstScanResult:
    repo_path = normalize_repo_path(path)
    resolved_role = resolve_code_role(path=repo_path, text=source, explicit_role=role)

    tree, parse_findings = parse_python_source(repo_path, source)
    if tree is None:
        return AstScanResult(
            path=repo_path,
            role=resolved_role,
            imports={},
            calls=tuple(),
            assignments=tuple(),
            findings=tuple(parse_findings),
        )

    aliases = build_import_aliases(tree)
    calls = collect_calls(tree, source, aliases)
    assignments = collect_assignments(tree, source)

    findings: list[Finding] = list(parse_findings)

    for call in calls:
        findings.extend(
            findings_for_call(
                path=repo_path,
                role=resolved_role,
                call=call,
                guard_id=guard_id,
                guard_file=guard_file,
            )
        )

    findings.extend(
        findings_for_file_mutations(
            tree=tree,
            source=source,
            aliases=aliases,
            path=repo_path,
            role=resolved_role,
            guard_id=guard_id,
            guard_file=guard_file,
        )
    )

    findings.extend(
        findings_for_ontology_assignments(
            path=repo_path,
            role=resolved_role,
            assignments=assignments,
            guard_id=guard_id,
            guard_file=guard_file,
        )
    )

    return AstScanResult(
        path=repo_path,
        role=resolved_role,
        imports=dict
        )
    )
