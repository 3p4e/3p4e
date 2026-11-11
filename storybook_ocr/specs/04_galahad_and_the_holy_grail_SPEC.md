# 04 — Галахад и Светиот грал (Galahad and the Holy Grail)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Галахад и Светиот грал** — Младиот витез Галахад го наоѓа Светиот грал и му носи исцеление и мир на својот болен дедо, кралот Пелес.

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
| Галахад / Galahad | Млад благороден витез со сребрен оклоп и бело наметало | story-suggested | AI-default |
| Крал Артур / King Arthur | Мудар крал на Камелот со златна круна и темноцрвен плашт | story-suggested | AI-default |
| Кралот Пелес / King Pelles | Стари благородник прикован за постелата, исцрпен и блед | story-suggested | AI-default |
| Витезите на Тркалезната маса / Round Table Knights | Група витези во разнобојни оклопи и плаштови | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~156.5s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Галахад пристигнува во Камелот, седнува на пророчкото празно место на Тркалезната маса и пред него се појавува Светиот грал.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S04 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S05 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S06 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S07 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S08 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S09 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S10 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S11 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S12 | WIDE | eye-level | crane-down | moderate | 4.0s | NAR |
| S13 | MACRO | macro | push-in | gentle | 3.0s | NAR |
| S14 | MEDIUM | eye-level | shot-reverse | moderate | 4.0s | NAR |

### Act II — Патот

*Галахад го напушта Камелот и по долго талкање пристигнува во замокот Карбонек, каде што неговиот болен дедо, кралот Пелес, лежи прикован за постелата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S16 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S17 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S18 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S19 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S20 | WIDE | eye-level | push-in | moderate | 4.0s | NAR |
| S21 | MEDIUM | low-angle | crane-up | moderate | 3.5s | NAR |
| S22 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S23 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S24 | MEDIUM | over-shoulder | static | moderate | 3.0s | NAR |
| S25 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S26 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S29 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S31 | MACRO | macro | push-in | gentle | 3.0s | NAR |
| S32 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S33 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S36 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S37 | WIDE | eye-level | crane-up | moderate | 4.0s | NAR |

### Act III — Исполнување

*Кралот Пелес оздравува, пророштвото се исполнува и Галахад му носи мир на светот, спасувајќи го Карбонек од страдањето.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S38 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S39 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S40 | WIDE | eye-level | crane-down | moderate | 4.0s | NAR |
| S41 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | NAR |
| S42 | WIDE | low-angle | crane-up | moderate | 4.0s | NAR |
| S43 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | push-in | moderate | 3.5s | NAR |
| S46 | WIDE | high-angle | crane-down | moderate | 4.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во зори, пред капиите на блескавиот Камелот, пристигна самотник на бел коњ.
- `S02` **NAR** — Се велеше дека тој е синот на славниот Ланселот.
- `S03` **NAR** — На престолот го чекаше кралот Артур.
- `S04` **NAR** — Во салата стоеше големата Тркалезна маса, исполнета со витези.
- `S05` **DLG** — Крал Артур: „Седни со нас на Тркалезната маса.“
- `S06` **NAR** — Сите погледи се свртеа кон едно празно, судбоносно место.
- `S07` **NAR** — Пророштвото велеше: тоа место е наменето само за најблагородниот и најчесниот.
- `S08` **NAR** — Галахад зачекори кон тоа место без страв.
- `S09` **NAR** — Застана, а потоа седна.
- `S10` **NAR** — Затаи дишењето — сите знаеја дека недостојните умирале на тоа место.
- `S11` **NAR** — Но Галахад остана здрав и жив, на чудење на сите.
- `S12` **NAR** — Тогаш, пред него, се појави сјаен пехар.
- `S13` **NAR** — Тоа беше Светиот грал — пехарот што даваше бесмртност на оној што ќе се напиеше од него.
- `S14` **NAR** — Кога пехарот исчезна, Галахад се заколна дека ќе тргне да го најде.
- `S15` **NAR** — Со зората, Галахад го напушти Камелот.
- `S16` **NAR** — Денови на пат низ стари шуми и отворени полиња.
- `S17` **NAR** — Минуваше реки и планински предели, секогаш натаму.
- `S18` **NAR** — Ноќите ги минуваше покрај оган, сам со својата клетва.
- `S19` **NAR** — Патот го водеше сè повисоко, низ ветар и магла.
- `S20` **NAR** — Конечно, пред него од маглата излезе замокот Карбонек.
- `S21` **NAR** — Портата беше тешка, а дворот тивок.
- `S22` **NAR** — Внатре владееше полумрак, само трепкаа факели.
- `S23` **NAR** — Галахад чекореше по ходниците, воден од некоја внатрешна сила.
- `S24` **NAR** — На крајот стигна до одајата на кралот.
- `S25` **NAR** — На постелата лежеше стариот крал Пелес, блед и немоќен.
- `S26` **NAR** — Ниту еден лекар долго време не можеше да му најде лек.
- `S27` **NAR** — Неговата кожа беше како восок, а очите затворени.
- `S28` **NAR** — Галахад тивко му пристапи на постелата.
- `S29` **NAR** — Пред него лежеше неговиот дедо, кралот на Карбонек.
- `S30` **NAR** — И само што се доближи, неговите раце почнаа да светат.
- `S31` **NAR** — Во неговите дланки се појави Светиот грал.
- `S32` **NAR** — Галахад го крена пехарот, а светлината се прошири низ одајата.
- `S33` **DLG** — Галахад: „Еве, дедо, испиј го ова.“
- `S34` **NAR** — Го потпре пехарот кон усните на старецот.
- `S35` **NAR** — Кралот Пелес се напи една голтка од чудотворната вода.
- `S36` **NAR** — И во истиот миг, бојата почна да му се враќа на лицето.
- `S37` **NAR** — Светлината го исполни целиот замок.
- `S38` **NAR** — Старецот ги отвори очите, бистри и полни со живот.
- `S39` **NAR** — Кралот Пелес се подигна од постелата, силен како некогаш.
- `S40` **NAR** — Одајата веќе не беше темна — стана дом на светлина.
- `S41` **NAR** — Дедо и внук се прегрнаа.
- `S42` **NAR** — Страдањето го напушти Карбонек.
- `S43` **NAR** — И над целата земја засвета мир.
- `S44` **NAR** — Галахад гледаше кон хоризонтот, смирен.
- `S45` **NAR** — Пророштвото се исполни.
- `S46` **NAR** — Така Галахад му донесе мир на светот и го спаси Карбонек од страдањето.

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
