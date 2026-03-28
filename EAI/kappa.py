from encode_v2 import encode_v2


def kappa_signature(a, transforms):

    errors = []

    for t1 in transforms:
        for t2 in transforms:

            x1 = t1(t2(a))
            x2 = t2(t1(a))

            e1 = encode_v2(x1)
            e2 = encode_v2(x2)

            e = sum(abs(i - j) for i, j in zip(e1, e2))

            errors.append(e)

    return sorted(errors)


def kappa_transition(kappa_series):

    import numpy as np

    transitions = []

    for t in range(1, len(kappa_series)):

        prev = np.array(kappa_series[t-1])
        curr = np.array(kappa_series[t])

        var_jump = np.var(curr) - np.var(prev)
        dist_shift = np.mean(np.abs(np.sort(prev) - np.sort(curr)))
        spike = np.max(curr) - np.max(prev)

        transitions.append({
            "t": t,
            "variance_jump": var_jump,
            "distribution_shift": dist_shift,
            "spike": spike
        })

    return transitions
