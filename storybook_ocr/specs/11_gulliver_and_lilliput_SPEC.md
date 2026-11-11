# 11 — Гуливер и Лилипут (Gulliver and Lilliput)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Гуливер и Лилипут** — A shipwrecked doctor wakes bound by a kingdom of six-inch people, wins their trust, refuses to enslave their enemies, and sails home with proof of his incredible journey.

*Genre:* Авантура · фантастична сага

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
| Гуливер | Доктор и морепловец, добродушен, чесен и храбар | story-suggested | AI-default |
| Кралот на Лилипут | Мал крал со златна круна, во почетокот прагматичен, потоа алчен | story-suggested | AI-default |
| Лилипутанците | Мали жители со црвени и сини униформи, вредни и храбри | story-suggested | AI-default |
| Кралот на Блефуску | Крал на соседниот остров, благодарен и мирољубив | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~166.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Бродот на доктор Гуливер тоне во бура, а тој се буди врзан на плажа, опколен од малечката војска на кралството Лилипут.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S03 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S04 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S05 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S06 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S07 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S08 | CLOSE | high-angle | push-in | gentle | 3.5s | NAR |
| S09 | INSERT | macro | static | gentle | 3.0s | NAR |
| S10 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S11 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S12 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S13 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |

### Act II — Преговорите и победата

*Гуливер го учи јазикот, го моли кралот за слобода и победува во војната против Блефуску, но одбива да поробува и бега кај непријателот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S14 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S15 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S16 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S17 | INSERT | macro | static | gentle | 3.0s | NAR |
| S18 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S19 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S21 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S23 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S24 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S25 | CLOSE | eye-level | static | gentle | 4.0s | DLG |
| S26 | CLOSE | low-angle | static | gentle | 4.0s | DLG |
| S27 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S29 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S30 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S31 | CLOSE | eye-level | push-in | gentle | 4.0s | DLG |
| S32 | CLOSE | eye-level | static | gentle | 4.0s | DLG |
| S33 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S34 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S35 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |

### Act III — Враќањето дома

*Со помош на благодарните Блефускујанци Гуливер поправа брод, добива подароци и запловува дома во Англија.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S36 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S37 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S38 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S39 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S40 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S41 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S42 | INSERT | macro | static | gentle | 3.0s | NAR |
| S43 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S44 | CLOSE | eye-level | static | gentle | 3.5s | DLG |
| S45 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S46 | MEDIUM | eye-level | pull-back | moderate | 3.5s | NAR |
| S47 | WIDE | eye-level | push-in | moderate | 3.5s | NAR |
| S48 | WIDE | high-angle | pull-back | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Огромен брод со едра плови среде бескрајниот океан.
- `S02` **NAR** — Докторот Лемјуел Гуливер стои на палубата и гледа кон хоризонтот.
- `S03` **NAR** — Небото ненадејно потемнува и морето станува немирно.
- `S04` **NAR** — Морнарите трчаат по палубата и се борат со јажињата.
- `S05` **NAR** — Огромен бран го превртува бродот.
- `S06` **NAR** — Гуливер се бори во водата и се губи во темнината.
- `S07` **NAR** — Разденува на непозната песочна плажа.
- `S08` **NAR** — Гуливер полека ги отвора очите.
- `S09` **NAR** — Илјадници малечки јаженца го прицврстуваат за земјата.
- `S10` **NAR** — Гуливер е врзан, а околу него стојат малечки човечиња.
- `S11` **NAR** — Беше опколен од армија многу мали војници со лакови и стрели.
- `S12` **NAR** — Кога и да се помрднеше, тие го боцкаа со своите мали мечови.
- `S13` **NAR** — Така Гуливер стигна во кралството Лилипут.
- `S14` **NAR** — Малечките луѓе зборуваа на непознат јазик.
- `S15` **NAR** — Гуливер со поглед и гест им покажа дека е гладен.
- `S16` **NAR** — Донесоа многу мали послужавници полни со храна.
- `S17` **NAR** — И многу мали буренца со вино.
- `S18` **NAR** — Најаден и уморен, Гуливер полека заспа.
- `S19` **NAR** — Следниот ден се разбуди во едно големо здание.
- `S20` **NAR** — Сѐ наоколу беше неверојатно мало: луѓе, куќи, кочии, животни.
- `S21` **NAR** — Секој ден малечки готвачи му носеа храна.
- `S22` **NAR** — А малечки кројачи му кроеја алишта.
- `S23` **NAR** — Малку по малку, Гуливер го научи нивниот јазик.
- `S24` **NAR** — Па праша дали може да се сретне со кралот.
- `S25` **NAR** — Ваше Височество, Ве молам, пуштете ме да си одам дома.
- `S25` **DLG** — Гуливер: „Ваше Височество, Ве молам, пуштете ме да си одам дома.
- `S26` **NAR** — Кралот му одговори со еден услов.
- `S26` **DLG** — Крал: „Ќе те пуштиме, ако ни помогнеш да ги поразиме Блефускујанците.
- `S27` **NAR** — Мал остров соседен, Блефуску, со кој војуваа со децении.
- `S28` **NAR** — Гуливер направи малечки трски за риболов.
- `S29` **NAR** — Со нив ги фати сите бродови на непријателската флота.
- `S30` **NAR** — Победата на Лилипут беше обезбедена.
- `S31` **NAR** — Но кралот посака уште повеќе.
- `S31` **DLG** — Крал: „Сега ќе ни помогнеш да го освоиме Блефуску и да ги поробиме неговите жители!“
- `S32` **NAR** — Гуливер одби.
- `S32` **DLG** — Гуливер: „Не. Нема да поробувам никого.
- `S33` **NAR** — Разгневените војници на кралот сакаа да го убијат.
- `S34` **NAR** — Затоа Гуливер пребега на непријателскиот остров.
- `S35` **NAR** — Таму беше пречекан со благодарност, не со војна.
- `S36` **NAR** — По некое време, во морето здогледа труп од брод.
- `S37` **NAR** — Ги замоли своите мали пријатели да му помогнат да го донесат до брегот.
- `S38` **NAR** — Заедно го извлекоа трупот и почнаа да го поправаат.
- `S39` **NAR** — Конечно можам да си заминам!“ рече Гуливер.
- `S39` **DLG** — Гуливер: „Конечно можам да си заминам!“
- `S40` **NAR** — Наскоро бродот можеше да заплови.
- `S41` **NAR** — Блефускујанците и нивниот крал му дадоа многу подароци.
- `S42` **NAR** — Вклучувајќи и неколку малечки крави.
- `S43` **NAR** — Сега моите сонародници ќе ми веруваат...“, рече Гуливер.
- `S43` **DLG** — Гуливер: „Сега моите сонародници ќе ми веруваат кога ќе им ја раскажувам оваа неверојатна приказна.“
- `S44` **NAR** — А јас никогаш нема да ве заборавам!“ им вети.
- `S44` **DLG** — Гуливер: „А јас никогаш нема да ве заборавам!“
- `S45` **NAR** — Гуливер ја крена котвата и замина дома.
- `S46` **NAR** — Малите кралства останаа зад него, на хоризонтот.
- `S47` **NAR** — Пред него се протегаше отвореното море и патот кон Англија.
- `S48` **NAR** — Така заврши неверојатното патување на доктор Гуливер.

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
