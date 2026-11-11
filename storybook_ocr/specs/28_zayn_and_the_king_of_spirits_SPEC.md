# 28 — Зејн и кралот на духовите (Zayn and the King of Spirits)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Зејн и кралот на духовите** — Разгален принц открива скриена одаја со девет златни столба и тргнува во Египет за најскапоцената статуа, само да дознае дека вистинското богатство е љубовта.

*Genre:* Легенда · источне приказни

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
| Зејн / Zayn | Млад разгален принц од Басра, раскошна источна облека и турбан | story-suggested | AI-default |
| Старецот од сонот / The Old Man of the Dream | Белобрадест мудрец со блескава сребрена руба и светлосна аура | story-suggested | AI-default |
| Кралот на духовите / The King of Spirits | Величествен дух-крал во светкава руба со мистична златна аура | story-suggested | AI-default |
| Водичот / The Guide | Виток патешественик во темна наметка, знае тајни патеки | story-suggested | AI-default |
| Принцезата на Персија / The Princess of Persia | Најубавата девојка на светот, источна принцеза со свилена облека и накит | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~172.5s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Разгалениот принц Зејн живее само за забави, игнорира мудриот совет од сонот и ја открива скриената одаја со девет златни столба — и натписот што го води кон Египет.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S03 | INSERT | macro | static | gentle | 3.0s | NAR |
| S04 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S05 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S06 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S07 | INSERT | macro | push-in | gentle | 3.5s | NAR |
| S08 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S09 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S10 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S11 | INSERT | macro | push-in | gentle | 3.5s | NAR |
| S12 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S13 | WIDE | eye-level | crane-down | moderate | 4.0s | NAR |
| S14 | WIDE | high-angle | pan-left | moderate | 4.5s | NAR |

### Act II — Патот

*Со водич, Зејн стигнува во Градот на духовите, се среќава со кралот кој е стариот од сонот и го прифаќа предизвикот: на летечки килим да ја донесе принцезата на Персија.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S16 | INSERT | macro | static | gentle | 3.5s | NAR |
| S17 | CLOSE | low-angle | push-in | gentle | 3.5s | NAR |
| S18 | WIDE | eye-level | pan-right | moderate | 4.0s | NAR |
| S19 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S20 | WIDE | high-angle | crane-down | moderate | 4.5s | NAR |
| S21 | MEDIUM | low-angle | push-in | moderate | 4.0s | NAR |
| S22 | CLOSE | eye-level | static | gentle | 3.5s | DLG |
| S23 | WIDE | eye-level | pan-left | moderate | 4.5s | NAR |
| S24 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S25 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S26 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S27 | MEDIUM | over-shoulder | static | moderate | 4.0s | NAR |
| S28 | MEDIUM | eye-level | track | moderate | 4.0s | NAR |
| S29 | INSERT | macro | push-in | gentle | 3.5s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 3.5s | NAR |
| S31 | WIDE | high-angle | crane-up | moderate | 4.5s | NAR |
| S32 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S33 | WIDE | eye-level | crane-down | moderate | 4.0s | NAR |
| S34 | MEDIUM | over-shoulder | track | moderate | 3.5s | NAR |
| S35 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S36 | MEDIUM | eye-level | track | moderate | 4.0s | NAR |
| S37 | CLOSE | over-shoulder | static | gentle | 4.0s | NAR |

### Act III — Исполнување

*Скршен, Зејн ја предава принцезата, но кралот му открива дека статуата е веќе на место — а дома го чека љубовта, награда поскапоцена од злато.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S38 | WIDE | high-angle | crane-down | moderate | 4.5s | NAR |
| S39 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S40 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S41 | WIDE | eye-level | pan-right | moderate | 4.0s | NAR |
| S42 | MEDIUM | low-angle | track | moderate | 3.5s | NAR |
| S43 | CLOSE | eye-level | push-in | gentle | 4.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S45 | WIDE | low-angle | crane-up | moderate | 4.0s | DLG |
| S46 | WIDE | eye-level | crane-down | moderate | 4.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во стариот пристанишен град Басра, каде златните минариња се огледуваат во реката, живееше принцот Зејн.
- `S02` **NAR** — Но Зејн не мислеше на проблемите на своето кралство.
- `S03` **NAR** — Неговиот свет беше полн само со гозби и забави.
- `S04` **NAR** — Ден и ноќ, во палатата одекнуваа музика и смеа.
- `S05` **NAR** — Никој не смееше да му спомене дека неговата грижа исчезнала.
- `S06` **NAR** — Една вечер, кога сонцето се скри, Зејн заспа на својата свилена постела.
- `S07` **NAR** — Во неговиот сон се подигна сребрена магла.
- `S08` **NAR** — Еден старец му шепна совет — да владее помудро.
- `S09` **NAR** — Но Зејн го одби советот и се сврте на другата страна.
- `S10` **NAR** — Но старецот се врати — и му покажа влез во одаја полна со златници.
- `S11` **NAR** — Златото светкаше како жив пламен.
- `S12` **NAR** — Штом се разбуди, Зејн им нареди на стражарите да копаат на скриеното место.
- `S13` **NAR** — Копачите дојдоа до тешка камена врата под земјата.
- `S14` **NAR** — Таму, полна со сјај, стоеше одајата на деветте златни столба.
- `S15` **NAR** — На осум столба стоеја мермерни статуи, но деветтиот беше празен.
- `S16` **NAR** — На него светеше само еден натпис.
- `S17` **NAR** — Деветтата статуа, најскапоцената, чекала во далечниот Египет.
- `S18` **NAR** — Зејн подготви карван и тргна во непознатото.
- `S19` **NAR** — На патот, еден водич му понуди да го одведе во Градот на духовите.
- `S20` **NAR** — Пред нив блесна Градот на духовите — прекрасен како сон.
- `S21` **NAR** — Градините беа бујни, а зданијата се креваа до небото.
- `S22` **DLG** — Водичот: „Ако не сме бегаме пред Кралската палата, кралот на духовите може да ни се покаже како чудовиште.“
- `S23` **NAR** — Тогаш пред нив се отвори Кралската палата.
- `S24` **NAR** — Од светлината се појави самиот Крал на духовите.
- `S25` **DLG** — Кралот на духовите: „Добре дојде, Зејн. Јас сум стариот од твоите соништа.“
- `S26` **NAR** — Зејн препозна во него добриот старец од сонот.
- `S27` **NAR** — Кралот му понуди зделка: ќе му ја даде статуата за најубавата девојка на светот.
- `S28` **NAR** — За да му помогне, кралот му подари летечки килим и волшебно огледало.
- `S29` **NAR** — Огледалото светна и покажа туѓо лице.
- `S30` **NAR** — Во него се огледуваше принцезата на Персија.
- `S31` **NAR** — Летајќи на волшебниот килим, Зејн прелета пустини и планини.
- `S32` **NAR** — Ветрот му ги развеваше наметката и решеноста.
- `S33` **NAR** — Килимот се спушти во градините на персиската палата.
- `S34` **NAR** — Меѓу цветата, Зејн ја здогледа неа.
- `S35` **NAR** — Таа беше поубава од сè што некогаш видел.
- `S36` **NAR** — Зејн ја зеде на килимот за да ја однесе во Египет.
- `S37` **NAR** — Но на небесниот пат, неговото срце се промени.
- `S38` **NAR** — Зејн ја одведе принцезата пред кралот на духовите.
- `S39` **NAR** — Неговото срце беше скршено — отишла од неговата рака.
- `S40` **DLG** — Кралот на духовите: „Оди си. Деветтата статуа е веќе со другите осум.“
- `S41` **NAR** — Зејн се врати во Басра, а патот му се чинеше подолг одошто било.
- `S42` **NAR** — Веднаш слезе во подземната одаја кај деветте столба.
- `S43` **NAR** — На местото на деветтата статуа стоеше некој многу попознат.
- `S44` **NAR** — Таму го чекаше неговата сакана принцеза.
- `S45` **DLG** — Духот: „Таа навистина е најскапоцената статуа!“
- `S46` **NAR** — Зејн се ожени со девојката и оттогаш владееше мудро, сакан од сите.

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
