# 25 — Демоно-ловец и паладинот: борба со Господарот на Пепелта (2+ мин cinematic boss fight)

> DEFINE deliverable. Zero cost — authoring only, no rental committed.
> Everything here follows `23_ERROR_REGISTER_AND_FIXES.md`, `24_CRITIQUE_REANALYSIS_REPORT.md`
> and the production doctrine: research-first, narration/dialogue as a separate sparse layer,
> visual-first, photoreal, first-last-frame (FLF) construction, 40–60 shots, Macedonian audio.
> Compiled 2026-11-05.

---

## 0. One-line concept

**„Ловецот и паладинот“** — ловец на демони (DD) и паладин-осветник (Азулон) заедно го
ловат и го соборуваат Ма́л‘гарот, Господарот на Пепелта, во три фази на ескалација —
брзина и фел-оган против светлина и правда — снимен со фотореален, кинески
boss-fight ритам на вештини: секој напад има име, визуелен потпис и последица.

---

## 1. Cast (verified from repo, not assumed)

| Role | Identity | Weapon / kit | Source (verified) |
|---|---|---|---|
| **Илли́дан / Ловецот (Demon Hunter)** | **DD** | Infernal dual crossbows + top-tier Immortal demon wings (Diablo Immortal style) | `faces/dd_cards_final/` (9 cards, enrolled) · `faces/identity_index.json` → `dd` |
| **Арион / Паладинот-осветник (Retribution Paladin)** | **Azulon-Master** `5b059323…` | two-handed greatsword; awakened Selûne tattoo = „Avenging Wrath“ | `higgsfield/AZULON_CANON.md` · `CHARACTER_SYSTEM.md` |
| **Мал‘гарот (boss)** | AI-default demon | phase-forms, no real face | original design, §3 |

**Rigid identity rules (from canon):**
- Demon Hunter face = DD real card only. No KORY (she is a *different* persona; this hero is DD).
- Paladin = Azulon-Master: pointed ears, Selûne fine-line tattoo; dormant + awakened (radiant) states.
- Boss and minions are AI-default creatures — never carry a real face.

---

## 2. Research basis (what was read, not guessed)

### 2.1 WoW ability sets (verified)

**Havoc Demon Hunter** (Wowhead / Icy Veins / Method, patch 12.1.5):
Fel Rush, Immolation Aura, Eye Beam, Blade Dance, Chaos Strike, Vengeful Retreat,
Metamorphosis, The Hunt.

**Retribution Paladin** (Icy Veins / Wowhead / Method, patch 12.1.5):
Blade of Justice, Judgment, Templar's Verdict, Divine Storm, Wake of Ashes,
Execution Sentence, Hammer of Light / Final Verdict, Avenging Wrath, Divine Toll.

### 2.2 Cinematic references (structure, not copy)

- **Frozen Throne — Illidan vs Arthas**: a duel of two power-signatures; wings against
  rune-magic; each strike shifts advantage. Lesson: *statechange per exchange*.
- **Blizzard cinematic grammar**: establishing wide → character silhouettes → close reaction
  → action cut on impact → aftermath wide. Camera never idles.
- **Wuxia / Chinese boss-fight style**: named techniques, a visible energy wavefront per hit,
  power shown through environment damage (rock cleaved, shockwave rings), slow-motion
  *inside* the strike then real-time impact.

### 2.3 Ability → VFX → on-screen action map (the core of “explicit skill”)

**Demon Hunter (fel-green / violet spectral):**
- `Fel Rush` — green streak; afterimage trail; linear dash punch.
- `Immolation Aura` — ring of emerald flame hugging the body, world-burning heat shimmer.
- `Eye Beam` — twin violet-fel lances from the eyes; ground scorch line; directional, channelled.
- `Blade Dance` — spinning circular slashes; camera orbits; sigils spinning mid-air.
- `Metamorphosis` — leap + explosive landing, demonic form, huge Immortal wings unfurl (fel torches).
- `The Hunt` — wind-up, then a devastating aerial lance-dive; impact crater + shockwave.

**Retribution Paladin (gold / white-holy):**
- `Blade of Justice` — summon a light-blade strike from above; blade falls, light pillar.
- `Templar's Verdict` — radiant arc swing that detonates on contact; golden shockwave.
- `Divine Storm` — spiral of golden blades radiating outward; crowd-clearing.
- `Wake of Ashes` — cone of white-hot divine flame scouring the ground to ash.
- `Execution Sentence` — a delayed rune-mark on the boss that detonates in a column of light.
- `Avenging Wrath` — awakened tattoo ignites; translucent golden wings; eyes glow white.

**Colour discipline (contrast the two heroes):**
- Demon Hunter = fel-green + violet + black leather; heat-haze; embers.
- Paladin = gold + white + steel; cool blue rim; light shafts.
- Boss = bruise-purple + cinder-orange + ash-grey; smoke; ember flecks.

---

## 3. The boss — Mal‘garot, Prince of Embers (original design)

A fallen Naar-adjacent flame-demon: a tall horned silhouette veiled in cinder and
brazier-ash, a semi-liquid forge-core glowing in its ribcage, one molten whip-arm, and a
crown of dead coals. Its power is **dominion over fire and ash** — it does not hit, it
*consumes*; everything it touches dies into smoke and ember.

**Three phases (Chinese boss-fight escalation):**

| Phase | Name (MK) | Form | Signature move | Music/SFX |
|---|---|---|---|---|
| P1 | „Огнената круна“ | veiled demon, speed + whip | **„Пепел-ками“** (ash-whip) — molten lash that leaves a burning furrow | low tribal percussion, whisper-tier strings, ember hiss |
| P2 | „Срцето на печките“ | armour sheds, forge-core exposed, area denial | **„Оган-сура“ / „Црн дожд“** — summons ember rain + obsidian gouts | rising brass, spatial fire, sub rumble |
| P3 | „Пепел и кралство“ | final enrage, full ember-leviathan | **„Сонцето на пепелта“** — rising supernova of embers, must be broken by both ultimates together | restrained choir swell → cut to stillness |

Boss dialogue is scarce and mocking (§5) — power shown, not described.

---

## 4. Full shot list — 46 shots, FLF, ~140 s, landscape 1280×720 @ 24 fps

Legend: **size** (W wide / M medium / C close-up / CU close / I insert) · **start→end**
keyframe states · **mover** = what actually animates between frames.
Durations 2.5–4 s for pacing; 46 shots × ~3 s ≈ 140 s (2:20).

### Phase 0 — Arrival & preamble (~14 s)

| # | Size | Start → End keyframe | Mover / camera | t |
|---|---|---|---|---|
| 01 | W | charred gorge, ember wind, two shadows on the ridge → same, they step forward | wide dolly-in; embers drift | 3.0 |
| 02 | W | two figures full-body at cliff edge → their footing cracks as weight shifts | slow push; heat shimmer | 2.5 |
| 03 | I | DD's hand cocking a crossbow bolt (fel charge) → bolt ignites | insert; flame licks | 2.5 |
| 04 | I | Paladin's gauntlet tightening on greatsword hilt → runes wake gold | insert; light travels wrist→blade | 2.5 |
| 05 | W | the boss unfolds from the ash beneath → stands, crown of coals | low-angle rise; ash falls upward | 3.5 |

### Phase 1 — „Огнената круна“ (~42 s)

| # | Size | Start → End keyframe | Mover / camera | t |
|---|---|---|---|---|
| 06 | C | boss's molten whip-arm coils → it snaps forward | whip crack; frame shake | 2.5 |
| 07 | M | DD raises an arm (Immolation Aura) → emerald flame ring flares around him | aura bloom; camera pulls | 2.5 |
| 08 | W | whip lash hits near them → furrow of fire gouges the ground | whip + scorch line; whip-pan | 3.0 |
| 09 | M | DD kicks off (Fel Rush) → green afterimage darts across | sprint smear; whip-pan cut | 2.5 |
| 10 | C | DD fires infernal crossbow volley → three fel bolts streak | bolts fly; slow-mo then realtime | 2.5 |
| 11 | I | bolt impacts on boss's cloak → ember spray bursts | impact + embers; crash-zoom | 2.5 |
| 12 | W | Paladin plants greatsword tip in the earth → gold shockwave cracks the floor | shockwave ring; low hold | 2.5 |
| 13 | M | Paladin swings two-handed arc (Templar's Verdict) → light arc detonates | swing + detonation; orbit | 3.0 |
| 14 | C | boss reels, mask cracks → forge-core flares brighter | recoil; push-in | 2.5 |
| 15 | W | boss sweeps ash-whip across the arena → both heroes vault clear | sweep + vault; cross-cut | 3.0 |
| 16 | M | DD flips backward (Vengeful Retreat) → lands in a crouch, crossbows smoking | flip + land; whip-pan | 2.5 |
| 17 | C | DD's eyes ignite (Eye Beam wind-up) → twin fel lances slash out | beam + scorch; rack-focus | 3.0 |
| 18 | W | Eye Beam rakes the boss → ground scorch line cuts through ash | beam sweeps; track | 3.0 |

### Phase 2 — „Срцето на печките“ (~44 s)

| # | Size | Start → End keyframe | Mover / camera | t |
|---|---|---|---|---|
| 19 | W | boss armour shatters off → forge-core exposed, obsidian shards rain | armour explode + shards; wide push | 3.0 |
| 20 | C | Paladin raises sword to the sky (Blade of Justice) → light-blade summons above | blade descends; tilt-up | 2.5 |
| 21 | M | summoned light-blade plunges → boss staggers, white pillar | blade + pillar; jarring pan | 3.0 |
| 22 | W | boss slams the ground → ember rain („Црн дожд“) starts falling | rain + shockwave; crane-up | 3.0 |
| 23 | M | DD curls under his wings (Immolation) → embers hiss off the wing membrane | shield + hiss; close | 2.5 |
| 24 | M | Paladin strides into the ember rain → divine light sheds it like water | walk + light; dolly-back | 3.0 |
| 25 | I | boss breathes obsidian gouts (flame) → column turns to glass mid-air | flame + solidification; insert | 2.5 |
| 26 | W | Paladin stands square (Wake of Ashes) → cone of white flame scours the ground | cone + ash; sweeping track | 3.0 |
| 27 | C | DD points (The Hunt wind-up) → wings fold, fel coils concentrate | wind-up; slow push | 3.0 |
| 28 | W | The Hunt dive → DD lances down through the smoke, crossbows first | dive + crater; aerial follow | 3.5 |
| 29 | M | impact crater → boss's core flickers, forced to one knee | impact + kneel; low shake | 3.0 |
| 30 | C | Paladin boots forward (sword switch-grip) → holy runes blaze up the blade | grip + runes; orbit | 2.5 |

### Phase 3 — „Пепел и кралство“ (~40 s)

| # | Size | Start → End keyframe | Mover / camera | t |
|---|---|---|---|---|
| 31 | W | boss begins final enrage → body swells, embers spiral into a vortex | swell + vortex; wide | 3.0 |
| 32 | C | boss's voice (subtitle) → „Од пепел сте и во пепел ќе ве вратам.“ | lips/mask only; CU | 2.5 |
| 33 | W | boss ignites „Сонцето на пепелта“ → rising supernova of embers | nova + rising heat; crane | 3.5 |
| 34 | M | DD reacts — wing-flare, crossbows raised → fel energy peaks (Metamorphosis) | flare + form-shift; orbit | 3.0 |
| 35 | M | Paladin plants both hands (Avenging Wrath) → awakened tattoo ignites, golden wings bloom | tattoo + wings; rack | 3.0 |
| 36 | W | the two share a beat of stillness → ember-nova above them | held wide; only embers move | 2.5 |
| 37 | M | DD leaps — full Metamorphosis, Immortal wings wide, demon form | leap + transform; aerial | 3.0 |
| 38 | M | Paladin rises — radiant, greatsword burning white-gold | rise + halo; tilt-up | 3.0 |
| 39 | W | both launch together at the core → twin streaks (fel green + gold) | twin dive; aerial follow | 3.0 |
| 40 | C | DD's Eye Beam + crossbows all fire at once → violet lance through the heart | beam + shot; slow-mo | 3.0 |
| 41 | C | Paladin's final Verdict arc → the core splits, light floods out | slash + split; crash | 3.0 |
| 42 | W | the supernova collapses inward → implosion, light versus ember | collapse; wide pull | 3.0 |
| 43 | I | the boss's crown of dead coals cracks → falls to the ground | crown + fall; inset | 2.5 |
| 44 | W | ash settles — two silhouettes standing over the extinguished core | ash drift; slow wide | 3.0 |
| 45 | C | DD lowers his hood, embers gutter around him → he exhales smoke | breath + embers; CU | 3.0 |
| 46 | W | Paladin turns, greatsword over shoulder → dawn light pierces the ash | walk + light; closing dolly | 3.5 |

**Continuity (IN/OUT) spine:** boss's core state (veiled → exposed → supernova →
extinguished), whip-arm (intact → cracked → shattered off-screen in P3 between shot 31 and 39),
and the two heroes' power states (dormant → partial → full ultimate) are the persistent
threads across every cut.

---

## 5. Narration and dialogue (Macedonian, scarce — adapted, not verbatim)

A boss fight is visual; the voice is filler. Keep only what earns its place.

| # | Speaker | Line (MK) | Context |
|---|---|---|---|
| D1 | Boss (P3, shot 32) | „Од пепел сте — и во пепел ќе ве вратам.“ | mocking, single taunt that triggers the finale |
| D2 | Paladin (P3, shot 35, barely audible under music) | „Светлината не се гаси.“ | only hero line — the paladin's vow |

No narrator. The story is carried by action; the two lines are punctuation, not exposition.
(Optional: one cold-open epitaph title card in Macedonian — „Исечени во пепелта“ —
before shot 01, as a stylistic choice. Confirm in §10.)

---

## 6. Spatial audio + music design (restrained)

```
SFX (spatial, generated/procedural — no model needed):
  - ember hiss / ash-wind bed (throughout, L-R drift)
  - whip CRACK (P1), floor-scorch sizzle
  - eye-beam THRUM + glass-solidify SIZZLE (P2)
  - crossbow BOLT WHINE, afterimages
  - greatsword metal RING + holy HUM
  - implosion SUCK + bass SUB (P3)
  - winged LIFT whoosh + landing THUD

MUSIC (restrained, score_lyria bed + rises only at phase boundaries):
  - P1  low tribal percussion, string whispers, silence-lean
  - P2  rising brass, sub-rumble, one brass hit per boss slam
  - P3  short choir swell → cut to STILLNESS at the killing blow

Rule: music never masks the two voices or the SFX; it sits under the fight.
```

---

## 7. The pipeline (research-first, zero-cost authoring before any rental)

```
P0 RESEARCH    ✓ this document: WoW ability sets, Blizzard/wuxia cinematic grammar,
               identity cards verified on disk
P1 ENHANCE     expand/condense source beats into the 46-shot action spine (done above)
P2 SPLIT       narration ≠ dialogue: 2 dialogue lines, no narrator (done §5)
P3 SCRIPT      ✓ shot list + dialogue + audio map (done §4–§6)
P4 STORYBOARD  46 shots, each = START + END keyframe (null shots flagged if a single
               reference is ever emitted — build step rejects it)
P5 PROMPTS     Qwen-Image keyframes (semantic) + Wan FLF video prompts (seed→motion)
               named: 25_dhpf_kf_P1_07_start.png / _end.png, 25_dhpf_vid_07.json…
P6 PRICE CHECK live Vast auction scan + itemized estimate + hard cap (pending §9)
P7 PROOF       1 scene (3–4 FLF shots, one ability each) for user judgement
P8 FULL RUN    approved shots under cap → copy + sha256 + ffprobe → local assembly
               → teardown (instances AND volumes), bill-stop confirmation
```

**Prompt templates** (concrete, model-specific):

```text
[KEYFRAME — Qwen-Image / Qwen-Image-Edit  @1280x720]
{IDENTITY LOCK verbatim from canon}. {costume + weapon}. {full body action/pose}.
{environment, light, depth}. {foreground / midground / background}.
Photorealistic cinematic film still, 35mm anamorphic, real skin, film grain.
Palette {per hero}. Negative: duplicate face, extra face, extra limbs, text, watermark,
cartoon, illustration, cel-shaded, 3d render, plastic skin.

[VIDEO — Wan FLF  run_wan_i2v.py --imagefile START --endimage END]
The first frame shows {EXACT start-frame content}. Then {single mover: subject OR
camera OR light} {direction + character}. Camera: {shot size + move}. Continuity:
{what stays fixed}. Light and mood: {palette + grade}.
```

**Naming convention (name the prompts appropriately)** — deterministic and sortable:

```
25_dhpf_kf_P{phase:1-3}_{shot:02d}_{start|end}.png      # keyframes
25_dhpf_vid_P{phase}_{shot:02d}.json                     # video prompt/refs
25_dhpf_mix.wav / 25_dhpf_OUT.mp4                        # audio / final
```

---

## 8. Acceptance criteria (testable, per critique report)

A final cut ships only if ALL hold:

1. **Shot count** = 46 (≥40), durations ≥2.5 s averaging ~3 s → **≥2:00 runtime**.
2. **References per shot** ≥ 2 (start + end); a single-reference job is rejected at build.
3. **Camera grammar** present in every video prompt (size + move).
4. **Motion floor** (frame-difference) — no beat reads as a held still.
5. **Ability legibility** — each signature move visibly matches its VFX signature (§2.3).
6. **Identity gates** — DD ≥0.50 vs dd centroid; Azulon ≥0.50 vs Azulon-Master; boss = 0 faces.
7. **Visual-first** — mute audio, the fight still reads (power shifts by image only).
8. **Audio** — spatial sfx + restrained score, voices never masked; Macedonian-only dialogue.
9. **Style kit** photoreal; no cartoon/illustration; validated against researched references only.

---

## 9. Cost estimate (to be re-priced at P6 — zero-cost scan)

```
Keyframes  : 46 start + 46 end = 92 keyframes, Qwen-Image @ ~$0.03–0.07 each ≈ $2.8–6.5
             (or bulk on a single FP8 rental ~$0.45 session)
Video      : 46 FLF clips × ~3s, Wan 2.2 FLF ~80s/clip on 4080S ≈ $0.05–0.09/clip
             ≈ $2.5–4.5 spread across one/few sessions
Audio      : procedural SFX (local, free) + OmniVoice/MOSS dialogue (reuse, free)
TOTAL      : ~$5.5–8.0  (re-priced from live offers; SEQUENTIAL, never parallel fan-out)
```

Balance today: Vast ~$2.05 → **top-up needed per §10**; no rental authorized yet.

---

## 10. Open questions / decisions for the user

1. **Duration target** — 46 shots ≈ 2:20. Push to ~3:00 (60 shots)? (recommend: yes, at
   P4 after the proof scales cleanly).
2. **Boss design** — approve „Mal‘garot, Господарот на Пепелта“ (fire/ash demon)? Or
   another concept (void / frost / shadow)?
3. **Ability subset** — use the full §2.3 ability list, or trim to the strongest 5–6 per hero?
4. **Title card** — include the Macedonian cold-open epitaph?
5. **Dialogue voices** — 2 lines OK? Add one more boss taunt in P1?
6. **Budget top-up** — for the ~$5.5–8.0 full run, how much will you add to the ~$2.05?

---

*DELIVERED AS DEFINE-ONLY. No GPU has been rented; nothing above spends money until you
approve the boss design, the ability subset, and an itemized cap from the P6 live scan.*
