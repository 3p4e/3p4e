# Studio brand

- `mark.svg`: studio mark, traced from the close-up photo of the founder's hand-drawn triangle (play-button) tattoo (`source_tattoo_closeup.png`). Vector, single path, `currentColor` fill.
- `mark_bold.svg`: thicker strokes for small sizes (favicon, app icon, watermark).
- `logo.png`: 1200×400 lockup (gold mark + name), transparent background. Rendered by `render_logo.js` from `logo.html` and `brand.json`.
- `mark_gold.png`, `mark_white.png`, `mark_black.png`: 1024 px mark, transparent background.
- `icon_512.png`: app icon / favicon (bold mark on the studio background).
- Name, city, contacts and colours come from `brand.json` (still placeholders: `placeholder: true`).

## Name and type

- Name: **BIG DOGMA** (Latin) / **БИГ ДОГМА** (Cyrillic, if needed). Lockup: `BIG DOGMA` + `AI STUDIO  |  Skopje`.
- Monogram **BD**: the **D** is the original tattoo triangle (`mark_D_single.svg`, traced from `source_tattoo_closeup.png`); the **B** is two smaller, newly drawn triangles in the same hand-drawn style, stacked, each different (`gen_b_triangles.py`, option 1: seeds 11 and 23). Combined mark: `mark.svg` (single path), `mark_bold.svg` for small sizes.
- Typeface: **Russo One** (Google Fonts, SIL Open Font License), one weight, for the wordmark, video titles and PDF headings. File in `fonts/`.

## Animated logo (`../fx/dogma_logo.js`)

The monogram ignites stroke by stroke (red-hot -> white-hot -> gold), then glows like heated metal and cycles through three colours (gold -> arcane blue -> violet). Each colour change lands on a power burst: shockwave ring, light rays, spark shower and a glint across the wordmark. Embers drift throughout. 3.5 s intro, then a seamless 12 s loop. The same code runs live on the pitch sites (preloader, nav mark) and renders the video exports via `fx/render_logo_anim.js` + `fx/export.sh`.
