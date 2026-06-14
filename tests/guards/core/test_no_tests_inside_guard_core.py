from __future__ import annotations

from pathlib import Path


def test_no_pytest_files_inside_guard_core_package() -> None:
    guard_core = Path("guards/core")
    forbidden = sorted(guard_core.glob("test_*.py"))

    assert forbidden == [], (
        "Pytest files must live under tests/guards/core/, "
        "not inside guards/core/ implementation package."
    )
