from EAI.implementation import TRANSFORMS

def test_kappa_purity(system, inputs):

    result = run_eai(system, inputs)

    assert "kappa_trace" in result, "kappa_trace missing"

    kappa = result["kappa_trace"]

    assert isinstance(kappa, list), "kappa_trace must be list"

    assert not isinstance(kappa, (int, float)), "κ must not be scalar"

    forbidden_keys = ["score", "threshold", "risk", "classification"]

    for key in result.keys():
        assert key not in forbidden_keys, f"Forbidden key detected: {key}"
