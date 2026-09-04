#!/usr/bin/env python3
"""Render the favicon and app icons from the arms SVGs.

    python3 tools/build-icons.py                  # rebuild the site icons
    python3 tools/build-icons.py --source flat    # ...from arms-flat.svg instead
    python3 tools/build-icons.py --all            # also render every candidate

Needs `pip install cairosvg`, and on macOS `brew install cairo`. On macOS the
script re-executes itself with DYLD_FALLBACK_LIBRARY_PATH set, because
cairosvg cannot find Homebrew's libcairo on its own.
"""
import argparse
import ctypes.util
import glob
import io
import os
import sys

# --- make libcairo findable on macOS, then carry on ------------------------
if (sys.platform == "darwin" and not ctypes.util.find_library("cairo")
        and "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ):
    for _d in ("/opt/homebrew/lib", "/usr/local/lib"):
        if os.path.exists(os.path.join(_d, "libcairo.2.dylib")):
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = _d
            os.execv(sys.executable, [sys.executable] + sys.argv)

import cairosvg                      # noqa: E402
from PIL import Image                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARMS = os.path.join(ROOT, "assets/arms")
CANDIDATES = os.path.join(ARMS, "favicons")

TILE_BG      = "#14130f"   # matches the site's dark paper
TILE_FILL    = 0.66        # shield height as a fraction of the tile
ICO_SIZES    = (16, 24, 32, 48, 64)
PREVIEW_SIZES = (16, 32, 48)


def render(src, w=None, h=None):
    """Rasterise an SVG at an exact size, keeping transparency."""
    png = cairosvg.svg2png(url=src, output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def square(img, px, bg=None):
    """Centre img on a px-by-px canvas, transparent unless bg is given."""
    out = Image.new("RGBA", (px, px), bg or (0, 0, 0, 0))
    out.paste(img, ((px - img.width) // 2, (px - img.height) // 2), img)
    return out


def write_ico(src, path, sizes=ICO_SIZES):
    """Transparent .ico, so it reads on light and dark browser chrome."""
    frames = [square(render(src, h=round(px * 0.94)), px) for px in sizes]
    frames[-1].save(path, format="ICO", sizes=[f.size for f in frames])
    return frames


def write_tile(src, path, px):
    """Solid square. iOS composites apple-touch-icon onto black, so the
    tile has to carry its own background."""
    shield = render(src, h=round(px * TILE_FILL))
    square(shield, px, TILE_BG).convert("RGB").save(path, optimize=True)


def build_site_icons(source):
    src = os.path.join(ARMS, f"arms-{source}.svg")
    if not os.path.exists(src):
        sys.exit(f"no such arms version: {src}")
    print(f"site icons from arms-{source}.svg")

    write_ico(src, os.path.join(ROOT, "favicon.ico"))
    print(f"  {'favicon.ico':22s} {list(ICO_SIZES)}")

    for px, name in ((180, "apple-touch-icon.png"),
                     (192, "icon-192.png"),
                     (512, "icon-512.png")):
        write_tile(src, os.path.join(ROOT, name), px)
        print(f"  {name:22s} {px}x{px}")

    # The scalable tab icon is just the source SVG, copied to the root.
    with open(src) as f:
        svg = f.read()
    with open(os.path.join(ROOT, "favicon.svg"), "w") as f:
        f.write(svg)
    print(f"  {'favicon.svg':22s} copy of arms-{source}.svg")


def build_candidates():
    """One .ico plus preview PNGs for every arms version, so they can be
    compared at the sizes a browser actually uses."""
    os.makedirs(CANDIDATES, exist_ok=True)
    names = sorted(os.path.basename(p)[5:-4]
                   for p in glob.glob(os.path.join(ARMS, "arms-*.svg")))
    print(f"\ncandidates -> assets/arms/favicons/ ({len(names)} versions)")
    for n in names:
        src = os.path.join(ARMS, f"arms-{n}.svg")
        write_ico(src, os.path.join(CANDIDATES, f"{n}.ico"))
        for px in PREVIEW_SIZES:
            square(render(src, h=round(px * 0.94)), px).save(
                os.path.join(CANDIDATES, f"{n}-{px}.png"))
        print(f"  {n:12s} .ico + {len(PREVIEW_SIZES)} preview PNGs")
    write_candidates_page(names)
    return names


def write_candidates_page(names):
    def cells(n):
        c = "".join(f'        <td><img src="{n}-{px}.png" width="{px}" height="{px}" alt=""></td>\n'
                    for px in PREVIEW_SIZES)
        # the 16px file blown up 4x with nearest-neighbour, so you can see
        # exactly which pixels survive
        c += (f'        <td><img class="zoom" src="{n}-16.png" width="64" height="64" alt=""></td>\n')
        return c

    rows = "\n".join(f'''      <tr>
        <th scope="row">{n}</th>
{cells(n)}        <td class="file"><code>arms-{n}.svg</code></td>
      </tr>''' for n in names)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Favicon candidates — Wrede arms</title>
<meta name="robots" content="noindex">
<style>
  :root {{ --ink:#1a1814; --soft:#6b6455; --paper:#faf8f3; --rule:#e2ddd0; }}
  body {{ margin:0; padding:3rem 1.5rem 5rem; background:var(--paper); color:var(--ink);
         font:16px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
  .wrap {{ max-width:44rem; margin:0 auto; }}
  h1 {{ font-family:ui-serif, Georgia, serif; font-weight:500; font-size:1.75rem; margin:0 0 .4rem; }}
  p  {{ color:var(--soft); max-width:36rem; }}
  table {{ border-collapse:collapse; margin:2.5rem 0 0; }}
  caption {{ text-align:left; font-weight:600; padding:0 0 .75rem; color:var(--ink); }}
  th, td {{ padding:.65rem 1.1rem; text-align:center; vertical-align:middle; }}
  th[scope=row] {{ text-align:left; font-weight:600; }}
  thead th {{ font-size:.75rem; font-weight:500; color:var(--soft); text-transform:uppercase; letter-spacing:.1em; }}
  tbody tr {{ border-top:1px solid var(--rule); }}
  .dark {{ background:#14130f; color:#f2efe6; border-radius:10px; }}
  .dark tbody tr {{ border-top-color:#302d25; }}
  .file code {{ font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:.75rem; color:var(--soft); }}
  .dark .file code {{ color:#a29d90; }}
  img {{ display:block; margin:0 auto; }}
  img.zoom {{ image-rendering:pixelated; outline:1px solid var(--rule); }}
  .dark img.zoom {{ outline-color:#302d25; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Favicon candidates</h1>
  <p>
    Each version of the arms rendered at the sizes a browser actually uses.
    Below 32px only the reduced marks stay readable — the detailed drawings
    turn to mush, and the line version nearly vanishes.
  </p>

  <table>
    <caption>On light</caption>
    <thead><tr><th></th>{"".join(f"<th>{px}px</th>" for px in PREVIEW_SIZES)}<th>16px &times;4</th><th></th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>

  <table class="dark">
    <caption>On dark</caption>
    <thead><tr><th></th>{"".join(f"<th>{px}px</th>" for px in PREVIEW_SIZES)}<th>16px &times;4</th><th></th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>

  <p style="margin-top:2.5rem">
    To make one of these the site favicon:<br>
    <code>python3 tools/build-icons.py --source &lt;name&gt;</code>
  </p>
</div>
</body>
</html>
'''
    with open(os.path.join(CANDIDATES, "index.html"), "w") as f:
        f.write(html)
    print("  index.html   comparison page")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--source", default="favicon",
                    help="which assets/arms/arms-NAME.svg to use (default: favicon)")
    ap.add_argument("--all", action="store_true",
                    help="also render a candidate set for every arms version")
    a = ap.parse_args()

    build_site_icons(a.source)
    if a.all:
        build_candidates()
    print("\ndone")


if __name__ == "__main__":
    main()
