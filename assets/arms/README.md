# Arms of Wrede

Six SVG versions of the Wrede family arms, drawn from scratch.

**Blazon:** *Per pale gules and or, a wreath set with five roses counterchanged.*

Source: [roskildehistorie.dk — Wrede (tysk)](https://www.roskildehistorie.dk/stamtavler/adel/svenske/Wrede/Wredetysk.htm),
which gives the German blazon —
"Das in Rot und Gold gespaltene Stammwappen zeigt einen Kranz mit fünf (1:2:2)
Rosen verwechselter Farbe." Motto on the same page: *Virtuti pro patria*.

These are original drawings following that blazon, not a trace of the page's
image. A coat of arms is defined by its written description, so any artist may
draw it; the specific picture on that site is somebody else's artwork and is
not reproduced here.

## The files

| File | Use |
| --- | --- |
| `arms-heraldic.svg` | Closest to the source drawing. Veined leaves, barbed and seeded roses. Best above about 80px. |
| `arms-flat.svg` | No dark outline; each shape is edged in the opposite tincture. Modern, flat. |
| `arms-line.svg` | One colour, `fill: none`, inherits `currentColor`. Letterheads and print. Paste it inline in your HTML and it takes the surrounding text colour; loaded through `<img>` it falls back to dark ink and will vanish on a dark background. |
| `arms-roundel.svg` | The same wreath in a circle. Avatars, stamps, social profiles. |
| `arms-minimal.svg` | Roses reduced to plain rosettes on a ring. Holds together down to ~28px. |
| `arms-favicon.svg` | Wreath reduced to a ring, roses dropped. The only version legible at 16px. |

Open `index.html` in a browser to see all six side by side, on light and dark,
and the favicon at real pixel sizes.

## Tinctures

| | Hex | Heraldic name |
| --- | --- | --- |
| Red | `#d9271b` | gules |
| Gold | `#f9c301` | or |
| Outline | `#3a1c10` | — |
| Rose centre | `#f6ecc9` | — |

The two colours were sampled from the source illustration. Swap them in
`generate.py` if you want the deeper, more traditional gules `#c8102e`.

## How the counterchange works

The wreath is drawn once into `<defs>` with **no `fill` attribute on any
shape**. It is then stamped twice with `<use>` — a gold copy clipped to the red
half, a red copy clipped to the gold half. Each copy's shapes inherit `fill`
from its `<use>`. That is why the line of the pale cuts straight through the
top rose instead of stopping at its edge, which is what the blazon asks for.

## Regenerating

```sh
python3 generate.py
```

Edit the constants at the top of `generate.py` to change the shield shape,
wreath radius, rose size, or how many leaves sit between the roses.
`arms-favicon.svg` is hand-written and is not touched by the script.
