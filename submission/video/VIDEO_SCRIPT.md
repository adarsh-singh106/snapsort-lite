# SnapSort Lite Video Script & Storyboard

**Project:** SnapSort Lite  
**Target:** Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady  
**Format:** 16:9 MP4 (1920×1080) @ 30 FPS, H.264 / AAC  
**Total Target Duration:** 74 Seconds (2,220 frames)  
**Style:** Edited technical walkthrough assembled from genuine application outputs and local execution evidence.

---

## Storyboard & Narration Transcript

### Scene 1: The Problem (00:00 – 00:08 | 8s)
- **Visual:** Windows File Explorer displaying a cluttered screenshot directory full of opaque timestamp filenames (`Screenshot 2026-10-25 184500.png`, `Screenshot 2026-10-25 184612.png`, etc.). Accompanying callout cards outline the core friction points: No content visibility, unsearchable files, sorting fatigue, and cloud privacy risks.
- **Top Badge:** `THE PROBLEM • SCREENSHOT CLUTTER`
- **On-Screen Caption:**  
  > *"Your screenshot folder remembers when. Not what."*
- **Technical Context:** Operating systems save screenshots by capture timestamp rather than content. To find a specific invoice, code snippet, or web bookmark, users must manually open dozens of files.

---

### Scene 2: The Solution (00:08 – 00:16 | 8s)
- **Visual:** Introduction of SnapSort Lite and its three architectural pillars:
  1. **Local OCR:** Tesseract v5.5 engine running 100% on the local CPU. Zero cloud uploads, zero API fees.
  2. **Meaningful Names:** Deterministic extraction of readable text lines into filesystem-safe slugs.
  3. **Organized Folders:** Transparent rule-based classification into `Code`, `Documents`, `Web`, `Conversations`, or `Other`.
  Below, previews of the three reproducible synthetic demo inputs (`fictional-invoice.png`, `fictional-web.png`, `python-code.png`) are shown with their expected category mappings.
- **Top Badge:** `THE SOLUTION • SNAPSORT LITE`
- **On-Screen Caption:**  
  > *"Local OCR. Meaningful names. Organized folders."*

---

### Scene 3: Step 1 — Dry Run Preview (00:16 – 00:30 | 14s)
- **Visual:** Authentic PowerShell terminal window executing the default preview command:
  ```powershell
  PS C:\snapsort-lite> python snapsort.py demo/input --output demo/output
  ```
  Real CLI output displays progressive text analysis and the proposed rename/categorize plan:
  ```text
  fictional-invoice.png -> Documents\fictional-data-for-demo.png
  fictional-web.png     -> Web\welcome-to-the-fictional-demo-site.png
  python-code.png       -> Code\return-f-hello-name.png
  Dry run only: 3 file(s) proposed. Add --apply to copy.
  ```
  Side panel highlights the safety guarantee: Zero disk changes, zero files created, zero files modified.
- **Top Badge:** `STEP 1 • DRY RUN PREVIEW`
- **On-Screen Caption:**  
  > *"Preview first. Nothing changes."*

---

### Scene 4: Step 2 — Apply Operation (00:30 – 00:48 | 18s)
- **Visual:** Terminal executing the explicit copy command with `--apply`:
  ```powershell
  PS C:\snapsort-lite> python snapsort.py demo/input --output demo/output --apply
  ```
  Terminal output verifies execution:
  ```text
  fictional-invoice.png -> Documents\fictional-data-for-demo.png
  fictional-web.png     -> Web\welcome-to-the-fictional-demo-site.png
  python-code.png       -> Code\return-f-hello-name.png
  Copied 3 file(s); originals retained.
  ```
  Directory tree visualizes the created structure (`demo/output/Code`, `Documents`, `Web`, and `manifest.json`). Callout confirms originals in `demo/input/` are 100% retained.
- **Top Badge:** `STEP 2 • APPLY OPERATION`
- **On-Screen Caption:**  
  > *"Copy safely. Keep originals."*

---

### Scene 5: Step 3 — Results & Manifest Audit (00:48 – 01:00 | 12s)
- **Visual:** Side-by-side comparison of input vs output filenames paired with a genuine syntax-highlighted extract of `manifest.json`. Highlights include SHA-256 integrity hashes, transparent OCR extraction text, and source-to-destination mappings.
- **Top Badge:** `STEP 3 • RESULTS & MANIFEST AUDIT`
- **On-Screen Caption:**  
  > *"Three screenshots. Three organized copies."*

---

### Scene 6: Open Source & Architecture (01:00 – 01:08 | 8s)
- **Visual:** Complete 6-stage architecture flow:
  `Input Directory` → `Pillow Image Load` → `Local Tesseract OCR` → `Slug Sanitizer` → `Keyword Classifier` → `Safe Copy + Manifest`
  Tech stack cards highlight Python 3.10+, Tesseract OCR v5.5, Pillow 12.3, 12/12 passing pytest unit tests, and the MIT License.
- **Top Badge:** `OPEN SOURCE & ARCHITECTURE`
- **On-Screen Caption:**  
  > *"Python + Tesseract OCR. Local-first. MIT licensed."*

---

### Scene 7: Final Frame & Call to Action (01:08 – 01:14 | 6s)
- **Visual:** Clean project summary card with official challenge metadata:
  - **Project:** SnapSort Lite
  - **Theme Motto:** "Slow and Steady: Automation You Can Review"
  - **Challenge:** Hacktoberfest Open-Source AI Challenge • Week 3
  - **Repository:** `https://github.com/adarsh-singh106/snapsort-lite`
  - **License:** Open Source (MIT)
- **On-Screen Caption:**  
  > *"SnapSort Lite • https://github.com/adarsh-singh106/snapsort-lite"*
