#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute SHA-256 of canonical anchor and write lock file."
    )
    parser.add_argument(
        "--input",
        default="anchors/CANONICAL_ANCHOR.md",
        help="Path to canonical anchor markdown file.",
    )
    parser.add_argument(
        "--output",
        default="anchors/CANONICAL_ANCHOR.sha256",
        help="Path to output SHA-256 file.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        return 1

    digest = sha256_file(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(digest + "\n", encoding="utf-8")

    print(f"[OK] SHA-256 written to: {output_path}")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
