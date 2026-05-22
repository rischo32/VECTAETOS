"""
Pytest configuration for VECTAETOS tests.

Purpose:
- make the repository root importable during pytest collection,
- preserve shared test fixtures,
- avoid relying on implicit PYTHONPATH behavior.

This file does not define ontology, validation, authority, or execution logic.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def system() -> Callable[[str], str]:
    """
    Simple deterministic fixture used by existing tests.

    Returns a function that reverses a string.
    """
    return lambda x: x[::-1]


@pytest.fixture
def inputs() -> list[str]:
    """
    Shared deterministic input fixture used by existing tests.
    """
    return ["alpha", "beta", "gamma"]
