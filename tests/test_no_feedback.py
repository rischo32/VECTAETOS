from EAI.implementation import run_eai

def test_no_feedback(system, inputs):

    history = []

    def wrapped(x):
        history.append(x)
        return system(x)

    run_eai(wrapped, inputs)

    assert history == inputs
