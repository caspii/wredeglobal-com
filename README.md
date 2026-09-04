# wredeglobal.com

The website for **wredeglobal.com**. Plain static HTML, no build step, deployed
to GitHub Pages by GitHub Actions on every push to `main`.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page — markup, styles and copy in one file. |
| `wrede-gathering-2028.ics` | The calendar file behind "Add it to your calendar". |
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
| `.conductor/settings.toml` | The Conductor **Run** button — a local preview server. |

## Editing the page

Open `index.html`. The text to change sits between the
`<!-- ==== EDIT THE COPY BELOW ==== -->` comments. The title and description
are marked the same way near the top. Colours are the seven `--` variables at
the top of the `<style>` block, with dark-mode versions below them.

The masthead (`header.mast`) is the gathering announcement, and it is sized to
fit on one phone screen without scrolling. If you add a line to it, check that
it still does — see "Above the fold" below. Four sections follow: the weekend,
the family, where we are, and the arms. The nav links point at their `id`s, so
renaming a section means updating both.

There is deliberately no email address on the page — see the note below.

Overall text size is the one `html { font-size: 112.5% }` rule at the top of
the `<style>` block. Every other size is in `rem`, so that single percentage
scales the whole page. Use a percentage, not a pixel value, so a reader's own
browser font-size setting still counts.

### The 2028 gathering

The dates live in three places and must agree:

1. The copy in `header.mast` and in `<section id="gathering">`.
2. The `Event` JSON-LD block near the bottom of `index.html` — this is what
   Google reads.
3. `wrede-gathering-2028.ics`. Note that `DTEND` is *exclusive*, so a
   15–17 September event ends `20280918`. Keep the CRLF line endings.

The "N days from today" line is drawn by the small script at the bottom of
`index.html`, from the date `Date.UTC(2028, 8, 15)`. Month 8 is September —
JavaScript counts months from zero.

There is no "tell us you are coming" link, because there is no mailbox behind
it yet. When one exists, put it back as a second `<a class="cta">` in
`<p class="actions">`, next to the calendar download.

### Above the fold

The whole masthead is meant to be visible on a phone without scrolling: the
mark, the family line, the headline, the dates, the countdown, the calendar
button and the nav. At 18px text on a 390×730 screen that leaves very little
slack, so anything added there pushes the button off-screen.

To check, serve the site and open a page holding it in a fixed-size frame:

```html
<iframe src="http://localhost:8000/" style="width:390px;height:730px"></iframe>
```

If it no longer fits, the cheapest things to give up are, in order: the
one-line description under the dates, the nav, and `.mark`'s height.

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

In Conductor, press **Run** instead. `.conductor/settings.toml` starts the same
server on the workspace's own port, so several workspaces can preview at once.

## Deploying

Push to `main`. The workflow publishes within about a minute. Watch it under
the repository's **Actions** tab.
