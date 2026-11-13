# 38 — Пегаз (Pegasus)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Пегаз** — Младиот принц Белерофон, со помош на божицата Атена, го зауздува крилестиот коњ Пегаз и се вјдигнува во небото, да се соочи со страшната Химера.

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
| Пегаз / Pegasus | Прекрасен снежно-бел крилест коњ, носителот на Зевсовите молњи | story-suggested | AI-default |
| Белерофон / Bellerophon | Млад и храбар принц со срце на вистински јунак | story-suggested | AI-default |
| Зевс / Zeus | Кралот на сите богови, моќен и величествен владетел на Олимп | story-suggested | AI-default |
| Атена / Athena | Божицата на мудроста, сјајна и смирена заштитничка на јунаците | story-suggested | AI-default |
| Химера / Chimera | Чудовиште со лавовска глава, козјо тело и змијска опашка, блуе оган | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~153.0s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*На Олимп крилестиот коњ Пегаз ги носи зевсовите молњи; долу во светот, младиот принц Белерофон ќе го победи чудовиштето Химера, а за тоа ќе го побара помошта на божицата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S03 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S04 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S05 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S06 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S07 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S08 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S09 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S10 | MEDIUM | low-angle | static | action | 3.5s | NAR |
| S11 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S12 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S13 | CLOSE-UP | over-shoulder | push-in | gentle | 3.0s | — |
| S14 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

### Act II — Пресврт

*Во сонот божицата Атена му дава златни узди и го упатува кон изворот Пирен; тамо Белерофон нечујно го зауздува крилестиот коњ.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | NAR |
| S17 | CLOSE-UP | eye-level | static | gentle | 3.0s | — |
| S18 | INSERT | macro | push-in | gentle | 3.0s | — |
| S19 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S20 | MEDIUM | over-shoulder | static | moderate | 4.0s | DLG |
| S21 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S22 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S23 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S24 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S25 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S26 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S27 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S28 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S29 | CLOSE-UP | high-angle | push-in | gentle | 3.0s | — |
| S30 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S31 | CLOSE-UP | macro | push-in | gentle | 3.0s | — |
| S32 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |

### Act III — Лет

*Белерофон го јавнува Пегаз, и двајцата се вйдигнуваат во небото, летајќи кон својата опасна авантура и содбата со Химера.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S33 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S34 | CLOSE-UP | over-shoulder | push-in | gentle | 3.0s | — |
| S35 | WIDE | low-angle | crane-up | moderate | 4.0s | NAR |
| S36 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S37 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S39 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S40 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S41 | INSERT | macro | push-in | gentle | 3.0s | — |
| S42 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S43 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S44 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | — |
| S45 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S46 | WIDE | eye-level | pull-back | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Високо над облаците, на врвот на светот, живееше еден коњ со крилја.
- `S02` **NAR** — Секој ден тој леташе по небото и ги носеше молњите на кралот на боговите.
- `S03` **NAR** — Никој смртник не можеше да го јава овој посебен коњ.
- `S04` **NAR** — Зевс, кралот на сите богови, сам ги примаше молњите.
- `S05` **NAR** — Секоја молња бликаше со своствено небесно сијање.
- `S06` **NAR** — Но далеку под планината, живееше еден млад принц.
- `S07` **NAR** — Белерофон беше наречен за најтешката задача: да го победи легендарното чудовиште.
- `S08` **NAR** — Но во него се роди една смела замисла.
- `S09` **NAR** — Далеку, во една задимена карпа, живееше страшно чудовиште.
- `S10` **NAR** — Химера имаше тело на коза, глава на лав и змијска опашка, а захарот ја беше огнен.
- `S11` **NAR** — Ниту еден смртник досега не беше го јавал крилестиот коњ.
- `S12` **DLG** — Белерофон: „Тој крилест коњ ќе стане моето тајно оружје во борбата со Химера.“
- `S14` **NAR** — Набеден на мисла за својата тајна, тој замоли божицата за помош.
- `S15` **NAR** — Во сонот му се јави самата божица на мудроста.
- `S16` **NAR** — Атена го погледна со благ насмев и му прошепоти тајна.
- `S19` **NAR** — В нејзините раце засвети чисто злато.
- `S20` **DLG** — Атена: „Земи ги овие златни узди. Оди кај изворот Пирен. Кога Пегаз ќе слета да пие вода, стави му ги околу вратот и појди го.“
- `S21` **NAR** — Кога се разбуди, покрај себе ги најде златните узди, дар од божицата.
- `S22` **NAR** — Златото засвети во неговите раце.
- `S23` **NAR** — Ојде таму каде што му рече божицата, кон изворот Пирен.
- `S24` **NAR** — Тамо отечеше чиста, ледена вода кроз зелената долина.
- `S25` **NAR** — Белерофон се притаи зад карпите и чекаше.
- `S26` **NAR** — Над водата се симна сенка, и крилестиот коњ се спушти кон изворот.
- `S27` **NAR** — Тамо го виде спокојно како си пие вода.
- `S28` **NAR** — Белерофон нечујно му се прикраде одзади.
- `S30` **NAR** — Со едно внимателно движење ги стави уздите околу вратот.
- `S32` **NAR** — Животното не се вознемири и не го отфрли.
- `S33` **NAR** — Потоа го јавна крилестиот коњ.
- `S35` **NAR** — Првиот замав на крилјата ги крена кон небото.
- `S36` **NAR** — Тие само одлетаа во утринското небо.
- `S37` **NAR** — Високо над облаците, светот стана мал.
- `S38` **NAR** — Ветрот му развеа наментката додека летаа.
- `S39` **NAR** — Наеднаш погледот му се смири кон хоризонтот.
- `S40` **NAR** — Далеку, на работ на видокот, се креваше нивната авантура.
- `S42` **NAR** — Однедечка го стрете вулканската планина од каде што се креваше чудовиштето.
- `S43` **NAR** — Белерофон не поколеба; срцето му беше полно со храброст.
- `S45` **NAR** — Пред нив беше опасна авантура.
- `S46` **NAR** — Им претстоеше голема авантура.

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
