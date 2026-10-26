*This is a submission for the *[Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

> Publication status: prepared locally on October 26, 2026. The official page lists the Week 3 entry deadline as October 25, 2026 at 11:59 PM PDT. No submission or publication has been made.

### What I Built

SnapSort Lite is a small Windows-friendly Python CLI for the problem that screenshot folders become timelines: names such as `Screenshot 2026-10-25 184500.png` tell me when I captured something, but not what it contains.

The tool scans a user-selected directory for PNG, JPG, JPEG, and WebP files. It reads visible text with the local Tesseract OCR engine, selects a short filesystem-safe filename, and applies transparent keyword rules to place a copy in `Code`, `Documents`, `Conversations`, `Web`, or `Other`. The repetitive work it removes is the first pass of opening screenshots, guessing what they are, and manually creating folders and names.

It is deliberately conservative: dry-run is the default, `--apply` is required to copy, originals are never deleted, existing names receive numeric suffixes, and a JSON manifest records the proposed or applied operations.

### Demo

The demo uses three Pillow-generated screenshots containing clearly fictional Python code, an invoice-like document, and a web page. The real run produced these operations:

```text
fictional-invoice.png -> Documents/fictional-data-for-demo.png
fictional-web.png -> Web/welcome-to-the-fictional-demo-site.png
python-code.png -> Code/return-f-hello-name.png
```

**Media to upload before publishing:** `submission/assets/before-after.png`  
`[DEV IMAGE URL AFTER UPLOAD]`

The terminal run executed both dry-run and `--apply`; the applied output contains the three categorized copies and `manifest.json`. See the reproducible commands and evidence in [`demo/DEMO.md`](demo/DEMO.md) and [`submission/VERIFICATION.md`](submission/VERIFICATION.md).

**Public demo URL:** Not available. The project was not published and no screen recording was created.

### Code

**Public GitHub repository:** Not available yet. No Git remote exists in the inspected workspace.

To create one after review:

```powershell
gh repo create snapsort-lite --public --source . --remote origin
git add .
git commit -m "Build SnapSort Lite MVP"
git push -u origin main
```

### How I Built It

The architecture is a short pipeline: scan supported files, load each image with Pillow, call local Tesseract through pytesseract, select a readable OCR line, slug it with standard-library regular expressions, classify the full OCR text with deterministic keyword rules, and build a collision-safe copy plan. `shutil.copy2` performs the non-destructive copy and `hashlib.sha256` plus JSON provide an audit manifest.

**Architecture media to upload before publishing:** `submission/assets/architecture.png`  
`[DEV IMAGE URL AFTER UPLOAD]`

The open-source AI component is Tesseract OCR, executed locally through its Python wrapper. It is not an LLM, generative model, or advanced visual-semantic system. The classifier is ordinary deterministic Python. Pillow, pytesseract, pytest, pathlib, argparse, shutil, and hashlib are the only project dependencies or required libraries.

The implementation keeps OCR injectable in tests, separates planning from applying, rejects source/destination conflicts, and turns a missing Tesseract executable into an explicit actionable error instead of silently inventing filenames.

### Why Does Open Innovation Matter?

Local open-source technology matters here because screenshots can contain private conversations, invoices, passwords, and tokens. Tesseract lets the OCR step run without uploading images to a hosted API or storing an API key. A local deterministic pipeline is reproducible, inspectable, replaceable, and easy to customize for another language or folder policy.

That privacy claim has a boundary: OCR quality depends on the local installation and image quality, and the tool does not understand visual content that has no readable text. Users should still review proposed operations and avoid running it on files they do not have permission to process.

### My Agent Session

No public DevRelay session link is available. The project was developed and verified locally with an AI coding assistant, with the implementation, tests, and generated demo artifacts retained in the workspace. No session URL is being fabricated.
