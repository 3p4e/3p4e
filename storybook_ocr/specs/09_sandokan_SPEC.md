# 09 — Сандокан (Sandokan)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **44 shots** (floor 40).

---

## 0. Concept

**Сандокан** — Малезискиот Тигар, пиратот Сандокан, се заколнува на одмазда против британските поробувачи — но една средба со англиската девојка Маријана го претвора ловецот во вљубен човек.

*Genre:* Авантура · епска акција · романса

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
| Сандокан / Sandokan | Харизматичен пират-водач, наречен Малезискиот Тигар, храбар и решителен, со црвен турбан | story-suggested | AI-default |
| Маријана / Marianna | Убава и нежна внука на лордот Гилонк, вљубена во Сандокан | story-suggested | AI-default |
| Лорд Џејмс Гилонк / Lord James Gillock | Англиски благородник, благороден и доверлив домаќин | story-suggested | AI-default |
| Јанез / Yanez | Верната десна рака на Сандокан, лукав и храбар пријател | story-suggested | AI-default |
| Британски војници / British soldiers | Непријателски војници во црвени униформи што ги гонат пиратите | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**44 shots · ~150.0s runtime · 221.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Го запознаваме Сандокан, Малезискиот Тигар, неговата заклетва за одмазда, потопувањето на бродот и спасоносниот брег во Лабуан.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S02 | CLOSE | low-angle | push-in | gentle | 3.5s | NAR |
| S03 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S04 | WIDE | eye-level | track | moderate | 4.0s | NAR |
| S05 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S06 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S07 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S08 | INSERT | eye-level | static | gentle | 2.5s | NAR |
| S09 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S10 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S11 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S12 | MEDIUM | high-angle | crane-down | moderate | 3.5s | NAR |

### Act II — Ловот, занданата и враќањето

*Во куќата на лордот Гилонк, Сандокан се претставува како бродоломен принц и ја запознава Маријана; ловот на тигри го разоткрива, но Јанез го спасува — а љубовта го влече назад.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S14 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S15 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S16 | OVER | over-shoulder | static | gentle | 3.0s | NAR |
| S17 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S18 | WIDE | eye-level | static | moderate | 3.5s | DLG |
| S19 | INSERT | macro | static | gentle | 2.5s | NAR |
| S20 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S21 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S22 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S23 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S24 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S25 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S26 | WIDE | high-angle | static | action | 3.0s | NAR |
| S27 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S28 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S29 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S30 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | DLG |
| S31 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S32 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S33 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S34 | WIDE | eye-level | track | moderate | 4.0s | NAR |
| S36 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |

### Act III — Љубовта победува

*Сандокан се враќа по Маријана, двајцата бегаат со бродот и се венчаат на Момпрачем на зајдисонце.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S35 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S37 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S39 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S40 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S41 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S42 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S43 | WIDE | low-angle | static | moderate | 4.0s | NAR |
| S44 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — На далечните мориња на Малезија, еден човек го знаеја како Малезискиот Тигар.
- `S02` **NAR** — Тој беше Сандокан, пират чија храброст втеруваше страв во срцата на непријателите.
- `S03` **NAR** — Откако непријателот му го одзеде семејството, Сандокан се заколна на одмазда.
- `S03` **DLG** — Сандокан: „Ќе се борам до крај со поробувачите!“
- `S04` **NAR** — Така направи: собра верна дружина што ќе го следи до крајот на светот.
- `S05` **NAR** — Неговиот брод ги гонеше непријателските бродови преку бескрајната вода.
- `S06` **NAR** — Топовите грмеа, а непријателскиот брод тонеше под црното знаме.
- `S07` **NAR** — Но надојде нерамноправна битка: цела флота ги опколи.
- `S08` **NAR** — Едно топовско ѓуле ја погоди палубата и бродот почна да се крши.
- `S09` **NAR** — Бродот на Тигарот се наведна и потона во разбеснетото море.
- `S10` **NAR** — Ранетиот Сандокан ги собра сите сили и заплива низ брановите.
- `S11` **NAR** — До зори доплива до плажата во Лабуан и се струполи на песокот.
- `S12` **NAR** — Некои слуги го најдоа онесвестен на плажата и го кренаа на раце.
- `S13` **NAR** — Кога се разбуди, Сандокан виде дека лежи на мека постела, во туѓа куќа.
- `S14` **NAR** — Сè му беше матно, но знаеше дека мора да го скрие своето вистинско име.
- `S15` **NAR** — Покрај него стоеше убавата Маријана, внуката на лордот Гилонк.
- `S16` **NAR** — Ако го откриеја неговиот вистински идентитет, Англичаните ќе го затвореа.
- `S17` **NAR** — И ја кажа приказната: дека е малезиски принц што преживеал бродолом.
- `S17` **DLG** — Сандокан: „Јас сум принц чиј брод го проголта морето.“
- `S18` **NAR** — Дојде лордот Гилонк, поверува на приказната и му понуди да остане додека не закрепне.
- `S18` **DLG** — Лорд Гилонк: „Бидете ми гостин, господине.“
- `S19` **NAR** — Поминаа денови, и Сандокан полека закрепна.
- `S20` **NAR** — На имотот се подготвуваше лов на тигри, со британски војници.
- `S21` **NAR** — Сандокан влезе сам во шумата, длабоко до срцето на џунглата.
- `S22` **NAR** — Одеднаш, лице в лице се најде со страшниот тигар.
- `S23` **NAR** — Сандокан го нападна со својот препознатлив воен крик.
- `S24` **NAR** — Но неговиот крик го слушнаа војниците што се беа бореле со него.
- `S24` **DLG** — Војници: „Те препознавме, пирату!“
- `S25` **NAR** — Војниците го заробија и го одвлекоа низ шумата.
- `S26` **NAR** — Го фрлија во мрачната зандана на лордовиот имот.
- `S27` **NAR** — Во окови, во темнина, Сандокан не го загуби својот пркос.
- `S28` **NAR** — Таа ноќ, во палатата на Гилонк засветлеа свеќите на големиот бал.
- `S29` **NAR** — Тој странец беше Јанез, верната десна рака на Сандокан, преправен како шкотски лорд.
- `S30` **NAR** — Јанез го најде својот пријател во занданата и скрши еден катанец.
- `S30` **DLG** — Јанез: „Дојди, Тигаре. Тие пеат горе.“
- `S31` **NAR** — Двајцата се лизнаа како сенки низ палатата и избегаа во ноќта.
- `S32` **NAR** — На островот Момпрачем, во скривалиштето, Тигарот доби слобода — но не и мир.
- `S33` **NAR** — Сандокан беше вљубен во Маријана и не можеше да ја заборави.
- `S33` **DLG** — Сандокан: „Ќе се вратам по тебе, Маријана.“
- `S34` **NAR** — И така, со своите верни „тигри“, го подготви бродот за враќање.
- `S36` **NAR** — На брегот, Сандокан се скри меѓу грмушките покрај градината.
- `S35` **NAR** — Бродот на Малезискиот Тигар пресече низ ноќта кон Лабуан.
- `S37` **NAR** — Тивко се провлече во градината и застана во сенката.
- `S38` **NAR** — Само што го виде, Маријана се стрча кон него и го прегрна.
- `S38` **DLG** — Маријана: „Се врати! Знаев дека ќе дојдеш.“
- `S39` **NAR** — И таа го сакаше. Мораа да побегнат пред да сване.
- `S40` **NAR** — Двајцата побегнаа низ градината кон брегот, рака под рака.
- `S41` **NAR** — Чекаше бродот на Тигарот, и тие се качија и испловија на полно море.
- `S42` **NAR** — Лабуан остана далеку зад нив, само сенка на вода.
- `S43` **NAR** — И на Момпрачем, на зајдисонце, се венчаа пред своите верни тигри.
- `S44` **NAR** — Така Тигарот на морето го најде својот дом — во срцето на Маријана.

---

## 5. Acceptance criteria (testable)

1. Shot count = 44 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
