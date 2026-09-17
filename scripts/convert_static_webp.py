#!/usr/bin/env python3
"""Конвертація растрових зображень mockup → static WebP."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow не встановлено. pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "mockup" / "img"
OUT = ROOT / "src" / "core" / "static" / "images"
QUALITY = 85


def convert_one(src: Path) -> Path:
    rel = src.relative_to(SRC)
    dest = OUT / rel.with_suffix(".webp")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        if img.mode == "RGBA":
            pass
        elif "A" in img.getbands():
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        img.save(dest, format="WEBP", quality=QUALITY, method=4)
    return dest


def main() -> None:
    if not SRC.exists():
        print(f"Немає джерела: {SRC}")
        sys.exit(1)
    files = sorted(
        list(SRC.rglob("*.jpg"))
        + list(SRC.rglob("*.jpeg"))
        + list(SRC.rglob("*.png"))
    )
    for src in files:
        dest = convert_one(src)
        print(f"{src.relative_to(ROOT)} → {dest.relative_to(ROOT)}")
    print(f"Готово: {len(files)} файлів, quality={QUALITY}")


if __name__ == "__main__":
    main()
