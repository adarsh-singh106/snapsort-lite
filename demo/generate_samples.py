from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
INPUT = ROOT / "input"


def make(name: str, heading: str, lines: list[str]) -> None:
    image = Image.new("RGB", (1100, 650), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1100, 85), fill="#263238")
    draw.text((35, 25), heading, fill="white", font=ImageFont.load_default(size=30))
    for index, line in enumerate(lines):
        draw.text((45, 130 + index * 55), line, fill="#111111", font=ImageFont.load_default(size=25))
    image.save(INPUT / name)


INPUT.mkdir(exist_ok=True)
make("python-code.png", "Python editor", ["def greet(name):", "    return f'Hello, {name}'", "print(greet('Ada'))"])
make("fictional-invoice.png", "Invoice", ["Acme Example Co.", "Invoice 2026-001", "Total Due: $42.00", "Fictional data for demo"])
make("fictional-web.png", "Example Web Page", ["Search results", "https://example.test", "Welcome to the fictional demo site"])
print(f"Created {len(list(INPUT.glob('*.png')))} synthetic screenshots in {INPUT}")
