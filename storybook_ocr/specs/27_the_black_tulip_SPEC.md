# 27 — Црното лале (The Black Tulip)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Црното лале** — In 17th-century Haarlem, a flower grower framed for treason escapes prison with his beloved's help and, disguised as the Black Tulip, reclaims his stolen bulbs, his freedom and his love.

*Genre:* Авантура · историска драма

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
| Корнелиј / Cornelius | Млад одгледувач на цвеќиња, смирен, вреден и добар; во облека од лен со кожна престилка | story-suggested | AI-default |
| Роза / Rosa | Неговата љубена — храбра, умна и верна; долга коса и шал преку глава | story-suggested | AI-default |
| Бокстел / Boxtel | Злобниот и завидлив сосед; светла кожа, тесно лице со љубоморни очи | story-suggested | AI-default |
| Кралските стражари / The Royal Guards | Војници во сини палта и челични шлемови со долги палки | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~146.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложбата

*Во Харлем, Корнелиј одгледува ретко црно лале вредно богатство, додека завидливиот сосед Бокстел го шпионира, краде луковиците и му потметнува лажни документи за велепредавство.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S02 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S03 | CLOSE | macro | static | gentle | 2.5s | NAR |
| S04 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S05 | INSERT | macro | static | action | 2.5s | NAR |
| S06 | WIDE | eye-level | pan-right | moderate | 3.0s | NAR |
| S07 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S08 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S09 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S10 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S11 | INSERT | macro | static | gentle | 2.5s | NAR |
| S12 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S13 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S14 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |

### Act II — Обвинението и бегството

*Корнелиј е уапсен и осуден на доживотна робија поради лажни докази. Роза му помага да избега во црна облека на црн коњ, па како „Црното Лале“ влегува кај Бокстел, ги враќа луковиците и доказите и го совладува непријателот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S16 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S17 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S18 | WIDE | high-angle | track | moderate | 3.0s | NAR |
| S19 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S20 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S21 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S23 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S24 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S25 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S26 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S27 | INSERT | macro | static | gentle | 2.5s | NAR |
| S28 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S29 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S30 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S31 | WIDE | high-angle | static | moderate | 3.0s | NAR |
| S32 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S33 | INSERT | macro | static | gentle | 2.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S35 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S36 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S37 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S39 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S40 | WIDE | low-angle | track | moderate | 3.5s | NAR |

### Act III — Слобода и цветови

*Вистината излегува на виделина, Корнелиј е ослободен, заработува богатство од своите лалиња, им помага на сиромашните, се жени за Роза и живее во куќа полна со прекрасни цвеќиња.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S41 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S42 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S43 | CLOSE | macro | static | action | 2.5s | NAR |
| S44 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S45 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S46 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S47 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S48 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во Харлем — градот на лалињата — во седумнаесеттиот век, цветаат илјадници разнобојни цвеќиња.
- `S02` **NAR** — Во тој град живее Корнелиј, млад човек чие срце е полно со цвеќиња.
- `S03` **NAR** — Неговите раце знаеја како да го одгледаат и најреткото цвеќе.
- `S04` **NAR** — Денови и ноќи работел, сè додека не создаде нешто невидено — црно лале.
- `S05` **NAR** — Црното лале, чија вредност би му донела огромно богатство.
- `S06` **NAR** — Но сè тоа време, некој го набљудуваше од соседната куќа.
- `S07` **NAR** — Неговиот сосед Бокстел — човек воден од завист.
- `S08` **NAR** — Ноќе, Бокстел ја прескокнуваше оградата и шпионираше.
- `S09` **NAR** — Дојде ноќта кога реши да ги украде ретките луковици.
- `S10` **NAR** — Тивко ја отвори вратата и влезе во куќата на Корнелиј.
- `S11` **NAR** — Ги зеде луковиците — она по што дошол.
- `S12` **NAR** — И остави нешто зад себе — лажни документи.
- `S13` **NAR** — Потоа исчезна во ноќта, цврсто држејќи ја торбата.
- `S14` **NAR** — Утрината, пред вратата на Корнелиј застанаа кралски стражари.
- `S15` **NAR** — Тешки тупаници затропаа на дрвената врата.
- `S16` **DLG** — Корнелиј: „Кој е? Што се случува?“
- `S17` **NAR** — Стражарите го фатија за рацете.
- `S18` **NAR** — „Обвинети сте за велепредавство!“ — грмеа гласовите.
- `S19` **NAR** — Поради лажните докази, судот го осуди на доживотна робија.
- `S20` **NAR** — Корнелиј ја слушна пресудата со неверување.
- `S21` **NAR** — Тешката порта на затворот се затвори зад него.
- `S22` **NAR** — Во студена ќелија, сè изгледаше изгубено.
- `S23` **NAR** — Но тој мислеше само на едно име — Роза.
- `S24` **NAR** — Роза, неговата љубена, не го остави сама.
- `S25` **NAR** — Таа им го одвлече вниманието на стражарите со една приказна.
- `S26` **NAR** — Низ решетките, таа му подаде црна облека.
- `S27` **NAR** — И прекрасен црн коњ, како што ѝ беше побарал.
- `S28` **NAR** — Облечен во црно, Корнелиј ја стави црната капа.
- `S29` **NAR** — Како „Црното Лале“, тој се упати низ ноќта.
- `S30` **NAR** — Под капата, неговите очи гореа со одлучност.
- `S31` **NAR** — Црното Лале влезе во куќата на својот непријател.
- `S32` **NAR** — Тивко како сенка, влезе внатре.
- `S33` **NAR** — Ги најде — луковиците од реткото лале.
- `S34` **NAR** — И доказите кои ќе го ослободат од сите обвиненија.
- `S35` **DLG** — Бокстел: „Ти?! Невозможно!“
- `S36` **DLG** — Корнелиј: „Ги зеде моите лалиња. Сега ќе ми ги вратиш.“
- `S37` **NAR** — Со два тешки удари, својот непријател го порази.
- `S38` **NAR** — И го остави врзан за столот.
- `S39` **NAR** — Корнелиј ги крена луковиците кон светлината.
- `S40` **NAR** — Со доказите и лалињата, Црното Лале излезе во ноќта.
- `S41` **NAR** — Вистината излезе на виделина.
- `S42` **NAR** — Благодарение на своите скапоцени лалиња, заработи многу пари.
- `S43` **NAR** — Златото и лалињата се насобраа во изобилство.
- `S44` **NAR** — Па, дел од тоа богатство им го подари на сиромашните.
- `S45` **NAR** — И се ожени за својата сакана Роза.
- `S46` **NAR** — Нивните лица зрачеа од среќа.
- `S47` **NAR** — И живееја во куќа полна со прекрасни цвеќиња.
- `S48` **NAR** — А црното лале — симболот на нивната победа — цветаше вечно.

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
