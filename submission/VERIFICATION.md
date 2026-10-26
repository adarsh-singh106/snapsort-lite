# Verification record

Date: 2026-10-26

## Automated tests

Command:

```powershell
python -m pytest -q
```

Result: **12 passed in 0.22s**.

Covered behaviors include filename sanitization, all category rules, empty OCR fallback, duplicate names, dry-run safety, copy-only behavior, manifest generation, and missing Tesseract handling.

## Environment

Executed successfully:

```text
Python 3.14.6
Pillow 12.3.0
pytesseract 0.3.13
tesseract v5.5.3.20260724
```

## Real application run

Generated three synthetic screenshots with `python demo\generate_samples.py`, then ran:

```powershell
python snapsort.py demo\input --output demo\output --manifest demo\preview-manifest.json
python snapsort.py demo\input --output demo\output --apply
```

Observed dry-run output:

```text
fictional-invoice.png -> Documents\fictional-data-for-demo.png
fictional-web.png -> Web\welcome-to-the-fictional-demo-site.png
python-code.png -> Code\return-f-hello-name.png
Dry run only: 3 file(s) proposed. Add --apply to copy.
```

Observed apply output:

```text
Copied 3 file(s); originals retained.
```

The generated manifest contains OCR text for all three files. It classified the invoice as `Documents`, the web sample as `Web`, and the Python sample as `Code`. The source directory remained unchanged and the output contained exactly three categorized copies plus `manifest.json`.

## Media evidence

`submission/assets/cover.png` is 1200x630. `submission/assets/before-after.png` is a local composite based on the actual generated filenames. `submission/assets/architecture.png` is a local diagram of the executed pipeline. These assets have not been uploaded to DEV and therefore have no public URLs.

## Eligibility finding

The official challenge page says the project must be brand-new, use open-source AI at its core, and be written about on DEV. It describes Week 3 as “Slow and Steady” and says the entry period ended October 25, 2026 at 11:59 PM PDT.

This project genuinely uses open-source Tesseract OCR locally. The published page does not explicitly state that a generative or open-weight language model is mandatory, but it does not explicitly confirm that OCR qualifies either. **Eligibility is unverified; do not claim challenge compliance without organizer confirmation.**

## Limitations

There is no public GitHub repository, public demo URL, hosted media, or real screen recording yet. The Week 3 deadline has passed according to the official page. These are publication blockers, not missing test evidence.
