def encode_v3(a, transforms):

    base = encode_v2(a)
    variants = [encode_v2(t(a)) for t in transforms]

    I = sum(abs(base[i] - variants[0][i]) for i in range(len(base)))

    V = np.var(variants)

    S = V / (len(variants) + 1e-12)

    t1 = transforms[0](transforms[1](a))
    t2 = transforms[1](transforms[0](a))

    T = sum(abs(x-y) for x,y in zip(encode_v2(t1), encode_v2(t2)))

    return (I, S, V, T)
