# Abracadabra TV Menu System — Operational Runbooks

Grounded in [the actual repo](/a0/usr/projects/vast/projects/abracadabra-menu/) and [INFRASTRUCTURE.md](/a0/usr/projects/vast/setup/INFRASTRUCTURE.md). Every command below was read from the repo, not invented.

---

## ⚠️ Read-from-the-box rule (applies to ALL runbooks)

The KVM4 public domain is masked in this environment as `srv1231216.hstgr.cloud`. **Do not guess it.** Throughout these runbooks the domain is written as `<KVM4_DOMAIN>`.

To obtain the real value **on the box**, read it from the running Traefik/compose config — it is the `Host()` label in the stack's `docker-compose.yml`. Example (this is the actual label from the repo's `deploy/docker-compose.yml`):

```yaml
traefik.http.routers.abracadabra-menu.rule=Host(`abracadabra.<KVM4_DOMAIN>`)
```

Get it without guessing:

```bash
# on KVM4
cd /opt/stacks/abracadabra-menu
cat docker-compose.yml | grep -E 'Host\('      # or: docker compose config
# or from the running container's live Traefik labels:
docker inspect abracadabra-menu --format '{{ index .Config.Labels "traefik.http.routers.abracadabra-menu.rule" }}'
```

The boarded URLs then follow this exact pattern (from the repo's README):

| Target | Short URL | Full URL |
|---|---|---|
| Screen 1 (left)  | `https://abracadabra.<KVM4_DOMAIN>/1` | `https://abracadabra.<KVM4_DOMAIN>/cinematic-board.html?screen=1` |
| Screen 2 (right) | `https://abracadabra.<KVM4_DOMAIN>/2` | `https://abracadabra.<KVM4_DOMAIN>/cinematic-board.html?screen=2` |
| Editor | `https://abracadabra.<KVM4_DOMAIN>/admin` | `https://abracadabra.<KVM4_DOMAIN>/admin.html` |

The `nginx.conf` short-addresses are real and in the repo (`deploy/nginx.conf`): `/`, `/1` → screen 1; `/2` → screen 2; `/admin` → admin.html.

**Where the hosted site lives on KVM4** (from README + INFRASTRUCTURE.md):

- `abracadabra-menu` stack: `/opt/stacks/abracadabra-menu/` (an `nginx:alpine` container named `abracadabra-menu`); site files in `site/`, config in `nginx.conf`; compose project name `abracadabra-menu`.
- NOTE — there is a **second, newer** deployment documented in INFRASTRUCTURE.md: the **ABRA stack** at `/opt/stacks/abra` (compose project `abra`) that serves the *patched board + the 87 LTX-2.5 clips* at `https://abra.<KVM4_DOMAIN>`. The old `abracadabra-menu` stack was left untouched. **Before editing live, check which stack the TVs actually point at by reading the Traefik `Host()` labels for both projects** — do not assume.

---

# Runbook 1 — Offline USB build

## 1.1 What the app is

A fully static site. There is no build step — the HTML/JS/CSS are served as-is. The two TV launcher files are one-line redirect pages (verified in `usb/`):

- `usb/TV1.html` → `<meta http-equiv=refresh content="0;url=cinematic-board.html?screen=1">`
- `usb/TV2.html` → `<meta http-equiv=refresh content="0;url=cinematic-board.html?screen=2">`

## 1.2 What a self-contained USB package must contain

From the repo's own `build-usb.sh`, a complete package is the folder `ABRACADABRA_MENU/` containing:

| Item | Why |
|---|---|
| `cinematic-board.html` | the board the TVs actually run |
| `index.html` | alternative "classic" look (optional but bundled) |
| `admin.html` | the price editor |
| `menu-data.js` | **the whole menu** (data source of truth for offline mode) |
| `assets/clip-map-ltx25.js` | **LTX-2.5 clip map** — maps names → `assets/video/ltx25/*` paths. REQUIRED or the spawn clips won't resolve |
| `assets/fonts/` | Russo One + Rubik (Cyrillic), must stay together |
| `assets/*.png`, `assets/*.jpg` | mascot/stage stills + logo (fallbacks) |
| `assets/video/ltx25/` | the LTX-2.5 clip set: **both `*.mp4` and `*.webm`** (87 mp4 + 87 webm = 174 files in the repo) |
| `TV1.html`, `TV2.html`, `TV1_classic.html`, `TV2_classic.html` | one-file launchers |
| `УПАТСТВО_INSTRUCTIONS.html`, `ПРОЧИТАЈ_README.txt` | bundled user guide |
| `preview/` | static preview PNGs (optional, cosmetic) |

**mp4 + webm rule (from the code in `cinematic-board.html`):** at load the board probes H.264 support and remembers WebM fallback per session:

```js
let MP4_OK = !!document.createElement("video").canPlayType('video/mp4; codecs="avc1.42E01E"');
// ...and a failed MP4 `error` event flips MP4_OK=false, sets sessionStorage "abra_webm",
//    and swaps .mp4 -> .webm on the fly.
```

So **ship both `.mp4` and `.webm` for every clip** — TVs without H.264 (many Android TV boxes / old smart-TV browsers) fall back to WebM/VP9 automatically. Missing the WebM twin = black video on those TVs.

## 1.3 Build the package

The repo ships a build script (`build-usb.sh`). Copy-pasteable:

```bash
cd /a0/usr/projects/vast/projects/abracadabra-menu
sh build-usb.sh
# -> writes dist/ABRACADABRA_MENU_USB.zip
```

⚠️ **Caveat (verified):** `build-usb.sh` copies `assets/` wholesale with `cp -r`, so **in this repo it WILL include `assets/clip-map-ltx25.js` and `assets/video/ltx25/`** — but the **existing committed `dist/ABRACADABRA_MENU_USB.zip` is stale** (see 1.6). Always rebuild; do not trust the old zip.

If you need a manual build without the script (script requires `zip`):

```bash
cd /a0/usr/projects/vast/projects/abracadabra-menu
STAGE=$(mktemp -d)/ABRACADABRA_MENU && mkdir -p "$STAGE"
cp -r assets cinematic-board.html index.html admin.html menu-data.js "$STAGE/"
cp usb/TV1.html usb/TV2.html usb/TV1_classic.html usb/TV2_classic.html "$STAGE/"
cp "usb/УПАТСТВО_INSTRUCTIONS.html" "usb/ПРОЧИТАЈ_README.txt" "$STAGE/"
# then copy the whole ABRACADABRA_MENU folder to the stick
```

## 1.4 Launch it on a TV (kiosk recipe)

The repo's own bundled guide gives this Chrome kiosk command (Windows example, USB drive `E:`):

```
chrome --kiosk --autoplay-policy=no-user-gesture-required --allow-file-access-from-files file:///E:/ABRACADABRA_MENU/TV1.html
```

For TV 2, swap the file:

```
chrome --kiosk --autoplay-policy=no-user-gesture-required --allow-file-access-from-files file:///E:/ABRACADABRA_MENU/TV2.html
```

Linux / Android TV box / mini-PC equivalent (same flags, adjust the `file://` path to where the stick mounts):

```
chromium --kiosk --app=file:///mnt/usb/ABRACADABRA_MENU/TV1.html \
  --autoplay-policy=no-user-gesture-required \
  --allow-file-access-from-files
```

**Flag meanings (what they fix, from the repo guide):**
- `--kiosk` — fullscreen, no chrome UI, no exit UX.
- `--autoplay-policy=no-user-gesture-required` — lets the background/cinematic clips autoplay without a tap.
- `--allow-file-access-from-files` — lets the page load sibling files (menu-data.js, fonts, videos) from the filesystem.
- Note: some kiosk browsers (Fully Kiosk Browser, commercial signage browsers) have their own "autostart / reload on error / no sleep" toggles — use those instead of raw Chrome flags when they exist. The repo README recommends **Fully Kiosk Browser** and a start URL of `…/cinematic-board.html?screen=1` (or `2`).

**Recommendation:** on a `file://` stick, prefer an Android TV box/mini-PC with Chrome/Chromium; many Smart-TV built-in browsers block local-file video autoplay (the repo guide says this explicitly).

## 1.5 Verify locally before shipping

Serve it over HTTP locally — closer to the hosted behavior than `file://` and avoids file-access restrictions:

```bash
cd /a0/usr/projects/vast/projects/abracadabra-menu
python3 -m http.server 8000
# screen 1: http://localhost:8000/cinematic-board.html?screen=1
# screen 2: http://localhost:8000/cinematic-board.html?screen=2
# editor:   http://localhost:8000/admin.html
```

Checks to perform:
1. Both screens render categories (screen 1 ≠ screen 2 — the board filters by a `screen` field).
2. Clips play: open DevTools → Network → filter `media`; confirm `ltx25/*` requests return 200 for both `.mp4` and (on H.264-less browsers) `.webm`.
3. Wrap the folder back into a zip and confirm `assets/clip-map-ltx25.js` and `assets/video/ltx25/` are present (the two things the stale committed zip is missing).

## 1.6 Inspect the existing `dist/ABRACADABRA_MENU_USB.zip`

Verified contents (via `python3 -c "import zipfile; ..."` because `unzip` is not installed on this box):

**It DOES contain:** `TV1.html`, `TV2.html`, `TV1_classic.html`, `TV2_classic.html`, `admin.html`, `index.html`, `cinematic-board.html`, `menu-data.js`, `assets/fonts/*`, `assets/{logo,mascot_day,mascot_night}.png`, `assets/{stage_day,stage_night}.jpg`, `assets/video/` **root-level clips only** (bg_day, bg_night, wand_*, cine_*, fx_slash — mp4 + webm), `preview/*`, `УПАТСТВО_INSTRUCTIONS.html`, `ПРОЧИТАЈ_README.txt`.

**It DOES NOT contain:** `assets/clip-map-ltx25.js`, `assets/clip-map.js`, `assets/css/skin.css`, and the entire `assets/video/ltx25/` tree (the 174-file LTX-2.5 set).

**Conclusion:** the committed zip is a **pre-LTX-2.5 snapshot** (built Nov 18 17:39, 97 MB; the current `assets/video/` alone is 381 MB with LTX-2.5). Its embedded `cinematic-board.html` references only `menu-data.js` and does **not** load `clip-map-ltx25.js`, so it renders the base menu without the per-item spawn-clip layer. **Do not burn this zip to a stick for production** — rebuild with `sh build-usb.sh` first.

## 1.7 Update the USB later

1. Rebuild the zip (`sh build-usb.sh`) or re-stage the folder as in 1.3.
2. Only the changed files must be re-copied onto the stick — but because navigation is by sibling file / folder names, **keep the folder structure intact** and never rename `assets/`, `assets/fonts/`, or `assets/video/ltx25/`.
3. `menu-data.js` is the most common change; copy the new `menu-data.js` over the old one (the bundled guide: press "⬇ menu-data.js" in `admin.html`, then replace on the stick).
4. On the TV, hard-refresh (`Ctrl+F5`) or reboot the kiosk browser.

---

# Runbook 2 — Item and price changes

There are **three real paths**. Only path 1 is global; paths 2 and 3 per-device / via sheet.

## Path 1 — Edit `menu-data.js` and redeploy (the only global offline change)

`menu-data.js` is a plain file defining `window.MENU_DATA`. Data shape (verified):

```js
window.MENU_DATA = {
  currency: "ден",
  sheetCsvUrl: "",        // optional, see Path 3
  refreshMinutes: 5,
  nightFrom: 19, nightTo: 6,
  cinematicMinutes: 2,
  promos: [ { title, subtitle, price, video } ],
  categories: [
    { id: "burgeri", screen: 1, name: "Бургери", note: "+ помфрит", color: "red",
      items: [ { name: "Хамбургер", price: 170 }, { name: "Веге бургер", price: null, badge: "ВЕГЕ" } ] }
  ]
};
```

Rules (from the file's own comments):
- `price: null` → item is **not shown**.
- `available: false` → temporarily hidden ("out of stock today").
- `badge`: `"ХИТ" | "НОВО" | "ВЕГЕ" | ""`.
- `screen`: `1` = left TV, `2` = right TV (this is what splits the menu across TVs).
- `promos[].video`: `wand_burger | wand_waffle | wand_wrap` (or empty).

Steps:
1. Edit `menu-data.js` in the repo.
2. Push to the host. Static files live in `site/` on KVM4:
   - `abracadabra-menu` stack → `/opt/stacks/abracadabra-menu/site/menu-data.js`
   - (verify which stack is live first, see the read-from-box rule)
3. **No container restart is needed** — `nginx.conf` serves `*.js` with `Cache-Control: no-cache`, and the board hard-reloads every 30 minutes when hosted (`setInterval(() => navigator.onLine && location.reload(), 30*60000)` in `cinematic-board.html`). So the change reaches the TVs within ≤30 min automatically.

Tradeoffs: global, permanent, needs host access; no phone-editing UX.

**Upload methods on KVM4** (from INFRASTRUCTURE.md — read the live token, don't trust a stored copy):
- `kvm4-runner`: `POST /file/write {path, content_b64}` (overwrite only) — endpoint + bearer token in the runner compose env.
- or `scp` the file into `site/`.

## Path 2 — `admin.html` localStorage override (PER-DEVICE ONLY)

Open `admin.html`, edit, press **Зачувај (Save)**. The editor stores a full JSON copy of the menu under the localStorage key **`abra_menu_override`**.

The board reads it like this (verified, `cinematic-board.html`):

```js
try { const o = localStorage.getItem("abra_menu_override"); if (o) DATA = JSON.parse(o); } catch (e) {}
```

**Explicitly: this is per-device.** It changes the menu on the one browser/TV-box where you clicked Save — it does NOT propagate to the other TV or the hosted site. The editor's own header note and the bundled guide both say this. Use it for:

- testing a change without touching the repo;
- a one-off override on a single TV.

To make it global this way is the wrong tool. The editor's **⬇ menu-data.js** button downloads the current (overridden) menu as `menu-data.js` — combine that with Path 1 to promote a tested override to global.

Reset: **Врати оригинал** removes the localStorage key and reverts to `menu-data.js`.

## Path 3 — Google Sheet CSV import (per-menu-field, refreshed automatically)

The board supports reading prices/items from a Google Sheet published as CSV. The wiring is a single field in `menu-data.js`:

```js
sheetCsvUrl: ""   // <- the key
```

The **exact key is `sheetCsvUrl`** (confirmed in `menu-data.js`, the `applySheet`/`loadSheet` logic, and the `admin.html` settings field). It is NOT a URL query param on the board — it lives in the menu data (and can be set per-device via admin.html → **Поставки → Google Sheet CSV линк**).

CSV columns (exact order, from `applySheet`):

```
category | name | price | available | badge
```

Behavior (verified):
- The board fetches `sheetCsvUrl + (& or ?) + "t="+Date.now()` (cache-bust), parses with its own CSV parser, and `applySheet` **rebuilds all categories' items from the sheet** onto the in-file `window.MENU_DATA` as a template.
- Category matching: by `id` first, then by name (case-insensitive); unknown categories are created on the fly with `screen` = current screen.
- `available` values `no / не / false / 0 / x` → hidden; anything else → shown.
- Refresh cadence: `setInterval(loadSheet, (DATA.refreshMinutes || 5) * 60000)` — **every 5 minutes by default** (`refreshMinutes`).

Setup steps (copy-pasteable):
1. In `admin.html` click **⬇ CSV** to get `abracadabra-meni.csv` with the correct header.
2. Import that CSV into Google Sheets → **File → Share → Publish to web → CSV**, copy the publish URL.
3. Paste the URL into `menu-data.js` under `sheetCsvUrl` (Path 1) **or** into admin.html Поставки (per-device).
4. Edit the sheet from your phone; TVs re-read it every `refreshMinutes` automatically.

Tradeoffs: global + phone-editable + zero host access, but requires an internet reachable sheet + the sheet's structure; it **replaces** the in-file item lists while active (the in-file `menu-data.js` items are the template only).

## Adding a NEW item that needs a NEW spawn clip

When the new item needs its own hover/tap "spawn" animation, three coordinated edits are required, because the spawn layer is a **separate static map** (`assets/clip-map-ltx25.js`), not generated from `menu-data.js`.

**1. Add the item in `menu-data.js`** (as in Path 1):
```js
{ name: "Нов артикл", price: 250, badge: "НОВО" }
```
Inside the right category (so the `screen` and `id` are inherited).

**2. Add the clip files** under `assets/video/ltx25/`, BOTH codecs:

`spawn_small_<category_id>_<slug>.mp4` and `spawn_small_<category_id>_<slug>.webm`

Real naming examples from the repo's 64 spawn_small entries:

| Item (MK) | category_id | file |
|---|---|---|
| Абракадабра бургер | burgeri | `spawn_small_burgeri_abracadabra-burger.{mp4,webm}` |
| Хамбургер со јајце | burgeri | `spawn_small_burgeri_hamburger-egg.{mp4,webm}` |
| Вафла со нутела и банани | deserti | `spawn_small_deserti_waffle-nutella-banana.{mp4,webm}` |
| Дрпано јунешко | vrapovi | `spawn_small_vrapovi_wrap-beef.{mp4,webm}` |

Convention: `spawn_small_` + category **id** (`burgeri`, not `Бургери`) + `_` + Latin-transliterated slug with hyphens for spaces (Cyrillic is not used in filenames).

**3. Add the map entry in `assets/clip-map-ltx25.js`**, keyed `category_id::ItemName` with the **exact same item name as in `menu-data.js`** (the board looks items up by `data-key="<category.id>::<item.name>"`, verified in the render code):

```js
items: {
  "<catId>::<Exact Item Name>": {
    "clip": "assets/video/ltx25/spawn_small_<catId>_<slug>",  // NO .mp4 here — the board appends .mp4/.webm
    "price": 250,
    "effect": "Your Effect Name",
    "theme": "forge_fire",
    "screen": 1
  }
}
```

⚠️ **Generator correction (important, verified):** the board loads `assets/clip-map-ltx25.js`, whose header says `/* AUTO-GENERATED from Claude LTX-2.5 package — do not edit */`. **`gen_clipmap.js` does NOT generate it.** `gen_clipmap.js` reads `clip_specification.json` and rewrites the **legacy** `assets/clip-map.js` (old `wand_*` names + `assets/video/<day_clip>` paths) — a file the current board no longer loads. There is **no in-repo script that regenerates `clip-map-ltx25.js`**, and the only in-repo record of the spawn mapping is `clip-map-ltx25.js` itself. So a new spawn clip is added **manually** to `clip-map-ltx25.js` (plus placing the mp4+webm files), not by running a generator. If a generator for the LTX-2.5 map exists, it is part of the external LTX-2.5 package, not this repo.

---

# Runbook 3 — New TV onboarding

## 3.1 Physical / power / browser setup

1. Mount/locate the screen (16:9, 1920×1080 native; the page scales from a 1920×1080 stage).
2. Choose the player: the repo recommends **Fully Kiosk Browser** on a cheap Android TV box/stick per screen, or Chromium/Chrome in kiosk mode on a mini-PC.
3. Browser must autostart, fullscreen, never sleep, and reload on error. Set the **start URL** per screen.

## 3.2 Which URL for screen 1 vs screen 2

| Screen | Start URL |
|---|---|
| **1 (left)**  | `https://abracadabra.<KVM4_DOMAIN>/1`  — or `.../cinematic-board.html?screen=1` |
| **2 (right)** | `https://abracadabra.<KVM4_DOMAIN>/2`  — or `.../cinematic-board.html?screen=2` |

(Offline/USB: point the kiosk at `file:///.../TV1.html` vs `TV2.html`, which simply redirect to the `?screen=` URLs.)

The `screen` value is set from the query string in the board (`const SCREEN = q.get("screen") === "2" ? 2 : 1;`) and drives everything.

## 3.3 Confirm the right screen is showing

The board **filters categories by a `screen` field** (`cinematic-board.html`):

```js
cats = DATA.categories.filter(c => (c.screen || 1) === SCREEN && c.items.some(shown));
```

Expected split (from `menu-data.js`):
- **Screen 1:** Бургери, Сендвичи, Тостови (+ Поховано, Веге when they have prices).
- **Screen 2:** Врапови, Скара, Салати, Десерти, Додатоци, Кафе, Пијалоци.

If a screen shows the wrong set, the `?screen=` param is wrong on that TV (or the WebView lost the query string — use the `/1` / `/2` short URLs, or the `TV1.html`/`TV2.html` launchers, which exist precisely to hardcode the redirect).

## 3.4 What to check when clips do not play

1. **Codec fallback (the big one):** the board starts with `MP4_OK` from `canPlayType('video/mp4; codecs="avc1.42E01E"')`, and on the first `.mp4` `error` event it sets `sessionStorage["abra_webm"]="1"` and swaps `.mp4 → .webm` for every clip thereafter. So if MP4 won't decode on a TV, it must have the `.webm` twins present (Runbook 1.2). **Symptom: no/brief black video** → verify the `.webm` files are on the stick (`assets/video/ltx25/*.webm`) or served by the host.
2. **Autoplay blocked:** the `<video>` elements are `muted playsinline`; if a browser still requires a gesture, the kiosk must run with `--autoplay-policy=no-user-gesture-required` (Runbook 1.4).
3. **Local file access blocked (USB):** needs `--allow-file-access-from-files`, otherwise `menu-data.js`/fonts/videos won't load.
4. **Files missing on a stale stick:** check `assets/clip-map-ltx25.js` and `assets/video/ltx25/` exist — the committed zip is missing them (Runbook 1.6).

## 3.5 Troubleshooting table

| Symptom | Cause | Fix |
|---|---|---|
| Wrong categories on a TV | `?screen=` param wrong/missing | Use `/1` vs `/2`, or launch `TV1.html`/`TV2.html` |
| Clips won't play / black video | H.264 unsupported or `.webm` twin missing | Ship `.webm`; confirm `ltx25/*.webm` present; enable `--autoplay-policy=no-user-gesture-required` |
| Blank screen on USB | Browser blocks local file access/autoplay | Run Chromium kiosk with `--allow-file-access-from-files` (Runbook 1.4); prefer Android TV box over Smart-TV browser |
| Old prices still showing (hosted) | ≤30-min auto-reload not elapsed, or file not replaced | Hard refresh; confirm `menu-data.js` replaced in `site/`; `*.js` is served `no-cache` but the page reloads on its own every 30 min |
| Old prices still showing (USB) | `menu-data.js` not re-copied | Replace `menu-data.js` on the stick; `Ctrl+F5` |
| Sheet changes not appearing | `sheetCsvUrl` empty / not a published-CSV URL / not yet `refreshMinutes` | Publish sheet as CSV, paste the `.../pub?output=csv` URL, wait ≤5 min |
| Odd/garbled text | `assets/fonts` missing or renamed | Keep `assets/fonts/` intact; don't rename the folder |
| Cinematic fires too often/never | `cinematicMinutes` setting | URL `&cine=N` minutes (0 = off), or admin.html Поставки |

---

## Quick reference — exact identifiers found in the code

| What | Value |
|---|---|
| localStorage override key | `abra_menu_override` |
| sessionStorage webm flag | `abra_webm` |
| Google Sheet field | `sheetCsvUrl` |
| CSV columns | `category, name, price, available, badge` |
| Clar map global | `window.CLIP_MAP_LTX25` → `.top` (background/mascot), `.items` (per-item spawn), `.full` (per-category full loop) |
| Item lookup key | `<category.id>::<item.name>` |
| Spawn file naming | `spawn_small_<category_id>_<slug>.mp4` / `.webm` |
| Screen filter | `(c.screen || 1) === SCREEN` |
| Hosted page auto-reload | every 30 min (`location.reload()` when `http`) |
| Sheet auto-reread | every `refreshMinutes` (default 5) min |
| Short URLs | `/1`, `/2`, `/admin` (nginx `location` redirects) |
