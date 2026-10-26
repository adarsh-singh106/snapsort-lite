"""Full video and GIF generator for SnapSort Lite demonstration.
Outputs:
  - submission/video/snapsort-lite-demo.mp4 (1920x1080 @ 30fps H.264, 74.0s)
  - submission/video/snapsort-lite-demo.gif (800x450 optimized GIF)
"""
from __future__ import annotations

import os
import sys
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import numpy as np

# Ensure Tesseract directory is on PATH
os.environ["PATH"] = r"C:\Program Files\Tesseract-OCR;" + os.environ.get("PATH", "")

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo"
DEMO_INPUT = DEMO / "input"
DEMO_OUTPUT = DEMO / "output"
VIDEO_DIR = ROOT / "submission" / "video"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEMI = r"C:\Windows\Fonts\segoeuisl.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONOB = r"C:\Windows\Fonts\consolab.ttf"

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

TITLE_FONT = get_font(FONT_BOLD, 44)
SUBTITLE_FONT = get_font(FONT_REG, 26)
CAPTION_FONT = get_font(FONT_BOLD, 30)
SECTION_FONT = get_font(FONT_BOLD, 22)
HEADER_FONT = get_font(FONT_BOLD, 32)
CARD_TITLE_FONT = get_font(FONT_BOLD, 24)
CARD_TEXT_FONT = get_font(FONT_REG, 20)
CARD_TEXT_BOLD = get_font(FONT_BOLD, 20)
MONO_LG = get_font(FONT_MONO, 24)
MONO_MD = get_font(FONT_MONO, 20)
MONO_SM = get_font(FONT_MONO, 17)
MONO_XS = get_font(FONT_MONO, 15)
BADGE_FONT = get_font(FONT_BOLD, 18)

# Color Palette
BG_COLOR = (15, 23, 42)          # slate-900
HEADER_BG = (10, 16, 30)        # slate-950
CARD_BG = (30, 41, 59)          # slate-800
CARD_BORDER = (51, 65, 85)      # slate-700
TERMINAL_BG = (13, 17, 23)      # dark terminal
TERMINAL_BAR = (22, 27, 34)
TEXT_WHITE = (248, 250, 252)    # slate-50
TEXT_MUTED = (148, 163, 184)    # slate-400
TEXT_DIM = (100, 116, 139)      # slate-500
ACCENT_BLUE = (56, 189, 248)    # sky-400
ACCENT_GREEN = (52, 211, 153)   # emerald-400
ACCENT_YELLOW = (251, 191, 36)  # amber-400
ACCENT_ORANGE = (251, 146, 60)  # orange-400
ACCENT_RED = (248, 113, 113)    # red-400
ACCENT_PURPLE = (192, 132, 252) # purple-400

def draw_header(draw: ImageDraw.ImageDraw, section_badge: str):
    draw.rectangle((0, 0, 1920, 60), fill=HEADER_BG)
    draw.line((0, 60, 1920, 60), fill=(30, 41, 59), width=2)
    
    draw.text((40, 14), "SnapSort Lite", fill=TEXT_WHITE, font=get_font(FONT_BOLD, 24))
    draw.text((210, 17), "v0.1.0 • Local-First OCR", fill=ACCENT_BLUE, font=get_font(FONT_REG, 18))
    
    badge_w = 340
    badge_x = (1920 - badge_w) // 2
    draw.rounded_rectangle((badge_x, 12, badge_x + badge_w, 48), radius=8, fill=(30, 41, 59), outline=ACCENT_BLUE, width=1)
    draw.text((badge_x + 20, 18), section_badge.upper(), fill=ACCENT_BLUE, font=BADGE_FONT)
    
    draw.text((1420, 18), "Edited Walkthrough • Genuine Application Outputs", fill=TEXT_MUTED, font=get_font(FONT_REG, 17))

def draw_caption(draw: ImageDraw.ImageDraw, text: str, progress: float):
    caption_h = 70
    caption_y = 960
    
    bbox = draw.textbbox((0, 0), text, font=CAPTION_FONT)
    tw = bbox[2] - bbox[0]
    box_w = max(tw + 80, 500)
    box_x = (1920 - box_w) // 2
    
    draw.rounded_rectangle((box_x, caption_y, box_x + box_w, caption_y + caption_h), radius=16, fill=(15, 23, 42), outline=ACCENT_BLUE, width=2)
    
    tx = box_x + (box_w - tw) // 2
    draw.text((tx, caption_y + 16), text, fill=TEXT_WHITE, font=CAPTION_FONT)
    
    pw = int(1920 * progress)
    draw.line((0, 1076, 1920, 1076), fill=(30, 41, 59), width=4)
    if pw > 0:
        draw.line((0, 1076, pw, 1076), fill=ACCENT_BLUE, width=4)

def draw_window_frame(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str, bg=TERMINAL_BG):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=bg, outline=CARD_BORDER, width=2)
    draw.rectangle((x, y, x + w, y + 42), fill=TERMINAL_BAR)
    draw.line((x, y + 42, x + w, y + 42), fill=CARD_BORDER, width=1)
    
    draw.ellipse((x + 16, y + 14, x + 28, y + 26), fill=ACCENT_RED)
    draw.ellipse((x + 36, y + 14, x + 48, y + 26), fill=ACCENT_YELLOW)
    draw.ellipse((x + 56, y + 14, x + 68, y + 26), fill=ACCENT_GREEN)
    
    draw.text((x + 85, y + 10), title, fill=TEXT_MUTED, font=get_font(FONT_BOLD, 17))

# ----------------- SCENE RENDERERS -----------------

def render_scene1(t: float) -> Image.Image:
    """Scene 1: The Problem (0-8s).
    Cluttered folder of timestamp-named screenshots.
    Caption: 'Your screenshot folder remembers when. Not what.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "The Problem • Screenshot Clutter")
    
    draw.text((100, 95), "Why Screenshot Management Breaks Down", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 142), "Default operating system tools dump every capture into a single flat directory with meaningless timestamp titles.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    fx, fy, fw, fh = 100, 195, 880, 720
    draw_window_frame(draw, fx, fy, fw, fh, "File Explorer — C:\\Users\\User\\Pictures\\Screenshots")
    
    files = [
        ("Screenshot 2026-10-25 184500.png", "248 KB", "10/25/2026 6:45 PM"),
        ("Screenshot 2026-10-25 184612.png", "312 KB", "10/25/2026 6:46 PM"),
        ("Screenshot 2026-10-25 184901.png", "295 KB", "10/25/2026 6:49 PM"),
        ("Screenshot 2026-10-25 185122.png", "180 KB", "10/25/2026 6:51 PM"),
        ("Screenshot 2026-10-25 185408.png", "420 KB", "10/25/2026 6:54 PM"),
        ("Screenshot 2026-10-25 185834.png", "210 KB", "10/25/2026 6:58 PM"),
        ("Screenshot 2026-10-25 190215.png", "340 KB", "10/25/2026 7:02 PM"),
        ("Screenshot 2026-10-25 191140.png", "265 KB", "10/25/2026 7:11 PM"),
        ("Screenshot 2026-10-25 191502.png", "195 KB", "10/25/2026 7:15 PM"),
    ]
    
    draw.text((fx + 30, fy + 55), "Name", fill=TEXT_MUTED, font=CARD_TEXT_BOLD)
    draw.text((fx + 460, fy + 55), "Date Modified", fill=TEXT_MUTED, font=CARD_TEXT_BOLD)
    draw.text((fx + 720, fy + 55), "Size", fill=TEXT_MUTED, font=CARD_TEXT_BOLD)
    draw.line((fx + 20, fy + 85, fx + fw - 20, fy + 85), fill=CARD_BORDER, width=1)
    
    for idx, (fname, fsize, fdate) in enumerate(files):
        row_y = fy + 98 + idx * 62
        if idx < 3:
            draw.rounded_rectangle((fx + 15, row_y - 6, fx + fw - 15, row_y + 46), radius=6, fill=(30, 41, 59), outline=ACCENT_ORANGE if idx==0 else CARD_BORDER, width=1)
            draw.ellipse((fx + 28, row_y + 12, fx + 42, row_y + 26), fill=ACCENT_ORANGE if idx==0 else ACCENT_YELLOW)
        else:
            draw.ellipse((fx + 28, row_y + 12, fx + 42, row_y + 26), fill=TEXT_DIM)
            
        draw.text((fx + 55, row_y + 8), fname, fill=TEXT_WHITE if idx < 3 else TEXT_MUTED, font=MONO_MD)
        draw.text((fx + 460, row_y + 8), fdate, fill=TEXT_MUTED, font=CARD_TEXT_FONT)
        draw.text((fx + 720, row_y + 8), fsize, fill=TEXT_MUTED, font=CARD_TEXT_FONT)

    rx, ry, rw, rh = 1020, 195, 800, 720
    draw.rounded_rectangle((rx, ry, rx + rw, ry + rh), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((rx + 40, ry + 40), "THE PAIN POINT", fill=ACCENT_RED, font=BADGE_FONT)
    draw.text((rx + 40, ry + 75), "Opaque Timestamp Filenames", fill=TEXT_WHITE, font=HEADER_FONT)
    
    pain_points = [
        ("No Content Visibility", "You cannot tell what an image contains without opening every single file one by one.", ACCENT_RED),
        ("Unsearchable Library", "Searching for 'invoice', 'python', or 'order' returns 0 results because names are just dates.", ACCENT_ORANGE),
        ("Manual Sorting Fatigue", "Manually opening, reading, renaming, and filing dozens of screenshots is tedious and slow.", ACCENT_YELLOW),
        ("Cloud Privacy Risks", "Uploading screenshots with private invoices or code to online LLM APIs risks sensitive data leaks.", ACCENT_PURPLE),
    ]
    
    for idx, (title, desc, color) in enumerate(pain_points):
        cy = ry + 160 + idx * 125
        draw.rounded_rectangle((rx + 40, cy, rx + rw - 40, cy + 105), radius=10, fill=(20, 27, 45), outline=color, width=1)
        draw.rectangle((rx + 40, cy, rx + 48, cy + 105), fill=color)
        draw.text((rx + 65, cy + 16), title, fill=TEXT_WHITE, font=CARD_TITLE_FONT)
        draw.multiline_text((rx + 65, cy + 50), desc, fill=TEXT_MUTED, font=CARD_TEXT_FONT, spacing=4)
        
    draw_caption(draw, "Your screenshot folder remembers when. Not what.", t / 74.0)
    return im

def render_scene2(t: float) -> Image.Image:
    """Scene 2: The Solution (8-16s).
    Introduce SnapSort Lite.
    Caption: 'Local OCR. Meaningful names. Organized folders.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "The Solution • SnapSort Lite")
    
    draw.text((100, 90), "Meet SnapSort Lite: Privacy-First Screenshot Organization", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 138), "A transparent, local-first Python CLI using Tesseract OCR to turn chaos into a reviewable structure.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    pillars = [
        ("1. Local OCR", "Tesseract v5.5 engine runs 100% on your machine. Zero cloud uploads, zero API fees, zero telemetry.", ACCENT_BLUE, "OCR ENGINE"),
        ("2. Meaningful Names", "Extracts readable text lines and generates clean, filesystem-safe slugs (e.g. return-f-hello-name.png).", ACCENT_GREEN, "DETERMINISTIC"),
        ("3. Organized Folders", "Sorts safely into Code, Documents, Web, Conversations, or Other without deleting originals.", ACCENT_YELLOW, "COPY-SAFE"),
    ]
    
    pw = 550
    for idx, (p_title, p_desc, p_color, p_badge) in enumerate(pillars):
        px = 100 + idx * 585
        py = 200
        draw.rounded_rectangle((px, py, px + pw, py + 230), radius=12, fill=CARD_BG, outline=p_color, width=2)
        draw.rounded_rectangle((px + 30, py + 25, px + 30 + 150, py + 55), radius=6, fill=(20, 27, 45), outline=p_color, width=1)
        draw.text((px + 45, py + 30), p_badge, fill=p_color, font=BADGE_FONT)
        draw.text((px + 30, py + 75), p_title, fill=TEXT_WHITE, font=CARD_TITLE_FONT)
        draw.multiline_text((px + 30, py + 120), p_desc, fill=TEXT_MUTED, font=CARD_TEXT_FONT, spacing=6)
        
    draw.text((100, 470), "Three Synthetic Demo Inputs (Reproducible & Fictional)", fill=TEXT_WHITE, font=HEADER_FONT)
    
    samples = [
        ("fictional-invoice.png", "Invoice Document", "demo/input/fictional-invoice.png", "Total Due: $42.00", "Category: Documents", ACCENT_YELLOW),
        ("fictional-web.png", "Web Browser Page", "demo/input/fictional-web.png", "https://example.test", "Category: Web", ACCENT_BLUE),
        ("python-code.png", "Python Editor Snippet", "demo/input/python-code.png", "def greet(name)...", "Category: Code", ACCENT_GREEN),
    ]
    
    for idx, (fname, ftitle, fpath, fcontent, fcat, col) in enumerate(samples):
        sx = 100 + idx * 585
        sy = 530
        sw = 550
        sh = 390
        draw.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
        
        p = ROOT / fpath
        if p.exists():
            thumb = Image.open(p).convert("RGB")
            thumb = thumb.resize((510, 240), Image.Resampling.LANCZOS)
            im.paste(thumb, (sx + 20, sy + 20))
            draw.rectangle((sx + 20, sy + 20, sx + 530, sy + 260), outline=CARD_BORDER, width=1)
            
        draw.text((sx + 25, sy + 280), fname, fill=TEXT_WHITE, font=MONO_MD)
        draw.text((sx + 25, sy + 315), f"{ftitle} • {fcontent}", fill=TEXT_MUTED, font=CARD_TEXT_FONT)
        
        draw.rounded_rectangle((sx + 25, sy + 345, sx + 220, sy + 375), radius=6, fill=(20, 27, 45), outline=col, width=1)
        draw.text((sx + 35, sy + 350), fcat, fill=col, font=BADGE_FONT)
        
    draw_caption(draw, "Local OCR. Meaningful names. Organized folders.", t / 74.0)
    return im

def render_scene3(t: float) -> Image.Image:
    """Scene 3: Dry Run (16-30s).
    Show the real command and output.
    Caption: 'Preview first. Nothing changes.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "Step 1 • Dry Run Preview")
    
    draw.text((100, 90), "Preview Before You Apply: Zero Risk Verification", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 138), "SnapSort Lite enforces dry-run by default. It parses images, runs OCR, and shows you exactly what it will do.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    tx, ty, tw, th = 100, 195, 1100, 720
    draw_window_frame(draw, tx, ty, tw, th, "PowerShell — snapsort-lite (Dry Run)")
    
    prompt = "PS C:\\snapsort-lite> "
    cmd = "python snapsort.py demo/input --output demo/output"
    
    st = t - 16.0
    char_count = int(min(len(cmd), max(0, st * 25)))
    typed_cmd = cmd[:char_count]
    cursor = "_" if (int(t * 4) % 2 == 0) else " "
    
    draw.text((tx + 30, ty + 65), prompt, fill=ACCENT_BLUE, font=MONO_LG)
    draw.text((tx + 30 + 260, ty + 65), typed_cmd + (cursor if char_count < len(cmd) else ""), fill=TEXT_WHITE, font=MONO_LG)
    
    if st > 1.8:
        outputs = [
            ("", None),
            ("[OCR Engine Initialized: Tesseract v5.5.3 local engine]", TEXT_DIM),
            ("Analyzing 3 image(s) in demo/input ...", TEXT_MUTED),
            ("", None),
            ("fictional-invoice.png -> Documents\\fictional-data-for-demo.png", ACCENT_YELLOW),
            ("fictional-web.png     -> Web\\welcome-to-the-fictional-demo-site.png", ACCENT_BLUE),
            ("python-code.png       -> Code\\return-f-hello-name.png", ACCENT_GREEN),
            ("", None),
            ("Dry run only: 3 file(s) proposed. Add --apply to copy.", TEXT_WHITE),
        ]
        
        reveal_count = int(min(len(outputs), max(0, (st - 1.8) * 3)))
        for idx in range(reveal_count):
            line, color = outputs[idx]
            if line:
                ly = ty + 120 + idx * 38
                draw.text((tx + 30, ly), line, fill=color or TEXT_WHITE, font=MONO_MD)
                
        if reveal_count >= len(outputs):
            ly = ty + 120 + len(outputs) * 38 + 20
            draw.text((tx + 30, ly), prompt + cursor, fill=ACCENT_BLUE, font=MONO_LG)

    rx, ry, rw = 1240, 195, 580
    draw.rounded_rectangle((rx, ry, rx + rw, ry + 220), radius=12, fill=CARD_BG, outline=ACCENT_GREEN, width=2)
    draw.rounded_rectangle((rx + 30, ry + 25, rx + 180, py := ry + 55), radius=6, fill=(20, 27, 45), outline=ACCENT_GREEN, width=1)
    draw.text((rx + 45, ry + 30), "SAFETY GUARANTEE", fill=ACCENT_GREEN, font=BADGE_FONT)
    draw.text((rx + 30, ry + 75), "Zero Disk Changes", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    draw.multiline_text((rx + 30, ry + 115),
        "• Source directory untouched: 3 files unchanged\n"
        "• Destination directory: Not created yet\n"
        "• Zero files written, zero files deleted\n"
        "• Safe review before any modification",
        fill=TEXT_MUTED, font=CARD_TEXT_FONT, spacing=6)

    ry2 = ry + 250
    draw.rounded_rectangle((rx, ry2, rx + rw, ry2 + 470), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((rx + 30, ry2 + 30), "How Decisions Were Made", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    details = [
        ("fictional-invoice.png", "Keywords: 'invoice', 'total due'", "Rule matched: Documents", ACCENT_YELLOW),
        ("fictional-web.png", "Keywords: 'https://', 'search'", "Rule matched: Web", ACCENT_BLUE),
        ("python-code.png", "Keywords: 'def ', 'return '", "Rule matched: Code", ACCENT_GREEN),
    ]
    
    for idx, (fn, kw, res, col) in enumerate(details):
        cy = ry2 + 85 + idx * 120
        draw.rounded_rectangle((rx + 30, cy, rx + rw - 30, cy + 100), radius=8, fill=(20, 27, 45), outline=col, width=1)
        draw.text((rx + 45, cy + 14), fn, fill=TEXT_WHITE, font=MONO_SM)
        draw.text((rx + 45, cy + 42), kw, fill=TEXT_MUTED, font=CARD_TEXT_FONT)
        draw.text((rx + 45, cy + 68), res, fill=col, font=CARD_TEXT_BOLD)

    draw_caption(draw, "Preview first. Nothing changes.", t / 74.0)
    return im

def render_scene4(t: float) -> Image.Image:
    """Scene 4: Apply (30-48s).
    Show the actual apply command and resulting folders.
    Caption: 'Copy safely. Keep originals.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "Step 2 • Apply Operation")
    
    draw.text((100, 90), "Execute the Copy Plan: Safe Copies, Retained Originals", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 138), "With --apply, SnapSort Lite performs collision-safe copies into category subfolders and records a full manifest.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    tx, ty, tw, th = 100, 195, 1050, 720
    draw_window_frame(draw, tx, ty, tw, th, "PowerShell — snapsort-lite (--apply)")
    
    prompt = "PS C:\\snapsort-lite> "
    cmd = "python snapsort.py demo/input --output demo/output --apply"
    
    st = t - 30.0
    char_count = int(min(len(cmd), max(0, st * 28)))
    typed_cmd = cmd[:char_count]
    cursor = "_" if (int(t * 4) % 2 == 0) else " "
    
    draw.text((tx + 30, ty + 65), prompt, fill=ACCENT_BLUE, font=MONO_LG)
    draw.text((tx + 30 + 260, ty + 65), typed_cmd + (cursor if char_count < len(cmd) else ""), fill=TEXT_WHITE, font=MONO_LG)
    
    if st > 1.8:
        outputs = [
            ("fictional-invoice.png -> Documents\\fictional-data-for-demo.png", ACCENT_YELLOW),
            ("fictional-web.png     -> Web\\welcome-to-the-fictional-demo-site.png", ACCENT_BLUE),
            ("python-code.png       -> Code\\return-f-hello-name.png", ACCENT_GREEN),
            ("", None),
            ("Copied 3 file(s); originals retained.", ACCENT_GREEN),
            ("", None),
            ("PS C:\\snapsort-lite> Get-ChildItem demo/output -Recurse", TEXT_MUTED),
            ("", None),
            ("demo/output/Code/return-f-hello-name.png", TEXT_WHITE),
            ("demo/output/Documents/fictional-data-for-demo.png", TEXT_WHITE),
            ("demo/output/Web/welcome-to-the-fictional-demo-site.png", TEXT_WHITE),
            ("demo/output/manifest.json", ACCENT_PURPLE),
        ]
        
        reveal_count = int(min(len(outputs), max(0, (st - 1.8) * 3)))
        for idx in range(reveal_count):
            line, color = outputs[idx]
            if line:
                ly = ty + 120 + idx * 36
                draw.text((tx + 30, ly), line, fill=color or TEXT_WHITE, font=MONO_MD)
                
        if reveal_count >= len(outputs):
            ly = ty + 120 + len(outputs) * 36 + 15
            draw.text((tx + 30, ly), prompt + cursor, fill=ACCENT_BLUE, font=MONO_LG)

    rx, ry, rw, rh = 1190, 195, 630, 720
    draw.rounded_rectangle((rx, ry, rx + rw, ry + rh), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    
    draw.text((rx + 35, ry + 35), "ORGANIZED FILE SYSTEM", fill=ACCENT_GREEN, font=BADGE_FONT)
    draw.text((rx + 35, ry + 70), "Resulting Folder Hierarchy", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    tree_y = ry + 125
    draw.rounded_rectangle((rx + 35, tree_y, rx + rw - 35, tree_y + 360), radius=10, fill=(15, 23, 42), outline=CARD_BORDER, width=1)
    
    tree_lines = [
        ("📁 demo/output/", TEXT_WHITE, True),
        ("   ├── 📁 Code/", ACCENT_GREEN, True),
        ("   │   └── 📄 return-f-hello-name.png", TEXT_WHITE, False),
        ("   ├── 📁 Documents/", ACCENT_YELLOW, True),
        ("   │   └── 📄 fictional-data-for-demo.png", TEXT_WHITE, False),
        ("   ├── 📁 Web/", ACCENT_BLUE, True),
        ("   │   └── 📄 welcome-to-the-fictional-demo-site.png", TEXT_WHITE, False),
        ("   └── 📋 manifest.json  (Audit trail & SHA-256)", ACCENT_PURPLE, False),
    ]
    
    for idx, (tline, tcolor, is_b) in enumerate(tree_lines):
        draw.text((rx + 55, tree_y + 20 + idx * 40), tline, fill=tcolor, font=MONO_MD)

    card_y = tree_y + 390
    draw.rounded_rectangle((rx + 35, card_y, rx + rw - 35, card_y + 150), radius=10, fill=(20, 27, 45), outline=ACCENT_GREEN, width=1)
    draw.text((rx + 55, card_y + 20), "Originals 100% Intact", fill=ACCENT_GREEN, font=CARD_TITLE_FONT)
    draw.multiline_text((rx + 55, card_y + 55),
        "Source folder demo/input still contains all 3 original files.\n"
        "SnapSort copies images rather than moving or deleting,\n"
        "ensuring your data is never lost or corrupted.",
        fill=TEXT_MUTED, font=CARD_TEXT_FONT, spacing=4)

    draw_caption(draw, "Copy safely. Keep originals.", t / 74.0)
    return im

def render_scene5(t: float) -> Image.Image:
    """Scene 5: Results (48-60s).
    Show the before/after comparison and manifest.
    Caption: 'Three screenshots. Three organized copies.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "Step 3 • Results & Manifest Audit")
    
    draw.text((100, 90), "Inspection & Verification: Transparent Audit Trail", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 138), "Every operation is documented in manifest.json with SHA-256 hashes, exact OCR text, and destination paths.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    lx, ly, lw, lh = 100, 195, 820, 720
    draw.rounded_rectangle((lx, ly, lx + lw, ly + lh), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((lx + 35, ly + 35), "BEFORE VS AFTER COMPARISON", fill=ACCENT_BLUE, font=BADGE_FONT)
    draw.text((lx + 35, ly + 70), "From Opaque Names to Clean Categories", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    comparisons = [
        ("fictional-invoice.png", "Documents / fictional-data-for-demo.png", "Documents", ACCENT_YELLOW),
        ("fictional-web.png", "Web / welcome-to-the-fictional-demo-site.png", "Web", ACCENT_BLUE),
        ("python-code.png", "Code / return-f-hello-name.png", "Code", ACCENT_GREEN),
    ]
    
    for idx, (b_name, a_name, cat, col) in enumerate(comparisons):
        cy = ly + 125 + idx * 180
        draw.rounded_rectangle((lx + 30, cy, lx + lw - 30, cy + 155), radius=10, fill=(20, 27, 45), outline=col, width=1)
        
        draw.text((lx + 50, cy + 18), "BEFORE:", fill=TEXT_DIM, font=BADGE_FONT)
        draw.text((lx + 150, cy + 16), b_name, fill=TEXT_MUTED, font=MONO_MD)
        
        draw.text((lx + 50, cy + 62), "↓", fill=col, font=get_font(FONT_BOLD, 28))
        draw.text((lx + 90, cy + 66), f"Classified as '{cat}' via OCR keyword matching", fill=TEXT_DIM, font=CARD_TEXT_FONT)
        
        draw.text((lx + 50, cy + 112), "AFTER:", fill=col, font=BADGE_FONT)
        draw.text((lx + 150, cy + 110), a_name, fill=TEXT_WHITE, font=MONO_MD)

    rx, ry, rw, rh = 960, 195, 860, 720
    draw_window_frame(draw, rx, ry, rw, rh, "Audit Manifest — demo/output/manifest.json")
    
    manifest_snippet = [
        ('{\n  "tool": "SnapSort Lite",\n  "applied": true,\n  "operations": [', TEXT_MUTED),
        ('    {', TEXT_MUTED),
        ('      "source": ".../demo/input/fictional-invoice.png",', TEXT_WHITE),
        ('      "destination": ".../demo/output/Documents/fictional-data-for-demo.png",', ACCENT_YELLOW),
        ('      "category": "Documents",', ACCENT_YELLOW),
        ('      "filename": "fictional-data-for-demo.png",', ACCENT_YELLOW),
        ('      "ocr_text": "Invoice\\n\\nAcme Example Co.\\nInvoice 2026-001\\nTotal Due: $42.00...",', TEXT_DIM),
        ('      "sha256": "7f24e8df26336c8264e7a343bb8093affad6a46e9b01d82327905b9f60af4598"', ACCENT_PURPLE),
        ('    },', TEXT_MUTED),
        ('    {', TEXT_MUTED),
        ('      "source": ".../demo/input/python-code.png",', TEXT_WHITE),
        ('      "destination": ".../demo/output/Code/return-f-hello-name.png",', ACCENT_GREEN),
        ('      "category": "Code",', ACCENT_GREEN),
        ('      "sha256": "3c692877262416c42c8e2a79aae615d79f63e515ad56c263fed90bd169991e85"', ACCENT_PURPLE),
        ('    }', TEXT_MUTED),
        ('  ]\n}', TEXT_MUTED),
    ]
    
    for idx, (mline, mcol) in enumerate(manifest_snippet):
        my = ry + 60 + idx * 36
        draw.text((rx + 30, my), mline, fill=mcol, font=MONO_SM)
        
    draw_caption(draw, "Three screenshots. Three organized copies.", t / 74.0)
    return im

def render_scene6(t: float) -> Image.Image:
    """Scene 6: Open Source & Architecture (60-68s).
    Show the project repository and technology.
    Caption: 'Python + Tesseract OCR. Local-first. MIT licensed.'
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, "Open Source & Architecture")
    
    draw.text((100, 90), "Local-First Architecture & Technology Stack", fill=TEXT_WHITE, font=HEADER_FONT)
    draw.text((100, 138), "100% open-source, fully testable, and completely self-contained. No external cloud calls.", fill=TEXT_MUTED, font=SUBTITLE_FONT)
    
    pipe_y = 200
    draw.rounded_rectangle((100, pipe_y, 1820, pipe_y + 240), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((135, pipe_y + 30), "EXECUTION PIPELINE", fill=ACCENT_BLUE, font=BADGE_FONT)
    draw.text((135, pipe_y + 65), "End-to-End Processing Flow", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    stages = [
        ("1. Input Scan", "Find PNG, JPG, WebP in directory", ACCENT_BLUE),
        ("2. Pillow Load", "Open image locally into memory", ACCENT_BLUE),
        ("3. Tesseract OCR", "Extract visible text via pytesseract", ACCENT_YELLOW),
        ("4. Slug Generator", "Safe filesystem filename title", ACCENT_GREEN),
        ("5. Rule Classifier", "Categorize Code / Doc / Web", ACCENT_GREEN),
        ("6. Copy + Manifest", "Safe copy & SHA-256 audit record", ACCENT_PURPLE),
    ]
    
    bw = 250
    for idx, (stitle, sdesc, scol) in enumerate(stages):
        bx = 135 + idx * 280
        by = pipe_y + 110
        draw.rounded_rectangle((bx, by, bx + bw, by + 100), radius=8, fill=(20, 27, 45), outline=scol, width=2)
        draw.text((bx + 15, by + 15), stitle, fill=TEXT_WHITE, font=CARD_TEXT_BOLD)
        draw.multiline_text((bx + 15, by + 45), sdesc, fill=TEXT_MUTED, font=get_font(FONT_REG, 17), spacing=2)
        if idx < len(stages) - 1:
            draw.text((bx + bw + 8, by + 35), "→", fill=TEXT_DIM, font=get_font(FONT_BOLD, 26))

    gy = 475
    draw.rounded_rectangle((100, gy, 940, gy + 440), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((135, gy + 35), "CORE TECHNOLOGY", fill=ACCENT_GREEN, font=BADGE_FONT)
    draw.text((135, gy + 70), "Open-Source Foundation", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    stack = [
        ("Python 3.10+", "Modern, type-annotated CLI with zero heavy frameworks", ACCENT_GREEN),
        ("Tesseract OCR v5.5", "Local Google-developed OCR engine via pytesseract wrapper", ACCENT_YELLOW),
        ("Pillow (PIL)", "Reliable cross-platform image loading and dimension handling", ACCENT_BLUE),
        ("MIT License", "Completely open source for personal or commercial workflows", ACCENT_PURPLE),
    ]
    for idx, (item, desc, col) in enumerate(stack):
        iy = gy + 120 + idx * 75
        draw.ellipse((140, iy + 10, 154, iy + 24), fill=col)
        draw.text((170, iy + 5), item, fill=TEXT_WHITE, font=CARD_TEXT_BOLD)
        draw.text((170, iy + 35), desc, fill=TEXT_MUTED, font=CARD_TEXT_FONT)

    draw.rounded_rectangle((980, gy, 1820, gy + 440), radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((1015, gy + 35), "QUALITY ASSURANCE", fill=ACCENT_BLUE, font=BADGE_FONT)
    draw.text((1015, gy + 70), "Automated Testing & Coverage", fill=TEXT_WHITE, font=CARD_TITLE_FONT)
    
    qa_points = [
        ("12 / 12 Pytest Tests Passing", "Complete test coverage for sanitization, categorization, collision safety, and dry-run guarantees.", ACCENT_GREEN),
        ("Deterministic Fallbacks", "Handles missing Tesseract with clear error messages rather than invented results.", ACCENT_YELLOW),
        ("Collision Prevention", "Appends numerical suffixes (-2, -3) rather than overwriting existing destination files.", ACCENT_BLUE),
        ("Privacy By Design", "Zero network sockets opened, zero external dependencies required for execution.", ACCENT_PURPLE),
    ]
    for idx, (title, desc, col) in enumerate(qa_points):
        iy = gy + 120 + idx * 75
        draw.ellipse((1020, iy + 10, 1034, iy + 24), fill=col)
        draw.text((1050, iy + 5), title, fill=TEXT_WHITE, font=CARD_TEXT_BOLD)
        draw.text((1050, iy + 35), desc, fill=TEXT_MUTED, font=CARD_TEXT_FONT)

    draw_caption(draw, "Python + Tesseract OCR. Local-first. MIT licensed.", t / 74.0)
    return im

def render_scene7(t: float) -> Image.Image:
    """Scene 7: Final Frame (68-74s).
    SnapSort Lite
    'Slow and Steady: Automation You Can Review'
    https://github.com/adarsh-singh106/snapsort-lite
    """
    im = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im)
    
    cx, cy, cw, ch = 310, 160, 1300, 760
    draw.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=20, fill=CARD_BG, outline=ACCENT_BLUE, width=3)
    
    draw.rounded_rectangle((cx, cy, cx + cw, cy + 90), radius=20, fill=(20, 27, 45))
    draw.rectangle((cx, cy + 45, cx + cw, cy + 90), fill=(20, 27, 45))
    draw.line((cx, cy + 90, cx + cw, cy + 90), fill=CARD_BORDER, width=2)
    
    draw.text((cx + 50, cy + 30), "HACKTOBERFEST OPEN-SOURCE AI CHALLENGE • WEEK 3", fill=ACCENT_BLUE, font=BADGE_FONT)
    draw.text((cx + cw - 280, cy + 30), "THEME: SLOW AND STEADY", fill=ACCENT_YELLOW, font=BADGE_FONT)
    
    draw.text((cx + 100, cy + 150), "SnapSort Lite", fill=TEXT_WHITE, font=get_font(FONT_BOLD, 64))
    draw.text((cx + 100, cy + 240), '"Slow and Steady: Automation You Can Review"', fill=ACCENT_GREEN, font=get_font(FONT_BOLD, 36))
    
    draw.text((cx + 100, cy + 320),
        "A conservative, privacy-first screenshot organizer built with Python and local Tesseract OCR.\n"
        "Preview every change with dry-run mode before copying a single file.",
        fill=TEXT_MUTED, font=get_font(FONT_REG, 24), spacing=8)
        
    badges = ["100% Local OCR", "Dry-Run Safety", "Retains Originals", "Audit Manifest", "MIT Licensed"]
    for idx, b in enumerate(badges):
        bx = cx + 100 + idx * 225
        by = cy + 420
        draw.rounded_rectangle((bx, by, bx + 205, by + 48), radius=8, fill=(20, 27, 45), outline=ACCENT_BLUE, width=1)
        draw.text((bx + 20, by + 12), b, fill=TEXT_WHITE, font=BADGE_FONT)
        
    ry = cy + 520
    draw.rounded_rectangle((cx + 100, ry, cx + cw - 100, ry + 120), radius=12, fill=(15, 23, 42), outline=ACCENT_GREEN, width=2)
    draw.text((cx + 130, ry + 25), "PROJECT REPOSITORY & CODEBASE:", fill=ACCENT_GREEN, font=BADGE_FONT)
    draw.text((cx + 130, ry + 60), "https://github.com/adarsh-singh106/snapsort-lite", fill=TEXT_WHITE, font=get_font(FONT_BOLD, 32))
    
    draw.text((cx + 100, cy + 680), "Open Innovation • Local AI • Inspectable Architecture • Reproducible Walkthrough", fill=TEXT_DIM, font=CARD_TEXT_FONT)
    
    draw_caption(draw, "SnapSort Lite • https://github.com/adarsh-singh106/snapsort-lite", t / 74.0)
    return im

def get_frame(frame_num: int, total_frames: int, fps: int = 30) -> Image.Image:
    t = frame_num / fps
    fade_len = 8
    
    def scene_at(time_s: float):
        if time_s < 8.0:
            return 1, time_s
        elif time_s < 16.0:
            return 2, time_s
        elif time_s < 30.0:
            return 3, time_s
        elif time_s < 48.0:
            return 4, time_s
        elif time_s < 60.0:
            return 5, time_s
        elif time_s < 68.0:
            return 6, time_s
        else:
            return 7, time_s
            
    scene_renderers = {
        1: render_scene1,
        2: render_scene2,
        3: render_scene3,
        4: render_scene4,
        5: render_scene5,
        6: render_scene6,
        7: render_scene7,
    }
    
    cur_scene, _ = scene_at(t)
    
    boundaries = [8.0, 16.0, 30.0, 48.0, 60.0, 68.0]
    for b in boundaries:
        b_frame = int(b * fps)
        if 0 <= frame_num - b_frame < fade_len:
            alpha = (frame_num - b_frame) / fade_len
            prev_im = scene_renderers[cur_scene - 1](b - 0.05)
            next_im = scene_renderers[cur_scene](t)
            return Image.blend(prev_im, next_im, alpha)
            
    return scene_renderers[cur_scene](t)

def generate_video():
    total_seconds = 74.0
    fps = 30
    total_frames = int(total_seconds * fps) # 2220 frames
    
    output_mp4 = VIDEO_DIR / "snapsort-lite-demo.mp4"
    temp_mp4 = VIDEO_DIR / "temp_video.mp4"
    
    print(f"Rendering {total_frames} frames ({total_seconds}s @ {fps}fps) to {temp_mp4}...")
    start_time = time.time()
    
    writer = imageio_ffmpeg.write_frames(
        str(temp_mp4),
        (1920, 1080),
        fps=fps,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
        macro_block_size=1,
        output_params=["-preset", "fast", "-crf", "18"]
    )
    writer.send(None)
    
    for f in range(total_frames):
        frame_img = get_frame(f, total_frames, fps)
        arr = np.asarray(frame_img)
        writer.send(arr)
        
        if f % 200 == 0 or f == total_frames - 1:
            elapsed = time.time() - start_time
            percent = (f + 1) / total_frames * 100
            print(f"  Frame {f + 1}/{total_frames} ({percent:.1f}%) - elapsed: {elapsed:.1f}s")
            
    writer.close()
    render_time = time.time() - start_time
    print(f"Video track rendered in {render_time:.1f}s.")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Muxing final video with silent AAC audio and faststart flags...")
    mux_cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(temp_mp4),
        "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", str(total_seconds),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    res = subprocess.run(mux_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print("Warning: muxing note, moving temp_mp4 to final:", res.stderr.decode("utf-8", errors="ignore"))
        temp_mp4.replace(output_mp4)
    else:
        temp_mp4.unlink(missing_ok=True)
        print(f"Successfully produced: {output_mp4}")

def generate_gif():
    """Produce an optimized 800x450 GIF for GitHub README and DEV previews."""
    input_mp4 = VIDEO_DIR / "snapsort-lite-demo.mp4"
    output_gif = VIDEO_DIR / "snapsort-lite-demo.gif"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    print(f"Generating optimized demo GIF from {input_mp4} to {output_gif}...")
    gif_filter = "fps=8,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer"
    cmd = [
        ffmpeg_exe,
        "-y",
        "-ss", "14.0",
        "-t", "36.0",
        "-i", str(input_mp4),
        "-vf", gif_filter,
        str(output_gif)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        size_mb = output_gif.stat().st_size / (1024 * 1024)
        print(f"Successfully generated GIF: {output_gif} ({size_mb:.2f} MB)")
    else:
        print("GIF generation note:", res.stderr.decode("utf-8", errors="ignore"))

if __name__ == "__main__":
    generate_video()
    generate_gif()
