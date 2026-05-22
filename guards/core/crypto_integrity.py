# guards/core/crypto_integrity.py

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import hashlib
import json


class Severity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"


@dataclass(frozen=True)
class IntegrityFinding:
    id: str
    guard_id: str
    path: str
    expected_sha256: str
    observed_sha256: str
    severity: Severity
    vector: str
    message: str
    ontology_authority: bool = False
    auto_fix_allowed: bool = False


@dataclass(frozen=True)
class GuardManifestEntry:
    guard_id: str
    path: str
    sha256: str
    perimeter: str
    vectors: tuple[str, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> list[GuardManifestEntry]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    entries: list[GuardManifestEntry] = []
    for item in raw["guards"]:
        entries.append(
            GuardManifestEntry(
                guard_id=item["guard_id"],
                path=item["path"],
                sha256=item["sha256"],
                perimeter=item["perimeter"],
                vectors=tuple(item.get("vectors", ())),
            )
        )

    return entries


def verify_guard_entry(repo_root: Path, entry: GuardManifestEntry) -> IntegrityFinding | None:
    target = repo_root / entry.path

    if not target.exists():
        return IntegrityFinding(
            id=f"EK-INTEGRITY-MISSING-{entry.guard_id}",
            guard_id=entry.guard_id,
            path=entry.path,
            expected_sha256=entry.sha256,
            observed_sha256="<missing>",
            severity=Severity.BLOCKER,
            vector="V15_guard_runtime_integrity",
            message="Guard file is missing from sealed manifest path.",
        )

    observed = sha256_file(target)

    if observed != entry.sha256:
        return IntegrityFinding(
            id=f"EK-INTEGRITY-DRIFT-{entry.guard_id}",
            guard_id=entry.guard_id,
            path=entry.path,
            expected_sha256=entry.sha256,
            observed_sha256=observed,
            severity=Severity.BLOCKER,
            vector="V15_guard_runtime_integrity",
            message="Guard runtime bytes differ from sealed manifest.",
        )

    return None
