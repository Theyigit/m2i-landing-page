#!/usr/bin/env python3
"""
Derives the site's raster assets from the two source images in public/images:
favicons and touch icon from the app icon, a lightweight WebP of the app's
home screen for the CTA, and the Open Graph card. Needs Pillow.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "public"
IMG = ROOT / "images"

BRAND = (22, 155, 98)        # Irish flag green, Pantone 347
BRAND_DARK = (12, 92, 58)
ACCENT = (255, 136, 62)      # Irish flag orange, Pantone 151


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def rounded_icon(size: int) -> Image.Image:
    icon = Image.open(IMG / "app-icon.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.22), fill=255)
    icon.putalpha(mask)
    return icon


def favicons() -> None:
    rounded_icon(64).save(ROOT / "favicon.png", optimize=True)
    rounded_icon(180).save(ROOT / "apple-touch-icon.png", optimize=True)


def screenshot() -> None:
    src = Image.open(IMG / "home-screen.png").convert("RGB")
    w = 720
    src = src.resize((w, int(src.height * w / src.width)), Image.LANCZOS)
    src.save(IMG / "home-screen.webp", "WEBP", quality=82, method=6)


def og_card() -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BRAND)
    px = img.load()
    for y in range(H):
        t = y / H
        for x in range(W):
            u = (x / W) * 0.6 + t * 0.4
            px[x, y] = tuple(int(BRAND[i] * (1 - u) + BRAND_DARK[i] * u) for i in range(3))
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 10, W, H), fill=ACCENT)

    icon = rounded_icon(200)
    img.paste(icon, (80, 105), icon)

    d.text((320, 120), "MOVING TO IRELAND", font=font(64), fill="white")
    d.text((320, 205), "Expat guide & relocation checklist", font=font(34, bold=False), fill=(232, 245, 238))

    lines = ["Housing · Paperwork · Healthcare · Schools", "Transport · Utilities · Pets · Before you move"]
    for i, line in enumerate(lines):
        d.text((320, 290 + i * 44), line, font=font(28, bold=False), fill=(220, 238, 228))

    d.rounded_rectangle((320, 430, 700, 500), radius=14, fill=ACCENT)
    d.text((350, 447), "Free on the App Store", font=font(28), fill="white")
    d.text((730, 452), "movingtoireland.co", font=font(26, bold=False), fill=(232, 245, 238))

    img.save(IMG / "og-default.png", optimize=True)


if __name__ == "__main__":
    favicons()
    screenshot()
    og_card()
    print("wrote favicon.png, apple-touch-icon.png, images/home-screen.webp, images/og-default.png")
