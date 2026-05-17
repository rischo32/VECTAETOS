#!/usr/bin/env python3
"""
VECTAETOS MASTER INDEX ROUTER GUARD

Purpose:
- Treat VECTAETOS_MASTER_INDEX.md / MASTER_INDEX.md as a canonical router.
- Verify that every referenced /formal/... document exists on disk.
- Distinguish missing canonical documents from explicit TODO anchors.
- Generate a deterministic inventory of /formal and /anchors files.

This guard does not interpret ontology.
It only checks repository integrity.

Exit codes:
0 = OK
1 = BROKEN_ROUTER / inventory mismatch
2 = guard misuse or unreadable repository state
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_INDEX_CANDIDATES = (
    "VECTAETOS_MASTER_INDEX.md",
    "MASTER_INDEX.md",
)

DEFAULT_INVENTORY_ROOTS = (
    "formal",
    "anchors",
    "Core",
    "governance",
    "infrastructure",
    "research",
    "repo_root",
)

REFERENCE_RE = re.compile(
    r"(?P<quote>[`'\"]?)"
    r"(?P<path>/formal/[A-Za-z0-9_.Φφ\- /]+?\.(?:md|txt|pdf))"
    r"(?P=quote)"
)

TODO_MARKERS = (
    "TODO_ANCHOR",
    "TODO-FORMAL",
    "PLACEHOLDER_ANCHOR",
    "INTENTIONAL_PLACEHOLDER",
)


@dataclass(frozen=True)
class RouterReference:
    path: str
    line: int
    raw_line: str
    is_todo: bool

    @property
    def disk_path(self) -> Path:
        return Path(self.path.lstrip("/"))


@dataclass(frozen=True)
class InventoryItem:
    path: str
    size_bytes: int
    sha256: str


def find_master_index(repo_root: Path, explicit: str | None) -> Path:
    if explicit:
        candidate = repo_root / explicit
        if not candidate.is_file():
            raise FileNotFoundError(f"Master index not found: {candidate}")
        return candidate

    for name in DEFAULT_INDEX_CANDIDATES:
        candidate = repo_root / name
        if candidate.is_file():
            return candidate

    joined = ", ".join(DEFAULT_INDEX_CANDIDATES)
    raise FileNotFoundError(f"No master index found. Tried: {joined}")


def normalize_router_path(raw: str) -> str:
    path = raw.strip()
    path = re.sub(r"\s+", " ", path)
    path = path.replace(" ", "%20") if " " in path else path
    return path


def extract_formal_references(master_index: Path) -> list[RouterReference]:
    refs: list[RouterReference] = []

    try:
        lines = master_index.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Cannot read {master_index} as UTF-8") from exc

    for line_no, line in enumerate(lines, start=1):
        for match in REFERENCE_RE.finditer(line):
            raw_path = match.group("path")
            normalized = normalize_router_path(raw_path)
            is_todo = any(marker in line for marker in TODO_MARKERS)
            refs.append(
                RouterReference(
                    path=normalized,
                    line=line_no,
                    raw_line=line.strip(),
                    is_todo=is_todo,
                )
            )

    # Deterministic de-duplication: preserve first occurrence.
    seen: set[str] = set()
    unique: list[RouterReference] = []
    for ref in refs:
        if ref.path not in seen:
            seen.add(ref.path)
            unique.append(ref)

    return unique


def check_router(repo_root: Path, master_index: Path) -> int:
    refs = extract_formal_references(master_index)

    if not refs:
        print(f"BROKEN_ROUTER: no /formal references found in {master_index}")
        return 1

    missing: list[RouterReference] = []
    todo_missing: list[RouterReference] = []

    for ref in refs:
        disk_path = repo_root / ref.disk_path
        if not disk_path.exists():
            if ref.is_todo:
                todo_missing.append(ref)
            else:
                missing.append(ref)

    if missing:
        print("BROKEN_ROUTER: canonical /formal references are missing on disk")
        print()
        for ref in missing:
            print(f"- {master_index}:{ref.line} -> {ref.path}")
            print(f"  line: {ref.raw_line}")
        print()
        if todo_missing:
            print("TODO_ANCHOR references also missing, but classified separately:")
            for ref in todo_missing:
                print(f"- {master_index}:{ref.line} -> {ref.path}")
        return 1

    print("MASTER_INDEX_ROUTER_OK")
    print(f"index: {master_index}")
    print(f"formal references checked: {len(refs)}")

    if todo_missing:
        print()
        print("TODO_ANCHOR_MISSING:")
        for ref in todo_missing:
            print(f"- {master_index}:{ref.line} -> {ref.path}")

    return 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_inventory_files(repo_root: Path, roots: Sequence[str]) -> Iterable[Path]:
    for root_name in roots:
        root = repo_root / root_name
        if not root.exists():
            continue
        if root.is_file():
            yield root
            continue
        for path in root.rglob("*"):
            if path.is_file():
                yield path


def build_inventory(repo_root: Path, roots: Sequence[str]) -> list[InventoryItem]:
    items: list[InventoryItem] = []

    for path in iter_inventory_files(repo_root, roots):
        rel = path.relative_to(repo_root).as_posix()
        if rel.startswith(".git/"):
            continue
        items.append(
            InventoryItem(
                path=rel,
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
            )
        )

    return sorted(items, key=lambda item: item.path)


def render_inventory_markdown(items: Sequence[InventoryItem], roots: Sequence[str]) -> str:
    lines: list[str] = [
        "# VECTAETOS Repository Inventory",
        "",
        "Status: GENERATED INVENTORY",
        "Authority: None",
        "Role: Repository map only",
        "",
        "This file is generated by `guards/master_index_router_guard.py --mode inventory`.",
        "It does not redefine ontology, anchors, Φ, K(Φ), κ, QE, Vortex, audit, projection, or LLM role.",
        "",
        "## Roots",
        "",
    ]

    for root in roots:
        lines.append(f"- `{root}/`")

    lines.extend(
        [
            "",
            "## Files",
            "",
            "| Path | Size bytes | SHA-256 |",
            "|---|---:|---|",
        ]
    )

    for item in items:
        lines.append(f"| `{item.path}` | {item.size_bytes} | `{item.sha256}` |")

    lines.append("")
    return "\n".join(lines)


def write_or_print_inventory(repo_root: Path, roots: Sequence[str], output: str | None) -> int:
    items = build_inventory(repo_root, roots)
    rendered = render_inventory_markdown(items, roots)

    if output:
        output_path = repo_root / output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"INVENTORY_WRITTEN: {output_path}")
        print(f"files indexed: {len(items)}")
    else:
        print(rendered)

    return 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check VECTAETOS master index router integrity and generate inventories."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root. Default: current directory.",
    )
    parser.add_argument(
        "--index",
        default=None,
        help="Master index path. Default: VECTAETOS_MASTER_INDEX.md or MASTER_INDEX.md.",
    )
    parser.add_argument(
        "--mode",
        choices=("check", "inventory"),
        default="check",
        help="check = verify router; inventory = generate /formal + /anchors inventory.",
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        default=list(DEFAULT_INVENTORY_ROOTS),
        help="Roots to inventory. Default: formal anchors",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output markdown path for inventory mode. If omitted, prints to stdout.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()

    if not repo_root.exists():
        print(f"ERROR: repo root does not exist: {repo_root}", file=sys.stderr)
        return 2

    try:
        if args.mode == "check":
            master_index = find_master_index(repo_root, args.index)
            return check_router(repo_root, master_index)

        if args.mode == "inventory":
            return write_or_print_inventory(repo_root, tuple(args.roots), args.output)

        print(f"ERROR: unknown mode: {args.mode}", file=sys.stderr)
        return 2

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
