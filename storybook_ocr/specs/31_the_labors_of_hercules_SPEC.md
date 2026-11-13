# 31 — Подвизите на Херкул (The Labors of Hercules)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **52 shots** (floor 40).

---

## 0. Concept

**Подвизите на Херкул** — Од лулка до легенда, Херкул со сила, ум и чест ги исполнува дванаесетте подвизи на древниот свет.

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
| Херкул / Hercules | Полубог со чудесна сила и лавовска кожа | story-suggested | AI-default |
| Зевс / Zeus | Врховниот бог, татко на Херкул | story-suggested | AI-default |
| Алкимена / Alcmene | Мајката на Херкул, кралица | story-suggested | AI-default |
| Хера / Hera | Божица полна со љубомора спрема Херкул | story-suggested | AI-default |
| Евристеј / Eurystheus | Плашлив крал кој му задава невозможни задачи | story-suggested | AI-default |
| Атена / Athena | Божица на мудроста, помага на Херкул | story-suggested | AI-default |
| Хиполита / Hippolyta | Кралицата на Амазонките | story-suggested | AI-default |
| Немејски лав / Nemean Lion | Огромен лав со непробоjна кожа | story-suggested | AI-default |
| Лернејска хидра / Lernean Hydra | Деветглава змија од мочуриштето | story-suggested | AI-default |
| Кербер / Cerberus | Триглавото куче чувар на Подземјето | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**52 shots · ~162.5s runtime · 262.1s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Заложба

*Од чудесното раѓање и гневот на Хера, малиот Херкул ја покажува својата сила; како млад му се заколнува на кралот Евристеј и го совладува првиот подвиг — Немејскиот лав.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S03 | CLOSE | low-angle | static | gentle | 2.5s | NAR |
| S04 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S05 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S06 | WIDE | eye-level | pull-back | moderate | 3.5s | NAR |
| S07 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S08 | MEDIUM | low-angle | push-in | moderate | 3.0s | DLG |
| S09 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.5s | DLG |
| S10 | WIDE | high-angle | crane-up | moderate | 3.0s | NAR |
| S11 | MEDIUM | eye-level | push-in | moderate | 3.0s | NAR |
| S12 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S13 | CLOSE | low-angle | static | gentle | 3.0s | NAR |
| S14 | WIDE | eye-level | crane-down | moderate | 3.5s | NAR |

### Act II — Подвизите

*Низ мочуришта, планини, штали и езера, Херкул ја совладува Хидрата, срната со златни рогови, еримантскиот вепар, шталите на Авгиј, стимфалските птици, критскиот бик и појасот на Амазонките.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S15 | MEDIUM | eye-level | pan-right | moderate | 3.0s | NAR |
| S16 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S17 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S18 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S19 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S20 | MACRO | macro | static | gentle | 3.0s | NAR |
| S21 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S22 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S23 | MEDIUM | eye-level | push-in | moderate | 3.0s | DLG |
| S24 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S25 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S26 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S27 | WIDE | high-angle | crane-up | moderate | 3.0s | NAR |
| S28 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S29 | MEDIUM | low-angle | push-in | moderate | 3.5s | DLG |
| S30 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S31 | WIDE | eye-level | pull-back | moderate | 3.0s | NAR |
| S32 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S33 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S34 | WIDE | high-angle | crane-up | moderate | 3.0s | NAR |
| S35 | MEDIUM | low-angle | track | moderate | 3.0s | NAR |
| S36 | WIDE | eye-level | static | moderate | 3.0s | DLG |
| S37 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S38 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S39 | MEDIUM | over-shoulder | shot-reverse | moderate | 3.0s | DLG |
| S40 | WIDE | high-angle | crane-down | moderate | 3.0s | NAR |
| S41 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S42 | MEDIUM | eye-level | track | moderate | 3.0s | NAR |
| S43 | WIDE | eye-level | crane-up | moderate | 3.5s | NAR |

### Act III — Легенда

*Последните подвизи — добитокот на Герион, златните јаболка и скротувањето на Кербер — го издигаат Херкул меѓу ѕвездите, каде името му останува засекогаш.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S44 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | track | moderate | 3.0s | NAR |
| S46 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S47 | MEDIUM | eye-level | pan-left | moderate | 3.0s | NAR |
| S48 | WIDE | low-angle | static | moderate | 3.0s | NAR |
| S49 | CLOSE | eye-level | track | gentle | 3.5s | NAR |
| S50 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S51 | WIDE | eye-level | push-in | moderate | 3.0s | NAR |
| S52 | WIDE | low-angle | crane-up | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Пред боговите и пред луѓето, судбината плетеше нишка за едно дете.
- `S02` **NAR** — Зевс, врховниот бог на Олимп, го држеше својот син во раце.
- `S02` **DLG** — Зевс: „Ќе станеш најлегендарниот јунак кој светот некогаш го видел.“
- `S03` **NAR** — Но не се радуваше целиот Олимп.
- `S04` **NAR** — Во ноќта, Хера испрати двајца неканети гости во лулката на детето.
- `S05` **NAR** — Но малото дете имаше чудесна сила.
- `S06` **NAR** — Така започна приказната за херојот чие име ќе го спомнуваат со векови.
- `S07` **NAR** — Годините летаа, и момчето израсна во моќен млад човек.
- `S08` **NAR** — Неговата судбина го водеше кон служба кај кралот Евристеј.
- `S08` **DLG** — Херкул: „Ќе му служам на кралот, колку и да е тешка задачата.“
- `S09` **NAR** — Евристеј веднаш смисли задача што никој не ја минал.
- `S09` **DLG** — Евристеј: „Донеси ми ја кожата на Немејскиот лав како доказ!“
- `S10` **NAR** — Патот кон Немеја водеше низ диви карпести предели.
- `S11` **NAR** — Пред пештерата го чекаше ѕвер чија кожа не можеше да ја пробие ни стрела.
- `S12` **NAR** — Херкул го пречека со голи раце.
- `S13` **NAR** — Кога стрелите не можеа да го пробијат, само силата остана.
- `S14` **NAR** — Кожата на лавот стана негов знак и заштита.
- `S15` **NAR** — Втората задача водеше кон мочуриштето Лернеј, каде живееше деветглав чудовиште.
- `S16` **NAR** — Хидрата имаше девет глави и остри заби.
- `S17` **NAR** — Секоја отсечена глава раѓаше две нови.
- `S18` **NAR** — Затоа Херкул ја искористи својата остроумност.
- `S19` **NAR** — Со оган го запре повторното растење и го совлада чудовиштето.
- `S20` **NAR** — Од крвта на Хидрата, неговите стрели станаа смртоносно оружје.
- `S21` **NAR** — Третата задача беше крадлив лов: срна со златни рогови.
- `S22` **NAR** — Не со сила, туку со трпение.
- `S23` **NAR** — Трпеливоста му ја донесе победата.
- `S23` **DLG** — Херкул: „Мирен си сега, кралу недостапен.“
- `S24` **NAR** — Потоа дојде огромен вепар на планината Еримантос.
- `S25` **NAR** — Народот се плашеше, но Херкул не.
- `S26` **NAR** — Кога вепарот беше скротен, враќањето во палатата беше триумфално.
- `S27` **NAR** — Тогаш Евристеј смисли нешто навидум невозможно.
- `S28` **NAR** — Шталите кралот Авгиј ги немаше чистено со години.
- `S28` **DLG** — Евристеј: „Само бог може да ги исчисти!“
- `S29` **NAR** — Но Херкул знаеше дека и јунак може да направи чуда.
- `S29` **DLG** — Херкул: „И јунак може да го направи тоа!“
- `S30` **NAR** — Ги пренасочи реките и водата ја заврши работата.
- `S31` **NAR** — Шталите блеснаа чисти, а Авгиј остана без зборови.
- `S32` **NAR** — Петтата задача водеше до езерото Стимфалија, полно со ужасни птици.
- `S33` **NAR** — Тука, божицата Атена му подари мудрост.
- `S33` **DLG** — Атена: „Земи ја оваа тропалка и треси ја — таа ќе ги исплаши!“
- `S34` **NAR** — Звукот ги исплаши птиците, а стрелите ја завршија работата.
- `S35` **NAR** — Една по една, птиците паѓаа, а езерото стана мирно.
- `S36` **NAR** — Ниту мудриот совет на Атена не помина незабележан.
- `S36` **DLG** — Евристеј: „Атена те извлече од тешка ситуација.“
- `S37` **NAR** — Потоа, на Крит, го чекаше див бик.
- `S38` **NAR** — Со голи раце го скроти дивиот бик.
- `S39` **NAR** — Од крајот на земјата, од Амазонките, Евристеј побара нешто уште поопасно.
- `S39` **DLG** — Евристеј: „Донеси ми го појасот на нивната кралица!“
- `S40` **NAR** — Амазонките беа воини и јавачки без рамни.
- `S41` **NAR** — Херкуловата храброст ја сретна нивната сила.
- `S41` **DLG** — Хиполита: „Силен си, но појасот се заработува со чест.“
- `S42` **NAR** — Со чест, а не со лукавство, ја доби задачата.
- `S43` **NAR** — Задачите се нижеа, а неговото име растеше.
- `S44` **NAR** — Остануваа уште најтешките подвизи — добитокот на Герион.
- `S45` **NAR** — Со оган и со трпение, ги водеше црвените стада дома.
- `S46` **NAR** — Потоа — златните јаболка на западниот раб на светот.
- `S47` **NAR** — На крајот го чекаше портата на Подземјето.
- `S48` **NAR** — Таму, триглавиот Кербер го чуваше прагот.
- `S49` **NAR** — Со раце, а не со меч, го скроти и последниот чувар.
- `S50` **NAR** — Дванаесетте подвизи беа исполнети.
- `S51` **NAR** — Светот го спомнуваше со почит, и боговите гледаа.
- `S52` **NAR** — И меѓу ѕвездите се запиша името на Херкул.

---

## 5. Acceptance criteria (testable)

1. Shot count = 52 (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.
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
