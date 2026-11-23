#!/usr/bin/env python3
"""Render entry.png: a one-image summary of the world news of 23 November 2026.

Dev-only tool. Requires Pillow and local TrueType fonts; it is NOT run by the
graded entry. main.py (standard library only) copies the PNG this produces.

Every headline below comes from a report published on 23 November 2026 by
Al Jazeera, France 24 or CNBC. Figures that the sources did not agree on are
written qualitatively ("dozens") rather than invented.
"""
from __future__ import annotations

import pathlib
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

BG = (14, 17, 22)
PANEL = (22, 27, 34)
RULE = (42, 50, 61)
INK = (242, 245, 248)
INK_DIM = (154, 167, 180)
RED = (216, 69, 60)
AMBER = (224, 163, 46)
BLUE = (109, 166, 217)

FONTS = pathlib.Path("C:/Windows/Fonts")
SERIF_B = FONTS / "cambriab.ttf"
COND_B = FONTS / "ARIALNB.TTF"
SANS_B = FONTS / "arialbd.ttf"
SANS = FONTS / "arial.ttf"


def font(path: pathlib.Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def track(draw, xy, text, fnt, fill, spacing=0.0):
    """Draw text with manual letter spacing; returns the advance width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing
    return x - xy[0]


def track_width(text, fnt, spacing=0.0):
    if not text:
        return 0.0
    return sum(fnt.getlength(c) for c in text) + spacing * (len(text) - 1)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def graticule(img, cx, cy, r):
    """A faint abstract globe: no claimed geography, just meridians."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    col = (109, 166, 217, 34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    for i in range(1, 4):
        rr = r * i / 4.0
        d.ellipse([cx - r, cy - rr, cx + r, cy + rr], outline=col, width=1)
    for i in range(1, 4):
        rr = r * i / 4.0
        d.ellipse([cx - rr, cy - r, cx + rr, cy + r], outline=col, width=1)
    img.alpha_composite(layer)


LEAD = {
    "tag": "UKRAINE",
    "head": "Russian strikes kill at least 15 in the Kyiv region",
    "deck": "Ukraine reports a fresh overnight barrage as Kyiv presses "
            "Washington to release Patriot interceptors.",
}

STORIES = [
    ("GULF", RED,
     "Houthis strike Saudi refinery as Hormuz attacks widen",
     "Brent near $92. Gulf states report further Iran-linked attacks."),
    ("MARKETS", AMBER,
     "AI-bubble fears drag Asian stocks lower",
     "Tech-heavy indices slide, with South Korea leading the retreat."),
    ("TURKEY", BLUE,
     "Thousands rally in Istanbul over media crackdown",
     "Crowds protest arrests of opposition figures and journalists."),
    ("INDONESIA", RED,
     "Dozens killed in factory fire as search goes on",
     "Recovery teams work through the wreckage; the toll keeps rising."),
    ("DR CONGO", AMBER,
     "WHO urges peace as fighting hits Ebola-zone hospital",
     "Patients and health workers are at grave risk, its chief says."),
    ("BELGIUM", BLUE,
     "Anti-austerity strike shuts the country's airports",
     "A national walkout grounds flights and halts public transport."),
]


def main() -> None:
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_kick = font(SANS_B, 15)
    f_mast = font(SERIF_B, 54)
    f_lead = font(COND_B, 50)
    f_deck = font(SANS, 18)
    f_tag = font(SANS_B, 14)
    f_head = font(COND_B, 29)
    f_sub = font(SANS, 15)
    f_foot = font(SANS, 14)

    M = 56  # page margin

    # ---- masthead -------------------------------------------------------
    track(d, (M, 42), "THE WORLD TODAY", f_kick, INK_DIM, 3.4)
    d.text((M, 68), "Monday 23 November 2026", font=f_mast, fill=INK)
    bar = track_width("THE WORLD TODAY", f_kick, 3.4)
    d.line([(M, 60), (M + bar, 60)], fill=RULE, width=1)
    d.line([(M, 142), (W - M, 142)], fill=RULE, width=2)

    # ---- lead ------------------------------------------------------------
    graticule(img, W - 150, 268, 190)
    d = ImageDraw.Draw(img)

    y = 170
    d.rectangle([M, y + 3, M + 4, y + 21], fill=RED)
    track(d, (M + 16, y + 4), LEAD["tag"], f_tag, RED, 2.2)
    y += 34
    for line in wrap(LEAD["head"], f_lead, W - 2 * M - 150):
        d.text((M, y), line, font=f_lead, fill=INK)
        y += 54
    y += 8
    for line in wrap(LEAD["deck"], f_deck, 560):
        d.text((M, y), line, font=f_deck, fill=INK_DIM)
        y += 25

    # ---- secondary grid --------------------------------------------------
    top = 416
    col_w = (W - 2 * M - 28) // 2
    row_h = 172
    for i, (tag, col, head, sub) in enumerate(STORIES):
        cx = M + (i % 2) * (col_w + 28)
        cy = top + (i // 2) * row_h
        d.rectangle([cx, cy, cx + col_w, cy + row_h - 22], fill=PANEL)
        d.rectangle([cx, cy, cx + 3, cy + row_h - 22], fill=col)

        ty = cy + 16
        track(d, (cx + 18, ty), tag, f_tag, col, 2.0)
        ty += 26
        for line in wrap(head, f_head, col_w - 36)[:2]:
            d.text((cx + 18, ty), line, font=f_head, fill=INK)
            ty += 32
        ty += 4
        for line in wrap(sub, f_sub, col_w - 36)[:2]:
            d.text((cx + 18, ty), line, font=f_sub, fill=INK_DIM)
            ty += 20

    # ---- footer ----------------------------------------------------------
    fy = H - 60
    d.line([(M, fy), (W - M, fy)], fill=RULE, width=1)
    d.text((M, fy + 16),
           "Compiled from reports published 23 November 2026 by "
           "Al Jazeera, France 24 and CNBC.",
           font=f_foot, fill=INK_DIM)

    out = pathlib.Path(__file__).resolve().parent.parent / "entry.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
