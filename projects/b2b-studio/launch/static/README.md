# BIG DOGMA: static social kit

Profile pictures, platform covers, a 9:16 logo intro and launch copy for BIG DOGMA (AI STUDIO | Skopje).
Design: dark cinematic (#0d0d0f), gold BD monogram (#f2c14e, metallic gradient + soft glow), BIG DOGMA wordmark in Russo One, tagline "AI видео за вашиот бизнис", and a perspective strip of stills from the studio's own public-safe AI clips.

## Files to upload

| File | Pixels | Size | Use |
|---|---|---|---|
| `profile_1080.png` | 1080 x 1080 | 831 KB | Profile picture on dark (Instagram, Facebook, TikTok, YouTube, X, LinkedIn logo) |
| `profile_white_bg_1080.png` | 1080 x 1080 | 476 KB | Alternative profile picture on a light background (deep-gold monogram) |
| `linkedin_cover_1128x191.png` | 1128 x 191 | 264 KB | LinkedIn company page cover |
| `facebook_cover_1640x624.png` | 1640 x 624 | 1000 KB | Facebook page cover |
| `youtube_banner_2560x1440.png` | 2560 x 1440 | 2.7 MB | YouTube channel banner (under the 6 MB limit) |
| `x_header_1500x500.png` | 1500 x 500 | 768 KB | X (Twitter) header |
| `post_hello_intro_9x16.mp4` | 1080 x 1920 | 2.8 MB | post_hello video for Instagram/TikTok (30.11 in the calendar): 7 s BD monogram ignition, wordmark, tagline, burned-in "Видео изработено со вештачка интелигенција" (on screen from the first frame). H.264 + silent AAC track; add music in the app |
| `post_hello_intro_16x9.mp4` | 1920 x 1080 | 1.7 MB | post_hello video for LinkedIn/Facebook/X: 6 s horizontal lockup, the same animation as `brand/anim/dogma_logo_intro_1080p.mp4` but rendered with the video kit's renderer, whose smaller letter-spacing sweep keeps "BIG DOGMA" inside the frame (the brand file sweeps the final "A" off the right edge at about 2.3-2.7 s). Same burned-in AI line, on screen from the first frame. H.264 + silent AAC track |
| `social_copy.md` | - | 44 KB | Bios (IG, TikTok, FB, LinkedIn, YouTube, X), the exact kit file for each post, captions for the 10 launch posts (5 hashtags each), short X versions (280 or fewer) for the four X posts, YouTube titles, 2-week calendar, rules. Macedonian + English |

All PNGs are RGB, exact platform pixel sizes (checked with ffprobe and PIL). No contact details are baked into the images; the only contact (the email) is in the texts in `social_copy.md`.

## Safe zones (verified)

The logo + text block was measured in the browser and checked against each platform's crop:

| Asset | Logo + text box (x0, y0, x1, y1) | Rule | Result |
|---|---|---|---|
| Profile pictures | mark reaches 444 px from centre | must stay inside the circle crop (radius 540) | 82% of radius, ok |
| Facebook | 453, 192, 1187, 405 | inside the central 820 x 312 (also inside desktop 1640 x 462 and mobile ~1110 wide) | ok |
| YouTube | 770, 556, 1790, 849 | inside the centred 1546 x 423 text-and-logo area | ok |
| X | 417, 130, 1083, 326 | clear of the bottom-left avatar, inside the top/bottom trim band | ok |
| LinkedIn | 333, 19, 795, 149 | inside x 180-948: clear of the bottom-left company logo, centred for mobile side crop | ok |

LinkedIn lockup is 1.3x the first version (mark 80 px, name 50, tagline 31, subline 14) so the tagline still reads at phone width.

The still strips sit outside the key-content zones; they are decorative and may be cropped.

**AI disclosure on the covers.** Every cover, LinkedIn included, carries the note "AI-генерирани кадри", centred under the tagline inside the same safe area as the logo, at 80% opacity with a dark shadow. `render_static.js` records its box and `guides.py` checks it (cyan box on the `_preview` sheets):

| Asset | Note size | Note box (x0, y0, x1, y1) | Safe area checked | Approx. size on screen |
|---|---|---|---|---|
| Facebook | 24 px | 669, 428, 971, 452 | key content 410-1230 x 156-468, mobile 265-1375 | ~8 px on a 390 px phone |
| YouTube | 32 px | 1078, 874, 1482, 906 | 1546 x 423 safe area (507-2053 x 508-931) | ~8 px on a 390 px phone |
| X | 24 px | 599, 350, 901, 374 | 60-440 band, right of the avatar | ~10 px at 600 px desktop |
| LinkedIn | 13 px | 482, 160, 646, 173 | x 180-948 | 13 px on desktop, ~4.5 px on a phone |

The LinkedIn note (like the subline) is only readable on desktop; at 191 px height there is no room for a larger line. The posts themselves carry the AI line in every caption.

## Review sheets (not for upload)

`_preview/` holds the check sheets: `*_safezones.jpg` (crop lines and safe areas drawn over each cover) and `profile_*_circlecheck.jpg` (circle crop, 85% safe circle, previews at 320/180/110/40 px).

## Stills used (public-safe only)

Frames grabbed with ffmpeg from the studio's own generic raw LTX clips, no brands or logos visible:
`ltx610/x_con_x1` (construction, 2.5 s), `ltx610/x_steel_x1` (welding, 2.5 s), `ltx610/x_food_x2` (chef, 2.5 s, YouTube only), `ltx610/x_prod_x1` (bottle, 2.5 s), `ltx610/x_re_x2` (rooftop, 1.0 s), `ltx610/x_wine_x2` (vineyard, 2.5 s, YouTube only).
No client concept film, pitch material or studio_showreel_ltx frame is used.

## Re-render

```
cd launch/static/_work
node render_static.js <S>                 # all assets (or add names, e.g. facebook_cover_1640x624)
/usr/bin/python3 guides.py <S>            # rebuild the _preview check sheets, prints the safe-zone checks (all true)
bash intro916/build_intro.sh <S> [all|9x16|16x9]   # post_hello_intro_9x16.mp4 + _16x9.mp4 (~3 min, frames are piped, nothing large on disk)
```

`intro916/build_intro.sh` renders both intros with the video kit's logo renderer (`launch/video/_work/logo_pipe.js` + `dogma_logo_kit.js`), which pipes PNG frames straight into ffmpeg. 9:16: layout `mark` (identical to `fx/dogma_logo.js`), 1080 x 2640, t = 0-7 s, cropped to 1080 x 1920 with the mark at y = 610 (above the Reels/TikTok bottom UI), plus three PIL overlays (`make_overlays.py`): wordmark + subline (fade in 2.2-3.3 s, same timing as the animated lockup), rule + tagline (3.0-4.0 s) and the AI line (from the first frame, no fade-in, at y = 1330, inside the 9:16 safe area). 16:9: layout `lockup`, 1920 x 1080, t = 0-6 s, plus the AI line at y = 950 from the first frame. `tools/xcount.py` is the X character counter used for the counts in `social_copy.md` (X weighting: Cyrillic 1, URL 23).

`<S>` is the scratchpad root. `render_static.js` builds one HTML page per asset (`_work/html/`), renders it with Playwright/Chromium at 1x and writes the PNG plus `_work/boxes.json` (logo + text and AI-note bounding boxes used by the safe-zone check). Source stills are in `_work/src/` (lossless PNG). `_work/cand/` and `_work/stills/` are earlier frame candidates and are not used.

## Open points

- Contact is email-only: `inf.unit@proton.me`, taken from `brand/brand.json`; `social_copy.md` uses no other contact. Profile link fields stay empty until the studio has its own domain.
- The post images are in the video kit: `launch/video/post_offer.png` (price card), `launch/video/post_process_1.png` to `post_process_3.png` (3-slide carousel) and `launch/video/post_hello.png` (still alternative to the post_hello video). `social_copy.md` lists the exact file for every post and matches the text on these images.
- `post_hello_intro_9x16.mp4` and `_16x9.mp4` are code-rendered logo animations with no AI footage; they still carry the AI line because the kit rule is that every public video carries it (labelling more than needed does no harm).
- LinkedIn and X overlay positions (company logo, avatar) are approximations; check once after upload on desktop and mobile.
