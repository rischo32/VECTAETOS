from EAI.implementation import TRANSFORMS

def test_no_adaptivity(system, inputs):

    calls = []

    def wrapped(x):
        calls.append(x)
        return system(x)

    run_eai(wrapped, inputs)

    assert calls == inputs, "Inputs were modified or reordered"
