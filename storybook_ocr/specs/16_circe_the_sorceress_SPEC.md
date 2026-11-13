# 16 — Волшебничката Кирка (Circe the Sorceress)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Волшебничката Кирка** — По бесот на Посејдон, Одисеј и неговата посада паѓаат во рацете на волшебничката Кирка, чија магија ги претвора луѓето во свињи — а само една билка од Хермес може да ги спаси.

*Genre:* Старогрчки мит · епска авантура

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
| Одисеј / Odysseus | Кралот на Итака, лукав и упорен херој со истрошена морнарска облека | story-suggested | AI-default |
| Кирка / Circe | Волшебничка на островот, елегантна и моќна, со блескава наметка и светлечки стап | story-suggested | AI-default |
| Еол / Aeolus | Бог на ветровите, величествен владетел на пловечкиот остров | story-suggested | AI-default |
| Хермес / Hermes | Гласник на боговите, окрилен и сјаен, носи билка со бели цветови | story-suggested | AI-default |
| Морепловците / The Sailors | Одисеевата посада, изморени морнари во парталави туники | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~151.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Посејдоновиот гнев шири нова бура, но бродовите на Одисеј наоѓаат мир кај Еол, богот на ветровите, кој му дава запечатена мешина со сите ветрови.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | low-angle | push-in | action | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S04 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S05 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S06 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S07 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S08 | INSERT | macro | push-in | gentle | 3.0s | DLG |
| S09 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S10 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S11 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S12 | CLOSE | eye-level | pan-left | gentle | 2.5s | NAR |

### Act II — Сукоб

*Љубопитните морнари ја отвораат мешината, торнадо ги носи на отворено море и на сурова брег — островот на Кирка — каде волшебничката ги претвора во свињи, а Одисеј мора да побара спас.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S14 | INSERT | macro | push-in | gentle | 2.5s | NAR |
| S15 | WIDE | low-angle | pull-back | moderate | 3.0s | NAR |
| S16 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S17 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S18 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S19 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S20 | WIDE | eye-level | pan-right | moderate | 3.0s | NAR |
| S21 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S22 | MEDIUM | eye-level | pull-back | moderate | 3.0s | NAR |
| S23 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S24 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S25 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S26 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S27 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S28 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S29 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S30 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S31 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S32 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S33 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S34 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S35 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S36 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |

### Act III — Расплет

*Кирка ја крева клетвата и на луѓето им се враќа човечкиот облик, излекувани и побројни; Одисеј со целата посада повторно плови кон дома.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S38 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S39 | CLOSE | eye-level | pull-back | gentle | 3.0s | NAR |
| S40 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S41 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S42 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S43 | MEDIUM | low-angle | crane-up | moderate | 3.5s | NAR |
| S44 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S45 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S46 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S47 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S48 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Киклопите беа синови на Посејдон.
- `S02` **NAR** — Богот бесен поради она што му се случи на Полифем.
- `S03` **NAR** — Тој предизвика уште една бура насочена кон бродовите на Одисеј.
- `S04` **NAR** — Но овој пат бродовите најдоа прибежиште.
- `S05` **NAR** — Во земјата на Еол, богот на ветрот.
- `S06` **NAR** — Еол го дочека Одисеј со гостопримство.
- `S06` **DLG** — Еол: „Кажи ми за Троја, Одисеј.“
- `S07` **NAR** — Тој сакаше да ги слушне приказните за Тројанската војна.
- `S07` **DLG** — Одисеј: „Десет години војна... и уште ме чека дома Итака.“
- `S08` **NAR** — По некое време, Еол му подари запечатена мешина.
- `S08` **DLG** — Еол: „Земи ја мешинава. Во неа се сите ветрови.“
- `S09` **NAR** — Ветровите можеле да го спречат да стигне до Итака.
- `S10` **NAR** — Бродовите повторно испловија, со ветер во грбот.
- `S11` **NAR** — Наскоро, на хоризонтот, се појави островот на Итака.
- `S12` **NAR** — Две посади гледаа кон дома — но љубопитноста веќе се будеше.
- `S13` **NAR** — Некои морепловци ja засакаа таинствената мешина.
- `S14` **NAR** — Со едно влечење, јазолот се одврза.
- `S15` **NAR** — Од неа излезе торнадо.
- `S16` **NAR** — Тоа ги одвлечка бродовите на отворено море.
- `S17` **NAR** — Потоа, еден брег се исправи пред нив.
- `S18` **NAR** — Беа принудени да се вкотват на островот на Кирка.
- `S19` **NAR** — А таму ги чекаше уште една неволја.
- `S20` **NAR** — Од мракот излезе волшебничката Кирка.
- `S21` **NAR** — Нејзиниот глас беше сладок, но клетвата — страшна.
- `S21` **DLG** — Кирка: „Ќе ве претворам во свињи.“
- `S22` **NAR** — Со замав на стапот, светлината ги поклопи.
- `S23` **NAR** — Еден по еден, луѓето почнаа да се менуваат.
- `S24` **NAR** — Салата се исполни со свињи на местото на храбри морнари.
- `S25` **NAR** — Одисеј остана сам, надвор од дофатот на магијата.
- `S25` **DLG** — Одисеј: „Што им стори? Врати ми ги луѓето!“
- `S26` **NAR** — Но Кирка беше посилна од нивните мечеви.
- `S26` **DLG** — Кирка: „Истото те чека и тебе, кралу.“
- `S27` **NAR** — Одисеј излезе од салата со тешко срце.
- `S28` **NAR** — Тогаш, од нигде никаде, се појави еден сјаен гласник.
- `S28` **DLG** — Хермес: „Не оди сам, Одисеј.“
- `S29` **NAR** — Во раката држеше билка со светли цветови.
- `S30` **NAR** — Оваа билка, рече тој, штити од секоја магија.
- `S30` **DLG** — Хермес: „Стуткај ја во зовриена вода. Ќе те штити од нејзината клетва.“
- `S31` **NAR** — Одисеј направи напивка од билките.
- `S32` **NAR** — Со една голтка, неговото тело стана отпорно.
- `S33` **NAR** — Се врати пред волшебничката, посилен од нејзината магија.
- `S34` **NAR** — Кирка го крена стапот — но зракот се скрши.
- `S35` **NAR** — Магијата немаше моќ над него.
- `S35` **DLG** — Кирка: „Кој те штити, смртнику?“
- `S36` **NAR** — Одисеј ја натера да му вети дека ќе им го врати обликот.
- `S36` **DLG** — Одисеј: „Врати им го човечкиот лик — или ќе се соочиш со меч, а не со зборови.“
- `S37` **NAR** — Кирка крена раце, а светлината омекна.
- `S38` **NAR** — Еден по еден, свињите почнаа да се исправаат.
- `S39` **NAR** — Лицата им се вратија, посветли од порано.
- `S40` **NAR** — Луѓето на Одисеј повторно стоеја на нозе.
- `S41` **NAR** — Дури и Кирка беше кротка кога молчеше.
- `S41` **DLG** — Одисеј: „Сега врати нè дома, и ќе си одиме во мир.“
- `S42` **NAR** — Бродовите беа поправени, а ветрот — милостив.
- `S43` **NAR** — Одисеј застана на прамниот крај и погледна кон хоризонтот.
- `S44` **NAR** — Срцето му беше мирно: Итака веќе не беше далеку.
- `S45` **NAR** — Со плна посада, бродовите испловија во ноќта.
- `S46` **NAR** — Зад нив, островот на Кирка полека се топеше во магла.
- `S47` **NAR** — Пред нив се простираше морето — пат кон дома.
- `S48` **NAR** — На хоризонтот, Итака ги чекаше.

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
