# 06 — Волшебникот Марку Браз (The Wizard Marku Braz)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Волшебникот Марку Браз** — Храбриот принц Каламан влегува во замокот на волшебникот Марку Браз за да ја ослободи принцезата на Шпанија, со нејзина помош ги совладува трите предизвици и ја крши магијата.

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
| Каламан / Calaman | Млад и храбар принц на Франција, патувачка облека, меч и израз на решеност | story-suggested | AI-default |
| Волшебникот Марку Браз / The Wizard Marku Braz | Моќен темен волшебник со долга наметка и огромен меч | story-suggested | AI-default |
| Принцезата / The Princess | Ќерка на кралот на Шпанија, убава како сонцето, вешта во магиските книги | story-suggested | AI-default |
| Стражарот / The Old Guard | Старец со бела брада, проколнат чувар на замокот | story-suggested | AI-default |
| Седумглавиот змеј / The Seven-Headed Dragon | Чудовишен змеј со седум глави и долга опашка | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~153.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Патувањето

*Каламан тргнува од дома, го наоѓа замокот во шумата, слуша предупредувањето на стражарот, влегува храбро и ја наоѓа принцезата во градината.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S04 | WIDE | low-angle | track | moderate | 3.0s | NAR |
| S05 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S06 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S07 | MEDIUM | eye-level | static | moderate | 2.5s | DLG |
| S08 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S09 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S10 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S11 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S12 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S13 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |
| S14 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |

### Act II — Трите предизвици

*Волшебникот се враќа, го заробува Каламан и му наметнува три предизвици. Со магијата и советите на принцезата, Каламан го совладува непријателот, седумглавиот змеј и на крај самиот волшебник.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | low-angle | track | moderate | 3.0s | NAR |
| S16 | MEDIUM | eye-level | push-in | action | 3.0s | NAR |
| S17 | MEDIUM | low-angle | crane-down | moderate | 3.0s | NAR |
| S18 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S19 | MEDIUM | high-angle | pan-right | moderate | 3.0s | NAR |
| S20 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S21 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S22 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S23 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S24 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S25 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S26 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S27 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S28 | CLOSE | high-angle | push-in | action | 3.0s | NAR |
| S29 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S30 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S31 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S32 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S33 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S34 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S35 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S36 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S37 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S38 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |

### Act III — Среќниот крај

*Магијата се крши: дрвјата повторно стануваат луѓе, стражарот е облечен во раскош, а Каламан и принцезата се венчаваат и живеат среќно.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S40 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S41 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S42 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S43 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S44 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S45 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S46 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S47 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S48 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Каламан, синот на кралот на Франција, сонувал да го истражи светот.
- `S02` **NAR** — Еден ден реши конечно да замине од дома.
- `S03` **NAR** — Патуваше долго, низ полиња и шуми од далечни земји.
- `S04` **NAR** — Најпосле стигна до густа, маѓепсана шума што го проголта патот.
- `S05` **NAR** — Среде шумата се издигаше огромен замок, потемнет од тајна магија.
- `S06` **NAR** — На портата стоеше стражарот со долгата бела брада.
- `S07` **DLG** — Каламан: „Би сакал да влезам, со ваша дозвола.“
- `S08` **NAR** — Старецот му одговори: местово припаѓа на еден моќен волшебник.
- `S08` **DLG** — Стражарот: „Ова место му припаѓа на моќниот волшебник!“
- `S09` **NAR** — Ги претворил неговите роднини и поданици во дрвјата во шумата.
- `S10` **NAR** — Ако допре нешто — ќе се претвори и самиот во дрво.
- `S10` **DLG** — Стражарот: „Ако допреш од раскошите внатре, и ти ќе станеш дрво!“
- `S11` **NAR** — Но Каламан беше храбар и влезе во замокот.
- `S12` **NAR** — Не ги допре ниту вкусната храна ниту сјајните камења и рубини.
- `S13` **NAR** — Во прекрасна градина ја најде принцезата, убава како сонцето.
- `S14` **NAR** — Двајцата се засакаа на прв поглед.
- `S14` **DLG** — Принцезата: „Ги читав книгите на волшебникот — сега сум помоќна од него. Заедно ќе ја тргнеме магијата!“
- `S15` **NAR** — Вечерта, Марку Браз се врати во замокот.
- `S16` **NAR** — Го виде Каламан и гнев му се разгоре.
- `S17` **NAR** — Со еден замав на магија, го зароби.
- `S18` **NAR** — Утре ќе се соочи со три предизвици — или црно му се пишува.
- `S18` **DLG** — Волшебникот: „Утре ќе се соочиш со три предизвици. Ако не ги поминеш — црно ти се пишува!“
- `S19` **NAR** — Ноќта, принцезата тајно ги читаше книгите на волшебникот.
- `S20` **NAR** — Во мугрите, започна првиот предизвик.
- `S21` **NAR** — Од сенките излезе првиот непријател, висок и оклопен.
- `S22` **NAR** — Принцезата му шепнеше совети и го штитеше со магијата.
- `S23` **NAR** — Со нејзина помош, Каламан го порази непријателот.
- `S24` **NAR** — Волшебникот тогаш му рече да се бори со седумглав змеј.
- `S24` **DLG** — Волшебникот: „Сега бори се со седумглавиот змеј!“
- `S25` **NAR** — Од чадот се појави чудовиштето со седум глави.
- `S26` **NAR** — Каламан застана цврсто пред змејот.
- `S27` **NAR** — Прво му ја пресече опашката.
- `S28` **NAR** — Потоа ја отсече главата во средината.
- `S29` **NAR** — Така полесно ги отсече и останатите глави.
- `S30` **NAR** — На крајот чудовиштето падна на земја, совладано.
- `S31` **NAR** — Тогаш волшебникот сам нападна, со огромниот меч.
- `S32` **NAR** — Благодарение на советите и волшепствата на принцезата, го избегна мечот.
- `S33` **NAR** — Каламан се сврте и се доближи.
- `S34` **NAR** — И право во срцето го прободе.
- `S35` **NAR** — Волшебникот исчезна во еден вител.
- `S36` **NAR** — Замокот замолкна, а магијата почна да бледнее.
- `S37` **NAR** — Каламан и принцезата се прегрнаа.
- `S38` **NAR** — А прозорците на замокот засветлеа за првпат по долго време.
- `S39` **NAR** — Малку по малку, дрвјата во шумата се преобразуваа.
- `S40` **NAR** — Повторно станаа убави дами и витези.
- `S41` **NAR** — Стражарот, сега во раскошна облека, зачекори напред.
- `S42` **NAR** — Им се заблагодари со најразлични подароци.
- `S42` **DLG** — Стражарот: „Ви благодарам од сè срце!“
- `S43` **NAR** — Во замокот започа голема прослава.
- `S44` **NAR** — Каламан и принцезата се венчаа.
- `S45` **NAR** — Сите ги славеа среќните младенци.
- `S46` **NAR** — Двајцата зачекорија низ градината, сега целата расцветана.
- `S47` **NAR** — Замокот и шумата блескаа, ослободени од магијата.
- `S48` **NAR** — И си живееја среќно, засекогаш.

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
