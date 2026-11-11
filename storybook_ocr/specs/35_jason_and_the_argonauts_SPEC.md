# 35 — Јасон и Аргонаутите (Jason and the Argonauts)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Јасон и Аргонаутите** — Младиот Јасон плови со Аргонаутите кон далечната Колхида по Златното Руно, а моќната волшебничка Медеја му помага да ги исполни три невозможни задачи и да си го врати тронот.

*Genre:* Легенда · епска авантура

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
| Јасон / Jason | Храбар, силен млад грчки јунак кој пораснал кај кентаврот Хирон. | story-suggested | AI-default |
| Алкимеда / Alcimede | Кралица и нежна мајка на Јасон, вдовица на кралот Ајсон. | story-suggested | AI-default |
| Пелеј / Pelias | Узурпатор, вујко на Јасон, лукав и потсмешлив владетел на Јолк. | story-suggested | AI-default |
| Хирон / Chiron | Мудар кентавр-учител, полу-човек полу-коњ, негов воспитувач. | story-suggested | AI-default |
| Медеја / Medea | Моќна волшебничка, ќерка на Еет, која се вљубува во Јасон. | story-suggested | AI-default |
| Еет / Aeëtes | Строг владетел на Колхида, давáч на трите задачи. | story-suggested | AI-default |
| Аргонаутите / The Argonauts | Педесет храбри момци, дружина што плови со бродот Арго. | story-suggested | AI-default |
| Змејот / The Dragon | Огромен, неспив змеј-чувар на Златното Руно. | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~165.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Алкимеда со малото Јасон бега ноќе од Јолк и го доверува на кентаврот Хирон, кој го одгледува во храбар и силен младич. Пораснат, Јасон решава да си го врати тронот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |
| S03 | INSERT | macro | static | gentle | 3.0s | NAR |
| S04 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S05 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S06 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S07 | CLOSE-UP | eye-level | push-in | gentle | 3.5s | DLG |
| S08 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S10 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S11 | CLOSE-UP | eye-level | push-in | gentle | 3.5s | NAR |
| S12 | WIDE | eye-level | track | moderate | 3.5s | NAR |

### Act II — Потрагата по Руното

*Пелеј му ја ветува круната само ако му го донесе Златното Руно од далечната Колхида. Јасон го гради бродот Арго, собира педесет Аргонаути и по мориња и чудовишта стигнува кај Еет, кој му поставува три задачи.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S14 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S15 | CLOSE-UP | low-angle | push-in | gentle | 3.5s | DLG |
| S16 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S17 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S18 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S19 | WIDE | low-angle | crane-up | action | 3.5s | NAR |
| S20 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S21 | MEDIUM | eye-level | pan-right | moderate | 3.5s | NAR |
| S22 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S23 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S24 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S25 | MEDIUM | low-angle | pan-left | moderate | 3.5s | NAR |
| S26 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S27 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S28 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S29 | CLOSE-UP | over-shoulder | push-in | gentle | 3.5s | NAR |
| S30 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S31 | CLOSE-UP | macro | push-in | gentle | 3.0s | NAR |
| S32 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S33 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S34 | MEDIUM | eye-level | pan-left | moderate | 3.5s | NAR |
| S35 | WIDE | low-angle | crane-up | action | 3.5s | NAR |
| S36 | MEDIUM | eye-level | push-in | moderate | 3.5s | DLG |

### Act III — Златното Руно

*Јасон со напивката на Медеја го заспива неспијниот змеј, го грабнува Златното Руно и со Медеја плови назад кон Јолк. Пред запрепастениот Пелеј, Јасон си го бара тронот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S38 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S39 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S40 | CLOSE-UP | macro | push-in | action | 3.0s | NAR |
| S41 | WIDE | low-angle | pan-left | moderate | 3.5s | NAR |
| S42 | CLOSE-UP | macro | push-in | gentle | 3.0s | NAR |
| S43 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S44 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S45 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S46 | MEDIUM | low-angle | shot-reverse | moderate | 3.5s | DLG |
| S47 | MEDIUM | low-angle | static | moderate | 3.5s | DLG |
| S48 | WIDE | low-angle | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во древниот град Јолк, сенка падна врз кралскиот дом.
- `S02` **NAR** — Кралицата Алкимеда го стегна своето новороденче.
- `S02` **DLG** — Алкимеда: „Ќе те спасам, чедо мое.“
- `S03` **NAR** — Смртта му го одзеде таткото таа ноќ.
- `S04` **NAR** — Под покривката на ноќта, мајката и синот избегаа од Јолк.
- `S05` **NAR** — Патуваа кон земјата на кентаврите, полу-луѓе, полу-коњи.
- `S06` **NAR** — Таму ги пречека мудриот кентавр Хирон.
- `S07` **NAR** — Алкимеда му го довери Јасон на стариот учител.
- `S07` **DLG** — Алкимеда: „Чувај го и научи го сè.“
- `S08` **NAR** — Годините течеа: Хирон го учеше да лови и да се бори.
- `S09` **NAR** — Но го подучуваше и на наука и уметност.
- `S09` **DLG** — Хирон: „Силната рака без мудар ум е само камен.“
- `S10` **NAR** — Порасна во храбар и силен младич.
- `S11` **NAR** — Во градите му се разгоре желбата да си го врати тронот.
- `S12` **NAR** — Така тргна кон Јолк, по своето наследство.
- `S13` **NAR** — Во Јолк, вујко му го пречека со срдечен лик.
- `S14` **NAR** — Додека не рече зошто дошол.
- `S14` **DLG** — Пелеј: „Седни, внуку. Што е тоа што го бараш?“
- `S15` **NAR** — Но тогаш прсна да се смее.
- `S15` **DLG** — Пелеј: „Круната ќе ти ја дадам кога ќе ми го донесеш Златното Руно!“
- `S16` **NAR** — А Јасон не трепна.
- `S16` **DLG** — Јасон: „Само кажи ми што е тоа, и ќе го најдам.“
- `S17` **NAR** — И му раскажа за легендарното руно на Златниот Овен.
- `S17` **DLG** — Пелеј: „Тоа лекува секоја рана. Но го чува змеј што никогаш не спие.“
- `S18` **NAR** — Визијата се отвори: руно на Златниот Овен, блескаво.
- `S19` **NAR** — А во далечната Колхида го чуваше неспивен змеј.
- `S20` **NAR** — Јасон не се обесхрабри — изгради голем брод и го нарече Арго.
- `S21` **NAR** — Собра педесет стројни момци — се нарекоа Аргонаути.
- `S22` **NAR** — И бродот Арго заплови по морињата.
- `S23` **NAR** — Премрежињата не доцнеа: бура и ѕидови од вода.
- `S24` **NAR** — Се бореа со диви морски чудовишта.
- `S25` **NAR** — Многу премрежиња, многу борби — и сè досега издржаа.
- `S26` **NAR** — Најпосле, по многу маки, стигнаа во Колхида.
- `S27` **NAR** — Со Колхида владееше строгиот крал Еет.
- `S28` **NAR** — Еет не даваше лесно.
- `S28` **DLG** — Еет: „Руното ќе биде твое ако исполниш три задачи.“
- `S29` **NAR** — Но ќерката на кралот, волшебничката Медеја, го погледна поинаку.
- `S30` **NAR** — Првата задача: да скроти два диви бика што блуеја оган од ноздрите.
- `S31` **NAR** — Оган и врева — но Јасон не отстапи.
- `S32` **NAR** — Ги врза за плуг и ги натера да изораат огромно поле.
- `S33` **NAR** — Како што рекол кралот, од земјата излегоа десетици воини.
- `S34` **NAR** — А Јасон ги совлада сите, до последниот.
- `S35` **NAR** — Остануваше последната задача: огромниот змеј што никогаш не спие.
- `S36` **NAR** — Но Медеја веќе знаеше како да му помогне.
- `S36` **DLG** — Медеја: „Оваа напивка ќе му донесе сон — барем за неколку минути.“
- `S37` **NAR** — Тие мигови се чинеа вечни.
- `S38` **NAR** — Јасон зачекори во змејската дувка.
- `S39` **NAR** — Го опсипа со напивката од Медеја.
- `S40` **NAR** — И чудовиштето, за првпат, заспа.
- `S41` **NAR** — Јунакот го грабна Златното Руно.
- `S42` **NAR** — Светлината од руното му го осветли лицето.
- `S43` **NAR** — И заедно со Медеја, побегнаа кон бродот.
- `S44` **NAR** — И пловија назад, кон Јолк.
- `S45` **NAR** — Стигнаа пред Пелеј — и му го покажаа неговото исполнето ветување.
- `S46` **NAR** — И тогаш Пелеј сфати.
- `S46` **DLG** — Пелеј: „Тоа е невозможно...“
- `S47` **NAR** — А Јасон, со руното во раце, си го побара тронот.
- `S47` **DLG** — Јасон: „Ги исполнив задачите. Круната е моја.“
- `S48` **NAR** — И така, Јасон си го врати наследството — со срце, дружина и една верна волшебничка до себе.

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
