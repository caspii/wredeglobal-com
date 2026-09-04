# wredeglobal.com

The website for **wredeglobal.com**. Plain static HTML, no build step, deployed
to GitHub Pages by GitHub Actions on every push to `main`.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page — markup, styles and copy in one file. |
| `404.html` | Shown for unknown URLs. |
| `assets/arms/` | The coat of arms, in six versions. See its own README. |
| `favicon.ico` | 16–64px, for browsers that ignore the SVG. |
| `favicon.svg` | The scalable tab icon. |
| `apple-touch-icon.png` | 180px, for iOS home screens. |
| `icon-192.png`, `icon-512.png` | For `site.webmanifest`. |
| `site.webmanifest` | Name, colours and icons, for installed web apps. |
| `CNAME` | Tells GitHub Pages the custom domain. Do not delete. |
| `robots.txt`, `sitemap.xml` | For search engines. |
| `.nojekyll` | Stops GitHub from running Jekyll over the files. |
| `.github/workflows/deploy.yml` | The deploy job. |

## Editing the page

Open `index.html`. The text to change sits between the
`<!-- ==== EDIT THE COPY BELOW ==== -->` comments. The title and description
are marked the same way near the top. Colours are the six `--` variables at
the top of the `<style>` block, with dark-mode versions below them.

To change the mark at the top of the page, point `img.mark` at a different
file in `assets/arms/`.

## Regenerating the icons

The icons are rendered from `assets/arms/arms-favicon.svg` (transparent
shield) and `assets/arms/arms-icon.svg` (solid tile). Rebuild them with:

```sh
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 tools/build-icons.py
```

That needs `pip install cairosvg` and `brew install cairo`.

## Previewing locally

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying

Push to `main`. The workflow publishes within about a minute. Watch it under
the repository's **Actions** tab.
