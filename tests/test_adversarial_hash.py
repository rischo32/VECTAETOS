from ek_core.hash import structural_hash
from ek_core.canonical import canonicalize   # ← PRIDAJ

def test_hash_invariance():
    delta = {(0,1,2): 1.0}

    c = canonicalize(delta)

    h1 = structural_hash(delta)
    h2 = structural_hash(c)

    assert h1 == h2, "Hash not invariant under canonicalization"
