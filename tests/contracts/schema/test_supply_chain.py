"""Fail closed if Stage 01 loses its lock hashes or gains unsafe imports."""

import ast
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_registry_artifacts_are_hash_locked() -> None:
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    assert lock["requires-python"].startswith(">=3.13")
    for package in lock["package"]:
        if package["source"].get("registry"):
            artifacts = [
                *package.get("wheels", []),
                *([package["sdist"]] if "sdist" in package else []),
            ]
            assert artifacts, package["name"]
            assert all(artifact["hash"].startswith("sha256:") for artifact in artifacts)


def test_build_backend_is_locked_and_registry_is_explicit() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    assert project["tool"]["uv"]["index"] == [
        {"name": "pypi", "url": "https://pypi.org/simple", "default": True}
    ]
    assert any(
        requirement.startswith("hatchling") for requirement in project["dependency-groups"]["dev"]
    )
    assert any(
        requirement.startswith("hatchling") for requirement in project["build-system"]["requires"]
    )
    assert "hatchling" in {package["name"] for package in lock["package"]}


def test_domain_and_application_have_no_infrastructure_or_deserialization_imports() -> None:
    forbidden = {
        "fastapi",
        "sqlalchemy",
        "celery",
        "pytesseract",
        "paddleocr",
        "pickle",
        "dill",
        "marshal",
        "joblib",
        "subprocess",
        "socket",
    }
    for part in ("domain", "application"):
        for source in (ROOT / "src" / "text_recognition_core" / part).rglob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module.split(".")[0]]
                else:
                    continue
                assert not forbidden.intersection(names), source
