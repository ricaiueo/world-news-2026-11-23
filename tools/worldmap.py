"""A coarse 72x36 equirectangular land mask, hand-encoded as cell ranges.

Resolution is 5 degrees per cell: enough for a stylised halftone dot map with
located markers, not a cartographic product. Antarctica is omitted, as it is
on most news maps. Row r covers latitude 90-5r down to 85-5r; column c covers
longitude -180+5c to -175+5c.
"""
from __future__ import annotations

COLS, ROWS = 72, 36

# row -> list of inclusive (first_col, last_col) spans of land
LAND: dict[int, list[tuple[int, int]]] = {
    1:  [(16, 32)],
    2:  [(14, 32), (39, 39), (55, 56)],
    3:  [(2, 7), (12, 32), (38, 40), (44, 70)],
    4:  [(2, 8), (8, 25), (26, 31), (38, 42), (42, 71)],
    5:  [(2, 8), (9, 26), (28, 31), (35, 36), (38, 42), (42, 71)],
    6:  [(2, 7), (9, 27), (36, 43), (43, 71)],
    7:  [(9, 28), (34, 36), (36, 44), (44, 71)],
    8:  [(10, 29), (35, 44), (44, 71)],
    9:  [(11, 29), (34, 44), (44, 71), (62, 64)],
    10: [(12, 29), (34, 44), (44, 52), (54, 64)],
    11: [(13, 29), (34, 44), (44, 52), (50, 64)],
    12: [(14, 28), (33, 44), (44, 52), (50, 62)],
    13: [(15, 21), (23, 25), (33, 44), (44, 50), (50, 62)],
    14: [(16, 21), (23, 26), (33, 45), (44, 49), (50, 62)],
    15: [(17, 22), (24, 28), (33, 46), (51, 56), (57, 62)],
    16: [(19, 22), (24, 29), (34, 47), (52, 52), (57, 62)],
    17: [(23, 30), (34, 48), (56, 63)],
    18: [(23, 31), (34, 48), (56, 64)],
    19: [(23, 31), (35, 48), (57, 66)],
    20: [(23, 31), (35, 47), (58, 67)],
    21: [(24, 31), (35, 46), (60, 67)],
    22: [(24, 31), (35, 45), (58, 67)],
    23: [(25, 31), (35, 44), (58, 67)],
    24: [(26, 31), (36, 42), (58, 66)],
    25: [(27, 30), (58, 62), (65, 65), (69, 70)],
    26: [(27, 30), (69, 71)],
    27: [(28, 30), (70, 70)],
    28: [(28, 30)],
    29: [(29, 30)],
}


def is_land(col: int, row: int) -> bool:
    for first, last in LAND.get(row, ()):
        if first <= col <= last:
            return True
    return False


def cell(lon: float, lat: float) -> tuple[int, int]:
    """Map longitude/latitude to a (col, row) cell."""
    col = int((lon + 180.0) / 5.0)
    row = int((90.0 - lat) / 5.0)
    return max(0, min(COLS - 1, col)), max(0, min(ROWS - 1, row))


def preview() -> str:
    lines = []
    for r in range(ROWS):
        lines.append("".join("#" if is_land(c, r) else "." for c in range(COLS)))
    return "\n".join(lines)


if __name__ == "__main__":
    print(preview())
