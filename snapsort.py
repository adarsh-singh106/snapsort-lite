"""SnapSort Lite: conservative, local screenshot organization with OCR."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Callable, Iterable

EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
CATEGORIES = ("Code", "Documents", "Conversations", "Web", "Other")


def slug(text: str, max_length: int = 64) -> str:
    """Return a short filesystem-safe slug, with a safe fallback."""
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:max_length].strip("-") or "untitled"


def classify_text(text: str) -> str:
    """Classify OCR text using transparent, intentionally conservative rules."""
    lowered = text.lower()
    rules = {
        "Code": ("traceback", "import ", "def ", "class ", "function ", "const ", "error:"),
        "Documents": ("invoice", "receipt", "statement", "total due", "application"),
        "Conversations": ("reply", "message", "chat", "sent", "conversation"),
        "Web": ("http://", "https://", "search", "sign in", "website", "browser"),
    }
    return next((category for category, terms in rules.items()
                 if any(term in lowered for term in terms)), "Other")


def extract_text(path: Path) -> str:
    """Run local Tesseract OCR and turn dependency/runtime errors into guidance."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: python -m pip install -r requirements.txt") from exc
    try:
        pytesseract.get_tesseract_version()
    except Exception as exc:
        raise RuntimeError(
            "Tesseract OCR is unavailable. Install Tesseract and ensure tesseract.exe is on PATH."
        ) from exc
    try:
        with Image.open(path) as image:
            return pytesseract.image_to_string(image)
    except Exception as exc:
        raise RuntimeError(f"OCR failed for {path.name}: {exc}") from exc


def analyze(path: Path, ocr: Callable[[Path], str] = extract_text) -> tuple[str, str, str]:
    """Return category, safe title, and the raw OCR text used for the decision."""
    text = ocr(path)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    meaningful = [line for line in lines if len(line) >= 3 and re.search(r"[A-Za-z0-9]", line)]
    title = max(meaningful[:8], key=lambda line: len(re.findall(r"[A-Za-z]", line)),
                default="screenshot")
    return classify_text(text), slug(title), text


def _available_target(directory: Path, title: str, suffix: str,
                      reserved: set[Path]) -> Path:
    candidate = directory / f"{title}{suffix.lower()}"
    number = 2
    while candidate.exists() or candidate in reserved:
        candidate = directory / f"{title}-{number}{suffix.lower()}"
        number += 1
    return candidate


def plan(source: Path, destination: Path,
         ocr: Callable[[Path], str] | None = None) -> list[dict[str, str]]:
    """Build a copy plan without creating directories or changing files."""
    ocr = ocr or extract_text
    reserved: set[Path] = set()
    operations: list[dict[str, str]] = []
    for path in sorted(source.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        category, title, text = analyze(path, ocr)
        target = _available_target(destination / category, title, path.suffix, reserved)
        reserved.add(target)
        operations.append({
            "source": str(path),
            "destination": str(target),
            "category": category,
            "filename": target.name,
            "ocr_text": text,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return operations


def write_manifest(path: Path, operations: Iterable[dict[str, str]], applied: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "tool": "SnapSort Lite",
        "applied": applied,
        "operations": list(operations),
    }, indent=2), encoding="utf-8")


def apply_plan(operations: Iterable[dict[str, str]]) -> None:
    for operation in operations:
        target = Path(operation["destination"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(operation["source"], target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview or copy-organize screenshots with local Tesseract OCR.")
    parser.add_argument("source", type=Path, help="directory containing screenshots")
    parser.add_argument("--output", type=Path, default=Path("sorted-screenshots"))
    parser.add_argument("--apply", action="store_true", help="copy files; without this flag, only preview")
    parser.add_argument("--manifest", type=Path, help="write a JSON manifest (also works during dry-run)")
    args = parser.parse_args(argv)
    source, output = args.source.resolve(), args.output.resolve()
    if not source.is_dir():
        parser.error("source must be an existing directory")
    if output == source or output.is_relative_to(source):
        parser.error("output must be outside the source directory")
    try:
        operations = plan(source, output)
    except RuntimeError as exc:
        parser.error(str(exc))
    for operation in operations:
        print(f'{Path(operation["source"]).name} -> '
              f'{Path(operation["destination"]).relative_to(output)}')
    if args.apply:
        apply_plan(operations)
        write_manifest(args.manifest or output / "manifest.json", operations, applied=True)
        print(f"Copied {len(operations)} file(s); originals retained.")
    else:
        if args.manifest:
            write_manifest(args.manifest, operations, applied=False)
        print(f"Dry run only: {len(operations)} file(s) proposed. Add --apply to copy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
