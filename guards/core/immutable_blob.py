from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


class AnchorIntegrityError(RuntimeError):
    pass


@dataclass(frozen=True)
class BlobHash:
    path: str
    sha256: str
    size: int
    role: str
    perimeter: str


@dataclass(frozen=True)
class AnchorIntegrityFinding:
    id: str
    path: str
    expected_sha256: str | None
    observed_sha256: str | None
    severity: str
    vector: str
    message: str
    ontology_authority: bool = False
    auto_fix_allowed: bool = False


class AnchorIntegrity:
    def __init__(self, repo_root: Path, manifest_path: Path):
        self.repo_root = repo_root.resolve()
        self.manifest_path = self._resolve_inside_repo(manifest_path)
        self.known_blobs = self._load_manifest()

    def _resolve_inside_repo(self, path: Path) -> Path:
        resolved = path.resolve()
        if not resolved.is_relative_to(self.repo_root):
            raise AnchorIntegrityError(f"Path escapes repository root: {path}")
        return resolved

    @staticmethod
    def _sha256_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _sha256_file(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _load_manifest(self) -> dict[str, BlobHash]:
        if not self.manifest_path.exists():
            raise AnchorIntegrityError(
                f"MANIFEST MISSING: {self.manifest_path}. Cannot verify anchors."
            )

        raw_bytes = self.manifest_path.read_bytes()

        # TODO: verify detached Ed25519 / Sigstore signature here.
        # The public verification key must be pinned outside the manifest.
        raw = json.loads(raw_bytes.decode("utf-8"))

        blobs: dict[str, BlobHash] = {}
        for item in raw.get("blobs", []):
            blob = BlobHash(**item)
            if blob.path in blobs:
                raise AnchorIntegrityError(f"Duplicate manifest entry: {blob.path}")
            blobs[blob.path] = blob

        if not blobs:
            raise AnchorIntegrityError("Manifest contains no protected blobs.")

        return blobs

    def verify_one(self, rel_path: str) -> AnchorIntegrityFinding | None:
        if rel_path not in self.known_blobs:
            return AnchorIntegrityFinding(
                id="P0-UNTRACKED-ANCHOR",
                path=rel_path,
                expected_sha256=None,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor path is not tracked in integrity manifest.",
            )

        expected = self.known_blobs[rel_path]
        target = self._resolve_inside_repo(self.repo_root / rel_path)

        if not target.exists():
            return AnchorIntegrityFinding(
                id="P0-MISSING-ANCHOR",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Tracked anchor file is missing.",
            )

        if target.is_symlink():
            return AnchorIntegrityFinding(
                id="P0-SYMLINK-ANCHOR",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=None,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Protected anchor path is a symlink.",
            )

        observed_hash = self._sha256_file(target)
        observed_size = target.stat().st_size

        if observed_hash != expected.sha256:
            return AnchorIntegrityFinding(
                id="P0-ANCHOR-HASH-MISMATCH",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=observed_hash,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor bytes differ from integrity manifest.",
            )

        if observed_size != expected.size:
            return AnchorIntegrityFinding(
                id="P0-ANCHOR-SIZE-MISMATCH",
                path=rel_path,
                expected_sha256=expected.sha256,
                observed_sha256=observed_hash,
                severity="BLOCKER",
                vector="V14_anchor_integrity_drift",
                message="Anchor size differs from integrity manifest.",
            )

        return None

    def verify_all(self) -> list[AnchorIntegrityFinding]:
        findings: list[AnchorIntegrityFinding] = []
        for rel_path in sorted(self.known_blobs):
            finding = self.verify_one(rel_path)
            if finding is not None:
                findings.append(finding)
        return findings
