# BIG DOGMA social video kit

Public-safe launch kit for Instagram, Facebook, TikTok, YouTube and LinkedIn. Every video is built only from the studio's own demo material (generic LTX clips and the public-safe sector and timelapse films). Every video carries an AI disclosure that is on screen from the first frame: the reels and both showreels open with the disclosure pill (reel_06 with the line on its title card), and the two `post_hello_intro` videos in `launch/static/` show their AI line from frame 0.

> **Contact details.** The contact line comes from `brand/brand.json` (`phone`, `email`, `web`), and only the fields that are filled in are shown. At the moment only the email is set (phone and website are empty), so the showreel end cards (both formats), `post_offer.png` and `post_hello.png` show the email alone. Reels 01-06 and the `post_process` carousel carry no contact details. If `brand.json` ever holds placeholder values again (an `example.*` domain or `XXX` digits), the rebuild adds `_PLACEHOLDER-CONTACT` to the names of the affected files (showreels, post_offer, post_hello), so they cannot be posted by mistake.

## Files

| File | Duration | Format | Loudness (I / true peak) | Size |
|---|---|---|---|---|
| `bigdogma_showreel_16x9.mp4` | 55.71 s | 1920x1080, 24 fps | -14.1 LUFS / -2.1 dBTP | 57.3 MB |
| `bigdogma_showreel_9x16.mp4` | 55.71 s | 1080x1920, 24 fps | -14.1 LUFS / -2.1 dBTP | 45.4 MB |
| `reel_01_construction.mp4` | 41.90 s | 1080x1920, 24 fps | -14.4 LUFS / -1.5 dBTP | 18.6 MB |
| `reel_02_real_estate.mp4` | 35.87 s | 1080x1920, 24 fps | -14.1 LUFS / -1.5 dBTP | 16.3 MB |
| `reel_03_food.mp4` | 31.18 s | 1080x1920, 24 fps | -14.2 LUFS / -1.4 dBTP | 12.7 MB |
| `reel_04_automotive.mp4` | 31.18 s | 1080x1920, 24 fps | -14.2 LUFS / -1.7 dBTP | 13.9 MB |
| `reel_05_interior_design.mp4` | 24.76 s | 1080x1920, 24 fps | -14.1 LUFS / -1.7 dBTP | 7.6 MB |
| `reel_06_howto_construction.mp4` | 16.17 s | 1080x1920, 24 fps | -14.6 LUFS / -1.0 dBTP | 7.9 MB |
| `post_offer.png` | – | 1080x1350 PNG (offer card) | – | – |
| `post_process_1.png` | – | 1080x1350 PNG (carousel 1/3) | – | – |
| `post_process_2.png` | – | 1080x1350 PNG (carousel 2/3) | – | – |
| `post_process_3.png` | – | 1080x1350 PNG (carousel 3/3) | – | – |
| `post_hello.png` | – | 1080x1350 PNG (brand intro) | – | – |

All videos: H.264 High, yuv420p, 24 fps, AAC 192 kbps / 48 kHz, `+faststart`. Loudness is normalised to -14 LUFS integrated, with true peak at or below -1.0 dBTP (EBU R128, measured on the final AAC files with ffmpeg `ebur128`; `_work/qc_table.txt`). The showreels measure -14.1 LUFS and the reels -14.1 to -14.6 LUFS.

### 1. Studio showreel (`bigdogma_showreel_16x9.mp4`, `bigdogma_showreel_9x16.mp4`)

- **Cut:** 55.7 s, cut on the bar grid of `music/ace_final/8_showreel.mp3`, starting on its first big hit at 4.10 s (about 115 bpm, one bar = 2.09 s). Cuts land every 1, 2, 3 or 4 beats (0.52 to 2.09 s). Both formats have the same edit.
- **9:16 reframe:** per shot, not a letterbox. Close-ups (the opening steel pour, the chef, the wine pour, the welder, the vase product shot) and the one-beat closing montage use a full-height 396x704 crop scaled to 1080x1920. All other shots, the wide and detailed ones, use a 560x704 (4:5) crop scaled to a 1080x1358 band in the middle of the frame, over a blurred, darkened cover of the same shot. This is the same look as the 9:16 film masters, and the upscale is 1.93x instead of 2.73x.
- **Hook (0-4 s):** molten steel and sparks under "ОВА НЕ Е СНИМЕНО." This is on screen from the first frame. Then 4 one-beat cuts under "ОВА Е AI.". The standard disclosure pill ("Видео изработено со вештачка интелигенција" / "AI-GENERATED VIDEO", Oswald on a dark translucent pill with a thin gold outline, the same design as the reels) is on screen from frame 0 to 4.15 s and fades out over the last 0.4 s, just before the first sector cut. In 9:16 it is the reels' overlay (`png/disc_top_9x16.png`, y ≈ 498-612, above the hook text). In 16:9 it is centred under the hook line (`png/disc_top_16x9.png`, pill y ≈ 700-810, clear of the player controls).
- **Sector captions** (Russo One, gold "AI ВИДЕО ЗА" kicker plus a sector name with a growing gold bar): ГРАДЕЖНИШТВО, НЕДВИЖНОСТИ, ВНАТРЕШЕН ДИЗАЈН, ХРАНА, ВИНО, ЧЕЛИК И ЦЕМЕНТ, ЕНЕРГЕТИКА, ЛАНСИРАЊЕ НА ПРОИЗВОДИ (one line in 16:9, two lines in 9:16), ИНДУСТРИЈА. The musical break carries "БЕЗ КАМЕРА. / БЕЗ ЕКИПА. / БЕЗ ЧЕКАЊЕ.", and the final 8-shot one-beat montage carries "ВАШАТА ПРИКАЗНА Е СЛЕДНА."
- **ЕНЕРГЕТИКА** is one 4-beat shot of the finished roof (`tl2_solar_2` from 4.0 s). `tl2_solar_1` and the first 4 s of `tl2_solar_2` were dropped because they show morphing workers and half-formed panels.
- **ГРАДЕЖНИШТВО** opens on the concrete pour (`tl_02_pour` 0.1-1.14 s, 2 beats), then the frame time-lapse (`tl_03_frame`, 4 beats at 2.5x) and the handover. `tl_01_dig` was dropped: its excavator and dump trucks melt and fuse (at 0.3 s, 1.0-1.4 s, 2.7-3.2 s and 4.0-4.4 s), and `tl_02_pour` is only used before its pump boom folds into a tangle (1.4 s).
- **НЕДВИЖНОСТИ** lobby (`x_re_x1`) uses only 0-0.83 s of the clip, played at 0.8x over 2 beats (a near-static moment). From 0.85 s a dark sleeve reaches through the glass door with no body attached. The rooftop (`x_re_x2`) takes the third beat.
- **Close:** at 45.9 s, on a music hit, the animated BIG DOGMA logo ignites (4.2 s, rendered with `fx/dogma_logo.js`). It is the horizontal lockup in 16:9 and a stacked one in 9:16 (mark above the wordmark, centred, wordmark within x ≈ 260-880). It cross-fades into the end card at 50.1 s: logo, "AI видео за вашиот бизнис", gold pill "Пилот-филм од €600", the contact from `brand.json` (currently the email), and "Видео изработено со вештачка интелигенција · AI-generated video". In 9:16 the end-card lockup is 740 px wide (x 170-910), clear of the right-hand action rail. The music ends at 54.7 s and the card fades out at 55.7 s.
- **Watermark:** a gold BD monogram, top-left, at 85 % opacity during the footage.
- **Shots used (39 cuts, all generic, no client material):** `ltx25/` br_c08_s2, br_c12_s1, tl_02_pour, tl_03_frame, tl_06_handover (x2), br_c09_s3to4, br_c10_s2to3, st_03_styled, br_c06_s2, br_c07_s1, br_c07_s2, br_c08_s3, br_c12_s2, br_c04_s4, br_c03_s2to3, br_c11_s1, br_c05_s2. Also `ltx610/` x_con_x2, tl2_garden_2, x_re_x2 (x2), x_re_x1, x_int_x2, x_food_x2, x_food_x1, x_wine_x1, x_steel_x1, x_steel_x2, tl2_solar_2, tl2_road_2, x_prod_x1, x_prod_x2, x_auto_x1, x_pharma_x1, x_rec_x2, tl2_expo_2, tl2_store_2, x_apt_x2.
- **Music:** `music/ace_final/8_showreel.mp3` (4.10 s to 58.8 s).

### 2. Reels (`reel_01` to `reel_06`, 1080x1920)

| Reel | Source | Notes |
|---|---|---|
| reel_01_construction | `final_music_9x16/timelapse_construction_9x16.mp4` + `subs/srt/timelapse_construction.mk.srt` | film body (opening 0-4.67 s rebuilt from two clean frames, see below) + native end card "Градба / Од празен плац до вашите клучеви." |
| reel_02_real_estate | `final_music_9x16/sector_real_estate_9x16.mp4` + `.mk.srt` | film body + native end card "Недвижности / Живот над градот." |
| reel_03_food | `final_music_9x16/sector_food_9x16.mp4` + `.mk.srt` | film body + native end card "Прехранбена индустрија / Вкусот што го знаете." |
| reel_04_automotive | `final_music_9x16/sector_automotive_9x16.mp4` + `.mk.srt` + `ltx610/x_auto_x2.mp4` | film body (hall shot 4.3-10.2 s replaced, see below) + native end card "Автомобилска индустрија / Направено во Македонија, возено низ Европа." (generic wire-harness plant, no brand) |
| reel_05_interior_design | `final_music_9x16/timelapse_interior_design_9x16.mp4` + `.mk.srt` | film body + native end card "Внатрешен дизајн / Простор што личи на вас." |
| reel_06_howto_construction | rebuilt natively in 9:16 from the same sources as `explainers/howto_construction.mp4` | see below |

- **Reel 05** used to be `timelapse_renovation`. It was replaced because its VO did not match the picture: "Бања во која сакате да влезете." started over the derelict "before" bathtub, and "Кујна каква што секогаш сте сакале." played over a kitchen that still looked dated. In `timelapse_interior_design` each line lands on its shot: bare walls, then plans on the floor, then the furnished loft.
- **Reel 01 opening (0-4.67 s):** in the film's first seconds the excavator melts into a yellow blob (0.3 s), dump trucks fuse into a crushed heap (1.3 s) and an excavator and truck melt again mid-frame (4.0-4.4 s). `reels.py` (`picture()`) replaces master frames 0-111 with two clean frames of the same master: frame 0 (the bare plot with the parked excavator and trucks, under the VO line "Секој дом почнува од гола земја.", 0.3-3.4 s) and frame 112 (the dug pit with its rebar grid), joined by a 0.5 s dissolve at 3.42-3.92 s. One continuous, eased pull-back (picture band zoom 1.08 to 1.00, 4x supersampled) runs across both and lands exactly on frame 112, where the time-lapse starts playing, so the join is seamless. The blurred top and bottom bands, the audio, the subtitles and every later frame are the master's own. Small vehicles at the back of the pit still pop in and out after 4.7 s, as in any time-lapse, but nothing large melts mid-frame.
- **Reel 04 hall shot (4.3-10.2 s):** the master's wire-harness hall (4.7-9.8 s) is staffed by visibly East Asian workers in a Chinese-style hall, under "Линија што никогаш не застанува." and before "Направено во Македонија". `reels.py` replaces master frames 113-234 with `ltx610/x_auto_x2.mp4` (an inspector in a hi-vis vest checking wire harnesses on racks in a bright European-style plant), laid out like the master (1080x608 band at y 656 over a blurred cover). It dissolves in from the exterior (9 frames, 4.33-4.67 s) and out into the crimping close-up (9.79-10.17 s). The clip has 121 frames for 140 output frames: its slow first 3 s (she reads her tablet) are stretched with frame blending and the rest plays at 1x, so the faster part (she reaches for the harness, the camera pans) has no ghosting. Audio, subtitles and the rest of the film are unchanged.
- **End card (reels 01-05):** the 9:16 masters end in a 16:9 DejaVu card whose blurred copy fills the top band. `reels.py` cuts each master just before its dissolve into that card (found automatically from the picture band) and dissolves into a native 1080x1920 card (`_work/png/reelend_<topic>_A/B/C.png`) for the same length, over the film's own audio. The card is set in Russo One and Oswald on the brand background with the gold monogram, and shows the sector title, the tagline, "Готов филм за 7–10 дена по одобрување на клучните кадри.", the pill "Пилот-филм од €600", the demo note "Демо концепт на студиото. Сцените се генерирани и не прикажуваат вистински објект." and "Видео изработено со вештачка интелигенција / AI-generated video". Measured on the rendered layers, all of it sits within x 213-868 and y 421-1377 with the gold monogram at the top included (the text block alone starts at y 570): clear of the action rail and above y 1436.
- **AI disclosure:** every reel shows it from the first frame. Reels 01-05 have a pill in the top blurred band (y ≈ 498-612 including its shadow, above the picture band, x ≈ 185-895) with "Видео изработено со вештачка интелигенција" (Oswald 33 px, white) and "AI-GENERATED VIDEO" (gold), for the first 3.8 s. Reel 06 has it on its title card, from frame 0: two lines ("Видео изработено со вештачка интелигенција", then "AI-generated video" in gold, Oswald 31 px) at y ≈ 1310-1386, the same height as on the outro and above TikTok's caption zone (from about y 1436). The top-band pill is not used in reel_06 because its step kickers and step texts sit in the top band from 2.0 s. All six repeat it on the end card (reels 01-05) and on the outro (all reels).
- **Subtitles:** Macedonian, burned in with libass, Russo One 54 px, white with a dark outline and shadow. They are top-anchored at y = 1282, right under the picture band (y 656-1264) of the 9:16 masters, so a two-line subtitle ends near y 1420, above TikTok's bottom ad zone (from about y 1436). Text is centred in the column x = 170 to 910, clear of the right 160 px of Reels buttons. Measured text boxes across all 25 subtitle events of reels 01-05 (`_work/subcheck.py`, last run ALL_OK; reel 06 uses the same style) fall within y 1287-1389 and x 167-912. The check compares each reel with its clean master below the picture band and counts only white pixels that changed (the text fill), grown by 4 px for the outline, so it stays valid where reel_01 and reel_04 carry replaced pictures. Timing comes straight from the SRT files. Meta recommends keeping the bottom 35 % (below y ≈ 1250) free of text. Nothing in this layout can meet that without covering the picture, so the subtitles sit as high as possible without overlapping it.
- **Watermark:** the gold monogram (`brand/mark_bold.svg`, 110 px wide, 85 % opacity) at top-left (x 34, y 196), below the Reels header.
- **Outro (2.8 s):** a vertical render of the animated BIG DOGMA logo in a stacked layout: mark above wordmark, centred, with the wordmark within x ≈ 260-880, so nothing runs into the action rail and the ignition is centred. It carries the AI disclosure at y ≈ 1320 and a 2.85 s sting taken from `8_showreel.mp3` at 50.04 s. This is the same hit the showreel logo lands on, so it works as a sonic logo across the kit.
- **reel_06 how-to:** the 13.4 s 16:9 explainer rebuilt as a native vertical (16.2 s). It opens straight on the title card, with no fade from black, so the platform's default cover is the title: "Како настанува рекламата", "ГРАДЕЖНИШТВО · ТАЈМЛАПС" and the AI disclosure, over a blurred `tl_06_handover`. Step 1 shows `construction/kf/con_01_excavation_start.png` ("Ваш рендер или фотографија од плацот"). Step 2 shows `ltx25/tl_03_frame.mp4` ("AI тајмлапс по фази"). Step 3 shows the finished ad: `timelapse_construction_9x16.mp4` from 28.70 s, the finished building, with its closing VO line "Од празен плац до вашите клучеви." kept whole and subtitled ("Готова реклама: глас, музика, 16:9 и 9:16"). The "КОРАК 1/2/3" kickers are 44 px gold Oswald on an opaque dark box. The music is `3_construction.mp3`, then the film audio, then the sting.

### 3. Post images (1080x1350, PNG)

| File | Content |
|---|---|
| post_offer.png | "AI видео за вашиот бизнис" with the subline "Готов филм за 7–10 дена по одобрување на клучните кадри." and 3 tiers: Пилот од €600 (1 film 20-30 s, 16:9 + 9:16), Лансирање од €1.800 (gold badge "ПРЕПОРАЧАН", the same label the site uses; main film 45-60 s + 3 spots + 10 short clips), Месечна содржина од €400/месец (6-8 clips a month, 3-month minimum). Footnote: 1 round of revisions, prices in euros without VAT, every video labelled as made with AI. Footer: contact from `brand.json` and "Пишете ни →". Tier wording matches the pitch pages. |
| post_process_1.png | Carousel 1/3 "Клучен кадар": first frame of `ltx25/br_c09_s1to2.mp4`, the staked-out empty plot (the keyframe of the developer demo) |
| post_process_2.png | Carousel 2/3 "AI анимација" ("кран, скеле, кат по кат, фаза по фаза"): frame at 3.0 s of `ltx25/br_c09_s1to2.mp4`, the structure in scaffolding. Checked at full resolution, with no visible morphing in the frame. |
| post_process_3.png | Carousel 3/3 "Готова реклама": frame at 16.3 s of `final_music/timelapse_developer.mp4` (the finished, landscaped building), plus the same moment from the 9:16 master. CTA "Пилот-филм од €600". |
| post_hello.png | Brand intro: glowing gold monogram, "Здраво, ние сме BIG DOGMA", "Правиме AI видео реклами за бизниси — готов филм за 7–10 дена по одобрување на клучните кадри.", the sector line and the contact from `brand.json`. |

The turnaround claim is the same everywhere: "готов филм за 7–10 дена по одобрување на клучните кадри". The carousel tells one project from plot to finished building, using the developer demo (a generic low-rise suburb). The construction demo was set in a visibly Japanese suburb. The carousel slides each carry "Демо на студиото · визуелите се генерирани со вештачка интелигенција". The posts are rendered from HTML with Playwright, using Russo One for headlines and Oswald for body text (both embedded as data URIs).

## Rebuild

All sources are in `_work/`. Work from `launch/video/_work`, using `/usr/local/bin/python3` for the video scripts and `/usr/bin/python3` for `static_html.py` and `subcheck.py`.

1. **Stills:** after any change to `brand/brand.json`, run `python3 static_html.py && node shoot.js jobs.json`. `contact.py` reads the contact fields. This renders the end cards (showreel and reels), the disclosure overlays, the posts, the watermark and the title card to `_work/png/`.
2. Copy the posts: `cp png/post_*.png ..`
3. **Showreel:** `python3 showreel.py all`. This needs `seg/logo_16x9.mp4` (layout `lockup`) and `seg/logo_9x16.mp4` (layout `stack`), which `logo_pipe.js` renders: `node logo_pipe.js <S> 1.5 6.0 24 stack 1080 1920 | ffmpeg -f image2pipe -framerate 24 -c:v png -i - -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p seg/logo_9x16.mp4`.
4. **Reels:** `python3 reels.py all` (or `01` to `06`).
5. **QC:** `python3 qc.py` reports durations, streams and loudness. `/usr/bin/python3 subcheck.py` checks the subtitle boxes against the safe zone (y 1264-1436, x 160-920).

`logo_pipe.js` loads `_work/dogma_logo_kit.js`. This is a copy of `fx/dogma_logo.js` with a smaller letter-spacing sweep on the wordmark reveal and an extra `stack` layout (mark centred above the wordmark) for vertical formats. The web original is unchanged.

## Not included, on purpose

The kit leaves out:

- Client concept films and clips.
- `studio_showreel_ltx.mp4`.
- Anything from `pitch/` or `pitch_9x16/`.
- The other explainers.

The source films were checked frame by frame for visible real brands, and none were found.

## Known limits

- The construction demo (`timelapse_construction`, `tl_0x` clips, `con_0x` keyframes) is set in a visibly Japanese suburb, with tile-roofed detached houses and a "mansion" apartment block. It still appears in reel_01, in reel_06 (steps 1-3) and in the showreel's ГРАДЕЖНИШТВО beat (`tl_02_pour`, `tl_03_frame`, `tl_06_handover`). Fixing that needs regenerated keyframes and clips with Balkan surroundings. The carousel has already been moved to the developer demo.
- reel_05, about 6.3-7.7 s: during the film's furnishing dissolve the sofa and the clothes rack show as semi-transparent double exposures. This is accepted as time-lapse style and left as is.
- `launch/static/social_copy.md` follows the swap: reel_05 is captioned, titled and scheduled as the interior design time-lapse, and the copy names the exact kit file for every post.
