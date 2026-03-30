from EAI.implementation import TRANSFORMS

def test_transform_immutability():

    assert isinstance(TRANSFORMS, tuple)

    original_ids = tuple(id(t) for t in TRANSFORMS)

    # pokus o mutáciu
    try:
        TRANSFORMS += (lambda x: x,)
        mutated = True
    except:
        mutated = False

    assert mutated is False

    after_ids = tuple(id(t) for t in TRANSFORMS)

    assert original_ids == after_ids
