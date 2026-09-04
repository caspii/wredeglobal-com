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

Every icon is rendered from one of the SVGs in `assets/arms/`:

```sh
python3 tools/build-icons.py                   # rebuild from the current source
python3 tools/build-icons.py --source roundel  # switch to a different version
python3 tools/build-icons.py --all             # also rebuild the candidate set
```

That needs `pip install cairosvg` and, on macOS, `brew install cairo`.

`--all` writes a favicon for every version into `assets/arms/favicons/`.
Open `assets/arms/favicons/index.html` to compare them at 16, 32 and 48px
before choosing. Only the reduced marks stay readable below 32px.

## Previewing locally

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying

Push to `main`. The workflow publishes within about a minute. Watch it under
the repository's **Actions** tab.
