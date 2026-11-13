# 30 — Проколнатата кралица (The Cursed Queen)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Проколнатата кралица** — Three brothers shelter in a cursed castle where a queen lies frozen in a fountain; the brave youngest endures two nights of beasts to break the spell.

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
| Најмалиот брат / The Youngest Brother | Храбар и добар младич, најмладиот од тројцата браќа. | story-suggested | AI-default |
| Кралицата / The Queen | Прекрасна кралица заробена под мразот на фонтаната. | story-suggested | AI-default |
| Лавот / The Lion | Огромен лав со светкави очи, чувар на проклетството. | story-suggested | AI-default |
| Волкот / The Wolf | Сив волк што ноќе ги демне одаите. | story-suggested | AI-default |
| Постарите браќа / The Older Brothers | Двајцата постари браќа, преплашени и пред да побегнат. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~142.8s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Ноќно засолниште

*Тројца браќа пристигнуваат ноќе во мистериозно здание; лавот и волкот ги прогонуваат, а најмалиот спие непоколебливо.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S04 | MEDIUM | low-angle | push-in | moderate | 2.8s | NAR |
| S05 | WIDE | eye-level | static | moderate | 3.2s | NAR |
| S06 | CLOSE | eye-level | static | gentle | 2.8s | NAR |
| S07 | WIDE | high-angle | static | moderate | 3.0s | NAR |
| S08 | MEDIUM | low-angle | push-in | action | 3.0s | NAR |
| S09 | CLOSE | eye-level | pan-left | action | 2.8s | NAR |
| S10 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S11 | WIDE | eye-level | track | moderate | 3.2s | NAR |
| S12 | CLOSE | eye-level | static | gentle | 2.8s | NAR |
| S13 | WIDE | high-angle | static | moderate | 3.2s | NAR |

### Act II — Проклетството

*Младичот ја открива кралицата заробена под мраз во фонтаната и ја дознава клетвата; две ноќи по ред ги заробува лавот и волкот во визбата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | WIDE | eye-level | pull-back | moderate | 3.0s | NAR |
| S15 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | push-in | moderate | 3.2s | NAR |
| S17 | CLOSE | eye-level | push-in | gentle | 3.2s | NAR |
| S18 | CLOSE | over-shoulder | static | gentle | 3.0s | NAR |
| S19 | MEDIUM | eye-level | shot-reverse | moderate | 3.2s | DLG |
| S20 | MEDIUM | eye-level | shot-reverse | moderate | 3.2s | DLG |
| S21 | CLOSE | eye-level | push-in | gentle | 3.2s | DLG |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S23 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S24 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S25 | WIDE | high-angle | static | moderate | 3.0s | NAR |
| S26 | MEDIUM | eye-level | track | moderate | 3.2s | NAR |
| S27 | WIDE | low-angle | static | moderate | 3.2s | NAR |
| S28 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S29 | WIDE | high-angle | static | action | 3.2s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 2.8s | NAR |
| S31 | MEDIUM | eye-level | track | action | 3.0s | NAR |
| S32 | MEDIUM | low-angle | pan-right | moderate | 3.0s | NAR |
| S33 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S34 | WIDE | eye-level | static | action | 3.2s | NAR |
| S35 | WIDE | eye-level | static | action | 3.0s | NAR |
| S36 | MEDIUM | eye-level | track | action | 3.0s | NAR |
| S37 | MEDIUM | low-angle | pan-left | moderate | 3.0s | NAR |

### Act III — Ослободување

*Во зори, првите сончеви зраци го кршат мразот и кралицата конечно е ослободена.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S38 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S39 | MEDIUM | eye-level | track | moderate | 3.2s | NAR |
| S40 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S41 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S42 | WIDE | high-angle | static | moderate | 3.2s | NAR |
| S43 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S44 | MEDIUM | low-angle | pull-back | moderate | 3.5s | NAR |
| S45 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S46 | CLOSE | eye-level | static | gentle | 3.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Тројца браќа патуваа кон престолнината на соседното кралство.
- `S02` **NAR** — По некое време решија да застанат и да отпочинат.
- `S03` **NAR** — Пред нив се издигна едно старо, тивко здание.
- `S04` **NAR** — Вратата се отвори со тежок звук.
- `S05` **NAR** — Внатре најдоа една одаја и си легнаа да преспијат.
- `S06` **NAR** — Најмалиот брат заспа длабоко, без грижа.
- `S07` **NAR** — Ноќта, нешто влезе во нивната одаја.
- `S08` **NAR** — Прво се појави еден лав.
- `S09` **NAR** — Зад него се прокрадна еден волк.
- `S10` **NAR** — Двајцата постари браќа се будеа и се уплашија.
- `S11` **NAR** — Тие избегаа кон ридовите.
- `S12` **NAR** — Најмалиот не насети ништо и сѐ уште спиеше.
- `S13` **NAR** — Ѕверовите кружеа, но не го допреа.
- `S14` **NAR** — Кога се разбуди, тргна да ги бара браќата.
- `S15` **NAR** — Влезе во огромна, зафрлена градина.
- `S16` **NAR** — Во фонтаната имаше девојка заробена под мраз.
- `S17` **NAR** — Нејзиното лице беше прекрасно и мирно.
- `S18` **NAR** — Младичот се наведна над ладната површина.
- `S19` **NAR** — „Што правиш тука?“, ја праша.
- `S19` **DLG** — Најмалиот брат: „Што правиш тука?“
- `S20` **NAR** — Од мразот одговори кралицата.
- `S20` **DLG** — Кралицата: „Јас сум кралицата на овој замок и сум проколната.“
- `S21` **NAR** — Таа му рече дека две ноќи ќе ја ослободат.
- `S21` **DLG** — Кралицата: „Ако поминеш уште две ноќи тука без да избегаш, ќе ме ослободиш.“
- `S22` **NAR** — Младичот не се двоумеше.
- `S22` **DLG** — Најмалиот брат: „Во ред.“
- `S23` **NAR** — Падна ноќта.
- `S24` **NAR** — Тој се разбуди кога се стемни.
- `S25` **NAR** — Слезе по скалите кон визбата.
- `S26` **NAR** — Се спушти чекор по чекор во темнината.
- `S27` **NAR** — Долу имаше визба со железни ќелии.
- `S28` **NAR** — Се скри зад еден столб и чекаше.
- `S29` **NAR** — Првата ноќ, лавот влезе во визбата.
- `S30` **NAR** — Младичот го држеше здивот.
- `S31` **NAR** — Лавот влезе во една од ќелиите.
- `S32` **NAR** — Младичот скокна и ја затвори вратата.
- `S33` **NAR** — Го заклучи лавот.
- `S34` **NAR** — Лавот остана заробен зад решетките.
- `S35` **NAR** — Следната ноќ, волкот влезе во визбата.
- `S36` **NAR** — Волкот кружеше, па влезе во ќелија.
- `S37` **NAR** — Исто како со лавот, го заклучи и волкот.
- `S38` **NAR** — Се ближеше зората.
- `S39` **NAR** — Младичот тргна кон фонтаната.
- `S40` **NAR** — Застана пред фонтаната.
- `S41` **NAR** — Погледна во лицето на кралицата.
- `S42` **NAR** — Првите зраци ја допреа фонтаната.
- `S43` **NAR** — Мразот почна да се крши.
- `S44` **NAR** — Мразот се скрши, а кралицата се издигна.
- `S45` **NAR** — Кралицата конечно беше ослободена.
- `S46` **NAR** — Таа му се насмевна во зраците на зората.

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
