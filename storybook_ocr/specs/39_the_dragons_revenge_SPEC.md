# 39 — Одмаздата на змејот (The Dragon's Revenge)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Одмаздата на змејот** — Водениот бог Гонг Гонг, лут од досадната должност, предизвикува поплави — сè додека огнениот бог Џу Ронг не го запре, а бесот на змејот не го скрши светиот столб помеѓу Земјата и Небото.

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
| Гонг Гонг / Gong Gong | Водениот бог — огромен змеј со црни крлушки, горделив и лесно лут | story-suggested | AI-default |
| Сјанглиу / Xiangliu | Помошничка на Гонг Гонг — змија со девет глави, подмолна и игрива | story-suggested | AI-default |
| Џу Ронг / Zhu Rong | Богот на огнот — строг и непоколеблив борец на тигар | story-suggested | AI-default |
| Тигарот / The Tiger | Верниот огнен тигар-товарник на Џу Ронг | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~158.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Вовед во древна Кина: водениот бог Гонг Гонг е здодевен од должноста да им дава имиња на реките и, на поттик на деветглавата змија Сјанглиу, реши да се побуни со поплави.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S03 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S04 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S05 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S06 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S07 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S08 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S09 | MEDIUM | low-angle | static | moderate | 3.0s | — |
| S10 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S11 | WIDE | high-angle | crane-down | action | 3.5s | — |

### Act II — Превртениот свет

*Гонг Гонг и Сјанглиу предизвикуваат цунами и поплави; од облаците на својот огнен тигар слегува богот Џу Ронг, кој со огнениот меч ја победува Сјанглиу.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S12 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S13 | MEDIUM | low-angle | track | moderate | 3.5s | DLG |
| S14 | WIDE | eye-level | pan-right | action | 3.0s | NAR |
| S15 | MACRO | macro | push-in | gentle | 3.0s | — |
| S16 | MEDIUM | eye-level | static | moderate | 3.0s | — |
| S17 | WIDE | low-angle | crane-up | action | 3.5s | NAR |
| S18 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S19 | MEDIUM | low-angle | push-in | moderate | 3.5s | — |
| S20 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S21 | MEDIUM | over-shoulder | static | moderate | 3.0s | — |
| S22 | WIDE | eye-level | static | moderate | 3.5s | DLG |
| S23 | CLOSE | low-angle | static | gentle | 3.0s | DLG |
| S24 | MEDIUM | eye-level | static | moderate | 3.0s | — |
| S25 | INSERT | macro | push-in | gentle | 3.0s | — |
| S26 | WIDE | high-angle | track | moderate | 3.5s | — |
| S27 | MEDIUM | low-angle | pan-left | action | 3.0s | — |
| S28 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | — |
| S29 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S30 | WIDE | eye-level | static | action | 3.5s | DLG |
| S31 | MEDIUM | high-angle | static | moderate | 3.5s | NAR |
| S32 | CLOSE | low-angle | static | action | 3.0s | — |
| S33 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S34 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S35 | WIDE | high-angle | static | action | 3.5s | NAR |
| S36 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |

### Act III — Одмазда на столбот

*Обезумен од бес и пораз, Гонг Гонг со главата го удира светиот столб Буџоу, расцепувајќи го столбот меѓу Земјата и Небото; сфаќа дека претерал и засекогаш се крие од огнениот меч на Џу Ронг.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | WIDE | eye-level | track | moderate | 3.5s | — |
| S38 | CLOSE | low-angle | macro | gentle | 3.0s | — |
| S39 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S40 | INSERT | macro | push-in | gentle | 3.0s | — |
| S41 | WIDE | high-angle | crane-up | action | 3.5s | NAR |
| S42 | WIDE | eye-level | pan-left | action | 3.5s | NAR |
| S43 | MEDIUM | high-angle | track | moderate | 3.5s | NAR |
| S44 | CLOSE | eye-level | static | gentle | 3.0s | — |
| S45 | WIDE | eye-level | static | action | 3.5s | — |
| S46 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S47 | WIDE | high-angle | crane-down | action | 3.5s | — |
| S48 | WIDE | low-angle | static | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во древна Кина, високо над свиените реки, живееше водениот бог Гонг Гонг.
- `S02` **NAR** — Негова должност беше да му даде име на секое езеро и секоја река.
- `S03` **NAR** — Но списокот немаше крај, а задачата му беше страшно здодевна.
- `S04` **DLG** — Гонг Гонг: „Ова веќе не можам да го поднесам, Сјанглиу.“
- `S05` **DLG** — Сјанглиу: „И јас, господару. Секој ден исто.“
- `S06` **DLG** — Гонг Гонг: „Зошто да не се побуниме? Да направиме цунами и поплави!“
- `S07` **DLG** — Гонг Гонг: „Толку ќе се забавуваме!“
- `S08` **NAR** — Двајцата се кренаа и небото наеднаш се замрачи.
- `S10` **NAR** — И тргнаа да го превртат светот наопаку.
- `S12` **NAR** — Цунами проголтаа полиња, а реките се излеаја од коритата.
- `S13` **DLG** — Гонг Гонг: „Ха! Гледај како бега светот!“
- `S14` **NAR** — Селата и полињата потонаа под надојдената вода.
- `S17` **NAR** — Но тогаш облаците се распукаа и силна светлина слезе од небото.
- `S18` **NAR** — Од облаците на својот тигар слезе Џу Ронг, богот на огнот.
- `S22` **DLG** — Џу Ронг: „Престанете!“
- `S23` **DLG** — Гонг Гонг: „А што ќе ми направиш ако не запрам?“
- `S30` **DLG** — Џу Ронг: „Ова.“
- `S31` **NAR** — Сјанглиу падна победена, а нејзината игра заврши.
- `S33` **NAR** — Морам да се предадам, си помисли Гонг Гонг.
- `S34` **NAR** — Но бесот му беше посилен, па полета кон светиот столб.
- `S35` **NAR** — Светата планина Буџоу — столбот што ја држеше Земјата одделена од Небото.
- `S36` **NAR** — И со сета сила удри со главата во неа.
- `S39` **NAR** — Карпата се распука под ударот.
- `S41` **NAR** — Целиот столб се затресе.
- `S42` **NAR** — Карпи и камења се стркалаа надолу како огромен водопад.
- `S43` **NAR** — Гонг Гонг сфати дека претерал.
- `S46` **NAR** — Затоа избега и се скри во длабоките води.
- `S48` **NAR** — Од тој ден, тој секогаш го избегнува Џу Ронг и неговиот огнен меч.

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
| 1 | DD HEADWEAR: no cap/hood/bandana/mask on head; hood = back-cowl only; bare head + teal-blue glowing hair always visible; any head/face covering = REJECT |
| 2 | LEGENDARY WEAPONS MUST APPEAR: DD = twin Frostbite-class hand crossbows; AZ = Dawnbreaker-class greatsword; hero sheet/keyframe without weapon = INCOMPLETE |
| 3 | WEAPON ANTI-SLOP: fantasy construction only; crossbow must NEVER read as firearm; anti-slop negatives always appended |
| 4 | BOSS FACE: Mal'garot HAS a prolific molten-lava face; faceless boss sheets SUPERSEDED |
| 5 | LOCATION BRIGHTNESS FLOOR: environment plates silhouette-readable at thumbnail; no murk-dark grades |

**Anti-slop negatives (always appended):** `firearm, gun, machinegun, Uzi, barrel, magazine, ammo clip, muzzle, modern weapon`

> Activates when face_lock changes from AI-default to an enrolled identity (DD/AZ).

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
