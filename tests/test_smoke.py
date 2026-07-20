from pathlib import Path


def test_project_root_contains_pyproject() -> None:
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / "pyproject.toml").is_file()
