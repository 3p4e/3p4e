# 20 — Брунхилда и огнениот прстен (Brunhilda and the Ring of Fire)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Брунхилда и огнениот прстен** — Откако валкиријата Брунхилда му пркоси на Один и е маѓепсана да спие зад илјада штитови и огнен прстен, храбриот Сигурд го следи гласот на птиците, минува низ огнот и ја буди — а љубовта им дава сила посилна од секоја клетва.

*Genre:* Нордиски мит · епска авантура

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
| Брунхилда / Brunhilda | Валкирија-воинка со крилест оклоп и златно-црвена коса; по казната смртна девојка во панцирна кошула | story-suggested | AI-default |
| Сигурд / Sigurd | Млад, храбар витез со темна коса, скромен оклоп и верен црн коњ; убиец на змејот Фафнир | story-suggested | AI-default |
| Один / Odin | Стар, едноок бог со сива брада, копје Гунгнир и гаврани на рамениците | story-suggested | AI-default |
| Птиците / The Birds | Гаврани-водичи што го водат Сигурд кон волшебниот замок | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~157.0s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Валкиријата Брунхилда му пркоси на Один, кој ја претвора во смртна и ја заклучува во замок зад илјада штитови и огнен прстен, маѓепсувајќи ја во длабок сон.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S04 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S05 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S06 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S07 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S08 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S09 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S10 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S11 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S12 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |

### Act II — Сукоб

*Воден од птиците, Сигурд стигнува до замокот, минува низ штитовите и огнениот прстен, ја наоѓа заспаната Брунхилда, ја буди и ѝ подарува волшебен прстен.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S14 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S15 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S16 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S17 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S18 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S19 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S20 | WIDE | eye-level | pull-back | moderate | 3.0s | NAR |
| S21 | WIDE | low-angle | push-in | moderate | 3.5s | NAR |
| S22 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S23 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S24 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S25 | WIDE | eye-level | pan-right | moderate | 3.5s | NAR |
| S26 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S27 | MEDIUM | over-shoulder | push-in | moderate | 3.0s | NAR |
| S28 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S29 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S30 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S31 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S32 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S33 | MEDIUM | eye-level | crane-up | moderate | 3.5s | NAR |
| S34 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S35 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S36 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |

### Act III — Расплет

*Проклетството се крева, огнот гасне и штитовите се смируваат; Сигурд и Брунхилда, поврзани со љубов и вечен завет, заедно јаваат кон изгрејсонцето.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S37 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S39 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S40 | MEDIUM | eye-level | shot-reverse | moderate | 3.0s | NAR |
| S41 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S42 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S43 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S44 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S45 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S46 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S47 | MEDIUM | low-angle | crane-up | moderate | 3.5s | NAR |
| S48 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Брунхилда беше валкирија — воинка што му служеше на Один.
- `S02` **NAR** — Таа беше најхрабрата меѓу нив.
- `S03` **NAR** — Валкириите ги водеа паднатите воини во Одиновата сала.
- `S04` **NAR** — Но еднаш, Брунхилда не послуша една Одинова заповед.
- `S05` **NAR** — Один ја повика пред својот престол.
- `S05` **DLG** — Один: „Ти пркоси на мојата волја, Брунхилда.“
- `S06` **NAR** — Како казна, тој ја претвори во смртна девојка и ја заклучи во замок.
- `S07` **NAR** — Один ја изрече својата пресуда.
- `S07` **DLG** — Один: „Ќе останеш овде додека не дојде витез што ќе те ослободи!“
- `S08` **NAR** — Илјада штитови се издигнаа околу замокот.
- `S09` **NAR** — А наоколу пламна огнен прстен.
- `S10` **NAR** — Со стара магија, Один ја маѓепса да падне во длабок сон.
- `S11` **NAR** — Брунхилда ги затвори очите и заспа.
- `S12` **NAR** — А во меѓувреме, младиот Сигурд веќе јаваше кон замокот.
- `S13` **NAR** — Сигурд го следеше гласот на птиците.
- `S14` **NAR** — Тој знаеше дека птиците го водат кон судбината.
- `S15` **NAR** — На крајот пред него се појави волшебниот замок.
- `S16` **NAR** — Пред него се издигнаа илјада штитови.
- `S17` **NAR** — Тој беше толку храбар што ништо не го исплаши.
- `S18` **NAR** — Слезе од коњот и тргна напред.
- `S19` **NAR** — Штитовите се разделија пред чистото срце.
- `S20` **NAR** — Илјадата штитови му отворија пат.
- `S21` **NAR** — Остануваше уште огнениот прстен.
- `S22` **NAR** — Но Сигурд не запре.
- `S23` **NAR** — Тој чекореше низ огнот неповреден.
- `S24` **NAR** — Огнот не го допре храбриот младич.
- `S25` **NAR** — Во срцето на замокот, заспана лежеше една девојка.
- `S26` **NAR** — Беше убава како сон.
- `S27` **NAR** — Сигурд застана пред неа, без здив.
- `S28` **NAR** — Тогаш, девојката ги отвори очите.
- `S29` **NAR** — Таа му се насмевна на својот ослободител.
- `S29` **DLG** — Брунхилда: „Се викам Брунхилда.“
- `S30` **NAR** — Сигурд се вљуби во неа на прв поглед.
- `S31` **NAR** — И ѝ го даде волшебниот прстен од змејот Фафнир.
- `S32` **NAR** — Тој го стави на нејзиниот прст.
- `S33` **NAR** — Проклетството на Один се скрши.
- `S34` **NAR** — Огнениот прстен згасна, а штитовите се смирија.
- `S35` **NAR** — Сигурд ѝ даде свето ветување.
- `S35` **DLG** — Сигурд: „Го давам мојот меч: ќе те штитам и ќе те сакам засекогаш.“
- `S36` **NAR** — А Брунхилда, слободна, го прифати од срце.
- `S37` **NAR** — Двајцата излегоа од замокот кон првата светлина.
- `S38` **NAR** — Огнениот прстен сега беше само венец од жар.
- `S39` **NAR** — Штитовите лежеа како заспани воини.
- `S40` **NAR** — Верниот коњ го чекаше својот господар.
- `S41` **NAR** — Тие заедно јавнаа низ полињата.
- `S42` **NAR** — Сега беше смртна — но послободна од кога било.
- `S43` **NAR** — Птиците ги водеа по патот кон новиот ден.
- `S44` **NAR** — Брунхилда погледна кон својот витез.
- `S44` **DLG** — Брунхилда: „Ти ми го врати срцето, Сигурде.“
- `S45` **NAR** — Прстенот на Фафнир светеше како мала ѕвезда.
- `S46` **NAR** — Тие јаваа кон изгрејсонцето.
- `S47` **NAR** — Две силуети, една судбина.
- `S48` **NAR** — Од тој ден, Сигурд и Брунхилда беа неразделни — штитени од љубов посилна од секој оган.

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
