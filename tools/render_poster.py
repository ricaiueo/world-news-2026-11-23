#!/usr/bin/env python3
"""Render entry.png: a broadsheet news poster for 23 November 2026.

Dev-only tool (needs Pillow and local fonts); the graded entry never runs it.
Drawn at 2x and downsampled, so the committed PNG stays inside the bounty's
1024x1024 cap while keeping type crisp.

Every headline, figure and location below comes from a report published on
23 November 2026 by Al Jazeera, France 24 or CNBC. Nothing is invented; where
sources disagreed on a developing toll, the figure is attributed to the source
that published it.
"""
from __future__ import annotations

import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import worldmap  # noqa: E402

S = 2                      # supersample factor
W, H = 723 * S, 1024 * S
M = 38 * S                 # page margin

PAPER = (242, 238, 228)
INK = (26, 24, 22)
SPOT = (217, 58, 30)
MUTED = (122, 115, 104)
RULE = (196, 189, 175)

F = pathlib.Path("C:/Windows/Fonts")
COND = F / "FRAMDCN.TTF"      # Franklin Gothic Medium Condensed
GOTH = F / "framd.ttf"        # Franklin Gothic Medium
SERIF = F / "georgia.ttf"
SERIF_I = F / "georgiai.ttf"


def ft(path, size):
    return ImageFont.truetype(str(path), int(size * S))


def track(d, xy, text, font, fill, sp=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + sp * S
    return x - xy[0]


def track_w(text, font, sp=0.0):
    if not text:
        return 0.0
    return sum(font.getlength(c) for c in text) + sp * S * (len(text) - 1)


def wrap(text, font, maxw):
    out, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if font.getlength(t) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, xy, text, font, fill, maxw, lh, maxlines=99):
    x, y = xy
    for line in wrap(text, font, maxw)[:maxlines]:
        d.text((x, y), line, font=font, fill=fill)
        y += lh * S
    return y


# ---------------------------------------------------------------- content
LEAD = dict(
    n="1", kicker="WAR", place="KYIV REGION, UKRAINE",
    head="Russian strikes kill at least 15 in the Kyiv region",
    deck="Ukrainian officials reported a fresh overnight barrage across the "
         "region as Kyiv pressed Washington to release Patriot interceptors.",
    src="France 24", lon=30.5, lat=50.4,
)

STORIES = [
    dict(n="2", kicker="ENERGY", place="STRAIT OF HORMUZ",
         head="Houthis hit Saudi refinery as Hormuz attacks widen",
         deck="Gulf states reported further Iran-linked attacks on shipping "
              "and industry over the weekend.",
         src="CNBC", lon=56.5, lat=26.6),
    dict(n="3", kicker="MARKETS", place="SEOUL",
         head="AI-bubble fears drag Asian stocks lower",
         deck="Tech-heavy indices slid, with South Korea leading the retreat.",
         src="Al Jazeera", lon=127.0, lat=37.6),
    dict(n="4", kicker="TECHNOLOGY", place="WASHINGTON",
         head="US widens Nvidia chip inquiry to Megaspeed",
         deck="A new figure emerged in the investigation into diverted "
              "high-end processors.",
         src="CNBC", lon=-77.0, lat=38.9),
    dict(n="5", kicker="CLIMATE", place="LONDON",
         head="Britain digs new reservoirs against drought",
         deck="Water companies move on storage after repeated dry years.",
         src="France 24", lon=-0.1, lat=51.5),
    dict(n="6", kicker="DISASTER", place="INDONESIA",
         head="Factory fire toll climbs as search goes on",
         deck="Police removed 24 body bags from the site; recovery continues.",
         src="Al Jazeera", lon=106.8, lat=-6.2),
    dict(n="7", kicker="SPORT", place="NEW ZEALAND",
         head="New Zealand battle to 239-5 to draw first Test",
         deck="A rearguard stand denied India the opener against the hosts.",
         src="France 24", lon=172.6, lat=-43.5),
]

FIGURES = [
    ("15", "killed in strikes on the Kyiv region", "France 24"),
    ("$92.35", "Brent crude, early Asia trading", "CNBC"),
    ("350%", "rise in attacks on medics, occupied West Bank", "Al Jazeera"),
]

CLOCKS = [("WASHINGTON", -5), ("LONDON", 0), ("KYIV", 2), ("RIYADH", 3),
          ("JAKARTA", 7), ("SEOUL", 9), ("AUCKLAND", 13)]

QUOTE = "Patients and health workers are at grave risk."
QUOTE_SRC = "WHO - ON FIGHTING NEAR AN EBOLA-ZONE HOSPITAL, DR CONGO - AL JAZEERA"


# ------------------------------------------------------------------ parts
def halftone(img, box, color, step, r0, r1):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    rows = int((y1 - y0) / step)
    cols = int((x1 - x0) / step)
    for i in range(cols):
        t = i / max(1, cols - 1)
        r = r0 + (r1 - r0) * t
        if r <= 0.2:
            continue
        for j in range(rows):
            cx = x0 + i * step + (step / 2 if j % 2 else 0)
            cy = y0 + j * step
            if cx > x1:
                continue
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def illustration(img, box):
    """Flat-shape linocut: a skyline under a struck sky."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=SPOT)
    halftone(img, (x0 + 6 * S, y0 + 6 * S, x1 - 6 * S, y0 + (y1 - y0) * 0.5),
             PAPER, 9 * S, 3.4 * S, 0.3 * S)
    d = ImageDraw.Draw(img)

    d.line([(x0 + 18 * S, y0 + 22 * S), (x1 - 34 * S, y0 + 84 * S)],
           fill=PAPER, width=int(2.2 * S))

    base = y1
    span = x1 - x0
    blocks = [(0, 112, 86), (90, 150, 120), (152, 206, 70),
              (208, 268, 136), (270, 320, 96)]
    for bx0, bx1, bh in blocks:
        rx0 = x0 + span * bx0 / 320.0
        rx1 = x0 + span * bx1 / 320.0
        top = base - bh * S
        d.rectangle([rx0, top, rx1, base], fill=INK)
        wy = top + 9 * S
        while wy < base - 12 * S:
            wx = rx0 + 9 * S
            while wx < rx1 - 12 * S:
                d.rectangle([wx, wy, wx + 5 * S, wy + 7 * S], fill=SPOT)
                wx += 13 * S
            wy += 15 * S

    nx0 = x0 + span * 208 / 320.0
    d.polygon([(nx0, base - 136 * S), (nx0 + 34 * S, base - 136 * S),
               (nx0 + 10 * S, base - 96 * S), (nx0 + 40 * S, base - 74 * S),
               (nx0, base - 70 * S)], fill=SPOT)


def dotmap(img, box, stories, rows=31):
    """Draw the land dots. Rows below `rows` are empty ocean/Antarctica and
    are left out, so the map fills its box instead of floating in a band."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    cw = (x1 - x0) / worldmap.COLS
    ch = (y1 - y0) / rows
    r = cw * 0.30
    for row in range(rows):
        for col in range(worldmap.COLS):
            if not worldmap.is_land(col, row):
                continue
            cx = x0 + (col + 0.5) * cw
            cy = y0 + (row + 0.5) * ch
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 171, 158))

    f = ft(GOTH, 9)
    for st in stories:
        col, row = worldmap.cell(st["lon"], st["lat"])
        cx = x0 + (col + 0.5) * cw
        cy = y0 + (row + 0.5) * ch
        rr = 8 * S
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=SPOT)
        tw = f.getlength(st["n"])
        d.text((cx - tw / 2, cy - 6 * S), st["n"], font=f, fill=PAPER)


def grain(img, seed=20261123):
    px = img.load()
    state = seed
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            if (state >> 16) % 23 == 0:
                r, g, b = px[x, y]
                px[x, y] = (max(0, r - 9), max(0, g - 9), max(0, b - 9))


# ------------------------------------------------------------------- page
def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    right = W - M

    f_mast = ft(COND, 62)
    f_sub = ft(GOTH, 11)
    f_kick = ft(GOTH, 9)
    f_lead = ft(COND, 44)
    f_deck = ft(SERIF, 11)
    f_head = ft(COND, 19)
    f_body = ft(SERIF, 9)
    f_fig = ft(COND, 38)
    f_small = ft(GOTH, 8)
    f_quote = ft(SERIF_I, 17)
    f_src = ft(SERIF_I, 8)
    f_clock = ft(COND, 15)

    # --- masthead
    y = M - 6 * S
    track(d, (M, y), "THE WORLD", f_mast, INK, 2.0)
    d.line([(M, y + 84 * S), (right, y + 84 * S)], fill=INK, width=int(3 * S))
    yy = y + 90 * S
    track(d, (M, yy), "MONDAY 23 NOVEMBER 2026", f_sub, INK, 2.6)
    issue = "VOL. 1, NO. 327"
    track(d, (right - track_w(issue, f_sub, 2.6), yy), issue, f_sub, MUTED, 2.6)
    d.line([(M, yy + 22 * S), (right, yy + 22 * S)], fill=RULE, width=S)

    # --- lead
    top = yy + 34 * S
    lead_w = 340 * S
    ill_x = M + lead_w + 16 * S
    illustration(img, (ill_x, top, right, top + 176 * S))
    d = ImageDraw.Draw(img)

    d.rectangle([M, top + 2 * S, M + 3 * S, top + 14 * S], fill=SPOT)
    track(d, (M + 9 * S, top + 2 * S), LEAD["n"] + "  " + LEAD["kicker"],
          f_kick, SPOT, 2.2)
    ly = top + 20 * S
    for line in wrap(LEAD["head"], f_lead, lead_w):
        d.text((M, ly), line, font=f_lead, fill=INK)
        ly += 38 * S
    ly += 6 * S
    ly = para(d, (M, ly), LEAD["deck"], f_deck, INK, lead_w, 16)
    track(d, (M, ly + 5 * S), LEAD["place"] + " - " + LEAD["src"].upper(),
          f_small, MUTED, 1.6)

    # --- figures band
    fy = top + 194 * S
    d.line([(M, fy), (right, fy)], fill=INK, width=int(2 * S))
    cw = (right - M) / 3
    for i, (big, label, src) in enumerate(FIGURES):
        cx = M + i * cw
        if i:
            d.line([(cx - 9 * S, fy + 8 * S), (cx - 9 * S, fy + 76 * S)],
                   fill=RULE, width=S)
        d.text((cx, fy + 8 * S), big, font=f_fig, fill=SPOT)
        para(d, (cx, fy + 48 * S), label, f_body, INK, cw - 22 * S, 12, 2)
        track(d, (cx, fy + 72 * S), src.upper(), f_small, MUTED, 1.4)
    d.line([(M, fy + 84 * S), (right, fy + 84 * S)], fill=RULE, width=S)

    # --- map + numbered index
    my = fy + 98 * S
    map_w = 396 * S
    dotmap(img, (M, my, M + map_w, my + 170 * S), [LEAD] + STORIES)
    d = ImageDraw.Draw(img)
    track(d, (M, my + 176 * S), "WHERE THE DAY'S NEWS BROKE", f_kick, MUTED, 2.2)

    lx = M + map_w + 18 * S
    ly2 = my + 2 * S
    for st in [LEAD] + STORIES:
        d.ellipse([lx, ly2, lx + 13 * S, ly2 + 13 * S], fill=INK)
        nw = f_small.getlength(st["n"])
        d.text((lx + 6.5 * S - nw / 2, ly2 + 2.5 * S), st["n"],
               font=f_small, fill=PAPER)
        track(d, (lx + 19 * S, ly2 + 2 * S), st["place"], f_small, INK, 1.4)
        ly2 += 24 * S

    # --- pull quote
    qy = my + 194 * S
    d.line([(M, qy), (right, qy)], fill=RULE, width=S)
    d.rectangle([M, qy + 10 * S, M + 3 * S, qy + 34 * S], fill=SPOT)
    para(d, (M + 14 * S, qy + 8 * S), QUOTE, f_quote, INK, 440 * S, 23)
    track(d, (M + 14 * S, qy + 38 * S), QUOTE_SRC, f_small, MUTED, 1.2)

    # --- secondary stories, three unequal columns
    sy = qy + 66 * S
    d.line([(M, sy - 10 * S), (right, sy - 10 * S)], fill=INK, width=int(2 * S))
    widths = [248 * S, 208 * S, 175 * S]
    xs, acc = [], M
    for w in widths:
        xs.append(acc)
        acc += w + 9 * S
    for i, st in enumerate(STORIES):
        cx = xs[i % 3]
        colw = widths[i % 3]
        cy = sy + (i // 3) * 106 * S
        if i % 3:
            d.line([(cx - 5 * S, cy - 2 * S), (cx - 5 * S, cy + 94 * S)],
                   fill=RULE, width=S)
        track(d, (cx, cy), st["kicker"], f_kick, SPOT, 2.0)
        hy = para(d, (cx, cy + 13 * S), st["n"] + "  " + st["head"],
                  f_head, INK, colw, 19, 3)
        hy = para(d, (cx, hy + 4 * S), st["deck"], f_body, INK, colw, 12, 3)
        track(d, (cx, hy + 3 * S), st["src"].upper(), f_small, MUTED, 1.4)

    # --- time strip
    ty = sy + 220 * S
    d.line([(M, ty), (right, ty)], fill=INK, width=int(2 * S))
    track(d, (M, ty + 8 * S), "LOCAL TIME AT 07:00 UTC", f_kick, MUTED, 2.2)
    step = (right - M) / len(CLOCKS)
    for i, (city, off) in enumerate(CLOCKS):
        cx = M + i * step
        hh = (7 + off) % 24
        d.text((cx, ty + 24 * S), "%02d:00" % hh, font=f_clock, fill=INK)
        track(d, (cx, ty + 44 * S), city, f_small, MUTED, 1.0)
        if i:
            d.line([(cx - 6 * S, ty + 22 * S), (cx - 6 * S, ty + 54 * S)],
                   fill=RULE, width=S)

    # --- footer
    gy = H - 26 * S
    d.line([(M, gy - 9 * S), (right, gy - 9 * S)], fill=RULE, width=S)
    d.text((M, gy), "Sources: Al Jazeera, France 24, CNBC - reports published "
                    "23 November 2026.", font=f_src, fill=MUTED)

    grain(img)
    out = pathlib.Path(__file__).resolve().parent.parent / "entry.png"
    img.resize((723, 1024), Image.LANCZOS).save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, out.stat().st_size))


if __name__ == "__main__":
    main()
