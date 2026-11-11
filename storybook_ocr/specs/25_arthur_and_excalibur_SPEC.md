# 25 — Артур и Екскалибур (Arthur and Excalibur)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Артур и Екскалибур** — Младиот штитоносец Артур го извлекува волшебниот меч Екскалибур од карпата и станува крал, враќајќи го мирот во кралството.

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
| Артур / Arthur | Млад штитоносец; срдечен, вреден и храбар момче | story-suggested | AI-default |
| Мерлин / Merlin | Стар, мудар волшебник со вештерски оган | story-suggested | AI-default |
| Кај / Kay | Млад благородник, син на господарот на имотот | story-suggested | AI-default |
| Крал Утер / King Uther | Стар крал чија смрт го покренува судирот | story-suggested | AI-default |
| Благородници / Nobles | Моќници кои се борат за тронот | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~161.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Младиот Артур расте под закрила на волшебникот Мерлин, потоа оди да живее кај благородничко семејство, каде станува вреден штитоносец и се спријателува со Кај.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S03 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S04 | INSERT | macro | static | gentle | 3.0s | NAR |
| S05 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S06 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S07 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S08 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S10 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S11 | INSERT | macro | static | gentle | 3.0s | NAR |
| S12 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S13 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |

### Act II — Судир за тронот

*Кралот Утер умира, а благородниците почнуваат судири за власта. На турнирот Кај го заборава мечот, па Артур го наоѓа Екскалибур во карпата и го извлекува.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S15 | MEDIUM | high-angle | static | moderate | 3.5s | NAR |
| S16 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S17 | MEDIUM | low-angle | static | action | 3.5s | DLG |
| S18 | WIDE | high-angle | pan-left | moderate | 3.5s | NAR |
| S19 | INSERT | macro | static | gentle | 3.0s | NAR |
| S20 | WIDE | low-angle | static | moderate | 4.0s | NAR |
| S21 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S22 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S23 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S24 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S25 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S26 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S27 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S28 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S29 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S30 | INSERT | macro | static | gentle | 3.0s | NAR |
| S31 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S32 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S33 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S34 | MEDIUM | over-shoulder | static | moderate | 3.0s | DLG |
| S35 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S36 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |

### Act III — Враќањето на мирот

*Веста се шири, а сомнежите се смируваат кога Артур повторно го извлекува мечот пред сите. Народот го прогласува за крал и мирот се враќа.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S38 | WIDE | high-angle | static | moderate | 3.5s | NAR |
| S39 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S40 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S41 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S42 | INSERT | macro | static | gentle | 3.0s | NAR |
| S43 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | pan-left | moderate | 4.0s | NAR |
| S46 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S47 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S48 | CLOSE | eye-level | push-in | gentle | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Далеку, во древна земја под сиво небо, живееше момче чие име ќе ја промени судбината на кралството.
- `S02` **NAR** — Во работилницата на волшебникот Мерлин, секој ден беше чудо.
- `S03` **NAR** — Младиот Артур остана со Мерлин неколку години.
- `S03` **DLG** — Мерлин: „Дојди, момче. Ќе те научам тајните на светот.“
- `S04` **NAR** — Во таа работилница научи неверојатни волшебнички трикови.
- `S05` **NAR** — Понекогаш грешеше поради младоста, но Мерлин секогаш беше таму да поправи сѐ.
- `S06` **NAR** — Годините минуваа, а момчето растеше во силно и умно момче.
- `S07` **NAR** — Еден ден, Мерлин му рече дека е време да оди понатаму.
- `S07` **DLG** — Мерлин: „Време ти е да живееш со благородничко семејство и да научиш како да бидеш доблестен крал.“
- `S08` **NAR** — Така, Артур тргна да живее во домот на еден благородник.
- `S09` **NAR** — Таму започна да работи како штитоносец и се спријатели со Кај.
- `S09` **DLG** — Кај: „Јас сум Кај. Ако ќе живееш овде, ќе бидеме другари!“
- `S10` **NAR** — Артур вредно ги извршуваше сите задачи: ги тимареше коњите.
- `S11` **NAR** — Го чистеше оклопот и ги остреше оружјата додека не светнеа.
- `S12` **NAR** — Сепак, тој и Кај понекогаш наоѓаа време за игра и за муабет.
- `S13` **NAR** — Но еден тажен ден, низ кралството се рашири црна вест.
- `S14` **NAR** — Кралот Утер умре, а со тоа започна немир во кралството.
- `S15` **NAR** — Стариот крал почина без наследник кој сите би го познале.
- `S16` **NAR** — Благородниците се собраа, секој сакајќи го тронот за себе.
- `S17` **NAR** — Жестоки кавги избија меѓу моќниците.
- `S17` **DLG** — Благородник: „Тронот му припаѓа мене!“
- `S18` **NAR** — Заради тронот, меѓу благородниците започнаа жестоки судири.
- `S19` **NAR** — Но постоеше древна легенда за еден волшебен меч.
- `S20` **NAR** — Величествениот Екскалибур беше забоден во карпа, чекајќи го вистинскиот крал.
- `S21` **NAR** — Многумина се обидоа да го извлечат, но безуспешно.
- `S22` **NAR** — Ниту еден од нив не беше достоен.
- `S23` **NAR** — Тогаш една група моќници организираше голем турнир.
- `S24` **NAR** — Кај реши да учествува и го поведе Артур со себе како свој штитоносец.
- `S24` **DLG** — Кај: „Артур, дојди! Денес ќе се борам за круната!“
- `S25` **NAR** — Двајцата јаваа кон турнирот, а возбудата растеше.
- `S26` **NAR** — Но кога дојде време да се бори, се случи несреќа.
- `S26` **DLG** — Кај: „Артур! Го заборавив мечот дома!“
- `S27` **NAR** — Немаше време да оди по него, па Артур веднаш почна да бара меч наоколу.
- `S28` **NAR** — Одеднаш, нешто светна меѓу дрвјата — тоа беше Екскалибур.
- `S29` **NAR** — „Сигурно некој витез го оставил!“ — си помисли Артур.
- `S30` **NAR** — Само што ја зграпчи дршката, почувствува нешто посебно.
- `S31` **NAR** — Повлече со сета своја сила, и мечот излезе од карпата.
- `S32` **NAR** — Екскалибур беше слободен, сјаејќи на сонцето.
- `S33` **NAR** — Артур истрча назад и му го подаде мечот на Кај.
- `S34` **NAR** — Витезот го праша од каде го најде.
- `S34` **DLG** — Кај: „Од каде ја доби оваа... ова? Од каде?“
- `S35` **NAR** — Артур, без двоумење, покажа кон карпата.
- `S36` **NAR** — Здив на чудење се рашири меѓу присутните.
- `S37` **NAR** — Веста дека едно момче го извлече Екскалибур се рашири како оган.
- `S38` **NAR** — Сите сакаа со свои очи да го видат момчето.
- `S39` **NAR** — Но некои, разочарано, велеа дека тој е само штитоносец.
- `S39` **DLG** — Благородник: „Ама... тој е само штитоносец!“
- `S40` **NAR** — Тогаш побараа од Артур да го повтори подвигот, тука, пред сите.
- `S40` **DLG** — Кај: „Нека покаже! Нека го извлече повторно пред нас!“
- `S41` **NAR** — Пред очите на сите, Артур застана пред карпата.
- `S42` **NAR** — Го зграпчи мечот и повлече — уште еднаш излезе лесно.
- `S43` **NAR** — Екскалибур се издигна високо, сјаен како сонце.
- `S44` **NAR** — Потоа го повтори уште еднаш, па уште еднаш, без напор.
- `S45` **NAR** — Гледајќи го тоа, сомнежите исчезнаа и сите спуштија глави.
- `S46` **NAR** — Артур беше прогласен за крал на целиот тој народ.
- `S47` **NAR** — Од тој миг, борбите за тронот запреа.
- `S48` **NAR** — Мирот конечно се врати во кралството, а младиот крал го држеше Екскалибур со чест.

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
