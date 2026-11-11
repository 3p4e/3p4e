# 22 — Волшебниот појас (The Magic Belt)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Волшебниот појас** — Sir Gawain keeps a year-old vow and faces the Green Knight's three sword blows at the Green Chapel, winning honor and a magic green belt that becomes the emblem of Camelot.

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
| Сер Гавејн / Sir Gawain | Млад витез со темна коса и сребрен оклоп, ја носи зелената волшебна појасна лента околу струкот | story-suggested | AI-default |
| Господарот на замокот / The Lord of the Castle (The Green Knight) | Наметлив, исправен витез во зелена облека и темен оклоп, мирна но силна појава, носи долг меч | story-suggested | AI-default |
| Кралот Артур / King Arthur | Достоинствен крал со златна круна и пурпурна наметка, строг но добронамерен | story-suggested | AI-default |
| Витезите од Камелот / The Knights of Camelot | Благородни витези во сјајни оклопи со шарени наметки, средновековен двор | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~137.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Патот кон предизвикот

*Сер Гавејн, една година по дадениот збор, патува низ маглив брешонски предел кон Зелената црква, со волшебниот зелен појас врзан околу струкот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S04 | INSERT | macro | static | gentle | 2.5s | NAR |
| S05 | MEDIUM | low-angle | pan-right | moderate | 3.0s | NAR |
| S06 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S07 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S08 | CLOSE | over-shoulder | static | gentle | 2.5s | NAR |
| S09 | WIDE | low-angle | crane-up | moderate | 3.0s | NAR |
| S10 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S11 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S12 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S13 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S14 | CLOSE | eye-level | static | gentle | 2.5s | NAR |

### Act II — Трите замави

*Пред Зелената црква господарот на замокот замавнува трипати со мечот; Гавејн поминува низ стравот, го добива зелениот појас како награда и му се открива смислата на предизвикот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | over-shoulder | static | moderate | 3.0s | DLG |
| S16 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S17 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S18 | MEDIUM | low-angle | static | moderate | 2.5s | NAR |
| S19 | INSERT | macro | static | gentle | 2.5s | NAR |
| S20 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S21 | CLOSE | eye-level | static | gentle | 2.0s | NAR |
| S22 | WIDE | eye-level | static | moderate | 2.5s | NAR |
| S23 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S24 | CLOSE | over-shoulder | static | gentle | 3.0s | NAR |
| S25 | MEDIUM | eye-level | static | moderate | 2.0s | NAR |
| S26 | INSERT | macro | static | gentle | 2.5s | NAR |
| S27 | WIDE | low-angle | crane-up | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S29 | CLOSE | macro | push-in | gentle | 2.5s | NAR |
| S30 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S31 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S32 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S33 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S34 | CLOSE | macro | static | gentle | 2.5s | NAR |
| S35 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S36 | WIDE | crane-up | static | moderate | 3.0s | NAR |
| S37 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S38 | WIDE | high-angle | static | moderate | 3.0s | NAR |
| S39 | CLOSE | eye-level | static | gentle | 2.5s | NAR |

### Act III — Честа на Камелот

*Гавејн се враќа во Камелот, раскажува сè вклучително и својот миг на слабост, а Артур порачува сите витези да носат зелен појас во спомен на авантурата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S40 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S41 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S42 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S43 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S44 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S45 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S46 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S47 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S48 | MEDIUM | eye-level | crane-down | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Пред една година, сер Гавејн дал збор — и сега дошол денот да го исполни.
- `S02` **NAR** — Витезот чекорел сам низ маглата, со сопствена волја кон својата судбина.
- `S03` **NAR** — Бил малку загрижен, но не покажувал страв.
- `S04` **NAR** — Околу струкот, цврсто врзан, го носел појасот кој го штитеше од секаква опасност.
- `S05` **NAR** — Година порано, истиот противник му го донел овој предизвик.
- `S06` **NAR** — Пред него, од маглата, изникна Зелената црква.
- `S07` **NAR** — Гавејн забавил чекор, но не застанал.
- `S08` **NAR** — Прстите му се стегнаа врз балчакот на мечот.
- `S09` **NAR** — Црквата била стара и немо сурова.
- `S10` **NAR** — Тој влезе на празното зеленило пред вратата.
- `S11` **NAR** — Лицето му беше решено.
- `S12` **NAR** — Од внатрешноста на Зелената црква излезе господарот на замокот.
- `S13` **NAR** — Неговата појава беше мирна, а наметлива.
- `S14` **NAR** — Двајцата се соочија во тишина.
- `S15` **NAR** — Господарот проговори со длабок глас.
- `S15` **DLG** — Господарот: "Си го одржа зборот. Сега клекни и чекај го мојот меч!"
- `S16` **NAR** — Гавејн почувствува студ.
- `S17` **NAR** — Тој клекна на студената земја.
- `S18` **NAR** — Господарот го крена мечот.
- `S19` **NAR** — Сечилото засветли.
- `S20` **NAR** — Првиот замав се спушти кон неговиот врат.
- `S21` **NAR** — Гавејн се исплаши и се помрдна.
- `S22` **NAR** — Мечот промаши.
- `S23` **NAR** — Господарот повторно го крена мечот.
- `S24` **NAR** — Вториот замав беше уште поодлучен.
- `S25` **NAR** — Гавејн се напрегна да не мрдне.
- `S26` **NAR** — Сечилото застана на само неколку сантиметри од вратот.
- `S27` **NAR** — Потоа, замавна и трет пат.
- `S28` **NAR** — Витезот беше само малку повреден.
- `S29` **NAR** — Малку крв потече, но тој остана на нозе.
- `S30` **NAR** — Гавејн скокна, готов да се бори.
- `S31` **NAR** — Но противникот не го нападна — се насмевна.
- `S32` **NAR** — Господарот ја објасни вистинската смисла на предизвикот.
- `S32` **DLG** — Господарот: "Моргана ле Феј, Артуровата полусестра, го смисли овој предизвик."
- `S33` **NAR** — Тој му соопшти дека храброста му донела награда.
- `S33` **DLG** — Господарот: "Ти се докажа дека си храбар, па затоа како награда ти го дадов овој зелен појас кој ми припаѓаше мене."
- `S34` **NAR** — Појасот премина од рака на рака.
- `S35` **NAR** — Гавејн го прими подарокот.
- `S36` **NAR** — Двајцата се поздравија како рамни.
- `S37` **NAR** — Гавејн тргна назад, кон Камелот.
- `S38` **NAR** — Пределот се отвораше пред него.
- `S39` **NAR** — Неговиот зелен појас светеше.
- `S40` **NAR** — Камелот го пречека со сјај.
- `S41` **NAR** — Пријателите достојно го пречекаа.
- `S42` **NAR** — Кралот Артур го дочека.
- `S43` **NAR** — Гавејн клекна пред својот крал.
- `S44` **NAR** — Тој му раскажа сè, дури и мигот на страв.
- `S45` **NAR** — Артур стана од престолот.
- `S46` **NAR** — Кралот го пофали.
- `S46` **DLG** — Артур: "Тој момент на слабост бил твојата сила!"
- `S47` **NAR** — Утре, сите витези ќе носат зелен појас.
- `S48` **NAR** — Во спомен на оваа авантура, зелениот појас засекогаш остана.

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
