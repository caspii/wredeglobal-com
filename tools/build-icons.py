#!/usr/bin/env python3
"""Render the favicon and app icons from the two source SVGs.

    DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 tools/build-icons.py

Needs `pip install cairosvg` and `brew install cairo`. The DYLD line is only
needed on macOS, where cairosvg cannot find Homebrew's libcairo on its own.
"""
import io, os, sys

import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIELD = os.path.join(ROOT, "assets/arms/arms-favicon.svg")  # transparent
TILE   = os.path.join(ROOT, "assets/arms/arms-icon.svg")     # solid square


def render(src, w=None, h=None):
    png = cairosvg.svg2png(url=src, output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main():
    # Solid tiles. iOS composites apple-touch-icon onto black, so these
    # must not be transparent.
    for px, name in ((180, "apple-touch-icon.png"),
                     (192, "icon-192.png"),
                     (512, "icon-512.png")):
        render(TILE, px, px).convert("RGB").save(os.path.join(ROOT, name), optimize=True)
        print(f"  {name:22s} {px}x{px}")

    # favicon.ico: transparent, so it sits on light or dark browser chrome.
    frames = []
    for px in (16, 24, 32, 48, 64):
        sh = render(SHIELD, h=round(px * 0.94))   # keeps the 200:238 ratio
        f = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        f.paste(sh, ((px - sh.width) // 2, (px - sh.height) // 2), sh)
        frames.append(f)
    frames[-1].save(os.path.join(ROOT, "favicon.ico"), format="ICO",
                    sizes=[f.size for f in frames])
    print(f"  {'favicon.ico':22s} {[f.size for f in frames]}")

    print("done")


if __name__ == "__main__":
    sys.exit(main())
