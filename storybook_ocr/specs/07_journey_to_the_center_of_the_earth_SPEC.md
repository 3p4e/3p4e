# 07 — Патување во центарот на Земјата (Journey to the Center of the Earth)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **42 shots** (floor 40).

---

## 0. Concept

**Патување во центарот на Земјата** — Професор и неговиот внук следат древен ракопис длабоко под земјата, преминуваат подземен океан и излегуваат на светло преку вулкан.

*Genre:* Авантура · научна фантастика

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
| Професор Лиденброк | Постар германски научник, опседнат, храбар и решен | story-suggested | AI-default |
| Аксел | Млад внук, внимателен и исплашен, но верен и расте во храброст | story-suggested | AI-default |
| Ханс | Исландски водич, тивок, вешт и невознемирен | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**42 shots · ~144.0s runtime · 211.7s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Во Хамбург, професорот Лиденброк открива стар ракопис на Арне Сакнусем со патот до центарот на Земјата. Со внукот Аксел тргнуваат кон Исланд и со водичот Ханс се искачуваат на изгасениот вулкан.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S02 | INSERT | high-angle | static | gentle | 3.0s | NAR |
| S03 | MEDIUM | low-angle | track | moderate | 3.5s | DLG |
| S04 | MEDIUM | over-shoulder | static | moderate | 3.0s | NAR |
| S05 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S06 | WIDE | eye-level | static | moderate | 3.5s | DLG |
| S07 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S08 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S10 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S11 | MEDIUM | low-angle | track | moderate | 3.5s | DLG |
| S12 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

### Act II — Подземниот свет

*Тројцата слегуваат во вулканот и стигнуваат до подземен океан со предисториски суштества. Го преминуваат со сплав, ги носат назад, ги наоѓаат иницијалите на Сакнусем, а динамитот отвора буица што ги однесе низ тунел нагоре.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | MEDIUM | high-angle | crane-down | moderate | 3.5s | NAR |
| S14 | WIDE | low-angle | pan-right | moderate | 3.5s | NAR |
| S15 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S16 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S17 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S18 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |
| S19 | WIDE | eye-level | track | moderate | 3.5s | DLG |
| S20 | WIDE | high-angle | static | moderate | 3.5s | NAR |
| S21 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S22 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | NAR |
| S23 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S24 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S25 | INSERT | macro | push-in | gentle | 3.5s | DLG |
| S26 | MEDIUM | low-angle | pan-right | moderate | 3.5s | NAR |
| S27 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S28 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S29 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S30 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S31 | WIDE | low-angle | pan-right | moderate | 3.5s | NAR |
| S32 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |

### Act III — Враќање на светлина

*Исфрлени на врвот на вулканот Стромболи во Сицилија, тројцата се извлекуваат неповредени и се собраат крај огништето со неверојатна приказна за раскажување.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S33 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S34 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S35 | MEDIUM | eye-level | pan-right | moderate | 3.5s | NAR |
| S36 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S37 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |
| S38 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S39 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |
| S40 | INSERT | eye-level | static | gentle | 3.0s | NAR |
| S41 | MEDIUM | over-shoulder | static | moderate | 3.5s | NAR |
| S42 | WIDE | eye-level | pull-back | moderate | 3.5s | DLG |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во стариот Хамбург, во полн со прашина работен кабинет, професорот Лиденброк проучуваше древни ракописи.
- `S02` **NAR** — Меѓу страниците се криеше еден стар, потемнет ракопис на таинствениот Арне Сакнусем.
- `S03` **NAR** — Одеднаш професорот скокна од столот и извика кон својот внук.
- `S03` **DLG** — Лиденброк: „Аксел! Гледај што најдов!“
- `S04` **NAR** — Неговиот внук Аксел, млад и љубопитен, ја погледна страницата.
- `S05` **NAR** — Професорот објави дека ракописот содржи насоки како да се стигне до самиот центар на Земјата.
- `S05` **DLG** — Лиденброк: „Содржи насоки како да се стигне до... центарот на Земјата!“
- `S06` **NAR** — Лиденброк никогаш не го напуштал Хамбург, но овој пат не се двоумеше.
- `S06` **DLG** — Лиденброк: „Спакувај се. Одиме на Исланд!“
- `S07` **NAR** — Вујкото и внукот се качија на брод што пловеше кон Рејкјавик.
- `S08` **NAR** — Низ студените северни мориња, пред нив се издигна дивиот, снежен брег на Исланд.
- `S09` **NAR** — Во Рејкјавик ги пречека висок и тивок водич, Ханс, искусен по планините.
- `S10` **NAR** — Упатствата беа јасни: мораа да се искачат по еден огромен, изгасен вулкан.
- `S11` **NAR** — Аксел беше исплашен, но професорот го смируваше.
- `S11` **DLG** — Лиденброк: „Најмив искусен водич, ништо нема да ти се случи.“
- `S12` **NAR** — По карпести патеки полни со опасности, тројцата стигнаа до врвот и погледнаа во темниот кратер.
- `S13` **NAR** — Опремени со јажиња, светилки и копачи, тројцата почнаа да слегуваат во внатрешноста на вулканот.
- `S14` **NAR** — Длабоко под земјата светлината од светилките откри карпи што изгледаа како скалила на џинови.
- `S15` **NAR** — Со денови пешачеа, спуштајќи се сè подлабоко во стомакот на Земјата.
- `S16` **NAR** — Одеднаш, пред нив се отвори огромна подземна плажа покрај бескраен океан.
- `S17` **NAR** — Плажата беше полна со предисториски растенија и огромни коски.
- `S18` **NAR** — Професорот стоеше пред џиновски коски, збунет и воодушевен од светот што никој не го видел.
- `S18` **DLG** — Лиденброк: „Свет од пред милиони години... пред нашите очи!“
- `S19` **NAR** — За да го преминат океанот, решија да изградат сплав од предисториско дрво.
- `S19` **DLG** — Лиденброк: „Ќе изградиме сплав и ќе го преминеме!“
- `S20` **NAR** — На сплавот, среде подземниот океан, патувањето стана опасно.
- `S21` **NAR** — Огромни морски чудовишта кренаа бранови што го тресеа нивниот сплав.
- `S22` **NAR** — Аксел и професорот се држеа за сплавот додека Ханс вешто управуваше низ брановите.
- `S23` **NAR** — Откако брановите се смирија, сфатија дека ги однело назад на истото место од кое отпловија.
- `S24` **NAR** — Почнаа да бараат друг премин и најдоа тесна пештера во карпата.
- `S25` **NAR** — На ѕидот стоеја две изрезбани букви: „А“ и „С“.
- `S25` **DLG** — Лиденброк: „Иницијалите на Арне Сакнусем! Ова е вистинскиот пат!“
- `S26` **NAR** — Но преминот понатаму беше блокиран од огромни карпи.
- `S27` **NAR** — Водичот предложи да ги разнесат карпите со динамит.
- `S27` **DLG** — Ханс: „Ќе ги разнесеме со динамит.“
- `S28` **NAR** — Ја запалија фитилот и се повлекоа зад карпите.
- `S29` **NAR** — Експлозијата прогрме и предизвика огромна буица вода да ја исполни пештерата.
- `S30` **NAR** — Буицата ги однесе тројцата низ тесен, темни тунел со голема брзина.
- `S31` **NAR** — Како плутани, тие летаа низ врела вода кои се пробиваа нагоре.
- `S32` **NAR** — Одеднаш светлината се проби и водата ги исфрли високо во воздухот.
- `S33` **NAR** — Кога се созедоа, сфатија дека стојат на врвот на вулканот Стромболи, во Сицилија.
- `S34` **NAR** — Професорот крена поглед и го виде синото небо над себе.
- `S34` **DLG** — Лиденброк: „На сигурно сме!“
- `S35` **NAR** — Аксел лежеше на карпите, смеејќи се од неверување и радост.
- `S36` **NAR** — Дури и тивкиот Ханс стоеше наведнат, гледајќи кон морето.
- `S37` **NAR** — Тројцата, извалкани од саѓи и морска вода, почнаа полека да се спуштаат по страната на вулканот.
- `S38` **NAR** — Ноќе, во едно селце крај морето, се собраа крај огниште полни со нова приказна.
- `S39` **NAR** — Професорот, како стар научник, зборуваше со раце полни со возбуда.
- `S39` **DLG** — Лиденброк: „Се спуштивме во земјата, а излеговме од небото!“
- `S40` **NAR** — На масата лежеше ракописот на Арне Сакнусем, потврда на нивниот неверојатен пат.
- `S41` **NAR** — Аксел се насмеа, гледајќи кон својот вујко со нова почит.
- `S42` **NAR** — Имаа неверојатна приказна за раскажување — приказна што ќе го промени светот на науката.
- `S42` **DLG** — Лиденброк: „И имаме неверојатна приказна за раскажување!“

---

## 5. Acceptance criteria (testable)

1. Shot count = 42 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
