# ============================================================
# HOLLOW BLOOM — COMPLETE GROK PACKET (keyframe + video prompts)
# assembled 2026-11-15 for handoff to Grok
# ============================================================

## PART 0 — FILM CANON (from 36_HOLLOW_BLOOM_BOSSFIGHT_SPEC_v3.md)

# 36 — Ловецот и Паладинот: Шупливиот Цвет (v3) — 2:25 cinematic boss fight

> DEFINE deliverable v3. Zero cost — authoring only, no rental committed.
> **Replaces `25`, `26_v2`, `27` for world, cast, boss, and fight.** Those files stay
> archived as the ash-titan draft; only the pipeline methodology carries forward.
> Design canon = the director's Grok design pack, installed at `media/dhpf_design_v5/`.
> Compiled 2026-11-08.
> **PIPELINE + RENDER REALITY (2026-11-10):** video renders via the OFFICIAL
> `ltx_pipelines.distilled` (Lightricks/LTX-2 repo), NOT ComfyUI — recipe +
> measured findings in 38_LTX_VIDEO_GENERATION_SPEC.md §0. Per-shot model
> assignment + the transform beat below are now canon.

---

## 0A. RENDER ASSIGNMENT (per shot — from the 2026-11-10 proofs)

Every shot is assigned a model by its content, because the 8-step distilled model
loses 60-98% of high-frequency detail after the first frame (DD's glowing hair dies
first), while violent-action drift is characterful:

| Shot content | Model | Why |
|---|---|---|
| **DD / AZ hero closeup, identity-critical** | **DEV (ltx-2.3-22b-dev, 30-step)** + hair-guard prompt | finest detail; holds the glowing teal-blue hair + face |
| **Violent action, boss thrash, wide chaos** | **DISTILLED (8-step)** | fast; the deliberate drift/mutation reads as energy |
| **Transform beat (the arrow-snap)** | **DISTILLED** | the DD→monster morph IS the effect here |

All shots: faithful verb-first motion-only prompt (39_CORRECTED_PROMPT_STANDARD.md),
--image strength 0.7, full 24GB gemma, 1216×704, 121 frames @ 24fps, native audio.

### THE TRANSFORM BEAT (canon — director-approved)

Where the fight turns, DD looses a volley of **ice arrows**; the scene **snaps/transforms**
and the **Hollow Bloom takes the hits**, ice blooming across its vines as it recoils.
This owns the violent-shot identity morph as a deliberate transition (DD → ice-mist →
the struck boss). It is a TRANSITION, never a hero-closeup leak.

---

## 0. Concept — the blight triangle

A fungal marsh is dying. Where the water glowed teal, a grey corruption now spreads
in a widening ring around **Шупливиот Цвет (The Hollow Bloom)** — a colossal
plant-vine aberration whose root-feet rot everything they touch. Two forces answer
it: **ICE** (the demon hunter — rot cannot spread through living frost) and **LIGHT**
(the paladin — gold fire sterilizes and purifies the ground). The fight runs on that
triangle and on the two heroes fighting as a unit: every phase ends in a tag-team
combination. The corruption ring is also a **spatial timer** — it visibly widens
across the film; ground the heroes stood on in Phase 1 is grey by Phase 3.

---

## 1. Cast (locked to the director's design pack)

| Role | Identity | Weapon / kit | The look | Source |
|---|---|---|---|---|
| **Ловецот — Демоно-ловец** | **DD** | twin crystal hand crossbows | bare head ALWAYS; glowing teal-blue hair waving weightlessly as if underwater; ICE/ARCANE palette; new armor from the director's pack | face `media/dhpf_refs/v2/dd_card_a.jpg` (+b,c); armor `design_v5/dd_armor_base.jpg`, state `dd_armor_state.jpg`, weapon `dd_weapon.jpg` |
| **Паладинот** | **AZ (Blagoj)** | legendary two-handed greatsword | face fully visible ALWAYS (open helm); molten-gold rune-tattoo on forearm; gold holy-fire kit | face `media/dhpf_refs/v2/az_card_a.jpg`; armor `design_v5/az_armor_base.jpg`, states `az_armor_state_a.jpg`/`_b.jpg`, weapon `az_weapon.jpg` |
| **Шупливиот Цвет — бос** | AI-default, ZERO human faces | tendril whips, spore-sacs, root-feet | corpse-flower maw, braided black-green vine body, grey blight ground | `design_v5/Monster/` (7 sheets) |

**DD constants (never change):** bare head — no helmet, hood, bandana, or mask in any
state. Hair glows teal→blue and waves as if underwater. Glacial colour system:
idle gradient → charging ripple bands → cast pulse → Glacier Form white-blue bloom
with teal sigil rings.

**AZ constants (UPDATED 2026-11-08 — bare-head rule DEAD per director):** closed helm or open-face, per the design sheet; face card NOT a mandatory ref. One-sided molten-gold
rune-tattoo surges per ability — only the technique's pathways ignite, white-gold.
Greatsword present in every shot.

---

## 2. Ability → VFX map

**Demon Hunter (ICE/ARCANE):**
- **Frost Rush** — comet of rime; frozen streak across marsh water, ice spidering over reeds.
- **Glacial Aura** — rotating ring of frost + arcane sigils; spores that touch it crystallize and fall like snow.
- **Rime Beams** — twin white-blue lances from the eyes; whatever they rake flash-freezes — tendrils go brittle ice-white.
- **Frost Dance** — spinning crescent slashes throwing razor-ice arcs.
- **Glacier Form** — leap + explosive landing sheets ground in ice; huge Immortal wings of blue-tipped frost; snowstorm. *(ability sheets in design_v5/DD)*
- **The Hunt (Glacial Drift)** — aerial lance-dive; impact blooms a frozen rose of ice spikes, then shatters.

**Retribution Paladin (GOLD LIGHT):**
- **Blade of Justice** — light-blade summoned from above; falls in a white pillar.
- **Templar's Verdict** — radiant two-handed arc; golden shockwave detonates on contact.
- **Divine Storm** — spiral of golden blades radiating outward.
- **Wake of Light** — cone of white-gold radiance that scours blight; corrupted ground flushes back to living teal.
- **Execution Sentence** — delayed rune-mark; detonates in a column of light.
- **Avenging Wrath** — tattoo surges fully; translucent golden wings; eyes white. *(ability sheets in design_v5/AZ)*

**The Hollow Bloom (BLIGHT):**
- **Tendril Whip** — thorned vine-arms crack like whips; gouge blight-furrows.
- **Spore Burst** — spore-sacs rupture; choking green clouds drift low.
- **Root Spikes** — root-feet erupt as a ring of black thorn spikes under a target.
- **Maw Snap** — the corpse-flower head lunges, vertical tooth-maw gaping.
- **Corruption Wave** — the grey ring visibly pulses outward; ground dies behind it.
- **Pollen Nova** (P3 supernova) — the bloom opens fully; a vortex of glowing spores rises and blots the marsh light.

**Interactions (the visual engine):**
- ICE × BLIGHT → freeze: tendrils brittle, spores crystallize and fall.
- LIGHT × BLIGHT → purify: blighted ground flushes back to glowing teal.
- ICE × LIGHT → the three tag combos below.

---

## 3. The boss — Шупливиот Цвет (The Hollow Bloom)

Colossal plant-vine aberration, ~4 m, hunched. Bloated corpse-flower head with a
vertical tooth-maw, no eyes. Braided black-green vine body, thorned tendril arms,
pulsing translucent spore-sacs on its back. Root-feet rot the earth grey; black
corruption veins spread outward. A hunger that flowers — not malice.
**Zero human faces, always.** Director's monster sheets (`design_v5/Monster/`) are
the only look references; ability variants from the same set.

| Phase | Name (MK) | Form | Signature | Music/SFX |
|---|---|---|---|---|
| P1 | „Коренот на гнилежот" | rooted, tendril reach | Tendril Whip + Root Spikes | low drone, wet strings, spore hiss |
| P2 | „Спорниот дожд" | spore-sacs burst, ring accelerates | Spore Burst + Corruption Wave | rising brass, sub rumble, spore wheeze |
| P3 | „Цветот што ја голта мочуриштето" | full-bloom enrage, marsh dies in waves | Pollen Nova | restrained choir → stillness |

---

## 4. Shot list — 50 shots, FLF, ~2:25

Legend: size (W/M/C/CU/I) · START→END · mover/camera · t(s). 50 × ~2.9 s ≈ 145 s.

### Phase 0 — Arrival (~15 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 01 | W | fungal marsh at dusk, teal water, giant mushroom towers → DD and AZ on a hummock at the corruption ring's edge, spore-mist drifting | dolly-in; mist drifts | 3.0 |
| 02 | W | both at the grey edge → the corruption visibly creeps a hand's width toward them | slow push; veins pulse | 2.5 |
| 03 | I | DD's hand cocks a crossbow → a frost-arrow crystallises in the groove | insert; frost spreads | 2.5 |
| 04 | I | DD's hair rolls in a slow weightless wave → neon teal brightens, nearby spores freeze and fall | insert; hair drifts like water | 2.5 |
| 05 | I | AZ's gauntlet grips the greatsword hilt → rune-tattoo ember-gold wakes along the wrist | insert; light travels | 2.5 |
| 06 | W | the Hollow Bloom rises from the corrupted patch, spore-sacs inflating → stands, maw opening | low rise; spores fall upward | 3.0 |

### Phase 1 — „Коренот на гнилежот" (~40 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 07 | C | tendril coils → snaps | whip crack; shake | 2.5 |
| 08 | M | DD raises an arm (Glacial Aura) → frost ring blooms, drifting spores crystallize | aura; camera pull | 2.5 |
| 09 | W | whip hits near → blight-furrow gouges the marsh | whip+scorch; whip-pan | 3.0 |
| 10 | M | DD kicks off (Frost Rush) → comet of rime over the water | sprint smear; whip-pan | 2.5 |
| 11 | C | DD fires both crossbows → three crystalline frost-bolts streaking | bolts; slow-mo→realtime | 2.5 |
| 12 | I | bolts hit tendril → flash-freeze patch, the vine goes brittle white | impact; crash-zoom | 2.5 |
| 13 | W | AZ plants greatsword tip → gold shockwave cracks the corrupted floor | ring; low hold | 2.5 |
| 14 | M | AZ swings Templar's Verdict → light arc detonates on the bloom | swing+boom; orbit | 3.0 |
| 15 | C | bloom reels, maw twisting → spore-sacs flare brighter | recoil; push-in | 2.5 |
| 16 | W | GROUP — bloom sweeps a tendril across the arena → both heroes vault opposite ways | sweep+vault; cross-cut | 3.0 |
| 17 | M | DD flips back → lands in crouch, frost-smoke | flip+land; whip-pan | 2.5 |
| 18 | C | DD's eyes ignite (Rime Beams) → twin white-blue lances slash out | beam+freeze; rack | 3.0 |
| 19 | W | COMBO #1 Freeze-and-Sunder: Rime Beams flash-freeze a tendril mid-swing → AZ's Verdict shatters it, golden shockwave through ice | beam→shatter; track | 3.5 |
| 20 | M | bloom staggers, frozen vine fracturing → maw opens in a silent roar | recoil; push | 2.5 |

### Phase 2 — „Спорниот дожд" (~44 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 21 | W | bloom hunches → spore-sacs rupture one after another | burst+sacs; wide | 3.0 |
| 22 | C | AZ raises sword (Blade of Justice) → light-blade summons above | blade descend; tilt | 2.5 |
| 23 | M | light-blade plunges → bloom staggers under a white pillar | blade+pillar; pan | 3.0 |
| 24 | W | bloom slams root-feet → Spore Rain begins, sky dims green | rain+shock; crane | 3.0 |
| 25 | M | DD curls under wings (Glacial Aura) → spores hiss to snow on the membrane | shield+hiss; close | 2.5 |
| 26 | M | AZ strides through spore rain → light sheds it like water, ground flushing teal at his boots | walk+light; dolly-back | 3.0 |
| 27 | I | bloom exhales a choking spore gout → green column | gout; insert | 2.5 |
| 28 | W | GROUP — DD vaults the gout while AZ charges through its shadow | split-action; wide | 3.0 |
| 29 | W | AZ stands square (Wake of Light) → white-gold cone scours ground, blight receding in a wave | cone+purge; sweep | 3.0 |
| 30 | C | DD winds up (The Hunt) → wings fold, snow coils concentrate | wind-up; push | 3.0 |
| 31 | W | The Hunt dive → lance down, crossbows first, frozen trail | dive+crater; aerial | 3.5 |
| 32 | M | impact crater → spore-sacs flicker, bloom forced to one root-knee | impact+kneel; shake | 3.0 |
| 33 | C | COMBO #2 Hoarfrost Judgement: AZ marks the sac-cluster (Execution Sentence rune) → DD's frost locks it → rune detonates in a light column through ice | mark→freeze→boom; orbit | 3.5 |
| 34 | C | AZ regrips sword → holy runes blaze up the blade | grip+runes; orbit | 2.5 |

### Phase 3 — „Цветот што ја голта мочуриштето" (~42 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 35 | W | bloom enrage → swells open, spores spiral into a vortex | swell+vortex; wide | 3.0 |
| 36 | CU | bloom-voice (subtitle) → „Од трева сте — и во трева ќе ве вратам.“ | maw; CU | 2.5 |
| 37 | W | bloom ignites the Pollen Nova → spore supernova rises, marsh light drowning | nova; crane | 3.5 |
| 38 | M | DD wing-flare, crossbows raised → glacier energy peaks | flare+shift; orbit | 3.0 |
| 39 | M | AZ plants hands (Avenging Wrath) → tattoo surges gold→white, golden wings bloom | surge+wings; rack | 3.0 |
| 40 | W | GROUP still-beat — the two hold under the rising spore-nova | held wide; spores only | 2.5 |
| 41 | M | DD leaps — full Glacier Form, Immortal wings wide, snowstorm against the spores | leap+form; aerial | 3.0 |
| 42 | M | AZ rises — radiant, greatsword burning white-gold | rise+halo; tilt | 3.0 |
| 43 | W | COMBO #3 Blizzard & Verdict: both launch together — frost streak and gold streak winding around each other | twin dive; aerial | 3.0 |
| 44 | C | DD fires Rime Beams + crossbows at once → violet-white lance through the bloom's heart | beam+shot; slow-mo | 3.0 |
| 45 | C | AZ's final Verdict arc → the bloom splits, light floods out | slash+split; crash | 3.0 |
| 46 | W | the Pollen Nova collapses inward — light versus spore | collapse; wide pull | 3.0 |
| 47 | I | the corpse-flower head cracks → folds shut, wilting | crown+fall; inset | 2.5 |
| 48 | W | spores settle like grey snow — two silhouettes over the purifying patch | drift; wide | 3.0 |
| 49 | C | DD exhales a wisp of frost, hair dimming to idle gradient → she almost smiles | breath+frost; CU | 3.0 |
| 50 | W | AZ turns, greatsword over shoulder → dawn breaks, marsh water glowing teal again | walk+light; dolly | 3.0 |

**Continuity spine:** corruption ring (narrow→wide→racing→purified); spore-sacs
(dim→flaring→ruptured→dark); tendrils (intact→frozen→shattered #19, regrown in P2,
blown apart in P3); DD hair never still; AZ tattoo surges per ability; hero power
states (dormant→partial→ultimate).

**Group & tag coverage:** all-three frames — 01,02,06,09,13,16,21,24,28,35,37,40,43,46,48,50.
DD solo — 03,04,08,10,11,12,17,18,25,30,31,38,41,44,49. AZ solo — 05,14,15,22,23,26,29,33,34,39,42,45.
Tag combos — #19 Freeze-and-Sunder, #33 Hoarfrost Judgement, #43–45 Blizzard & Verdict.

---

## 5. Narration & dialogue (Macedonian — 7 lines, no narrator)

| # | Speaker | Line (MK) | Moment |
|---|---|---|---|
| D1 | Bloom (spore-voice, subtitle) | „Дојдовте да расцветате во мене, како сите што дојдоа пред вас.“ | P1, after #07 |
| D2 | Bloom | „Мразот само го успорува гнилежот.“ | P1→P2, after #19 |
| D3 | Paladin | „Светлината не се гаси.“ | P2, #26, under breath |
| D4 | Bloom | „Од трева сте — и во трева ќе ве вратам!“ | P3, #36 |
| D5 | DD | „Замрзни.“ | P3, #44 |
| D6 | Paladin | „Суди.“ | P3, #45 |
| D7 | DD (epilogue) | „И во најтоплото мочуриште, зимата наоѓа пат.“ | #49, whispered |

---

## 6. Audio (restrained, spatial)

```
SFX: spore hiss / marsh-wind bed (L-R drift); tendril CRACK (P1); ice-shatter
CRACKLE on every flash-freeze; Rime-beam THRUM + freeze SIZZLE; crossbow frost-bolt
WHINE; greatsword RING + holy HUM; tattoo surge electric HISS; spore-rain WHEEZE;
wing-lift WHOOSH + landing THUD; Pollen Nova as implosion SUCK + sub.
MUSIC: P1 low drone + wet strings, silence-lean; P2 rising brass + sub-rumble, one
hit per bloom slam; P3 short choir swell → STILLNESS at the killing blow.
Rule: score never masks voice or SFX.
```

---

## 7. Pipeline (research-first; zero cost until price approved)

```
P0 RESEARCH    ✓ director's design pack installed at design_v5/
P1 ENHANCE     ✓ this v3 spec — 50-shot spine, kits, combos
P2 SPLIT       ✓ 7 dialogue lines, no narrator
P3 SCRIPT      ✓ §4–§6
P4 STORYBOARD  storyboards/42_hollow_bloom.html + machine JSON
P5 PROMPTS     100 keyframe jobs (50×2 FLF) + Wan FLF video jobs; marsh world,
               design_v5 refs, v2 face cards; canonical names only
P6 PRICE CHECK live Vast scan + itemized estimate + per-run approval
P7 PROOF       10-shot sample → director verdict (loop until accepted)
P8 FULL RUN    approved shots → copy+sha256+ffprobe → assembly → teardown (verified)
```

**Prompt template (Qwen-Image-Edit, 1280×720):**
```
{IDENTITY LOCK verbatim}. {DD: bare head, glowing teal weightless hair, frost-arcane}.
{AZ: face visible, molten-gold rune-tattoo forearm, greatsword}. {armor/weapon from
design_v5 sheets}. {action}. {marsh env: teal water, giant fungi, spore-mist, grey
corruption patch}. {fore/mid/background}. Photorealistic cinematic film still, 35mm
anamorphic, real skin, film grain.
Negative: duplicate/extra face, extra limbs, text, watermark, cartoon, illustration,
cel-shaded, 3d render, plastic skin.
```

---

## 8. Acceptance criteria

1. Shots = 50 (≥40), 2.5–3.5 s each → ≥2:20 runtime.
2. FLF: start+end reference for every shot; single-reference jobs rejected.
3. Camera grammar in every video prompt.
4. Motion floor via frame-difference — no held stills.
5. Ability legibility — each signature matches its VFX map (§2), tattoo surge reads.
6. **Blight triangle reads visually**: frost stops the spread, light purifies ground.
7. Group + combo coverage: ≥1 all-three series + 3 tag combos verified.
8. Identity gates: DD ≥0.50 vs dd v2 centroid; AZ ≥0.50 vs az centroid; bloom = 0 faces.
9. Mute test: the fight still reads.
10. Audio: spatial SFX + restrained score; Macedonian-only voices; 7 lines.
11. DD hair waves underwater-style in every DD shot; bare head always. AZ face visible always.
12. Photoreal only; external references only (no self-deliverables as benchmarks).
13. **Corruption-ring continuity**: the grey ring visibly widens P1→P3, purified at #46+.

---

## 9. Asset wiring (design_v5 → refs)

```
DD ARMOR   media/dhpf_design_v5/dd_armor_base.jpg (+dd_armor_state.jpg, +6 ability shots in DD/)
DD WEAPON  media/dhpf_design_v5/dd_weapon.jpg
AZ ARMOR   media/dhpf_design_v5/az_armor_base.jpg (+az_armor_state_a.jpg, _b.jpg, +6 ability shots in AZ/)
AZ WEAPON  media/dhpf_design_v5/az_weapon.jpg
BOSS       media/dhpf_design_v5/Monster/ (7 sheets: look + ability variants)
SETTING    media/dhpf_design_v5/Setting/ (12 plates; 1–2 primary plates + detail refs)
FACES      media/dhpf_refs/v2/dd_card_a.jpg (+b,c) · az_card_a.jpg
DEAD CANON: malgarot_look_card, canyon plates, old dd/az look cards + fused masters
```

---

## 10. Open questions

1. Which Setting plate is the primary arena view? (default: chosen at storyboard build; director may override)
2. Which DD ability shot is the ULTIMATE anchor for #37–41? (default: the wings/full-bloom one; director may override)
3. Same for AZ ultimate anchor (#39–42).
4. Title card: „Расцветано во мраз" — include? (default: yes, 1.5 s before #01)

---

*DEFINE-ONLY. No GPU spend until P5 audit passes, a P6 itemized estimate is approved,
and the P7 proof loop returns an accepted sample.*

## PART 1 — THE 100 KEYFRAME IMAGE PROMPTS (37_GROK, EXACT, UNABRIDGED)

# HOLLOW BLOOM — 100 KEYFRAME PROMPTS FOR GROK GENERATION

Film: Шупливиот Цвет (The Hollow Bloom) — demon hunter DD + retribution paladin AZ vs the Hollow Bloom, in a blighted fungal marsh.

## NAMING — save every image EXACTLY like this

```
kf_01_start.png   kf_01_end.png
kf_02_start.png   kf_02_end.png
... through ...
kf_50_start.png   kf_50_end.png
```
- `kf_NN` = the shot number, always two digits (01, 02, ... 50).
- `_start` / `_end` = the FIRST and LAST frame of that shot (Wan FLF needs both).
- So 50 shots x 2 = 100 files total. Nothing else in the filename.

## THE REFERENCE IMAGES TO ATTACH (upload these into Grok once, attach per shot as listed)

- **dd_armor_base.jpg** — DD complete character card (armor + HER face)
- **az_armor_base.jpg** — AZ complete character card (armor + HIS face)
- **dd_weapon.jpg** — DD twin crossbows
- **az_weapon.jpg** — AZ greatsword
- **dd_armor_state.jpg**, **az_armor_state_a.jpg**, **az_armor_state_b.jpg** — ability states
- **Monster/<the 7 monster sheets>** — the Hollow Bloom + abilities
- **Setting/<the 12 marsh plates>** — the world

Attach rule: every shot lists its exact attachments under it. Attach exactly those, nothing more.

---


## SHOT 1  (phase end · W)

### kf_01_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: stand on a hummock at the corruption ring edge, mist drifting. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — dolly-in.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_01_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: stand on a hummock at the corruption ring edge, mist drifting. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: dolly-in, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 2  (phase end · W)

### kf_02_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: face the creeping grey edge; the corruption advances a handspan. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — slow push.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_02_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: face the creeping grey edge; the corruption advances a handspan. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: slow push, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 3  (phase end · I)

### kf_03_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: hand cocks a crossbow; a frost-arrow crystallises in the groove. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — insert.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_03_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: hand cocks a crossbow; a frost-arrow crystallises in the groove. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: insert, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 4  (phase end · I)

### kf_04_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: hair rolls in a slow weightless wave; neon teal brightens; spores near her freeze and fall. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — insert.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_04_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: hair rolls in a slow weightless wave; neon teal brightens; spores near her freeze and fall. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: insert, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 5  (phase end · I)

### kf_05_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: gauntlet grips the greatsword hilt; rune-tattoo ember-gold wakes along the wrist. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — insert.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_05_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: gauntlet grips the greatsword hilt; rune-tattoo ember-gold wakes along the wrist. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: insert, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 6  (phase end · W)

### kf_06_end.png
**Attach:** boss_main.jpg, set_plate.jpg, dd_ab1.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: rises from the corrupted patch; spore-sacs inflate; maw opens. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — low rise.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_06_start.png
**Attach:** boss_main.jpg, set_plate.jpg, dd_ab1.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: rises from the corrupted patch; spore-sacs inflate; maw opens. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: low rise, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 7  (phase end · C)

### kf_07_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: a thorned tendril coils tight, then snaps. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — whip crack.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_07_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: a thorned tendril coils tight, then snaps. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: whip crack, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 8  (phase end · M)

### kf_08_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: raises an arm; a rotating frost-and-sigil ring blooms; drifting spores crystallize and fall. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — aura pull.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_08_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: raises an arm; a rotating frost-and-sigil ring blooms; drifting spores crystallize and fall. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: aura pull, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 9  (phase end · W)

### kf_09_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: tendril whip gouges a blight-furrow across the marsh. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — whip-pan.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_09_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: tendril whip gouges a blight-furrow across the marsh. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: whip-pan, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 10  (phase end · M)

### kf_10_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: kicks off in a comet of rime over the water. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — sprint smear.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_10_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: kicks off in a comet of rime over the water. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: sprint smear, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 11  (phase end · C)

### kf_11_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: fires both crossbows; three crystalline frost-bolts streak. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — slow-mo to realtime.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_11_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: fires both crossbows; three crystalline frost-bolts streak. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: slow-mo to realtime, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 12  (phase end · I)

### kf_12_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: bolts strike a tendril; flash-freeze spreads; the vine goes brittle white. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — crash-zoom.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_12_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: bolts strike a tendril; flash-freeze spreads; the vine goes brittle white. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: crash-zoom, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 13  (phase end · W)

### kf_13_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: plants the greatsword tip; a gold shockwave cracks the corrupted floor. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — low hold.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_13_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: plants the greatsword tip; a gold shockwave cracks the corrupted floor. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: low hold, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 14  (phase end · M)

### kf_14_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg, az_ab1.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: swings a radiant two-handed arc; it detonates on the bloom. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — orbit.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_14_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg, az_ab1.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: swings a radiant two-handed arc; it detonates on the bloom. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: orbit, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 15  (phase end · C)

### kf_15_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: reels; maw twists; spore-sacs flare brighter. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — push-in.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_15_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: reels; maw twists; spore-sacs flare brighter. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: push-in, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 16  (phase end · W)

### kf_16_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the bloom sweeps a tendril across the arena; both heroes vault opposite ways. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — cross-cut.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_16_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the bloom sweeps a tendril across the arena; both heroes vault opposite ways. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: cross-cut, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 17  (phase end · M)

### kf_17_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: flips back and lands in a crouch, frost-smoke curling. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — whip-pan.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_17_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: flips back and lands in a crouch, frost-smoke curling. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: whip-pan, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 18  (phase end · C)

### kf_18_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: eyes ignite; twin white-blue lances slash out. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — rack.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_18_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: eyes ignite; twin white-blue lances slash out. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: rack, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 19  (phase end · W)

### kf_19_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Freeze-and-Sunder: her Rime Beams freeze a tendril mid-swing; his Verdict shatters it in a golden shockwave through ice. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — track.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_19_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Freeze-and-Sunder: her Rime Beams freeze a tendril mid-swing; his Verdict shatters it in a golden shockwave through ice. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: track, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 20  (phase end · M)

### kf_20_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: staggers; the frozen vine fractures; the maw opens in a silent roar. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — push.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_20_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: staggers; the frozen vine fractures; the maw opens in a silent roar. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: push, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 21  (phase end · W)

### kf_21_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: hunches; spore-sacs rupture one after another. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — wide.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_21_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: hunches; spore-sacs rupture one after another. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: wide, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 22  (phase end · C)

### kf_22_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: raises the sword; a light-blade summons above. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — tilt.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_22_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: raises the sword; a light-blade summons above. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: tilt, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 23  (phase end · M)

### kf_23_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the light-blade plunges; the bloom staggers under a white pillar. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — pan.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_23_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the light-blade plunges; the bloom staggers under a white pillar. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: pan, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 24  (phase end · W)

### kf_24_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: slams root-feet; spore rain begins; the sky dims green. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — crane.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_24_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: slams root-feet; spore rain begins; the sky dims green. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: crane, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 25  (phase end · M)

### kf_25_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab2.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: curls under her wings in a Glacial Aura; spores hiss to snow on the membrane. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — close.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_25_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab2.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: curls under her wings in a Glacial Aura; spores hiss to snow on the membrane. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: close, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 26  (phase end · M)

### kf_26_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: strides through the spore rain; light sheds it like water; the ground flushes teal at his boots. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — dolly-back.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_26_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: strides through the spore rain; light sheds it like water; the ground flushes teal at his boots. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: dolly-back, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 27  (phase end · I)

### kf_27_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: exhales a choking green spore gout in a rising column. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — insert.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_27_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: exhales a choking green spore gout in a rising column. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: insert, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 28  (phase end · W)

### kf_28_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: she vaults the gout while he charges through its shadow. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — wide.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_28_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: she vaults the gout while he charges through its shadow. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: wide, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 29  (phase end · W)

### kf_29_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: stands square; a white-gold cone scours the ground; blight recedes in a wave. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — sweep.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_29_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: stands square; a white-gold cone scours the ground; blight recedes in a wave. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: sweep, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 30  (phase end · C)

### kf_30_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab3.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: winds up; wings fold; snow coils concentrate around her. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — push.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_30_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab3.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: winds up; wings fold; snow coils concentrate around her. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: push, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 31  (phase end · W)

### kf_31_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: dives lance-first, crossbows leading, a frozen trail behind. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — aerial.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_31_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: dives lance-first, crossbows leading, a frozen trail behind. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: aerial, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 32  (phase end · M)

### kf_32_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: impact crater; spore-sacs flicker; the bloom is forced to one root-knee. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — shake.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_32_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: impact crater; spore-sacs flicker; the bloom is forced to one root-knee. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: shake, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 33  (phase end · C)

### kf_33_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Hoarfrost Judgement: he marks the sac-cluster with a rune; her frost locks it; the rune detonates in a light column through ice. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — orbit.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_33_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Hoarfrost Judgement: he marks the sac-cluster with a rune; her frost locks it; the rune detonates in a light column through ice. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: orbit, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 34  (phase end · C)

### kf_34_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: regrips the sword; holy runes blaze up the blade. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — orbit.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_34_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: regrips the sword; holy runes blaze up the blade. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: orbit, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 35  (phase end · W)

### kf_35_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: enrages; swells open; spores spiral into a vortex. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — wide.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_35_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: enrages; swells open; spores spiral into a vortex. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: wide, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 36  (phase end · CU)

### kf_36_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the maw opens full; a spore-voice speaks (subtitle D4). Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — CU.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_36_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the maw opens full; a spore-voice speaks (subtitle D4). Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: CU, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 37  (phase end · W)

### kf_37_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: ignites the Pollen Nova; a spore supernova rises, drowning the marsh light. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — crane.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_37_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: ignites the Pollen Nova; a spore supernova rises, drowning the marsh light. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: crane, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 38  (phase end · M)

### kf_38_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: wing-flare, crossbows raised; glacier energy peaks. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — orbit.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_38_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: wing-flare, crossbows raised; glacier energy peaks. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: orbit, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 39  (phase end · M)

### kf_39_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg, az_ab6.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: plants his hands; the tattoo surges gold-to-white; golden wings bloom. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — rack.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_39_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg, az_ab6.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: plants his hands; the tattoo surges gold-to-white; golden wings bloom. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: rack, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 40  (phase end · W)

### kf_40_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: still-beat: the two hold under the rising spore-nova. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — held wide.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_40_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: still-beat: the two hold under the rising spore-nova. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: held wide, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 41  (phase end · M)

### kf_41_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab6.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: leaps in full Glacier Form; Immortal wings wide; snowstorm against the spores. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — aerial.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_41_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg, dd_ab6.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: leaps in full Glacier Form; Immortal wings wide; snowstorm against the spores. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: aerial, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 42  (phase end · M)

### kf_42_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: rises radiant; greatsword burning white-gold. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — tilt.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_42_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: rises radiant; greatsword burning white-gold. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: tilt, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 43  (phase end · W)

### kf_43_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Blizzard & Verdict: both launch together; a frost streak and a gold streak winding around each other. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — twin dive.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_43_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: COMBO Blizzard & Verdict: both launch together; a frost streak and a gold streak winding around each other. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: twin dive, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 44  (phase end · C)

### kf_44_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: fires Rime Beams and both crossbows at once; a violet-white lance punches through the bloom heart. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — slow-mo.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_44_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: fires Rime Beams and both crossbows at once; a violet-white lance punches through the bloom heart. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: slow-mo, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 45  (phase end · C)

### kf_45_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the final Verdict arc splits the bloom; light floods out. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — crash.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_45_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: the final Verdict arc splits the bloom; light floods out. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: crash, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 46  (phase end · W)

### kf_46_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the Pollen Nova collapses inward; light versus spore. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — wide pull.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_46_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the Pollen Nova collapses inward; light versus spore. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: wide pull, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 47  (phase end · I)

### kf_47_end.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the corpse-flower head cracks, folds shut, wilts. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — inset.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_47_start.png
**Attach:** boss_main.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: The Hollow Bloom: a colossal plant-vine aberration with a bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the ground grey. Action: the corpse-flower head cracks, folds shut, wilts. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: inset, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 48  (phase end · W)

### kf_48_end.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: spores settle like grey snow; two silhouettes over the purifying patch. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — wide.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_48_start.png
**Attach:** dd_face.jpg, set_plate.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference alongside a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: spores settle like grey snow; two silhouettes over the purifying patch. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: wide, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 49  (phase end · C)

### kf_49_end.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: exhales a wisp of frost; hair dims to the idle gradient; she almost smiles. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — CU.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_49_start.png
**Attach:** dd_face.jpg, dd_base.jpg, dd_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a woman demon hunter with her head completely BARE (no helmet, no hood, no bandana), glowing teal-to-blue hair waving weightlessly as if underwater, wearing the exact frost-arcane armor from the reference. Action: exhales a wisp of frost; hair dims to the idle gradient; she almost smiles. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: CU, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana


## SHOT 50  (phase end · W)

### kf_50_end.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: turns, greatsword over his shoulder; dawn breaks; the marsh water glows teal again. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: the end of the movement — dolly.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

### kf_50_start.png
**Attach:** az_face.jpg, az_base.jpg, az_weapon.jpg
**Prompt:**
Cinematic film still, photoreal: a retribution paladin in full plate with the helm from the reference (closed or open-face), a one-sided molten-gold rune-tattoo on his forearm, carrying the legendary two-handed greatsword, wearing the exact armor from the reference. Action: turns, greatsword over his shoulder; dawn breaks; the marsh water glows teal again. Environment: a dying fungal marsh at dusk: giant pale-blue mushroom towers, drifting luminous spore-mist, shallow teal-glowing water, and a spreading patch of grey corrupted ground with black veins around the boss. Foreground detail, midground hero, background giant fungi in spore-mist. 35mm anamorphic, real skin, film grain, dramatic dusk light. Moment: dolly, frozen at the opening beat.
**Negative:** duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin, helmet, hood on head, mask, bandana

## PART 2 — THE 116 VIDEO (CLIP) PROMPTS (p23_hb_k6c2_116.json, EXACT)

--- hb_s01_k6.mp4 | kf: kf_01_start.png | seed: 701
Fungal marsh at dusk, teal water, giant mushroom towers; DD (bare-headed demon hunter, glowing teal hair, frost-arcane armor) and AZ (full-plate paladin, greatsword) stand on a hummock at the corruption ring edge, spore-mist drifting BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, slow dolly-in, mist drifts. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s02_k6.mp4 | kf: kf_02_start.png | seed: 702
both heroes at the grey corruption edge; the blight visibly creeps a hand-width toward them, black veins pulsing BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, slow push-in, veins pulse. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s03_k6.mp4 | kf: kf_03_start.png | seed: 703
extreme close-up: DD bare hand cocks the twin crossbow; a crystalline frost-arrow materialises in the groove, frost spreading. Camera: INSERT shot, insert, macro, frost spreads. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s04_k6.mp4 | kf: kf_04_start.png | seed: 704
extreme close-up: DD glowing teal hair rolls in a slow weightless wave; neon teal brightens, nearby spores freeze and fall. Camera: INSERT shot, insert, hair drifts like water. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s05_k6.mp4 | kf: kf_05_start.png | seed: 705
extreme close-up: AZ gauntleted hand grips the greatsword hilt; the molten-gold rune-tattoo wakes along his forearm. Camera: INSERT shot, insert, light travels up the arm. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s06_k6.mp4 | kf: kf_06_start.png | seed: 706
the Hollow Bloom boss rises from the corrupted patch, spore-sacs inflating, then stands breathing, weight shifting with maw opening; spores fall upward BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, low rise, spores drift up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s07_k6.mp4 | kf: kf_07_start.png | seed: 707
a blight tendril coils tight then SNAPS forward like a whip-crack; marsh debris shakes BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: CLOSE-UP shot, whip crack, camera shake. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s08_k6.mp4 | kf: kf_08_start.png | seed: 708
DD raises one arm; a Glacial Aura frost-ring blooms outward, drifting spores crystallising to snow in the air BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 03 The Flank.. Camera: MEDIUM shot, aura bloom, camera pull-back. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s09_k6.mp4 | kf: kf_09_start.png | seed: 709
the whip-tendril slams the marsh near the heroes; a blight-furrow gouges the teal water, scorch and spray BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, whip impact, whip-pan. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s10_k6.mp4 | kf: kf_10_start.png | seed: 710
DD kicks off in a Frost Rush, becoming a comet of rime streaking low over the teal water BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 05 The Pursuit.. Camera: MEDIUM shot, sprint smear, whip-pan. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s11_k6.mp4 | kf: kf_11_start.png | seed: 711
DD fires BOTH crossbows; three crystalline frost-bolts streak out trailing ice BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, bolts, slow-mo to realtime. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s12_k6.mp4 | kf: kf_12_start.png | seed: 712
the frost-bolts slam a tendril; flash-freeze spreads, the vine goes brittle white and cracks BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 06 The Trap-Spring.. Camera: INSERT shot, impact, crash-zoom. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s13_k6.mp4 | kf: kf_13_start.png | seed: 713
AZ plants the greatsword tip into the ground; a gold shockwave cracks outward across the corrupted floor BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, ring shock, low hold. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s14_k6.mp4 | kf: kf_14_start.png | seed: 714
AZ swings Templar Verdict; a light-arc detonates on the Hollow Bloom, gold fire blooming BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: MEDIUM shot, swing and boom, orbit. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s15_k6.mp4 | kf: kf_15_start.png | seed: 715
the Hollow Bloom reels, its maw twisting; spore-sacs flare brighter in agitation BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: CLOSE-UP shot, recoil, push-in. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s16_k6.mp4 | kf: kf_16_start.png | seed: 716
the Bloom sweeps a tendril across the whole arena; DD and AZ vault in OPPOSITE directions to evade BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 04 The Split-Engagement.. Camera: WIDE shot, sweep and vault, cross-cut. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s17_k6.mp4 | kf: kf_17_start.png | seed: 717
DD flips backward and lands in a low crouch, frost-smoke pooling at her boots BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 05 The Pursuit.. Camera: MEDIUM shot, flip and land, whip-pan. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s18_k6.mp4 | kf: kf_18_start.png | seed: 718
DD eyes ignite; twin white-blue Rime Beam lances slash out across the marsh BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, beam and freeze, rack-focus. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s19_k6.mp4 | kf: kf_19_start.png | seed: 719
COMBO Freeze-and-Sunder: DD Rime Beams flash-freeze a tendril mid-swing, then AZ Verdict shatters it, golden shockwave ripping through the ice BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 02 The Tag-Out.. Camera: WIDE shot, beam then shatter, track. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s20_k6.mp4 | kf: kf_20_start.png | seed: 720
the Bloom staggers, its frozen vine fracturing; the maw opens in a silent roar BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: MEDIUM shot, recoil, push-in. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s21_k6.mp4 | kf: kf_21_start.png | seed: 721
the Bloom hunches; its spore-sacs rupture one after another, green spore-mushrooms blooming BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: WIDE shot, burst and sacs, wide. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s22_k6.mp4 | kf: kf_22_start.png | seed: 722
AZ raises the greatsword; a Blade of Justice light-blade summons above him, descending BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, blade descend, tilt-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s23_k6.mp4 | kf: kf_23_start.png | seed: 723
the light-blade plunges down; the Bloom staggers under a white pillar of holy light BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: MEDIUM shot, blade and pillar, pan. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s24_k6.mp4 | kf: kf_24_start.png | seed: 724
the Bloom slams its root-feet; Spore Rain begins, the sky dimming sickly green BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, rain and shock, crane-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s25_k6.mp4 | kf: kf_25_start.png | seed: 725
DD curls under her frost-wings; the Glacial Aura membrane shields her as spores hiss to snow on it BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 08 The Cover-Expose.. Camera: MEDIUM shot, shield and hiss, close. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s26_k6.mp4 | kf: kf_26_start.png | seed: 726
AZ strides forward through the spore rain; his holy light sheds the spores like water, ground flushing teal at his boots BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 05 The Pursuit.. Camera: MEDIUM shot, walk and light, dolly-back. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s27_k6.mp4 | kf: kf_27_start.png | seed: 727
the Bloom exhales a choking green spore-gout; a thick green column blasts outward BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 06 The Trap-Spring.. Camera: INSERT shot, gout, insert. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s28_k6.mp4 | kf: kf_28_start.png | seed: 728
GROUP: DD vaults OVER the spore-gout while AZ charges THROUGH its shadow, both converging on the Bloom BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 04 The Split-Engagement.. Camera: WIDE shot, split-action, wide. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s29_k6.mp4 | kf: kf_29_start.png | seed: 729
AZ stands breathing, weight shifting square; a Wake of Light white-gold cone scours the ground, blight receding in a wave before him BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 03 The Flank.. Camera: WIDE shot, cone and purge, sweep. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s30_k6.mp4 | kf: kf_30_start.png | seed: 730
DD winds up The Hunt; her frost-wings fold, snow coils concentrating around her BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, wind-up, push-in. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s31_k6.mp4 | kf: kf_31_start.png | seed: 731
DD executes The Hunt dive; a lance down crossbows-first, leaving a frozen trail, crater on impact BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 07 The Aerial Combo.. Camera: WIDE shot, dive and crater, aerial. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s32_k6.mp4 | kf: kf_32_start.png | seed: 732
the impact crater erupts; spore-sacs flicker, the Bloom forced down to one root-knee BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: MEDIUM shot, impact and kneel, shake. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s33_k6.mp4 | kf: kf_33_start.png | seed: 733
COMBO Hoarfrost Judgement: AZ marks the sac-cluster with an Execution Sentence rune; DD frost locks it; the rune detonates in a light-column through the ice BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 02 The Tag-Out.. Camera: CLOSE-UP shot, mark freeze boom, orbit. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s34_k6.mp4 | kf: kf_34_start.png | seed: 734
AZ regrips the greatsword two-handed; holy runes blaze up the blade length BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, grip and runes, orbit. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s35_k6.mp4 | kf: kf_35_start.png | seed: 735
the Bloom ENRAGES; it swells open, spores spiralling into a rising vortex BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: WIDE shot, swell and vortex, wide. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s36_k6.mp4 | kf: kf_36_start.png | seed: 736
the Bloom maw fills frame; it speaks (subtitle beat), spore-light pulsing in its throat BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, maw, close-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s37_k6.mp4 | kf: kf_37_start.png | seed: 737
the Bloom ignites the Pollen Nova; a spore supernova rises, marsh light drowning in green BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, nova, crane-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s38_k6.mp4 | kf: kf_38_start.png | seed: 738
DD wing-flares, both crossbows raised; glacier energy peaking around her, hair blazing teal BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 03 The Flank.. Camera: MEDIUM shot, flare and shift, orbit. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s39_k6.mp4 | kf: kf_39_start.png | seed: 739
AZ plants both hands; Avenging Wrath surges his tattoo gold-to-white, golden wings blooming at his back BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 03 The Flank.. Camera: MEDIUM shot, surge and wings, rack-focus. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s40_k6.mp4 | kf: kf_40_start.png | seed: 740
GROUP still-beat: DD and AZ hold side by side under the rising spore-nova, only spores moving BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, held wide, spores only. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s41_k6.mp4 | kf: kf_41_start.png | seed: 741
DD leaps in full Glacier Form, Immortal wings wide, a personal snowstorm blasting against the spores BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 07 The Aerial Combo.. Camera: MEDIUM shot, leap and form, aerial. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s42_k6.mp4 | kf: kf_42_start.png | seed: 742
AZ rises radiant, the greatsword burning white-gold, a halo of light at his back BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 03 The Flank.. Camera: MEDIUM shot, rise and halo, tilt-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s43_k6.mp4 | kf: kf_43_start.png | seed: 743
COMBO Blizzard and Verdict: both launch together, a frost streak and a gold streak winding around each other toward the Bloom BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 07 The Aerial Combo.. Camera: WIDE shot, twin dive, aerial. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s44_k6.mp4 | kf: kf_44_start.png | seed: 744
DD fires Rime Beams and both crossbows at once; a violet-white lance punches through the Bloom heart BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 12 The Killing Blow.. Camera: CLOSE-UP shot, beam and shot, slow-mo. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s45_k6.mp4 | kf: kf_45_start.png | seed: 745
AZ final Verdict arc; the greatsword splits the Bloom, holy light flooding out of the wound BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 12 The Killing Blow.. Camera: CLOSE-UP shot, slash and split, crash. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s46_k6.mp4 | kf: kf_46_start.png | seed: 746
the Pollen Nova collapses inward; light versus spore in a tightening sphere BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 11 The Collapse-Rally.. Camera: WIDE shot, collapse, wide pull. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s47_k6.mp4 | kf: kf_47_start.png | seed: 747
the corpse-flower head cracks and folds shut, wilting, spore-sacs going dark BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 06 The Trap-Spring.. Camera: INSERT shot, crown and fall, inset. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s48_k6.mp4 | kf: kf_48_start.png | seed: 748
spores ease down like grey snow; two silhouettes stand over the purifying patch BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 01 The Standoff.. Camera: WIDE shot, drift, wide. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s49_k6.mp4 | kf: kf_49_start.png | seed: 749
DD exhales a wisp of frost, her glowing hair dimming to an idle gradient; she almost smiles BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 09 The Disarm.. Camera: CLOSE-UP shot, breath and frost, close-up. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s50_k6.mp4 | kf: kf_50_start.png | seed: 750
AZ turns, greatsword over his shoulder; dawn breaks, the marsh water glowing teal again, purified BLOCKING (staging law 28): camera three-quarter side angle, low, never frontal to the fight; hero bodies oriented AT the boss, weapon line-of-action to the boss, sightlines converge on one point; no body faces the lens; depth planes read (midground heroes sharp, background boss threat visible, ground plane continuous). Staged as 05 The Pursuit.. Camera: WIDE shot, walk and light, dolly. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people, bystanders, morphing, drift. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s01_end_k6.mp4 | kf: kf_01_end.png | seed: 951
Aftermath micro-beat: the two armoured figures stand at the corruption ring edge; teal spore-mist keeps drifting past their legs. Camera: the dolly-in eases to a stop as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_cu1_k6.mp4 | kf: kf_CU1_dd_eye_ignite.jpg | seed: 951
INSERT, macro: the demon hunter one eye fills frame, the iris blooming teal to white-blue arcane fire, a Rime Beam lance leaking from the pupil, frost crystallising across the lower lashes, the rest of the face falling to darkness; frost-crack audio. Camera: extreme close-up, shallow focus, a slow rack from dark lash to the igniting iris.. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s02_end_k6.mp4 | kf: kf_02_end.png | seed: 952
Aftermath micro-beat: the two figures watch the grey creep halt a hand's width closer; the corruption veins pulse once and still. Camera: the slow push settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_cu2_k6.mp4 | kf: kf_CU2_az_rune_wake.jpg | seed: 952
INSERT, macro: the paladin plated forearm and gauntleted fist, the one-sided molten-gold rune-tattoo igniting rune by rune down the forearm like embers catching, light travelling under the skin and reflecting off the wet gauntlet, the greatsword grip entering at the fist; rune-ignition hum audio. Camera: extreme close-up, macro, a slow track along the waking runes.. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s03_end_k6.mp4 | kf: kf_03_end.png | seed: 953
Aftermath micro-beat: DD's hand holds the cocked crossbow; frost creeps a finger's width further along the groove, glittering. Camera: the insert holds, breathing as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_cu3_k6.mp4 | kf: kf_CU3_bloom_maw_pore.jpg | seed: 953
INSERT, macro: the Hollow Bloom maw-pore, the spiral pore-ring tightening, pollen-sac membranes straining translucent, sickly green bioluminescence pulsing brighter with each breath, spore-dust catching light at the rim; deep spore-breath audio. Camera: extreme close-up, macro, a slow push-in as the pore tightens.. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_s04_end_k6.mp4 | kf: kf_04_end.png | seed: 954
Aftermath micro-beat: DD's hair hangs in its weightless wave, neon teal steady; freshly-frozen spores keep falling past the glow. Camera: the insert holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s05_end_k6.mp4 | kf: kf_05_end.png | seed: 955
Aftermath micro-beat: AZ's gauntlet rests on the greatsword hilt; the rune-tattoo embers settle to a low gold simmer. Camera: the insert holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s06_end_k6.mp4 | kf: kf_06_end.png | seed: 956
Aftermath micro-beat: the Hollow Bloom stands tall, maw open; spores continue to fall upward around it. Camera: the low rise eases into a hold as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s07_end_k6.mp4 | kf: kf_07_end.png | seed: 957
Aftermath micro-beat: the snapped tendril recoils; sapped ichor beads at the crack, steam rising. Camera: the shake steadies as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s08_end_k6.mp4 | kf: kf_08_end.png | seed: 958
Aftermath micro-beat: DD holds the Glacial Aura ring; frost-dust keeps crystallising out of the air at its edge. Camera: the pull eases out as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s09_end_k6.mp4 | kf: kf_09_end.png | seed: 959
Aftermath micro-beat: the blight-furrow smoulders; teal water hisses where it touches the scorched gouge. Camera: the whip-pan settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s10_end_k6.mp4 | kf: kf_10_end.png | seed: 960
Aftermath micro-beat: the rime comet has passed; a trail of settling frost-smoke drifts over the water. Camera: the whip-pan eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s11_end_k6.mp4 | kf: kf_11_end.png | seed: 961
Aftermath micro-beat: the three frost-bolts have streaked away; frost-spark tracings hang a beat in the air, fading. Camera: slow-mo eases back to realtime as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s12_end_k6.mp4 | kf: kf_12_end.png | seed: 962
Aftermath micro-beat: the tendril patch holds brittle white; fine frost-dust sifts off the frozen vine. Camera: the crash-zoom breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s13_end_k6.mp4 | kf: kf_13_end.png | seed: 963
Aftermath micro-beat: AZ holds the planted greatsword; the gold shockwave ring fades into the marsh floor. Camera: the low hold continues as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s14_end_k6.mp4 | kf: kf_14_end.png | seed: 964
Aftermath micro-beat: the light arc has detonated on the bloom; gold embers sift down through the spore-mist. Camera: the orbit steadies as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s15_end_k6.mp4 | kf: kf_15_end.png | seed: 965
Aftermath micro-beat: the bloom reels, maw twisted; its spore-sacs flare, then hold brighter. Camera: the push-in eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s16_end_k6.mp4 | kf: kf_16_end.png | seed: 966
Aftermath micro-beat: both heroes land from the vault, opposite sides; frost-smoke and disturbed spores drift between them. Camera: the cross-cut settles to a wide hold as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s17_end_k6.mp4 | kf: kf_17_end.png | seed: 967
Aftermath micro-beat: DD holds the crouch, frost-smoke curling off her armour; the smoke thins. Camera: the whip-pan eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s18_end_k6.mp4 | kf: kf_18_end.png | seed: 968
Aftermath micro-beat: DD's eyes hold the ignited afterglow; twin thin lances of residual Rime Beam smoke rise. Camera: the rack settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s19_end_k6.mp4 | kf: kf_19_end.png | seed: 969
Aftermath micro-beat: the shattered frozen vine hangs broken; ice shards and gold motes sift through the gap. Camera: the track eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s20_end_k6.mp4 | kf: kf_20_end.png | seed: 970
Aftermath micro-beat: the bloom staggers, fractured vine shedding frost; the silent roar's breath disturbs the spore-mist. Camera: the push eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s21_end_k6.mp4 | kf: kf_21_end.png | seed: 971
Aftermath micro-beat: the bloom hunches, ruptured sacs deflating; pale sac-fluid drizzles off the petals. Camera: the wide hold breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s22_end_k6.mp4 | kf: kf_22_end.png | seed: 972
Aftermath micro-beat: AZ holds the sword raised; the summoned light-blade steadies above, humming. Camera: the tilt eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s23_end_k6.mp4 | kf: kf_23_end.png | seed: 973
Aftermath micro-beat: the bloom holds staggered under the white pillar; pillar-light particles sift down. Camera: the pan steadies as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s24_end_k6.mp4 | kf: kf_24_end.png | seed: 974
Aftermath micro-beat: the bloom holds its slammed stance; the first spore-rain streaks begin to fall, sky dimming green. Camera: the crane settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s25_end_k6.mp4 | kf: kf_25_end.png | seed: 975
Aftermath micro-beat: DD holds curled under the wing membrane; melt-water beads where spores hissed to snow. Camera: the close hold breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s26_end_k6.mp4 | kf: kf_26_end.png | seed: 976
Aftermath micro-beat: AZ holds his stride; holy light keeps shedding the spores like water, teal flushing at his boots. Camera: the dolly-back eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s27_end_k6.mp4 | kf: kf_27_end.png | seed: 977
Aftermath micro-beat: the bloom's maw holds open after the gout; the green column dissipates to drifting wisps. Camera: the insert holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s28_end_k6.mp4 | kf: kf_28_end.png | seed: 978
Aftermath micro-beat: DD holds the landing crouch past the gout, AZ holds mid-charge; their disturbed wake of spores drifts. Camera: the wide eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s29_end_k6.mp4 | kf: kf_29_end.png | seed: 979
Aftermath micro-beat: AZ stands square in the Wake of Light; the white-gold cone's purge wave recedes to a steady glow. Camera: the sweep settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s30_end_k6.mp4 | kf: kf_30_end.png | seed: 980
Aftermath micro-beat: DD holds the wound-up stance; coiled snow keeps spiralling inward around her. Camera: the push holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s31_end_k6.mp4 | kf: kf_31_end.png | seed: 981
Aftermath micro-beat: the lance has hit, crossbows first; the frozen trail keeps venting frost-steam. Camera: the aerial eases down as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s32_end_k6.mp4 | kf: kf_32_end.png | seed: 982
Aftermath micro-beat: the bloom holds on one root-knee, crater smoking; its spore-sacs flicker in sequence. Camera: the shake steadies as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s33_end_k6.mp4 | kf: kf_33_end.png | seed: 983
Aftermath micro-beat: the rune-marked sac-cluster holds locked in frost; the light column's afterglow sifts through the ice. Camera: the orbit eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s34_end_k6.mp4 | kf: kf_34_end.png | seed: 984
Aftermath micro-beat: AZ holds the regripped sword; holy runes blaze steady up the blade. Camera: the orbit holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s35_end_k6.mp4 | kf: kf_35_end.png | seed: 985
Aftermath micro-beat: the bloom holds swollen open; spiralling spores keep feeding the vortex. Camera: the wide breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s36_end_k6.mp4 | kf: kf_36_end.png | seed: 986
Aftermath micro-beat: the maw holds, subtitle spent; warm breath-mist pulses from the pore-ring. Camera: the CU holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s37_end_k6.mp4 | kf: kf_37_end.png | seed: 987
Aftermath micro-beat: the Pollen Nova holds risen; the marsh light keeps drowning greener. Camera: the crane eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s38_end_k6.mp4 | kf: kf_38_end.png | seed: 988
Aftermath micro-beat: DD holds the wing-flare, crossbows raised; glacier energy steadies to a clean glow. Camera: the orbit settles as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s39_end_k6.mp4 | kf: kf_39_end.png | seed: 989
Aftermath micro-beat: AZ holds, tattoo surged gold-to-white; the golden wings hold their bloom, light motes drifting. Camera: the rack eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s40_end_k6.mp4 | kf: kf_40_end.png | seed: 990
Aftermath micro-beat: the two hold under the rising nova; only spores move, spiralling up past them. Camera: the held wide breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s41_end_k6.mp4 | kf: kf_41_end.png | seed: 991
Aftermath micro-beat: DD holds the full Glacier Form mid-leap-turn; her snowstorm beats the spores back in a steady curtain. Camera: the aerial holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s42_end_k6.mp4 | kf: kf_42_end.png | seed: 992
Aftermath micro-beat: AZ holds risen, radiant; the white-gold greatsword halo steadies. Camera: the tilt eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s43_end_k6.mp4 | kf: kf_43_end.png | seed: 993
Aftermath micro-beat: the twin streaks have wound past; frost- and light-trails hang, slowly fading. Camera: the aerial eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s44_end_k6.mp4 | kf: kf_44_end.png | seed: 994
Aftermath micro-beat: the violet-white lance holds through the bloom's heart; afterglow pulses outward in slow rings. Camera: the slow-mo eases to realtime as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s45_end_k6.mp4 | kf: kf_45_end.png | seed: 995
Aftermath micro-beat: AZ holds the final arc, greatsword extended; light keeps flooding from the split. Camera: the crash eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s46_end_k6.mp4 | kf: kf_46_end.png | seed: 996
Aftermath micro-beat: the nova holds collapsing inward; light and spore wind past each other in the pull. Camera: the wide pull eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s47_end_k6.mp4 | kf: kf_47_end.png | seed: 997
Aftermath micro-beat: the corpse-flower head hangs cracked; the crown folds a degree further, wilting. Camera: the inset holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s48_end_k6.mp4 | kf: kf_48_end.png | seed: 998
Aftermath micro-beat: the two silhouettes stand over the purifying patch; grey spores keep settling like snow. Camera: the wide breathes as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s49_end_k6.mp4 | kf: kf_49_end.png | seed: 999
Aftermath micro-beat: DD holds, hair dimming to idle gradient; the frost wisp thins off her breath. Camera: the CU holds as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_s50_end_k6.mp4 | kf: kf_50_end.png | seed: 1000
Aftermath micro-beat: AZ holds the turn, greatsword over shoulder; dawn light spreads further across the teal-glowing water. Camera: the dolly eases as the motion dies. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. Residual motion keeps drifting - settling, pulsing, sifting - never a frozen hold.

--- hb_a1_k6.mp4 | kf: kf_A1_dd_clash.jpg | seed: 1100
Continuation of the frozen beat: the demon hunter holds with visible tension, breathing her skidded stop, crossbows tracking the tendril as it lunges in, frost-smoke streaming off her boots, weight shifting to spring aside. Camera: low wide, a slow push as the tendril enters. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_a2_k6.mp4 | kf: kf_A2_az_clash.jpg | seed: 1101
Continuation of the frozen beat: the paladin shoves forward to meet the same lunge, the greatsword rising through the first Verdict arc, gold light sweeping across the wet marsh. Camera: low wide, a rising tilt following the blade. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_b1_k6.mp4 | kf: kf_B1_dd_crossfire.jpg | seed: 1102
Continuation of the frozen beat: the demon hunter rides the vault over the scything tendril, twin crossbows spitting their frost-bolts down into the Bloom flank, ice-trails converging as she clears the arc. Camera: eye-level side-on, a whip-pan tracking the vault. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_b2_k6.mp4 | kf: kf_B2_az_crosssunder.jpg | seed: 1103
Continuation of the frozen beat: the paladin steps into the vacated space and the rising gold arc detonates on the frozen flank, the shockwave rippling the teal water out past his boots. Camera: eye-level side-on, a shake as the arc lands. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_c1_k6.mp4 | kf: kf_C1_dd_overwhelmed.jpg | seed: 1104
Continuation of the frozen beat: the demon hunter strains against the two pinning tendrils on her knee, the defensive crossbow trembling, frost-crack spidering further through the shallows, hair guttering. Camera: low close-up, a slow push on her set jaw. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_c2_k6.mp4 | kf: kf_C2_az_overwhelmed.jpg | seed: 1105
Continuation of the frozen beat: the paladin crashes through the mushroom-stand and rolls to a stop, spore-dust settling over his cracked helm, tattoo flaring back to life as he drags the greatsword up. Camera: low close-up, a hand-held ease down. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_d1_k6.mp4 | kf: kf_D1_dd_feint.jpg | seed: 1106
Continuation of the frozen beat: the demon hunter hangs limp a beat longer, then her free hand closes on the hidden frost-charge, eyes still locked on the Bloom eye-cluster, breath frosting. Camera: eye-level, an almost-still hold. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_d2_k6.mp4 | kf: kf_D2_az_reversal.jpg | seed: 1107
Continuation of the frozen beat: the paladin explodes up through the rising Verdict slash, the wound-line in the tendril glowing gold then black, water sheeting off his plate as he reaches full extension. Camera: low wide, a rising arc with the blade. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_e1_k6.mp4 | kf: kf_E1_both_mechanic.jpg | seed: 1108
Continuation of the frozen beat: back-to-back at centre, she slams the reload home as he raises the Execution-Sentence rune, the ring of tendrils tightening one coil closer, teal and gold pools flickering. Camera: high wide, a slow spiral down. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_e2_k6.mp4 | kf: kf_E2_dd_mechanic.jpg | seed: 1109
Continuation of the frozen beat: her bare hand slaps the frost-charge onto the tendril and ice blooms up its length, spore-sacs crystallising white in sequence, her crossbow already coming up on the next coil. Camera: macro insert, a fast rack with the ice bloom. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_e3_k6.mp4 | kf: kf_E3_az_mechanic.jpg | seed: 1110
Continuation of the frozen beat: his gauntleted fist drives the greatsword point into the frozen length and the rune ignites, racing up the ice toward the Bloom core, his stance set against the kick. Camera: macro insert, a push following the rune-light. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_f1_k6.mp4 | kf: kf_F1_dd_kill.jpg | seed: 1111
Continuation of the frozen beat: in full Glacier-Form she discharges the violet-white lance, beams and crossbows together, recoil bucking her shoulders, snowstorm streaming off the spread wings. Camera: eye-level close, a slow-mo drift on the discharge. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

--- hb_f2_k6.mp4 | kf: kf_F2_az_kill.jpg | seed: 1112
Continuation of the frozen beat: the paladin brings the final cleave down through the splitting crown, holy light flooding out as the corpse-flower opens, her lance crossing his frame. Camera: low wide, a crash down with the blade. One continuous phase, no cuts. No morphing, no drift, no new people; the named camera move is the only camera motion. Negative: duplicate face, extra limbs, text, watermark, cartoon, new people. The movement stays strong and continuous through the final frame - bodies in visible motion, nothing settles into a held pose.

## PART 3 — BOTH-SIDES FIGHT KEYFRAMES (45)

# 45 — Hollow Bloom BOTH-SIDES cinematic fight-expansion keyframe prompts (Grok-ready)
2026-11-15 · zero-GPU prep for K6-distilled render (engine busy elsewhere).
These are IMAGE-gen keyframe prompts (for Grok) that ADD both-perspective fight coverage to the
Hollow Bloom spec v3. Each has a DD-side and an AZ-side angle of the SAME beat = real both-sides
cinematic (shot/reverse-shot), per director D4 (full fight arc) + D5 (high-contrast register) + 44 rules.

RULES BAKED IN (44 + 43 + D-rules): no invented props; ONE phase per clip; body-form guards;
crowd 'no people'; full-body motion for emotional beats; D5 chiaroscuro header; D2 resolution directive;
image = photoreal still (no motion verbs in the still beyond the frozen instant); identity locked to the
armor/face/master sheets by reference, named ONCE.

REFERENCES TO ATTACH PER SHOT (upload to Grok once, attach as listed):
  DD side → dd_face_card.jpg, dd_armor_base.jpg, dd_master_sheet.jpg, dd_weapon.jpg
  AZ side → az_face_card.jpg, az_armor_base.jpg, az_master_sheet.jpg, az_weapon.jpg
  Boss  → hollowbloom_boss_design.jpg (the corpse-flower from the design pack)
  All   → set the marsh plate (teal water, giant fungi, corruption ring)

D5 REGISTER HEADER (prepend to EVERY prompt below verbatim):
"High-contrast cinematic action still: bold chiaroscuro lighting, hard rim-light carving the subject from
deep shadow, hot specular highlights on wet metal and ice, deep crushed blacks, 35mm anamorphic energy."

D2 RESOLUTION DIRECTIVE (append to EVERY prompt below verbatim):
"Generate at 2432×1408 minimum, ideally 3840×2160 (4K landscape)."

---

## BEAT A — THE CLASH OPENS (DD side + AZ side)

### A1 · DD-side · kf_A1_dd_clash.png
Attach: dd set. WIDE, low angle. The demon hunter (bare-headed, glowing teal-to-blue hair frozen
mid-sweep, exact frost-arcane armor from reference) has just SKIDDED to a stop on the teal water,
both crossbows RAISED and trained on the rising Hollow Bloom, frost-smoke curling off her boots,
her weight on the back foot ready to spring. The boss's tendril is mid-lunge toward her, filling the
right third of frame. No other people in frame. Boss = the corpse-flower design from reference.
Negative: duplicate face, extra limbs, extra crossbows, new people, morphing, text, watermark.

### A2 · AZ-side · kf_A2_az_clash.png
Attach: az set. WIDE, low angle (reverse of A1). The retribution paladin (full plate, helm open-face,
molten-gold rune-tattoo lit on his forearm, legendary greatsword held low in both hands, exact armor
from reference) plants his boots and SHOVES forward to meet the same lunging tendril, the blade
already rising for the first Verdict arc, gold light catching the wet marsh. No other people in frame.
Negative: duplicate face, extra limbs, extra swords, new people, morphing, text, watermark.

## BEAT B — CROSSFIRE / CROSS-SUNDER (DD side + AZ side)

### B1 · DD-side · kf_B1_dd_crossfire.png
Attach: dd set. MEDIUM, eye level, side-on. DD mid-vault OVER a scything tendril, cloak and teal hair
whipping, twin crossbows SPITTING three frost-bolts each down into the Bloom's flank, the bolts'
ice-trails converging, her body a clean diagonal of motion. The frozen furrow of her landing glistens
below. No other people in frame. One phase: mid-vault, firing.
Negative: duplicate face, extra limbs, extra bolts beyond six, new people, morphing, text, watermark.

### B2 · AZ-side · kf_B2_az_crosssunder.png
Attach: az set. MEDIUM, eye level, side-on (reverse of B1). AZ steps INTO the space DD just left,
greatsword describing a rising gold arc that DETONATES on the Bloom's frozen flank, the shockwave
rippling the teal water outward, his tattoo blazing, boots dug into the marsh. No other people in frame.
One phase: the strike landing.
Negative: duplicate face, extra limbs, extra swords, new people, morphing, text, watermark.

## BEAT C — OVERWHELMED (DD side + AZ side) — the near-death low

### C1 · DD-side · kf_C1_dd_overwhelmed.png
Attach: dd set. CLOSE-UP, low angle looking up. DD is DOWN on one knee in the shallows, one
crossbow knocked away, the other raised defensively as TWO tendrils pin her frost-wing against her
back, her teal hair flat and dimming, teeth bared, frost-crack spreading from her grounded knee —
the lowest point. Full-body strain, no gore. No other people in frame.
Negative: duplicate face, extra limbs, gore, blood, new people, morphing, text, watermark.

### C2 · AZ-side · kf_C2_az_overwhelmed.png
Attach: az set. CLOSE-UP, low angle looking up (reverse of C1). AZ is HURLED backward through a
shallow mushroom-stand, greatsword still clutched, helm cracked open to show the set jaw, gold
tattoo guttering, spore-dust exploding around the impact — the paladin's lowest point. Full-body,
no gore. No other people in frame.
Negative: duplicate face, extra limbs, gore, blood, new people, morphing, text, watermark.

## BEAT D — FEINT & REVERSAL (DD side + AZ side)

### D1 · DD-side · kf_D1_dd_feint.png
Attach: dd set. MEDIUM, eye level. The feint: DD goes LIMP under a pinning tendril as if finished —
body slack, crossbow dropped, hair dull — while her free hand closes silently on a hidden frost-charge
at her belt, eyes NOT closed but locked on the Bloom's eye-cluster. Held-breath stillness in a still.
No other people in frame.
Negative: duplicate face, extra limbs, new people, morphing, text, watermark.

### D2 · AZ-side · kf_D2_az_reversal.png
Attach: az set. WIDE, low angle. The reversal: AZ EXPLODES up from the marsh in a rising diagonal
Verdict slash that OPENS the Bloom's main tendril in a line of black ichor and gold fire, his whole
body the drawn bow of the strike, water sheeting off his plate, tattoo flaring white-gold. No gore
fountain; a clean wound-line. No other people in frame. One phase: the follow-through.
Negative: duplicate face, extra limbs, dismemberment, gore fountain, new people, morphing, text, watermark.

## BEAT E — THE MECHANIC (both together, then split to solo)

### E1 · BOTH · kf_E1_both_mechanic.png
Attach: dd + az + boss sets. WIDE, high angle looking down the arena. DD and AZ BACK-TO-BACK at
centre-frame inside a ring of converging tendrils — she reloading crossbows, he raising the
Execution-Sentence rune on the blade — the two heroes small against the closing Bloom, teal and
gold light pools holding the dark back. EXACTLY two people in frame.
Negative: duplicate face, extra limbs, a third person, merged bodies, new people, morphing, text, watermark.

### E2 · DD-side · kf_E2_dd_mechanic.png
Attach: dd set. INSERT, macro. DD's bare hand SLAPS the frost-charge onto a tendril; ice blooms
instantly across its length, crystallising spore-sacs to white, her other crossbow already coming up.
One phase: the plant-and-freeze. No other people in frame.
Negative: duplicate face, extra limbs, new people, morphing, text, watermark.

### E3 · AZ-side · kf_E3_az_mechanic.png
Attach: az set. INSERT, macro (reverse of E2). AZ's gauntleted fist DRIVES the greatsword point
into the frozen tendril's length, the Execution-Sentence rune igniting and racing up the ice toward
the Bloom's core. One phase: the mark landing. No other people in frame.
Negative: duplicate face, extra limbs, new people, morphing, text, watermark.

## BEAT F — THE KILL (both sides, the final exchange)

### F1 · DD-side · kf_F1_dd_kill.png
Attach: dd set. CLOSE-UP, eye level. DD, fully Glacier-Form, Immortal wings spread wide against the
spore-nova light, fires the Rime Beams AND both crossbows in one violet-white lance — the recoil
bucking her shoulders, snowstorm streaming off her wings, eyes blazing. One phase: the discharge.
No other people in frame.
Negative: duplicate face, extra limbs, extra muzzles, new people, morphing, text, watermark.

### F2 · AZ-side · kf_F2_az_kill.png
Attach: az set. WIDE, low angle (reverse of F1). AZ, Avenging-Wrath radiant, greatsword burning
white-gold at apex, brings the FINAL Verdict cleave down through the Bloom's crown as the corpse-flower
SPLITS and holy light floods out, the twin lance of DD's fire crossing his frame. EXACTLY two people
in frame. One phase: the cleave connecting.
Negative: duplicate face, extra limbs, a third person, severed-head gore, new people, morphing, text, watermark.

---
END OF EXPANSION PACK — 13 both-sides keyframes (A1-F2) covering D4 arc beats A-F in DD+AZ
perspective pairs. Render with K6 distilled (tools/vast/jobs/p23_hb_k6_50.json is the 50-shot base;
these 13 extend it to a 116-clip cut (103 spine + 13) for the both-sides cut). Fire only on the user's GO.
## PART 4 — CU TEXTURE INSERTS (45B)

# 45B — Hollow Bloom CU-texture insert keyframes (3 additional, Grok-ready)
2026-11-15 · from the whole-film cinematographic review (CU coverage was 1 shot; adding 3 texture beats).
Format matches 37/45 packs. D5 header + D2 resolution directive are baked into each prompt below.
These are IMAGE-gen keyframe prompts (for Grok). Attach references as listed per shot.

REFERENCES (upload to Grok once, attach as listed):
  DD shots → dd_face_card.jpg, dd_armor_base.jpg
  Boss shot → hollowbloom_boss_design.jpg (corpse-flower from the design pack)

---

### INSERT 1 · kf_CU1_dd_eye_ignite.png  (slots into Phase 1, before shot 18)
Attach: dd_face_card.jpg, dd_armor_base.jpg
EXTREME CLOSE-UP, one eye and the bridge of the nose only, filling frame. High-contrast cinematic action still:
bold chiaroscuro lighting, hard rim-light carving the subject from deep shadow, deep crushed blacks,
35mm anamorphic energy. The demon hunter's bare-headed face — glowing teal-to-blue hair falling across the
brow out of focus, real skin texture, film grain — with ONE EYE IGNITING: the iris blooming from natural
teal into white-blue arcane fire, a thin lance of Rime Beam light just beginning to leak from the pupil,
frost crystallising outward across the lower lashes. Everything else of the face falls to darkness.
Photoreal, macro detail, shallow depth of field. Generate at 2432×1408 minimum, ideally 3840×2160 (4K landscape).
Negative: second eye sharp, both eyes lit, duplicate face, helmet, hood, extra limbs, text, watermark.

### INSERT 2 · kf_CU2_az_rune_wake.png  (slots into Phase 2, before shot 22)
Attach: az_armor_base.jpg
EXTREME CLOSE-UP, a plated forearm and gauntleted fist filling frame. High-contrast cinematic action still:
bold chiaroscuro lighting, hot specular highlights on wet metal, deep crushed blacks, 35mm anamorphic
energy. The retribution paladin's forearm in full plate — the one-sided molten-gold rune-tattoo WAKING:
each rune igniting sequentially down the forearm like embers catching, ember-gold light travelling
under the skin and reflecting off the wet gauntlet, the greatsword grip just entering frame at the fist.
Macro detail, visible metal scratches, film grain. Photoreal. Generate at 2432×1408 minimum, ideally
3840×2160 (4K landscape).
Negative: tattoo on both arms, full-body view, face in frame, duplicate arm, extra fingers, text, watermark.

### INSERT 3 · kf_CU3_bloom_maw_pore.png  (slots into Phase 3, before shot 37)
Attach: hollowbloom_boss_design.jpg
EXTREME CLOSE-UP, the Hollow Bloom's maw-pore filling frame. High-contrast cinematic action still:
bold chiaroscuro lighting, deep crushed blacks, 35mm anamorphic energy. The corpse-flower boss's central
maw — the spiral pore-ring tightening, pollen-sac membranes straining translucent, sickly green bioluminescence
pulsing brighter from within with each breath, spore-dust catching the light at the rim, wet organic
texture, fibrous petal-edges curling at frame corners. Photoreal macro horror texture, film grain.
Generate at 2432×1408 minimum, ideally 3840×2160 (4K landscape).
Negative: human face in the maw, teeth instead of pore-ring, cute flower, cartoon, text, watermark.

---
END — 3 CU-texture inserts. Each renders as a ~2.5s K6 clip (native audio: frost-crack / rune-ignition
hum / deep spore-breath). They slot before shots 18, 22, 37 respectively.
