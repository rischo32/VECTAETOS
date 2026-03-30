from EAI.implementation import TRANSFORMS


def test_transform_immutability():

    assert isinstance(TRANSFORMS, tuple)

    original_ids = tuple(id(t) for t in TRANSFORMS)

    # pokus o "mutáciu" (vytvorí nový tuple, nesmie ovplyvniť originál)
    new = TRANSFORMS + (lambda x: x,)

    after_ids = tuple(id(t) for t in TRANSFORMS)

    assert original_ids == after_ids
