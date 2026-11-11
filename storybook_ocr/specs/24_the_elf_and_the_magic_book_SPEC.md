# 24 — Виленикот и волшебната книга (The Elf and the Magic Book)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **44 shots** (floor 40).

---

## 0. Concept

**Виленикот и волшебната книга** — Ситен виленик од бакалница следи еден студент и открива дека стара скината книга крие волшебно дрво од светлина — и мора да избере меѓу вкусниот оброк и поголемото богатство.

*Genre:* Бајка · фантазија

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
| Виленикот / The Elf | ситен, милолик, љубопитен; земјени бои, зашилени уши | story-suggested | AI-default |
| Бакалот / The Grocer | округлест, добродушен трговец со престилка и топла насмевка | story-suggested | AI-default |
| Студентот / The Student | млад, љубезен, зачудувачки читател со торбичка со книги | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**44 shots · ~133.0s runtime · 221.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Во топлата бакалница ситниот виленик живее од чинијата ориз и путер на добриот бакалот. Една вечер студент влегува и ја купува старата скината книга со која бакалот го завиткувал кашкавалот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S03 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S04 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S05 | CLOSE | macro | static | gentle | 3.0s | NAR |
| S06 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S07 | WIDE | eye-level | slow track | moderate | 3.0s | NAR |
| S08 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S10 | INSERT | macro | static | gentle | 3.0s | NAR |
| S11 | CLOSE | eye-level | push-in | gentle | 2.5s | DLG |
| S12 | SHOT-REVERSE | over-shoulder | static | gentle | 3.0s | DLG |
| S13 | CLOSE | high-angle | static | gentle | 3.0s | NAR |
| S14 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |

### Act II — Волшебната книга

*Налутен, виленикот го следи студентот до неговата соба и гледа како од книгата излегува зрак светлина што се претвора во прекрасно дрво со цветови и овошја сјајни како ѕвезди.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | pull-back | moderate | 3.0s | NAR |
| S16 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S17 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S18 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S19 | INSERT | macro | static | gentle | 3.0s | NAR |
| S20 | CLOSE | eye-level | push-in | gentle | 2.5s | DLG |
| S21 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S22 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S23 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S24 | MACRO | macro | static | gentle | 3.0s | NAR |
| S25 | MACRO | macro | static | gentle | 3.0s | — |
| S26 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S27 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S28 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S29 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S30 | MACRO | macro | static | gentle | 3.0s | NAR |
| S31 | WIDE | low-angle | static | moderate | 3.0s | DLG |
| S32 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S33 | WIDE | eye-level | pull-back | moderate | 3.0s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S36 | WIDE | eye-level | static | moderate | 3.0s | NAR |

### Act III — Поголемото богатство

*Виленикот не може да живее без храната на бакалот, но секоја вечер се враќа кај волшебното дрво — зашто прекрасната книга е поголемо богатство.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S38 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S39 | WIDE | eye-level | crossfade | moderate | 3.0s | NAR |
| S40 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S41 | MEDIUM | low-angle | crane-up | moderate | 3.5s | NAR |
| S42 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S43 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S44 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во еден стар европски град, под калдрмата, тивко стоеше една мала бакалница.
- `S02` **NAR** — Внатре, меѓу рафтовите со намирници, беше топло и мирисаше на зачини.
- `S03` **NAR** — Таму, во едно ковче, живееше ситниот виленик.
- `S04` **NAR** — А добриот бакалот секој ден му носеше чинија ориз со путер.
- `S05` **NAR** — Тоа беше навистина вкусен оброк!
- `S06` **DLG** — Виленик: „Ммм, навистина вкусно!“
- `S07` **NAR** — Така си живееја двајцата — во мир и тишина.
- `S08` **NAR** — Една вечер вратата се отвори и влезе еден студент.
- `S09` **DLG** — Студент: „Добар вечер. Едно парче кашкавал, ве молам.“
- `S10` **NAR** — Но студентот забележа дека бакалот го завиткува кашкавалот во страници скинати од стара книга.
- `S11` **DLG** — Студент: „Што правите со таа книга? Побарајте... да ја купам целата.“
- `S12` **DLG** — Бакалот: „Се разбира! И онака не ми треба.“
- `S13` **NAR** — Момчето се насмеа: „Сигурен сум дека не ти треба.“
- `S14` **NAR** — А виленикот се налути — помисли дека студентот е дрзок со неговиот заштитник.
- `S15` **NAR** — И така, реши да го следи, за да си поигра мајтап со него.
- `S16` **NAR** — Тивко го следеше низ улиците.
- `S17` **NAR** — Дури до неговата скромна соба.
- `S18` **NAR** — Студентот ја извади скинатата книга и ја отвори.
- `S19` **NAR** — Тогаш, од страниците излезе зрак светлина.
- `S20` **DLG** — Студент: „Што е ова...?“, шепоти зачуено.
- `S21` **NAR** — Светлината растеше, придружена со милозвучна музика.
- `S22` **NAR** — И зракот полека се претвори во дрво.
- `S23` **NAR** — Дрво на кое натежнуваа цветови и овошја.
- `S24` **NAR** — Сјајни како ѕвезди.
- `S26` **NAR** — Студентот гледаше во чудото.
- `S27` **NAR** — А од сенките, виленикот гледаше вчудовидено.
- `S28` **NAR** — Целата соба се претвори во волшебна градина.
- `S29` **NAR** — Виленикот пријде поблиску, не можеше да одолее.
- `S30` **NAR** — Секој цвет светеше како мала ѕвезда.
- `S31` **DLG** — Виленик: „Сакам да останам тука засекогаш...“
- `S32` **DLG** — Виленик: „...ама момчето не ми дава ориз и путер!“
- `S33` **NAR** — Но дрвото блескаше поубаво од се.“
- `S34` **NAR** — Музиката се разлеваше низ собата.
- `S35` **DLG** — Виленик: „Сепак, ќе дојдам уште еднаш...“
- `S36` **NAR** — И така, утрото се врати дома.
- `S37` **NAR** — Бакалот, како и секој ден, му приготви чинија ориз со путер.
- `S38` **DLG** — Виленик: „Фала, бакале. Не можам без оваа храна.“
- `S39` **NAR** — Но од тој ден, секоја вечер се враќаше кај студентот.
- `S40` **NAR** — Не можеше да живее без храната на бакалот, но прекрасната книга беше поголемо богатство.
- `S41` **NAR** — Секоја вечер го чекаше дрвото од светлина.
- `S42` **NAR** — И со него, малиот виленик — среќен.
- `S43` **NAR** — Зашто некои богатства не се јадат — но го хранат срцето.
- `S44` **NAR** — Крај.

---

## 5. Acceptance criteria (testable)

1. Shot count = 44 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
