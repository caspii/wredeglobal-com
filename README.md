# wredeglobal.com

The website for **wredeglobal.com**. Plain static HTML, no build step, deployed
to GitHub Pages by GitHub Actions on every push to `main`.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page — markup, styles and copy in one file. |
| `404.html` | Shown for unknown URLs. |
| `CNAME` | Tells GitHub Pages the custom domain. Do not delete. |
| `assets/arms/` | The coat of arms, in six versions. See its own README. |
| `robots.txt`, `sitemap.xml` | For search engines. |
| `.nojekyll` | Stops GitHub from running Jekyll over the files. |
| `.github/workflows/deploy.yml` | The deploy job. |

## Editing the page

Open `index.html`. The text to change sits between the
`<!-- ==== EDIT THE COPY BELOW ==== -->` comments. The title and description
are marked the same way near the top. Colours are the five `--` variables at
the top of the `<style>` block, with dark-mode versions below them.

## Previewing locally

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying

Push to `main`. The workflow publishes within about a minute. Watch it under
the repository's **Actions** tab.
