#!/usr/bin/env python3
"""Entrypoint for make.fun news-image-20261122.

Copies the pre-built entry.png next to this file to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png when set, for local runs).
Standard library only, no network. Deterministic: the same bytes
every run.
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_DIM = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_png(path):
    """Check the entry image: PNG signature, <= 1 MiB, <= 1024x1024."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)
    with open(path, "rb") as f:
        header = f.read(33)
    if not header.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))


def main():
    src = os.path.join(HERE, "entry.png")
    validate_png(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
