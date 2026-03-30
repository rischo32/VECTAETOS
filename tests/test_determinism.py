from EAI.implementation import run_eai

def test_determinism(system, inputs):

    r1 = run_eai(system, inputs)
    r2 = run_eai(system, inputs)
    r3 = run_eai(system, inputs)

    assert r1 == r2 == r3
