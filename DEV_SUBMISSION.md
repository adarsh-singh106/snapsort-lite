# SnapSort Lite: My Screenshots Had Timestamps, Not Names

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

## What I Built

My screenshots folder was becoming a timeline instead of a library. A name like `Screenshot 2026-10-25 184500.png` tells me when I captured something, but not what I wanted to remember.

I built **SnapSort Lite**, a small, local-first Python CLI that uses Tesseract OCR to read visible text from screenshots, suggest readable filenames, and sort **copies** into broad folders: `Code`, `Documents`, `Conversations`, `Web`, and `Other`.

It removes the repetitive first pass of opening images, identifying their contents, and renaming them manually. It deliberately doesn't promise to understand every screenshot: the first version works from recognized text and straightforward keyword rules.

Safety matters as much as convenience. The default is a **dry run**, so I can review the proposed filenames and destinations. Only `--apply` copies files. Originals remain untouched, filename collisions receive suffixes, and a JSON manifest records the operations.

## Demo

<!-- BEFORE PUBLISHING: Replace the line below with the new SnapSort Lite YouTube video ID. Do NOT use the ShadowInputs Week 2 video. -->
<!-- {% youtube ACTUAL_SNAPSORT_VIDEO_ID %} -->

I used three Pillow-generated screenshots with fictional content: a Python snippet, an invoice-like document, and a webpage. The local demonstration produced these mappings:

```text
fictional-invoice.png -> Documents/fictional-data-for-demo.png
fictional-web.png     -> Web/welcome-to-the-fictional-demo-site.png
python-code.png       -> Code/return-f-hello-name.png
```

These are demonstration results, not a measured accuracy benchmark. The code-derived filename also shows why human review is still useful.

![Before and after organization](https://raw.githubusercontent.com/adarsh-singh106/snapsort-lite/main/submission/assets/before-after.png)

To preview and then apply:

```bash
python snapsort.py ./screenshots --output ./organized
python snapsort.py ./screenshots --output ./organized --apply
```

The first command previews the copy plan. The second creates organized copies and a manifest, without deleting the source images. The reproducible [demo walkthrough](https://github.com/adarsh-singh106/snapsort-lite/blob/main/demo/DEMO.md) and [verification notes](https://github.com/adarsh-singh106/snapsort-lite/blob/main/submission/VERIFICATION.md) are in the repository.

## Code

{% github https://github.com/adarsh-singh106/snapsort-lite %}

The [public repository](https://github.com/adarsh-singh106/snapsort-lite) includes the CLI, tests, synthetic demo inputs, documentation, and MIT license.

To get started, clone the repository, install the Python requirements and install Tesseract OCR separately. Then run the commands above against a directory you choose. Nothing is copied until you explicitly pass `--apply`.

## How I Built It

![SnapSort Lite architecture](https://raw.githubusercontent.com/adarsh-singh106/snapsort-lite/main/submission/assets/architecture.png)

The pipeline is deliberately short:

1. Discover supported PNG, JPG, JPEG, and WebP images in a selected directory.
2. Load each image using Pillow and extract visible text through `pytesseract` and the locally installed Tesseract engine.
3. Choose a promising text line and normalize it into a filesystem-safe filename.
4. Apply deterministic keyword rules to choose a category.
5. Prepare a collision-safe copy plan, show it in dry-run mode, and copy with `shutil.copy2` only when asked.
6. Write a JSON manifest, including file hashes, to make the result inspectable.

**What counts as AI here?** Tesseract is the open-source OCR engine doing text recognition locally. It is **not** an LLM or vision-language model, and the category classifier is regular Python logic. The project depends on OCR for its useful naming behavior, but it cannot infer the meaning of text-free diagrams or identify apps from their appearance.

The implementation separates planning from applying, keeps OCR replaceable for testing, rejects source/destination conflicts, and reports a missing Tesseract executable instead of silently inventing OCR results.

The next improvements I'd consider are content-based deduplication, better title selection, and an optional local open-weight vision-language model for screenshots without useful text. None of those are claimed as implemented today.

## Why Does Open Innovation Matter?

Screenshots can contain source code, invoices, conversations, or other private information. With local Tesseract OCR, recognizing text doesn't require sending images to a third-party API or managing an inference API key.

The open-source pipeline is inspectable and adaptable. Someone can improve the naming heuristics, add OCR language packs, replace the classifier, or change how copies are organized without waiting on a closed service. Running locally also makes it easier to reproduce behavior and understand its limitations.

That isn't a blanket security guarantee. Users should still protect their screenshots, review the dry-run plan, and remember that OCR can misread text.

## My Agent Session

I used an AI coding assistant to help implement and document this small proof of concept. The repository retains the code, tests, synthetic demo inputs, and verification notes. I am not claiming a public DevRelay recording or a session link that doesn't exist.

## The Lazy Payoff

The payoff is a first-pass organization proposal without manually opening and renaming each screenshot. In the three-image synthetic demonstration, SnapSort Lite produced categorized copies while leaving originals intact.

I haven't measured time savings on a large personal screenshot library, so I won't invent a percentage. For now, **slow and steady** means giving automation a small, reviewable job before trusting it with more.
