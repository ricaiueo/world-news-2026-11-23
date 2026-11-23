#!/usr/bin/env python3
"""Write one image summarising the world news of 23 November 2026.

The image is rendered ahead of time and committed to this repository as
entry.png; this program copies it to the output directory. That keeps the
run deterministic and free of any network access or third-party package:
the bytes written are exactly the bytes committed.

Before writing, the committed file is checked against the competition's
guardrails (a whole PNG, at most 1 MiB, at most 1024x1024) so a bad build
fails here with a clear message instead of at grading time.
"""
from __future__ import annotations

import os
import pathlib
import struct
import sys

OUTPUT_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MAX_EDGE = 1024


def output_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check(data: bytes) -> None:
    """Raise ValueError unless the bytes are a PNG within the size caps."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR header")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_EDGE or height > MAX_EDGE:
        raise ValueError(f"entry.png is {width}x{height}, over {MAX_EDGE} px")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise ValueError("entry.png is truncated: no IEND chunk")


def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    src = here / OUTPUT_NAME
    try:
        data = src.read_bytes()
    except OSError as exc:
        print(f"cannot read {src}: {exc}", file=sys.stderr)
        return 1

    try:
        check(data)
    except ValueError as exc:
        print(f"refusing to write a bad entry: {exc}", file=sys.stderr)
        return 1

    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / OUTPUT_NAME).write_bytes(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
