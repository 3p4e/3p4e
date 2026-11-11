# 37 — Поразот на Химера (The Defeat of the Chimera)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Поразот на Химера** — Младиот јунак Белерофон, јавајќи го крилестиот Пегаз, се соочува со огнената Химера на карпеста планина — и со итрина на место со меч, го победува чудовиштето што никој не го преживеал.

*Genre:* Стагрчки мит · епска акција

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
| Белерофон / Bellerophon | Храбар и снаодлив млад јунак; отфрлен гостин кој станува победник. | story-suggested | AI-default |
| Пегаз / Pegasus | Снежно-бел крилест коњ, верен неразделен пријател на Белерофон. | story-suggested | AI-default |
| Химера / Chimera | Огнено чудовиште со лавовска глава, козјо тело и змиска опашка; блуе оган. | story-suggested | AI-default |
| Кралот Прет / King Proetus | Владетел на Тиринт, растргнат меѓу светиот закон на гостите и молбата на сопругата. | story-suggested | AI-default |
| Кралицата Стенебеја / Queen Stheneboea | Навредена и лута кралица што сака одмазда. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~157.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба во палатата

*Во палатата во Тиринт, навредената кралица Стенебеја бара Белерофон да плати со живот. Кралот Прет одбива да го повреди гостинот, но смислува невозможна задача — борба со Химера, од која никој не преживеал.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S03 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S04 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S05 | CLOSE-UP | over-shoulder | static | gentle | 3.0s | DLG |
| S06 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S07 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S08 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S09 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S10 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S11 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S12 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S13 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S14 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |

### Act II — Планината и битката

*Белерофон и Пегаз летаат кон карпестата планина каде се крие Химера. Чудовиштето излегува блуејќи оган; Белерофон сфаќа дека само еден е начинот да ги изгасне пламените — со итрина: стопува оловни грутки и, побрз од огнот, го истура во устата на Химера, каде зацврснува и го победува чудовиштето.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S17 | WIDE | high-angle | pan-right | moderate | 3.5s | NAR |
| S18 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S19 | WIDE | low-angle | crane-up | action | 3.5s | NAR |
| S20 | CLOSE-UP | macro | push-in | gentle | 3.0s | NAR |
| S21 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S22 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S23 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S24 | WIDE | low-angle | static | action | 3.0s | NAR |
| S25 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S26 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S27 | MEDIUM | eye-level | static | action | 3.5s | NAR |
| S28 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S29 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S30 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S31 | WIDE | low-angle | static | action | 3.0s | NAR |
| S32 | CLOSE-UP | macro | push-in | gentle | 3.0s | NAR |
| S33 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S34 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S35 | WIDE | low-angle | static | action | 3.5s | NAR |
| S36 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S37 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | pull-back | moderate | 3.5s | NAR |

### Act III — Простувањето и новиот пат

*Белерофон се враќа во Тиринт како победник. Кралот Прет го пречекува со почит и простува. Белерофон и Пегаз остануваат заедно, подготвени за многу нови авантури.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | high-angle | pan-right | moderate | 3.5s | NAR |
| S40 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S41 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S42 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S43 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S44 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S45 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S46 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S47 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S48 | WIDE | low-angle | pull-back | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во градот Тиринт, зад ѕидови од огромен камен, живееше една стара лутина.
- `S02` **NAR** — Кралицата Стенебеја не можеше да заспие од навредата.
- `S03` **NAR** — За неа тоа беше непростливо — а гостинот мораше да плати.
- `S04` **NAR** — Утрото, таа го преколнуваше сопругот да ѝ ја исполни желбата.
- `S04` **DLG** — Стенебеја: „Сакам неговата крв! Отстрани го Белерофон!“
- `S05` **NAR** — Нејзиниот збор беше како кама — остар и брз.
- `S05` **DLG** — Стенебеја: „Не смее да остане жив!“
- `S06` **NAR** — Но кралот знаеше дека гостинот е свет и недопирлив.
- `S06` **DLG** — Прет: „Не можам. Боговите ни забрануваат да го повредиме нашиот гостин.“
- `S07` **NAR** — Законот на гостите беше постар и посилен од секој гнев.
- `S08` **NAR** — Тогаш, во него се роди една подмолна смисла.
- `S09` **NAR** — Ќе го прати онаму каде никој не се враќа.
- `S10` **NAR** — На гостинот му назначи задача од која нема враќање.
- `S10` **DLG** — Прет: „Ќе одиш против Химера. Никој никогаш не преживеал.“
- `S11` **NAR** — А во дворот, под раното сонце, чекаше младиот гостин.
- `S12` **NAR** — Задачата му пристигна како тешка, студена клетва.
- `S13` **NAR** — Стравот немаше да го запре — само ќе го изостри.
- `S14` **NAR** — Со својот верен Пегаз, Белерофон се крена во небото.
- `S15` **NAR** — Летаа над диви предели, кон местото каде што никој не оди.
- `S16` **NAR** — Белерофон гледаше напред — и знаеше дека не смее да згреши.
- `S17` **NAR** — Таму, над една напукната планина, се креваше чад како предупредување.
- `S18` **NAR** — Тогаш, од темнината излезе суштеството кое не можеше да се опише со зборови.
- `S19` **NAR** — Лавовска глава, козјо тело и опашка од змија — сè во едно.
- `S20` **NAR** — Нејзината муцка беше печка, а очите — две жарчиња.
- `S21` **NAR** — Белерофон не трепна — тој мереше, а не се плашеше.
- `S22` **NAR** — Не му требаше меч — туку ладнокрвна глава.
- `S23` **NAR** — Чудовиштето полета кон нив, носејќи оган како копје.
- `S24` **NAR** — Од градите ѝ се крена бран од оган.
- `S25` **NAR** — И тогаш — блесок. Само така ќе ги изгаси пламените.
- `S26` **NAR** — Со еден замав, раздвоија небото и се спуштија кон земјата.
- `S27` **NAR** — Со острицата извади неколку тешки, сиви грутки од земјата.
- `S28` **NAR** — Од жештината, оловото се стопи во течен, сјаен метал.
- `S29` **NAR** — Повторно се кренаа, носијќи го течниот метал како тајно оружје.
- `S30` **NAR** — Сè беше готово — остана само вистинскиот миг.
- `S31` **NAR** — Химера ја отвори устата за да го проголта со оган.
- `S32` **NAR** — Таа зјапаше како отворена печка на небото.
- `S33` **NAR** — Но Белерофон беше побрз од самиот оган.
- `S34` **NAR** — И во последниот миг, го истури оловото точно во отворената уста.
- `S35` **NAR** — Металот за миг се стврдна — и чудовиштето замолкна.
- `S36` **NAR** — Оловото се зацврсти и го згасна огнот одвнатре.
- `S37` **NAR** — И така, чудовиштето од кое сите бегаа — падна.
- `S38` **NAR** — Горе остана само победникот и неговиот неразделен пријател.
- `S39` **NAR** — Утрото ја покри планината со мирна, розова светлина.
- `S40` **NAR** — Со полно сонце, Белерофон слета пред ѕидовите на Тиринт.
- `S41` **NAR** — Во неговите очи се мешаа умор и заслужена гордост.
- `S42` **NAR** — Пред кралот, стоеше жив — доказ дека постои и невозможен пат.
- `S43` **NAR** — Гневот во палатата се стопи како мраз на сонце.
- `S43` **DLG** — Прет: „Сè е простено. Ти донесе победа на нашиот град.“
- `S44` **NAR** — Никогаш порано не погледнал така — со благодарност.
- `S45` **NAR** — Белерофон се поклони — не од потчинетост, туку од мир.
- `S46` **NAR** — Палатата, некогаш студена, сега светеше од помиреност.
- `S47` **NAR** — А надвор, го чекаше неговиот крилест пријател.
- `S48` **NAR** — И заедно, полетаа кон уште многу нови авантури.

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
