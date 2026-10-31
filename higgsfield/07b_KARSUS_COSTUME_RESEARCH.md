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
