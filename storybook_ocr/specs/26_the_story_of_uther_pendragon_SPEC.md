# 26 — Приказната за Утер Пендрагон (The Story of Uther Pendragon)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Приказната за Утер Пендрагон** — Храбриот принц Утер, следејќи го пророштвото на волшебникот Мерлин од кометата-змеј, станува крал Пендрагон и, опкружен со непријатели, го доверува својот син Артур на мудриот волшебник.

*Genre:* Брешонска легенда · епска акција

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
| Утер Пендрагон / Uther Pendragon | Храбар принц, подоцна крал; силен, решително лице со оклоп на црвен змеј | story-suggested | AI-default |
| Мерлин / Merlin | Стар, мудар волшебник со долга бела брада, стап и светечка магија | story-suggested | AI-default |
| Крал Амброзиј / King Ambrosius | Постар, благороден крал, брат на Утер | story-suggested | AI-default |
| Играин / Igraine | Убава, нежна кралица со топло, грижливо срце | story-suggested | AI-default |
| Артур / Arthur (бебе) | Мил, светлокос бебе со мирно лице | story-suggested | AI-default |
| Непријатели / Enemies | Саксонски воини и војски на границата, темни оклопи | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~161.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Кометата-змеј

*Во древна Британија живее храбар принц Утер, брат на кралот Амброзиј. Кога Мерлин здогледува комета во облик на змеј и му прорекува дека ќе стане крал, Амброзиј умира и Утер го презема тронот, земајќи го името Пендрагон.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S03 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S04 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S05 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S06 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S07 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S08 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S09 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S10 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S11 | INSERT | macro | static | gentle | 3.0s | NAR |
| S12 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S13 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S14 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |

### Act II — Кралицата и принцот

*Кралот ја избира убавата Играин за своја кралица. Им се раѓа син Артур. Но додека семејството доживува радост, на границите се собираат непријатели, па Утер решава да го довери Артур на Мерлин.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S17 | MEDIUM | over-shoulder | static | moderate | 3.0s | DLG |
| S18 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S19 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S20 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S21 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S23 | WIDE | high-angle | pan-right | moderate | 3.5s | NAR |
| S24 | INSERT | macro | static | gentle | 3.0s | NAR |
| S25 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S26 | MEDIUM | shot-reverse | static | moderate | 3.5s | DLG |
| S27 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S29 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S30 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S31 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S32 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S33 | MEDIUM | low-angle | track | moderate | 3.5s | NAR |
| S34 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S35 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S36 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S37 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S38 | CLOSE | eye-level | static | gentle | 3.5s | NAR |

### Act III — Змејовата глава

*Утер, како Пендрагон, ја поведува војската во битка под багроволикиот знаме, додека Мерлин се грижи и го подучува малиот Артур длабоко во шумата, полагајќи го семето на идната легенда.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S40 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S41 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S42 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S43 | INSERT | macro | static | gentle | 3.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S45 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S46 | INSERT | macro | static | gentle | 3.0s | NAR |
| S47 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S48 | CLOSE | eye-level | push-in | gentle | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Пред повеќе од илјада и петстотини години, во магливата Британија живееше еден принц.
- `S02` **NAR** — Тоа беше Утер, брат на кралот Амброзиј и најхрабар од сите воини.
- `S03` **NAR** — Благодарение на неговата смелост, секогаш ги поразуваше своите непријатели.
- `S04` **NAR** — Но не беше сам — негов верен пријател беше големиот волшебник Мерлин.
- `S05` **NAR** — Една ноќ, Мерлин ги следеше ѕвездите од неговата кула.
- `S06` **NAR** — Тогаш на небото се појави голема комета во облик на змеј.
- `S07` **NAR** — Обликот на змејот светеше како жив оган.
- `S08` **NAR** — Со сигурен глас, Мерлин му рече на Утер дека наскоро ќе стане крал.
- `S08` **DLG** — Мерлин: „Наскоро ќе станеш крал.“
- `S09` **NAR** — Набрзо потоа, кралот Амброзиј мирно почина.
- `S10` **NAR** — Утер остана единствениот законит владетел на Британија, токму како што предвиде Мерлин.
- `S11` **NAR** — Во чест на кометата, Утер нареди на својот оклоп да биде нацртан црвен змеј.
- `S12` **NAR** — Го зеде името Пендрагон, што значи „змејова глава“.
- `S12` **DLG** — Утер: „Од денес, јас ќе бидам Пендрагон.“
- `S13` **NAR** — Пендрагон се издигна над сите останати, а неговото име одекна низ целата земја.
- `S14` **NAR** — Но на кралот му требаше кралица покрај него.
- `S15` **NAR** — Утер го бараше правото срце за своја кралица.
- `S16` **NAR** — Таа се викаше Играин — убава, нежна и блага.
- `S17` **NAR** — Утер ја избра Играин, и таа стана кралица покрај него.
- `S17` **DLG** — Утер: „Ќе бидеш мојата кралица.“
- `S18` **NAR** — На свадбата, целата земја се радуваше.
- `S19` **NAR** — Потоа дојде вест исполнета со среќа — во дворецот ќе се роди дете.
- `S20` **NAR** — И така се роди едно дете, кое го нарекоа Артур.
- `S21` **NAR** — Малиот Артур беше мирен, со очи полни светлина.
- `S22` **NAR** — Утер и Играин ја држеа бесценетата нова радост.
- `S22` **DLG** — Играин: „Артур... тој е совршен.“
- `S23` **NAR** — Но на границата, од сенките се собираа непријатели.
- `S24` **NAR** — Над нивните кампови тапаните биеја како далечен гром.
- `S25` **NAR** — Утер знаеше дека битката доаѓа.
- `S26` **NAR** — Кралот беше опкружен со непријатели, па мораше да донесе тешка одлука.
- `S26` **DLG** — Утер: „Овде Артур не е безбеден.“
- `S27` **NAR** — Утер го зеде својот син в раце, тежок од тага.
- `S28` **NAR** — Реши да го довери Артур на Мерлин — оној кој го учеше и му прорече сѐ.
- `S29` **NAR** — Со мудра смиреност, Мерлин го прифати бебето.
- `S29` **DLG** — Мерлин: „Не грижи се. Ќе биде безбеден со мене.“
- `S30` **NAR** — Ќе го учеше литература и наука, а можеби и неколку волшебнички трикови.
- `S31` **NAR** — Играин, со солзи во очите, ја кажа својата мајчинска молба.
- `S31` **DLG** — Играин: „Пази на моето момче, Мерлин.“
- `S32` **NAR** — Потоа Мерлин исчезна во шумата со бебето во раце.
- `S33` **NAR** — Низ древната шума, Мерлин го носеше Артур како што би носел ризница.
- `S34` **NAR** — Од далечина, катанецот на замокот се спушти зад нив.
- `S35` **NAR** — А Утер се врати во салата, каде војската веќе чекаше.
- `S36` **NAR** — Тој ја собра својата војска за следната битка.
- `S36` **DLG** — Утер: „Соберете ги луѓето. Одиме во војна.“
- `S37` **NAR** — Во долината пред дворецот, војските се подредија во црвени редови.
- `S38` **NAR** — Утер погледна кон шумата, знаејќи дека синот му е на сигурно.
- `S39` **NAR** — Со црвениот змеј напред, Утер ја поведе војската кон границата.
- `S40` **NAR** — Неговата решителност гореше посветло од било кој оган.
- `S41` **NAR** — Низ ридовите, непријателските војски дојдоа да го пречекаат.
- `S42` **NAR** — Далеку во шумата, Мерлин ја палеше ограната лулка.
- `S43` **NAR** — Книгите и науката се отвораа пред малиот Артур како светулка во ноќта.
- `S44` **NAR** — Додека Утер се бореше, Мерлин го подучуваше Артур на мирни работи.
- `S44` **DLG** — Мерлин: „Еден ден, и ти ќе водиш. Но со мудрост, не со меч.“
- `S45` **NAR** — Пендрагон ја поведе војската напред, а црвениот змеј го крилеше со крилјата.
- `S46` **NAR** — Знамето со змејовата глава се вивна високо над бојното поле.
- `S47` **NAR** — Така името Пендрагон — „змејова глава“ — остана да свети низ вековите.
- `S48` **NAR** — А во шумата, малото семе на идната легенда растеше под закрила на волшебникот.

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
