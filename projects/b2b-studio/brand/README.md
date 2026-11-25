# Studio brand

- `mark.svg`: studio mark, traced from the close-up photo of the founder's hand-drawn triangle (play-button) tattoo (`source_tattoo_closeup.png`). Vector, single path, `currentColor` fill.
- `mark_bold.svg`: thicker strokes for small sizes (favicon, app icon, watermark).
- `logo.png`: 1600×400 lockup (gold BD mark + BIG DOGMA + AI STUDIO  |  Skopje), transparent background. Rendered by `render_logo.js` from `logo.html` and `brand.json`.
- `mark_gold.png`, `mark_white.png`, `mark_black.png`: 1024 px mark, transparent background.
- `icon_512.png`: app icon / favicon (bold mark on the studio background).
- Name, city, contacts and colours come from `brand.json`, the single source for every generator. Contact is email only: inf.unit@proton.me (phone, WhatsApp and web are empty and are left out everywhere until they exist).

## Name and type

- Name: **BIG DOGMA** (Latin) / **БИГ ДОГМА** (Cyrillic, if needed). Lockup: `BIG DOGMA` + `AI STUDIO  |  Skopje`.
- Monogram **BD**: the **D** is the original tattoo triangle (`mark_D_single.svg`, traced from `source_tattoo_closeup.png`); the **B** is two smaller, newly drawn triangles in the same hand-drawn style, stacked, each different (`gen_b_triangles.py`, option 1: seeds 11 and 23). Combined mark: `mark.svg` (single path), `mark_bold.svg` for small sizes.
- Typeface: **Russo One** (Google Fonts, SIL Open Font License), one weight, for the wordmark, video titles and PDF headings. File in `fonts/`.

## Animated logo (`../fx/dogma_logo.js`)

The monogram ignites stroke by stroke (red-hot -> white-hot -> gold), then glows like heated metal and cycles through three colours (gold -> arcane blue -> violet). Each colour change lands on a power burst: shockwave ring, light rays, spark shower and a glint across the wordmark. Embers drift throughout. 3.5 s ignition inside a 6 s intro file, then a seamless 12 s loop. The same code runs live on the pitch sites (preloader, nav mark) and renders the video exports via `fx/render_logo_anim.js` + `fx/export.sh`.

## Animated logo exports (S/brand/anim, backed up privately on KVM4 in /opt/bigdogma_backup/brand_anim)

| File | Format | Length |
|---|---|---|
| `dogma_logo_intro_1080p.mp4` | H.264 1920x1080, 30 fps | 6 s |
| `dogma_logo_loop_1080p.mp4` | H.264 1920x1080, 30 fps, seamless loop | 12 s |
| `dogma_logo_loop_36s_1080p.mp4` | H.264 1920x1080, three loops | 36 s |
| `dogma_logo_loop.gif` | 640x360, 15 fps, loops forever | 12 s |
| `dogma_logo_loop_alpha.mov` | ProRes 4444 with alpha (for editors) | 12 s |
| `dogma_logo_loop_alpha.webm` | VP9 with alpha (for the web) | 12 s |
| `dogma_mark_loop_1080x1080.mp4` | H.264 1080x1080, mark only | 12 s |

Re-export with `fx/export.sh` after any change to `fx/dogma_logo.js` or `brand.json`.
