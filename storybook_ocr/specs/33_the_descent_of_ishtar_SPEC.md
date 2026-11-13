# 33 — Слегувањето на Иштар (The Descent of Ishtar)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Слегувањето на Иштар** — Моќната божица на љубовта Иштар слегува во подземјето за да ја види сестра си Ерешкигал, но останува заробена — и само замена со сопствениот неверен маж ѝ го враќа престолот над Земјата.

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
| Иштар / Ishtar | Божица на љубовта и војната — убава, моќна и горда, златна и лапис-лазулна облека | story-suggested | AI-default |
| Ерешкигал / Ereshkigal | Владетелка на подземјето Иркала, сестра на Иштар — темна, строга кралица во обсидијан | story-suggested | AI-default |
| Тамуз / Tammuz | Мажот на Иштар, пастирски бог — рамнодушен, занесен во себе | story-suggested | AI-default |
| Вратар / Gatekeeper | Исплашен чувар на портата на подземјето | story-suggested | AI-default |
| Гласник / Messenger | Пратеник на луѓето — смирен, храбар молбеник | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~145.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Иштар, божицата на љубовта, одлучува да слезе во Иркала кај сестра си Ерешкигал. Го разбива отпорот на портата и влегува пред темната кралица, која ја прогласува за заточеничка.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | crane-down | crane-down | moderate | 3.5s | NAR |
| S02 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S03 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S04 | MEDIUM | high-angle | track | moderate | 3.5s | NAR |
| S05 | WIDE | low-angle | static | moderate | 2.5s | NAR |
| S06 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S07 | MEDIUM | eye-level | static | action | 2.5s | NAR |
| S08 | CLOSE | low-angle | static | gentle | 3.0s | DLG |
| S09 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S10 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S11 | MEDIUM | over-shoulder | track | moderate | 3.5s | NAR |
| S12 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S13 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S14 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S15 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |

### Act II — Заробеништво

*Без Иштар, Земјата венее — плодовите не зреат и луѓето престануваат да се љубат. Гласник на луѓето ја моли Ерешкигал, која прифаќа да ја ослободи, но само ако некој друг дојде на нејзино место.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S16 | MEDIUM | high-angle | crane-down | moderate | 3.0s | NAR |
| S17 | CLOSE | macro | push-in | gentle | 2.5s | NAR |
| S18 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S19 | MACRO | macro | push-in | gentle | 2.5s | NAR |
| S20 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S21 | WIDE | high-angle | crane-up | moderate | 3.0s | NAR |
| S22 | INSERT | macro | push-in | gentle | 2.5s | NAR |
| S23 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S24 | MEDIUM | high-angle | track | moderate | 3.5s | NAR |
| S25 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S26 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S29 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S30 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S31 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S32 | WIDE | crane-up | crane-up | moderate | 3.5s | NAR |
| S33 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S34 | MACRO | macro | pull-back | gentle | 2.5s | NAR |
| S35 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S36 | WIDE | crane-up | crane-up | moderate | 3.0s | NAR |
| S37 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S38 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |

### Act III — Разрешница

*Иштар се враќа дома и открива дека Тамуз ни не забележал дека ја немало. Разгневена, го праќа него на своето место во Иркала и повторно завладува со Земјата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S40 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S41 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S42 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S43 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S44 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S45 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S46 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S47 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S48 | WIDE | crane-up | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Многу одамна, во срцето на Земјата, лежеше Иркала — мрачно царство на мртвите.
- `S02` **NAR** — А над Земјата, горе, живееше Иштар — убавата и моќна божица на љубовта.
- `S03` **NAR** — Мислата за сестра ѝ Ерешкигал не ѝ даваше мир, и таа посака да слезе кај неа по секоја цена.
- `S04` **NAR** — И така, гордата божица го напушти небото и тргна надолу, кон подземјето.
- `S05` **NAR** — Пред неа се издигна порта на подземјето — висока до небото, студена и застрашувачка.
- `S06` **NAR** — Но Иштар не знаеше за страв.
- `S07` **NAR** — Таа застана пред портата и крена рака да тропне.
- `S08` **NAR** — И извика со глас што го стресе каменот.
- `S08` **DLG** — Иштар: „Отвори, или ќе ја скршам портава!“
- `S09` **NAR** — Од другата страна, исплашен вратар слушаше и трепереше.
- `S10` **NAR** — Тој не се осмели да спори — и ја отвори тешката порта.
- `S11` **NAR** — Вратарот ја поведе низ темни ходници, сè подлабоко во Иркала.
- `S12` **NAR** — Длабоко во царството ги чекаше престолната сала на Ерешкигал.
- `S13` **NAR** — А на престолот седеше самата Ерешкигал — темната кралица на мртвите.
- `S14` **NAR** — Ерешкигал ја погледна сестра си, а прашањето ѝ падна како ладен камен.
- `S14` **DLG** — Ерешкигал: „Ако ти си тука, тогаш кој ја шири љубовта на Земјата?“
- `S15` **NAR** — Иштар немаше одговор. А сестра ѝ ја изрече пресудата.
- `S15` **DLG** — Ерешкигал: „Сакаше да го посетиш моето царство, а сега ќе станеш моја заточеничка!“
- `S16` **NAR** — И така, гордоста на Иштар остана окована во подземјето.
- `S17` **NAR** — Нејзините златни нараквици веќе не светеа како порано.
- `S18` **NAR** — А горе, на Земјата, нешто почнуваше да се гаси.
- `S19` **NAR** — Плодовите престанаа да зреат.
- `S20` **NAR** — Мажите и жените веќе не се вљубуваа едни во други.
- `S21` **NAR** — Целиот свет молчеше во тага.
- `S22` **NAR** — Дури и најубавиот цвет свена и падна.
- `S23` **NAR** — Тогаш еден гласник на луѓето излезе напред.
- `S24` **NAR** — Тој тргна по патот надолу, кон Иркала, да моли за Иштар.
- `S25` **NAR** — И застана пред престолот на Ерешкигал, мал пред бескрајната темнина.
- `S26` **NAR** — Со мир, но со молба, гласникот зборуваше.
- `S26` **DLG** — Гласник: „Поштеди ја Иштар, господарке, зашто Земјата венее без неа.“
- `S27` **NAR** — Ерешкигал размисли — и во очите ѝ блесна студено сочувство.
- `S28` **NAR** — И темната кралица даде одговор.
- `S28` **DLG** — Ерешкигал: „Во ред, ќе ја ослободам — но само ако некој друг дојде на нејзино место.“
- `S29` **NAR** — Условот беше јасен: некој мора да го заземе нејзиното место.
- `S30` **NAR** — И тогаш, за прв пат по долго време, оковите на Иштар паднаа.
- `S31` **NAR** — Слободна, Иштар тргна по долгите скали нагоре.
- `S32` **NAR** — И конечно, одново го виде сонцето.
- `S33` **NAR** — Земјата почна повторно да живее.
- `S34` **NAR** — И плодовите одново созреваа.
- `S35` **NAR** — Мажите и жените повторно се погледнаа со љубов.
- `S36` **NAR** — Целиот свет повторно пееше од среќа.
- `S37` **NAR** — А Иштар, слободна, тргна кон својот дом.
- `S38` **NAR** — Таа се качи по скалите на палатата и влезе.
- `S39` **NAR** — Но дома ја чекаше нешто што не го очекуваше.
- `S40` **NAR** — Тамуз, нејзиниот маж, седеше занесен во себе — како да не забележал ништо.
- `S41` **NAR** — Тој воопшто не ни примети дека ја немало толку долго.
- `S42` **NAR** — А во градите на Иштар, празнината се претвори во гнев.
- `S43` **NAR** — И разгневената божица ја изрече пресудата.
- `S43` **DLG** — Иштар: „Еве кој ќе оди на моето место!“
- `S44` **NAR** — И во истиот миг, слугите на Ерешкигал се појавија од сенките.
- `S45` **NAR** — Тие го зграпчија Тамуз и го повлекоа кон портата на Иркала.
- `S46` **NAR** — И го одведоа надолу, во царството на мртвите.
- `S47` **NAR** — Иштар гледаше — а во победата имаше и сенка на тага.
- `S48` **NAR** — А Иштар, сега слободна и безбедна, повторно завладеа со Земјата.

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
