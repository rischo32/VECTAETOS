def kappa_signature(a, transforms):

    errors = []

    for t1 in transforms:
        for t2 in transforms:

            x1 = t1(t2(a))
            x2 = t2(t1(a))

            e = sum(abs(i-j) for i,j in zip(
                encode_v2(x1),
                encode_v2(x2)
            ))

            errors.append(e)

    return sorted(errors)
