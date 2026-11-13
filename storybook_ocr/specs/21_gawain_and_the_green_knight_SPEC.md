# 21 — Гавејн и Зелениот Витез (Gawain and the Green Knight)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Гавејн и Зелениот Витез** — Младиот витез Гавејн го прифаќа натприродниот предизвик на Зелениот Витез и по една година и еден ден тргнува да го исполни својот збор.

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
| Гавејн / Gawain | Млад благороден витез, внук на кралот Артур, во сребрен оклоп и темноцрвен плашт | story-suggested | AI-default |
| Зелениот Витез / Green Knight | Мистериозен џиновски витез со зелена кожа, зелена коса, зелена облека и зелен коњ | story-suggested | AI-default |
| Крал Артур / King Arthur | Мудар крал на Камелот со златна круна и темноцрвен плашт | story-suggested | AI-default |
| Господарот на замокот / Lord of the Castle | Гостопримлив моќник со крзнени облеки, дарежлив домаќин | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~162.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Предизвикот

*За време на гозбата на кралот Артур влегува Зелениот Витез и предизвикува некој да му зададе удар што ќе го врати по една година. Гавејн го прифаќа предизвикот и му ја отсекува главата, но витезот си заминува неповреден.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S02 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S04 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S05 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S06 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S07 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S08 | WIDE | high-angle | static | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S10 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S11 | WIDE | eye-level | shot-reverse | moderate | 3.5s | NAR |
| S12 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S13 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S14 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |

### Act II — Патот и дарот

*Минуваат месеци и Гавејн тргнува да го исполни зборот. По долг и студен пат, еден гостопримлив господар го прима во својот замок и му подарува волшебен зелен појас за заштита.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S17 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S18 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S19 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S20 | WIDE | eye-level | push-in | moderate | 4.0s | NAR |
| S21 | MEDIUM | low-angle | crane-up | moderate | 3.5s | NAR |
| S22 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S23 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S24 | MEDIUM | over-shoulder | static | moderate | 3.0s | NAR |
| S25 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S26 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S27 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S29 | MACRO | macro | push-in | gentle | 3.0s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S31 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S32 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S33 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S34 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S35 | WIDE | eye-level | push-in | moderate | 3.5s | NAR |
| S36 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S37 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S38 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |

### Act III — Кон Зелената црква

*Гавејн со волшебниот појас стигнува пред Зелената црква, каде што храбро чекори кон својата судбина за да го исполни ветувањето.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S40 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S41 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S42 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S43 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S44 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S45 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S46 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S47 | WIDE | low-angle | static | moderate | 4.0s | NAR |
| S48 | MEDIUM | eye-level | push-in | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Кралот Артур приреди богата гозба за сите свои витези.
- `S02` **NAR** — На почесното место седеше кралот Артур.
- `S03` **NAR** — Салата беше полна со светлина, песна и смеа.
- `S04` **NAR** — Одеднаш, големите врати силно се отворија.
- `S05` **NAR** — Влезе непознат туѓинец — целиот во зелено, јавајќи на зелен коњ.
- `S06` **NAR** — Имаше зелена кожа, зелена коса и зелена облека.
- `S07` **DLG** — Зелениот Витез: „Кој ќе се осмели да ме удри со меч, но потоа да прими удар од мене?“
- `S08` **NAR** — Тишина падна врз витезите — никој не се осмели.
- `S09` **NAR** — Но Гавејн, внукот на Артур, стана и истапи напред.
- `S10` **DLG** — Гавејн: „Јас ќе го прифатам твојот предизвик.“
- `S11` **NAR** — Зелениот Витез клекна и го подаде вратот, а Гавејн го крена мечот.
- `S12` **NAR** — Но, како ништо да не се случило, витезот си ја зеде главата.
- `S13` **DLG** — Зелениот Витез: „Ќе те чекам кај Зелената црква по една година и еден ден.“
- `S14` **NAR** — И додека заминуваше, главата му го кажа датумот на враќањето.
- `S15` **NAR** — Месеците минуваа како лисја на ветрот.
- `S16` **NAR** — Датумот на предизвикот беше сè поблиску.
- `S17` **NAR** — Гавејн реши да замине и да го исполни својот збор.
- `S18` **NAR** — Патот го водеше низ замрзнати шуми и празни полиња.
- `S19` **NAR** — Деновите беа студени, а ноќите уште постудени.
- `S20` **NAR** — На крајот од патот, од вечерната магла излезе еден замок.
- `S21` **NAR** — Портата беше топла и гостопримлива.
- `S22` **NAR** — Во дворот го пречекаа слуги и гости достојни на витез.
- `S23` **DLG** — Господарот: „Ако преноќиш тука, утре моите слуги ќе те одведат до Зелената црква.“
- `S24` **NAR** — Гавејн со благодарност ја прифати поканата.
- `S25` **NAR** — Истата вечер, замокот го почести со гозба и песна.
- `S26` **NAR** — Ноќта мина мирно, а зората дојде брзо.
- `S27` **NAR** — Следното утро, господарот го дарува со проштален подарок.
- `S28` **DLG** — Господарот: „Земи го зелениов појас. Тој е волшебен и ќе те заштити.“
- `S29` **NAR** — Појасот блескаше со чудна, жива светлина.
- `S30` **NAR** — Гавејн гледаше во дарот со чудење и надеж.
- `S31` **NAR** — Тој го преврза појасот околу половината.
- `S32` **NAR** — Слугите му го доведоа коњот, спремни да му го покажат патот.
- `S33` **DLG** — Гавејн: „Ти благодарам за гостопримството и за дарот.“
- `S34` **NAR** — И така, Гавејн ја напушти гостопримливата тврдина.
- `S35` **NAR** — Патот се стеснуваше и тонеше сè подлабоко во зеленикава шума.
- `S36` **NAR** — Едната рака му почиваше на волшебниот појас.
- `S37` **NAR** — Далеку напред, од маглата се провираше форма на стара црква.
- `S38` **NAR** — Појасот трепна со светлина, како да му шепотеше храброст.
- `S39` **NAR** — Во студената зора, Гавејн стигна пред Зелената црква.
- `S40` **NAR** — Коњот застана, а Гавејн погледна кон камените врати.
- `S41` **NAR** — Црквата беше тивка, обвиткана во зеленикава мразна магла.
- `S42` **NAR** — Гавејн зачекори напред, една рака врз мечот, другата врз појасот.
- `S43` **NAR** — Волшебниот појас светеше, ветувајќи му заштита.
- `S44` **NAR** — На чистината пред црквата застана и чекаше.
- `S45` **NAR** — Никаков звук, само ветрот низ старите камења.
- `S46` **NAR** — Но Гавејн не се поколеба — тој беше дошол да го исполни зборот.
- `S47` **NAR** — Вратите на Зелената црква се отворија сами.
- `S48` **NAR** — Со појасот крај половината, Гавејн чекори напред кон својата судбина.

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
