# #23 Perseus & Medusa — SOUND DESIGN PLAN v2 (60-shot)

> Refined per-shot cue sheet + scene beds + one-motif dirge + LTX audio strategy.
> Supersedes `23_SFX_PLAN.md` (which was written against the retired 48-shot cut).
> Shot canon: **60 shots** per `data/23_perseus_defeats_medusa_data.json` and
> `23_GROK_60_KEYFRAME_PROMPTS.md`. Act map: **Act I S01–S14 · Act II S15–S45 · Act III S46–S60**.
> Aesthetic: GRIMDARK AEGEAN HORROR — dread, not gore; no blood/wet-impact splatter;
> Medusa's defeat reads as **stone-stillness**. Sound obeys the same rule.

Sources: freesound.org (CC0) + synthesized layers (pure-sine/noise-bed builds in Audacity
or ffmpeg `sine`/`anoisesrc`); no non-free licences. Music: AI-generated (Suno/Udio-class)
royalty-free renders or licensed CC0/PD recordings; no commercial library cues.
Assembly: ffmpeg per-clip stems, 24 fps timeline, mix loudness **-16 LUFS** (integrated),
peak ceiling **-1 dBTP**, VOX always clear of bed by ≥ 14 dB.

---

## 1. Stem contract (per shot — 5 stems, 48 kHz / 24-bit WAV)

| # | Stem | Carries | Notes |
|---|------|---------|-------|
| 1 | `BED` | scene ambience loop + musical drone (dirge) | continuous under the whole shot; -20 dB under VOX nominal |
| 2 | `SFX` | 1–4 designed event sounds tied to beats | one-shots; never masked under dialogue |
| 3 | `FOLEY` | cloth, armor, steps, chains, leather, breath, wing-cloth | close-mic'd, intimate scale |
| 4 | `VOX` | narration (center) + dialogue (per-character, slight L/R pan) | Macedonian master; EN dub alternate |
| 5 | `MUSIC` | one-motif dirge only | see §4; no hero fanfare, no trailer hits, no stingers |

- Per-shot stems: `audio/s##_{BED,SFX,FOLEY,VOX,MUSIC}.wav` — 48 kHz / 24-bit PCM.
- Masters: `audio/23_master_MK.wav`, `audio/23_master_EN.wav` (48 kHz / 24-bit).
- Final mp4 mux: **forced 44 100 Hz** sample rate at container level (operating rule);
  masters stay 48 kHz — the 44.1 k conversion happens at mux, not in the mix.
- Loudness: masters -16 LUFS integrated, -1 dBTP true-peak; stems un-normalized headroom,
  levels set at the 24 fps timeline mix (ffmpeg `amix`/`loudnorm`).

---

## 2. Environment beds — 6 scene-level ambiences

Shot ranges below use env refs from the data JSON + env plates. Each bed is a **loopable
stereo bed** built from named layers; each layer lists a concrete acquisition route
(CC0 source class or synth recipe). All beds keep a **sub-40 Hz component ≤ -28 dB**
except where noted — felt, not heard.

### BED-A — STORM-SEA (open water, wind over water)
Shots: **S35–S37, S44, S46, S49–S55, S57–S59** (sea flight, sacrifice rock, ketos surface).
Layers:
1. **Open-sea wash** — long 20–30 s loop, CC0 "ocean waves distant storm"; high-pass 120 Hz,
   low-pass 8 kHz, slow LFO on level ±1.5 dB @ 0.05 Hz.
2. **Wind rush** — CC0 "wind howling coastal" or pink-noise synth (`anoisesrc=color=pink`)
   through a slow band-sweep; stereo width wide; -18 dB under the sea wash.
3. **Sub swell** — pure 38 Hz sine, amplitude tied to the wave loop's crest (sidechain from
   layer 1 via ffmpeg `sidechaincompress`), -30 dB. The "breathing sea" of the weird-art canon.
4. **Sparse gulls** — 1–2 CC0 gull cries per 30 s, only in calm aftermath shots (S55, S59);
   high-pass 1 kHz, throw them wide L or R.

### BED-B — TEMPLE / MEGARON (palace hall interior)
Shots: **S02, S03** (throne hall); divine gift scenes S06–S10 use **BED-F (SKY/OLYMPUS)**.
Layers:
1. **Room tone** — CC0 "castle hall interior room tone" or synthetic: brown noise
   (`anoisesrc=color=brown`) low-passed 250 Hz, very low level; the "weight of stone".
2. **Torch crackle** — CC0 "fire torch burning loop", narrow-band, center-panned, irregular;
   -26 dB.
3. **Hall air** — barely-moving air synth: white noise at -40 dB through a 400 Hz–1.2 kHz
   band-pass, very slow amplitude drift.
4. **Sub room** — 45 Hz sine at -32 dB, constant. Sells the megaron's mass.

### BED-C — CAVE / GROTTO (cavern interior, weeping walls)
Shots: **S15–S30, S38, S40**.
Layers:
1. **Cavern drone** — CC0 "cave ambience deep" or synth stack: 55 Hz + 82.5 Hz sines
   (fifth) at -26 dB with ±2 dB slow drift; the cave "breathes".
2. **Water drips** — CC0 "cave water drips"; place 6–8 drops irregularly per 10 s,
   long reverb tail (ffmpeg `aecho`), alternate L/R.
3. **Stone creak** — CC0 "stone grinding low" or slowed-down wood-creak pitch-shifted -12 st;
   one creak every 8–14 s, random pan.
4. **Hiss layer (Medusa presence)** — a looped, quiet serpent-hiss bed (CC0 "snake hiss"
   looped and reverbed hard), faded in from S17, peaking S19–S26, gone by S31.
   This is the tension ramp: level +2 dB per shot from S17 to S26, then hard cut at S27.
5. **Sub 32 Hz** — -30 dB, constant, only S19–S30 (her waking weight).

### BED-D — ROCK / COAST (exterior cliff, wind-stunted scrub, shore rock)
Shots: **S01, S11–S14, S31–S34, S36–S37, S41–S43, S56, S60**.
Layers:
1. **Wind over rock** — CC0 "wind mountain cliff" ; mid-focused, moderate; the workhorse bed.
2. **Sea below** — distant surf wash (CC0 "waves on rocks distant"), low-passed 1.5 kHz,
   -20 dB; constant reminder of the Aegean below.
3. **Scrub rustle** — CC0 "dry grass wind" at -30 dB, only on land approach/journey shots
   (S11–S14, S31–S34).
4. **Stone birds** — sparse carrion-bird cries (CC0 "crow raven distant"), 1 per 20 s on
   S13–S14 only (the petrified field warning).

### BED-E — PETRIFIED-FIELD (standing-stone field of former warriors)
Shots: **S13 (tail), S14, S15, S42**.
Layers (built ON TOP of BED-D, replacing its scrub/sea weight):
1. **Dead-air variant** — BED-D layers but high-passed harder and pulled -4 dB;
   the world goes quieter near the statues.
2. **Stone-murmur** — heavily processed layer: slowed speech-like whisper formants
   (ffmpeg `vibrato`+`aecho` on any whisper recording, pitch -18 st), -38 dB, unintelligible.
   The statues "almost speak" — weird-art touch, must stay subliminal.
3. **Petrify residue** — a faint crystalline ring (see SFX-A9 recipe) hovering at -42 dB
   from S14 onward, returning full-force at S42.

### BED-F — SKY / OLYMPUS (high air, divine register)
Shots: **S06–S10 (divine gift), S33–S35 (take-off/climb), S46–S48, S57–S59**.
Layers:
1. **High wind** — CC0 "high altitude wind", brighter than BED-A wind (high-pass 300 Hz),
   constant on flight shots.
2. **Wingbeat pulse** — a soft, low thump synthesized from a 60 Hz sine burst + noise tail,
   **1 per second** in rhythm with Pegasus' wing cycle; kept "felt not heard" at -24 dB,
   panned to follow screen direction. Present S33–S35, S44, S46–S48, S57–S59.
3. **Radiant hum** — for divine materializations (S06) and Pegasus' presence: a warm
   detuned-pair drone (220 Hz + 220.7 Hz) with slow tremolo, -28 dB; this is the ONLY
   warm timbre in the film and it belongs to the gods/Pegasus.
4. **Air sparkle** — rare, tiny high "glass" pings (synth: sine chirp 4 kHz→6 kHz, 80 ms),
   1–2 per shot only on S06–S10; divine dust.

Bed assignment is per-shot in the cue sheet (§3, "Bed" column).

---

## 3. Per-shot SFX cue sheet — all 60 shots

Intensity 1–5 (1 = near-silent texture, 5 = full event). "—" in SFX = only bed+foley.
Stem targets: B = BED, S = SFX, F = FOLEY, V = VOX, M = MUSIC (see §4 for MUSIC column).
Events are derived from the data-JSON beat_timeline / action lines (ground truth).

### ACT I — Заложба и божествена дарба (S01–S14)

| Shot | Event | SFX description | Stems | Int | Bed |
|------|-------|-----------------|-------|-----|-----|
| S01 | Establishing crane-down over citadel | distant surf below walls; one far gull; bronze banner snap ×2 | B,S | 2 | D |
| S02 | Perseus kneels; vow DLG | marble knee-contact (soft); torch flare as he lifts his head | B,S,F,V | 3 | B |
| S03 | CU resolve; NAR | single marble knock (the oath) — low, dry, one note; flame flutter | B,S,F,V | 2 | B |
| S04 | NAR insert — Medusa's lair | distant serpent hiss (very far, reverb tail 3 s); stone shift | B,S,V | 2 | C-preset* |
| S05 | CU Medusa eyes open | faint crystalline shimmer (gaze "charging"); snake slide across brow (foley) | B,S,F,V | 3 | C-preset* |
| S06 | Athena materializes | radiant bloom swell (sub-boom + rising hum, no hit); air sparkle ping | B,S,V | 3 | F |
| S07 | Shield offered | bronze hum as shield catches light; soft metal set-into-hands | B,S,F,V | 2 | F |
| S08 | Harpe offered; Hermes DLG | blade shing (cold reverb, short tail); wing flutter | B,S,F,V | 3 | F |
| S09 | Athena's warning; DLG | low warning drone swell under line (music stem); cloth shift | B,F,V,M | 3 | F |
| S10 | CU — warning sinks in; NAR | heartbeat single thump (35 Hz) under "врежан"; then silence | B,S,F,V | 2 | F |
| S11 | Journey wide track | hard wind gust; distant thunder roll (storm-gloom); gravel steps | B,S,F,V | 2 | D |
| S12 | Shield polish check | leather-strap creak; thumbnail on bronze (tiny ring) | B,S,F,V | 1 | D |
| S13 | Cave mouth revealed | carrion-bird cry ×1; stone-murmur enters (subliminal); wind drop | B,S,V | 3 | D→E |
| S14 | Pan past petrified warrior | stone whisper tail; dust fall (fine debris patter); dead-air drop | B,S,V | 3 | E |

\* S04/S05 are narration inserts of the lair — use a **remote lair preset**: BED-C layers at
low level + heavy reverb, as if heard through stone, so Act I never physically enters the cave.

### ACT II — Пештерата и падот на Медуза (S15–S45)

| Shot | Event | SFX description | Stems | Int | Bed |
|------|-------|-----------------|-------|-----|-----|
| S15 | Perseus studies statues | his steady breath (foley, close); knuckle creak on strap | B,F,V | 2 | E→C |
| S16 | CU steeling himself | one slow inhale / exhale; heartbeat returns, softer than S10 | B,F,V | 2 | C |
| S17 | Backward entry, shield raised | measured backward steps (heel-stone, ×4); hiss layer fades IN | B,F,V | 3 | C |
| S18 | Macro shield reflection | silver "water" shimmer on bronze; drip with long tail | B,S,V | 3 | C |
| S19 | **Medusa rises** | stone-bed grind (low, long); serpent crown unfurls — layered hiss burst; sub-drop 32 Hz | B,S,V | 5 | C |
| S20 | Medusa lunges | rush of air; claw-whoosh; stone-foot slam | B,S,V | 4 | C |
| S21 | Claws rake mirror-shield | metal scrape + ring + bronze sparks (tiny sizzle tail) | B,S,V | 4 | C |
| S22 | Perseus spins, eyes shut | cloak spin; blade arc whoosh; foot pivot | B,S,F,V | 4 | C |
| S23 | Medusa recoils from own gaze | serpent-hair whip-crack (×2); her shriek attack — **withheld**, only a cut-off gasp | B,S,V | 4 | C |
| S24 | CU Perseus eyes shut | sweat drop; breath held; near-silence bed dip (-6 dB) | B,F,V | 3 | C |
| S25 | Harpe hooks past guard | blade hook-and-drag on stone (sparks); her stagger-step | B,S,V | 4 | C |
| S26 | **Decisive strike** | single clean cleave whoosh → **muted** impact (NO gore); body-to-stone crumble; dust plume | B,S,V | 5 | C |
| S27 | CU head at rest | serpents coil still (tiny scale-slides); eyes dim = faint green-hum fade-out; cave falls quiet | B,S,V | 2 | C |
| S28 | Head into kibisis sack | leather mouth-open; soft head-settle (weight, cloth-muffled); knot cinch | B,S,F,V | 3 | C |
| S29 | Macro mirror-catch | **crystalline shimmer 1 s** (SFX-A9); the gaze "locked" — high sine cluster 2.8/3.5/4.2 kHz | B,S,V | 4 | C |
| S30 | Sprint to daylight | fast footsteps; daylight-wash (bed opens up, high shelf lifts); breath bursts | B,F,V | 4 | C→D |
| S31 | Pegasus waiting; crane-down | wing-unfold cloth-snap; radiant hum enters; horse breath | B,S,F,V | 3 | D+F |
| S32 | Trust nuzzle | muzzle-in-palm (soft); tack creak; warm chime (tiny) | B,S,F,V | 2 | D+F |
| S33 | Mount; wings unfurl; lift | big wingbeat ×3 (felt thumps); launch air-rush; crane-up wind | B,S,F,V | 4 | F |
| S34 | Two Gorgons burst out | **Gorgon shriek** — processed female cry + reverse-reverb tail, capped -6 dB under VOX; wing-snap | B,S,V | 5 | D |
| S35 | Victory flight over sea | wingbeat pulse; sea-spray hiss as they skim; sack flap | B,S,F,V | 3 | A |
| S36 | Sacrifice rock revealed | surf pound below (closer); chain rattle in wind (far); gull sparse | B,S,V | 3 | A/D |
| S37 | Andromeda chained, wind | chain clink close; tunic whip (foley); her shivering breath | B,F,V | 3 | A/D |
| S38 | **Cavern answers — Gorgons wake** | deep-cave answering rumble; falling stone patter (from above); second shriek, farther | B,S,V | 4 | C |
| S39 | CU Andromeda hopeful | tear-trail (tiny wet foley); wind softens; music dirge lifts 1 dB | B,F,V,M | 2 | A/D |
| S40 | Perseus, shield up, not looking back | shield raise ring; jaw-set breath; shriek muffled behind stone | B,S,F,V | 3 | C/D |
| S41 | Pegasus lands on ledge | wing-brake flaps ×2; hoof-stone contact ×2; dismount armor clink | B,S,F,V | 4 | A/D |
| S42 | **Pursuer petrifies at cave mouth** | stone-race crackle rising up her body, then **dead-silent stop**; dust settle | B,S,V | 5 | E |
| S43 | Chains loosened | iron link-work close (dry, detailed); chains fall onto rock with ring; wrist rub | B,S,F,V | 3 | A/D |
| S44 | Lift-off with Andromeda | wingbeat ×2 heavy; her startled breath; surf recedes below | B,S,F,V | 3 | A |
| S45 | Andromeda thanks; DLG | cloth settle; wind hush; single warm string note support (music) | B,F,V,M | 2 | A |

### ACT III — Спасението на Андромеда (S46–S60)

| Shot | Event | SFX description | Stems | Int | Bed |
|------|-------|-----------------|-------|-----|-----|
| S46 | Glide high; NAR | smooth high wind; wing-glide (no flaps — soaring); distant coast tone | B,F,V | 2 | F/A |
| S47 | Andromeda introduces herself; DLG | wind tucked low under line; cloth flutter; horse breath rhythm | B,F,V | 2 | F/A |
| S48 | Recounts mother's offense; DLG | bed thins (-3 dB) for intimacy; memory-tone (cold minor cluster, music) | B,F,V,M | 2 | F/A |
| S49 | **Ketos coils below** | huge water displacement; sub-boom 30 Hz; deep pressure shift | B,S,V | 4 | A |
| S50 | Ketos head rises | foam surge; maw-open pressure creak; water sheet off scales | B,S,V | 4 | A |
| S51 | Sacrifice explained; DLG | sea rises (layer swell); her steady voice over it; foreboding cluster (music) | B,F,V,M | 3 | A |
| S52 | **Ketos rears over rock** | sea "stands up" — massive displacement + roar (low, wet, no screech); rock spray | B,S,V | 5 | A |
| S53 | **Kibisis opened** | leather untie; soft **dread tone** (synth: 110 Hz minor-second beating pair) as head swings free | B,S,F,V | 4 | A |
| S54 | **THE GAZE across the water** | **ALL SFX cut to silence 0.8 s** → low petrifying drone (60 Hz + slow gliss down); one crystalline shimmer as the gaze lands | B,S,V | 5 | A (cut) |
| S55 | Ketos grey-stone reef | drone decays; **surf returns over stone**, regular, calm; gull ×1; sea "breathes" again | B,S,V | 3 | A |
| S56 | Storm eases; her hand finds his arm | wind drops audibly (bed automation); cloth-on-arm touch; first warm air entry | B,F,V | 2 | D→F |
| S57 | Realization dawns | low heart thump ×1; protective breath; dirge begins resolve (music) | B,F,V,M | 2 | F |
| S58 | **Hands clasp** | soft leather grip (intimate, close); tiny armor plate settle; near-silence around it | B,F,V | 2 | F |
| S59 | Descent to city | city tone enters (distant crowd murmur -36 dB, bells); wingbeat slows; gulls | B,S,V | 3 | F/D |
| S60 | Reunion; pull-back; NAR | one distant city bell (single, warm); family footsteps on stone; bed resolves to near-silence with sea far below | B,S,V,M | 2 | D (calm) |

**Design-voice recap:** peak intensities sit on S19 (rise), S26 (strike), S34/S38 (shrieks),
S42 (petrification), S52–S54 (ketos + gaze). Five 5/5 events in 60 shots — restraint holds.

---

## 4. The one motif — "The Stone Dirge"

One musical idea only, per the doctrine. A **dirge**: slow, vocal-led, modal.
No hero fanfare. No trailer hits. No percussion section.

### 4.1 Concrete motif spec
- **Tempo:** 48 BPM (half-time feel; one beat ≈ 1.25 s at 24 fps ≈ 30 frames).
- **Mode/interval structure:** **Phrygian mode on E**. Core cell of **3 notes**:
  **E – F – B♭** (minor 2nd up, then tritone up) — the "stone stare" cell:
  the minor 2nd is the dread rub, the tritone is the mythic distance.
  Response cell: **B♭ – A – E** (falling, resignation). Full phrase: cell A ×2, response ×1.
- **Instrumentation (all royalty-free / AI-gen friendly):**
  - Lead: **low female voice** on "ah/eh", no lyrics, heavy hall reverb (~3.2 s tail) — Medusa's theme.
  - Under-voice: **contrabass drone on E0/E1**, slow bow — constant floor.
  - Color: **ney or duduk** (wind) doubles the voice an octave up, only in Act III.
  - Optional (Act III only): **warm strings (violas)** playing the response cell as a held pad.
  - Explicitly excluded: drums, brass, piano, harp glissandi, choir swells.
- **AI-generation route:** prompt a Suno/Udio-class model with: *"funeral dirge, 48 bpm,
  phrygian mode, low female drone vocal, contrabass, duduk, no percussion, dark ambient,
  ancient Greek, reverb-heavy, instrumental aside from wordless voice"*. Render ≥ 3 takes;
  pick the one whose vocal sits under -20 LUFS solo. CC0 fallback: layer public-domain
  gregorian-style chant formant-shifted -5 st under a synth contrabass.

### 4.2 Variation across the three acts

| Act | Where | Treatment |
|-----|-------|-----------|
| **Act I** (S01–S14) | absence | **No dirge.** Only the radiant hum (gods) and drones. The dirge is withheld so its first entry lands. |
| **Act II** | S15 | contrabass alone, pianissimo (-30 dB), enters with the petrified field. |
| | S17–S18 | + ney fragment, barely audible. |
| | **S19** | **full dirge statement**: voice enters on E–F–B♭ as Medusa rises; repeats through S26. |
| | S23 | voice **fractures**: the singer breaks the B♭ into a tremolo (the mirror-catch); instruments hold. |
| | S26–S27 | **the dirge stops on the strike** — not a hit, the bow simply leaves the string. One beat of nothing. |
| | S28–S30 | contrabass only, fading; silence is the point. |
| | S34/S38 | shrieks are diegetic; music does NOT answer them (do not dramatize — doctrine). |
| | S42 | one solo contrabass note on E as the pursuer petrifies; let it decay fully. |
| **Act III** | S46–S51 | dirge returns in **memory form**: voice sings the response cell only (B♭–A–E), slower, under Andromeda's story. |
| | S53 | dread tone (110 Hz beating pair) is a **harmonization of the dirge at 1/4 speed** — same intervals, unrecognizable, dread. |
| | **S54** | with the 0.8 s silence: **everything, including the dirge, stops**. |
| | **S56–S58** | **resolution**: voice returns on the response cell but the final E is replaced by a **major third G♯** (Phrygian → Picardy lift, one semitone of mercy). Strings pad underneath. This is the only warm chord in the film and it is earned at S56, not S60. |
| | S59–S60 | dirge thins to a single sustained E (open fifth with B) under the city; fades to silence 1 s before the last frame. |

### 4.3 Mix rule for MUSIC
MUSIC stem rides at **-22 LUFS nominal**, never within 6 dB of VOX, and is fully ducked
(≥ -8 dB gain reduction) under every dialogue line by the mix compressor. If a listener
can hum the tune after one watch, it is too loud.

---

## 5. LTX-native audio — extraction / keep-vs-replace strategy

LTX-Video renders clips with a native stereo audio track (model-generated ambience + effects).
Quality is inconsistent; the plan treats native audio as **raw material, never as the mix**.

### 5.1 Per-clip triage (run on every rendered clip)
| Native content | Verdict | Action |
|----------------|---------|--------|
| Room tone / wind / sea wash | **KEEP as texture** | High-pass 80 Hz, denoise (`afftdn`), use at -25 dB under designed BED to glue shots; never solo. |
| Cloth / footsteps / armor incidental | **KEEP if clean** | Gate out between events; else replace with designed foley. |
| Wing flaps (Pegasus) | **KEEP rhythmic timing, REPLACE timbre** | Use native clip only to mark wingbeat positions on the timeline; replace with the designed wingbeat pulse. |
| Serpent hiss / cave rumble | **REPLACE** | Designed layers (BED-C) are controlled; native versions peak unpredictably. |
| **Voices / whispered words / "music"** | **ALWAYS REPLACE / MUTE** | Native LTX speech is unusable for VOX. Strip completely; use `23_AUDIO_SCRIPT_MK_EN.md` VO takes. Any native "score" is muted 100%. |
| Shrieks / roars / impacts (S19–S26, S34, S38, S42, S52–S54) | **REPLACE** | These are the film's five peaks; design owns them (see §3). Native audio may supply a noise layer at -30 dB only. |

### 5.2 Extraction pipeline (per clip)
```
ffmpeg -i clip_XX.mp4 -map 0:a? -vn -ac 2 -ar 48000 -c:a pcm_s24le raw/sXX_ltx.wav
ffmpeg -i raw/sXX_ltx.wav -af "highpass=f=80,afftdn=nr=12,acompressor=threshold=-30dB:ratio=2" stem_ltx/sXX_clean.wav
# audition vs. cue sheet; classify each 0.5 s window keep/replace per §5.1 table
```
Every keep/replace decision is logged in `audio/sXX_audio_triage.csv` (shot, window, class,
verdict, dB offset) so the mix is auditable against this plan.

---

## 6. Output contract (restated, non-negotiable)

- **Stems per shot:** `audio/s##_{BED,SFX,FOLEY,VOX,MUSIC}.wav` — 48 kHz / 24-bit PCM, start
time-aligned to shot head at 24 fps (frame-exact).
- **Masters:** `audio/23_master_MK.wav`, `audio/23_master_EN.wav` — 48 kHz / 24-bit,
  -16 LUFS integrated, -1 dBTP.
- **Mux:** forced **44 100 Hz** audio at final mp4 container (operating rule); the 48 kHz
  masters are the archive, the 44.1 k stream is delivery.
- **Mix template:** BED -20 dB under VOX nominal; MUSIC duck ≥ 8 dB under DLG;
  five 5/5 events only; 0.8 s full-cut at S54 honored at the timeline level (all stems).
- **Audit:** triage CSV (§5.2) + per-shot cue sheet (§3) ship with the masters.

## 7. Changelog from v1
- Re-mapped every cue from the retired 48-shot numbering to the **60-shot canon**.
- Expanded scene beds from 4 to **6 environments** with named layering sources and shot ranges.
- Specified the dirge concretely: **E Phrygian, E–F–B♭ cell, 48 BPM**, voice/contrabass/ney,
  with act-by-act variation and an explicit S54 full-stop and S56 Picardy lift.
- Added the **LTX-native audio triage + extraction pipeline** (keep-vs-replace table, ffmpeg recipe,
  audit CSV).
- Locked the **0.8 s S54 silence**, the five 5/5 events, and the MUSIC ducked-under-DLG rule.
- Restated the 5-stem / 48 kHz / 24-bit contract and the forced-44.1 k mux.
