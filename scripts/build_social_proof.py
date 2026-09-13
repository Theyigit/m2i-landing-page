#!/usr/bin/env python3
"""
Composes public/images/app-social-proof.webp — the card in the app CTA block,
in the same layout as the UK driving-test site's: a polaroid collage on the
left, a headline and two App Store reviews on the right, and the app in a phone
frame on the far right.

Inputs:
  scripts/assets/collage.png      the polaroid collage (generated once, committed)
  public/images/home-screen.png   the app's home screen
The two reviews are quoted verbatim from the Irish App Store storefront.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "scripts/assets"
IMG = ROOT / "public/images"

W, H = 1400, 782
BG = (246, 247, 248)
INK = (23, 32, 27)
INK_SOFT = (85, 98, 91)
GREEN = (12, 92, 58)
ORANGE = (255, 136, 62)
WHITE = (255, 255, 255)

REVIEWS = [
    ("So useful when relocating", "I have used this app to manage my todos during moving to Ireland. It is very useful to keep you organised."),
    ("Really informative app", "Really informative app and very easy to use. Would recommend for people moving to Ireland."),
]


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def wrap(draw, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def shadow_card(base, box, radius, blur=18, alpha=40):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 8, x1, y1 + 8), radius=radius, fill=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh)
    ImageDraw.Draw(base).rounded_rectangle(box, radius=radius, fill=WHITE + (255,))


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    draw.polygon(pts, fill=fill)


def stars(draw, x, y, size=24):
    """Arial has no ★ glyph, so the stars are drawn."""
    for i in range(5):
        star(draw, x + size / 2 + i * (size + 4), y + size / 2, size / 2, ORANGE)


def phone(screen_path: Path, width: int) -> Image.Image:
    """The app screen inside a dark bezel with a dynamic island, like the
    App Store screenshot frames."""
    bezel, r = 14, 58
    screen = Image.open(screen_path).convert("RGB")
    sw = width - 2 * bezel
    screen = screen.resize((sw, int(screen.height * sw / screen.width)), Image.LANCZOS)
    ph = Image.new("RGBA", (width, screen.height + 2 * bezel), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, width - 1, ph.height - 1), radius=r + bezel, fill=(24, 24, 26, 255))
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, screen.height - 1), radius=r, fill=255)
    ph.paste(screen, (bezel, bezel), mask)
    iw, ih = int(width * 0.28), int(width * 0.075)
    d.rounded_rectangle(((width - iw) // 2, bezel + 12, (width + iw) // 2, bezel + 12 + ih), radius=ih // 2, fill=(0, 0, 0, 255))
    return ph


def main() -> None:
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)

    # Collage, left half
    collage = Image.open(ASSETS / "collage.png").convert("RGBA")
    ch = H - 40
    collage = collage.resize((int(collage.width * ch / collage.height), ch), Image.LANCZOS)
    img.alpha_composite(collage, (10, 20))

    # Headline
    x = 740
    f_big = font(62)
    d.text((x, 62), "Join expats", font=f_big, fill=INK)
    tw = d.textlength("Join expats ", font=f_big)
    pill = (x + tw, 52, x + tw + 200, 130)
    d.rounded_rectangle(pill, radius=39, fill=GREEN)
    d.text((pill[0] + 22, 62), "4.9", font=f_big, fill=WHITE)
    star(d, pill[0] + 22 + d.textlength("4.9 ", font=f_big) + 22, 92, 24, ORANGE)
    d.text((x, 138), "who settled in Ireland", font=f_big, fill=INK)

    # Review cards
    cw, cx = 380, x
    cy = 250
    f_t, f_b = font(27), font(21, bold=False)
    for title, body in REVIEWS:
        lines = wrap(d, body, f_b, cw - 48)
        chh = 24 + 30 + 12 + 34 + len(lines) * 28 + 24
        shadow_card(img, (cx, cy, cx + cw, cy + chh), 22)
        d = ImageDraw.Draw(img)
        stars(d, cx + 24, cy + 22)
        d.text((cx + 24, cy + 62), title, font=f_t, fill=INK)
        for i, line in enumerate(lines):
            d.text((cx + 24, cy + 104 + i * 28), line, font=f_b, fill=INK_SOFT)
        cy += chh + 22
    d.text((x, cy + 4), "Reviews from the App Store, Ireland", font=font(17, bold=False), fill=INK_SOFT)

    # Phone
    ph = phone(IMG / "home-screen.png", 250)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((1140, 260, 1390, 260 + ph.height), radius=70, fill=(0, 0, 0, 70))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
    img.alpha_composite(ph, (1140, 240))

    out = img.convert("RGB")
    out.save(IMG / "app-social-proof.webp", "WEBP", quality=82, method=6)
    print("wrote images/app-social-proof.webp", out.size)


if __name__ == "__main__":
    main()
