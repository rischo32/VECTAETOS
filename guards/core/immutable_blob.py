#!/usr/bin/env python3
"""
VECTAETOS — Immutable Blob Integrity Core

Role:
    Shared read-only byte-integrity helpers for canonical anchors, guard runtime
    manifests, and other repository perimeter blobs.

Boundary:
    This module verifies bytes, not truth.

    It does not define ontology, prove semantic validity, validate safety,
    authorize deployment, interpret anchors, mutate Φ, modify files, quarantine
    files, revert git state, notify external systems, or decide repository truth.

Python:
    3.11+

Dependencies:
    standard library only
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

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
    from guards.core.perimeter import EnforcementMode, enum_value
except ModuleNotFoundError:
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
    from perimeter import EnforcementMode, enum_value  # type: ignore


SUPPORTED_SCHEMA_VERSION = "1.0"
DEFAULT_HASH_ALGORITHM = "sha256"
DEFAULT_MANIFEST_ROLE = "anchor_blob_integrity"

DEFAULT_GUARD_ID = "GUARD-24"
DEFAULT_GUARD_FILE = "guards/anchor_blob_integrity_guard.py"

READ_CHUNK_SIZE = 1024 * 1024


class BlobIntegrityError(RuntimeError):
    """
    Infrastructure-level integrity error.

    This exception is for guard infrastructure flow only.
    It is not ontology.
    """


@dataclasses.dataclass(frozen=True, slots=True)
class BlobDigest:
    path: str
    size: int
    sha256: str
    sha3_512: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class BlobRecord:
    path: str
    sha256: str
    size: int
    role: str = "tracked_blob"
    sha3_512: str | None = None
    anchor_ref: str | None = None
    notes: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class BlobManifest:
    schema_version: str
    manifest_role: str
    hash_algorithm: str
    blobs: tuple[BlobRecord, ...]

    def by_path(self) -> dict[str, BlobRecord]:
        return {record.path: record for record in self.blobs}


def enum_schema_value(value: Any) -> Any:
    """
    Return stable schema value for enum-like inputs.

    Retained for backwards compatibility with earlier immutable_blob versions.
    """

    return enum_value(value)


def normalize_repo_path(path: Path | str) -> str:
    value = str(path).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return value


def ensure_relative_repo_path(path: str | Path) -> str:
    normalized = normalize_repo_path(path)

    if not normalized:
        raise BlobIntegrityError("manifest blob path must not be empty")

    candidate = Path(normalized)

    if candidate.is_absolute():
        raise BlobIntegrityError(f"manifest blob path must be repo-relative: {path}")

    if ".." in candidate.parts:
        raise BlobIntegrityError(f"manifest blob path must not contain '..': {path}")

    return normalized


def resolve_under_root(root: Path | str, repo_relative_path: Path | str) -> Path:
    repo_path = ensure_relative_repo_path(repo_relative_path)

    root_resolved = Path(root).resolve()
    target = (root_resolved / repo_path).resolve()

    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise BlobIntegrityError(
            f"resolved path escapes repository root: {repo_path}"
        ) from exc

    return target


def hash_file(path: Path | str, *, include_sha3_512: bool = False) -> BlobDigest:
    """
    Return byte digest for a single file.

    The digest is a byte-integrity observable only.
    It is not semantic truth and not ontology.
    """

    source = Path(path)
    sha256 = hashlib.sha256()
    sha3_512 = hashlib.sha3_512() if include_sha3_512 else None
    size = 0

    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(READ_CHUNK_SIZE), b""):
            size += len(chunk)
            sha256.update(chunk)
            if sha3_512 is not None:
                sha3_512.update(chunk)

    return BlobDigest(
        path=normalize_repo_path(source),
        size=size,
        sha256=sha256.hexdigest(),
        sha3_512=sha3_512.hexdigest() if sha3_512 is not None else None,
    )


def validate_sha256(value: str, *, context: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 64 or any(char not in "0123456789abcdef" for char in normalized):
        raise BlobIntegrityError(f"{context} has invalid sha256")
    return normalized


def validate_sha3_512(value: str, *, context: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 128 or any(char not in "0123456789abcdef" for char in normalized):
        raise BlobIntegrityError(f"{context} has invalid sha3_512")
    return normalized


def optional_text(raw: Mapping[str, Any], key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def record_from_mapping(raw: Mapping[str, Any], *, index: int) -> BlobRecord:
    required = ("path", "sha256", "size")
    for key in required:
        if key not in raw:
            raise BlobIntegrityError(
                f"manifest blob #{index} missing required field: {key}"
            )

    path = ensure_relative_repo_path(raw["path"])
    sha256 = validate_sha256(str(raw["sha256"]), context=f"manifest blob #{index}: {path}")

    try:
        size = int(raw["size"])
    except (TypeError, ValueError) as exc:
        raise BlobIntegrityError(
            f"manifest blob #{index} has invalid size: {path}"
        ) from exc

    if size < 0:
        raise BlobIntegrityError(f"manifest blob #{index} has negative size: {path}")

    sha3_512_value = raw.get("sha3_512")
    sha3_512 = None
    if sha3_512_value is not None:
        sha3_512 = validate_sha3_512(
            str(sha3_512_value),
            context=f"manifest blob #{index}: {path}",
        )

    return BlobRecord(
        path=path,
        sha256=sha256,
        size=size,
        role=str(raw.get("role", "tracked_blob")).strip() or "tracked_blob",
        sha3_512=sha3_512,
        anchor_ref=optional_text(raw, "anchor_ref"),
        notes=optional_text(raw, "notes"),
    )


def load_manifest(manifest_path: Path | str) -> BlobManifest:
    source = Path(manifest_path)

    if not source.exists():
        raise BlobIntegrityError(f"manifest missing: {normalize_repo_path(source)}")

    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BlobIntegrityError(
            f"manifest invalid JSON: {normalize_repo_path(source)}"
        ) from exc
    except OSError as exc:
        raise BlobIntegrityError(
            f"manifest unreadable: {normalize_repo_path(source)}"
        ) from exc

    if not isinstance(raw, dict):
        raise BlobIntegrityError("manifest root must be a JSON object")

    schema_version = str(raw.get("schema_version", "")).strip()
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        raise BlobIntegrityError(
            f"manifest schema_version must be {SUPPORTED_SCHEMA_VERSION!r}, "
            f"got {schema_version!r}"
        )

    manifest_role = str(raw.get("manifest_role", "")).strip()
    if not manifest_role:
        raise BlobIntegrityError("manifest_role is required")

    hash_algorithm = str(raw.get("hash_algorithm", DEFAULT_HASH_ALGORITHM)).strip().lower()
    if hash_algorithm != DEFAULT_HASH_ALGORITHM:
        raise BlobIntegrityError(
            f"unsupported hash_algorithm {hash_algorithm!r}; "
            f"supported: {DEFAULT_HASH_ALGORITHM!r}"
        )

    blob_items = raw.get("blobs")
    if not isinstance(blob_items, list):
        raise BlobIntegrityError("manifest field 'blobs' must be a list")

    records: list[BlobRecord] = []
    seen: set[str] = set()

    for index, item in enumerate(blob_items):
        if not isinstance(item, dict):
            raise BlobIntegrityError(f"manifest blob #{index} must be an object")

        record = record_from_mapping(item, index=index)

        if record.path in seen:
            raise BlobIntegrityError(f"duplicate manifest blob path: {record.path}")

        seen.add(record.path)
        records.append(record)

    return BlobManifest(
        schema_version=schema_version,
        manifest_role=manifest_role,
        hash_algorithm=hash_algorithm,
        blobs=tuple(records),
    )


def blob_finding(
    *,
    rule_id: str,
    path: Path | str,
    message: str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    severity: Severity | str = Severity.BLOCKER,
    confidence: Confidence | str = Confidence.HIGH,
    observed_pattern: str | None = None,
    protected_object: str | None = None,
    contract_schema_version: str = SUPPORTED_SCHEMA_VERSION,
    anchor_ref: str | None = None,
    contract_ref: str | None = None,
    safer_form: str | None = None,
) -> Finding:
    return make_finding(
        guard_id=guard_id,
        guard_file=guard_file,
        rule_id=rule_id,
        contract_schema_version=contract_schema_version,
        level=PerimeterLevel.LEVEL_0,
        scope=PerimeterScope.FUNDAMENTAL_REPOSITORY,
        vector=DriftVector.V14_ANCHOR_INTEGRITY_DRIFT,
        severity=severity,
        confidence=confidence,
        path=normalize_repo_path(path),
        message=message,
        protected_object=protected_object,
        observed_pattern=observed_pattern,
        evidence_class_allowed=EvidenceClass.E1_STATIC_SCAN,
        enforcement_mode=EnforcementMode.STRICT,
        anchor_ref=anchor_ref,
        contract_ref=contract_ref,
        safer_form=safer_form,
        integrity_posture=IntegrityPosture.BYTE_INTEGRITY_READ_ONLY,
    )


def verify_blob(
    *,
    root: Path | str,
    record: BlobRecord,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    contract_schema_version: str = SUPPORTED_SCHEMA_VERSION,
    contract_ref: str | None = None,
) -> list[Finding]:
    """
    Verify one manifest record against repository bytes.

    Returns findings instead of mutating files.
    """

    repo_root = Path(root)
    findings: list[Finding] = []

    try:
        target = resolve_under_root(repo_root, record.path)
    except BlobIntegrityError as exc:
        return [
            blob_finding(
                rule_id="BLOB-PATH-INVALID",
                path=record.path,
                message=str(exc),
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
            )
        ]

    if not target.exists():
        return [
            blob_finding(
                rule_id="BLOB-MISSING",
                path=record.path,
                message="Tracked blob is missing from repository working tree.",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
                safer_form=(
                    "Restore the tracked file or update the manifest through "
                    "reviewed human process."
                ),
            )
        ]

    if not target.is_file():
        return [
            blob_finding(
                rule_id="BLOB-NOT-FILE",
                path=record.path,
                message="Tracked blob path exists but is not a regular file.",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
            )
        ]

    try:
        actual = hash_file(target, include_sha3_512=record.sha3_512 is not None)
    except OSError as exc:
        return [
            blob_finding(
                rule_id="BLOB-UNREADABLE",
                path=record.path,
                message=f"Tracked blob could not be read: {exc}",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
            )
        ]

    if actual.size != record.size:
        findings.append(
            blob_finding(
                rule_id="BLOB-SIZE-MISMATCH",
                path=record.path,
                message="Tracked blob size differs from manifest.",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
                observed_pattern=(
                    f"expected_size={record.size}; actual_size={actual.size}"
                ),
                safer_form=(
                    "Review the file bytes and update manifest only through "
                    "explicit human review."
                ),
            )
        )

    if actual.sha256 != record.sha256:
        findings.append(
            blob_finding(
                rule_id="BLOB-SHA256-MISMATCH",
                path=record.path,
                message="Tracked blob SHA-256 differs from manifest.",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
                observed_pattern=(
                    f"expected_sha256={record.sha256}; actual_sha256={actual.sha256}"
                ),
                safer_form=(
                    "Treat as repository-state integrity drift; do not infer "
                    "semantic truth or falsehood from the hash."
                ),
            )
        )

    if record.sha3_512 is not None and actual.sha3_512 != record.sha3_512:
        findings.append(
            blob_finding(
                rule_id="BLOB-SHA3-512-MISMATCH",
                path=record.path,
                message="Tracked blob SHA3-512 differs from manifest.",
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=contract_schema_version,
                anchor_ref=record.anchor_ref,
                contract_ref=contract_ref,
                protected_object=record.role,
                observed_pattern=(
                    f"expected_sha3_512={record.sha3_512}; "
                    f"actual_sha3_512={actual.sha3_512}"
                ),
                safer_form=(
                    "Treat as repository-state integrity drift; do not infer "
                    "semantic truth or falsehood from the hash."
                ),
            )
        )

    return findings


def verify_manifest(
    *,
    root: Path | str,
    manifest_path: Path | str,
    guard_id: str = DEFAULT_GUARD_ID,
    guard_file: str = DEFAULT_GUARD_FILE,
    contract_schema_version: str = SUPPORTED_SCHEMA_VERSION,
    contract_ref: str | None = None,
) -> list[Finding]:
    """
    Verify all blobs in a manifest.

    This function is read-only. It never modifies repository files.
    """

    manifest_ref = contract_ref or normalize_repo_path(manifest_path)

    try:
        manifest = load_manifest(manifest_path)
    except BlobIntegrityError as exc:
        return [
            blob_finding(
                rule_id="BLOB-MANIFEST-INVALID",
                path=manifest_path,
                message=str(exc),
                guard_id=guard_id,
                guard_file=guard_file,
                severity=Severity.BLOCKER,
                confidence=Confidence.HIGH,
                protected_object="blob_manifest",
                contract_schema_version=contract_schema_version,
                contract_ref=manifest_ref,
                safer_form=(
                    "Restore or regenerate manifest through explicit "
                    "human-reviewed process."
                ),
            )
        ]

    findings: list[Finding] = []
    for record in manifest.blobs:
        findings.extend(
            verify_blob(
                root=root,
                record=record,
                guard_id=guard_id,
                guard_file=guard_file,
                contract_schema_version=manifest.schema_version,
                contract_ref=manifest_ref,
            )
        )

    return findings


def manifest_record_for_file(
    *,
    root: Path | str,
    path: Path | str,
    role: str = "tracked_blob",
    anchor_ref: str | None = None,
    notes: str | None = None,
    include_sha3_512: bool = False,
) -> BlobRecord:
    """
    Build a manifest record from current repository bytes.

    This helper does not write a manifest.
    The caller must decide whether to store the generated record.
    """

    repo_root = Path(root)
    repo_path = ensure_relative_repo_path(path)
    target = resolve_under_root(repo_root, repo_path)

    if not target.exists() or not target.is_file():
        raise BlobIntegrityError(
            f"cannot create manifest record for missing/non-file path: {repo_path}"
        )

    digest = hash_file(target, include_sha3_512=include_sha3_512)

    return BlobRecord(
        path=repo_path,
        sha256=digest.sha256,
        size=digest.size,
        role=role,
        sha3_512=digest.sha3_512,
        anchor_ref=anchor_ref,
        notes=notes,
    )


def manifest_to_dict(manifest: BlobManifest) -> dict[str, Any]:
    return {
        "schema_version": manifest.schema_version,
        "manifest_role": manifest.manifest_role,
        "hash_algorithm": manifest.hash_algorithm,
        "blobs": [
            {
                key: value
                for key, value in dataclasses.asdict(record).items()
                if value is not None
            }
            for record in manifest.blobs
        ],
    }


def build_manifest(
    *,
    root: Path | str,
    paths: Iterable[Path | str],
    manifest_role: str = DEFAULT_MANIFEST_ROLE,
    role: str = "canonical_anchor",
    include_sha3_512: bool = False,
) -> BlobManifest:
    records = [
        manifest_record_for_file(
            root=root,
            path=path,
            role=role,
            include_sha3_512=include_sha3_512,
        )
        for path in sorted(normalize_repo_path(item) for item in paths)
    ]

    return BlobManifest(
        schema_version=SUPPORTED_SCHEMA_VERSION,
        manifest_role=manifest_role,
        hash_algorithm=DEFAULT_HASH_ALGORITHM,
        blobs=tuple(records),
    )


def render_manifest_json(manifest: BlobManifest) -> str:
    return (
        json.dumps(
            manifest_to_dict(manifest),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


__all__ = [
    "SUPPORTED_SCHEMA_VERSION",
    "DEFAULT_HASH_ALGORITHM",
    "DEFAULT_MANIFEST_ROLE",
    "DEFAULT_GUARD_ID",
    "DEFAULT_GUARD_FILE",
    "READ_CHUNK_SIZE",
    "BlobIntegrityError",
    "BlobDigest",
    "BlobRecord",
    "BlobManifest",
    "enum_schema_value",
    "normalize_repo_path",
    "ensure_relative_repo_path",
    "resolve_under_root",
    "hash_file",
    "validate_sha256",
    "validate_sha3_512",
    "optional_text",
    "record_from_mapping",
    "load_manifest",
    "blob_finding",
    "verify_blob",
    "verify_manifest",
    "manifest_record_for_file",
    "manifest_to_dict",
    "build_manifest",
    "render_manifest_json",
]
