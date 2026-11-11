# 05 — Трите волшебни клуча (The Three Magic Keys)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Трите волшебни клуча** — Млад овчар го брани кралското стадо од гладно чудовиште и со три волшебни клуча — железен, сребрен и златен — открива градина, рози и златен замок.

*Genre:* Бајка · фантастична авантура

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
| Овчарот / The Shepherd | Млад овчар со прост волнен капут, ленена кошула и стап во рака | story-suggested | AI-default |
| Чудовиштето / The Monster | Гладно темно чудовиште со блескави очи и остри канџи | story-suggested | AI-default |
| Принцезата / The Princess | Кралска ќерка во елегантна тоалета, топла насмевка | story-suggested | AI-default |
| Кралот / The King | Крал со круна и наметка, благ а строг | story-suggested | AI-default |
| Овците / The Flock | Бело стадо овци, мирно и драгоцено за кралството | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~141.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Младиот овчар го чува кралското стадо, открива пештера со три врати, го одбива чудовиштето и со железниот клуч отклучува градина со темјанушки.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S04 | CLOSE | eye-level | push-in | gentle | 3.0s | — |
| S05 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S06 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S07 | WIDE | low-angle | push-in | moderate | 3.0s | NAR |
| S08 | MEDIUM | over-shoulder | push-in | moderate | 3.5s | NAR |
| S09 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S10 | WIDE | low-angle | push-in | moderate | 3.0s | NAR |
| S11 | MEDIUM | eye-level | track | moderate | 2.5s | NAR |
| S12 | WIDE | eye-level | pan-right | moderate | 3.0s | NAR |
| S13 | MACRO | macro | static | gentle | 2.5s | — |
| S14 | CLOSE | eye-level | push-in | gentle | 2.5s | DLG |
| S15 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S16 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |

### Act II — Сребрениот клуч

*Вториот напад му носи сребрен клуч и градина со рози; подароците ги носи на принцезата и кралот, а стадото останува на број.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S17 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S18 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S19 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S20 | MEDIUM | over-shoulder | push-in | moderate | 2.5s | DLG |
| S21 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S22 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S23 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S24 | WIDE | low-angle | push-in | moderate | 3.0s | NAR |
| S25 | MEDIUM | eye-level | track | moderate | 2.5s | NAR |
| S26 | WIDE | eye-level | pan-right | moderate | 3.0s | NAR |
| S27 | MACRO | macro | static | gentle | 2.5s | — |
| S28 | CLOSE | eye-level | push-in | gentle | 2.5s | DLG |
| S29 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S30 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S31 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S32 | CLOSE | high-angle | push-in | gentle | 2.5s | NAR |
| S33 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S34 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S35 | MEDIUM | over-shoulder | push-in | moderate | 2.5s | DLG |
| S36 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S37 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |

### Act III — Златниот замок

*Овчарот го победува чудовиштето засекогаш, со златниот клуч го отвора златниот замок и се жени со принцезата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | low-angle | push-in | moderate | 3.0s | NAR |
| S40 | MEDIUM | low-angle | track | moderate | 2.5s | NAR |
| S41 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S42 | MACRO | macro | static | gentle | 2.5s | — |
| S43 | CLOSE | eye-level | push-in | gentle | 2.5s | DLG |
| S44 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S46 | WIDE | eye-level | push-in | moderate | 3.0s | DLG |
| S47 | MEDIUM | over-shoulder | push-in | moderate | 3.5s | NAR |
| S48 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — На високите кралски пасишта, млад овчар го чуваше стадото дење и ноќе.
- `S02` **NAR** — Тој не дозволуваше ниту една овца да се оддалечи.
- `S03` **NAR** — Кога паѓаше ноќта, тој палеше оган и чуваше стража.
- `S05` **NAR** — Еден ден, на самото пасиште, нешто му привлече поглед.
- `S06` **NAR** — Меѓу карпите се отвораше влез во пештера.
- `S07` **NAR** — Тој слезе и застана пред темниот отвор.
- `S08` **NAR** — Внатре светкаа три врати: железна, сребрена и златна.
- `S09` **DLG** — Овчарот: „Се прашувам што ли кријат?“
- `S10` **NAR** — Од темнината изрипа чудовиштето и го нападна.
- `S11` **NAR** — Без да се колеба, момчето го удри.
- `S12` **NAR** — Чудовиштето избега, оставајќи железен клуч зад себе.
- `S14` **DLG** — Овчарот: „Ова сигурно е клучот за железната врата.“
- `S15` **NAR** — Го стави клучот во железната брава и сврте.
- `S16` **NAR** — Железната врата се отвори кон прекрасна градина.
- `S17` **NAR** — Меѓу цветовите набра темјанушки.
- `S18` **NAR** — Од нив свитка мал букет.
- `S19` **NAR** — Вечерта, со стадото и букетот, слезе кон кралската палата.
- `S20` **DLG** — Овчарот: „За вас, принцезо.“
- `S21` **NAR** — Принцезата ја прими со топла насмевка.
- `S22` **NAR** — Сите овци беа на број — ниту една не недостасуваше.
- `S23` **NAR** — Дојде и вториот ден.
- `S24` **NAR** — Чудовиштето го нападна повторно, исто како првиот пат.
- `S25` **NAR** — Овчарот го удри исто како претходниот ден.
- `S26` **NAR** — Овојпат, зад него остана сребрен клуч.
- `S28` **DLG** — Овчарот: „Повторно клуч — овојпат сребрен.“
- `S29` **NAR** — Сребрената врата се отклучи со еден вртеж.
- `S30` **NAR** — Зад неа беше градина уште поубава од првата.
- `S31` **NAR** — Овчарот застана вчудоневен.
- `S32` **NAR** — Внимателно набра неколку рози.
- `S33` **NAR** — И свитка букет поубав од првиот.
- `S34` **NAR** — Навечер ги однесе во палатата, заедно со стадото.
- `S35` **DLG** — Овчарот: „Повторно донесов дарови, кралу.“
- `S36` **NAR** — Целата палата се дивеше на розите.
- `S37` **NAR** — И по втор пат, ниту една овца не беше изгубена.
- `S38` **NAR** — Дојде и третиот ден — последниот.
- `S39` **NAR** — Чудовиштето излезе за последен, страшен напад.
- `S40` **NAR** — Овчарот го удри со сета сила.
- `S41` **NAR** — Чудовиштето падна — побе́дено засекогаш.
- `S43` **DLG** — Овчарот: „Ова го отвора златниот свет.“
- `S44` **NAR** — Златната врата се отвори во бура од светлина.
- `S45` **NAR** — Зад неа чекаше прекрасен замок полн со богатства.
- `S46` **DLG** — Овчарот: „Ова ќе биде мојот нов дом!“
- `S47` **NAR** — Потоа се ожени со принцезата.
- `S48` **NAR** — И си живееја заедно во златниот замок.

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
