# Зелена Империја — Green Empire

A bilingual (Macedonian / English) cannabis-cultivation tycoon game that runs in
the browser: plant strains, water and feed them, harvest, dry, cure, breed
hybrids, fill orders, hire staff, and prestige.

The game itself is a single self-contained `index.html` (no build step, no
framework). `assets/art.js` adds generated artwork on top of it.

## Run

```bash
python3 -m http.server 8080     # then open http://localhost:8080/
```

## The plant art

The centrepiece is the cultivation view, where a plant **visibly grows from
seedling to harvest** instead of stepping through a drawing.

Four photographs of the *same* plant were generated from one shared reference
image, so the pot, framing, and lighting are identical across all of them:

| stage | what it shows |
|-------|---------------|
| `seedling` | a sprout in an otherwise empty pot |
| `veg` | a leafy vegetative plant, no buds |
| `flower` | early buds forming, light frosting |
| `harvest` | dense, frosty, harvest-ready |

At runtime `fotoRastenie()` picks the two stages nearest the plant's `napredok`
(0→1) and cross-fades between them, so growth is continuous rather than four
jumps. Plant health desaturates and darkens the image, and each strain tints the
scene with its own colour. If `assets/art.js` is missing the game falls back to
the original procedural SVG plant, so it still runs without any artwork.

Each of the 10 strains also has its own bud portrait (shown on plant cards), and
the cultivation tab has a grow-room hero banner.

## Regenerating the artwork

Raw generations live in `assets/raw/` and are **not** committed (they are tens of
megabytes); `assets/art.js` is the built bundle that ships, ~360 KB of compressed
JPEG data URIs.

```bash
node assets/black_bg.mjs    # re-render each stage on flat black (Venice API)
node assets/build_art.mjs   # composite + compress everything into assets/art.js
```

`black_bg.mjs` needs `VENICE_API_KEY`. `build_art.mjs` needs `playwright` (it
uses headless Chromium purely as an image encoder).

**Why flat black?** The stages have to sit in a grow room, which means removing
their studio backdrop. Alpha cut-outs baked a bright checkerboard into the
semi-transparent leaf edges, leaving a white halo that no amount of de-fringing
removed cleanly. Rendering the plants on pure black instead makes the background
add nothing under an additive composite, so it drops out perfectly while the
dark fabric pot keeps every pixel.
