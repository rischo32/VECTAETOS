from EAI.implementation import TRANSFORMS

def test_transform_immutability():

    assert isinstance(TRANSFORMS, tuple), "TRANSFORMS must be tuple"

    original_ids = tuple(id(t) for t in TRANSFORMS)

    try:
        TRANSFORMS += (lambda x: x,)
        mutated = True
    except:
        mutated = False

    assert mutated is False, "TRANSFORMS must be immutable"

    after_ids = tuple(id(t) for t in TRANSFORMS)

    assert original_ids == after_ids, "TRANSFORMS changed"
