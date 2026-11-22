#!/usr/bin/env python3
"""Entrypoint for make.fun news-image-20261122 (v7).

Copies the pre-rendered entry.png into the output directory and
validates the competition gate: the PNG must be at most 1 MiB and
at most 1024x1024 pixels. Stdlib only; deterministic (a byte copy).
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576  # 1 MiB
MAX_SIDE = 1024


def png_size(path):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a valid PNG")
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png not found next to main.py")
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit"
                         % size)
    width, height = png_size(src)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("entry.png (%d bytes, %dx%d) -> %s" % (size, width, height, dst))


if __name__ == "__main__":
    main()
