# 18 — Сусану и Ороки (Susanoo and Orochi)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Сусану и Ороки** — Богот на бурите Сусану слегува на Земјата за да го порази осумглавиот змеј Ороки и да ја спаси саканата Кушинада — со гром и божествен меч.

*Genre:* Јапонска легенда · епска акција

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
| Сусану / Susanoo | Богот на бурите, храбар и решителен; воинствен, но благороден и длабоко вљубен во Кушинада | story-suggested | AI-default |
| Ороки / Orochi | Колосален змеј со осум глави и осум опашки, тело што зафаќа осум долини и осум рида; суетен и арогантен | story-suggested | AI-default |
| Кушинада / Kushinada | Млада убава девојка, следната жртва на чудовиштето; нежна и храбра | story-suggested | AI-default |
| Селаните / The Villagers | Плашени луѓе кои од страв за своите домови ги исполнуваат условите на чудовиштето | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~150.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Богот на бурите Сусану слегува од небото. Го откриваме земјата на осумте долини и рида и огромниот змеј Ороки, кој штотуку испил осум буриња вино и спие. Во селото, како следна жртва, ја среќаваме Кушинада.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | WIDE | eye-level | crane-up | moderate | 3.0s | NAR |
| S03 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S04 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S05 | WIDE | high-angle | pan-right | moderate | 3.0s | NAR |
| S06 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S07 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S08 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S09 | CLOSE | macro | static | gentle | 3.0s | NAR |
| S10 | INSERT | eye-level | static | gentle | 2.5s | NAR |
| S11 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S12 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S13 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S14 | WIDE | eye-level | static | moderate | 3.5s | NAR |

### Act II — Сукоб

*Сусану со гром го буди Ороки. Започнува вербален и физички судир: змејот се потсмева и напаѓа, но Сусану, вљубен во Кушинада, го извлекува својот божествен меч и собира моќ од бурата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S16 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S17 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S18 | WIDE | low-angle | pan-left | moderate | 3.5s | NAR |
| S19 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | NAR |
| S20 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S21 | CLOSE | low-angle | static | gentle | 3.0s | DLG |
| S22 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S23 | MEDIUM | over-shoulder | track | moderate | 3.0s | DLG |
| S24 | CLOSE | low-angle | push-in | gentle | 2.5s | DLG |
| S25 | CLOSE | eye-level | shot-reverse | gentle | 3.0s | DLG |
| S26 | INSERT | eye-level | static | gentle | 2.5s | NAR |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S29 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S30 | CLOSE | low-angle | static | gentle | 3.0s | NAR |
| S31 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S32 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S33 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S34 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S35 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S36 | CLOSE | low-angle | push-in | gentle | 2.5s | NAR |
| S37 | INSERT | macro | static | gentle | 2.5s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |

### Act III — Расплет

*Сусану ги совладува осумте глави на Ороки една по една, се шегува над победениот змеј, се соединува со Кушинада и останува да ги штити луѓето.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | high-angle | crane-up | action | 3.5s | NAR |
| S40 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S41 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S42 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S43 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S44 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | NAR |
| S45 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S46 | WIDE | high-angle | crane-down | moderate | 4.0s | DLG |
| S47 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S48 | WIDE | eye-level | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Високо над светот, меѓу облаците и молњите, живееше Сусану, богот на бурите.
- `S02` **NAR** — Под небото на бурите се протегаше земја од осум долини и осум рида.
- `S03` **NAR** — Сусану, воин и заштитник, зачекори низ небото.
- `S04` **NAR** — Во неговото срце гореше светлата молња на правдата.
- `S05` **NAR** — Еден ден, тој слезе на Земјата кај страшниот змеј Ороки.
- `S06` **NAR** — Таму живееше Ороки, змеј од осум глави и осум опашки, чие тело зафаќаше осум долини и осум рида.
- `S07` **NAR** — Ороки беше толку огромен што неговите глави допираа до облаците.
- `S08` **NAR** — Неговите крлушки беа тврди како железо, а од ноздрите му излегуваше пареа.
- `S09` **NAR** — Змејот штотуку испи осум буриња оризово вино и грчеше многу гласно.
- `S10` **NAR** — Осум празни буриња вино лежеа истурени покрај него.
- `S11` **NAR** — А во подножјето на планината, луѓето живееја во страв.
- `S12` **NAR** — Следна жртва на чудовиштето требаше да биде убавата Кушинада.
- `S13` **NAR** — Таа знаеше што ја чека, но не губеше надеж.
- `S14` **NAR** — А од ридот над селото, сè гледаше Сусану.
- `S15` **NAR** — Сусану зачекори кон заспаниот змеј, а ветрот го следеше.
- `S16` **NAR** — Тогаш Сусану плесна со рацете.
- `S17` **NAR** — Одекна татнеж на гром што ги затресе планините.
- `S18` **NAR** — Ороки почна да се буди, глава по глава.
- `S19` **NAR** — Малечкиот бог стоеше неподвижно пред чудовиштето.
- `S20` **NAR** — Осум пара очи блеснаа во мракот.
- `S21` **DLG** — Ороки: „Што бараш овде?“
- `S22` **DLG** — Сусану: „Дојдов да те спречам да ги повредуваш луѓето.“
- `S23` **DLG** — Сусану: „Имаш лоша навика — јадеш млади девојки како да се сочни портокали!“
- `S24` **DLG** — Ороки: „Нивните родители сами ми ги нудат!“
- `S25` **DLG** — Сусану: „А ако не го направат тоа, ќе им ги запалиш куќите!“
- `S26` **NAR** — Всушност, Сусану беше длабоко вљубен во Кушинада.
- `S27` **NAR** — Тој немаше да дозволи чудовиштето да ѝ наштети.
- `S28` **NAR** — Така започна судирот на небото и бездната.
- `S29` **NAR** — Ороки му се потсмеваше, сигурен дека е непобедлив.
- `S30` **NAR** — Чудовиштето не ја виде опасноста во неговите очи.
- `S31` **NAR** — Ороки замавна со своите осум глави.
- `S32` **NAR** — Но ниту една глава не можеше да го допре.
- `S33` **NAR** — Неговата рака се склучи врз древната дршка.
- `S34` **NAR** — Тој го извлече својот божествен меч.
- `S35` **NAR** — Небото се собра над него во виор.
- `S36` **NAR** — Во очите на Ороки блесна првата сенка на сомнеж.
- `S37` **NAR** — Мечот беше полн со светлината на бурите.
- `S38` **NAR** — Еден миг молчење — а потоа блесок.
- `S39` **NAR** — Сусану скокна, и мечот запеа низ воздухот.
- `S40` **NAR** — Првата глава беше совладана во блесок.
- `S41` **NAR** — Втора и трета глава паднаа една по друга.
- `S42` **NAR** — Мечот не запираше.
- `S43` **NAR** — Огромното тело почна да попушта.
- `S44` **NAR** — Остана последната, средишна глава.
- `S45` **NAR** — И тогаш — последниот блесок.
- `S46` **DLG** — Сусану: „Не мислеше трезвено, пријателе. Сакето ти удрило во... главите! Хахахаха!“
- `S47` **NAR** — Потоа Сусану се спушти кај Кушинада, и им се врати на луѓето.
- `S48` **NAR** — Сусану се ожени со Кушинада и живееше меѓу луѓето, штитејќи ги од нивните непријатели.

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
