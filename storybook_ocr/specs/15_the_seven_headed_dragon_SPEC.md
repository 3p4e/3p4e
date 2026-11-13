# 15 — Змејот со седум глави (The Seven-Headed Dragon)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Змејот со седум глави** — Брат и сестра, три волшебни кучиња и една gold девојка против змејот со седум глави.

*Genre:* Легенда · епска бајка

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
| Братот / The Brother | Млад, добродушен селанец во едноставна ткаена облека; кроток, но храбар кога треба | story-suggested | AI-default |
| Сестрата / The Sister | Млада жена, првично грижлива, потоа завистлива и страшлива | story-suggested | AI-default |
| Змејот со седум глави / The Seven-Headed Dragon | Колосален змеј со седум глави, железни крлушки и чад од ноздрите | story-suggested | AI-default |
| Трите кучиња / The Three Dogs | Кинисинџир, Кршизид и Виткајжелезо — три волшебни кучиња со надприродна сила | story-suggested | AI-default |
| Туѓинецот / The Stranger | Мистериозен трговец со наметка, кој ги чува трите волшебни кучиња | story-suggested | AI-default |
| Девојката од јаболкницата / The Maiden from the Apple Tree | Убава маѓепсана господарка на дворецот, ослободена од магијата | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~152.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Наследството и трампата

*Брат и сестра наследуваат три овци. Братот ги разменува за три волшебни кучиња, а лутата сестра го избрка. Тој заминува и го наоѓа напуштениот дворец.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S04 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S05 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | NAR |
| S06 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S07 | INSERT | MACRO | static | gentle | 3.0s | NAR |
| S08 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | NAR |
| S09 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S10 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S11 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S12 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |
| S13 | WIDE | eye-level | pull-back | moderate | 3.0s | NAR |
| S14 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

### Act II — Дворецот и предавството

*Брат живее како принц и ја кани сестрата. Змејот со седум глави ја заканува, таа го предавствува братот, но трите кучиња го спасуваат и го бркаат змејот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S17 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S18 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S19 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S20 | INSERT | MACRO | static | gentle | 3.0s | NAR |
| S21 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S22 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S23 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S24 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S25 | CLOSE | low-angle | static | gentle | 3.0s | NAR |
| S26 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S27 | CLOSE | over-shoulder | static | gentle | 3.5s | DLG |
| S28 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S29 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S30 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S31 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S32 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S33 | CLOSE | low-angle | static | action | 3.0s | NAR |
| S34 | WIDE | eye-level | pan-right | moderate | 3.5s | DLG |
| S35 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S36 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S37 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |

### Act III — Ослободувањето

*Јаболкницата се отвора и излегува маѓепсаната господарка. Дворецот оживува, а братот, девојката и кучињата живеат среќно засекогаш.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S40 | CLOSE | low-angle | static | gentle | 3.0s | NAR |
| S41 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S42 | CLOSE | over-shoulder | static | gentle | 3.0s | NAR |
| S43 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S44 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S45 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S46 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S47 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S48 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во едно мирно италијанско село живееја брат и сестра, со само три овци во наследство.
- `S02` **NAR** — Братот и сестрата живееја во слога и се грижеа за овците.
- `S03` **NAR** — Татко им оставил три овци, сето што го имаа.
- `S04` **NAR** — Еден ден братот тргна кон пазарот да ги продаде овците.
- `S05` **NAR** — По пат го сретна непознат човек, а покрај него три силни кучиња.
- `S06` **NAR** — Човекот рече: „Ова се чудесни животни.“
- `S07` **NAR** — Кинисинџир, Кршизид и Виткајжелезо — така се викаа трите кучиња.
- `S08` **NAR** — Човекот му понуди да ги размени неговите овци за трите кучиња.
- `S09` **NAR** — Момчето долго се двоумеше, но на крајот ја прифати понудата.
- `S10` **NAR** — Со трите кучиња, тој се врати дома.
- `S11` **NAR** — Но сестрата се разлути кога го виде.
- `S12` **DLG** — Сестрата: „Го даде нашето единствено богатство! За три бескорисни кучиња!“
- `S13` **NAR** — И така, таа го избрка од куќата.
- `S14` **NAR** — Поодеше долго, додека во далечината не здогледа раскошен дворец.
- `S15` **NAR** — Дворецот беше празен и напуштен, но блескаше како да е жив.
- `S16` **NAR** — Братот реши да живее тука, и заживеа како принц.
- `S17` **NAR** — Одите беа мраморни, а од светлината танцуваше прашина.
- `S18` **NAR** — Срцето му трепереше од радост.
- `S19` **NAR** — Со денови јадеше од златни чинии и спиеше во меки одаи.
- `S20` **NAR** — Ништо не му недостасуваше.
- `S21` **NAR** — Во градината стоеше чудна јаболкница, со едно златно јаболко.
- `S22` **NAR** — Бидејќи беше среќен, братот ја покани сестрата да живее со него.
- `S23` **NAR** — И повторно заживеаја убаво, сè до еден ден.
- `S24` **NAR** — Тогаш од небото се спушти Змејот со седум глави.
- `S25` **NAR** — Седумте глави сискаа, а од ноздрите му се виореше чад.
- `S26` **NAR** — Девојката преплашена се повлече пред змејот.
- `S27` **DLG** — Сестрата: „Смилувај се! Изеди го брат ми, а мене поштеди ме!“
- `S28` **DLG** — Змејот: „Добро! Но прво ќе направиш како што ти велам.“
- `S29` **DLG** — Сестрата: „Твоиве кучиња смрдат! Изнеси ги надвор!“
- `S30` **NAR** — Братот, секогаш добар, ги врза кучињата надвор.
- `S31` **DLG** — Сестрата (од прозорецот): „Ако си веќе во градината, донеси ми едно јаболко!“
- `S32` **NAR** — Тој ја послуша и скина едно јаболко.
- `S33` **NAR** — Тогаш повторно се појави змејот и се нафрли на момчето.
- `S34` **DLG** — Братот: „Кинисинџир, Кршизид и Виткајжелезо, помогнете ми!“
- `S35` **NAR** — За миг, кучињата ги скинаа синџирите и ги скршија ѕидовите.
- `S36` **NAR** — Змејот, уплашен, побегна со молскавична брзина.
- `S37` **NAR** — Братот ги прегрна своите верни кучиња.
- `S38` **NAR** — Во градината повторно завладеа мир.
- `S39` **NAR** — Тогаш јаболкницата се отвори, и од неа блисна силна светлина.
- `S40` **NAR** — Од светлината излезе една убава девојка.
- `S41` **DLG** — Девојката: „Јас сум господарка на овој дворец. Ти конечно ме ослободи од магијата!“
- `S42` **NAR** — Братот не можеше да поверува на своите очи.
- `S43` **NAR** — Дворецот оживеа — бојата се врати, а магијата се сруши.
- `S44` **NAR** — „Сега ќе живееш со мене“, му рече девојката.
- `S45` **NAR** — Дворецот запеа од радост, осветлен како никогаш порано.
- `S46` **NAR** — Рацете им се споија, а погледите им се сретнаа.
- `S47` **NAR** — И живееја во среќа и слога, засекогаш.
- `S48` **NAR** — Така, добрината и верните пријатели секогаш победуваат.

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
