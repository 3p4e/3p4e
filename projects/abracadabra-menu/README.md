# ABRACADABRA — Digital menu board (2 screens)

A browser-based menu that runs non-stop on two TVs in front of the store. Each TV opens the
same page with a different `screen` parameter:

| TV | Address | Shows |
|---|---|---|
| Left  | `index.html?screen=1` | Бургери, Сендвичи, Тостови (+ Поховано, Веге when they have prices) |
| Right | `index.html?screen=2` | Врапови, Скара, Салати, Десерти, Додатоци, Кафе, Пијалоци |
| Editor | `admin.html` | Change prices, items, promos, ticker text |

## Features
- **Brand look:** dark background, the logo's colours (red, orange, lime, yellow), triangle-confetti
  motif, and the animated **Абра** mascot with a rotating promo panel.
- **Day/night switching:** automatic. From 19:00 to 06:00 the screens use the magenta neon look of the
  night sign and the night mascot. Test it with `&mode=night` or `&mode=day`.
- **Hidden items:** an empty price hides the item. A category with no prices disappears automatically.
- **Auto-fit:** the layout fits itself. Text sizes adjust so everything fits on one line, the columns
  balance, and any leftover space shows a spinning-logo brand card.
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
assets/mascot_day.png / mascot_night.png   the Абра mascot (day and neon-night versions)
assets/fonts/     Russo One + Rubik (Cyrillic), bundled for offline use
```
