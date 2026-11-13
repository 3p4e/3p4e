# 32 — Василиса и Баба Јага (Vasilisa and Baba Yaga)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Василиса и Баба Јага** — Млада Василиса, благословена со волшебна кукла, ја преживува загубата на мајка си, суровоста на маќеата и искушението на Баба Јага, за на крај да најде љубов во царскиот дворец.

*Genre:* Легенда · епска акција

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
| Василиса / Vasilisa | Прекрасна, кротка и храбра млада жена; хероина со волшебна кукла. | story-suggested | AI-default |
| Мајката / The Mother | Бледа, нежна жена на самртна постела; и ја дава куклата на ќерка си. | story-suggested | AI-default |
| Таткото трговец / The Merchant Father | Богат руски трговец со долга брада; заминува на пат. | story-suggested | AI-default |
| Маќеата / The Stepmother | Строга, завистлива жена во темни руски алишта. | story-suggested | AI-default |
| Посестрите (2) / Stepsisters (2) | Разгалени, надмени млади жени во скапи алишта. | story-suggested | AI-default |
| Куклата / The Magic Doll | Мала дрвена кукла со благ сјај; чуварка и советничка. | story-suggested | AI-default |
| Баба Јага / Baba Yaga | Ужасна вештерка со остри црти; живее во колиба на пилешки нозе. | story-suggested | AI-default |
| Старата шивачка / The Old Seamstress | Добра, вешта старица; ја прима Василиса во градот. | story-suggested | AI-default |
| Царот / The Tsar | Царствен, млад владетел; се восхитува и се вљубува во Василиса. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~161.0s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Раѓањето на Василиса, смртта на мајка ѝ и подарокот на волшебната кукла; строгата маќеа и разгалените посестри; преселбата на работ на темната шума.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | crane-down | crane-down | action | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S03 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S04 | INSERT | macro | push-in | action | 3.0s | NAR |
| S05 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S06 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |
| S07 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S08 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S09 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S10 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.0s | NAR |
| S11 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S12 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S13 | WIDE | eye-level | pan-left | action | 3.0s | NAR |
| S14 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |

### Act II — Искушението

*Василиса е испратена по оган кај Баба Јага; преживува со куклата, служи верно, добива стап со череп и ја победува злобата на маќеата и посестрите.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S16 | INSERT | macro | pull-back | action | 3.0s | NAR |
| S17 | MEDIUM | low-angle | static | moderate | 3.0s | DLG |
| S18 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S19 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S21 | INSERT | macro | push-in | action | 3.0s | NAR |
| S22 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S23 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S24 | INSERT | macro | pan-left | action | 3.0s | NAR |
| S25 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S26 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.0s | DLG |
| S29 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S30 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S31 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S32 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S33 | WIDE | eye-level | pan-right | action | 3.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | INSERT | macro | push-in | action | 3.5s | NAR |
| S36 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S37 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S39 | LOW | low-angle | push-in | moderate | 3.0s | NAR |
| S40 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |

### Act III — Нов живот

*Бегство во градот, вештината на генијална шивачка, препознавање од царот и величествената венчавка со саканата кукла крај неа.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S41 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S42 | WIDE | crane-up | crane-up | action | 3.5s | NAR |
| S43 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S45 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S46 | WIDE | eye-level | crane-down | action | 3.5s | NAR |
| S47 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S48 | MEDIUM | over-shoulder | push-in | moderate | 3.5s | NAR |
| S49 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S50 | CLOSE | eye-level | pull-back | gentle | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Пред многу години, во една снежна руска варош, живееше богат трговец со своето семејство.
- `S02` **NAR** — Мајката на Василиса се разболе и лежеше бледа во својата одаја.
- `S03` **NAR** — Знаејќи дека ѝ одѕвонува, таа ја повика ќерка си за последен подарок.
- `S04` **NAR** — „Кога ќе ти биде тешко, зборувај со неа. Ќе ти помогне.“ – ѝ прошепоти мајката.
- `S05` **NAR** — Василиса ја притисна куклата до гради и тивко заплака.
- `S06` **NAR** — Кога мајката си отиде, куќата остана празна и тивка.
- `S07` **NAR** — Годините минаа, а таткото се прежени со една строга жена што носеше две разгалени ќерки.
- `S08` **NAR** — Новите домаќинки гледаа со презир на сè наоколу.
- `S09` **NAR** — Сите најтешки домашни работи паднаа на плеќите на Василиса.
- `S10` **NAR** — Маќеата не жалеше остри зборови за падорицата.
- `S11` **NAR** — Една вечер таткото објави дека заминува на долг трговски пат.
- `S12` **NAR** — Целото семејство се пресели во куќа на самиот раб на темната шума.
- `S13` **NAR** — За таа шума се шушкаше дека е дом на ужасната вештерка Баба Јага.
- `S14` **NAR** — Гледајќи кон шумата, Василиса ја стегна куклата како талисман.
- `S15` **NAR** — Маќеата, сакајќи да се ослободи од Василиса, смисли опасен план.
- `S16` **NAR** — Огништето беше намерно згаснато – без искра, без оган.
- `S17` **NAR** — „Оди во шумата кај Баба Јага и донеси оган.“ – нареди маќеата.
- `S17` **DLG** — Маќеата: „Оди во шумата и донеси оган, па додека можеш.“
- `S18` **NAR** — Василиса ја грабна својата кукла и, без збор, тргна кон шумата.
- `S19` **NAR** — Таа потона во темната шума, меѓу високи стебла што го голтаа месечниот сјај.
- `S20` **NAR** — Секој крцот и сенка ѝ се чинеше како нешто што демне.
- `S21` **NAR** — Во нејзиниот џеб, куклата тихо сјаеше, бодрејќи ја да продолжи.
- `S22` **NAR** — Пред неа се издигна колибата на Баба Јага – поставена на огромни пилешки нозе.
- `S23` **NAR** — Василиса застана скаменета од страв, а срцето ѝ удираше како чекан.
- `S24` **NAR** — Ѕидовите беа од стара коска, а оградата – низа бели черепи.
- `S25` **NAR** — Собирајќи ја сета храброст, Василиса стапна напред и тропна на вратата.
- `S26` **NAR** — Вратата се отвори со крцот, а на прагот застана самата вештерка.
- `S27` **NAR** — Очите на Баба Јага пробиваа како искри.
- `S28` **NAR** — Василиса ѝ објасни зошто дошла – ѝ требаше оган за своето огниште.
- `S28` **DLG** — Василиса: „Дојдов да ве замолам за малку оган за нашиот дом.“
- `S29` **NAR** — „Ќе ти дадам што ти треба – ама прво ќе ми помогнеш во моите работи.“
- `S29` **DLG** — Баба Јага: „Ќе ти дадам оган, ама мора да останеш и да ми служиш.“
- `S30` **NAR** — Василиса кимна и се фати за работа – да мете, да готви и да чисти.
- `S31` **NAR** — Скришно, куклата ѝ помагаше – шепотејќи совети и завршувајќи ги тешките работи.
- `S32` **NAR** — Баба Јага оддалеку гледаше и, задоволна, се насмевна.
- `S33` **NAR** — Седмиците минуваа брзо; колибата светеше чиста и уредна.
- `S34` **NAR** — Задоволна од нејзиното однесување, вештерката реши да ја награди.
- `S35` **NAR** — Од градите извади стап, а на неговиот врв – череп со два сјајни дијаманта за очи.
- `S36` **NAR** — „Ова ќе ти даде оган. Покажи им го на маќеата и на посестрите.“
- `S36` **DLG** — Баба Јага: „Земи го. Кога ќе биде потребно, покажи го – ќе добиеш оган.“
- `S37` **NAR** — Со стапот во рака, Василиса се упати назад низ шумата – кон дома.
- `S38` **NAR** — Кога стигна, на вратата ја чекаа маќеата и двете посестри.
- `S39` **NAR** — Василиса го крена стапот високо кон трите жени.
- `S40` **NAR** — Очите на черепот светнаа толку силно што светлината ги победи трите жени.
- `S41` **NAR** — Исплашена од сè што се случи, Василиса побегна низ ноќта.
- `S42` **NAR** — Стигна во големиот град, под неговите бели кули и златни покриви.
- `S43` **NAR** — Една добра старица, вешта шивачка, ја прими под својот покрив.
- `S44` **NAR** — Со куклата секогаш покрај себе, Василиса шиеше ден и ноќ.
- `S45` **NAR** — Нејзините везови станаа толку фини што сите ги споредуваа со чуда.
- `S46` **NAR** — Гласот за нејзините изработки стигна и до самиот царски дворец.
- `S47` **NAR** — Царот им се восхитуваше на изработките и посака да ја запознае шивачката.
- `S48` **NAR** — Кога ја виде убавата Василиса, царот во истиот миг се вљуби.
- `S49` **NAR** — Набрзо се одржа и величествената венчавка.
- `S50` **NAR** — Татко ѝ присуствуваше, како и старата шивачка... и, се разбира, саканата кукла.

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
