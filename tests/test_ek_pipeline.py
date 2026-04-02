import pytest

from epistemic_cryptography.ek_core.pipeline import ek_step, ek_trajectory


def test_ek_step_structure():
    outputs = ["alpha", "beta", "gamma"]

    result = ek_step(outputs)

    assert "delta" in result
    assert "hash" in result
    assert "kappa_trace" in result


def test_ek_hash_determinism():
    outputs = ["alpha", "beta"]

    a = ek_step(outputs)
    b = ek_step(outputs)

    assert a["hash"] == b["hash"]


def test_kappa_trace_determinism():
    outputs = ["x", "y"]

    a = ek_step(outputs)["kappa_trace"]
    b = ek_step(outputs)["kappa_trace"]

    assert a == b


def test_trajectory_merkle():
    stream = [
        ["a", "b"],
        ["c", "d"],
        ["e", "f"],
    ]

    result = ek_trajectory(stream)

    assert "artifact" in result
    assert "merkle_root" in result["artifact"]
    assert isinstance(result["artifact"]["merkle_root"], str)
