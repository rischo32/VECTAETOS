from pathlib import Path

from vectaetos_lsp import load_contract, resolve_contract_path


def test_loads_contract_from_explicit_path(tmp_path: Path) -> None:
    contract_path = tmp_path / "vectaetos_code_contract.json"
    contract_path.write_text(
        '{"version":"test","status":"fundamental_repository_perimeter"}',
        encoding="utf-8",
    )

    contract = load_contract(contract_path)

    assert contract["version"] == "test"
    assert contract["status"] == "fundamental_repository_perimeter"


def test_missing_contract_returns_empty_dict(tmp_path: Path) -> None:
    contract = load_contract(tmp_path / "missing.json")

    assert contract == {}


def test_resolve_contract_path_points_to_repo_contract_shape() -> None:
    path = resolve_contract_path()

    assert path.name == "vectaetos_code_contract.json"
    assert "contracts" in path.parts
