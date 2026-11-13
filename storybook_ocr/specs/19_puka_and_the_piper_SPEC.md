# 19 — Пука и гајдаџијата (Pooka and the Piper)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Пука и гајдаџијата** — Еден невешт млад гајдаџија му свири на шумскиот дух Пука и на самовилите Банши, преку една магична ноќ станува најдобриот гајдаџија во цела Ирска.

*Genre:* Легенда · мистична авантура

---

## 1. Render contract (non-negotiable)

| Field | Value |
|---|---|
| resolution / aspect | 1216x704 / 16:9 |
| fps | 24 |
| model | model-agnostic (chosen at generation) |
| frames | 121 (8k+1; fallback 81) |
| routing | model chosen per story at generation (43 sec.4 routes ledger) |
| model note | Model chosen per story at generation (43 sec.4). Keyframes + continuation prompts are generator-agnostic; only the render command differs per model. |

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
| Гајдаџијата / The Piper | Млад, добродушен и истраен свирач со едноставни селски алишта | story-suggested | AI-default |
| Пука / Pooka | Шумски дух со рогови, разбушавена грива и палав, но благ насмев | story-suggested | AI-default |
| Банши / Banshees | Самовили со долги зелени наметки и свилена коса, бледо сјаење | story-suggested | AI-default |
| Мајката / The Mother | Грижлива старица покрај огништето | story-suggested | AI-default |
| Соседите / The Neighbors | Едноставни ирски селани во волнени облеки | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~165.0s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Младиот невешт гајдаџија го среќава шумскиот дух Пука, кој му нуди да го однесе на магично патување.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S03 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S04 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S05 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | DLG |
| S06 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S07 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S08 | CLOSE | over-shoulder | static | gentle | 3.0s | DLG |
| S09 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | DLG |
| S10 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S11 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S12 | MEDIUM | over-shoulder | static | moderate | 3.0s | DLG |
| S13 | CLOSE | eye-level | static | gentle | 3.0s | DLG |

### Act II — Патот и пештерата

*Пука го носи гајдаџијата во пештерата на Баншите, каде младичот свири цела ноќ и го открива својот дар.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S15 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S16 | CLOSE | over-shoulder | track | gentle | 3.0s | — |
| S17 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S18 | MEDIUM | eye-level | push-in | moderate | 3.5s | — |
| S19 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S21 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S22 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | DLG |
| S23 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S24 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | DLG |
| S25 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S26 | INSERT | macro | static | gentle | 3.0s | — |
| S27 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S28 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S29 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S30 | MEDIUM | over-shoulder | pan-left | moderate | 3.5s | — |
| S31 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S32 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S33 | MEDIUM | eye-level | track | moderate | 3.5s | — |
| S34 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |
| S35 | CLOSE | over-shoulder | static | gentle | 3.0s | — |
| S36 | WIDE | low-angle | pan-right | moderate | 3.5s | — |
| S37 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S38 | WIDE | high-angle | static | moderate | 3.5s | — |
| S39 | CLOSE | eye-level | static | gentle | 3.5s | NAR |

### Act III — Наградата и вистината

*Младичот добива златници, но тие се претвораат во лисја. Сепак, од тој ден неговото свирење е совршено и сите го признаваат.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S40 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S41 | INSERT | macro | static | gentle | 3.0s | NAR |
| S42 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S43 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S44 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S45 | CLOSE | over-shoulder | static | gentle | 3.0s | — |
| S46 | INSERT | macro | static | gentle | 3.5s | NAR |
| S47 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S48 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S49 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S50 | WIDE | low-angle | crane-down | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во дамнешна Ирска, сред зелените ридови, живееше еден млад гајдаџија.
- `S02` **NAR** — Тој свиреше со сето срце, но неговите мелодии беа груби и нескладни.
- `S03` **NAR** — По цел ден вежбаше, но песната му излегуваше рапава.
- `S04` **NAR** — Дури и птиците се разлетуваа кога ќе засвиреше.
- `S05` **DLG** — Гајдаџијата: „Добро е што знам барем една песна.“
- `S06` **NAR** — Тогаш, од маглата на шумата, се појави сенка со рогови.
- `S07` **NAR** — Тоа беше Пука, шумски дух што сакаше да плаши и да се шегува со луѓето.
- `S08` **DLG** — Гајдаџијата: „Подалеку од мене!“
- `S09` **DLG** — Пука: „Не плаши се, младичу!“
- `S10` **DLG** — Пука: „Качи ми се на грбот! Фати се за роговите!“
- `S11` **DLG** — Пука: „Ќе те одведам да ми посвириш малку.“
- `S12` **DLG** — Гајдаџијата: „Ама јас знам само една песна.“
- `S13` **DLG** — Пука: „Не е важно. Ќе те претворам во најдобриот гајдаџија.“
- `S14` **NAR** — И така, младичот се качи на грбот на духот.
- `S15` **NAR** — Пука побрза низ шумата како ветар.
- `S17` **NAR** — Стигнаа до устието на пештера во карпата.
- `S19` **NAR** — Внатре чекаа повеќе од стотина суштества со долги коси.
- `S20` **NAR** — Тоа беа Баншите, шумските самовили, сите во зелено.
- `S22` **DLG** — Банши: „Добровечер, Пука. Кој е овој човек со тебе?“
- `S23` **DLG** — Пука: „Тој е најдобриот гајдаџија во цела Ирска.“
- `S24` **DLG** — Пука: „Почни да свириш!“
- `S27` **NAR** — Штом засвире, воздухот во пештерата затрепери.
- `S28` **NAR** — Баншите почнаа да се нишаат во ритам.
- `S29` **NAR** — Самовилите започнаа да танцуваат.
- `S31` **NAR** — И не запреа цела ноќ.
- `S34` **NAR** — Колата стануваше сè подива.
- `S37` **NAR** — Гајдаџијата свиреше без престан, а музиката беше магична.
- `S39` **NAR** — Дури првите зраци на зората не допреа до устието на пештерата.
- `S40` **NAR** — Како награда, самовилите му дадоа полна кеса со златници.
- `S41` **NAR** — Златниците светкаа како жар.
- `S42` **NAR** — Најсреќен, младичот се врати дома на грбот на Пука.
- `S43` **DLG** — Гајдаџијата: „Мајко, самовилите ме наградија со злато!“
- `S44` **NAR** — Соседите се собраа да ја чујат чудната приказна.
- `S46` **NAR** — Но кога ја извади кесата, златниците беа исчезнати.
- `S47` **DLG** — Соседите: „Будалче! Те измамија!“
- `S48` **NAR** — Младичот не рече ништо. Ги подигна гајдите.
- `S49` **NAR** — Штом засвире, неговата песна беше совршена.
- `S50` **NAR** — Од тој ден, сите знаеја дека тој е најдобриот гајдаџија на сите времиња.

---

## 5. Acceptance criteria (testable)

1. Shot count = 50 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
| 1 | DD HEADWEAR: no cap/hood/bandana/mask on head; hood = back-cowl only (cape-like); bare head + teal-blue glowing hair always visible; any head/face covering = REJECT |
| 2 | LEGENDARY WEAPONS MUST APPEAR: DD = twin Frostbite-class hand crossbows (ice-blue arcane crystal limbs, frost runes, frozen-light string, teal-blue glow); AZ = Dawnbreaker-class greatsword (pale sunsteel, molten-gold runes, golden holy fire edge, sunburst crossguard); hero sheet/keyframe without weapon = INCOMPLETE |
| 3 | WEAPON ANTI-SLOP: fantasy construction only; crossbow must NEVER read as firearm (no barrel/magazine/stock/Uzi/SMG silhouette = REJECT); anti-slop negatives always appended |
| 4 | BOSS FACE: Mal'garot HAS a prolific molten-lava face (lava dripping/running, drops falling to ground); faceless boss sheets SUPERSEDED |
| 5 | LOCATION BRIGHTNESS FLOOR: environment plates silhouette-readable at thumbnail; no murk-dark grades |

**Anti-slop negatives (always appended):** `firearm, gun, machinegun, Uzi, barrel, magazine, ammo clip, muzzle, modern weapon`

> Activates when face_lock changes from AI-default to an enrolled identity (DD/AZ). AI-default packages carry this as a forward constraint, not a current defect.

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
