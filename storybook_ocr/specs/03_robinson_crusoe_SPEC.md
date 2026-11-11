# 03 — Островот на Робинсон Крусо (Robinson Crusoe)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **49 shots** (floor 40).

---

## 0. Concept

**Островот на Робинсон Крусо** — A young Englishman shipwrecked on a deserted island survives alone, befriends a castaway native he names Friday, and together they outwit mutineers to sail home.

*Genre:* Авантура · морска сага

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
| Робинсон Крусо | Млад Англичанец, упорен, снаодлив и храбар | story-suggested | AI-default |
| Петко | Спасен домородец, верен и благодарен пријател | story-suggested | AI-default |
| Капетанот | Капетан на британскиот брод, праведен водач | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**49 shots · ~155.0s runtime · 247.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Робинсон Крусо запловува во потрага по авантури, но страшна бура го потонува бродот и тој завршува сам на далечен остров.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S02 | MEDIUM | low-angle | push-in | moderate | 3.0s | DLG |
| S03 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S04 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S05 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S06 | INSERT | high-angle | static | gentle | 2.5s | NAR |
| S07 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |
| S08 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S09 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S10 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S11 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S12 | MEDIUM | low-angle | pull-back | moderate | 3.0s | NAR |

### Act II — Опасноста и пријателството

*На островот, Робинсон открива човечки траги, го спасува врзаниот Петко и тие стануваат неразделни пријатели, чекајќи спас.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S14 | INSERT | macro | static | gentle | 2.5s | NAR |
| S15 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S17 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S18 | INSERT | high-angle | static | gentle | 2.5s | NAR |
| S19 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S20 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S21 | MEDIUM | over-shoulder | static | moderate | 3.0s | NAR |
| S22 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S23 | CLOSE | over-shoulder | push-in | gentle | 3.0s | NAR |
| S24 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S25 | INSERT | macro | static | gentle | 2.5s | NAR |
| S26 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S29 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S30 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S31 | CLOSE | eye-level | pan-right | gentle | 3.0s | NAR |
| S32 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S33 | WIDE | eye-level | track | moderate | 3.5s | DLG |
| S34 | INSERT | high-angle | static | gentle | 2.5s | NAR |
| S35 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |

### Act III — Спасение

*Британски брод пристигнува, но морнарите се побуниле. Робинсон и Петко му помагаат на капетанот да си го врати бродот и заминуваат кон дома.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S36 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S37 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | track | moderate | 3.0s | DLG |
| S39 | MEDIUM | low-angle | static | moderate | 3.0s | DLG |
| S40 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S41 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S42 | WIDE | low-angle | pan-right | moderate | 3.0s | NAR |
| S43 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | NAR |
| S44 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S45 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S46 | CLOSE | eye-level | shot-reverse | gentle | 3.5s | DLG |
| S47 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S48 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S49 | MEDIUM | eye-level | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Младиот Англичанец Робинсон Крусо сонуваше за далечни мориња и големи авантури.
- `S02` **DLG** — Робинсон: „Еј! Отпловувам во потрага по авантури!“
- `S03` **NAR** — Првите денови на море беа мирни, небото чисто и водата спокојна.
- `S04` **NAR** — Но наеднаш, небото се затемни и брановите пораснаа.
- `S05` **NAR** — Страшна бура го зафати бродот со големи бранови и силни ветришта.
- `S06` **NAR** — Со татнеж, јарболот се скрши.
- `S07` **NAR** — Бродот потона во бурата, а Робинсон остана единствениот преживеан.
- `S08` **NAR** — Држејќи се за парче дрво, тој се предаде на струјата.
- `S09` **NAR** — Струјата го носеше кон еден далечен остров среде океанот.
- `S10` **NAR** — Кога се разбуди, лежеше на една осамен плажа.
- `S11` **NAR** — Околу него немаше никој — само растенија и дрвја.
- `S12` **NAR** — Сепак, Робинсон не се предаде — реши да преживее.
- `S13` **NAR** — Си направи колиба додека чекаше да дојде некој да го спаси.
- `S14` **NAR** — Од гранки и лисја го крена својот дом.
- `S15` **NAR** — Деновите минуваа, а тој чекаше спас.
- `S16` **NAR** — Во колибата, тој ги бележеше деновите и чекаше.
- `S17` **NAR** — Едно утро, шетајќи по плажата, виде нешто чудно.
- `S18` **NAR** — Отпечаток од човечко стапало — поголемо од неговото.
- `S19` **NAR** — Срцето му чукаше силно — не беше сам на островот.
- `S20` **NAR** — Потоа слушна гласови и сфати дека не беше единствениот човек на островот.
- `S21` **NAR** — Се сокри зад грмушки и погледна.
- `S22` **NAR** — Виде неколку домородци како врзаа еден друг домородец.
- `S23` **NAR** — Го оставија самиот, беспомошен, и си заминаа.
- `S24` **NAR** — Кога заминаа, Робинсон се приближи до него.
- `S25` **NAR** — Внимателно го одврза.
- `S26` **DLG** — Робинсон: „Ќе те викам Петко.“
- `S27` **NAR** — Од тој ден, тие станаа неразделни пријатели.
- `S28` **NAR** — Тие делеа работа, храна и надеж.
- `S29` **NAR** — Заедно ловеа, рибареа и се смееја.
- `S30` **NAR** — Годините минуваа полека.
- `S31` **NAR** — Робинсон никогаш не престана да гледа кон хоризонтот.
- `S32` **NAR** — И едно утро, конечно...
- `S33` **DLG** — Робинсон: „Брод! Гледај, Петко — брод!“
- `S34` **NAR** — Имаше британско знаме.
- `S35` **DLG** — Робинсон: „Ќе можам да се вратам дома!“
- `S36` **NAR** — Веднаш се упатија кон плажата.
- `S37` **NAR** — Таму видоа морнари кои оставија тројца врзани офицери на песокот и заминаа во густежот.
- `S38` **DLG** — Капетанот: „Јас сум капетанот на бродот. Моите морнари се побунија.“
- `S39` **DLG** — Робинсон: „Ќе ви помогнеме да си го вратите бродот!“
- `S40` **NAR** — Во текот на ноќта, Робинсон и Петко допливаа до бродот.
- `S41` **NAR** — Се прикрадоа на него незабележани.
- `S42` **NAR** — Бунтовниците шетаа по палубата без да знаат.
- `S43` **NAR** — Еден по еден, ги фаќаа бунтовниците.
- `S44` **NAR** — Ги заклучуваа во делот за товар.
- `S45` **NAR** — Капетанот повторно ја презеде командата.
- `S46` **DLG** — Робинсон: „Мораме да се збогуваме, Петко.“ Петко: „Доаѓам со тебе во Англија!“
- `S47` **NAR** — По неколку седмици на море, копното се појави.
- `S48` **NAR** — Облечени во нови алишта, слегоа на пристаништето.
- `S49` **NAR** — И останаа пријатели засекогаш.

---

## 5. Acceptance criteria (testable)

1. Shot count = 49 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
