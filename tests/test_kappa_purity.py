from EAI.implementation import run_eai

def test_kappa_purity(system, inputs):

    result = run_eai(system, inputs)

    assert "kappa_trace" in result

    kappa = result["kappa_trace"]

    assert isinstance(kappa, list)
    assert not isinstance(kappa, (int, float))

    forbidden = ["score", "threshold", "risk", "classification"]

    for key in result.keys():
        assert key not in forbidden
