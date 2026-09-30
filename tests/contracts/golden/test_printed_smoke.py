from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from tools import printed_golden_smoke
from tools.printed_golden_smoke import edit_distance, manifest_samples


def test_golden_manifest_and_images_are_bounded_and_unchanged() -> None:
    samples = manifest_samples()
    assert {sample["language"] for sample in samples} == {"eng", "rus", "ukr"}
    assert {sample["id"] for sample in samples} == {"en-001", "ru-001", "uk-001"}
    assert all(Path(sample["file"]).name == sample["file"] for sample in samples)


def test_edit_distance_counts_unicode_and_word_errors() -> None:
    assert edit_distance(list("КОТ"), list("КИТ")) == 1
    assert edit_distance("one two".split(), "one three".split()) == 1


def test_digest_tamper_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    corpus = tmp_path / "corpus"
    shutil.copytree(printed_golden_smoke.CORPUS, corpus)
    image = corpus / "en.png"
    image.write_bytes(image.read_bytes() + b"changed")
    monkeypatch.setattr(printed_golden_smoke, "CORPUS", corpus)
    with pytest.raises(ValueError, match="digest changed"):
        manifest_samples()


def test_path_escape_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    corpus = tmp_path / "corpus"
    shutil.copytree(printed_golden_smoke.CORPUS, corpus)
    manifest_path = corpus / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["samples"][0]["file"] = "../outside.png"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(printed_golden_smoke, "CORPUS", corpus)
    with pytest.raises(ValueError, match="outside allowlist"):
        manifest_samples()
