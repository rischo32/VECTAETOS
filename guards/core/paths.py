#!/usr/bin/env python3
"""
VECTAETOS — Shared Guard Path Core

Role:
    Shared repository path normalization, role inference, and deterministic file
    iteration helpers for perimeter guards.

Boundary:
    This module classifies paths and exposes path-policy diagnostics.

    It does not decide ontology.
    It does not validate safety.
    It does not interpret anchors.
    It does not mutate repository files.
    It does not globally exclude repository areas by itself.

    Path exclusion from any guard must be declared by the calling guard or by a
    machine-readable contract. Exclusion from one guard is not exclusion from the
    whole perimeter.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import enum
from collections.abc import Iterable, Iterator
from pathlib import Path

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
except ModuleNotFoundError:
    # Allows direct local execution when cwd is guards/core or when tests import by path.
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


DEFAULT_GUARD_ID = "GUARD-19"
DEFAULT_GUARD_FILE = "guards/repo_path_guard.py"
SUPPORTED_CONTRACT_SCHEMA_VERSION = "1.0"


class PathPolicyError(RuntimeError):
    """
    Repository path policy error.

    This exception concerns path integrity only.
    It is not ontology.
    """


class PathRole(str, enum.Enum):
    ROOT = "root"
    ANCHOR = "anchor"
    FORMAL = "formal"
    GUARD = "guard"
    GUARD_CORE = "guard_core"
    CONTRACT = "contract"
    WORKFLOW = "workflow"
    TEST = "test"
    FIXTURE = "fixture"
    RESEARCH = "research"
    ARCHIVE = "archive"
    DOCS = "docs"
    KNOWLEDGE_BASE = "knowledge_base"
    PUBLIC = "public"
    SOURCE = "source"
    REQUIREMENTS = "requirements"
    CONFIG = "config"
    LICENSE = "license"
    UNKNOWN = "unknown"


TEXT_SUFFIXES = frozenset(
    {
        ".md",
        ".txt",
        ".py",
        ".json",
        ".jsonl",
        ".yml",
        ".yaml",
        ".toml",
        ".ini",
        ".cfg",
        ".html",
        ".css",
        ".js",
        ".mjs",
        ".cjs",
        ".ts",
        ".tsx",
        ".jsx",
        ".rst",
        ".csv",
        ".sh",
        ".bash",
        ".ps1",
        ".env.example",
        ".gitignore",
        ".gitattributes",
    }
)

BINARY_SUFFIXES = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".ico",
        ".pdf",
        ".zip",
        ".gz",
        ".tar",
        ".tgz",
        ".7z",
        ".woff",
        ".woff2",
        ".ttf",
        ".otf",
        ".eot",
        ".mp3",
        ".mp4",
        ".mov",
        ".avi",
        ".sqlite",
        ".db",
        ".pyc",
        ".pyo",
        ".so",
        ".dll",
        ".dylib",
    }
)

HEAVY_OR_GENERATED_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "dist",
        "build",
        "site",
        ".next",
        ".cache",
        ".tox",
        ".nox",
        "coverage",
        "htmlcov",
    }
)

ROOT_TEXT_FILES = frozenset(
    {
        "README.md",
        "LICENSE",
        "LICENSE.md",
        "NOTICE",
        "NOTICE.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "MASTER_INDEX.md",
        "VOCABULARY_LOCK.md",
        "GUARD_TABLE.md",
        "REQUIREMENTS.txt",
        "REQUIREMENTS-dev.txt",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "ruff.toml",
    }
)


@dataclasses.dataclass(frozen=True, slots=True)
class PathInfo:
    repo_path: str
    role: PathRole
    level: PerimeterLevel
    scope: PerimeterScope
    suffix: str
    parts: tuple[str, ...]
    is_text_candidate: bool
    is_binary_candidate: bool
    is_guard_core: bool
    is_fixture: bool
    is_archive: bool
    is_generated_or_heavy: bool


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def path_parts(repo_path: str | Path) -> tuple[str, ...]:
    normalized = normalize_repo_path(repo_path)
    if not normalized:
        return tuple()
    return tuple(part for part in normalized.split("/") if part)


def ensure_repo_relative(path: Path | str) -> str:
    normalized = normalize_repo_path(path)

    if not normalized:
        raise PathPolicyError("repository path must not be empty")

    candidate = Path(normalized)

    if candidate.is_absolute():
        raise PathPolicyError(f"repository path must be relative: {path}")

    if ".." in candidate.parts:
        raise PathPolicyError(f"repository path must not contain '..': {path}")

    return normalized


def resolve_under_root(root: Path | str, repo_relative_path: Path | str) -> Path:
    repo_path = ensure_repo_relative(repo_relative_path)

    root_resolved = Path(root).resolve()
    target = (root_resolved / repo_path).resolve()

    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise PathPolicyError(f"resolved path escapes repository root: {repo_path}") from exc

    return target


def infer_path_role(path: Path | str) -> PathRole:
    repo_path = normalize_repo_path(path)
    parts = path_parts(repo_path)

    if not parts:
        return PathRole.ROOT

    if len(parts) == 1 and parts[0] in ROOT_TEXT_FILES:
        if parts[0].casefold().startswith("license"):
            return PathRole.LICENSE
        if parts[0].casefold().startswith("requirements"):
            return PathRole.REQUIREMENTS
        return PathRole.ROOT

    if parts[0] == "anchors":
        return PathRole.ANCHOR

    if parts[0] == "formal":
        return PathRole.FORMAL

    if parts[0] == "guards":
        if len(parts) >= 2 and parts[1] == "core":
            return PathRole.GUARD_CORE
        return PathRole.GUARD

    if parts[0] == "contracts":
        return PathRole.CONTRACT

    if len(parts) >= 2 and parts[0] == ".github" and parts[1] == "workflows":
        return PathRole.WORKFLOW

    if parts[0] == ".github":
        return PathRole.CONFIG

    if parts[0] == "tests":
        if "fixtures" in parts:
            return PathRole.FIXTURE
        return PathRole.TEST

    if "fixtures" in parts:
        return PathRole.FIXTURE

    if parts[0] == "research":
        return PathRole.RESEARCH

    if parts[0] in {"archive", "docs/archive"}:
        return PathRole.ARCHIVE

    if parts[0] == "docs":
        return PathRole.DOCS

    if parts[0] in {"knowledge-base", "knowledge_base"}:
        return PathRole.KNOWLEDGE_BASE

    if parts[0] in {"public", "site", "web"}:
        return PathRole.PUBLIC

    if parts[0] in {"src", "Core", "core", "scripts", "tools", "ek_core"}:
        return PathRole.SOURCE

    if parts[0] in {".config", "config"}:
        return PathRole.CONFIG

    return PathRole.UNKNOWN


def level_for_path_role(role: PathRole) -> PerimeterLevel:
    if role in {
        PathRole.ROOT,
        PathRole.ANCHOR,
        PathRole.FORMAL,
        PathRole.GUARD,
        PathRole.GUARD_CORE,
        PathRole.CONTRACT,
        PathRole.WORKFLOW,
        PathRole.REQUIREMENTS,
        PathRole.CONFIG,
        PathRole.LICENSE,
    }:
        return PerimeterLevel.LEVEL_0

    if role in {PathRole.SOURCE}:
        return PerimeterLevel.LEVEL_3

    if role in {PathRole.PUBLIC}:
        return PerimeterLevel.LEVEL_5

    if role in {PathRole.RESEARCH, PathRole.DOCS, PathRole.KNOWLEDGE_BASE}:
        return PerimeterLevel.LEVEL_2

    if role in {PathRole.TEST, PathRole.FIXTURE}:
        return PerimeterLevel.LEVEL_5

    if role == PathRole.ARCHIVE:
        return PerimeterLevel.LEVEL_2

    return PerimeterLevel.LEVEL_0


def scope_for_path_role(role: PathRole) -> PerimeterScope:
    level = level_for_path_role(role)

    if level == PerimeterLevel.LEVEL_0:
        return PerimeterScope.FUNDAMENTAL_REPOSITORY
    if level == PerimeterLevel.LEVEL_1:
        return PerimeterScope.SPECIALIZED_ONTOLOGICAL
    if level == PerimeterLevel.LEVEL_2:
        return PerimeterScope.SEMANTIC_VOCABULARY
    if level == PerimeterLevel.LEVEL_3:
        return PerimeterScope.CODE_BEHAVIOR
    if level == PerimeterLevel.LEVEL_4:
        return PerimeterScope.BRIDGE_PROJECTION_TRACE
    if level == PerimeterLevel.LEVEL_5:
        return PerimeterScope.RUNTIME_EVIDENCE_RELEASE

    return PerimeterScope.FUNDAMENTAL_REPOSITORY


def is_text_candidate_path(path: Path | str) -> bool:
    repo_path = normalize_repo_path(path)
    name = Path(repo_path).name
    suffix = Path(repo_path).suffix.lower()

    if name in ROOT_TEXT_FILES:
        return True

    if suffix in TEXT_SUFFIXES:
        return True

    return False


def is_binary_candidate_path(path: Path | str) -> bool:
    return Path(normalize_repo_path(path)).suffix.lower() in BINARY_SUFFIXES


def should_skip_heavy_dir(path: Path | str) -> bool:
    parts = path_parts(normalize_repo_path(path))
    return any(part in HEAVY_OR_GENERATED_DIR_NAMES for part in parts)


def describe_path(path: Path | str) -> PathInfo:
    repo_path = normalize_repo_path(path)
    role = infer_path_role(repo_path)
    suffix = Path(repo_path).suffix.lower()
    parts = path_parts(repo_path)

    return PathInfo(
        repo_path=repo_path,
        role=role,
        level=level_for_path_role(role),
        scope=scope_for_path_role(role),
        suffix=suffix,
        parts=parts,
        is_text_candidate=is_text_candidate_path(repo_path),
        is_binary_candidate=is_binary_candidate_path(repo_path),
        is_guard_core=role == PathRole.GUARD_CORE,
        is_fixture=role == PathRole.FIXTURE,
        is_archive=role == PathRole.ARCHIVE,
        is_generated_or_heavy=should_skip_heavy_dir(repo_path),
    )


def iter_repo_files(
    root: Path | str,
    *,
    text_only: bool = False,
    include_binary: bool = False,
    skip_heavy_dirs: bool = True,
    extra_skip_dir_names: Iterable[str] = (),
) -> Iterator[Path]:
    """
    Iterate repository files deterministically.

    This helper only applies technical traversal skips for generated/dependency
    directories when requested. Semantic inclusion/exclusion remains the caller's
    responsibility.
    """

    root_path = Path(root)
    extra_skip = frozenset(extra_skip_dir_names)

    for path in sorted(root_path.rglob("*")):
        if path.is_dir():
            continue

        try:
            rel = path.relative_to(root_path).as_posix()
        except ValueError:
            rel = normalize_repo_path(path)

        parts = path_parts(rel)

        if skip_heavy_dirs and any(part in HEAVY_OR_GENERATED_DIR_NAMES for part in parts):
            continue

        if extra_skip and any(part in extra_skip for part in parts):
            continue

        if text_only and not is_text_candidate_path(rel):
            continue

        if not include_binary and is_binary_candidate_path(rel):
            continue

        yield path


def path_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    severity: Severity | str = Severity.BLOCKER,
    confidence: Confidence | str = Confidence.HIGH,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
    observed_pattern: str | None = None,
    protected_object: str | None = "repo_path",
    safer_form: str | None = None,
) -> Finding:
    info = describe_path(path)

    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=PerimeterLevel.LEVEL_0,
        scope=PerimeterScope.FUNDAMENTAL_REPOSITORY,
        vector=DriftVector.V6_PATH_STATUS_LAUNDERING,
        severity=severity,
        confidence=confidence,
        path=normalize_repo_path(path),
        message=message,
        role=info.role.value,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.STRICT,
        integrity_posture=IntegrityPosture.PATH_POLICY_READ_ONLY,
        safer_form=safer_form,
    )


def validate_repo_path(
    path: Path | str,
    *,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
) -> list[Finding]:
    try:
        ensure_repo_relative(path)
    except PathPolicyError as exc:
        return [
            path_finding(
                rule_id="PATH-INVALID",
                path=path,
                message=str(exc),
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
            )
        ]

    return []


def validate_paths(
    paths: Iterable[Path | str],
    *,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    contract_schema_version: str = SUPPORTED_CONTRACT_SCHEMA_VERSION,
) -> list[Finding]:
    findings: list[Finding] = []

    for path in paths:
        findings.extend(
            validate_repo_path(
                path,
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
            )
        )

    return findings


def info_to_dict(info: PathInfo) -> dict[str, object]:
    return {
        "repo_path": info.repo_path,
        "role": info.role.value,
        "level": info.level.value,
        "scope": info.scope.value,
        "suffix": info.suffix,
        "parts": list(info.parts),
        "is_text_candidate": info.is_text_candidate,
        "is_binary_candidate": info.is_binary_candidate,
        "is_guard_core": info.is_guard_core,
        "is_fixture": info.is_fixture,
        "is_archive": info.is_archive,
        "is_generated_or_heavy": info.is_generated_or_heavy,
    }


__all__ = [
    "DEFAULT_GUARD_ID",
    "DEFAULT_GUARD_FILE",
    "SUPPORTED_CONTRACT_SCHEMA_VERSION",
    "PathPolicyError",
    "PathRole",
    "TEXT_SUFFIXES",
    "BINARY_SUFFIXES",
    "HEAVY_OR_GENERATED_DIR_NAMES",
    "ROOT_TEXT_FILES",
    "PathInfo",
    "normalize_repo_path",
    "path_parts",
    "ensure_repo_relative",
    "resolve_under_root",
    "infer_path_role",
    "level_for_path_role",
    "scope_for_path_role",
    "is_text_candidate_path",
    "is_binary_candidate_path",
    "should_skip_heavy_dir",
    "describe_path",
    "iter_repo_files",
    "path_finding",
    "validate_repo_path",
    "validate_paths",
    "info_to_dict",
]
