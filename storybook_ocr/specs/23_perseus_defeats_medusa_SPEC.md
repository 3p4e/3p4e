# 23 — Персеј ја победува Медуза (Perseus Defeats Medusa)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Персеј ја победува Медуза** — Младиот Персеј, со помош на Атена и Хермес, го победува чудовиштето Медуза гледајќи го само нејзиниот одраз, а потоа го освојува небото на Пегаз и ја спасува Андромеда.

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
| Персеј / Perseus | Храбар и снаодлив млад јунак со решителен поглед; носи бронзен оклоп и сандали, кратка кадрава коса. | story-suggested | AI-default |
| Медуза / Medusa | Застрашувачко чудовиште со тело на жена, змии место коса, крилест грб и скаменувачки поглед. | story-suggested | AI-default |
| Атена / Athena | Божица на мудроста — висока, мирна, со сребрено-бронзен шлем и копје. | story-suggested | AI-default |
| Хермес / Hermes | Гласник на боговите — млад, брз, со крилести сандали и златен летечки шлем. | story-suggested | AI-default |
| Пегаз / Pegasus | Снежно-бел крилест коњ, мирен и благороден, со огромни бели крила. | story-suggested | AI-default |
| Андромеда / Andromeda | Убава и достоинствена девојка, окована за карпа, со долга темна коса и бела туника. | story-suggested | AI-default |
| Кралот / The King | Постар, строг владетел на островот, во пурпурна наметка. | story-suggested | AI-default |
| Горгоните / The Gorgons | Две ужасни сестри на Медуза, со змиска коса и остри канџи. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~162.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба и божествена дарба

*Персеј му ветува на кралот дека ќе ја донесе главата на Медуза; Атена и Хермес му даваат сребрен штит-огледало и остар меч, и го советуваат да не ја гледа директно.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S03 | CLOSE-UP | low-angle | static | gentle | 3.0s | NAR |
| S04 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S05 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S06 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S07 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S08 | CLOSE-UP | eye-level | static | gentle | 3.0s | DLG |
| S09 | MEDIUM | eye-level | two-shot | moderate | 3.5s | DLG |
| S10 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S11 | WIDE | eye-level | track | moderate | 4.0s | NAR |
| S12 | MEDIUM | low-angle | push-in | moderate | 3.5s | NAR |
| S13 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S14 | MEDIUM | eye-level | pan-right | moderate | 3.5s | NAR |

### Act II — Пештерата и падот на Медуза

*Персеј стигнува до пештерата полна со скаменети воини, влегува наназад гледајќи во штитот, ја победува Медуза, ја зема главата и бега на Пегаз пред Горгоните.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S16 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S17 | WIDE | behind | track | moderate | 4.0s | NAR |
| S18 | CLOSE-UP | macro | static | gentle | 3.0s | NAR |
| S19 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S20 | MEDIUM | low-angle | push-in | action | 3.5s | NAR |
| S21 | MEDIUM | eye-level | swish-pan | moderate | 3.0s | NAR |
| S22 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S23 | WIDE | eye-level | static | action | 3.0s | NAR |
| S24 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S25 | MEDIUM | eye-level | pan-right | moderate | 3.5s | NAR |
| S26 | WIDE | low-angle | crane-up | moderate | 3.0s | NAR |
| S27 | WIDE | eye-level | crane-down | moderate | 4.0s | NAR |
| S28 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S29 | WIDE | low-angle | crane-up | moderate | 4.0s | NAR |
| S30 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S31 | MEDIUM | eye-level | track | moderate | 4.0s | NAR |
| S32 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S33 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S34 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S35 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S36 | CLOSE-UP | eye-level | static | gentle | 3.0s | NAR |
| S37 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S38 | CLOSE-UP | eye-level | static | gentle | 3.0s | DLG |

### Act III — Спасението на Андромеда

*Летајќи над морето, Персеј ја наоѓа Андромеда окована за карпа, ја спасува и ја носи дома, а таа ја раскажува својата приказна за морската змија и жртвата.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S39 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S40 | MEDIUM | eye-level | two-shot | moderate | 3.5s | DLG |
| S41 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | DLG |
| S42 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |
| S43 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S44 | CLOSE-UP | eye-level | static | gentle | 3.0s | DLG |
| S45 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S46 | CLOSE-UP | eye-level | push-in | gentle | 3.0s | NAR |
| S47 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S48 | WIDE | eye-level | pull-back | moderate | 4.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Кралот владеел со еден остров сред синото море.
- `S02` **DLG** — Персеј: „Ќе ти ја донесам главата на Медуза.“
- `S03` **NAR** — Зборот беше даден — а пред него стоеше само стравот од Медуза.
- `S04` **NAR** — Медуза беше страшно чудовиште — жена одоздола, змии место коса.
- `S05` **NAR** — Еден поглед во тие очи — и човек станува камен.
- `S06` **NAR** — За среќа, со него беа Атена и брзоногиот Хермес.
- `S07` **NAR** — Хермес му даде остар меч, а Атена — сребрен штит сјаен како огледало.
- `S08` **DLG** — Хермес: „Земи го ова — ќе ти треба повеќе одошто мислиш.“
- `S09` **DLG** — Атена: „Кога ќе бидеш близу Медуза, не гледај во неа! Гледај го само нејзиниот одраз во штитот.“
- `S10` **NAR** — Не гледај во неа — само во одразот. Тој совет му остана врежан.
- `S11` **NAR** — Јунакот замина на долг пат, кон мрачните карпи каде се криеше чудовиштето.
- `S12` **NAR** — Од време на време проверуваше дали среброто сè уште свети како огледало.
- `S13` **NAR** — Најпосле, пред него се отвори пештерата — а пред влезот стоеја неколку статуа.
- `S14` **NAR** — Скаменети воини — замрзнати во последниот миг на ужас.
- `S15` **NAR** — Зар и тој ќе стане статуа? Прашањето тежеше во воздухот.
- `S16` **NAR** — Се охрабри и влезе.
- `S17` **NAR** — Чекореше наназад, а штитот му беше очи.
- `S18` **NAR** — Во сјајот на среброто можеше да ја види... неа.
- `S19` **NAR** — Медуза стана од својот камен кревет.
- `S20` **NAR** — Таа се вдаде кон него за да го убие.
- `S21` **NAR** — Но Персеј брзо се сврти — со затворени очи.
- `S22` **NAR** — Гледаше само наназад — и удри со мечот.
- `S23` **NAR** — Со еден удар — Медуза беше победена.
- `S24` **NAR** — Главата на Медуза потона во тишина.
- `S25` **NAR** — Внимателно ја стави во вреќа — и ја врза цврсто.
- `S26` **NAR** — Истрча од пештерата кон светлината.
- `S27` **NAR** — Надвор го чекаше Пегаз — крилестиот коњ на боговите.
- `S28` **NAR** — Коњот мирно го пречека како стар пријател.
- `S29` **NAR** — Го јавна Пегаз и се кренаа во небото.
- `S30` **NAR** — Две ужасни сестри излетаа од пештерата — но предоцна.
- `S31` **NAR** — Победнички полетаа над синото море.
- `S32` **NAR** — Додека леташе над морето, здогледа девојка окована за карпа.
- `S33` **NAR** — Таа стоеше сама меѓу брановите и чекаше.
- `S34` **NAR** — Солзи и надеж се сретнаа во нејзиниот поглед.
- `S35` **NAR** — Без размислување, тој слезе да ја спаси.
- `S36` **NAR** — Ги одврза — и ја качи на Пегаз.
- `S37` **NAR** — Заедно се кренаа над брановите — слободни.
- `S38` **DLG** — Андромеда: „Ти благодарам многу.“
- `S39` **NAR** — Летаа кон нејзиниот дом, а таа раскажуваше.
- `S40` **DLG** — Андромеда: „Јас сум Андромеда, ќерка на кралицата Касиопеја.“
- `S41` **DLG** — Андромеда: „Мајка ми ги навреди Нереидите, морските нимфи.“
- `S42` **NAR** — Поради тоа Посејдон испрати ужасна морска змија да ги измачува.
- `S43` **NAR** — Единствениот спас — жртва... девојката сама на карпата.
- `S44` **DLG** — Андромеда: „Единствениот начин да нè ослободи е да понудиме жртва...“
- `S45` **NAR** — Персеј сфати од каква судбина ја одбрани.
- `S46` **NAR** — Меѓу нив се роди тивок ветерок на доверба.
- `S47` **NAR** — Ја врати дома — кај нејзините родители.
- `S48` **NAR** — И така приказната заврши — со победа, спасение и нова надеж.

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
| 1 | DD HEADWEAR: no cap/hood/bandana/mask on head; hood = back-cowl only; bare head + teal-blue glowing hair always visible; any head/face covering = REJECT |
| 2 | LEGENDARY WEAPONS MUST APPEAR: DD = twin Frostbite-class hand crossbows; AZ = Dawnbreaker-class greatsword; hero sheet/keyframe without weapon = INCOMPLETE |
| 3 | WEAPON ANTI-SLOP: fantasy construction only; crossbow must NEVER read as firearm; anti-slop negatives always appended |
| 4 | BOSS FACE: Mal'garot HAS a prolific molten-lava face; faceless boss sheets SUPERSEDED |
| 5 | LOCATION BRIGHTNESS FLOOR: environment plates silhouette-readable at thumbnail; no murk-dark grades |

**Anti-slop negatives (always appended):** `firearm, gun, machinegun, Uzi, barrel, magazine, ammo clip, muzzle, modern weapon`

> Activates when face_lock changes from AI-default to an enrolled identity (DD/AZ).

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
