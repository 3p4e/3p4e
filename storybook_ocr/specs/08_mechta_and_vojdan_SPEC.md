# 08 — Мечта и Војдан (Mechta and Vojdan)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **40 shots** (floor 40).

---

## 0. Concept

**Мечта и Војдан** — Принцезата Мечта, проколната да се претвори во бела кошута при допир на сончев зрак, ја разбива клетвата преку љубовта и стрелата на принцот Војдан.

*Genre:* Бајка · романтична фантазија

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
| Мечта | Млада принцеза, прекрасна и шармантна, проколната да се менува во бела кошута | story-suggested | AI-default |
| Војдан | Млад принц, искрен, вљубен во портретот на Мечта | story-suggested | AI-default |
| Кралица и kral | Родители на Мечта, љубезни но загрижени | story-suggested | AI-default |
| Добра самовила | Млада самовила, блага, гради заштитна кула и го води спасот | story-suggested | AI-default |
| Стара самовила | Навредена, моќна самовила што фрла клетва | story-suggested | AI-default |
| Добра дворска дама | Мила, верна сопатничка на Мечта | story-suggested | AI-default |
| Завидлива дворска дама | Злобна, завидлива, го имитира ликот на Мечта | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**40 shots · ~138.5s runtime · 201.6s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Раѓањето на принцезата Мечта е прославено, но навредена стара самовила фрла клетва. Млада самовила гради кула без врати и прозорци. Годините минуваат, портретот на Мечта стигнува до принцот Војдан кој се вљубовува во неа.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S12 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |
| S02 | INSERT | eye-level | push-in | gentle | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S04 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |
| S05 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S06 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |
| S07 | MEDIUM | eye-level | shot-reverse | moderate | 3.5s | DLG |
| S08 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S09 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S10 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S11 | MEDIUM | over-shoulder | static | moderate | 3.5s | NAR |
| S12 | CLOSE | low-angle | push-in | gentle | 3.5s | DLG |

### Act II — Клетвата и конакот

*Во црната кочија, завидливата дворска дама вади бодеж, а сончевиот зрак ја претвора Мечта во бела кошута што бега во шумата. Добрата самовила го открива лекот — стрелата на љубовта. Војдан на лов ја погодува кошутата и следејќи ја ја пронаоѓа девојката од портретот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S30 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S14 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S15 | CLOSE | over-shoulder | push-in | gentle | 3.5s | NAR |
| S16 | CLOSE | low-angle | push-in | gentle | 3.5s | NAR |
| S17 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S18 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S19 | WIDE | eye-level | static | moderate | 3.5s | DLG |
| S20 | CLOSE | low-angle | push-in | gentle | 3.5s | NAR |
| S21 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S23 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |
| S24 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S25 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S26 | CLOSE | over-shoulder | push-in | gentle | 3.5s | NAR |
| S27 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S28 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S29 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S30 | MEDIUM | eye-level | static | moderate | 3.5s | DLG |

### Act III — Љубовта победува

*Стрелата на Војдан ја скршува клетвата. Следува прекрасен бал, а завидливата дворска дама, засрамена, избега далеку и веќе никој не ја виде.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S40 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |
| S32 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S33 | CLOSE | eye-level | push-in | gentle | 3.5s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S35 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S36 | WIDE | low-angle | static | moderate | 3.5s | NAR |
| S37 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |
| S38 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S39 | CLOSE | eye-level | push-in | gentle | 3.5s | DLG |
| S40 | WIDE | high-angle | pull-back | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S12` **NAR** — Војдан толку многу се вљубени во неа што веднаш испрати гласници да ја побараат нејзината рака.
- `S12` **DLG** — Војдан: „Веднаш испратете гласници! Сакам да се оженам со неа.“
- `S02` **NAR** — Во лулката спие малата принцеза, а кралот и кралицата стојат покрај неа полни со среќа.
- `S03` **NAR** — За раѓањето се подготвуваше голема гозба, а гласници ги канеа самовилите.
- `S04` **NAR** — Но една од најстарите самовили не доби покана и не се појави на гозбата.
- `S05` **NAR** — Среде гозбата, вратите се отворија и старата самовила влезе со ветер и зетвнатост.
- `S06` **NAR** — Таа крена рака и ја изрече клетвата над детето.
- `S06` **DLG** — Самовила: „Кога сончев зрак ќе ја допре принцезата, ќе се претвори во животно!“
- `S07` **NAR** — Кралот и кралицата беа очајни, но една млада самовила пројде низ толпата со нежен благ зрак.
- `S07` **DLG** — Млада самовила: „Ќе изградам кула без врати и прозорци. Таму ќе биде безбедна.“
- `S08` **NAR** — Младата самовила протри со своето волшебно стапче и подигна висока кула без врати и прозорци.
- `S09` **NAR** — Годините минуваа, а Мечта израсна во прекрасна и шармантна девојка во внатрешноста на кулата.
- `S10` **NAR** — Бидејќи не можеше да излезе, нејзиниот портрет беше насликан за да им се испрати на соседните кралства.
- `S11` **NAR** — Портретот стигна до див и благороден принц во соседното кралство.
- `S12` **NAR** — Војдан толку многу се вљубени во неа што веднаш испрати гласници да ја побараат нејзината рака.
- `S12` **DLG** — Војдан: „Веднаш испратете гласници! Сакам да се оженам со неа.“
- `S30` **NAR** — Мечта му ја раскажа својата приказна, смеејќи се и плачејќи во исто време.
- `S30` **DLG** — Мечта: „Твојата стрела ја скрши клетвата!“
- `S14` **NAR** — Со неа појдоа две дворски дами — едната мила, а другата завидлива.
- `S15` **NAR** — Тогаш завидливата дворска дама го извади бодежот и го распори покривот на кочијата.
- `S16` **NAR** — Само што сончев зрак го допре лицето на Мечта, таа се преобрази во бела кошута.
- `S17` **NAR** — Белата кошута скокна од кочијата и избега во шумата, гобејќи се меѓу дрвјата.
- `S18` **NAR** — Милата дворска дама ја следеше Мечта низ шумата, викајќи по неа.
- `S19` **NAR** — А завидливата дворска дама пристигна во палатата и се претстави како принцезата.
- `S19` **DLG** — Завидлива дама: „Еве сум! Сега ќе треба да се венчаш со мене!“
- `S20` **NAR** — Но Војдан не го препозна убавото лице во кое се вљубени. Беше тажен.
- `S21` **NAR** — Војдан избега од палатата и се скри во еден конак во шумата.
- `S22` **NAR** — Во меѓувреме, добрата самовила ги најде кошутата и дворската дама кои беа прегрнати и плачеа.
- `S23` **NAR** — Добрата самовила ги смири и им го откри лекот.
- `S23` **DLG** — Добра самовила: „Мечта ќе си го враќа човечкиот облик секоја вечер, додека не ја погоди стрелата на љубовта.“
- `S24` **NAR** — Потоа им покажа еден конак во кој можеа да престојуваат — истиот конак во кој се криеше принцот.
- `S25` **NAR** — Едно утро, додека беше на лов, Војдан забележа бела кошута во шумата.
- `S26` **NAR** — Младичот ја погоди белата кошута со стрелата на љубовта.
- `S27` **NAR** — Кошутата побегна, а Војдан ја следеше до конакот.
- `S28` **NAR** — Во конакот, тој откри дека во собата веднаш до неговата имаше дворска дама.
- `S29` **NAR** — Дворската дама ѝ ја превиваше раката на една девојка — иста како портретот.
- `S30` **NAR** — Мечта му ја раскажа својата приказна, смеејќи се и плачејќи во исто време.
- `S30` **DLG** — Мечта: „Твојата стрела ја скрши клетвата!“
- `S40` **NAR** — И така, љубовта беше посилна од секоја клетва.
- `S32` **NAR** — Мечта, облечена во блескав венчален фустан, танцуваше со Војдан полна со среќа.
- `S33` **NAR** — Војдан со љубов гледаше кон неа, врел со благодарност.
- `S34` **NAR** — Добрата самовила и милата дворска дама гледаа одстрана, среќни за Мечта.
- `S35` **NAR** — Но завидливата дворска дама, засрамена, избега далеку од палатата.
- `S36` **NAR** — И веќе никој не ја виде — само ветерот и темнината останаа зад неа.
- `S37` **NAR** — Балот продолжи во ноќта, со музика и светлина над целиот град.
- `S38` **NAR** — Мечта и Војдан излегоа на балконот, гледајќи се со мир и љубов.
- `S39` **NAR** — Мечта гледаше во него и знаеше дека клетвата е засекогаш скината.
- `S39` **DLG** — Мечта: „Сега сум слободна... и те сакам.“
- `S40` **NAR** — И така, љубовта беше посилна од секоја клетва.

---

## 5. Acceptance criteria (testable)

1. Shot count = 40 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
