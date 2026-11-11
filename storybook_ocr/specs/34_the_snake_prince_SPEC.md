# 34 — Принцот змија (The Snake Prince)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Принцот змија** — Млад принц, роден од змија, ја крие својата тајна од саканата принцеза — додека една исповед не го врати во лушпите, а нејзината храброст не го избави засекогаш.

*Genre:* Легенда · љубовна бајка

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
| Принцот / The Prince | Нежен млад принц со тајно потекло од змија; во змиска форма — тиркизно-златна змија. | story-suggested | AI-default |
| Принцезата / The Princess | Храбра, верна сопруга од соседното кралство. | story-suggested | AI-default |
| Кралот / The King | Благороден владетел на индиското кралство. | story-suggested | AI-default |
| Кралицата / The Queen | Нежна владетелка и посвоена мајка. | story-suggested | AI-default |
| Кралот на змиите / The Snake King | Најголема, највеличествена змија со крунообразни лушпи и светкави очи. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~164.0s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба и чудото

*Индиско кралство копнее по наследник; змија се шмугнува во фустанот на кралицата, а наутро во него е новороденче. Кралот и кралицата го одгледуваат како принц.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S04 | MACRO | macro | push-in | gentle | 3.0s | NAR |
| S05 | MEDIUM | low-angle | pan-right | moderate | 3.0s | NAR |
| S06 | INSERT | macro | static | gentle | 3.0s | NAR |
| S07 | WIDE | eye-level | push-in | moderate | 3.5s | NAR |
| S08 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S09 | CLOSE-UP | over-shoulder | static | gentle | 3.0s | NAR |
| S10 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S11 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S12 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S13 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S14 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |

### Act II — Љубовта и тајната

*Принцот се жени за принцезата од соседното кралство и живее среќно, но тајната за своето потекло го тежи. Кога ќе се обиде да ѝ признае, повторно се претвора во змија и заминува; принцезата тажи со месеци и слуша порака во сонот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | NAR |
| S17 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S18 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S19 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S21 | WIDE | high-angle | pan-left | moderate | 3.0s | NAR |
| S22 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S23 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S24 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S25 | MEDIUM | eye-level | pull-back | moderate | 3.5s | NAR |
| S26 | CLOSE-UP | over-shoulder | push-in | gentle | 3.0s | NAR |
| S27 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S28 | CLOSE-UP | eye-level | static | gentle | 3.5s | DLG |
| S29 | CLOSE-UP | over-shoulder | static | gentle | 3.0s | NAR |
| S30 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S31 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S32 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S33 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S34 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S35 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S36 | WIDE | high-angle | pan-right | moderate | 3.5s | NAR |
| S37 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S38 | INSERT | macro | push-in | gentle | 3.5s | DLG |

### Act III — Млекото и враќањето

*Принцезата става сад со млеко до вратата; од реката доаѓаат сите змии, а меѓу нив и кралот на змиите. Таа храбро го моли да ѝ го врати мажот; големиот змиски крал ги склопува очите и принцот излегува од лушпите. Двајцата се прегрнуваат и остануваат заедно засекогаш.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S40 | CLOSE-UP | macro | static | gentle | 3.0s | NAR |
| S41 | WIDE | low-angle | pan-right | moderate | 3.5s | NAR |
| S42 | MEDIUM | high-angle | push-in | moderate | 3.5s | NAR |
| S43 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S44 | WIDE | low-angle | crane-up | action | 3.5s | NAR |
| S45 | CLOSE-UP | over-shoulder | static | gentle | 3.0s | NAR |
| S46 | CLOSE-UP | eye-level | static | gentle | 3.5s | DLG |
| S47 | CLOSE-UP | macro | push-in | gentle | 3.0s | NAR |
| S48 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S49 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S50 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во далечно индиско кралство, владетелите копнееја по наследник.
- `S02` **NAR** — Но небото остануваше тивко на нивната молитва.
- `S03` **NAR** — Еден ден, кралицата се капеше во реката.
- `S04` **NAR** — Од трските, една змијка се шмугна во џебот од фустанот.
- `S05` **NAR** — Завршено со капењето, кралицата го однесе фустанот кон палатата.
- `S06` **NAR** — Во темнината на џебот, гостинката чекаше тивко.
- `S07` **NAR** — Наредното утро, во фустанот ги дочека вистинско чудо.
- `S08` **NAR** — Кралицата го прегрна детето како одговор од небото.
- `S09` **NAR** — Кралот виде благослов и се поклони со благодарност.
- `S10` **NAR** — Години одминуваа, а момчето растеше сакано како свој син.
- `S11` **NAR** — Од дете во младич, принцот раснеше во градините на палатата.
- `S12` **NAR** — Ја учеа историјата, зборот и должностите на престолот.
- `S13` **NAR** — Но во неговите очи, нешто старо и ладнокрвно сè уште дремеше.
- `S14` **NAR** — Кога порасна, принцот беше подготвен да го започне својот пат.
- `S15` **NAR** — Патот го одведе во соседното кралство, кај принцезата.
- `S16` **NAR** — Во миризлива градина, двајцата се сретнаа за првпат.
- `S17` **NAR** — Принцезата почувствува како срцето ѝ забрзува.
- `S18` **NAR** — А принцот — веќе беше заробен од нејзината насмевка.
- `S19` **NAR** — Наскоро, две кралства се обединија со свечена венчавка.
- `S20` **NAR** — Со размена на цветни венци, ги врзаа своите животи.
- `S21` **NAR** — Настапи прослава преполна со музика, светла и смеа.
- `S22` **NAR** — Деновите им течеа благо, во заедничка среќа.
- `S23` **NAR** — Нејзината смеа ги исполнуваше сите одаи.
- `S24` **NAR** — Но зад неговата насмевка, тајната тежеше како камен.
- `S25` **NAR** — Ноќите го наоѓаа буден, со поглед кон реката.
- `S26` **NAR** — Ги погледна своите дланки и се сети од каде дошол.
- `S27` **NAR** — Една вечер, принцот одлучи да ѝ ја каже вистината.
- `S28` **NAR** — Рече дека има нешто што мора да го соопшти.
- `S28` **DLG** — Принцот: „Пред некое време... јас не бев човек.“
- `S29` **NAR** — Таа слушаше збунета, без да разбере што значи тоа.
- `S30` **NAR** — Ја отвори устата да доврши — но реченицата остана неречена.
- `S30` **DLG** — Принцот: „Јас бев... една змија.“
- `S31` **NAR** — Кожата му светна, а телото почна да се менува.
- `S32` **NAR** — Пред очите на сопругата, принцот се претвори во змија.
- `S33` **NAR** — Принцезата остана скаменета, со празен поглед кон вратата.
- `S34` **NAR** — Змијата замина, ползејќи кон реката од која дошла.
- `S35` **NAR** — Очајот ја собори, и солзите не престануваа.
- `S36` **NAR** — Месеци одминаа, а таа плачеше и чекаше, без здив од надеж.
- `S37` **NAR** — Најпосле, една вечер, заспа со тешко срце.
- `S38` **NAR** — Тогаш, во домот на соништата, слушна нежен, сигурен глас.
- `S38` **DLG** — Глас: „Стави сад со млеко до вратата и помоли се на кралот на змиите.“
- `S39` **NAR** — Следната вечер, таа стори како што ѝ беше кажано.
- `S40` **NAR** — Полната чаша светкаше, како покана во ноќта.
- `S41` **NAR** — Од реката почнаа да се појавуваат безброј змии.
- `S42` **NAR** — Тивко, сите влегоа во одајата и се собраа околу млекото.
- `S43` **NAR** — Тивко, со раздвоени јазици, пиеја од понуденото млеко.
- `S44` **NAR** — Тогаш, меѓу нив, се издигна највеличествената змија.
- `S45` **NAR** — Со голема храброст, таа ја погледна во очи.
- `S46` **NAR** — И со јасен глас, ја упати својата молба.
- `S46` **DLG** — Принцезата: „Ваше Височество, ве молам, вратете ми го мажот.“
- `S47` **NAR** — Животното ја слушаше — и полека, ги склопи очите.
- `S48` **NAR** — Од лескавите лушпи излезе принцот — повторно човек.
- `S49` **NAR** — Двајцата се прегрнаа, со солзи што печат од среќа.
- `S50` **NAR** — И оттогаш, заедно живееја среќно — засекогаш.

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
