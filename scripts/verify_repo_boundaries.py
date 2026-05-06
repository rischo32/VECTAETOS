#!/usr/bin/env python3
"""
VECTAETOS :: Repository Boundary Verifier

Role:
- verifies that the VECTAETOS repository does not import downstream layers
- detects reverse imports from ASIMULATOR / ASI_MOD into the root repository
- does not mutate files
- does not modify ontology, Φ, K(Φ), κ, QE, Vortex, audit, or projection
- does not claim truth, safety, deployment validity, or L4 evidence

This is a repository verifier, not an ontological authority.

Python:
- 3.11+

Run from:
- repository root

Exit codes:
- 0 = no reverse downstream imports detected
- 1 = boundary violation detected
- 2 = execution/config error
"""

from __future__ import annotations

import argparse
import ast
import dataclasses
import re
import sys
from pathlib import Path
from typing import Iterable


VERSION = "0.2.0"

CODE_EXTENSIONS = {
    ".py",
}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "node_modules",
    "archive",
    ".runtime",
}

EXCLUDED_PATH_PARTS = {
    ("docs", "observatory"),
}

FILE_ALLOW_MARKERS = {
    "vectaetos-boundary-allow-file",
    "vectaetos-repo-boundary-allow-file",
}

LINE_ALLOW_MARKERS = {
    "vectaetos-boundary-allow",
    "vectaetos-repo-boundary-allow",
}

FORBIDDEN_ROOT_MODULES = {
    "asimulator",
    "asi_mod",
}

IMPORT_LINE_PATTERN = re.compile(
    r"^\s*(from|import)\s+(asimulator|asi_mod)\b",
    re.IGNORECASE | re.UNICODE,
)


@dataclasses.dataclass(frozen=True)
class Violation:
    path: Path
    line_no: int
    import_name: str
    text: str


def normalize_repo_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def has_file_allow_marker(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20]).lower()
    return any(marker in head for marker in FILE_ALLOW_MARKERS)


def has_line_allow_marker(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in LINE_ALLOW_MARKERS)


def is_path_excluded(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts

    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return True

    for excluded_parts in EXCLUDED_PATH_PARTS:
        if len(rel_parts) < len(excluded_parts):
            continue

        for idx in range(0, len(rel_parts) - len(excluded_parts) + 1):
            if tuple(rel_parts[idx : idx + len(excluded_parts)]) == excluded_parts:
                return True

    return False


def should_scan(path: Path, root: Path) -> bool:
    if not path.is_file():
        return False

    if is_path_excluded(path, root):
        return False

    return path.suffix.lower() in CODE_EXTENSIONS


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if should_scan(path, root):
            yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None
    except OSError as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}") from exc


def root_module(name: str) -> str:
    return name.split(".", 1)[0].lower()


def line_text(lines: list[str], line_no: int) -> str:
    if line_no <= 0 or line_no > len(lines):
        return ""
    return lines[line_no - 1].strip()


def scan_ast(path: Path, text: str) -> list[Violation]:
    lines = text.splitlines()
    tree = ast.parse(text, filename=str(path))

    violations: list[Violation] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_root = root_module(alias.name)

                if module_root not in FORBIDDEN_ROOT_MODULES:
                    continue

                original_line = line_text(lines, node.lineno)

                if has_line_allow_marker(original_line):
                    continue

                violations.append(
                    Violation(
                        path=path,
                        line_no=node.lineno,
                        import_name=alias.name,
                        text=original_line,
                    )
                )

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            module_root = root_module(node.module)

            if module_root not in FORBIDDEN_ROOT_MODULES:
                continue

            original_line = line_text(lines, node.lineno)

            if has_line_allow_marker(original_line):
                continue

            violations.append(
                Violation(
                    path=path,
                    line_no=node.lineno,
                    import_name=node.module,
                    text=original_line,
                )
            )

    return violations


def scan_import_lines_fallback(path: Path, text: str) -> list[Violation]:
    """
    Fallback scanner for syntactically invalid Python files.

    It only looks at actual import/from statements and ignores comments
    by checking the line prefix shape.
    """
    violations: list[Violation] = []

    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if has_line_allow_marker(stripped):
            continue

        match = IMPORT_LINE_PATTERN.search(line)
        if not match:
            continue

        violations.append(
            Violation(
                path=path,
                line_no=idx,
                import_name=match.group(2),
                text=stripped,
            )
        )

    return violations


def scan_file(path: Path) -> list[Violation]:
    text = read_text(path)
    if text is None:
        return []

    if has_file_allow_marker(text):
        return []

    try:
        return scan_ast(path, text)
    except SyntaxError:
        return scan_import_lines_fallback(path, text)


def print_report(violations: list[Violation], root: Path, scanned_count: int) -> None:
    print(f"VECTAETOS Repository Boundary Verifier v{VERSION}")
    print("===========================================")
    print(f"Scanned Python files: {scanned_count}")
    print(f"Violations:           {len(violations)}")
    print()

    if not violations:
        print("[OK] No reverse downstream imports detected.")
        return

    print("[ERROR] Repository boundary violations detected:")
    print()

    for violation in violations:
        rel = normalize_repo_path(violation.path, root)
        print(f"- {rel}:{violation.line_no}")
        print(f"  import: {violation.import_name}")
        print(f"  line:   {violation.text}")
        print(
            "  why:    VECTAETOS root repository must not import downstream "
            "ASIMULATOR / ASI_MOD layers."
        )
        print(
            "  use:    keep downstream dependencies outside the VECTAETOS root, "
            "or route through explicit non-authoritative interface contracts."
        )
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify VECTAETOS repository boundary imports."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current working directory.",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    violations: list[Violation] = []
    scanned_count = 0

    try:
        for path in iter_python_files(root):
            scanned_count += 1
            violations.extend(scan_file(path))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    violations.sort(key=lambda item: (str(item.path), item.line_no, item.import_name))

    print_report(violations, root, scanned_count)

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
