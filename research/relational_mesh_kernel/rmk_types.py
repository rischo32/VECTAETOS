from dataclasses import dataclass
from typing import List

@dataclass
class NodeState:
    E: float
    C: float
    T: float
    M: float
    S: float


class RelationalMesh:
    def __init__(self, size: int):
        self.size = size
        self.R = [[0.0 for _ in range(size)] for _ in range(size)]

    def set(self, i: int, j: int, value: float):
        self.R[i][j] = value
        self.R[j][i] = -value  # antisymetria

    def get(self, i: int, j: int) -> float:
        return self.R[i][j]
