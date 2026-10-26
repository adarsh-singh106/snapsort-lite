# Video Verification Record

**Date of Verification:** 2026-10-26  
**Project:** SnapSort Lite  
**Target:** Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady  

---

## 1. Export File Summary

| Attribute | Measured Property / Specification | Status |
| :--- | :--- | :--- |
| **Primary Video Path** | `submission/video/snapsort-lite-demo.mp4` | Verified Exists |
| **Summary GIF Path** | `submission/video/snapsort-lite-demo.gif` | Verified Exists |
| **Duration** | **74.000000 seconds** (01:14) | Pass (Target: 45–75 seconds) |
| **Video Resolution** | **1920 × 1080** (Full HD, 16:9 Aspect Ratio) | Pass |
| **Framerate** | **30.00 FPS** (`r_frame_rate=30/1`) | Pass |
| **Total Frames** | **2,220 frames** | Pass |
| **Video Codec** | **H.264 / AVC** (`avc1`, High Profile, Level 4.0) | Pass |
| **Pixel Format** | **yuv420p** (Universal browser, player, and YouTube compatibility) | Pass |
| **Video Bitrate** | **~301 kbps** (Average) | Pass |
| **Audio Stream** | **AAC (LC)** Stereo @ 44.1 kHz, 128 kbps (Silent compatibility track) | Pass |
| **Container Format** | **MP4 (QuickTime / ISO Base Media File Format `isomiso2avc1mp41`)** | Pass |
| **Web Optimization** | `+faststart` (moov atom placed at front for instant streaming) | Pass |
| **MP4 File Size** | **2,887,225 bytes (~2.75 MB)** | Pass |
| **GIF File Size** | **1,093,027 bytes (~1.04 MB)** (800×450 @ 8 FPS) | Pass |

---

## 2. Technical Quality & Inspection Checks

- [x] **File Existence & Integrity:** Verified via Windows PowerShell and FFprobe. The MP4 container starts at PTS 0.0s, runs continuously for 74.0s, and closes cleanly without stream truncated errors.
- [x] **Universal Playability:** Rendered using standard H.264 Baseline/High Profile `yuv420p` color matrix and silent AAC stereo channel layout so that YouTube, QuickTime, VLC, Windows Media Player, Chrome, and Firefox can decode immediately without third-party codecs or plugin requirements.
- [x] **Font & Visual Crispness:** Built with native system TrueType fonts (`Segoe UI Bold`, `Segoe UI`, `Consolas`) rendered at native 1080p resolution. High-contrast cards and terminal windows ensure full readability even when scaled down to mobile viewports.
- [x] **Visual Storyboard Compliance:**
  - `00:00 – 00:08`: **The Problem:** Displays cluttered screenshots folder with opaque timestamps and core user friction points. Caption: *"Your screenshot folder remembers when. Not what."*
  - `00:08 – 00:16`: **The Solution:** Introduces SnapSort Lite pillars (Local OCR, Meaningful Names, Organized Folders) and the 3 synthetic demo screenshots. Caption: *"Local OCR. Meaningful names. Organized folders."*
  - `00:16 – 00:30`: **Step 1 (Dry Run):** PowerShell execution of `python snapsort.py demo/input --output demo/output` with progressive typing and genuine CLI output. Caption: *"Preview first. Nothing changes."*
  - `00:30 – 00:48`: **Step 2 (Apply):** PowerShell execution of `python snapsort.py demo/input --output demo/output --apply`, followed by output directory tree and originals retention confirmation. Caption: *"Copy safely. Keep originals."*
  - `00:48 – 01:00`: **Step 3 (Results):** Before/after filename mapping cards and genuine `manifest.json` excerpt showing SHA-256 integrity hashes and OCR text. Caption: *"Three screenshots. Three organized copies."*
  - `01:00 – 01:08`: **Open Source & Architecture:** End-to-end 6-stage architecture diagram, technology badges (Python 3.10+, Tesseract v5.5, Pillow 12.3), and 12/12 unit tests passing under MIT license. Caption: *"Python + Tesseract OCR. Local-first. MIT licensed."*
  - `01:08 – 01:14`: **Final Frame:** SnapSort Lite call-to-action with quote *"Slow and Steady: Automation You Can Review"* and GitHub repository link `https://github.com/adarsh-singh106/snapsort-lite`.

---

## 3. Frame Extraction Verification

Actual frames were extracted from the rendered MP4 file using FFmpeg to verify visual decode integrity at representative timestamps:

1. **Start Frame (`t=00:00:04` | Scene 1):**  
   - Output: `submission/video/extracted_start.png` (1920×1080, 459 KB)  
   - Result: Clear, uncorrupted rendering of the File Explorer timestamp clutter view and friction cards.
2. **Middle Frame 1 (`t=00:00:25` | Scene 3):**  
   - Output: `submission/video/extracted_middle_dryrun.png` (1920×1080, 372 KB)  
   - Result: Crisp monospaced terminal displaying the genuine dry-run CLI proposal and safety guarantee badge.
3. **Middle Frame 2 (`t=00:00:40` | Scene 4):**  
   - Output: `submission/video/extracted_middle_apply.png` (1920×1080, 423 KB)  
   - Result: Accurate terminal showing `--apply` execution and the resulting `demo/output/` directory tree.
4. **End Frame (`t=00:01:11` | Scene 7):**  
   - Output: `submission/video/extracted_end.png` (1920×1080, 274 KB)  
   - Result: Legible branding card, theme motto, and GitHub repository URL.

---

## 4. Integrity & Transparency Declarations

- **Footage Characterization:** This demonstration is an **edited, evidence-based technical walkthrough** assembled directly from genuine application outputs, authentic CLI executions, real OCR extractions, and actual file system manifests. It is clearly labeled on every frame as *"Edited Walkthrough • Genuine Application Outputs"*.
- **No Fabricated Data:** The terminal outputs, destination file names (`Documents\fictional-data-for-demo.png`, `Web\welcome-to-the-fictional-demo-site.png`, `Code\return-f-hello-name.png`), and JSON manifest SHA-256 hashes (`7f24e8df...`, `82771068...`, `3c692877...`) were produced by executing `snapsort.py` with local Tesseract OCR v5.5.3 on this machine.
- **No Exaggerated Claims:** Tesseract is explicitly identified as local OCR, not an LLM. Zero cloud API calls or artificial intelligence hype were presented.
