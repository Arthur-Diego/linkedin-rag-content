"""Renders the post card PNG (1200x1350) with Pillow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH, HEIGHT = 1200, 1350
MARGIN = 90
BG_TOP, BG_BOTTOM = (11, 18, 32), (16, 27, 51)
OVERLAY_ALPHA = 150  # darkening over AI backgrounds so text stays readable
ACCENT = (56, 189, 248)
TEXT = (237, 242, 247)
MUTED = (172, 184, 204)

_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
]


def _font(bold: bool, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for d in _FONT_DIRS:
        p = Path(d) / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default(size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        cand = f"{line} {word}".strip()
        if draw.textlength(cand, font=font) <= max_width:
            line = cand
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _gradient() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    px = img.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        row = tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM))
        for x in range(WIDTH):
            px[x, y] = row
    return img


def _prepare_background(background: Image.Image | None) -> Image.Image:
    if background is None:
        return _gradient()
    img = ImageOps.fit(background.convert("RGB"), (WIDTH, HEIGHT), Image.LANCZOS)
    overlay = Image.new("RGB", (WIDTH, HEIGHT), BG_TOP)
    mask = Image.new("L", (WIDTH, HEIGHT), OVERLAY_ALPHA)
    img.paste(overlay, (0, 0), mask)
    return img


def render_card(post, out_path: Path, background: Image.Image | None = None) -> Path:
    """Render the card from the frontmatter (image.headline, image.bullets).

    `background` is an optional AI-generated illustration; without it, the
    default gradient is used.
    """
    image_meta = post.meta.get("image") or {}
    headline = image_meta.get("headline") or post.title
    bullets = image_meta.get("bullets") or []
    topic = str(post.meta.get("topic", "RAG")).upper()

    img = _prepare_background(background)
    draw = ImageDraw.Draw(img)
    content_width = WIDTH - 2 * MARGIN

    chip_font = _font(True, 34)
    pad_x, pad_y = 28, 14
    chip_w = draw.textlength(topic, font=chip_font) + 2 * pad_x
    chip_h = 34 + 2 * pad_y
    y = MARGIN
    draw.rounded_rectangle([MARGIN, y, MARGIN + chip_w, y + chip_h], radius=chip_h // 2,
                           outline=ACCENT, width=3)
    draw.text((MARGIN + pad_x, y + pad_y - 2), topic, font=chip_font, fill=ACCENT)
    y += chip_h + 70

    head_font = _font(True, 78)
    for line in _wrap(draw, headline, head_font, content_width):
        draw.text((MARGIN, y), line, font=head_font, fill=TEXT)
        y += 96
    y += 20
    draw.line([MARGIN, y, MARGIN + 140, y], fill=ACCENT, width=8)
    y += 70

    bullet_font = _font(False, 44)
    for bullet in bullets:
        lines = _wrap(draw, str(bullet), bullet_font, content_width - 60)
        draw.ellipse([MARGIN, y + 18, MARGIN + 18, y + 36], fill=ACCENT)
        for i, line in enumerate(lines):
            draw.text((MARGIN + 48, y), line, font=bullet_font, fill=TEXT)
            y += 58
        y += 26

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    return out_path
