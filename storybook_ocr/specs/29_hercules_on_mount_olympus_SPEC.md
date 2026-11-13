# 29 — Херкул на планината Олимп (Hercules on Mount Olympus)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Херкул на планината Олимп** — Завршувајќи ги дванаесетте подвизи, Херкул го врзува Кербер и се искачува на Олимп, каде ја добива својата вистинска награда — место меѓу боговите и божицата на младоста.

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
| Херкул / Hercules | Силниот полубог со лавовска кожа и клава | story-suggested | AI-default |
| Евристеј / Eurystheus | Плашлив крал кој издава задачи | story-suggested | AI-default |
| Ладон / Ladon | Огромниот змијски чувар на градината | story-suggested | AI-default |
| Кербер / Cerberus | Триглавото куче чувар на Подземјето | story-suggested | AI-default |
| Зевс / Zeus | Таткото на Херкул, крал на Олимп | story-suggested | AI-default |
| Хеба / Hebe | Божицата на младоста, невестата | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~155.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Евристеј му ја задава задачата за златните јаболка; Херкул ја наоѓа скриената градина и се соочува со чуварот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S03 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S04 | MEDIUM | low-angle | static | moderate | 3.0s | DLG |
| S05 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S06 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S07 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S08 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S10 | WIDE | low-angle | static | moderate | 3.0s | NAR |

### Act II — Пресврт

*Херкул го совладува Ладон, ја слуша наредбата за Кербер и слегува во Подземјето да се соочи со триглавото куче.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S11 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S12 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S13 | MEDIUM | over-shoulder | static | moderate | 3.0s | NAR |
| S14 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S15 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S16 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S17 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S18 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S19 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S20 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S21 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |

### Act III — Апотеоза

*Херкул го победува Кербер, го носи кај Евристеј, а потоа се искачува на Олимп, каде Зевс го прима и го венчава со Хеба.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S23 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S24 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S25 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S26 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S27 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S29 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S30 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S31 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S32 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S33 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S36 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S37 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S38 | WIDE | high-angle | static | moderate | 3.5s | NAR |
| S39 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S40 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S41 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S42 | WIDE | eye-level | static | moderate | 4.0s | NAR |
| S43 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S44 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S45 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S46 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S47 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S48 | WIDE | high-angle | crane-up | moderate | 4.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во зенитот на својата слава, Херкул доби уште еден необичен налог.
- `S02` **NAR** — Од балконот на својата палата, Евристеј го гледаше со мешавина од страв и презир.
- `S03` **NAR** — Меѓу прстите му беше испишана наредбата за златните јаболка.
- `S04` **DLG** — Евристеј: „Сега ги сакам златните јаболка од Градината на Хесперидите.“
- `S05` **NAR** — Во дворот, Херкул ја крена главата без трепкање.
- `S06` **NAR** — Градината беше скриена светиња, но нозете веќе го водеа по патот.
- `S07` **NAR** — Зад златната завеса од лисја се криеше градината посветена на Хера.
- `S08` **NAR** — Секое јаболко светеше со внатрешна жар.
- `S09` **NAR** — Но градината имаше свој чувар — и тој не спиеше.
- `S10` **NAR** — Од сенката се изви своето огромно тело.
- `S11` **NAR** — Херкул не се повлече ниту еден чекор.
- `S12` **NAR** — Неговата стрела беше подмачкана со смртоносниот отров на Хидра.
- `S13` **NAR** — Со еден потег, лакот запеа.
- `S14` **NAR** — Стрелата го најде ѕверот веднаш.
- `S15` **NAR** — Чуварот падна, а градината остана мирна.
- `S16` **NAR** — Но ветрот донесе уште една вест — за новата задача.
- `S17` **DLG** — Глас: „Ајде да ти кажам за последната задача... мора да го донесеш Кербер.“
- `S18` **NAR** — Најдлабокиот влез во Подземјето веќе го чекаше.
- `S19` **NAR** — Низ сенките, Херкул слезе до камените порти.
- `S20` **NAR** — Таму се издигна чудовиштето со три грла.
- `S21` **NAR** — Шест очи гледаа право во него.
- `S22` **NAR** — Херкул ги стегна тупаниците — знаеше дека силата нема да биде доволна.
- `S23` **NAR** — Вратата се отвори со татнеж од синџири.
- `S24` **NAR** — Кербер јуришна, земјата се тресеше.
- `S25` **NAR** — Не со жестокост, туку со ум — тој ги фати наколниците на ѕверот.
- `S26` **NAR** — Мускулите му се напрегнаа како бронзени јажиња.
- `S27` **NAR** — Чудовиштето почна да попушта.
- `S28` **NAR** — Со тешки синџири, тој го врза ѕверот.
- `S29` **NAR** — И го поведе нагоре, кон светлината на светот.
- `S30` **NAR** — Пред портите на Евристеј, градот онеме од чудото.
- `S31` **NAR** — Самиот Евристеј се скри во бронзена буре.
- `S32` **NAR** — Така заврши и последниот, дванаесетти подвиг.
- `S33` **NAR** — Но вистинската награда допрва следуваше.
- `S34` **NAR** — Чекор по чекор, смртникот се искачи кон Олимп.
- `S35` **NAR** — На врвот, палатите на боговите светеа без сенки.
- `S36` **NAR** — Зевс го прими со раширени раце.
- `S37` **NAR** — Таткото ја препозна силата и достоинството на синот.
- `S38` **NAR** — Сите богови на Олимп се собраа за свеченоста.
- `S39` **NAR** — Хеба, божицата на младоста, слезе по скалите.
- `S40` **NAR** — Очите на Херкул се сретнаа со нејзините.
- `S41` **DLG** — Зевс: „Денес мојот син станува дел од небесниот дом.“
- `S42` **NAR** — Венчавката го исполни Олимп со светлина.
- `S43` **NAR** — Вечниот сјај го облече смртникот како наметка.
- `S44` **NAR** — Веќе не смртник — Херкул стана бог.
- `S45` **NAR** — Ги гледаше полињата и градовите што некогаш го чекаа.
- `S46` **NAR** — Неговото име се изговараше со почит под небото.
- `S47` **NAR** — Лицето на младоста и лицето на силата — сега едно.
- `S48` **NAR** — И така, на планината Олимп, завршува приказната за Херкул.

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
