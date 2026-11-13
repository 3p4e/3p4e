# 01 — Дрвото што умееше да оди (The Walking Tree)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Дрвото што умееше да оди** — A child alarms his village about a giant walking tree; when the villagers cut it down, its falling fruits become the first fish of the world.

*Genre:* Легенда · природна фантазија

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
| Детето / The Child | Љубопитно полинезиско дете, босо, едноставна ткаена облека и лента на косата | story-suggested | AI-default |
| Огромното дрво / The Walking Tree | Колосален древен столб чии корења чекорат како нозе; крошна преполна со светли, блескави овошја | story-suggested | AI-default |
| Селаните / The Villagers | Полинезиски мажи и жени со ножеви и секири, исплашени но решени | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~149.5s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Празниот свет

*Свет без риби. Дете на речниот брег здогледува огромно дрво што оди на своите корења и трча да го предупреди селото.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S02 | MEDIUM | eye-level | static | action | 3.0s | NAR |
| S03 | WIDE | eye-level | pan-left | moderate | 3.0s | NAR |
| S04 | CLOSE | high-angle | push-in | gentle | 3.0s | NAR |
| S05 | MEDIUM | eye-level | static | moderate | 2.5s | NAR |
| S06 | WIDE | low-angle | track | action | 3.5s | NAR |
| S07 | INSERT | macro | static | action | 2.5s | NAR |
| S08 | MEDIUM | low-angle | push-in | action | 3.5s | NAR |
| S09 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S10 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S11 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S12 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S13 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S14 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |

### Act II — Нападот

*Селаните со ножеви и секири се нафрлаат на дрвото кое не престанува да оди, па го сечат додека огромното стебло не падне на земја.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S16 | MEDIUM | low-angle | static | action | 3.0s | NAR |
| S17 | CLOSE | macro | static | gentle | 2.5s | NAR |
| S18 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S19 | INSERT | macro | static | gentle | 2.5s | NAR |
| S20 | MEDIUM | low-angle | pan-left | moderate | 3.0s | NAR |
| S21 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S22 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S23 | INSERT | macro | static | gentle | 2.5s | NAR |
| S24 | MEDIUM | eye-level | push-in | action | 3.0s | NAR |
| S25 | WIDE | low-angle | pan-right | action | 3.5s | NAR |
| S26 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S27 | INSERT | macro | static | action | 2.5s | NAR |
| S28 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S29 | WIDE | high-angle | pan-left | moderate | 3.0s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S31 | MEDIUM | low-angle | crane-up | action | 3.0s | NAR |
| S32 | WIDE | eye-level | track | action | 3.5s | NAR |
| S33 | INSERT | macro | static | action | 2.5s | NAR |
| S34 | MEDIUM | eye-level | pull-back | moderate | 3.0s | NAR |
| S35 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S36 | CLOSE | macro | static | action | 2.5s | NAR |
| S37 | MEDIUM | low-angle | static | action | 3.0s | NAR |
| S38 | WIDE | high-angle | crane-down | action | 3.5s | NAR |
| S39 | INSERT | macro | static | action | 2.5s | NAR |
| S40 | MEDIUM | eye-level | track | action | 3.0s | NAR |

### Act III — Првите риби

*Овошјата паѓаат во водите и се претвораат во првите морски и слатководни риби, кои брзо ги населуваат сите води во светот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S41 | WIDE | eye-level | track | action | 3.0s | NAR |
| S42 | INSERT | macro | static | action | 2.5s | NAR |
| S43 | MEDIUM | eye-level | track | action | 3.0s | NAR |
| S44 | WIDE | eye-level | pan-right | action | 3.5s | NAR |
| S45 | WIDE | high-angle | track | action | 3.0s | NAR |
| S46 | INSERT | macro | static | action | 2.5s | NAR |
| S47 | MEDIUM | eye-level | track | action | 3.0s | NAR |
| S48 | WIDE | eye-level | pan-left | action | 3.0s | NAR |
| S49 | WIDE | high-angle | crane-up | action | 3.5s | NAR |
| S50 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Пред многу долго време, реките и морињата биле празни — без ниту една риба.
- `S02` **NAR** — Водата била бистра, но сосема тивка — ништо не пливало во неа.
- `S03` **NAR** — На брегот, едно дете си играло сосема само.
- `S04` **NAR** — Си играло со камчиња и песок на самиот раб на водата.
- `S05` **NAR** — Одеднаш, детето ја подигнало главата.
- `S06` **NAR** — Пред него стоело огромно дрво — и тоа дрво чекорело.
- `S07` **NAR** — Неговите корења се кревале од земјата како да биле нозе.
- `S08` **NAR** — Стеблото беше толку големо што ја засени целата должинка на брегот.
- `S09` **NAR** — Детето останало скаменето од чудење и страв.
- `S10` **NAR** — Па се свртело и се стрчало кон селото.
- `S11` **NAR** — Истрчало низ патеката, викајќи со полни гради.
- `S12` **DLG** — Детето: „Брзо, доаѓајте! Ужасна опасност ни се наближува!“
- `S13` **NAR** — Мажите и жените излегле од своите колиби.
- `S14` **NAR** — Сите грабнале ножеви и секири.
- `S15` **NAR** — Целото село се упатило кон дрвото, со оружје во раце.
- `S16` **NAR** — А дрвото, во меѓувреме, само продолжувало да оди.
- `S17` **NAR** — Тие се нафрлиле врз огромното стебло.
- `S18` **NAR** — Со ножеви и секири почнале да удираат по стеблото.
- `S19` **NAR** — Удирај ваму, удирај таму.
- `S20` **NAR** — Дрвото, сепак, безгрижно продолжило со својот чекор.
- `S21` **NAR** — „Ако дојде тука, ќе уништи сè!“, си помислиле исплашени.
- `S22` **NAR** — Па уште пожестоко го нападнале огромното стебло.
- `S23` **NAR** — Ножевите се впивале длабоко, дрвените сплитери летале на сите страни.
- `S24` **NAR** — Стеблото почнало да покажува длабоки рани.
- `S25` **NAR** — За првпат, дрвото се занишало.
- `S26` **NAR** — Лицата на селаните биле преплавени со напор.
- `S27` **NAR** — Се обидувале да го исечат на самиот корен на стеблото.
- `S28` **NAR** — Сите заедно затегнале со последна сила.
- `S29` **NAR** — Со страшен звук, стеблото почнало да пука.
- `S30` **NAR** — Детето го гледало од далечина, со раце на устата.
- `S31` **NAR** — Дрвото се навалило и паднало.
- `S32` **NAR** — Паднало на земја со силен тресок.
- `S33` **NAR** — Земјата се разнесе под удирот.
- `S34` **NAR** — Селаните отстапиле, здивнувајќи.
- `S35` **NAR** — Настанало чудно молчење додека прашината се смирувала.
- `S36` **NAR** — Едно лисје сè уште треперело.
- `S37` **NAR** — Крошната се стресела и нејзините овошја се разлабавиле.
- `S38` **NAR** — Од крошната отпаднале стотици вкусни овошја.
- `S39` **NAR** — Овошјата светкале и се тркалале по земјата.
- `S40` **NAR** — Некои се тркалале кон морето, а некои кон реката.
- `S41` **NAR** — Некои овошја завршиле во морето.
- `S42` **NAR** — Тие се претвориле во првите морски риби.
- `S43` **NAR** — Сребрена, првата риба заплива во морското синило.
- `S44` **NAR** — Наскоро, цели јата запливале низ морето.
- `S45` **NAR** — А други овошја завршиле во реките.
- `S46` **NAR** — И тие се претвориле во првите слатководни риби.
- `S47` **NAR** — Првата слатководна риба стрелнала низ реката.
- `S48` **NAR** — И реките се исполниле со живот.
- `S49` **NAR** — За многу кусо време, рибите ги населиле сите води во светот.
- `S50` **NAR** — Детето стоело на брегот, насмеано, гледајќи го новиот свет што полнеше со живот.

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
