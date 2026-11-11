# 17 — Дартањан и тројцата мускетари (D'Artagnan and the Three Musketeers)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Дартањан и тројцата мускетари** — Младиот Гасконец Дартањан пристигнува во Париз да стане мускетар, но прво мора да ги победи, а потоа да ги придобие Атос, Портос и Арамис — пред кралска мисија за дванаесетте дијаманти да ги сплоти во неразделен квартет.

*Genre:* Историска авантура · епска акција

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
| Дартањан / D'Artagnan | Млад Гасконец, желен за слава, со испилени црти, темна коса и табатски меч | story-suggested | AI-default |
| Атос / Athos | Благороден и достоинствен мускетар, сериозен, со темна брадичка и елегантна униформа | story-suggested | AI-default |
| Портос / Porthos | Крупен и весел мускетар со раскошен појас и громогласен глас | story-suggested | AI-default |
| Арамис / Aramis | Префинет мускетар со чисти црти, мазен говор и грациозно држење | story-suggested | AI-default |
| Кардинал Ришелје / Cardinal Richelieu | Моќен кардинал во црвена одежда, остар поглед и студено држење | story-suggested | AI-default |
| Милејди / Milady | Злобна шпионка на кардиналот, елегантна и лукава, со темен превез | story-suggested | AI-default |
| Кралицата / The Queen | Француската кралица, достоинствена и љубезна, во светла дворска тоалета | story-suggested | AI-default |
| Војвода од Бакингам / Duke of Buckingham | Висок, префинет англиски благородник со сјајна облека и стрплива тага | story-suggested | AI-default |
| Војниците на кардиналот / The Cardinal's Guards | Гардисти во темни униформи со калпаци, дисциплинирани и груби | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~153.0s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Младиот Гасконец Дартањан пристигнува во Париз и налетува на тројцата мускетари, кои го предизвикуваат на двобој. Кога гардата на кардиналот го прекинува двобојот, Дартањан застанува на страната на мускетарите и сите четворица ги победуваат.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S04 | INSERT | eye-level | pan-left | gentle | 3.0s | NAR |
| S05 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S06 | CLOSE | over-shoulder | shot-reverse | gentle | 3.5s | DLG |
| S07 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S08 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S09 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S10 | WIDE | eye-level | track | moderate | 3.5s | DLG |
| S11 | MEDIUM | low-angle | push-in | moderate | 3.0s | DLG |
| S12 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S13 | MEDIUM | low-angle | pull-back | moderate | 3.5s | DLG |

### Act II — Пресврт

*Кралицата ги праќа четворицата да ги вратат дванаесетте дијаманти од војводата од Бакингам. На патот кон Лондон ги пречекува заседа на кардиналовите војници; само Дартањан стигнува до војводата, кој открива дека злобната Милејди украла два дијаманта.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S15 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S16 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S17 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S18 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S19 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S20 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S21 | WIDE | high-angle | crane-down | moderate | 3.5s | DLG |
| S22 | MEDIUM | eye-level | pan-right | moderate | 3.5s | NAR |
| S23 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S24 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S25 | WIDE | high-angle | track | moderate | 3.5s | NAR |
| S26 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S27 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S28 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S29 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S30 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |

### Act III — Кулминација

*Дартањан се враќа во Париз и ја фаќа Милејди во последен момент пред бало, ги враќа дијамантите и ја спасува мисијата. Кралицата наредува да биде унапреден во полковник, а неговиот сон конечно станува стварност.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S31 | WIDE | high-angle | track | moderate | 3.5s | NAR |
| S32 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S33 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S34 | CLOSE | over-shoulder | shot-reverse | gentle | 3.5s | DLG |
| S35 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S36 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S37 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S39 | CLOSE | over-shoulder | shot-reverse | gentle | 3.5s | DLG |
| S40 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S41 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S42 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S43 | MEDIUM | high-angle | static | moderate | 3.0s | NAR |
| S44 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S45 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S46 | WIDE | low-angle | pull-back | moderate | 3.5s | DLG |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Од југ, од прашливите патишта на Гаскоњ, пристигнуваше еден млад и дрзок сонувач.
- `S02` **NAR** — Го викаа Дартањан, и носеше само еден сон на ум.
- `S03` **NAR** — Во Париз стоеше палатата, дом на мускетарите — избраната гарда на кралот.
- `S04` **NAR** — Додека излегуваше од Версај, брзаше и не гледаше каде оди.
- `S05` **NAR** — Со еден несмасент удар се судри во Атос, Арамис и Портос.
- `S05` **DLG** — Атос: „Гледај каде одиш, момче!“
- `S06` **NAR** — Навредени од непокажувањето почит, тие му наредија двобој.
- `S06` **DLG** — Портос: „Го гледаш ли тоа дрско лице? Ќе платиш за ова!“
- `S07` **NAR** — Дартањан, сосема сигурен во себе, прифати.
- `S07` **DLG** — Дартањан: „Ве чекам утре напладне под ѕидините на кралската палата.“
- `S08` **NAR** — Следниот ден, точно напладне, четворицата застанаа под ѕидините.
- `S09` **NAR** — Но дуелот никогаш не почна.
- `S10` **NAR** — Пристигнаа војниците на кардиналот Ришелје, советникот кој правеше што сака на дворот.
- `S10` **DLG** — Војник: „Двобоите се забранети од кралот! Уапсени сте!“
- `S11` **NAR** — Без да размисли, Дартањан го извлече мечот и застана на страната на тројцата мускетари.
- `S11` **DLG** — Дартањан: „Ако ве апсат, тогаш и мене ќе ме апсете!“
- `S12` **NAR** — Заедно ги изгонија војниците.
- `S13` **NAR** — Од тој ден станаа најдобри пријатели и си дадоа заклетва.
- `S13` **DLG** — Атос и Портос: „Еден за сите!“ Арамис и Дартањан: „Сите за еден!“
- `S14` **NAR** — Деновите минаа, но нивното пријателство остана челично.
- `S15` **NAR** — По некое време, француската кралица ги повика кај себе.
- `S16` **NAR** — Таа им довери една многу важна задача.
- `S16` **DLG** — Кралицата: „Одете кај војводата од Бакингам и кажете му да ми ги врати дванаесетте дијаманти.“
- `S17` **NAR** — Тоа беа нејзиниот подарок од кралот.
- `S18` **NAR** — Кралот сакаше да ги носи на следниот дворски бал.
- `S18` **DLG** — Кралицата: „Тие ми се подарок од кралот, и мора да ги носам на бало.“
- `S19` **NAR** — Честа им беше да и служат.
- `S19` **DLG** — Четворицата: „Чест ни е што Ви служиме, Височество.“
- `S20` **NAR** — Веднаш заминаа на пат кон морето.
- `S21` **NAR** — Пред да се качат на бродот за Лондон, повторно беа нападнати.
- `S21` **DLG** — Портос: „Ах, пак војниците на кардиналот!“
- `S22` **NAR** — Кардиналот ги следеше бидејќи мислеше лошо на кралицата.
- `S23` **NAR** — Само Дартањан успеа да се пробие.
- `S23` **DLG** — Атос: „Оди! Ние ќе ги задржиме!“
- `S24` **NAR** — Бродот исплови, а тројцата останаа безбедни на кејот.
- `S25` **NAR** — Стигна во Лондон, во дворецот на војводата од Бакингам.
- `S26` **NAR** — Војводата го прими во својата одаја.
- `S26` **DLG** — Војвода: „Добредојде, мускетару. Имаш вести од кралицата?“
- `S27` **NAR** — Потоа лицето му се смрачи.
- `S27` **DLG** — Војвода: „Имам само десет дијаманти. Другите два ги украде злобната Милејди.“
- `S28` **NAR** — Два гнезда стоеја празни.
- `S29` **NAR** — Милејди — шпионка на кардиналот Ришелје.
- `S29` **DLG** — Дартањан: „Милејди? Која е таа?“ Војвода: „Шпионка на кардиналот.“
- `S30` **NAR** — Остануваше малку време, а бало наближуваше.
- `S30` **DLG** — Дартањан: „Морам да се вратам пред бало.“
- `S31` **NAR** — Бродот брзаше назад кон Франција.
- `S32` **NAR** — Дартањан влета во Париз сред ноќ.
- `S33` **NAR** — Пријателите го пречекаа со прегратки.
- `S34` **NAR** — Но мисијата уште не беше завршена.
- `S34` **DLG** — Дартањан: „Два дијаманта украде Милејди. Треба да ја најдам пред бало.“
- `S35` **NAR** — Го бараа низ осветлените коридори на палатата.
- `S36` **NAR** — Пред нив — Милејди, шпионката на кардиналот.
- `S37` **NAR** — Потерата се разгори.
- `S38` **NAR** — Во една темна одаја, Милејди остана без излез.
- `S38` **DLG** — Милејди: „Нема да стигнеш...“
- `S39` **NAR** — Дартањан ја побара назад.
- `S39` **DLG** — Дартањан: „Дај ми ги дијамантите. Веднаш.“
- `S40` **NAR** — Двата дијаманта паднаа во неговата дланка.
- `S41` **NAR** — Токму пред бало, сите дванаесет беа повторно заедно.
- `S42` **NAR** — Кралицата ја носеше сјајната низа, а кралот гледаше со гордост.
- `S43` **NAR** — Само кардиналот Ришелје гледаше од сенка, мрачен.
- `S44` **NAR** — Мисијата беше успешна, и доаѓаше награда.
- `S44` **DLG** — Кралицата: „За неговата храброст, нека биде унапреден во полковник на мускетарите!“
- `S45` **NAR** — Кардиналот мораше да нареди, но во очите му гореше злоба.
- `S45` **DLG** — Ришелје: „Нека биде така.“
- `S46` **NAR** — Дартањан прослави со своите неразделни пријатели — неговиот сон конечно стана стварност.
- `S46` **DLG** — Четворицата: „За мускетарите!“

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
