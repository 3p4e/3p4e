# 10 — Иван и огнената птица (Ivan and the Firebird)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **50 shots** (floor 40).

---

## 0. Concept

**Иван и огнената птица** — A young prince, aided by a magical gray wolf, captures a firebird, a golden-maned horse, and a princess through the wolf's shape-shifting tricks, returning home to marry his love and keep the faithful wolf at his side forever.

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
| Иван / Ivan | Млад храбар принц, син на царот Берендеј | story-suggested | AI-default |
| Цар Берендеј / Tsar Berendey | Остар возрасен владетел, татко на Иван | story-suggested | AI-default |
| Огнената птица / The Firebird | Сјајна златна птица од жив оган | story-suggested | AI-default |
| Сивиот волк / The Gray Wolf | Магичен волк што зборува и се преобразува | story-suggested | AI-default |
| Цар Афрон / Tsar Afron | Владетел што ја чува огнената птица во златен кафез | story-suggested | AI-default |
| Цар Кусман / Tsar Kusman | Владетел со коњот со златна грива | story-suggested | AI-default |
| Цар Далмат / Tsar Dalmat | Татко на Елена, владетел на далечен дворец | story-suggested | AI-default |
| Елена / Elena | Убава принцеза, ќерка на царот Далмат | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**50 shots · ~164.5s runtime · 252.0s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Златните јаболка на Берендеј ги краде мистериозна птица; Иван чува стража, ја здогледува огнената птица и успева да искубе само еден пердув, по што царот го испраќа по неа.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |
| S02 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S03 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S04 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S05 | CLOSE | eye-level | static | gentle | 2.5s | DLG |
| S06 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S07 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S08 | WIDE | eye-level | pan-left | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S10 | MACRO | macro | static | gentle | 3.0s | NAR |
| S11 | MEDIUM | eye-level | track | action | 3.5s | NAR |
| S12 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S13 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S14 | MACRO | macro | static | gentle | 3.0s | NAR |
| S15 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |

### Act II — Пресврт

*Сивиот волк го совладува коњот на Иван, но му ветува замена. Водејќи го, Иван краде огнена птица, па коњ со златна грива, и ја среќава Елена; волкот со своите преобразби ги надмудрува царевите Кусман и Афрон.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S16 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S17 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S18 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S19 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S20 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S21 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S23 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S24 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S25 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S26 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S27 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S28 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S29 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S30 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S31 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S32 | MEDIUM | over-shoulder | static | moderate | 3.5s | DLG |
| S33 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S35 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S36 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S37 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S38 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S39 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S40 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |

### Act III — Разврска

*Иван се враќа дома со сите дарови, се жени со Елена и никогаш не се разделува од верниот сив волк.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S41 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S42 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S43 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S45 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S46 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S47 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S48 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S49 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S50 | WIDE | eye-level | static | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Во далечното царство на царот Берендеј, покрај сјајниот дворец, растеше овоштарник полн со златни јаболка.
- `S02` **NAR** — Златните јаболка блескаа како оган на гранките.
- `S03` **NAR** — Но некој ги крадеше јаболката ноќе, и владетелот беше загрижен.
- `S04` **DLG** — Цар Берендеј: „Сине, чувај стража вечерва — некој ни ги краде златните јаболка.“
- `S05` **DLG** — Иван: „Ќе ја чувам стражата, татко, и ќе ја најдам крадецот.“
- `S06` **NAR** — Таа ноќ, Иван седна под дрвото со фенер и чекаше.
- `S07` **NAR** — Минуваа часови, а тишината стануваше се потешка.
- `S08` **NAR** — Одеднаш, низ ноќта блесна сјајна светлина — птица од жив оган.
- `S09` **NAR** — Огнената птица слета на гранка, сјаејќи како мало сонце.
- `S10` **NAR** — Со клунот, таа береше златни јаболка едно по едно.
- `S11` **NAR** — Иван се прикраде, посакувајќи да ја фати.
- `S12` **NAR** — Но успеа да искубе само еден пердув од нејзината опашка.
- `S13` **NAR** — Птицата распна крилја и исчезна во ноќното небо.
- `S14` **NAR** — Пердувот светеше во дланката на Иван, топол како жар.
- `S15` **DLG** — Цар Берендеј: „Оседлај го коњот и донеси ми ја таа птица!“
- `S16` **NAR** — Во мугрите, Иван се качи на својот коњ и тргна во потрага.
- `S17` **NAR** — Патуваше низ густи шуми и ширни полиња.
- `S18` **NAR** — Одеднаш, од грмушките излезе страшен сив волк.
- `S19` **NAR** — Волкот се нафрли на коњот пред да може Иван да реагира.
- `S20` **NAR** — Коњот падна, а Иван остана сам пред ѕверот.
- `S21` **NAR** — Срцето на Иван се стегна од тага.
- `S22` **DLG** — Волкот: „Ќе ти надоместам. Ќе те одведам до птицата што ја бараш.“
- `S23` **NAR** — Иван се качи на грбот на волкот, верувајќи му.
- `S24` **NAR** — Волкот трчаше брзо како ветрот низ гори и долини.
- `S25` **NAR** — Стигнаа до дворецот на царот Афрон, каде птицата беше чувана во златен кафез.
- `S26` **NAR** — Иван ги послуша советите на волкот и ја извади птицата од кафезот.
- `S27` **NAR** — Но стражарите го фатија и го одведоа пред царот.
- `S28` **DLG** — Цар Афрон: „Ќе ти ја дадам птицата во замена за коњот со златна грива на царот Кусман.“
- `S29` **NAR** — Волкот го однесе Иван кон замокот на царот Кусман.
- `S30` **NAR** — Иван го украде коњот со златна грива од шталите на Кусман.
- `S31` **NAR** — Но и овој пат стражарите го фатија.
- `S32` **DLG** — Цар Кусман: „Ќе ти го дадам коњот ако ми ја донесеш убавата Елена, ќерката на царот Далмат.“
- `S33` **NAR** — Волкот и Иван патуваа кон далечниот дворец на царот Далмат, кон високата кула на принцезата.
- `S34` **NAR** — Волкот ја најде принцезата Елена во цветната градина.
- `S35` **NAR** — Иван остана без здив пред нејзината убавина.
- `S36` **DLG** — Иван: „Не сакам да живеам без оваа девојка мила... помогни ми!“
- `S37` **DLG** — Волкот: „Ќе ја скриеме во шумата, а потоа ќе одиме пред царот.“
- `S38` **NAR** — Пред портите на замокот, волкот се претвори во ликот на убавата Елена.
- `S39` **NAR** — Кусман му го даде коњот на Иван и ѝ посака добредојде на лажната принцеза.
- `S40` **NAR** — Вечерта, кога царот се обиде да ја прегрне, таа повторно стана волк и избега од замокот.
- `S41` **NAR** — Волкот избега и им се придружи на Иван и на принцезата во шумата.
- `S42` **DLG** — Иван: „Не сакам да живеам без овој прекрасен коњ... помогни ми!“
- `S43` **NAR** — Волкот го искористи истиот трик — се претвори во коњот со златна грива.
- `S44` **NAR** — Иван му го предаде лажниот коњ на царот Афрон, а тој му ја даде птицата.
- `S45` **NAR** — Кога Афрон се доближи, лажниот коњ се стресе, го подеба царот и побегна кај Иван.
- `S46` **NAR** — Со сите дарови — Елена, коњот и огнената птица — Иван тргна кон дома.
- `S47` **NAR** — Го пречекаа пред портите на царството, сјајни и победнички.
- `S48` **NAR** — Цар Берендеј со гордост го благослови сина си и сите дарови.
- `S49` **NAR** — Иван се ожени со убавата Елена, а целото царство славеше.
- `S50` **NAR** — И никогаш не се разделија од верниот и приврзан сив волк.

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
