#!/usr/bin/env python3
"""
VECTAETOS — EK Core Phi/EK Tests
================================

Target path:
    tests/test_ek_core_phi_ek_core.py

Run:
    python3 -S -m unittest discover -s tests -p "test_*.py"

Scope:
    Deterministic behavior tests for ek_core/vectaetos_phi_ek_core.py.

These tests verify mechanical audit behavior only.

They do not:
    - validate truth,
    - validate K(Φ),
    - validate κ,
    - claim safety,
    - select trajectories,
    - control a Vortex,
    - treat h_topo as a score,
    - treat ledger/hash as ontological verdict.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = REPO_ROOT / "ek_core" / "vectaetos_phi_ek_core.py"


def load_core_module() -> ModuleType:
    """
    Load ek_core/vectaetos_phi_ek_core.py directly from file.

    This avoids relying on PYTHONPATH and keeps the test compatible with:
        python3 -S -m unittest discover -s tests -p "test_*.py"
    """
    if not CORE_PATH.exists():
        raise AssertionError(f"Missing EK core file: {CORE_PATH}")

    spec = importlib.util.spec_from_file_location("vectaetos_phi_ek_core_under_test", CORE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot create import spec for: {CORE_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CORE = load_core_module()


class TestPhiEkCoreStructure(unittest.TestCase):
    """Mechanical structure and shape invariants."""

    def test_canonical_edge_and_triangle_counts(self) -> None:
        self.assertEqual(len(CORE.canonical_edges()), 28)
        self.assertEqual(len(CORE.canonical_triangles()), 56)

    def test_sigma_order_is_canonical_8(self) -> None:
        self.assertEqual(
            CORE.SIGMA_ORDER,
            ("INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE"),
        )

    def test_sample_R_is_valid_so8_shape(self) -> None:
        matrix = CORE.sample_R()
        validated = CORE.validate_R(matrix)

        self.assertEqual(len(validated), 8)
        for row in validated:
            self.assertEqual(len(row), 8)

        for i in range(8):
            self.assertEqual(validated[i][i], 0.0)

        for i, j in CORE.canonical_edges():
            self.assertAlmostEqual(validated[i][j], -validated[j][i], places=12)


class TestPhiEkCoreValidation(unittest.TestCase):
    """Fail-fast checks for malformed relational matrices."""

    def test_rejects_non_8x8_matrix(self) -> None:
        with self.assertRaises(CORE.VectaetosInputError):
            CORE.validate_R([[0.0]])

    def test_rejects_non_numeric_value(self) -> None:
        matrix = CORE.sample_R()
        matrix[0][1] = "not-a-number"

        with self.assertRaises(CORE.VectaetosInputError):
            CORE.validate_R(matrix)

    def test_rejects_nonzero_diagonal(self) -> None:
        matrix = CORE.sample_R()
        matrix[3][3] = 0.25

        with self.assertRaises(CORE.VectaetosInputError):
            CORE.validate_R(matrix)

    def test_rejects_broken_antisymmetry(self) -> None:
        matrix = CORE.sample_R()
        matrix[0][1] = 1.0
        matrix[1][0] = 1.0

        with self.assertRaises(CORE.VectaetosInputError):
            CORE.validate_R(matrix)


class TestPhiEkCoreObservables(unittest.TestCase):
    """Audit observable checks. These values are not ontological verdicts."""

    def test_delta_has_56_cycles_and_is_deterministic(self) -> None:
        matrix = CORE.sample_R()

        delta_1 = CORE.compute_delta(matrix)
        delta_2 = CORE.compute_delta(matrix)

        self.assertEqual(len(delta_1), 56)
        self.assertEqual(delta_1, delta_2)
        self.assertEqual(delta_1[0]["indices"], [0, 1, 2])
        self.assertEqual(delta_1[0]["labels"], ["INT", "LEX", "VER"])

    def test_T_EK_sum_is_one_for_nonzero_sample(self) -> None:
        matrix = CORE.sample_R()
        t_ek = CORE.compute_T_EK(matrix)

        self.assertEqual(len(t_ek), 8)
        self.assertAlmostEqual(sum(t_ek), 1.0, places=12)

    def test_zero_matrix_observables_are_defined_without_authority(self) -> None:
        zero = [[0.0 for _ in range(8)] for _ in range(8)]

        t_ek = CORE.compute_T_EK(zero)
        chi = CORE.compute_chi(zero)
        c_ek = CORE.compute_C_EK(chi)
        mu = CORE.compute_mu(t_ek, c_ek)
        a_ek = CORE.compute_A_EK(mu)
        h_topo = CORE.compute_h_topo(mu, a_ek)

        self.assertEqual(t_ek, [0.0] * 8)
        self.assertEqual(chi, [0.0] * 8)
        self.assertEqual(c_ek, [1.0] * 8)
        self.assertEqual(mu, [0.0] * 8)
        self.assertEqual(h_topo, 0.0)

    def test_record_contains_boundary_non_authority_flags(self) -> None:
        record = CORE.build_record(
            CORE.sample_R(),
            field_state_id="unit-test-phi",
            run_id="unit-test-run",
            ledger_index=0,
        )

        boundary = record["boundary"]
        self.assertEqual(boundary["mode"], "deterministic_audit_only")
        self.assertFalse(boundary["phi_write_back"])
        self.assertFalse(boundary["vortex_control"])
        self.assertFalse(boundary["computes_K_phi"])
        self.assertFalse(boundary["computes_kappa"])
        self.assertFalse(boundary["selects_trajectory"])
        self.assertFalse(boundary["truth_authority"])
        self.assertFalse(boundary["safety_authority"])

        self.assertIn("h_topo", record["observables"])
        self.assertIn("fingerprint", record)
        self.assertIn("sha256", record["fingerprint"])
        self.assertIn("sha3_512", record["fingerprint"])


class TestPhiEkCoreFingerprint(unittest.TestCase):
    """Canonical fingerprint integrity checks."""

    def test_build_record_is_deterministic_for_same_input(self) -> None:
        matrix = CORE.sample_R()

        record_1 = CORE.build_record(
            matrix,
            field_state_id="same",
            run_id="same-run",
            ledger_index=1,
        )
        record_2 = CORE.build_record(
            matrix,
            field_state_id="same",
            run_id="same-run",
            ledger_index=1,
        )

        self.assertEqual(record_1["fingerprint"], record_2["fingerprint"])
        self.assertTrue(CORE.verify_fingerprint(record_1))
        self.assertTrue(CORE.verify_fingerprint(record_2))

    def test_tampering_invalidates_fingerprint(self) -> None:
        record = CORE.build_record(CORE.sample_R(), field_state_id="tamper", run_id="tamper")
        self.assertTrue(CORE.verify_fingerprint(record))

        tampered = copy.deepcopy(record)
        tampered["observables"]["h_topo"] = 0.999

        self.assertFalse(CORE.verify_fingerprint(tampered))

    def test_canonical_serialize_rejects_nan(self) -> None:
        with self.assertRaises(CORE.VectaetosInputError):
            CORE.canonical_serialize({"bad": float("nan")})


class TestPhiEkCoreLedger(unittest.TestCase):
    """Append-only ledger mechanics and Merkle-like root tests."""

    def test_append_read_verify_and_merkle_root(self) -> None:
        record = CORE.build_record(
            CORE.sample_R(),
            field_state_id="ledger-phi",
            run_id="ledger-run",
            ledger_index=0,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "ledger.jsonl"
            CORE.append_ledger(ledger_path, record)

            entries = CORE.read_ledger(ledger_path)
            self.assertEqual(len(entries), 1)
            self.assertTrue(CORE.verify_fingerprint(entries[0]))

            merkle_root = CORE.build_merkle_root([entries[0]["fingerprint"]["sha256"]])
            self.assertEqual(merkle_root, entries[0]["fingerprint"]["sha256"])

    def test_empty_merkle_root_is_deterministic(self) -> None:
        self.assertEqual(
            CORE.build_merkle_root([]),
            "e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855",
        )


class TestPhiEkCoreCli(unittest.TestCase):
    """CLI tests through python -S."""

    def run_core_cli(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["PYTHONNOUSERSITE"] = "1"

        return subprocess.run(
            [sys.executable, "-S", str(CORE_PATH), *args],
            cwd=str(cwd or REPO_ROOT),
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def test_cli_selftest_passes_under_python_dash_S(self) -> None:
        result = self.run_core_cli("selftest")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("SELFTEST PASS", result.stdout)

    def test_cli_sample_audit_verify_ledger_under_python_dash_S(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            sample_path = tmp / "R_sample.json"
            record_path = tmp / "latest_record.json"
            ledger_path = tmp / "ledger.jsonl"
            summary_path = tmp / "ledger_summary.json"

            sample = self.run_core_cli("sample", "--out", str(sample_path), cwd=tmp)
            self.assertEqual(sample.returncode, 0, msg=sample.stderr)
            self.assertTrue(sample_path.exists())

            audit = self.run_core_cli(
                "audit",
                "--input",
                str(sample_path),
                "--out",
                str(record_path),
                "--ledger",
                str(ledger_path),
                "--field-state-id",
                "cli-phi",
                "--run-id",
                "cli-run",
                "--ledger-index",
                "0",
                cwd=tmp,
            )
            self.assertEqual(audit.returncode, 0, msg=audit.stderr)
            self.assertTrue(record_path.exists())
            self.assertTrue(ledger_path.exists())

            verify = self.run_core_cli("verify", "--input", str(record_path), cwd=tmp)
            self.assertEqual(verify.returncode, 0, msg=verify.stderr)
            self.assertIn("VALID", verify.stdout)

            ledger = self.run_core_cli(
                "ledger",
                "--input",
                str(ledger_path),
                "--out",
                str(summary_path),
                cwd=tmp,
            )
            self.assertEqual(ledger.returncode, 0, msg=ledger.stderr)
            self.assertTrue(summary_path.exists())

            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["entries"], 1)
            self.assertEqual(summary["invalid_fingerprint_indices"], [])


if __name__ == "__main__":
    unittest.main()
