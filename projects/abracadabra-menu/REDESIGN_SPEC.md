# ABRACADABRA — REDESIGN SPEC v1

Date: 2026-11-18 · Target: LTX-2.5 22B (distilled INT8, 8 steps, 121f, 1280×720)
Scope: new skin, redesigned living mascot, per-item magic effects, render plan

---

## 1. Analysis of the current build (honest read)

### What works and must be kept
| Strength | Why it stays |
|---|---|
| Two-screen split (1 = left, 2 = right) | Correct physical layout, one HTML file per screen |
| Full-screen cinematic takeover every N min | Genuinely holds attention in a venue |
| Wand-slash transition between featured items | Cheap, effective, already coded (`fx_slash.mp4`) |
| Admin → LocalStorage / menu-data.js / Google CSV | Three-tier edit model is the right architecture |
| Day/night auto-switch at 19:00 | Fits the venue's actual trade |
| Burn-in nudge + periodic reload | Real signage problem, already solved |

### What is wrong (and gets fixed in this redesign)
| Problem | Evidence | Fix |
|---|---|---|
| **Reads as a video game lobby, not a restaurant** | Blizzard main-menu framing, rune-ring portal, "summon" language | Reframe as a *luxury conjuring bistro* — food is the hero, magic is the garnish |
| **Mascot is an object, not a presence** | Абра = static wand inside a portal; idle loop only | Абра becomes a **living character** with posture, gesture, gaze and reaction |
| **Only 3 food clips exist for 35 priced items** | `wand_burger`, `wand_wrap`, `wand_waffle` | **35 unique item effects**, one per priced item |
| **Clipping risk**: items with `price: null` still occupy layout slots | 15 hidden items sit in the same lists | Data already handles it; the new skin must not reserve empty frames |
| **Duplicate day/night video renders** double cost for little gain | `wand_idle_day` / `wand_idle_night` pattern | **Grade night in CSS**, render one clip per item. Halves render spend |
| **No combos in the data at all** | `menu-data.js` has zero combo entries | Add a `combos` array + combo clips so "+ помфрит" becomes a real upsell item |
| **Audio unused** | All clips are silent H.264 | LTX-2.5 generates native audio — add magic chimes + sizzle |

---

## 2. New skin — "The Grand Bistro of Illusions"

**Direction:** candlelit Art Nouveau restaurant, arcane linework as ornament, food lit like
jewellery. Not a game menu. Magic is atmospheric, never louder than the price list.

### Palette
| Token | Day ("Природна светлина") | Night ("Свеќи и неон") |
|---|---|---|
| `--bg` | `#0b0a12` deep aubergine | `#06040d` near-black violet |
| `--surface` | `rgba(28,22,38,.72)` | `rgba(18,12,30,.78)` |
| `--gold` | `#d9a441` antique gold | `#f0c46a` warmed gold |
| `--ember` | `#e0733a` | `#ff8a4c` |
| `--sage` | `#7fa88b` | `#8fc9a4` |
| `--ink` | `#f5efe3` | `#fff6e6` |
| `--arcane` | `#7b6bd6` faint violet | `#b48cff` neon violet |

Category colours are re-derived from this set (never raw red/lime/yellow):
burgers → ember, sandwiches → sage, toasts → warm sand, wraps → clay,
grill → charred crimson, desserts → rose gold, coffee → deep cocoa,
drinks → pale cyan, sides → gold.

### Typography
- **Display:** *Cormorant Garamond* (serif, high contrast) for category titles — restaurant voice
- **Items:** *Manrope* or *Rubik* (already bundled, Cyrillic-safe) — legibility at 3 m
- **Price:** *Cormorant* small caps, `--gold`, optically aligned right with a hairline leader dot row
- Cyrillic must be verified in both faces before commit

### Structure per screen
```
┌──────────────────────────────────────────────┐
│  A B R A C A D A B R A   ·  ornament rule     │  ← slim header, 6% height
├──────────────────────────────────────────────┤
│  ┌─ category card ────┐  ┌─ category card ─┐  │
│  │ БУРГЕРИ       ✦   │  │ СЕНДВИЧИ     ✦  │  │  ← cards float on the
│  │ Хамбургер    170  │  │ Пилешка ...  150 │  │    conjured stage video,
│  │ Чизбургер    200  │  │ Врат ...     160 │  │    blurred far behind
│  │ ...                │  │ ...              │  │
│  └────────────────────┘  └──────────────────┘  │
├──────────────────────────────────────────────┤
│  ✦ promo strip: name · price · live clip      │  ← bottom third
└──────────────────────────────────────────────┘
```

**Layer order (z-index):** stage video (blurred, 0.35 opacity) → vignette → cards →
Абра (only during a flourish) → item clip → cinematics (full-screen) → ticker.

**Improvement over current:** the stage video is *defocused* so text never fights motion.
The current build plays a sharp background video under text — a legibility defect.

---

## 3. Абра — the living wand (character bible)

**Concept:** Абра is the bistro's resident conjurer — a **living wand**: an enchanted
object with a will of its own, expressed through motion, light and glow. **Абра is a
wand, not a person.** No face, no eyes, no mouth, no hands, no body. Every "expression"
is a change of orientation, sway, pulse or light — never a human gesture.

### Physical form (lock to the DEPLOYED design — from the original README)
- **Black lacquered body** with **gold rune bands** (unchanged from the deployed mascot).
- **Crystal tip glowing in the logo's red and orange**, surrounded by the logo's
**triangle confetti**. At night the crystal turns **neon magenta**, matching the neon sign.
The tip is the **only expressive element** — it flares, dims, quickens and tilts toward
whatever interests it. It is a glowing crystal, **never a face or eye**.
- **Floats inside a portal with two rotating rune rings** (day/night variants), exactly
as deployed — not a free-floating rod, and not the earlier light-ribbon concept.
- A faint **gold ember trail** where it moves — proves it is alive.

### Personality (drives every animation — object-motion only)
| Trait | Expression |
|---|---|
| Proud host | Upright tilt, slow sweep of the light trails toward the door on idle |
| Mischievous | Flicks, spins, shows off a trick, crystal flashes bright |
| Attentive | Freezes and tilts its tip toward a new order |
| Theatrical | Signature flourish before every reveal |

**Guard rail:** never add a face, eyes, a mouth, hands, a body, or human posture to
Абра. If a generation adds them, it is a defect — reject the clip.

### Required animation set (idle behaviour, loops)
1. `abra_idle_breath` — gentle sway, crystal pulse at ~0.5 Hz (alive, not static)
2. `abra_idle_look` — tilts, pauses, tip turns toward the counter
3. `abra_sweep` — formal sweep of the light trails toward the door
4. `abra_tap` — impatient/playful tap on the stage, crystal flash
5. `abra_present` — the flourish that precedes every item reveal

**Rule:** Абра never appears during a cinematic takeover, and never overlaps the
price column. Presence is punctuation, not wallpaper.

---

## 4. Per-item magic effects (35 unique)

Every priced item gets its own effect. Twelve elemental families, each item a distinct
flourish within its family. Effect name = what Абра does + what the food does.

### Бургери — `forge_fire`
| Item | Effect | Beats |
|---|---|---|
| Хамбургер | **Ember Stamp** | crystal taps bun → ember ring brands the crown → smoke curl |
| Чизбургер | **Gold Cascade** | cheese pours upward as molten gold → folds over the patty |
| Абракадабра бургер | **Signature Ignition** | double tap → rune circle blooms, stack assembles itself in air |
| Хамбургер со јајце | **Yolk Sunburst** | egg cracks mid-air, yolk flares like a small sun, settles |
| Чикен бургер | **Feather Fry** | feather bursts into golden crumb that rains onto the fillet |
| Чикен чизбургер | **Ember & Feather** | feather spirals into molten cheese ribbon |
| Дрпан бургер | **Pull-Apart Shred** | crystal forks, meat unfurls into strands, re-stacks |
| Смачкан бургер | **Press of the Palm** | invisible hand flattens it, sear marks flare |

### Сендвичи / Тостови — `alchemy_press`
| Item | Effect | Beats |
|---|---|---|
| Пилешка шунка и кашкавал (сендвич) | **Alchemist's Seal** | wax seal stamps, bread seals itself |
| Врат и кашкавал (сендвич) | **Smoke Ring Press** | smoke ring descends, pressed into the crust |
| Кулен и кашкавал (сендвич) | **Spice Spark** | pepper sparks arc between layers |
| Свинска шунка и кашкавал (сендвич) | **Hearth Fold** | bread folds like warm linen |
| Хот дог | **Rune Skewer** | a rune skewer impales and lifts it, steam rises |
| Корн дог | **Golden Crust Lace** | corn lattice weaves itself around the sausage |
| Пилешка шунка и кашкавал (тост) | **Grid Brand** | grill bars brand themselves, cheese bubbles |
| Врат и кашкавал (тост) | **Toast Levitation** | hovers, rotates, lands toasted |
| Кулен и кашкавал (тост) | **Curing Glow** | warm amber glow passes through the slice |
| Свинска шунка и кашкавал (тост) | **Butter Gleam** | butter melts in a thin gold sheet |

### Врапови — `spiral_binding`
| Item | Effect | Beats |
|---|---|---|
| Дрпано јунешко | **Spiral Bind** | tortilla spirals itself, ribbons of light stitch the seam |
| Дрпано пилешко | **Feather Spiral** | feathers orbit inward, become the wrap |

### Скара — `dragon_breath`
| Item | Effect | Beats |
|---|---|---|
| Ражнич со пилешки џигер | **Skewer Flame Lick** | three small flames lick along the skewer |
| Кебапче | **Coal Breath** | coals exhale, ember dust settles |

### Десерти — `crystal_lattice` / `sugar_sorcery`
| Item | Effect | Beats |
|---|---|---|
| Вафла со нутела и банани | **Chocolate Lattice** | lattice weaves, chocolate floods the squares |
| Вафла со мармелад | **Jewel Drops** | marmalade drops fall and set like gems |
| Вафла со крем од ф'стак | **Pistachio Dust Storm** | green dust storm settles into cream |
| Абракадабра вафла | **Signature Snow** | powdered-sugar snow falls upward, then down |
| Сутлијаш | **Cinnamon Sigil** | cinnamon writes a sigil on the surface, sinks in |

### Додатоци — `lightning_cut` / `golden_crust`
| Item | Effect | Beats |
|---|---|---|
| Лепче | **Dough Rise** | dough swells and crusts over in one breath |
| Помфрит мал | **Arc Cut** | one thin arc splits a potato, fries fall into place |
| Помфрит голем | **Arc Storm** | three arcs, cascade of fries |
| Чипс | **Crisp Snap** | a snap ripples through, chips curl |

### Кафе — `dark_elixir`
| Item | Effect | Beats |
|---|---|---|
| Нес-кафе | **Dark Brew Conjure** | dark liquid rises into the glass, foam crowns it |
| Фрапе | **Frost Vortex** | ice shards spiral into a frosted vortex |

### Пијалоци — `potion_mastery`
| Item | Effect | Beats |
|---|---|---|
| Милкшејк | **Cream Cyclone** | cream cyclone spins up, cherry lands last |
| Сок | **Citrus Bloom** | citrus segments bloom outward, juice arcs into glass |

---

## 5. Design improvements implemented in the rebuild

1. **Defocused stage** — background video blurred so text owns the frame
2. **Single clip per item** — night achieved by CSS grade + `filter`, halving render spend
3. **No empty frames** — `price: null` items collapse cleanly instead of reserving space
4. **Combos modelled** — `combos[]` in data with own price and own clip
5. **Audio enabled** — native LTX-2.5 audio: chimes, sizzle, pour (muted off by policy on TV, kept for social cuts)
6. **Legibility gate** — text must pass contrast ≥ 7:1 over the brightest frame of the stage video
7. **Cinematic interval respects both screens** — offset math kept, but night cinematics now shorter (6 s) to match lower foot traffic
8. **Preload budget** — only featured + next-category clips preload; the rest stream on demand
9. **Admin gains "effect library" view** — shows which of the 35 effects is assigned where
10. **Reduced-motion fallback** — static poster frame if the TV reports low performance

---

## 6. Render plan (LTX-2.5 on Vast.ai)

| Parameter | Value | Source |
|---|---|---|
| Model | `ltx-2.5-22b-distilled-transformer-comfy-int8-convrot` | doc 59 §1 |
| Encoder | `gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot` | doc 59 §11 (settled) |
| VAE | video + audio, both | doc 59 §1 |
| Steps / CFG | 8 / 1.0 | doc 59 §10 |
| Frames | 121 (8n+1) ≈ 5 s @ 24 fps | doc 59 §1 |
| Resolution | 1280×720 (÷32) | doc 59 §6 |
| Chain | I2V from food keyframe → two-stage upscale | doc 59 §10 |
| Prompt form | continuation-form, one action, prop anchored, audio cue | anti-slop standard |

**Clip inventory:** 35 item clips + 5 Абра idle/gesture clips + 1 stage loop = **41 clips**
**Not 70** — day/night is graded, not re-rendered.

### Cost projection (must be approved before rent)
| Line | Estimate |
|---|---|
| 48 GB GPU (A100/H100 class) | ~$0.70–1.20 /hr |
| Weight download ~40 GB | 20–40 min |
| ComfyUI + node setup | 30–45 min |
| 41 clips × ~2.5 min (incl. 2-stage upscale) | ~1.7 hr |
| Retrieval + verification | 20 min |
| **Total wall clock** | **~3.5–4.5 hr** |
| **Total spend** | **~$3.50–5.50** |

**Available credit: $10.87. Zero instances currently running.**
Recommended cap: **$6.00**, hard-stop at 41 clips or on any failed gate.
This leaves ≥$4.80 reserve — credit exhaustion is treated as data loss, never as a stopping point.

---

## 7. Build order

1. Write this spec ✔
2. Generate `clip_specification.json` with 35 unique effects + LTX prompts ✔
3. Build new `index.html` skin (structure, palette, type, cards) — no GPU
4. Build Абра overlay component + gesture timeline — no GPU
5. Generate 35 food keyframes (still images — no video GPU needed)
6. **Spend gate: itemized approval + $6.00 cap**
7. Rent one 48 GB box, prove 1 clip end-to-end, pass gates, then batch
8. Pull clips home as they land, verify per clip, then deploy to KVM4
