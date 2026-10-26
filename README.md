# SnapSort Lite

SnapSort Lite is a privacy-first Python CLI for making small, safe improvements to a screenshot collection. It reads visible text with the local Tesseract OCR engine, proposes a short filename, and copies each image into a transparent category.

## Problem

Windows screenshots often accumulate under timestamp-based names. SnapSort Lite turns that timeline into a reviewable first pass without deleting or uploading originals.

## Features

- PNG, JPG, JPEG, and WebP support
- Local OCR with Pillow and pytesseract
- Deterministic, filesystem-safe filenames
- Rule-based `Code`, `Documents`, `Conversations`, `Web`, and `Other` categories
- Dry-run preview by default; `--apply` is required to copy
- Never overwrites an existing destination; uses `-2`, `-3`, etc.
- SHA-256 and OCR details in a JSON manifest
- Originals are always retained

## Installation on Windows

Install Python 3.10 or newer, then from this folder:

```powershell
python -m pip install -r requirements.txt
```

Install Tesseract OCR separately, for example from the [UB Mannheim Windows builds](https://github.com/UB-Mannheim/tesseract/wiki), and make sure `tesseract.exe` is on PATH. Confirm with `tesseract --version`. SnapSort reports a clear error if the executable is missing.

## Usage

Preview first:

```powershell
python snapsort.py "C:\Pictures\Screenshots" --output "C:\Pictures\Sorted"
```

Apply the reviewed plan:

```powershell
python snapsort.py "C:\Pictures\Screenshots" --output "C:\Pictures\Sorted" --apply
```

The apply command writes `manifest.json` in the output directory. A dry-run manifest can be requested explicitly with `--manifest preview.json`. The source and destination must be different, and the destination cannot be inside the source.

## Safety and privacy

Images stay on the local machine. There are no cloud uploads, paid APIs, API keys, watchers, background processes, or automatic startup. The tool copies rather than moves and never overwrites existing files. Review the dry-run output and manifest before applying; screenshots can contain passwords, tokens, invoices, or private conversations.

## Architecture

`main()` validates CLI paths, `plan()` scans supported files and builds pure operation records, `extract_text()` calls local Tesseract, `classify_text()` applies visible keyword rules, and `apply_plan()` performs only the explicitly requested copies. `write_manifest()` records the plan and SHA-256 hashes.

## Limitations

This is OCR, not an LLM or advanced visual-semantic model. It cannot infer meaning from diagrams or images without readable text, and classification is intentionally heuristic. It scans only the top level of the source directory, supports one OCR language, and quality depends on image resolution and Tesseract installation. It is not a substitute for checking sensitive screenshots.

## Testing

```powershell
python -m pytest -q
```

The test suite mocks OCR for deterministic unit tests and covers sanitization, category rules, empty OCR, collisions, dry-run safety, copy-only behavior, manifests, and missing Tesseract handling. A real OCR smoke test can be run manually when `tesseract --version` succeeds.

## Demo

The reproducible fictional samples and walkthrough are in [`demo/`](demo/). Generate them with `python demo/generate_samples.py`, then follow [`demo/DEMO.md`](demo/DEMO.md). Synthetic screenshots are not real user data.

## Future roadmap

- Optional recursive scanning with explicit opt-in
- Better user-configurable keyword rules and OCR languages
- A review UI that exposes every proposed operation
- Optional local open-weight vision models, clearly separated from this OCR-only MVP
