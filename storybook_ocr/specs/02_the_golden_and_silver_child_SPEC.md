# 02 — Златното дете и сребреното дете (The Golden and Silver Child)

> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.
> Photoreal · N-clip start-frame-only (43 sec.2) · 1216×704 · 24 fps · model-agnostic (43 sec.4) · **48 shots** (floor 40).

---

## 0. Concept

**Златното дете и сребреното дете** — Златен и сребрен близнак, украдени од завидлива слугинка, растат кај добродушен ловец додека не им ја откријат вистинската судбина во дворецот на богот Нјаме.

*Genre:* Африканска легенда · фантазија

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
| Златното дете / The Golden Child | Новороденче со светкава златна кожа и топол сјај | story-suggested | AI-default |
| Сребреното дете / The Silver Child | Новороденче со светкава сребрена кожа и ладен сјај | story-suggested | AI-default |
| Невестата на Нјаме / Nyame's Bride | Величествена жена во бело-златни облеки, нежна мајка | story-suggested | AI-default |
| Богот Нјаме / God Nyame | Величествен небесен бог со златна круна и бурна аура | story-suggested | AI-default |
| Злобната слугинка / The Jealous Servant | Завидлива жена во темна наметка, подоцна претворена во кокошка | story-suggested | AI-default |
| Ловецот / The Hunter | Добродушен ловец во земјени тонови, со дрвен лак | story-suggested | AI-default |
| Крастави жаби / Toads | Две одвратни жаби со брадавичеста кожа | story-suggested | AI-default |

> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).

---

## 3. Acts & shot list (FLF)

**48 shots · ~159.5s runtime · 241.9s rendered @ ~5s/clip.** Per-shot TWO-PROMPT model (43 sec.3): image-gen keyframe prompt (3a) + video-gen continuation prompt (3b); KF·A/KF·B keyframes, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).

### Act I — Раѓањето и кражбата

*Невестата на Нјаме раѓа златно и сребрено дете. Завидлива слугинка ги краде, ги остава во шумата и во лулките става крастави жаби. Измамениот Нјаме во гнев ја изгонува жена си.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S01 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S02 | MEDIUM | eye-level | push-in | moderate | 3.5s | NAR |
| S03 | INSERT | macro | static | gentle | 3.0s | NAR |
| S04 | MEDIUM | over-shoulder | pan-right | moderate | 3.0s | NAR |
| S05 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S06 | MEDIUM | low-angle | track | moderate | 3.5s | NAR |
| S07 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S08 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S09 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S10 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S11 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S12 | WIDE | low-angle | crane-down | moderate | 4.0s | NAR |

### Act II — Ловецот

*Добродушен ловец ги наоѓа децата во шумата и ги одгледува како свои. Од нивниот златен и сребрен прав гради фарма, но кога ја слуша приказната за исчезнатите близнаци, решава да ги врати кај вистинскиот татко.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S13 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S14 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S15 | MEDIUM | eye-level | track | moderate | 3.5s | NAR |
| S16 | CLOSE | macro | push-in | gentle | 3.5s | NAR |
| S17 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S18 | WIDE | low-angle | crane-up | moderate | 3.5s | DLG |
| S19 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S20 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S21 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S22 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S23 | CLOSE | macro | static | gentle | 3.0s | NAR |
| S24 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S25 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S26 | MEDIUM | eye-level | static | moderate | 3.5s | NAR |
| S27 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S28 | WIDE | high-angle | crane-down | moderate | 3.5s | NAR |
| S29 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S30 | WIDE | eye-level | track | moderate | 4.0s | NAR |
| S31 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |

### Act III — Враќањето

*Ловецот ги враќа децата кај Нјаме. Семејството се обединува, Нјаме ја повикува жена си назад, ја претвора злобната слугинка во кокошка и богато го наградува ловецот.*

| # | Size | Angle | Move | motion | t | cue |
|---|---|---|---|---|---|---|
| S32 | WIDE | eye-level | push-in | moderate | 3.5s | NAR |
| S33 | MEDIUM | over-shoulder | pan-right | moderate | 3.0s | NAR |
| S34 | CLOSE | eye-level | push-in | gentle | 3.0s | NAR |
| S35 | WIDE | low-angle | crane-down | moderate | 3.5s | NAR |
| S36 | MEDIUM | eye-level | static | moderate | 3.0s | DLG |
| S37 | WIDE | eye-level | track | moderate | 3.5s | NAR |
| S38 | CLOSE | eye-level | static | gentle | 3.0s | NAR |
| S39 | WIDE | eye-level | static | moderate | 3.5s | NAR |
| S40 | MEDIUM | low-angle | push-in | moderate | 3.0s | NAR |
| S41 | CLOSE | macro | push-in | gentle | 3.0s | NAR |
| S42 | WIDE | low-angle | crane-up | moderate | 3.5s | NAR |
| S43 | INSERT | macro | push-in | gentle | 3.0s | NAR |
| S44 | MEDIUM | eye-level | static | moderate | 3.0s | NAR |
| S45 | WIDE | eye-level | static | moderate | 3.0s | NAR |
| S46 | MEDIUM | over-shoulder | pan-left | moderate | 3.0s | DLG |
| S47 | WIDE | high-angle | crane-up | moderate | 4.0s | NAR |
| S48 | WIDE | high-angle | crane-down | moderate | 4.0s | NAR |

---

## 4. Narration & dialogue (Macedonian, adapted — never verbatim)

Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.

- `S01` **NAR** — Високо над светот, во дворецот на небото, почна сѐ. Таму живееше богот Нјаме.
- `S02` **NAR** — Неговата невеста роди две деца убави како сон.
- `S03` **NAR** — Едното дете беше цело од злато, а другото — од сребро.
- `S04` **NAR** — Но една слугинка не можеше да ја поднесе туѓата среќа.
- `S05` **NAR** — Зависта ѝ го стегна срцето и во мракот смисли зло дело.
- `S06` **NAR** — Среде ноќ, таа ги зеде децата од нивните лулки и ги однесе.
- `S07` **NAR** — Низ темната шума, сѐ подлабоко, ги однесе да ги остави.
- `S08` **NAR** — Под едно големо дрво ги положи во листовите и си замина.
- `S09` **NAR** — А во нивните лулки остави две одвратни крастави жаби.
- `S10` **NAR** — Кога таткото дојде да ги види децата, го чекаа само жаби.
- `S11` **NAR** — Наместо детски смеи, заслуша само кркање.
- `S12` **NAR** — Во гневот, Нјаме ѝ судеше на сопствената жена и ја изгони од небото.
- `S13` **NAR** — Далеку, во шумата, живееше еден добродушен ловец.
- `S14` **NAR** — Едно утро, нешто слатко допре до неговото уво.
- `S15` **NAR** — Го поведе тој глас низ папратите и грмушките.
- `S16` **NAR** — И под големото дрво, меѓу листовите, најде две сјајни деца.
- `S17` **DLG** — Ловецот: „Колку сте убави!“
- `S18` **DLG** — Ловецот: „Ќе ве однесам кај мене дома!“
- `S19` **NAR** — Ги сакаше како вистински свои синови, и дните минуваа среќно.
- `S20` **NAR** — Секој ден ги капеше во топла вода, и тогаш се случуваше чудо.
- `S21` **NAR** — Од златното дете, во водата паѓаше златен прав.
- `S22` **NAR** — А од сребреното — сребрен прав, како снег од месечина.
- `S23` **NAR** — Ловецот внимателно го собираше тој скапоцен прав.
- `S24` **NAR** — Со тој прав купуваше храна и облека за сите нив.
- `S25` **NAR** — Малку по малку, имаше доволно прав за цела голема фарма.
- `S26` **NAR** — Но еден ден, слушна приказна за златниот и сребрениот близнак.
- `S27` **NAR** — Приказна за деца што исчезнале од дворецот на Нјаме.
- `S28` **NAR** — Тогаш разбра: овие деца му припаѓаат на вистинскиот татко.
- `S29` **DLG** — Ловецот: „Ќе ве вратам кај вашиот вистински татко.“
- `S30` **NAR** — И така тргнаа на долгиот пат кон небесниот дворец.
- `S31` **NAR** — На хоризонтот ги чекаше дворецот на Нјаме, обвиен во бура.
- `S32` **NAR** — Ловецот пристигна пред портите на небото со децата.
- `S33` **NAR** — Во престолната сала стана тишина.
- `S34` **NAR** — Тогаш очите на Нјаме здогледаа сјај што го знаеше.
- `S35` **NAR** — Со раширени раце, богот се спушти кон нив од радост.
- `S36` **DLG** — Нјаме: „Мои деца! Се вративте дома!“
- `S37` **NAR** — Нјаме ја повика невестата да се врати, и таа дојде.
- `S38` **NAR** — Мајката плачеше од среќа, стегајќи ги децата.
- `S39` **NAR** — Целото семејство конечно беше заедно.
- `S40` **NAR** — Тогаш погледот на Нјаме се сврте кон слугинката.
- `S41` **NAR** — Таа трепереше, зашто нејзиното зло дело беше откриено.
- `S42` **NAR** — Нјаме ја крена раката и блесна божествена светлина.
- `S43` **NAR** — Таа светлина ја обви слугинката и почна чудо.
- `S44` **NAR** — Каде што стоеше злобната, сега кокоткаше кокошка.
- `S45` **NAR** — Децата мирно ја гледаа кокошката, а судот молчеше.
- `S46` **DLG** — Нјаме: „Те наградувам за твоето добро срце.“
- `S47` **NAR** — И пред ловецот се појавија богатства: злато, скапоцени камења и свила.
- `S48` **NAR** — И на златното зајдисонце, дворецот блескаше од среќа и мир.

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
