#!/usr/bin/env python3
"""make.fun entry writer.

Copies the sibling entry.png (1024x1024, 18 November 2026 world news collage)
to <output_dir>/entry.png.

Output directory resolution order:
  1. $MAKEFUN_OUTPUT_DIR (if set and non-empty)
  2. /output

Usage:
  python3.13 main.py           # validate + write <output_dir>/entry.png
  python3.13 main.py --check   # validate + print sha256 only, write nothing

Standard library only. No network access.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_SIZE = 1048576  # 1 MiB
SRC_NAME = "entry.png"
DEST_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def script_dir() -> Path:
    """Directory containing this script, independent of the current working directory."""
    return Path(__file__).resolve().parent


def source_path() -> Path:
    return script_dir() / SRC_NAME


def output_dir() -> Path:
    """$MAKEFUN_OUTPUT_DIR if set and non-empty, else /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    raw = raw.strip()
    if not raw:
        return Path(DEFAULT_OUTPUT_DIR)
    return Path(raw)


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def validate(path: Path) -> int:
    """Check the source image is a non-empty PNG within the size cap. Returns byte count."""
    if not path.exists():
        raise ValueError(f"missing source image: {path}")
    if not path.is_file():
        raise ValueError(f"source is not a regular file: {path}")

    size = path.stat().st_size
    if size <= 0:
        raise ValueError(f"source image is empty: {path}")
    if size > MAX_SIZE:
        raise ValueError(f"source image too large: {size} bytes (max {MAX_SIZE})")

    with path.open("rb") as fh:
        head = fh.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        raise ValueError(
            f"source image is not a PNG: signature {head.hex()} != {PNG_SIGNATURE.hex()}"
        )
    return size


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str]) -> int:
    rest = argv[1:]
    check_only = False
    for arg in rest:
        if arg in ("--check", "-c"):
            check_only = True
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        else:
            return fail(f"unknown argument: {arg!r} (supported: --check)")

    try:
        src = source_path()
        size = validate(src)
    except ValueError as exc:
        return fail(str(exc))
    except OSError as exc:
        return fail(f"cannot read {source_path()}: {exc}")

    if check_only:
        print(f"CHECK ok: {src} {size} bytes sha256={sha256_of(src)} (nothing written)")
        return 0

    dest_dir = output_dir()
    dest = dest_dir / DEST_NAME
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    except OSError as exc:
        return fail(f"cannot write {dest}: {exc}")

    try:
        written = dest.stat().st_size
    except OSError as exc:
        return fail(f"cannot stat written file {dest}: {exc}")

    if written != size:
        return fail(f"size mismatch after copy: wrote {written} bytes, expected {size}")

    print(f"OK: wrote {dest} ({written} bytes, sha256={sha256_of(dest)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
