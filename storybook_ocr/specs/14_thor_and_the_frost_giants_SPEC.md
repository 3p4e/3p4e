# 14 — Тор и ледените џинови (Thor and the Frost Giants)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Тор и ледените џинови** — Кога измамата на Локи го води брат му Тор без оружје во царството на ледените џинови, богот на громовите мора да го докаже своето херојство само со даровите на Грид.

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
| Тор / Thor | Богот на громовите — силен, чесен и бестрашен | story-suggested | AI-default |
| Локи / Loki | Богот на измамата — лукав и завидлив, брат на Тор | story-suggested | AI-default |
| Героид / Geirröd | Злобниот леден џин — груб и омразен насилник | story-suggested | AI-default |
| Грид / Gríðr | Добрата исполинка — пријателка на Один, му помага на Тор | story-suggested | AI-default |
| Гјалп / Gjálp | Ќерка на Героид — демне во реката да ги удави | story-suggested | AI-default |
| Греип / Greip | Ќерка на Героид — лукава домаќинка која подготвува стапица | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~147.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Измамата на Локи

*Локи, претворен во птица, е заробен од џинот Героид и се спасува ветувајќи да го доведе Тор без оружје. Враќајќи се во Асгард, со ласкање го наговара Тор да го остави чеканот и да тргне со него.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S04 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | NAR |
| S05 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S06 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S07 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S08 | MEDIUM | low-angle | static | moderate | 3.0s | DLG |
| S09 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S10 | WIDE | high-angle | crane-up | moderate | 3.0s | NAR |
| S11 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S12 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S13 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | DLG |
| S14 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S15 | WIDE | eye-level | track | moderate | 3.5s | NAR |

### Act II — Патот низ мразот

*Низ снежна бура браќата стигнуваат кај добрата исполинка Грид, која им дава железна ракавица, железна палка и појас. На патот ја совладуваат речната заседа на Гјалп, а во палатата ги чекаат стапиците на Греип и бесен Героид.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S16 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S17 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S18 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S19 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S20 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | DLG |
| S21 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S22 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S23 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S24 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S25 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S26 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S27 | WIDE | low-angle | pan-right | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S29 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S30 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S31 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S32 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S33 | CLOSE | low-angle | push-in | action | 3.0s | NAR |
| S34 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S35 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S36 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S37 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S38 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S39 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |

### Act III — Враќањето

*Победувајќи го Героид со неговата сопствена гламна, Тор се враќа дома горд, но Локи останува со срце полно завист што брат му успеа и без чеканот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S40 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S41 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S42 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S43 | CLOSE | eye-level | shot-reverse | gentle | 3.0s | DLG |
| S44 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S45 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S46 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S47 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S48 | WIDE | eye-level | track | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во кралството на мразот, ѕидовите од мраз светкаат како скапоцени камења. Една сенка прелетува над нив.
- `S02` **NAR** — Тоа не е обична птица. Тоа е Локи, богот на измамата, кој дошол да шпионира.
- `S03` **NAR** — Од палатата на мразот, Локи ја набљудува величествената тврдина на џиновите.
- `S04` **NAR** — Но во сенките демне стапица. Огромна рака се испружува од зад ледениот столб.
- `S05` **NAR** — Злобниот Героид го фати Локи и го затвори во кафез.
- `S06` **NAR** — Локи брзо смислува измама.
- `S07` **DLG** — Локи: „Знам дека ти и брат ми не сте пријатели.“
- `S08` **DLG** — Локи: „Ако ме пуштиш, ќе го доведам Тор овде — без оружје.“
- `S09` **NAR** — Џинот ја прифаќа понудата.
- `S10` **NAR** — Конечно слободен, Локи одлетува назад во Асгард.
- `S11` **NAR** — Во златниот Асгард, Тор дочекува го својот брат.
- `S12` **DLG** — Локи: „Брате, колку убави нешта видов во кралството на џиновите!“
- `S13` **DLG** — Локи: „Ќе биде подобро да одиме без оружје — ќе им бидеме гости.“
- `S14` **NAR** — Тор го остава својот чекан — од кој никогаш не се делеше.
- `S15` **NAR** — Без оружје и оклоп, двајцата браќа тргнуваат по застрашувачкиот пат кон земјата на џиновите.
- `S16` **NAR** — Патот ги води низ сè пострмни предели, а небото се полни со тежок снег.
- `S17` **NAR** — Снежната бура ги зафаќа со полна сила.
- `S18` **NAR** — Тие бараат засолниште во пештерата на исполинката Грид.
- `S19` **DLG** — Грид: „Пријателка сум со Один, татко ви. Ќе ви помогнам.“
- `S20` **DLG** — Грид: „Героид е насилник и не ми се допаѓа. Еве ви железна ракавица — ќе ви затреба.“
- `S21` **DLG** — Грид: „Земи ја и оваа железна палка и појасот.“
- `S22` **NAR** — Со даровите од Грид, браќата продолжуваат кон палатата на Героид.
- `S23` **NAR** — На патот ги пресретнува брза, разбеснета река.
- `S24` **NAR** — Во реката демне Гјалп, ќерката на џинот.
- `S25` **NAR** — Гјалп ја надига реката за да ги удави.
- `S26` **NAR** — Тор ја забива железната палка длабоко во коритото на реката.
- `S27` **NAR** — Со силата на палката, тој се исправа против струјата и се извлекува на брегот.
- `S28` **NAR** — Наскоро, тие стигнуваат до ледените порти на палатата на Героид.
- `S29` **NAR** — Нив ги дочекува Греип, другата ќерка на Героид.
- `S30` **NAR** — Греип ги води низ гостинската одаја и му нуди на Тор стол да седне.
- `S31` **DLG** — Греип: „Седни, Тор. Одмори се по долгиот пат.“
- `S32` **NAR** — Одеднаш, таванот почнува да се спушта — Греип го крева столот на рамениците.
- `S33` **NAR** — Тор ја грабнува железната палка и удира.
- `S34` **NAR** — Исполинката се сопнува и се срушува на подот, поразена.
- `S35` **NAR** — Во тој миг се појавува Героид, со разгорена гламна во раката.
- `S36` **NAR** — Тор ја крева железната ракавица и ја фаќа усвитената гламна.
- `S37` **NAR** — Со сета сила, Тор ја фрла назад кон Героид.
- `S38` **NAR** — Гламната го погодува ледениот џин.
- `S39` **NAR** — Ледената снага на Героид се крши и тој паѓа, поразен.
- `S40` **NAR** — Со победата над Героид, браќата излегуваат од палатата на мразот.
- `S41` **NAR** — Тор чекори гордо, а Локи молчи — но не од радост.
- `S42` **DLG** — Локи: „Ти успеа... дури и без чеканот.“
- `S43` **DLG** — Тор: „Силата не е само во чеканот, брате.“
- `S44` **NAR** — Напред ги чека златниот сјај на Асгард.
- `S45` **NAR** — Во Асгард, чеканот сè уште лежи каде што Тор го остави.
- `S46` **NAR** — Тор ја крева својата моќ повторно, а чеканот се пали со гром.
- `S47` **NAR** — А Локи стои во сенката, со срце полно завист.
- `S48` **NAR** — Така завршува приказната за Тор и ледените џинови — каде силата е во срцето, не во оружјето.

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
