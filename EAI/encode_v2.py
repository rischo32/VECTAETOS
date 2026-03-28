import zlib
import math
from collections import Counter


def entropy(s):
    freq = Counter(s)
    L = len(s)
    probs = [c / L for c in freq.values()]
    return -sum(p * math.log(p + 1e-12) for p in probs)


def encode_v2(a: str):

    L = len(a)

    # Hn
    H = entropy(a)
    alphabet = len(set(a))
    Hn = H / (math.log(alphabet + 1e-12) + 1e-12)

    # Cn
    compressed = zlib.compress(a.encode())
    Cn = len(compressed) / (L + 1e-12)

    # Rn
    substrings = [a[i:i+3] for i in range(len(a)-2)]
    unique = len(set(substrings))
    Rn = 1 - (unique / (len(substrings) + 1e-12))

    # Dn
    mid = L // 2
    H1 = entropy(a[:mid]) if mid > 0 else 0
    H2 = entropy(a[mid:]) if mid > 0 else 0
    Dn = abs(H1 - H2)

    return (Hn, Cn, Rn, Dn)
