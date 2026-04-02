from epistemic_cryptography.ek_core.pipeline import ek_step


def test_no_interpretation_fields():
    result = ek_step(["alpha"])

    forbidden = {
        "score",
        "risk",
        "label",
        "classification",
        "decision",
    }

    for key in result.keys():
        assert key not in forbidden


def test_kappa_is_trace_only():
    result = ek_step(["alpha", "beta"])

    kappa = result["kappa_trace"]

    assert isinstance(kappa, list)
    assert all(isinstance(x, str) for x in kappa)


def test_hash_is_pure_identity():
    result = ek_step(["a", "b"])

    h = result["hash"]

    assert isinstance(h, str)
    assert len(h) > 0


def test_no_hidden_state():
    a = ek_step(["same"])
    b = ek_step(["same"])

    assert a == b
