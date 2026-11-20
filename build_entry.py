#!/usr/bin/env python3
"""Draw the front page for "The Brexit Reset".

Reads the Brussels hero photograph from assets/, lays out a broadsheet
front page for Friday 20 November 2026 on a 1024x1024 canvas, and writes
entry.png next to this script.

The build is fully deterministic: no randomness, no network, no clock and
no timestamps anywhere in the image, so two runs produce identical bytes.
Only Pillow is needed; fonts come from the system Liberation family.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
HERO_PATH = HERE / "assets" / (
    "media-generation-brussels-eu-quarter-dusk-0-a7c1f0f3-d0bf-4297-ab9c-"
    "4ca258caa997.webp"
)
OUTPUT_PATH = HERE / "entry.png"

CANVAS_W = 1024
CANVAS_H = 1024
MAX_BYTES = 1_048_576  # competition limit: the image must fit in 1 MiB

PAPER = (251, 250, 246)
INK = (20, 20, 20)
MUTED = (92, 88, 82)
MASTHEAD_BG = (16, 19, 24)
GOLD = (232, 164, 32)
RULE = (196, 190, 178)
WHITE = (255, 255, 255)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF_BOLD = FONT_DIR / "LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR / "LiberationSerif-Italic.ttf"
SANS = FONT_DIR / "LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR / "LiberationSans-Bold.ttf"

MARGIN = 48
CONTENT_W = CANVAS_W - 2 * MARGIN


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType font, falling back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Greedy word wrap: pack as many words per line as fit in max_width."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cover_crop(photo: Image.Image, width: int, height: int, y_bias: float) -> Image.Image:
    """Scale the photo to cover width x height, then crop with a vertical bias.

    y_bias 0 keeps the top of the photo, 1 keeps the bottom; 0.35 keeps the
    Berlaymont facade and the flag row in frame.
    """
    scale = max(width / photo.width, height / photo.height)
    grown = photo.resize(
        (round(photo.width * scale), round(photo.height * scale)), Image.LANCZOS
    )
    left = (grown.width - width) // 2
    top = int((grown.height - height) * y_bias)
    top = max(0, min(top, grown.height - height))
    return grown.crop((left, top, left + width, top + height))


def shade_bottom(canvas: Image.Image, top: int, bottom: int, peak_alpha: int) -> None:
    """Paint a black gradient over rows top..bottom so white type stays legible."""
    veil = Image.new("RGBA", (canvas.width, bottom - top), (0, 0, 0, 0))
    painter = ImageDraw.Draw(veil)
    span = max(1, bottom - top)
    for row in range(bottom - top):
        strength = int(peak_alpha * (row / span) ** 1.6)
        painter.line([(0, row), (canvas.width, row)], fill=(0, 0, 0, strength))
    canvas.alpha_composite(veil, (0, top))


# The six stories under the lead, in reading order: left column first.
STORIES = [
    {
        "tag": "UKRAINE",
        "colour": (178, 38, 30),
        "headline": "Missiles hit Kyiv bridges",
        "body": "Russian ballistic missiles hit three Dnipro bridges "
        "overnight; three killed, 15 hurt.",
    },
    {
        "tag": "MARKETS",
        "colour": (178, 106, 0),
        "headline": "Taiwan stocks crash 6.2%",
        "body": "Taiex sheds 2,393.60 to 36,033.29 in its worst week "
        "since 1991; TSMC below NT$2,000.",
    },
    {
        "tag": "EUROPE",
        "colour": (29, 78, 216),
        "headline": "Europe eyes Russia talks",
        "body": "Merz says new Ukraine talks including Europe are near; "
        "Putin invites EU leaders to Moscow.",
    },
    {
        "tag": "WORLD",
        "colour": (109, 40, 168),
        "headline": "US sanctions crime gangs",
        "body": "Washington blacklists Australia's Comancheros and "
        "Italy's \u2019Ndrangheta.",
    },
    {
        "tag": "TECH",
        "colour": (15, 118, 110),
        "headline": "Anthropic IPO closes today",
        "body": "Record $81.3bn listing closes after a debut that briefly "
        "valued the AI firm at $2tn.",
    },
    {
        "tag": "CULTURE",
        "colour": (14, 116, 144),
        "headline": "Fiona the hippo dies",
        "body": "Cincinnati Zoo's beloved hippo dies days after "
        "swallowing a visitor's hat.",
    },
]

LEAD_KICKER = "THE BREXIT RESET \u00b7 UK\u2013EU SUMMIT, BRUSSELS"
LEAD_LINES = ["UK AND EU SEAL", "BREXIT RESET DEAL"]
LEAD_DECK = (
    "Youth mobility for 100,000 a year each way; food checks end and "
    "carbon markets relink as Burnham and von der Leyen sign."
)
ALSO_TODAY = (
    "ALSO TODAY:  Harris meets Macron \u00b7 Genoa airport halts flights "
    "after drone \u00b7 Florida's 20th execution this year"
)


def draw_masthead(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([0, 0, CANVAS_W, 76], fill=MASTHEAD_BG)
    date_font = load_font(SANS_BOLD, 40)
    date = "FRIDAY, 20 NOVEMBER 2026"
    draw.text(
        ((CANVAS_W - date_font.getlength(date)) / 2, 16),
        date,
        font=date_font,
        fill=WHITE,
    )
    draw.rectangle([0, 76, CANVAS_W, 80], fill=GOLD)


def draw_hero(page: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    hero_top, hero_bottom = 80, 516
    photo = Image.open(HERO_PATH).convert("RGB")
    page.paste(cover_crop(photo, CANVAS_W, hero_bottom - hero_top, 0.35), (0, hero_top))
    shade_bottom(page, hero_bottom - 190, hero_bottom, 215)

    kicker_font = load_font(SANS_BOLD, 24)
    draw.text(
        (MARGIN, 350), LEAD_KICKER, font=kicker_font, fill=GOLD
    )
    headline_font = load_font(SERIF_BOLD, 62)
    y = 380
    for line in LEAD_LINES:
        draw.text((MARGIN, y), line, font=headline_font, fill=WHITE)
        y += 64


def draw_lead_deck(draw: ImageDraw.ImageDraw) -> None:
    deck_font = load_font(SERIF_ITALIC, 24)
    y = 530
    for line in wrap_text(LEAD_DECK, deck_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=deck_font, fill=INK)
        y += 30
    draw.line([(MARGIN, 600), (CANVAS_W - MARGIN, 600)], fill=RULE, width=2)


def draw_story_grid(draw: ImageDraw.ImageDraw) -> None:
    col_w = (CONTENT_W - 36) // 2
    row_tops = [616, 732, 848]
    for index, story in enumerate(STORIES):
        col = index % 2
        row = index // 2
        x = MARGIN + col * (col_w + 36)
        y = row_tops[row]

        tag_font = load_font(SANS_BOLD, 18)
        draw.text((x, y), story["tag"], font=tag_font, fill=story["colour"])

        head_font = load_font(SERIF_BOLD, 27)
        draw.text((x, y + 26), story["headline"], font=head_font, fill=INK)

        body_font = load_font(SANS, 20)
        line_y = y + 62
        for line in wrap_text(story["body"], body_font, col_w):
            draw.text((x, line_y), line, font=body_font, fill=MUTED)
            line_y += 25


def draw_also_today(draw: ImageDraw.ImageDraw) -> None:
    draw.line([(MARGIN, 958), (CANVAS_W - MARGIN, 958)], fill=RULE, width=2)
    strip_font = load_font(SANS, 19)
    y = 970
    for line in wrap_text(ALSO_TODAY, strip_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=strip_font, fill=INK)
        y += 24


def build() -> Path:
    # RGBA while drawing so the hero shading can composite; the saved
    # file is plain RGB.
    page = Image.new("RGBA", (CANVAS_W, CANVAS_H), PAPER + (255,))
    draw = ImageDraw.Draw(page)
    draw_masthead(draw)
    draw_hero(page, draw)
    draw_lead_deck(draw)
    draw_story_grid(draw)
    draw_also_today(draw)
    page.convert("RGB").save(OUTPUT_PATH, format="PNG")
    return OUTPUT_PATH


def main() -> None:
    target = build()
    raw = target.read_bytes()
    if len(raw) > MAX_BYTES:
        raise SystemExit(
            f"entry too big: {len(raw)} bytes exceeds the {MAX_BYTES} byte limit"
        )
    print(f"wrote {target} ({len(raw)} bytes)")
    print(f"sha256 {hashlib.sha256(raw).hexdigest()}")
    with Image.open(target) as check:
        print(f"size {check.size[0]}x{check.size[1]} mode {check.mode}")


if __name__ == "__main__":
    main()
