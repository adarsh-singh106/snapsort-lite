import json
from pathlib import Path

import pytest

from snapsort import analyze, classify_text, main, plan, slug, write_manifest


def test_filename_sanitization():
    assert slug("Hello, World!") == "hello-world"
    assert slug("!!!") == "untitled"
    assert len(slug("a" * 100)) <= 64


@pytest.mark.parametrize(("text", "category"), [
    ("def hello():\n import os", "Code"),
    ("Invoice 2026\nTotal Due $42", "Documents"),
    ("Chat message: reply", "Conversations"),
    ("Search results https://example.test", "Web"),
    ("pixels only", "Other"),
])
def test_category_selection(text, category):
    assert classify_text(text) == category


def test_empty_ocr_output_uses_safe_fallback(tmp_path: Path):
    category, title, text = analyze(tmp_path / "shot.png", lambda _: "")
    assert (category, title, text) == ("Other", "screenshot", "")


def test_duplicate_filename_handling(tmp_path: Path):
    source, output = tmp_path / "source", tmp_path / "output"
    source.mkdir()
    (source / "one.png").write_bytes(b"one")
    (source / "two.png").write_bytes(b"two")
    operations = plan(source, output, lambda _: "Invoice\nSame title")
    assert [Path(item["destination"]).name for item in operations] == ["same-title.png", "same-title-2.png"]


def test_dry_run_safety(monkeypatch, tmp_path: Path):
    source, output = tmp_path / "source", tmp_path / "output"
    source.mkdir()
    (source / "shot.png").write_bytes(b"data")
    monkeypatch.setattr("snapsort.extract_text", lambda _: "")
    assert main([str(source), "--output", str(output)]) == 0
    assert not output.exists()
    assert (source / "shot.png").exists()


def test_copy_only_behavior_and_manifest(monkeypatch, tmp_path: Path):
    source, output = tmp_path / "source", tmp_path / "output"
    source.mkdir()
    original = source / "shot.png"
    original.write_bytes(b"data")
    monkeypatch.setattr("snapsort.extract_text", lambda _: "")
    assert main([str(source), "--output", str(output), "--apply"]) == 0
    copied = output / "Other" / "screenshot.png"
    assert copied.read_bytes() == b"data"
    assert original.read_bytes() == b"data"
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["applied"] is True
    assert manifest["operations"][0]["category"] == "Other"


def test_manifest_generation(tmp_path: Path):
    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, [{"source": "a", "destination": "b"}], applied=False)
    assert json.loads(manifest.read_text())["operations"][0]["source"] == "a"


def test_missing_tesseract_error(monkeypatch, tmp_path: Path):
    from snapsort import extract_text
    class Missing:
        def get_tesseract_version(self):
            raise RuntimeError("not found")
    monkeypatch.setitem(__import__("sys").modules, "pytesseract", Missing())
    monkeypatch.setitem(__import__("sys").modules, "PIL", __import__("PIL"))
    with pytest.raises(RuntimeError, match="Tesseract OCR is unavailable"):
        extract_text(tmp_path / "shot.png")
