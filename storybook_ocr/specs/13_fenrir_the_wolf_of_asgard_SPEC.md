# 13 — Фенрир, волкот од Асгард (Fenrir, the Wolf of Asgard)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Фенрир, волкот од Асгард** — Кога дивиот волк Фенрир расте како закана за Асгард, боговите го врзуваат со магичен синџир — а храбриот Тир ја жртвува својата рака за да го заштити светот.

*Genre:* Нордиски мит · епска акција

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
| Один / Odin | Сеотецот, кралот на Асгард; мудар, строг и далекувид | story-suggested | AI-default |
| Локи / Loki | Богот-измамник, татко на Фенрир; лукав, но колеблив пред сопственото дете | story-suggested | AI-default |
| Фенрир / Fenrir | Огромниот див волк, син на Локи; расте од волче во закана за боговите | story-suggested | AI-default |
| Тир / Týr | Богот на војната; храбар, благороден и подготвен на врвна жртва | story-suggested | AI-default |
| Јормунгандир / Jörmungandr | Светската змија, син на Локи; истеран во длабокото море | story-suggested | AI-default |
| Хел / Hel | Божицата на подземниот свет, ќерка на Локи; бледа и мирна | story-suggested | AI-default |
| Џуџињата ковачи / The Dwarf Smiths | Најдобрите ковачи на железо во темните пештери на Нидавелир | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~149.5s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Растењето

*Во златниот Асгард, Локи ги има трите деца — Фенрир, Јормунгандир и Хел. Один ги гони Јормунгандир и Хел како чудовишта, но го задржува Фенрир. Ден по ден волкот расте огромен, сè додека не стане закана за боговите.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S04 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S05 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S06 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S07 | WIDE | low-angle | pan-right | moderate | 3.0s | NAR |
| S08 | MEDIUM | high-angle | crane-down | moderate | 3.0s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S10 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S11 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S12 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S13 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S14 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |

### Act II — Синџирот

*Один наредува Фенрир да се врзе, но Локи одбива. Тир се понудува. Железниот синџир што Тир го наоѓа не издржува — волкот го крши лесно. Тир бара помош од џуџињата во Нидавелир, кои коваат нежен, магичен синџир. Но Фенрир не е глупав: бара раката на Тир во својата уста како залог.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S16 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S17 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S18 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S19 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S20 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S21 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S22 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S23 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S24 | MEDIUM | eye-level | static | action | 3.0s | NAR |
| S25 | INSERT | macro | push-in | gentle | 3.5s | NAR |
| S26 | MACRO | macro | static | gentle | 3.0s | NAR |
| S27 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S28 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S29 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S30 | CLOSE | eye-level | static | gentle | 4.0s | DLG |
| S31 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S32 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S33 | MACRO | macro | push-in | gentle | 3.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S36 | WIDE | low-angle | static | action | 3.5s | NAR |

### Act III — Жртвата

*Фенрир се бори, но магичниот синџир не се крши. Бесен, волкот ја затвора устата и ја одзема десната рака на Тир. Морничав крик одекнува низ Асгард, а Тир за навек останува храбар бог без десница.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | WIDE | eye-level | track | action | 3.5s | NAR |
| S38 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S39 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S40 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S41 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S42 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S43 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S45 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S46 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Златниот Асгард блеска високо над облаците — домот на боговите.
- `S02` **NAR** — Во неговото срце седи Один, Сеотецот, мудар и строг.
- `S03` **NAR** — Но во сенката стои Локи — а зад него чекорат три негови деца.
- `S04` **NAR** — Фенрир, волкчето; Јормунгандир, змијата; и Хел, бледата девојка.
- `S05` **NAR** — Один ги гледа змијата и девојката — и во нив гледа чудовишта.
- `S06` **NAR** — Тогаш од неговите гради грми наредба.
- `S06` **DLG** — Один: „Изгонете ги Јормунгандир и Хел од Асгард!“
- `S07` **NAR** — Јормунгандир, светската змија, е фрлен во длабокото море.
- `S08` **NAR** — А Хел — мирна и бледа — е испратена во подземниот свет.
- `S09` **NAR** — Само Фенрир останува — растејќи како дете меѓу боговите.
- `S10` **NAR** — Ден по ден, волкот растеше сè поголем и поголем.
- `S11` **NAR** — Наскоро Фенрир стана џиновски ѕвер — закана за целиот Асгард.
- `S12` **NAR** — И Один повеќе не можеше да гледа како волкот расте без крај.
- `S13` **NAR** — И тогаш, на глас, Сеотецот изговори страшна наредба.
- `S13` **DLG** — Один: „Врзете го!“
- `S14` **NAR** — Но кога Один го погледна Локи, таткото на волкот го одврати лицето.
- `S14` **DLG** — Один: „Локи, можеш ти да го направиш тоа?“
- `S15` **NAR** — Тогаш напред чекори Тир, богот на војната — храбар и решителен.
- `S15` **DLG** — Тир: „Јас ќе го врзам Фенрир.“
- `S16` **NAR** — Тир замина да бара синџир — тежок, дебел, направен од чисто железо.
- `S17` **NAR** — Тир го донесе тешкиот железен синџир пред волкот.
- `S18` **NAR** — Боговите пристапија внимателно, со синџирот во рацете.
- `S19` **NAR** — Тие го обвиткаа волкот со железо и го стегнаа со сета сила.
- `S20` **NAR** — Но Фенрир само ги напрегна мускулите — и железото пукна како конец.
- `S21` **NAR** — Волкот стана слободен — а боговите отстапија во страв.
- `S22` **NAR** — Тир знаеше дека железото не е одговор — му требаше магија на џуџињата.
- `S23` **NAR** — Длабоко во темните пештери на Нидавелир — домот на најдобрите ковачи.
- `S24` **NAR** — Таму, зад вжарените огништа, работат џуџињата-ковачи.
- `S25` **NAR** — Од најнежни нешта — шепот на ветрот, корења и магла — тие го плетеа новиот синџир.
- `S26` **NAR** — Синџирот што го направија беше толку тенок и нежен — а сепак непокршлива стапица.
- `S27` **NAR** — Тир му го донесе тенкиот синџир на Фенрир — а волкот веднаш насети нешто.
- `S28` **NAR** — Фенрир не беше глупав — а неговите очи сè гледаа.
- `S29` **NAR** — Тогаш Тир проговори со ладен, мирен глас.
- `S29` **DLG** — Тир: „Да видиме дали ќе можеш да го скинеш и овој синџир.“
- `S30` **NAR** — А волкот одговори со жестока, лукава пресметка.
- `S30` **DLG** — Фенрир: „Може да ме врзеш — но ќе ја ставиш раката во мојата уста. Ако не се ослободам, и ти ќе изгубиш нешто!“
- `S31` **NAR** — Боговите замолкнаа — цената беше престрашна за да се прифати.
- `S32` **NAR** — Но Тир, без трепет, ја подаде десната рака — залогот на неговата смелост.
- `S33` **NAR** — Топла и влажна, устата на волкот се затвори околу раката на Тир.
- `S34` **NAR** — Со слободната рака, Тир го обвитка волкот со тенкиот магичен синџир.
- `S35` **NAR** — Штом синџирот се затегна, руните се разгореа — и магијата се разбуди.
- `S36` **NAR** — Фенрир се напрегна — но овој пат синџирот на џуџињата не попушташе.
- `S37` **NAR** — Волкот се преташе и грчеше, со синџирот на џуџињата цврсто до коски.
- `S38` **NAR** — Колку повеќе се бореше, толку посилно синџирот го држеше.
- `S39` **NAR** — Тогаш во очите на волкот се разгоре бес — и тој ги затвори вилиците.
- `S40` **NAR** — И раката, залогот на смелоста — веќе ја немаше.
- `S41` **NAR** — Морничав крик одекна низ целиот Асгард — до небесата.
- `S42` **NAR** — Боговите го гледаа ужаснати — цената беше платена.
- `S43` **NAR** — А Тир, без десната рака, застана исправен — непобегнат.
- `S44` **NAR** — Од тој ден, Тир мораше да живее без својата десна рака.
- `S45` **NAR** — А Фенрир, врзан со најнежниот синџир, мирно легна во сенката на карпата.
- `S46` **NAR** — Така заврши легендата за волкот — и за храброста што го скроти светот.

---

## 5. Acceptance criteria (testable)

1. Shot count = 46 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
