# 36 — Чудниот свирач од Хамелин (The Pied Piper of Hamelin)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Чудниот свирач од Хамелин** — Мистериозен свирач ја ослободува Хамелин од стаорците, а кога градот ја крши зделката, неговата освета ги одведува децата — сè додека едно мало дете не го допре неговото добро срце.

*Genre:* Легенда · таинствена бајка

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
| Свирачот / The Piper | Мистериозен, слаб патник во шарени крпени алишта; носи стара дрвена шупелка и има проникливи, тажни очи. | story-suggested | AI-default |
| Градоначалникот / The Mayor | Полничка, горделива градска старешина во скапи плишани плашти со златен синџир. | story-suggested | AI-default |
| Децата / The Children | Група мали деца од Хамелин во едноставни, светли градски кошули и капи. | story-suggested | AI-default |
| Малото дете / The Little Child | Најмалото, побледо и побавно дете со босо стапало и извеано капче; срцето на приказната. | story-suggested | AI-default |
| Жителите / The Townsfolk | Очајни граѓани и родители на Хамелин во средновековни волнени алишта. | story-suggested | AI-default |
| Стаорците / The Rats | Безброј свиленкасто-сиви глодачи со црвени очи; нечовечки ликови што ги преплавуваат улиците. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~163.0s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Наездата

*Утрото на наездата: стаорците го преплавуваат Хамелин; очајниот градоначалник ветува награда; се појавува таинствениот свирач во шарени крпени алишта и ја склучува зделката.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S02 | WIDE | eye-level | track | action | 3.0s | NAR |
| S03 | CLOSE-UP | low-angle | push-in | gentle | 3.0s | NAR |
| S04 | CLOSE-UP | high-angle | crane-down | gentle | 3.0s | NAR |
| S05 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S06 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S07 | WIDE | eye-level | static | moderate | 3.5s | DLG |
| S08 | WIDE | high-angle | static | action | 3.0s | NAR |
| S09 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S10 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S11 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S12 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |

### Act II — Волшебната мелодија

*Свирачот ја свири волшебната мелодија; стаорците, маѓепсани, го следат од градот до реката и исчезнуваат во водата; враќајќи се по наградата, свирачот е одбиен и навреден.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S14 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S15 | WIDE | high-angle | crane-down | action | 3.0s | NAR |
| S16 | CLOSE-UP | low-angle | push-in | gentle | 3.0s | NAR |
| S17 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S18 | WIDE | high-angle | track | moderate | 3.5s | NAR |
| S19 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S20 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S21 | WIDE | low-angle | static | action | 3.0s | NAR |
| S22 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S23 | MACRO | macro | push-in | gentle | 3.0s | NAR |
| S24 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S25 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S26 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S27 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S29 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S30 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S31 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S32 | CLOSE-UP | eye-level | static | action | 3.0s | NAR |
| S33 | WIDE | low-angle | track | moderate | 3.5s | NAR |

### Act III — Децата

*Налутен, свирачот свири повторно и децата го следат во шумата; малото дете го моли за милост; свирачот, со добро срце, му ја подарува шупелката и ги враќа децата дома; градот ја памети лекцијата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S34 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S35 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S36 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S37 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S39 | MEDIUM | low-angle | track | moderate | 3.5s | NAR |
| S40 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S41 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S42 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S43 | WIDE | low-angle | static | action | 3.0s | NAR |
| S44 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S45 | CLOSE-UP | high-angle | push-in | gentle | 3.0s | DLG |
| S46 | MEDIUM | eye-level | crane-down | moderate | 3.5s | NAR |
| S47 | CLOSE-UP | high-angle | static | gentle | 3.0s | DLG |
| S48 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S49 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S50 | WIDE | high-angle | crane-up | action | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Некогаш, покрај реката Весер, лежеше малиот град Хамелин.
- `S02` **NAR** — Едно утро градот се разбуди опколен од стаорци.
- `S03` **NAR** — Беа насекаде: во складиштата, во кујните, дури и покрај јадењето.
- `S04` **NAR** — Дојдоа и до креветчината на децата.
- `S05` **NAR** — Луѓето стоеја пред вратите, преплашени и немоќни.
- `S06` **NAR** — И градоначалникот беше очаен: завитка раце и се сожали на судбината.
- `S07` **DLG** — Градоначалник: „Илјада златници за оној што ќе нè спаси од оваа напаст!“
- `S08` **NAR** — Поминаа неколку денови, а никој не доаѓаше.
- `S09` **NAR** — Тогаш на портата се појави чуден, тесен силует.
- `S10` **DLG** — Свирач: „Ќе го ослободам Хамелин од стаорците… но во замена сакам илјада златници.“
- `S11` **DLG** — Градоначалник: „Договорено! Направи го тоа, и ќе добиеш сè што сакаш!“
- `S12` **NAR** — Така, со еден стисок, зделката беше склучена.
- `S13` **NAR** — Утрото свирачот излезе на средината на плоштадот.
- `S14` **NAR** — И почна да свири една чудна, милозвучна мелодија.
- `S15` **NAR** — Гласот на шупелката се разлеа низ улиците како топол ветер.
- `S16` **NAR** — Во темните дувла стаорците наострија уши.
- `S17` **NAR** — Еден по еден, тие излегоа од сенките.
- `S18` **NAR** — Стаорците, како маѓепсани, се собраа околу свирачот.
- `S19` **NAR** — Луѓето гледаа, скаменети, од прозорците.
- `S20` **NAR** — Свирачот ги поведе кон градската порта.
- `S21` **NAR** — Портата се отвори широко пред нив.
- `S22` **NAR** — Ги одведе надвор, по патот што води кон реката.
- `S23` **NAR** — Очите им беа празни и сјајни, како заслепени од музиката.
- `S24` **NAR** — На самиот брег, свирачот не престануваше да свири.
- `S25` **NAR** — И тогаш, како едно, сите се фрлија во брзата вода.
- `S26` **NAR** — За неколку минути во Хамелин не остана ниту еден стаорец.
- `S27` **NAR** — И гордо се упати кон градското собрание да си го земе ветеното.
- `S28` **NAR** — Но во собранието го чекаше сосема друг пречек.
- `S29` **DLG** — Свирач: „Дојдов за моите илјада златници.“
- `S30` **DLG** — Градоначалник: „Бегај оттука, несреќен скитнику! Никогаш нема да го платам тоа!“
- `S31` **NAR** — Во очите на свирачот се разгоре ладен жар.
- `S32` **NAR** — Вратата на собранието се тресна зад него.
- `S33` **NAR** — А тој, молчејќи, го крена инструментот уште еднаш.
- `S34` **NAR** — Па повторно засвири — но овојпат со друга, повеклива мелодија.
- `S35` **NAR** — Децата ги кренаа главите, а очите им светнаа.
- `S36` **NAR** — Смеејќи се, тие излегоа на улица и тргнаа по звукот.
- `S37` **NAR** — И сите мали деца го следеа свирачот кон портата.
- `S38` **NAR** — Мајките и татковците, со ужас, сфатија што се случува.
- `S39` **NAR** — Само едно мало дете заостана и не можеше да го стигне чекорот.
- `S40` **NAR** — Очајните родители побараа помош од градоначалникот.
- `S41` **NAR** — Но гласот му заглави во грлото.
- `S42` **NAR** — Децата го следеа свирачот длабоко во шумата.
- `S43` **NAR** — И застанаа пред влезот на една огромна пештера.
- `S44` **NAR** — Тогаш малото дете конечно ги стигна и се фрли пред нозете на свирачот.
- `S45` **DLG** — Малото дете: „Те молам… немој да нè одведеш!“
- `S46` **NAR** — А свирачот, кој имаше добро срце, се наведна до него.
- `S47` **DLG** — Свирач: „Ти свири на неа, тврдоглаво детенце. Ти ја подарувам. Ајде, со сите врати се дома.“
- `S48` **NAR** — И така децата тргнаа назад, дома, кон своите родители.
- `S49` **NAR** — На портата, воздишки и смеа — секое дете најде прегратка.
- `S50` **NAR** — А од тој ден, Хамелин секогаш ги држеше своите ветувања. За чудниот свирач веќе никој не слушна.

---

## 5. Acceptance criteria (testable)

1. Shot count = 50 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
