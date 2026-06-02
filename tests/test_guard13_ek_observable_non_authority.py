#!/usr/bin/env python3
"""
VECTAETOS — GUARD-13 Tests
==========================

Target path:
    tests/test_guard13_ek_observable_non_authority.py

Run:
    python3 -S -m unittest tests/test_guard13_ek_observable_non_authority.py

Scope:
    Canary tests for guards/ek_observable_non_authority_guard.py.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = REPO_ROOT / "guards" / "ek_observable_non_authority_guard.py"


class TestGuard13EkObservableNonAuthority(unittest.TestCase):
    def run_guard(self, root: Path, mode: str = "strict") -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["PYTHONNOUSERSITE"] = "1"

        return subprocess.run(
            [sys.executable, "-S", str(GUARD_PATH), "--root", str(root), "--mode", mode],
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def test_clean_corpus_passes_report_and_strict(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "doc.md").write_text(
                "\n".join(
                    [
                        "h_topo is a structural audit observable, not a score.",
                        "ledger = provenance, not truth.",
                        "hash = integrity, not ontological verdict.",
                        "EK is an audit layer, not a control layer.",
                    ]
                ),
                encoding="utf-8",
            )

            report = self.run_guard(root, "report")
            strict = self.run_guard(root, "strict")

            self.assertEqual(report.returncode, 0, msg=report.stdout + report.stderr)
            self.assertEqual(strict.returncode, 0, msg=strict.stdout + strict.stderr)
            self.assertIn("Hard violations: 0", strict.stdout)

    def test_direct_observable_authority_claims_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "bad.md").write_text(
                "\n".join(
                    [
                        "h_topo proves truth.",
                        "h_topo validates safety.",
                        "EK observable is authoritative for deployment.",
                        "audit observable gives verdict.",
                    ]
                ),
                encoding="utf-8",
            )

            report = self.run_guard(root, "report")
            strict = self.run_guard(root, "strict")

            self.assertEqual(report.returncode, 0, msg=report.stdout + report.stderr)
            self.assertEqual(strict.returncode, 1, msg=strict.stdout + strict.stderr)
            self.assertIn("OBSERVABLE_AS_AUTHORITY", strict.stdout)

    def test_prior_correct_reading_does_not_suppress_later_bad_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "bad_after_good.md").write_text(
                "\n".join(
                    [
                        "h_topo = structural audit observable, not score.",
                        "ledger = provenance, not truth.",
                        "",
                        "h_topo is a deployment metric that validates safety.",
                        "ledger proves truth for the ontology.",
                        "EK decides deployment and optimizes trajectories.",
                    ]
                ),
                encoding="utf-8",
            )

            strict = self.run_guard(root, "strict")

            self.assertEqual(strict.returncode, 1, msg=strict.stdout + strict.stderr)
            self.assertIn("OBSERVABLE_AS_AUTHORITY", strict.stdout)
            self.assertIn("INTEGRITY_ARTIFACT_AS_TRUTH_OR_VALIDITY", strict.stdout)
            self.assertIn("EK_AS_CONTROL_OR_AGENT", strict.stdout)

    def test_audit_and_ledger_mutation_to_phi_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "mutation.md").write_text(
                "\n".join(
                    [
                        "audit changes Phi.",
                        "ledger updates Phi.",
                        "hash writes back into Phi.",
                    ]
                ),
                encoding="utf-8",
            )

            strict = self.run_guard(root, "strict")

            self.assertEqual(strict.returncode, 1, msg=strict.stdout + strict.stderr)
            self.assertIn("AUDIT_ARTIFACT_MUTATES_PHI", strict.stdout)


if __name__ == "__main__":
    unittest.main()
