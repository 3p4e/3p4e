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
