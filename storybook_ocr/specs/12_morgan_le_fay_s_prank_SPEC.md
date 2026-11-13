# 12 — Шегата на Моргана ле Феј (Morgan le Fay's Prank)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **46 shots** (floor 40).

---

## 0. Concept

**Шегата на Моргана ле Феј** — Моргана ле Феј ги наведува Артур и сер Аколон на опасен двобој со заменети мечеви — но вистинскиот Екскалибур ја разоткрива нејзината шега.

*Genre:* Артурска легенда · фантазија

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
| Моргана ле Феј / Morgan le Fay | Темнокоса волшебничка и вештерка, полусестра на Артур; лукава и полна со омраза | story-suggested | AI-default |
| Артур / Arthur | Млад крал од Камелот, благороден и храбар | story-suggested | AI-default |
| Сер Аколон / Sir Accolon | Верен пријател и витез на Артур | story-suggested | AI-default |
| Таинствена дама / The Mysterious Lady | Мистериозна гласничка во занданата | story-suggested | AI-default |
| Џуџето / The Dwarf | Ситно суштество, гласник од грмушките | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**46 shots · ~143.0s runtime · 231.8s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Замката

*Моргана ле Феј ја сплеткува својата омраза кон Артур. Кралот оди на лов со сер Аколон, гоштеваат и заспиваат — а Артур се буди во темна зандана каде таинствена дама му подава лажен Екскалибур.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S03 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S04 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S05 | WIDE | low-angle | pan-right | moderate | 3.5s | NAR |
| S06 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S07 | MEDIUM | high-angle | static | moderate | 3.5s | DLG |
| S08 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S09 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |
| S10 | MEDIUM | high-angle | crane-down | moderate | 3.5s | NAR |
| S11 | CLOSE | eye-level | push-in | gentle | 3.0s | DLG |
| S12 | MEDIUM | low-angle | static | moderate | 3.5s | NAR |
| S13 | CLOSE | eye-level | static | gentle | 3.5s | DLG |
| S14 | INSERT | macro | push-in | gentle | 3.0s | NAR |

### Act II — Двобојот

*Сер Аколон се буди на ливада и добива меч од џуџето — но тоа е вистинскиот Екскалибур. Артур волшебно се појавува, двајцата носат тешки шлемови и не се препознаваат. Почнува жестока борба, сè додека Артур не го забележи вистинскиот Екскалибур во рацете на соперникот и не побара да му го симне шлемот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S16 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S17 | CLOSE | low-angle | static | gentle | 3.0s | DLG |
| S18 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S19 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S21 | WIDE | low-angle | pan-left | moderate | 3.0s | NAR |
| S22 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S23 | MEDIUM | eye-level | track | action | 3.5s | NAR |
| S24 | WIDE | high-angle | pan-right | moderate | 3.0s | NAR |
| S25 | CLOSE | over-shoulder | push-in | gentle | 3.0s | NAR |
| S26 | CLOSE | eye-level | static | gentle | 2.5s | NAR |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | INSERT | macro | push-in | gentle | 2.5s | NAR |
| S29 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S30 | CLOSE | eye-level | static | gentle | 3.0s | DLG |
| S31 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S32 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S33 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S34 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S35 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S36 | CLOSE | eye-level | push-in | gentle | 2.5s | NAR |
| S37 | MEDIUM | low-angle | static | moderate | 3.0s | NAR |

### Act III — Одмаздата

*Артур извикува дека Моргана ќе плати, го боди својот коњ и се упатува дома во бура на одлучност. Моргана, во својата одаја, насетува дека планот ѝ пропаднал.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S38 | CLOSE | low-angle | push-in | gentle | 3.0s | DLG |
| S39 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S40 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S41 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S42 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S43 | WIDE | low-angle | track | moderate | 3.5s | NAR |
| S44 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S45 | CLOSE | low-angle | push-in | gentle | 3.0s | NAR |
| S46 | WIDE | high-angle | crane-up | moderate | 3.5s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Камелот се буди под раното утро, а во сенките веќе тлее омраза.
- `S02` **NAR** — Моргана ле Феј, полусестрата на кралот, ги гледа дворјаните со студен поглед.
- `S03` **NAR** — Кралот Артур и неговиот пријател сер Аколон јаваат низ портите на лов.
- `S04` **NAR** — Ловот води длабоко во шумата, меѓу високи дабови и сенки.
- `S05` **NAR** — Еден величенствен елен лета низ грмушките, а ловџиите го следат.
- `S06` **NAR** — До вечерта ловот е богат: многу уловени животни лежат крај огнот.
- `S07` **NAR** — Крај пламенот се слави: се јаде, се пие и се смее до доцна.
- `S07` **DLG** — Артур: „За ловот и за приjателството!“
- `S08` **NAR** — Смеата ја исполнува ливадата, а чашите се креваат високо.
- `S08` **DLG** — Аколон: „Нема подобар лов од овој, кралу мој.“
- `S09` **NAR** — Кога огнот се смирува, двајцата другари тонат во длабок сон под дрвјата.
- `S10` **NAR** — Артур ги отвора очите — но гората ја снемало: се буди во темна зандана.
- `S11` **NAR** — Сенките дишат, а кралот вика во празниот мрак.
- `S11` **DLG** — Артур: „Каде се наоѓам?“
- `S12` **NAR** — Од никаде, во мракот се појавува една таинствена дама.
- `S13` **NAR** — Дамата му го подава мечот со зборови што кријат замка.
- `S13` **DLG** — Дама: „Еве ти го Екскалибур, твојот меч. Моргана ти го праќа.“
- `S14` **NAR** — Прстите на кралот се затвораат околу лажниот меч — тој уште не знае.
- `S15` **NAR** — Додека Артур е во мракот, сер Аколон се буди на сончева ливада.
- `S16` **NAR** — Одеднаш, од грмушките скока едно џуџе и му подава меч.
- `S17` **NAR** — Џуџето му го соопштува предизвикот со лукави зборови.
- `S17` **DLG** — Џуџе: „Моргана ти го испраќа Екскалибур за да се бориш со витезот кој ќе дојде тука.“
- `S18` **NAR** — Аколон ја прифаќа рачката — несвесен дека држи вистински Екскалибур.
- `S19` **NAR** — Одеднаш воздухот затреперува — и самиот Артур волшебно се појавува на ливадата.
- `S20` **NAR** — И двајцата носат тешки шлемови и не се препознаваат.
- `S21` **NAR** — Мечевите летнуваат — и двајцата се втурнуваат еден кон друг.
- `S22` **NAR** — Првиот удар — и челикот раѓа искри.
- `S23` **NAR** — Борбата се разгорува: челик врз челик, удар по удар.
- `S24` **NAR** — Артур е потиснат, но не отстапува.
- `S25` **NAR** — Аколон напаѓа, а Артур го пречекува со парира.
- `S26` **NAR** — Уште една серија — и челикот повторно крвари светлина.
- `S27` **NAR** — Но тогаш Артур забележува: вистинскиот Екскалибур е во рацете на соперникот.
- `S28` **NAR** — Незаборавниот сјај на вистинскиот меч — ниедна копија не може да го лажира.
- `S29` **NAR** — Артур застанува, го спушта мечот и го крева дланката.
- `S30` **NAR** — Гласот му е мирен, но наредбата е цврста: симни го шлемот.
- `S30` **DLG** — Артур: „Симни го шлемот!“
- `S31` **NAR** — Аколон се двоуми — но нешто во гласот му е чудно познато.
- `S32` **NAR** — Полека, Аколон го извадува својот шлем — и лицето конечно се открива.
- `S33` **NAR** — Артур исто така го симнува шлемот — и двајцата пријатели се препознаваат.
- `S34` **NAR** — Мечевите се спуштаат, а пријателството победува.
- `S34` **DLG** — Аколон: „Кралу мој... речи нели нешто крие?!“
- `S35` **NAR** — Во очите на кралот се пали оган — измамата сè разјаснува.
- `S36` **NAR** — Неговата тупаница се стега — шегата ќе чини скапо.
- `S37` **NAR** — Разјаснет, кралот се свртува кон дома — со една мисла на одмазда.
- `S38` **NAR** — Од градите на кралот се исторва бесен извик.
- `S38` **DLG** — Артур: „Моргана ќе ми плати за ова!“
- `S39` **NAR** — Тој го боди својот коњ и се втурнува напред кон Камелот.
- `S40` **NAR** — Галопот бучи низ ливадите, а Аколон јава веднаш зад него.
- `S41` **NAR** — Во меѓувреме, Моргана седи во својата одаја среќна — сè уште не знае.
- `S41` **DLG** — Моргана: „Двајца пријатели... два меча... каква чиста шега.“
- `S42` **NAR** — Но насмевката ѝ се лади — магијата ѝ шепоти дека нешто тргнало наопаку.
- `S43` **NAR** — Кралот јава како виор, а бурата се собира над него.
- `S44` **NAR** — Портите на Камелот го пречекуваат — кралот се враќа со одмазда во срцето.
- `S45` **NAR** — Во очите на кралот сјае одлучноста — шегата доби свој крај.
- `S46` **NAR** — А бурата над Камелот станува нем сведок на претстојната пресметка.

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
