#!/usr/bin/env python3
"""Render poster.html to entry.png.

Dev-only tool; the graded entry never runs it. Chrome renders the poster at
its design size of 1200x1700 with a 2x device scale, and the shot is then
downsampled to 723x1024 - the bounty caps entries at 1024x1024 px, so the
poster keeps its 1200:1700 proportions at a legal size.

The result is quantised to a palette: the poster uses few flat colours plus
paper grain, so a palette keeps it visually identical while staying well
under the 1 MiB cap.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
RAW = ROOT / "poster_raw.png"
OUT = REPO / "entry.png"

DESIGN = (1200, 1700)
FINAL = (723, 1024)
MAX_BYTES = 1024 * 1024

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if pathlib.Path(c).exists():
            return c
    raise SystemExit("no Chrome or Edge found for rendering")


def shoot() -> None:
    subprocess.run([
        find_chrome(),
        "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--force-device-scale-factor=2",
        f"--window-size={DESIGN[0]},{DESIGN[1]}",
        "--virtual-time-budget=20000",
        f"--screenshot={RAW}",
        (ROOT / "poster.html").as_uri(),
    ], check=True, capture_output=True)


def main() -> int:
    shoot()
    img = Image.open(RAW).convert("RGB").resize(FINAL, Image.LANCZOS)

    for colors in (256, 192, 128, 96):
        pal = img.quantize(colors=colors, method=Image.MEDIANCUT, dither=0)
        pal.save(OUT, "PNG", optimize=True)
        size = OUT.stat().st_size
        if size <= MAX_BYTES * 0.80:
            print(f"wrote {OUT} ({size} bytes, {colors}-colour palette)")
            return 0
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)", file=sys.stderr)
    return 0 if OUT.stat().st_size <= MAX_BYTES else 1


if __name__ == "__main__":
    sys.exit(main())
