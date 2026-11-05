# 26 — Ловецот и Паладинот: Господарот на Пепелта (v2) — 2:20 cinematic boss fight

> DEFINE deliverable v2. Zero cost — authoring only, no rental committed.
> Replaces `25_..._SPEC.md` after user approvals and new design mandates.
> Follows `23_ERROR_REGISTER_AND_FIXES.md`, `24_CRITIQUE_REANALYSIS_REPORT.md` and the
> production doctrine: research-first, sparse narration/dialogue, visual-first, photoreal,
> first-last-frame (FLF), 46+ shots, Macedonian audio, landscape 1280×720 @ 24 fps.
> Compiled 2026-11-05.

---

## 0. Concept — the elemental triangle

Three forces collide in a charred gorge: **ICE** (the demon hunter), **FIRE** (the boss),
and **LIGHT** (the paladin). Cold and heat cancel and shatter; light purifies. The fight is
built on that triangle — ice locks, fire consumes, light judges — and on the two heroes
**fighting as a unit**: every phase ends in a tag-team combination, not a solo strike.

---

## 1. Cast (verified + new design mandates)

| Role | Identity | Weapon / kit | The look | Source |
|---|---|---|---|---|
| **Ловецот — Демоно-ловец (Demon Hunter)** | **DD** | dual infernal crossbows + Immortal wings | **COLD / ARCANE**: white-blue frost, violet-arcane core; hair glowing blue-to-teal neon, constantly waving as if underwater (the world is NOT underwater — the hair moves on its own, suspensor-magic) | `faces/dd_cards_final/` (9 enrolled) · identity_index → `dd` |
| **Азулон — Паладинот-осветник (Retribution Paladin)** | **Blagoj** (`Blagoj-shaven` `454a359e…`, alt `Blagoj-Base` `f5e2e917…`) | two-handed greatsword | bald, clean-shaven real face + **one-sided molten-gold rune-tattoo** (below); Avenging Wrath = summoned golden wings | `IDENTITY.md` · `CHARACTER_SYSTEM.md` |
| **Мал‘гарот — Господарот на Пепелта (boss)** | AI-default | molten whip-arm, forge-core, ember-lever form | fire/ash demon, 3 phase-forms, no real face | original (§3) |

**DD COLD/ARCANE identity (the defining look):**
- Palettes: white ice, glacier-cyan (arcane azure blue), neon teal; vapour breath; frost rimes;
  drifting snow-motes.
- Hair: glows blue→teal neon, perpetually weightless, flowing and waving exactly like hair under
  water, even in dry wind — a signature of his arcane-ice attunement. Never static, never clipped
  by physics; it must read as *enchanted*, not wet.
- Weapon glow: crossbow bolts are crystalline frost-arrows with an arcane-violet core; the bolt
  core colour follows the same state machine as the hair below.

**DD GLACIAL COLOUR SYSTEM (two-colour interchange + patterns):**
Two colours share his magic — **arcane azure blue** and **neon teal** — and they are never
static: they interchange and draw *patterns* as his power state changes.

| State | Hair colour behaviour | Magic pattern |
|---|---|---|
| **Idle** | blue→teal gradient along the strands (azure at the roots, teal at the tips); slow tide-shift, blue-dominant ⇄ teal-dominant | faint drifting snow-motes; no sigils |
| **Charging** | gradient brightens; alternating blue and teal bands ripple along the hair length like a travelling pulse | frost-rune sigils glow on skin/armour; breath becomes visible vapour |
| **Cast** | a single white-blue pulse travels root→tip, then settles back to gradient | the ability's sigil flares once; orbiting rune-rings |
| **Ultimate (Glacier Form)** | full white-blue bloom; teal sigil rings orbit the head | sheets of frost; Immortal wings blue-tipped; snowstorm |

This mirrors **Azulon's tattoo surge** so both heroes share one readable "power signature"
language: the paladin reads his skills from his skin, the demon hunter from his hair and runes.
Every ability description in §2 names its colour state.

**AZULON rune-tattoo (the defining look):**
- A single **one-sided** flowing calligraphic rune-maze: it crosses the eye, along the cheek,
  through the corner of the mouth, down the chin, onto the neck, then **wraps the skull to the
  back of the head**, pours down the spine, and splits out across the shoulders, arms and torso.
  Asymmetrical by design — the other side of the face stays clean for contrast.
- **Chosen color: molten gold** (matching his holy-light kit), normally a **subtle ember-gold**
  resting on the skin.
- **Surge behaviour:** with every ability, swing, block and spell, *specific segments* of the
  maze ignite from gold to blazing white-gold and flood with glowing energy, travelling along the
  lines; the whole tattoo never lights at once — only the pathways matching the technique surge,
  so the viewer can read the skill from his skin.

### §1b — Composable character-card system (adopted)

Adopted per user direction: a hero is no longer one flat image. Identity and look are **two
cards composed per shot**, because the past failures were always a costume/head leaking into a
face render or a face reference outvoting the prompt.

```
FACE CARD    identity, locked to the real person, centroid-gated (already exist)
SUIT CARD    look: full body, armor, weapons, hair-magic, wing/tattoo FX —
             deliberately WITHOUT an assigned head
COMPOSITION  per shot: Qwen-Image-Edit multi-reference =
             1 FACE card  +  1 SUIT card  (+ ULTIMATE variant)  +  scene
```

**Best-practice decision (as proposed and accepted):** SUIT cards are **hooded/helmed** — the
head is covered by the gear itself, eliminating both the random-head seam and the neck-fill
artefact. Hair and tattoo belong to the SUIT (they are gear), not the face.

**Card inventory to build (zero-cost renders before any video):**

```
DD FACE         faces/dd_cards_final/  (existing, 9 cards, enrolled)   → primary
DD SUIT base    "demon-hunter plate suit card"  hooded, head covered;
                dual infernal crossbows; Immortal frost wings (blue-tipped);
                under-water-waving blue-to-teal neon hair spilling from the hood
DD SUIT ult     "Glacier Form suit card"  hood down, full Glacier Form,
                Immortal wings wide, snowstorm, hair white-blue bloom + teal rings

AZULON FACE     Blagoj — `Blagoj-shaven` 454a359e… (clean-shaven default hero)
                or `Blagoj-Base` f5e2e917… (neutral 4-view). REMOTE ONLY:
                Higgsfield Cloud UUIDs, NOT on local disk. Must be retrieved
                and centroid-gated before any suit card or keyframe → primary
AZULON SUIT     "paladin plate suit card"  full helm (head covered);
  base          two-handed greatsword; one-sided molten-gold rune tattoo, subtle
                ember-gold on the exposed neck/arms
AZULON SUIT     "Avenging Wrath suit card"  helm OFF (he is bare-headed here
  ult           so the face + full tattoo read); rune maze surged white-gold;
                translucent golden wings; eyes white
```

**Composition rule (rigid):** each keyframe prompt names exactly **one FACE + one SUIT** (+ the
U1 ultimate suit where the beat calls for it) **+ one scene**. A shot must never accept a
second face reference; the face card is the only identity input, always primary.

**Face-visible shots:** DD keeps his hood on through the whole fight — his face is on the FACE
card only in the epilogue insert (#49, hood lowered). Azulon's face is visible **only** in his
Avenging Wrath ultimate (#39/#42/#45), where the helm-off variant is used; everywhere else he
is helmed. The boss remains face-free (AI-default).

---

## 2. Ability → VFX → action map (full list, cold/arcane + light)

**Demon Hunter (COLD/ARCANE — white-blue + wizard-violet):**
- `Fel Rush` → **Frost Rush** — a comet of rime; afterimage of broken ice; leaves a frozen streak
  on the ground; hair whips then reignites.
- `Immolation Aura` → **Glacial Aura** — a slowly-rotating ring of frost and arcane sigils around
  the body; embers die and turn to snow when they touch it.
- `Eye Beam` → **Rime Beams** — twin lances of white-blue light with violet cores from the eyes;
  whatever they rake **flash-freezes**: flame becomes ice sculpture.
- `Blade Dance` → **Frost Dance** — spinning crescent slashes that throw arcs of razor-ice and
  summon floating arcane sigils; camera orbits.
- `Metamorphosis` → **Glacier Form** — leap + explosive landing that sheets the ground in ice;
  demon form with huge Immortal wings of **blue-tipped frost**; snowstorm on landing.
- `The Hunt` → **The Hunt (Glacial Drift)** — aerial wind-up, then a lance-dive of crystalline
  cold; impact blooms a **frozen rose** of ice spikes, then shatters.

**Retribution Paladin (gold / white-holy):**
- `Blade of Justice` — light-blade summoned from above; falls in a white pillar.
- `Templar's Verdict` — radiant two-handed arc; detonates on contact in a golden shockwave.
- `Divine Storm` — spiral of golden blades radiating outward.
- `Wake of Ashes` — cone of white-hot divine flame that scours to ash.
- `Execution Sentence` — delayed rune-mark on the boss; detonates in a column of light.
- `Avenging Wrath` — the one-sided rune-tattoo ignites fully; translucent golden wings; eyes white.

**Elemental interactions (the visual story engine):**
- ICE × FIRE → shatter, steam, obsidian-glass; the boss *hates* cold: it cracks and slows.
- LIGHT × FIRE → purification; ash scatters, the forge-core dims.
- ICE × LIGHT → **combination techniques** (below).

---

## 3. The boss — Mal‘garot, Prince of Embers (unchanged design, re-lit

same fallen flame-demon: tall horned silhouette veiled in cinder, semi-liquid forge-core glowing
in the ribcage, one molten whip-arm, a crown of dead coals. Dominion over fire and ash — it
consumes; everything it touches dies into smoke and ember. **Its elemental opposite is cold.**

| Phase | Name (MK) | Form | Signature | Music/SFX |
|---|---|---|---|---|
| P1 | „Огнената круна“ | veiled demon, whip-speed | „Пепел-ками“ ash-whip | low tribal, whisper strings, ember hiss |
| P2 | „Срцето на печките“ | armour shed, forge-core exposed | „Црн дожд“ ember rain + obsidian gouts | rising brass, sub rumble, fire whoosh |
| P3 | „Пепел и кралство“ | ember-leviathan enrage | „Сонцето на пепелта“ ember supernova | restrained choir → stillness |

---

## 4. Full shot list — 52 shots, FLF, ~150 s (2:30), incl. ALL group + tag combos

Legend: size (W/M/C/CU/I) · START→END · mover/camera · t(s). 52 × ~2.9 s ≈ 150 s.

### Phase 0 — Arrival (~15 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 01 | W | charred gorge, ember wind, two figures on the ridge → they step forward | dolly-in; embers drift | 3.0 |
| 02 | W | both at cliff edge → footing cracks as weight shifts | slow push; heat shimmer | 2.5 |
| 03 | I | DD's hand cocks a crossbow → a **frost-arrow** crystallises in the groove | insert; frost spreads | 2.5 |
| 04 | I | DD's hair rolls in a slow, weightless wave → its neon teal brightens | insert; hair drifts like water | 2.5 |
| 05 | I | Paladin's gauntlet grips the hilt → rune-tattoo ember-gold wakes along wrist | insert; light travels | 2.5 |
| 06 | W | boss unfolds from the ash → stands, crown of coals | low rise; ash falls upward | 3.0 |

### Phase 1 — „Огнената круна“ (~42 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 07 | C | whip-arm coils → snaps | whip crack; shake | 2.5 |
| 08 | M | DD raises an arm (Glacial Aura) → frost ring blooms | aura; camera pull | 2.5 |
| 09 | W | whip hits near → fire-furrow gouges ground | whip+scorch; whip-pan | 3.0 |
| 10 | M | DD kicks off (Frost Rush) → comet of rime, ice streak behind | sprint smear; whip-pan | 2.5 |
| 11 | C | DD fires crossbows → three crystalline frost-bolts streaking | bolts; slow-mo→realtime | 2.5 |
| 12 | I | bolts hit cloak → **flash-freeze** patch, ember spray curdles to snow | impact; crash-zoom | 2.5 |
| 13 | W | Paladin plants greatsword tip → gold shockwave cracks floor | ring; low hold | 2.5 |
| 14 | M | Paladin swings Templar's Verdict → light arc detonates on boss | swing+boom; orbit | 3.0 |
| 15 | C | boss reels, mask cracks → forge-core flares | recoil; push-in | 2.5 |
| 16 | W | **GROUP** — boss sweeps ash-whip across the arena → both heroes vault in opposite directions | sweep+vault; cross-cut | 3.0 |
| 17 | M | DD flips back (Vengeful Retreat) → lands in crouch, frost-smoke | flip+land; whip-pan | 2.5 |
| 18 | C | DD's eyes ignite (Rime Beams) → twin white-blue lances slash out | beam+freeze; rack | 3.0 |
| 19 | W | **COMBO #1 — Freeze-and-Sunder**: DD's Rime Beams flash-freeze the whip-arm mid-swing → Paladin's Verdict shatters it, golden shockwave through ice | beam→shatter; track | 3.5 |
| 20 | M | boss staggers, frozen arm fracturing → it roars | recoil; push | 2.5 |

### Phase 2 — „Срцето на печките“ (~46 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 21 | W | boss sheds armour → forge-core exposed, obsidian shards rain | explode+shards; wide | 3.0 |
| 22 | C | Paladin raises sword (Blade of Justice) → light-blade summons above | blade descend; tilt | 2.5 |
| 23 | M | light-blade plunges → boss staggers, white pillar | blade+pillar; pan | 3.0 |
| 24 | W | boss slams ground → „Црн дожд“ ember rain begins | rain+shock; crane | 3.0 |
| 25 | M | DD curls under wings (Glacial Aura) → embers hiss to snow on the membrane | shield+hiss; close | 2.5 |
| 26 | M | Paladin strides through ember rain → light sheds it like water | walk+light; dolly-back | 3.0 |
| 27 | I | boss breathes obsidian gouts → column of flame | flame; insert | 2.5 |
| 28 | W | **GROUP** — DD vaults over the gout while Paladin charges through its shadow | split-action; wide | 3.0 |
| 29 | W | Paladin stands square (Wake of Ashes) → white flame cone scours ground | cone+ash; sweep | 3.0 |
| 30 | C | DD winds up (The Hunt) → wings fold, snow coils concentrate | wind-up; push | 3.0 |
| 31 | W | The Hunt dive → DD lances down, crossbows first, frozen trail | dive+crater; aerial | 3.5 |
| 32 | M | impact crater → core flickers, boss forced to one knee | impact+kneel; shake | 3.0 |
| 33 | C | **COMBO #2 — Hoarfrost Judgement**: Paladin marks the core (Execution Sentence rune) → DD's frost locks it → the rune detonates in a light column through the ice | mark→freeze→boom; orbit | 3.5 |
| 34 | C | Paladin regrips sword → holy runes blaze up the blade | grip+runes; orbit | 2.5 |

### Phase 3 — „Пепел и кралство“ (~42 s)

| # | Sz | START → END | Mover/camera | t |
|---|---|---|---|---|
| 35 | W | boss enrage → swells, embers spiral into vortex | swell+vortex; wide | 3.0 |
| 36 | C | boss voice (subtitle) → „Од пепел сте — и во пепел ќе ве вратам.“ | lips/mask; CU | 2.5 |
| 37 | W | boss ignites „Сонцето на пепелта“ → supernova of embers rises | nova; crane | 3.5 |
| 38 | M | DD wing-flare, crossbows raised → glacier-form energy peaks | flare+shift; orbit | 3.0 |
| 39 | M | Paladin plants hands (Avenging Wrath) → tattoo **surges** gold→white, golden wings bloom | surge+wings; rack | 3.0 |
| 40 | W | **GROUP still-beat** — the two hold, ember-nova above | held wide; embers only | 2.5 |
| 41 | M | DD leaps — full Glacier Form, Immortal wings wide, snowstorm | leap+form; aerial | 3.0 |
| 42 | M | Paladin rises — radiant, greatsword burning white-gold | rise+halo; tilt | 3.0 |
| 43 | W | **COMBO #3 — Blizzard & Verdict**: both launch together at the core — fel-frost streak and gold streak winding around each other | twin dive; aerial | 3.0 |
| 44 | C | DD fires Rime Beams + all crossbows at once → violet-white lance through the heart | beam+shot; slow-mo | 3.0 |
| 45 | C | Paladin's final Verdict arc → core splits, light floods out | slash+split; crash | 3.0 |
| 46 | W | supernova collapses inward — light versus ember | collapse; wide pull | 3.0 |
| 47 | I | crown of dead coals cracks → falls | crown+fall; inset | 2.5 |
| 48 | W | ash settles — two silhouettes over the extinguished core | ash drift; wide | 3.0 |
| 49 | C | DD lowers hood, embers gutter → he exhales a wisp of frost | breath+frost; CU | 3.0 |
| 50 | W | Paladin turns, greatsword over shoulder → dawn light pierces ash | walk+light; dolly | 3.0 |

**Continuity spine:** core state (veiled→exposed→supernova→extinguished); whip-arm
(intact→frozen→shattered in #19, regrown molten in P2 off-screen, then blown away in P3);
DD hair never still; Azulon tattoo surges per ability; power states (dormant→partial→ultimate).

**Group & tag coverage map (what the user asked for):**
- **All three in frame:** #01, #02, #06, #09, #13, #16, #21, #24, #28, #35, #37, #40, #43, #46, #48, #50.
- **DD solo:** #03, #04, #08, #10, #11, #12, #17, #18, #25, #30, #31, #38, #41, #44, #49.
- **Paladin solo:** #05, #14, #15, #22, #23, #26, #29, #33, #34, #39, #42, #45.
- **Tag combinations:** #19 (Freeze-and-Sunder), #33 (Hoarfrost Judgement), #43–#45 (Blizzard & Verdict).

---

## 5. Narration & dialogue (Macedonian — more than 2 lines now)

A boss fight is visual; voices are punctuation, not exposition. Seven lines total:

| # | Speaker | Line (MK) | Moment |
|---|---|---|---|
| D1 | Boss | „Дојдовте да изгорите, како сите пред вас.“ | P1, after #07 first whip crack |
| D2 | Boss | „Мразот само ја прави пепелта поубава.“ | P2, after #19 freeze-and-sunder, mocking the cold |
| D3 | Paladin | „Светлината не се гаси.“ | P2, #26, under breath |
| D4 | Boss | „Од пепел сте — и во пепел ќе ве вратам!“ | P3, #36, the taunt that triggers the nova |
| D5 | DD | „Замрзни.“ | P3, #44, single cold word at the killing strike |
| D6 | Paladin | „Суди.“ | P3, #45, the Verdict |
| D7 | DD (epilogue) | „Пепелта е само снег што не стигнал на време.“ | #49, whispered |

No narrator. Optional title card: „Исечени во пепелта“ before #01 (confirm in §10).

---

## 6. Spatial audio + music (restrained)

```
SFX (procedural, spatial): ember hiss / ash-wind bed (L-R drift); whip CRACK (P1);
  ice-shatter CRACKLE whenever fire is flash-frozen; eye/Rime-beam THRUM + freeze
  SIZZLE; crossbow frost-bolt WHINE; greatsword RING + holy HUM; tattoo surge
  electric HISS; implosion SUCK + sub; wing-lift WHOOSH + landing THUD.
MUSIC: P1 low tribal + string whisper, silence-lean; P2 rising brass + sub-rumble,
  one hit per boss slam; P3 short choir swell → STILLNESS at the killing blow.
Rule: score never masks voice or SFX.
```

---

## 7. Pipeline (research-first; zero cost until user approves price)

```
P0 RESEARCH    ✓ WoW ability sets (Wowhead/Icy Veins/Method); tattoo + cold/VFX refs;
               identity cards verified
P1 ENHANCE     ✓ 52-shot action spine incl. group frames + 3 tag combos
P2 SPLIT       ✓ narration ≠ dialogue: 7 lines, no narrator
P3 SCRIPT      ✓ §4–§6
P4 STORYBOARD  every shot = START + END (single-reference jobs rejected at build)
P5 PROMPTS     Qwen-Image keyframes + Wan FLF video prompts; naming:
               26_dhpf_kf_P{phase}_{shot:02d}_{start|end}.png
               26_dhpf_vid_P{phase}_{shot:02d}.json
P6 PRICE CHECK live Vast scan + itemized estimate + per-run approval
P7 PROOF       1 scene (3–4 FLF shots, one ability/one combo) for user judgement
P8 FULL RUN    approved shots → copy+sha256+ffprobe → local assembly → teardown
               (instances AND volumes, bill-stop confirmed)
```

**Prompt templates (model-specific):**

```text
[KEYFRAME — Qwen-Image @1280x720]
{IDENTITY LOCK verbatim}. {DD: glowing blue-to-teal weightless under-water-waving hair,
frost-arcane}. {AZULON: bald, one-sided molten-gold rune-tattoo maze, subtle glow}.
{costume + weapon}. {full-body action}. {env, light, depth}. {fore/mid/background}.
Photorealistic cinematic film still, 35mm anamorphic, real skin, film grain.
Negative: duplicate/extra face, extra limbs, text, watermark, cartoon, illustration,
cel-shaded, 3d render, plastic skin.

[VIDEO — Wan FLF --imagefile START --endimage END]
First frame shows {EXACT start content}. Then {ONE mover} {direction + character}.
Camera: {size + move}. Continuity: {fixed}. Light/mood: {palette + grade}.
Signature VFX: {ability} = {ice/gold surge description}.
```

---

## 8. Acceptance criteria (testable)

1. **Shots** = 52 (≥40), durations 2.5–3.5 s → **≥2:20 runtime** (can push to ~3:00).
2. **References per shot** ≥ 2 (start+end); single-reference jobs rejected.
3. **Camera grammar** in every video prompt.
4. **Motion floor** via frame-difference — no held stills.
5. **Ability legibility** — each signature matches its VFX (§2) incl. surge pattern for Azulon.
6. **Ice/light/fire triangle** reads visually: cold shatters, light purifies.
7. **Group + combo coverage** — ≥1 series where all three fight together + 3 tag combos verified.
8. **Identity gates** — DD ≥0.50 vs dd centroid; Paladin ≥0.50 vs Blagoj centroid; boss = 0 faces.
9. **Visual-first** — mute audio, the fight still reads.
10. **Audio** — spatial SFX + restrained score; Macedonian-only voices; 7 lines.
11. **DD hair** waves like underwater in every DD shot; **Azulon tattoo** surges per ability.
12. **Style kit** photoreal; validated against researched references only (no self-deliverables).

---

## 9. Cost (budget not a problem — but per-run approval and itemized estimate still apply)

```
Keyframes  ~104 (52×2) Qwen-Image            ≈ $3–7
Video      52 FLF clips, Wan 2.2             ≈ $3–6
Audio      procedural SFX + OmniVoice/MOSS   free/reuse
TOTAL      ≈ $6–13 (re-priced at P6; SEQUENTIAL, never parallel)
```

The no-spend-without-approval rule is unchanged; budget flexibility does not remove the itemized
estimate gate or the proof-scene gate.

---

## 10. Open questions

1. **Paladin tattoo colour** — molten gold is my choice (matches holy kit). Confirm or
   change (e.g. azure, crimson)?
2. **DD hair** — blue-to-teal confirmed (vs pure ice-white)?
3. **Title card** — include „Исечени во пепелта“?
4. **Proof scene** — proceed with one 3–4-shot FLF proof before the full run?
5. **Runtime** — lock ~2:30 (52 shots) or scale to ~3:00 (60+ shots)?

---

*DEFINE-ONLY. No GPU rented; nothing spends until boss/tattoo/hair/title/proof are
confirmed and an itemized P6 estimate is approved per run.*
