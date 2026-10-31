# Karsus: costume research (2026-10-30)

## What I could and could not find
- **No canonical description of Karsus's clothing.** I searched and read the accessible pages (planewalker.com, bg3.wiki Crown of Karsus, the Obsidian "Wizard Karsus" page). None describes his dress. The only physical detail is about his remains: "his gigantic living heart beats ponderously within a butte of red stone." The Forgotten Realms wiki and WorldAnvil pages refused my requests (HTTP 402 and 403).
- **I could not view images.** My tools read text only, so I could not look at the artwork on those sites. Any "reference image" claim from me would be invented.
- **The nearest canon:** the *Robe of the Archmagi* ("fine garment, typically made from costly white, gray, or black cloth and marked with silvery magical runes; colour matched the wearer's alignment"). It is a magic item, not Netherese fashion, but it is the closest official image of "an archmage's robe". Source: Forgotten Realms Wiki, "Robe of the archmagi".
- **Other canon facts that can be shown:** Karsus built the floating city Eileanar at 22, the youngest ever to do so; he made the *Crown of Karsus*, which later held three Netherstones; his remains became the Karsestone.

## Design proposal (my invention, built on those facts)
1. **Colour:** the robe of the archmagi's canon palette, **deep indigo-black** (the "evil/neutral" archmage colours would suit a man who crosses a line) lined **ivory**, with **silver rune-embroidery**. Gold is kept for one item only (the crown), so the eye goes to it.
2. **Silhouette:** floor-length robe with a **very high standing collar** that frames the face, long hanging sleeves, a layered mantle on the shoulders. Vertical lines read as "tall, ancient, imperial", and a long robe also hides the body proportions that AI models drift on.
3. **Netherese identity:** geometric glyph borders (circles, straight lines, nested rings) matching the rings of his ritual. The same motifs appear on the cities' architecture, so he looks like a product of his empire.
4. **The crown:** a thin **silver circlet** with one large pale gem at the brow (an echo of the Netherstones). It lights up in Set Piece 3. It is the only head ornament; his hairless head carries the sigil.
5. **Hands:** many silver rings, one per finger. When the rings of glyphs ignite in the sky, the rings on his fingers ignite first.
6. **Arc through the film:** at the start he is immaculate. After the apotheosis his robe is partly **burnt back to the shoulders by the light**. In the epitaph the stone has taken the shape of the same robe.

## What I need from you
If you have a Karsus image you like (official art, a game, a painting), **send it**, and I will match it. Otherwise I take the proposal above into the KARSUS LOCK once you approve it.

## Costume tests with Gemini `gemini-3-pro-image` (2026-10-30, local files in `keyframes/karsus/`, git-ignored)
| File | What | Likeness (mean SFace) | Verdict |
|---|---|---|---|
| `k_gemini_BN_GEMINI_API.png` | first costume, large crown | 0.508 | crown too big, floated above the scalp; costume generic |
| `k_crown_small.png` | same, crown shrunk to a fitted circlet | 0.455 | crown right; likeness fell |
| `k_v2_A.png` | **Direction A, regal archmage-emperor**: indigo brocade, ivory-lined mantle, tall halo collar, one sculpted shoulder, spell-diagram on the chest, staff with an orbiting rune ring | 0.512 (nose-mouth +13.5 %) | grand, "ruler" reading |
| `k_v2_B.png` | **Direction B, battle-archmage**: plate-and-mail, violet tabard, a big spell circle on the chest, orbiting rune ring above the hand, floating city behind | **0.557** (all geometry within ±10 % except eye-nose −9 %) | stronger action pose, better likeness |

Runes are now one deliberate spell diagram (nested circles and straight lines) instead of text-like bands.

## DECISION 2026-10-31: Direction A (regal archmage-emperor) is the Karsus costume
The user chose the left image (A). Costume sheet generated with Gemini `gemini-3-pro-image`, face from `Blagoj-Base` views, costume from `k_v2_A.png`. Local files in `keyframes/karsus/` (git-ignored; upload to Higgsfield when the video step starts).

| File | View | Mean SFace vs 20 real photos |
|---|---|---|
| `A_front.png` | full-length front | 0.519 |
| `A_three_quarter.png` | full-length three-quarter | 0.572 |
| `A_back.png` | full-length back (spell diagram on the back, train of the mantle) | n/a (no face) |
| `A_bust.png` | close-up for face shots | **0.562** |
| `A_crown.png` | the crown alone | n/a |

Rejected: Direction B sheet (`sheet_*.png`): close-up 0.478 and front 0.498, below or at the limit. The three B close-up retries were interrupted by the user and never completed.

**KARSUS LOCK (final, replaces section 6 of the script):** `the man from the Blagoj-Base reference, unmistakably the same real person, same face, eyes, nose, mouth, jaw and age; hairless shaved head, clean-shaven, light grey-green eyes, real unretouched skin; Karsus, archwizard of Netheril: heavy indigo-to-midnight brocade robe woven with silver geometric patterns, a long open ceremonial over-mantle with an ivory-silk lining and train, a tall flared stiff collar standing high behind the head like a halo, fine silver mail at the forearms and a mail gorget, one asymmetric sculpted steel shoulder piece on the left shoulder with gold scale inlay and pale blue glowing gems, a wide jewelled belt, a ruby brooch clasping the mantle, silver rings on every finger, a glowing cyan spell diagram (nested concentric circles and straight lines) over the chest and down the robe, a small slim fitted crown of mottled silver-steel with two small hooked horns, a short central spike, gold scale inlay and two rubies, a tall silver staff topped by a large pale blue gem with a ring of tiny glowing runes orbiting its head`

## Seedance 2.5 draft test, ritual set piece (2026-10-31)
- Job `1917adc1-bc9e-4ae5-bd3f-f0c9cbff98a7`, `seedance_2_5`, `omni_reference`, 480p **draft**, 22 s, audio off, 3 references (costume bust, front, back). Cost **66 credits** (balance 347.19 to 281.19). Saved in project folder 03.
- Uploaded references (Higgsfield media_input IDs): front `3054d4c4-ba0e-477e-9dea-a629e1815ef2`, bust `1c05fc54-58fc-4be1-966f-78b6733ad9de`, back `0da7fa2a-4ad4-4473-947d-163fb21820db`.
- Higgsfield again offered the preset "IN THE DARK"; declined with `declined_preset_id` 24bae836-2c4a-48e0-89b6-49fcc0b21612.
- Result: scene detection found **no cuts** (one true continuous take). Floating cities, expanding cyan glyph rings, lightning, vortex all present.
- Gaps: the face was never visible (small, from behind), so likeness in video is untested; the "lights of distant cities dim and stream towards him" beat did not read; the camera pull-back loses the wizard from about 16 s (he becomes a speck).

## Seedance 2.5 draft 2, ritual set piece: front-facing, more explicit magic (2026-10-31)
- Job `e4e7bcaf-e14f-46b9-9685-28515bf6806a`, same settings as draft 1 (480p draft, 22 s, 3 references, audio off), 66 credits. Local: `keyframes/karsus/video/sp3_draft2.mp4`.
- **No cuts** (scene detection). The hero faces the camera for the first ~8 s with the face clearly visible; **likeness in video: mean SFace 0.53-0.56** on frames at 0.5-4 s (limit 0.50).
- Magic now reads: dozens of concentric glyph rings, hundreds of glowing runes rising in vertical streams, columns of light, a vortex, lightning converging on him.
- Gaps: from ~12 s the camera retreats and he is small again; the face cannot be checked after ~6 s. The beat "other cities' lights dim and flow to him" is still not clear. His crown and chest diagram flicker slightly between frames; the mantle turned green-cream at 6 s (cloth colour drift).

## Seedance 2.5 fresh 720p render of the draft-1 prompt (2026-10-31)
- Job `a2776928-6948-420c-ba0a-529e63e575b3`, 720p, 22 s, same prompt and 3 references as draft 1, **154 credits** (balance 315.19 to 161.19). Local: `keyframes/karsus/video/sp3_720p.mp4`.
- Finalising draft 1 exactly would have cost 352 credits (any draft finalisation renders at 1080p). A fresh generation is NOT the same take.
- Result: no cuts, 1280x720, one continuous take, rings/vortex/city present. **It is a different take from draft 1**: the wizard becomes a speck by ~8 s and is absent from the frame from ~12 s; the lightning and the dimming beats are weaker than in draft 1; the glyph rings are thinner. Draft 1 (`1917adc1…`) remains the better scene; draft 2 (`e4e7bcaf…`) the better face and magic.

## Seedance 2.0 Mini test, Set Piece 1 sky cities (2026-10-31)
- Job `3616a160-515f-4050-a599-882004cec20f`, `seedance_2_0_mini`, 720p, 15 s, audio off, 2 references (costume front and bust). **15 credits** (balance 161.19 to 146.19). Local: `keyframes/karsus/video/sp1_mini.mp4`.
- Result: 1280x720, **no cuts**, a convincing dawn glide between floating white-stone cities on inverted mountains, waterfalls off the edges, god rays, golden skiffs, ending on a spire where the wizard stands tiny. Quality comparable to Seedance 2.5 at a seventh of the price.
- Flaws: the skiffs read as small helicopters or drones in some frames; the wizard is too small at the end to check face or costume; the final tower is a lighthouse-like shaft rather than the grandest spire.
- Price table for 15 s clips (quotes, 2026-10-31): Seedance 2.0 Mini 720p 15 cr (1 cr/s); Kling 3.0 30 cr (2 cr/s); MiniMax H3 Max 768p 37.5 cr; Seedance 2.0 720p 67.5 cr; Grok Video 1.5 720p 67.5 cr; Seedance 2.5 720p 154 cr for 22 s.
- Plan: remaining about 71 s (SP2 13, SP4 14, SP5 22, SP6 12, inserts about 10) on the Mini would cost about 71 cr, about 92 cr with a 30 % reserve, against a balance of 146.19.

## Stabilised-prompt batch on Seedance 2.0 Mini (2026-10-31)
All 720p, audio off, no cuts (scene detection), prompts as in section 11 of the script. Balance 146.19 to 70.19 (76 credits).
| Set piece | Job | Length | Notes |
|---|---|---|---|
| SP1 sky cities (v2) | `380b20ad-4552-48ce-8516-780abca40178` | 15 s | no helicopters or fish; cities hang still; the cities look partly sunk in cloud at 1 s; the wizard's face is visible at the end |
| SP2 grey hunger | `e88c04d8-61ae-494e-9475-0e227b4a573b` | 13 s | forest, river and lake buried by a sand front; excellent |
| SP4 apotheosis | `5c7446ce-3925-4793-b671-cc96aeb49918` | 14 s | face visible; web of cyan threads; woman-of-light outline; **likeness only 0.41-0.46 (limit 0.50)** |
| SP5a lights go out | `c2e65285-6094-4fcb-86fe-e398eb0cd22b` | 8 s | start/end frames `116610c8…` (lit) and `ac5dc7ce…` (dark); exact blackout |
| SP5b the fall | `b80cd11a-4ec7-428f-821a-a26a5863cd0d` | 14 s | city tumbles and breaks up through clouds; strong |
| SP6 epitaph | `a59b8134-1297-44fa-bcbb-e9592dfab468` | 12 s | moss-covered statue in forest light, push-in to the stone face; excellent |
SP3 is the Seedance 2.5 draft 1 (`1917adc1…`, 480p, upscaled). Rough cut `karsus_rough_cut_v1.mp4`, 98.3 s, no audio, local in `keyframes/karsus/video/`.
Finding: the Mini keeps the costume but loses the face (0.41-0.46 vs 0.53-0.56 on Seedance 2.5). Plan: use a start image (the costume bust still) for the face-critical clips.

## Face inserts and apotheosis v2 with the costume close-up as start frame (2026-10-31)
Seedance 2.0 Mini, 720p, audio off, all single takes (no cuts). Balance 70.19 to 40.19 (30 credits).
| Clip | Job | Length | Result |
|---|---|---|---|
| SP4 apotheosis v2 (start image = bust) | `fbe3d007-3802-4aab-b749-a2a313e81afa` | 14 s | face locked at the start (0.50 at 1 s), drifts and shrinks as the camera pulls back; woman-of-light forms behind |
| i1 eyes glow | `9413d684-2020-44e4-a69b-294471463965` | 4 s | face 0.53 to 0.46; eyes glow white-cyan |
| i2 sigil ignites | `0124d4c4-f220-4e52-8d3c-a8887cfa5394` | 4 s | face 0.53 to 0.47; forehead sigil ignites |
| i3 dread | `1972a133-1d5c-487b-901a-25d3f13a6539` | 4 s | strong expression; SFace falls to 0.39-0.47 because of the wide-eyed expression |
| i4 stone spreads | `78492efb-20f2-4ac3-863e-d6dd42b56307` | 4 s | hands turn to grey stone; no face |
Likeness note: SFace scores drop when the expression is extreme or the face is small; they are not a fair measure of identity on i3 and the end of SP4.
Rough cut v2 (`karsus_rough_cut_v2.mp4`, inserts trimmed to 2.5 s, no audio): order SP1, i1, SP2, SP3 (2.5 draft 1, 480p upscaled), i2, SP4 v2, i3, SP5a, SP5b, i4, SP6.
Voice previews (ElevenLabs eleven_ttv_v3): Karsus `64Eyj3ChxBavO2dBqxph`, `eRZqsCTgtEziOSM3QNPu`, `C3iGAHaDHGjTzwrz19Lg`; Mystryl `8vxf9p6poKFmfutjUqSP`, `4PUebsnEIzT1IFq2xpVH`, `Q3LkydeY4oUZN16c5aMd`. Waiting for the user to choose.
