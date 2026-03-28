import numpy as np
from encode_v2 import encode_v2


def encode_v3(a, transforms):

    base = encode_v2(a)
    variants = [encode_v2(t(a)) for t in transforms]

    # Identity stability
    I = sum(abs(base[i] - variants[0][i]) for i in range(len(base)))

    # Variability
    V = np.var(variants)

    # Sensitivity
    S = V / (len(variants) + 1e-12)

    # Closure
    t1 = transforms[0](transforms[1](a))
    t2 = transforms[1](transforms[0](a))

    e1 = encode_v2(t1)
    e2 = encode_v2(t2)

    T = sum(abs(x - y) for x, y in zip(e1, e2))

    return (I, S, V, T)
