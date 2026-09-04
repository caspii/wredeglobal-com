"""Generate the SVG versions of the Wrede family arms (Stammwappen).

Run:  python3 assets/arms/generate.py
It rewrites every arms-*.svg in this folder except arms-favicon.svg,
which is hand-written because it is a different, reduced mark.

Blazon, from roskildehistorie.dk:
  "Das in Rot und Gold gespaltene Stammwappen zeigt einen Kranz mit
   fuenf (1:2:2) Rosen verwechselter Farbe."
  Per pale gules and or, a wreath set with five roses, counterchanged.

The counterchange is not painted rose by rose. The wreath is drawn once
into <defs>, then stamped twice - gold clipped to the red half, red
clipped to the gold half - so the line of the pale cuts straight through
the top rose, as it does in the source drawing.
"""
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))

GULES = "#d9271b"   # sampled from the source drawing
OR    = "#f9c301"
INK   = "#3a1c10"
SEED  = "#f6ecc9"

W, H   = 200, 238
SHIELD = "M10 10H190V128C190 172 158 206 100 229C42 206 10 172 10 128Z"
CX, CY = 100, 114
R      = 58
ROSE_R = 19

# per style: leaves per gap, leaf length, splay from the tangent, veins
STYLES = {
    "heraldic": dict(n=4, leaf=29, splay=34, veins=True),
    "flat":     dict(n=4, leaf=30, splay=34, veins=False),
    "line":     dict(n=4, leaf=29, splay=34, veins="midrib"),
    "minimal":  dict(n=0, leaf=0,  splay=0,  veins=False),
}


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def petal(s=1.0):
    p = [(-7, -6), (-13.4, -11), (-11.2, -20), (0, -20), (11.2, -20), (13.4, -11), (7, -6)]
    p = [(x * s, y * s) for x, y in p]
    return (f"M{f(p[0][0])},{f(p[0][1])}C{f(p[1][0])},{f(p[1][1])} {f(p[2][0])},{f(p[2][1])} "
            f"{f(p[3][0])},{f(p[3][1])}C{f(p[4][0])},{f(p[4][1])} {f(p[5][0])},{f(p[5][1])} "
            f"{f(p[6][0])},{f(p[6][1])}Z")


BARB = "M0,-24.6L3.8,-18.6L0,-15.8L-3.8,-18.6Z"


def leaf_path(L):
    return f"M0,0C{f(L*0.255)},{f(-L*0.255)} {f(L*0.725)},{f(-L*0.255)} {L},0C{f(L*0.725)},{f(L*0.255)} {f(L*0.255)},{f(L*0.255)} 0,0Z"


def rose(style, r=ROSE_R):
    """Heraldic rose: five petals, barbed and seeded."""
    s = r / 20.0
    g = [f'<g transform="scale({f(s)})">']
    if style != "minimal":
        for i in range(5):
            g.append(f'<path d="{BARB}" transform="rotate({i * 72 + 36})"/>')
    for i in range(5):
        g.append(f'<path d="{petal()}" transform="rotate({i * 72})"/>')
    if style != "minimal":
        for i in range(5):
            g.append(f'<path d="{petal(0.54)}" transform="rotate({i * 72 + 36})"/>')
    g.append('<circle r="5.4" fill="none"/>' if style == "line"
             else f'<circle r="5.4" fill="{SEED}"/>')
    if style == "heraldic":
        g.append(f'<circle r="0.75" fill="{INK}" stroke="none"/>')
        for i in range(5):
            a = math.radians(i * 72 - 90)
            g.append(f'<circle cx="{f(2.9*math.cos(a))}" cy="{f(2.9*math.sin(a))}" '
                     f'r="0.75" fill="{INK}" stroke="none"/>')
    g.append("</g>")
    return "".join(g)


def wreath(style):
    cfg = STYLES[style]
    parts, angles = [], [-90 + i * 72 for i in range(5)]

    if style == "minimal":
        parts.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" '
                     f'stroke="currentColor" stroke-width="10"/>')
    else:
        L, step = cfg["leaf"], 72 / (cfg["n"] + 1)
        veins = ""
        if cfg["veins"] == "midrib":
            veins = f'<path d="M{f(L*0.1)},0H{f(L*0.9)}" fill="none" stroke-width="0.9"/>'
        elif cfg["veins"]:
            veins = (f'<path d="M{f(L*0.1)},0H{f(L*0.9)}" fill="none" stroke-width="0.8"/>'
                     '<path fill="none" stroke-width="0.6" d="'
                     + "".join(f"M{f(L*x)},{f(L*0.01)} {f(L*(x+0.09))},{f(-L*0.125)}"
                               for x in (0.26, 0.45, 0.64))
                     + "".join(f"M{f(L*x)},{f(L*0.015)} {f(L*(x+0.09))},{f(L*0.13)}"
                               for x in (0.32, 0.51, 0.70))
                     + '"/>')
        for a in angles:
            for k in range(1, cfg["n"] + 1):
                la = a + k * step
                lr = math.radians(la)
                px, py = CX + R * math.cos(lr), CY + R * math.sin(lr)
                t = (f"translate({f(px)},{f(py)}) rotate({f(la + 90 - cfg['splay'])}) "
                     f"translate({f(-L * 0.42)},0)")
                parts.append(f'<g transform="{t}"><path d="{leaf_path(L)}"/>{veins}</g>')

    for a in angles:
        ar = math.radians(a)
        px, py = CX + R * math.cos(ar), CY + R * math.sin(ar)
        parts.append(f'<g transform="translate({f(px)},{f(py)}) rotate({f(a + 90)})">'
                     + rose(style) + "</g>")
    return "\n    ".join(parts)


TITLE = ("Arms of the Wrede family: per pale gules and or, "
         "a wreath set with five roses counterchanged")


def build(name, style, field, w=W, h=H, cx=None, outline="", dx_stroke=None,
          sn_stroke=None, sw=0):
    """field: path defining the shape of the field (shield or roundel).
    dx/sn_stroke: outline colour for the gold copy and the red copy."""
    p, cx = name[:-4], cx if cx is not None else w / 2

    def use(fill, color, clip, stroke):
        s = (f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
             f' stroke-linecap="round"' if sw and stroke else "")
        return f'<use href="#{p}-wreath" fill="{fill}" color="{color}" clip-path="url(#{p}-{clip})"{s}/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="{p}-t">
  <title id="{p}-t">{TITLE}</title>
  <defs>
    <clipPath id="{p}-field"><path d="{field}"/></clipPath>
    <clipPath id="{p}-dx"><rect x="0" y="0" width="{f(cx)}" height="{h}"/></clipPath>
    <clipPath id="{p}-sn"><rect x="{f(cx)}" y="0" width="{f(w - cx)}" height="{h}"/></clipPath>
    <g id="{p}-wreath">
    {wreath(style)}
    </g>
  </defs>

  <g clip-path="url(#{p}-field)">
    <rect x="0" y="0" width="{f(cx)}" height="{h}" fill="{GULES}"/>
    <rect x="{f(cx)}" y="0" width="{f(w - cx)}" height="{h}" fill="{OR}"/>
    {use(OR, OR, "dx", dx_stroke)}
    {use(GULES, GULES, "sn", sn_stroke)}
  </g>
{outline}</svg>
'''
    open(os.path.join(OUT, name), "w").write(svg)
    print(f"  {name:26s} {len(svg):6d} B")


SH_OUT = f'  <path d="{SHIELD}" fill="none" stroke="{INK}" stroke-width="3.4"/>\n'
ROUNDEL = f"M{CX-97} {CY}a97 97 0 1 0 194 0a97 97 0 1 0-194 0Z"

# 1. heraldic - closest to the source drawing
build("arms-heraldic.svg", "heraldic", SHIELD, outline=SH_OUT,
      dx_stroke=INK, sn_stroke=INK, sw=1.2)

# 2. flat - the opposite tincture outlines each shape, so overlaps stay legible
build("arms-flat.svg", "flat", SHIELD,
      dx_stroke=GULES, sn_stroke=OR, sw=1.3)

# 3. minimal - survives down to favicon size
build("arms-minimal.svg", "minimal", SHIELD,
      dx_stroke=GULES, sn_stroke=OR, sw=2.4)

# 4. roundel - the same wreath in a circle, for avatars and stamps
build("arms-roundel.svg", "heraldic", ROUNDEL, w=200, h=228, cx=100,
      outline=f'  <circle cx="{CX}" cy="{CY}" r="95" fill="none" stroke="{INK}" stroke-width="4"/>\n',
      dx_stroke=INK, sn_stroke=INK, sw=1.2)


# 5. line - one colour, inherits currentColor, prints at any size
def build_line():
    p = "arms-line"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="{p}-t" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round" color="{INK}">
  <title id="{p}-t">{TITLE}</title>
  <path d="{SHIELD}" stroke-width="3.4"/>
  <path d="M100 12V227" stroke-width="2.2"/>
  <g>
    {wreath("line")}
  </g>
</svg>
'''
    open(os.path.join(OUT, p + ".svg"), "w").write(svg)
    print(f"  {p + '.svg':26s} {len(svg):6d} B")


build_line()
print("done")
