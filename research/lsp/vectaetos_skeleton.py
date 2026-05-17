# vectaetos_skeleton.py
# Python 3.11+
# v.0.1
from __future__ import annotations
import dataclasses
import json
import hashlib
from pathlib import Path
from typing import Mapping, Sequence, Iterable, Tuple, Any
import collections

# ---------- Základné typy a invarianty ----------

@dataclasses.dataclass(frozen=True)
class Phi:
    """Nemenná reprezentácia epistemického poľa Φ = (Σ, R)."""
    Sigma: Tuple[str, ...]  # immutable symbol set
    R: Tuple[Tuple[float, ...], ...]  # antisymmetric matrix stored immutably

    def __post_init__(self):
        # overenie antisymetrie a nulových diagonál
        n = len(self.R)
        if any(len(row) != n for row in self.R):
            raise ValueError("R must be square")
        for i in range(n):
            if abs(self.R[i][i]) > 1e-12:
                raise ValueError("R diagonal must be zero")
            for j in range(n):
                if abs(self.R[i][j] + self.R[j][i]) > 1e-9:
                    raise ValueError("R must be antisymmetric")

# ---------- RMK: len vystavuje, nemodifikuje ----------

class RMK:
    """Relational Mesh Kernel: číta a vystavuje štruktúru, nezasahuje do Φ."""
    def __init__(self, phi: Phi):
        self._phi = phi

    @property
    def Sigma(self) -> Tuple[str, ...]:
        return self._phi.Sigma

    @property
    def R(self) -> Tuple[Tuple[float, ...], ...]:
        return self._phi.R

    def compute_delta(self, i: int, j: int, k: int) -> float:
        """Δ(i,j,k) = R(i,j) + R(j,k) + R(k,i). Len pozorovateľ, nie skóre."""
        R = self._phi.R
        return R[i][j] + R[j][k] + R[k][i]

    def iter_triples(self) -> Iterable[Tuple[int,int,int]]:
        n = len(self._phi.R)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    yield (i,j,k)

# ---------- Vortex: len projekcie, žiadna mutácia ----------

class Vortex:
    """Vortex generuje projekcie / trajektórne možnosti bez výberu alebo mutácie."""
    def __init__(self, rmk: RMK):
        self._rmk = rmk

    def generate_candidate_projection(self, seed_marker: int) -> Mapping[str, Any]:
        """Vytvorí popis možnej projekcie; NIKDY nemení Φ ani R."""
        # deterministické, bez optimalizácie
        deltas = []
        for (i,j,k) in self._rmk.iter_triples():
            d = self._rmk.compute_delta(i,j,k)
            if abs(d) > 1e-12:
                deltas.append(((i,j,k), float(d)))
        # zjednodušená projekcia: len popis možných markerov
        projection = {
            "seed": int(seed_marker),
            "delta_count": len(deltas),
            "delta_sample": deltas[:10],
        }
        return projection

# ---------- Serializácia a deterministické hashovanie ----------

def deterministic_serialize(obj: Any) -> bytes:
    """Deterministická serializácia JSON (kľúče zoradené, bez plávajúcich nepresností)."""
    def _clean(o):
        if isinstance(o, dict):
            return {k: _clean(o[k]) for k in sorted(o)}
        if isinstance(o, (list, tuple)):
            return [_clean(x) for x in o]
        if isinstance(o, float):
            # normalizovať float na string s pevnou presnosťou pre deterministickosť
            return format(o, ".12g")
        return o
    cleaned = _clean(obj)
    text = json.dumps(cleaned, separators=(",", ":"), ensure_ascii=False)
    return text.encode("utf-8")

def dual_hash(data: bytes) -> Tuple[str,str]:
    """SHA-256 potom SHA3-512; vráti hex digesty."""
    h1 = hashlib.sha256(data).hexdigest()
    h2 = hashlib.sha3_512(data).hexdigest()
    return h1, h2

# ---------- Merkle leaf / root (jednoduchá implementácia) ----------

def merkle_root(leaves: Sequence[bytes]) -> str:
    """Jednoduchý deterministický Merkle root (pairwise concat + sha256)."""
    if not leaves:
        return hashlib.sha256(b"").hexdigest()
    nodes = [hashlib.sha256(l).digest() for l in leaves]
    while len(nodes) > 1:
        next_nodes = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else nodes[i]
            next_nodes.append(hashlib.sha256(left + right).digest())
        nodes = next_nodes
    return nodes[0].hex()

# ---------- Ledger commit (append-only) ----------

class Ledger:
    """Append-only ledger: zapisuje len fingerprinty a metadáta; neudáva autoritu."""
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # neotvárame súbor na zápis pri init; zápis explicitný cez commit()

    def commit(self, entry: Mapping[str, Any]) -> None:
        """Deterministicky serializovať a pridať záznam; žiadna interpretácia."""
        data = deterministic_serialize(entry)
        h1, h2 = dual_hash(data)
        record = {
            "entry": entry,
            "sha256": h1,
            "sha3_512": h2,
        }
        line = json.dumps(record, separators=(",", ":"), ensure_ascii=False)
        # append-only write
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

# ---------- Observables / audit-only funkcie ----------

def compute_topology_hash(R: Tuple[Tuple[float,...], ...]) -> str:
    """Deterministický fingerprint topológie (len audit marker)."""
    data = deterministic_serialize({"R": R})
    return hashlib.sha256(data).hexdigest()

# ---------- Príklad použitia (bez mutácií) ----------

def example_run(out_ledger: Path) -> None:
    # definícia Σ a R (nemenné)
    Sigma = ("INT","LEX","VER","LIB","UNI","REL","WIS","CRE")
    # príklad antisymetrickej matice 8x8 (len demo)
    R = tuple(tuple(0.0 if i==j else (0.1*(i-j)) for j in range(8)) for i in range(8))
    phi = Phi(Sigma=Sigma, R=R)
    rmk = RMK(phi)
    vortex = Vortex(rmk)

    projection = vortex.generate_candidate_projection(seed_marker=0)
    topo_hash = compute_topology_hash(phi.R)

    ledger = Ledger(out_ledger)
    # commit len popisnej stopy; nikdy neoznačujeme za "pravdu" alebo "kappa"
    ledger.commit({
        "type": "trajectory_trace",
        "projection": projection,
        "topology_hash": topo_hash,
        "note": "descriptive trace only; not a decision or truth claim"
    })

# ---------- Koniec skeletonu ----------
