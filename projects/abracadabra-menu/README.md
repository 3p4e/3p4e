# ABRACADABRA — Digital menu board (2 screens)

A browser-based menu that runs non-stop on two TVs in front of the store. Each TV opens the
same page with a different `screen` parameter:

| TV | Address | Shows |
|---|---|---|
| Left  | `index.html?screen=1` | Бургери, Сендвичи, Тостови (+ Поховано, Веге when they have prices) |
| Right | `index.html?screen=2` | Врапови, Скара, Салати, Десерти, Додатоци, Кафе, Пијалоци |
| Editor | `admin.html` | Change prices, items, promos, ticker text |

## Cinematic look (game main-menu style)
The board is built like the main menu of a AAA game, not like a flat slideshow. The menu text and prices
stay live HTML, so they are always editable. Everything around them is 3D, cinematic motion made with Higgsfield:

| Layer | Clip / effect | What it does |
|---|---|---|
| 3D environment | `bg_day.mp4`, `bg_night.mp4` (still fallback: `stage_day.jpg`, `stage_night.jpg`) | An arcane magician's stage that is also a burger kitchen. By day: velvet curtains, god rays, smoke, floating crystal shards, a glowing magic circle on a mirror floor. By night: the same stage in magenta and violet neon. A slow camera drift and seamless looping make it feel alive. |
| Mascot portal | `wand_idle_day.mp4`, `wand_idle_night.mp4` | **Абра, the living magic wand**, floats inside a portal with two rotating rune rings. By day he adjusts his monocle and welcomes guests; by night he rocks out and draws neon spirals. |
| Spell reveals | `wand_burger.mp4`, `wand_wrap.mp4`, `wand_waffle.mp4` | For each featured item, the wand casts a spell and the food materializes in a flash of light. Pick the clip per promo in admin.html. |
| Wand-slash transition | `fx_slash.mp4` | Every ~40 seconds a blazing wand slash crosses the whole board and explodes into crystal shards, and the featured item changes. The two screens are offset so they never fire together. |

**Effects in the page itself:**
- **Typography:** an extruded 3D gold wordmark with a light sweep, and prices rendered as glowing gold numerals.
- **Panels:** gold-framed "inventory" panels with jewel icons, tilted in 3D perspective.
- **Particles:** glowing embers and tumbling crystal shards at three depths.
- **Atmosphere:** light rays, vignette, film grain and cinematic letterbox bars.
- **Signature items:** a pulsing glow on "ХИТ" items.

All clips are H.264 without sound (about 20 MB total), which TV boxes play natively. If a clip is missing,
the board falls back to the still images.

## Mascot: Абра, the living magic wand
The wand is the one object everybody connects with "Abracadabra", and the brand's vintage wand sign already
uses it. As a character it becomes **ownable**: no food chain has a wand mascot. Research on long-running ad
campaigns (System1 / IPA "Fluent Devices") shows that a recurring, distinctive brand character makes advertising much more effective.

- **Personality:** smart and witty. He wears a monocle, raises a confident eyebrow and has white magician's gloves.
  He does not just stand there; he *makes* the food appear.
- **Brand look:** a black lacquered body with gold rune bands, and a crystal tip glowing in the logo's red and
  orange, surrounded by the logo's triangle confetti. At night the crystal turns neon magenta, matching the neon sign.
- **Earlier concept:** an earlier version used Абра the fox. It was replaced by the wand on request; old menu
  files that still name `fox_*` clips automatically play the wand clips.

Sources: [System1 — The Seven Habits of Highly Effective Characters](https://system1group.com/blog/the-seven-habits-of-highly-effective-characters),
[WARC — Identifying and measuring the Fluent Device](https://www.warc.com/en/article/identifying-and-measuring-the-fluent-device-96789122d7c54358bf1129c0c32d85ec),
[Campaign — mascot study](https://campaignlive.com/article/starbucks-triumphs-mr-mucus-gets-battering-mascot-study/1593815),
[Quirk's — most memorable brand mascots](https://www.quirks.com/articles/mascot-matchup-the-most-memorable-brands).

## Features
- **Brand look:** a cinematic 3D stage, the logo's colours (red, orange, lime, yellow), triangle crystal
  shards, and the animated **Абра** wand with a rotating promo panel.
- **Day/night switching:** automatic. From 19:00 to 06:00 the screens use the magenta neon look of the
  night sign and the neon wand. Test it with `&mode=night` or `&mode=day`.
- **Hidden items:** an empty price hides the item. A category with no prices disappears automatically.
- **Auto-fit:** the layout fits itself. Text sizes adjust so everything fits on one line, the columns
  balance, and any leftover space shows a rotating-coin logo brand card.
- **Panel and ticker:** the two TVs show different promos at the same time, and a ticker runs along the bottom.
- **Built for 24/7 running:** the picture shifts a few pixels every 3 minutes (burn-in protection), and
  the page reloads periodically when hosted.
- **Offline:** works with no internet. Fonts and images are included, so you can run it from a USB stick.

## Changing prices — three ways
1. **On the TV box:** open `admin.html`, edit, then press **Зачувај**. This saves on that device only.
2. **Permanent change for both TVs:** in `admin.html`, press **⬇ menu-data.js** and replace the file
   (on the USB stick or the web host).
3. **From a phone (recommended):** press **⬇ CSV** and open the file in Google Sheets. Then use
   *File → Share → Publish to web → CSV*, and paste the link into **Поставки → Google Sheet CSV**.
   The TVs re-read the sheet every few minutes, so a price changed on your phone appears by itself.
   Columns: `category, name, price, available, badge`.

## Recommended hardware & setup (research summary)
- **Screen brightness is the deciding factor.** The screens sit in front of the store, behind or near
  glass. A normal home TV (about 350 nits) washes out in daylight. Window-facing signage typically needs
  about 2,000–3,000 nits; fully outdoor screens need 3,000–4,000 nits, and should be weather-rated and
  readable with polarized sunglasses. Commercial panels also handle the heat behind glass, which kills
  consumer TVs.
- **Screen size and orientation:** two 55" commercial displays in landscape, 1920×1080 (4K also works;
  the page scales). A rule of thumb is about 4–6 ft of viewing distance per 10" of screen; for queues of
  3–6 m, go with 50–65".
- **Player:** a cheap Android TV box or stick per screen, running a kiosk browser such as
  **Fully Kiosk Browser**. Set it to auto-start, go fullscreen, never sleep and reload on errors, with
  the start URL `…/index.html?screen=1` (or `screen=2`). Most commercial "smart signage" displays have a
  built-in browser that can open the page directly.
- **Design rules applied:**
  - **Legibility:** large, high-contrast sans-serif text on a dark background, with content inside a
    safe margin from the screen edges.
  - **Density:** few items per section, with unavailable items hidden instead of shown as blank boxes.
  - **Prices:** the currency appears once per category rather than after every price.
  - **Signature items:** marked with a "ХИТ" badge and rotated in the large promo panel.
  - **Attention:** the promo sits in the top-right "golden triangle" area where eyes land first.
- **Next upgrade:** real photos of your own food in the promo panel. Photos sell better than text, but
  use real photos, not AI images of the food.

Sources:
- [Kitcast — common digital menu board mistakes](https://kitcast.tv/blog/common-digital-menu-board-mistakes)
- [Delphi Display — Best Practices: Digital Menu Boards (PDF)](https://www.delphidisplay.com/downloads/Delphi-Best%20Practices-Digital-Menu-Boards-2021.pdf)
- [LOOK Digital Signage — digital menu board size](https://www.lookdigitalsignage.com/blog/digital-menu-board-size)
- [Seen Labs — legibility & contrast for QSR signage](https://seenlabs.com/blog/digital-menu-legibility-typography-contrast-standards-for-qsr-signage)
- [CrownTV — high-brightness displays](https://www.crowntv-us.com/blog/high-brightness-outdoor-tvs-for-digital-signage-displays/)
- [CrownTV — window displays](https://crowntv-us.com/solutions/use-cases/window-displays/)
- [Samsung Insights — outdoor displays](https://insights.samsung.com/2019/09/12/fighting-the-bright-outdoor-displays-propel-businesses-forward)
- [AOL — the psychological trick fast-food menu boards use](https://www.aol.com/articles/psychological-trick-fast-food-menu-150947682.html)
- [Capterra — Fully Kiosk](https://www.capterra.com/p/156468/Fully/)

## Files
```
index.html        the player (both screens)
admin.html        the editor
menu-data.js      menu content (prices, items, promos, settings)
assets/logo.png   clean redraw of the logo emblem
assets/mascot_day.png / mascot_night.png   Абра the wand, still images (fallback)
assets/stage_day.jpg / stage_night.jpg     3D stage stills (fallback for the background video)
assets/video/     Higgsfield clips: 3D stage loops, wand idles and spell reveals, wand-slash transition
assets/fonts/     Russo One + Rubik (Cyrillic), bundled for offline use
```
