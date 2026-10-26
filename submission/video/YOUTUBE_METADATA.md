# YouTube Publishing Metadata & DEV Embed Guide

**Project:** SnapSort Lite  
**Challenge:** Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady  
**Date:** 2026-10-26  

---

## YouTube Video Metadata

### Title
```text
SnapSort Lite | Local AI Screenshot Organizer | Hacktoberfest 2026
```

### Category
Science & Technology / Howto & Style

### Description
```text
SnapSort Lite is a privacy-first, local Python CLI tool that transforms cluttered screenshot directories into organized, searchable folders using open-source Tesseract OCR.

Submission for the Hacktoberfest Open-Source AI Challenge Week 3: "Slow and Steady" (Automation You Can Review).

GitHub Repository:
https://github.com/adarsh-singh106/snapsort-lite

Key Highlights:
• 100% Local-First: Powered by local Tesseract OCR v5.5; zero cloud uploads, zero API fees, zero telemetry.
• Preview by Default: Conservative dry-run workflow shows you proposed filenames and target categories before touching disk.
• Non-Destructive: Originals are always preserved; files are safely copied only when --apply is explicitly passed.
• Collision Safety: Automatic numerical deduplication (-2, -3) prevents overwriting existing files.
• Auditable Manifest: Generates a JSON manifest containing exact extracted OCR text and SHA-256 integrity hashes.
• Open Source: Fully testable Python 3.10+ codebase covered by 12 automated unit tests under the MIT license.

Video Timeline:
0:00 - The Problem: Opaque timestamp-named screenshots
0:08 - The Solution: SnapSort Lite architecture
0:16 - Step 1: Dry run preview (zero risk)
0:30 - Step 2: Apply operation (safe copy)
0:48 - Step 3: Verified results and JSON manifest audit
1:00 - Open source technology stack and tests
1:08 - Project links & Hacktoberfest Week 3 theme

#Hacktoberfest #OpenSource #Python #TesseractOCR #ScreenshotOrganizer #DevTools #LocalAI
```

### Tags
```text
Hacktoberfest, OpenSource, Python, TesseractOCR, ScreenshotOrganizer, DevTools, LocalAI, ComputerVision, Automation, PrivacyFirst, ImageProcessing, DeveloperTools
```

### Video File Details
- **File Name:** `snapsort-lite-demo.mp4`
- **Resolution:** 1920 × 1080 (1080p Full HD, 16:9 widescreen)
- **Framerate:** 30 FPS
- **Video Codec:** H.264 (AVC) High Profile, yuv420p
- **Audio Track:** Silent Stereo AAC (128 kbps, 44.1 kHz) for universal YouTube compatibility
- **Duration:** 74 seconds (01:14)

---

## DEV Community Embed Snippet

Once uploaded to YouTube, copy the unique 11-character YouTube video ID (e.g., `dQw4w9WgXcQ` from `https://www.youtube.com/watch?v=dQw4w9WgXcQ`) and insert it into `DEV_SUBMISSION.md` replacing the placeholder:

```liquid
{% youtube YOUR_ACTUAL_SNAPSORT_YOUTUBE_VIDEO_ID %}
```

> [!WARNING]
> Do NOT reuse the Week 2 ShadowInputs video embed (`_xY1zABC123`). This video is a dedicated, newly produced technical demonstration specifically for SnapSort Lite and Hacktoberfest Week 3.

### GitHub README Embed Snippet

To embed the demonstration in `README.md`, you can use either the direct YouTube link or the optimized summary GIF:

```markdown
### Demo Walkthrough

[![SnapSort Lite Demo Video](https://img.youtube.com/vi/YOUR_ACTUAL_SNAPSORT_YOUTUBE_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_ACTUAL_SNAPSORT_YOUTUBE_VIDEO_ID)

*Or view the lightweight animated preview:*

![SnapSort Lite Demo GIF](submission/video/snapsort-lite-demo.gif)
```
