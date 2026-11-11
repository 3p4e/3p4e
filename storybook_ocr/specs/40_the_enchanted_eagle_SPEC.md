# 40 — Маѓепсаниот орел (The Enchanted Eagle)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Маѓепсаниот орел** — Младата селанка, претворена од волшебникот Ките во орел, го води својот сакан принц до дрвото со златни јаболка за да го добие благословот на кралот.

*Genre:* Бајка · фантазија · љубовна приказна

---

## 1. Render contract (non-negotiable)

| Field | Value |
|---|---|
| resolution / aspect | 1216x704 / 16:9 |
| fps | 24 |
| model | model-agnostic (chosen at generation) |
| frames | 121 (8k+1; fallback 81) |
| routing | model chosen per story at generation (43 sec.4 routes ledger) |
| model note | Model chosen per story at generation (43 §4). Keyframes + continuation prompts are generator-agnostic; only the render command differs per model. |

**Model routes (43 sec.4 — choose per story at generation):**

| Model | Input | Status |
|---|---|---|
| Wan2.1-FLF2V-14B-720P | start+end native (run START-ONLY) | WORKING (lead for 14B quality) |
| Kandinsky 6.0 Lite/Pro | start-image-only | WORKING (Pro-distill untested at scale) |
| SkyReels-V3 R2V-14B | start-image-only | WORKING (fallback) |
| LTX-Video 2B v0.9.5 | start-image-only | WORKING (small/fast, low ceiling) |
| Mochi-1 | start-image-only | untested here |
| LTX-2.3 22B distilled | start-image-only | DEAD (nanobind native-crash, 42 note) |
| style | photoreal |
| clip model | N-clip start-frame-only (43 sec.2) |
| language | mk |
| shot floor–max | 40–60 |
| seed policy | fixed-per-shot (same seed → reproducible shot; re-roll per shot id) |
| style anchor | Diablo 2 cinematic · World of Warcraft cinematic · StarCraft cinematic |

**Negative prompt:**

```
deformed, extra limbs, morphing, watermark, text, static frame, blurry, low quality, cropped head, cut-off face
```

---

## 2. Cast

| Role | Trait | Source | Face-lock |
|---|---|---|---|
| Принцот / The Prince | Млад, храбар принц во богата облека, заљубен во селанката | story-suggested | AI-default |
| Селанката / The Peasant Girl | Убава млада селанка со светли очи, подоцна претворена во орел | story-suggested | AI-default |
| Кралот / The King | Строг татко на принцот со круна, црвени облеки и сива брада | story-suggested | AI-default |
| Волшебникот Ките / The Wizard Kite | Мудар, белобрад чаробник со дрвено волшебно стапче | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~152.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Средбата

*Принцот ја среќава убавата селанка во полето и се вљубува, но кралот го одбива бракот и двајцата се принудени да бидат разделени.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S03 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S04 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S05 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S06 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S07 | WIDE | low-angle | crane-up | moderate | 3.0s | NAR |
| S08 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S09 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S10 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S11 | WIDE | high-angle | track | moderate | 3.0s | NAR |
| S12 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S13 | CLOSE-UP | low-angle | push-in | gentle | 3.0s | NAR |

### Act II — Полетот

*Девојката ја бара помошта на волшебникот Ките и се претвора во орел; лета до дворецот, го поканува принцот, го крева во небото и го носи до дрвото со златни јаболка.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | WIDE | eye-level | crane-down | moderate | 3.0s | NAR |
| S15 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S16 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | DLG |
| S17 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S18 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S19 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S20 | MACRO | macro | static | gentle | 3.0s | NAR |
| S21 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S22 | WIDE | high-angle | track | moderate | 3.5s | NAR |
| S23 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S24 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S25 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S26 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S27 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S29 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S30 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S31 | WIDE | high-angle | track | moderate | 4.0s | NAR |
| S32 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S33 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S34 | WIDE | eye-level | crane-down | moderate | 3.0s | NAR |
| S35 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S36 | MACRO | macro | static | gentle | 3.0s | NAR |
| S37 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |

### Act III — Благословот

*Ките го претвора орелот повторно во девојка, златните јаболка стануваат мираз, а кралот дава благослов за венчавката.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S40 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S41 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S42 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S43 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S44 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S46 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S47 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S48 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Еден принц патуваше низ златните полиња и здогледа девојка меѓу пченката.
- `S02` **NAR** — Девојката работеше тивко, а нејзината убавина светеше сред златото на полето.
- `S03` **NAR** — Принцот јаваше кон неа, срцето му забрза.
- `S04` **NAR** — Кога ја виде, застана како маѓепсан.
- `S05` **NAR** — И таа го забележа него.
- `S06` **NAR** — Двајцата млади се сретнаа меѓу пченките и веднаш се вљубија.
- `S07` **NAR** — Сонцето ги позлати додека ветуваа љубов.
- `S08` **NAR** — Но кралот, таткото на принцот, не го сакаше тој брак.
- `S09` **NAR** — Кралската гордост не дозволуваше селанка да стане принцеза.
- `S10` **DLG** — Принц: „Таа е единствената што ја сакам.“
- `S11` **NAR** — Со тешко срце ги разделија, еден од друг.
- `S12` **NAR** — Девојката остана сама, со очи полни солзи.
- `S13` **NAR** — Но решена, таа тргна да ја побара моќта на волшебникот Ките.
- `S14` **NAR** — Во сенчеста клисура живееше волшебникот Ките, познат по чуда.
- `S15` **DLG** — Ките: „Дојде за љубовта што ти ја одзедоа.“
- `S16` **DLG** — Ките: „Ќе те претворам во орел, и ќе одлеташ кај твојот љубен.“
- `S17` **NAR** — Ките крена волшебно стапче кон својата гостинка.
- `S18` **NAR** — Топла светлина ја обви девојката.
- `S19` **NAR** — И одеднаш, на нејзините раменици раснаа крилја.
- `S20` **NAR** — Пердувите се распростираа под златната светлина.
- `S21` **NAR** — Таа стана величествен орел и се крена кон небото.
- `S22` **NAR** — Орелот долета над дворецот на принцот.
- `S23` **NAR** — И слета на балконот каде принцот тагуваше.
- `S24` **NAR** — Орелот го повика со очи и јасно му покажа да тргне.
- `S25` **NAR** — Во нејзините очи принцот ја препозна својата љубена.
- `S26` **NAR** — Принцот веднаш побрза кон клисурата на Ките.
- `S27` **NAR** — Застана пред волшебникот, без здив.
- `S28` **DLG** — Ките: „Ќе го добиеш тоа што го сакаш ако ми донесеш три златни јаболка.“
- `S29` **NAR** — Цената беше чудна: три јаболка од злато.
- `S30` **NAR** — Додека излегуваше, орелот со канџи го крена високо во небото.
- `S31` **NAR** — Летаа долго над полиња и шуми.
- `S32` **NAR** — Принцот гледаше како земјата се стеснува под нив.
- `S33` **NAR** — Покрај едно езеро блесна дрво со златни плодови.
- `S34` **NAR** — Орелот го спушти принцот крај мирната вода.
- `S35` **NAR** — Принцот тргна кон чудното дрво.
- `S36` **NAR** — Плодовите светеа како мало сонце.
- `S37` **NAR** — Набра три јаболка од злато.
- `S38` **NAR** — Со јаболката в раце, се врати кај орелот.
- `S39` **NAR** — И двајцата се вратија кај Ките.
- `S40` **NAR** — Ките со едно замавнување со стапчето...
- `S41` **NAR** — ...го претвори орелот повторно во девојка.
- `S42` **NAR** — Девојката стоеше повторно пред него, цела и насмеана.
- `S43` **DLG** — Ките: „Златните јаболка ќе бидат твојот мираз.“
- `S44` **NAR** — Сега со богатство и љубов, тргнаа кон дворецот.
- `S45` **NAR** — Кралот ги прими, и младата повеќе не беше сиромашна.
- `S46` **NAR** — Со благослов, кралот даде одобрување за венчавката.
- `S47` **NAR** — И двајцата си го дадоа ветувањето.
- `S48` **NAR** — Така љубовта, посилна од круната, победи во златниот дворец.

---

## 5. Acceptance criteria (testable)

1. Shot count = 48 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
2. References per shot ≥ 2 (start + end FLF); single-reference jobs rejected at build.
3. Camera grammar present in every shot (size + angle + move).
4. Motion floor via frame-difference — no held stills.
5. Narration/dialogue split, adapted not verbatim; narration is filler.
6. Visual-first — mute audio, the story still reads.
7. Audio — spatial SFX + restrained score; Macedonian-only voices.
8. Style: photoreal, validated against external references only (no self-made benchmark).

---


---

## 5b. Director corrections (KB §13 — binding from 2026-11-07)

*KB §13 DIRECTOR CORRECTIONS — overrides all prior asset/keyframe guidance · issued 2026-11-07*

| # | Rule |
|---|---|
| 1 | EAGLE FORM: the girl's eagle is a photoreal golden-brown eagle that MUST retain her identity thread (same amber eye warmth, soft gaze); never a generic or cartoon bird; off-model eagle = REJECT |
| 2 | TRANSFORMATION FX: magic is light-driven and coherent (golden ribbons and motes, wings unfurl from light) — no cartoon sparkle storm, no anime glow halo, no 2D flash frames |
| 3 | GOLDEN APPLES: three distinct glowing golden apples with apple silhouette and stem, never oranges, peaches or featureless orbs; the count stays three across all shots |
| 4 | WIZARD KITE: aged, white-bearded sorcerer with a carved wooden staff; no modern props, no firearm or gun silhouette anywhere |
| 5 | CHILD-SAFE: eagle talons carry the prince by his shoulders with no injury, no blood, no distress; separation is shown as sorrow, not violence |
| 6 | AI-DEFAULT FACES: prince, girl, king and kite all AI-default; face identity must stay consistent across all shots (no real faces) |

**Anti-slop negatives (always appended):** `firearm, gun, machinegun, Uzi, barrel, magazine, ammo clip, muzzle, modern weapon, cartoon sparkle, anime glow, plastic skin, low poly, 3d render`

> Activates when face_lock changes from AI-default to an enrolled identity. AI-default packages carry this as a forward constraint, not a current defect.

## 6. Pipeline note

```
P0 RESEARCH    source text read + cinematic language researched
P1 ENHANCE     beat spine authored into shot list
P2 SPLIT       narration != dialogue (Macedonian)
P3 SCRIPT      shot list + cues (this spec)
P4 STORYBOARD  every shot = START + END keyframe (FLF)
P5 PROMPTS     Qwen-Image keyframes (3a) + model-agnostic continuation prompts (3b)
P6 PRICE CHECK live Vast scan + itemized estimate + per-run approval
P7 PROOF       1 scene (3-4 FLF shots) for user judgement
P8 FULL RUN    approved shots -> copy+sha256+ffprobe -> assembly -> teardown
```

*DEFINE-ONLY. No GPU rented; nothing spends until P6 is approved per run.*
