"""Generate local submission media from the real SnapSort demo outputs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
PROJECT = ROOT.parent


def font(size: int):
    return ImageFont.load_default(size=size)


def cover() -> None:
    image = Image.new("RGB", (1200, 630), "#101827")
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "SnapSort Lite", fill="#f8fafc", font=font(54))
    draw.text((72, 125), "Turn Screenshot Chaos Into Searchable Files", fill="#8bd5ca", font=font(27))
    draw.text((80, 235), "Screenshot 2026-10-25 184500.png", fill="#cbd5e1", font=font(23))
    draw.text((80, 285), "Screenshot 2026-10-25 184612.png", fill="#cbd5e1", font=font(23))
    draw.text((80, 335), "Screenshot 2026-10-25 184901.png", fill="#cbd5e1", font=font(23))
    draw.text((480, 295), "→", fill="#fbbf24", font=font(64))
    draw.rounded_rectangle((625, 205, 1115, 455), radius=18, fill="#1e293b", outline="#8bd5ca", width=3)
    for y, label in [(245, "Code / return-f-hello-name.png"),
                     (310, "Documents / fictional-data-for-demo.png"),
                     (375, "Web / welcome-to-the-fictional-demo-site.png")]:
        draw.text((655, y), label, fill="#f8fafc", font=font(19))
    draw.text((72, 545), "Local OCR • deterministic rules • copies only after approval", fill="#94a3b8", font=font(20))
    image.save(ASSETS / "cover.png")


def architecture() -> None:
    image = Image.new("RGB", (1400, 500), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.text((45, 28), "SnapSort Lite architecture", fill="#0f172a", font=font(34))
    boxes = [
        ("Screenshot\n directory", "#dbeafe"),
        ("Image\n loading", "#dbeafe"),
        ("Local OCR\n(Tesseract)", "#fef3c7"),
        ("Filename\n generation", "#dcfce7"),
        ("Categorization\n(deterministic)", "#dcfce7"),
        ("Safe copy +\nmanifest", "#dcfce7"),
    ]
    x = 35
    for index, (label, color) in enumerate(boxes):
        draw.rounded_rectangle((x, 180, x + 190, 315), radius=12, fill=color, outline="#334155", width=2)
        draw.multiline_text((x + 20, 220), label, fill="#0f172a", font=font(22), spacing=8)
        if index < len(boxes) - 1:
            draw.text((x + 198, 230), "→", fill="#64748b", font=font(30))
        x += 225
    draw.text((260, 390), "OCR reads visible text locally; green steps are transparent Python rules.", fill="#475569", font=font(22))
    image.save(ASSETS / "architecture.png")


def before_after() -> None:
    before = Image.new("RGB", (1200, 500), "#fff7ed")
    draw = ImageDraw.Draw(before)
    draw.text((45, 30), "Before: timestamp-based input files", fill="#9a3412", font=font(32))
    names = ["Screenshot 2026-10-25 184500.png", "Screenshot 2026-10-25 184612.png", "Screenshot 2026-10-25 184901.png"]
    for index, name in enumerate(names):
        draw.text((60, 120 + index * 75), name, fill="#431407", font=font(23))
    after = Image.new("RGB", (1200, 500), "#ecfdf5")
    draw = ImageDraw.Draw(after)
    draw.text((45, 30), "After: actual SnapSort output", fill="#166534", font=font(32))
    names = ["Code/return-f-hello-name.png", "Documents/fictional-data-for-demo.png", "Web/welcome-to-the-fictional-demo-site.png"]
    for index, name in enumerate(names):
        draw.text((60, 120 + index * 75), name, fill="#14532d", font=font(21))
    result = Image.new("RGB", (1200, 1050), "white")
    result.paste(before, (0, 0))
    result.paste(after, (0, 550))
    result.save(ASSETS / "before-after.png")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    cover()
    architecture()
    before_after()
    print(f"Generated assets in {ASSETS}")
