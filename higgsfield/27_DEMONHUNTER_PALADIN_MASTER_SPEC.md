# 27 — Ловецот и Паладинот: Господарот на Пепелта — RECONCILED MASTER SPEC

> **This is the single authoritative package for the Hunter & Paladin boss-fight film.**
> It reconciles `25_…_SPEC.md`, `26_…_SPEC_v2.md`, and the generated storyboard into one lock.
> Zero cost — authoring only. No GPU rented.
> Status: **DEFINE · reconciled + locked**. Compiled 2026-11-05.

---

## 0. What this document is

| File | Role after this reconciliation |
| --- | --- |
| `25_DEMONHUNTER_PALADIN_BOSSFIGHT_SPEC.md` | **ARCHIVED** — superseded by v2. |
| `26_DEMONHUNTER_PALADIN_BOSSFIGHT_SPEC_v2.md` | **CANONICAL FULL SHOT LIST** — the 52-shot beat spine, ability map, 7 dialogue lines, audio, pipeline, acceptance criteria (§2–§10). |
| **`27_…_MASTER_SPEC.md` (this file)** | **AUTHORITATIVE LOCK** — the reconciliation deltas, identity lock, and file convention. Everything that drifted is corrected here. |
| `storybook_ocr/storyboards/41_lovecot_paladin_gospodar_pepelta.html` | **VISUAL LAYER** — generated pre-vis + machine JSON, regenerated to match this lock. |

**Rule:** `26_v2` owns the *cinematic beat spine*; `27` owns the *boundary decisions* (who plays whom, canonical ability names, file convention). They may not disagree. `25` is dead.

---

## 1. Reconciliation findings (what drifted, and the fix)

### 1a. Casting — CRITICAL (my storyboard had it inverted)

| Role | Power colour | `25` | `26 v2` (canonical) | storyboard `#41` as first built | **LOCKED** |
| --- | --- | --- | --- | --- | --- |
| **Ловецот / Demon Hunter** | ❄️ ICE (cold/arcane) | DD | **DD** | ~~Blagoj~~ ✗ | **DD** |
| **Паладинот / Азулон** | ✨ LIGHT (gold) | Azulon-Master `5b059323…` | **Blagoj** (`Blagoj-shaven` `454a359e…`) | ~~DD~~ ✗ | **Blagoj** |
| **Мал‘гарот / boss** | 🔥 FIRE (ash) | AI-default | AI-default | AI-default ✓ | **AI-default** |

- The power/colour mapping was **correct** in my storyboard (Hunter=ice, Paladin=gold); only the **face assignment was swapped**.
- `25` named the paladin **Azulon-Master**; `26 v2` re-cast him to **Blagoj** (the user's own face). v2 wins.
- **Lock:** DD = Demon Hunter (cold/arcane). Blagoj = Paladin (light). Boss = AI-default, always zero faces.

### 1b. Ability names — canonicalized to v2 (cold/arcane re-skin)

| Concept | `25` (WoW names) | `26 v2` (canonical) | storyboard drift | **LOCKED** |
| --- | --- | --- | --- | --- |
| Aura ring | Immolation Aura | **Glacial Aura** | "Леден ореол" / ICE HALO | **Glacial Aura** |
| Eye lance | Eye Beam | **Rime Beams** | "мразни греди" / ice-beams | **Rime Beams** |
| Dash | Fel Rush | **Frost Rush** | (not in 20-shot board) | **Frost Rush** |
| Spin | Blade Dance | **Frost Dance** | (not in board) | **Frost Dance** |
| Ultimate (DD) | Metamorphosis | **Glacier Form** | "Ледената облика" / ICE FORM | **Glacier Form** |
| Dive | The Hunt | **The Hunt (Glacial Drift)** | (not in board) | **The Hunt (Glacial Drift)** |
| Combo #1 | (unnamed) | **Freeze-and-Sunder** | "Замрзни-и-Скрши" | **Freeze-and-Sunder** |
| Combo #2 | (unnamed) | **Hoarfrost Judgement** | "Скрежна пресуда" | **Hoarfrost Judgement** |
| Combo #3 | (not in 25) | **Blizzard & Verdict** | (condensed) | **Blizzard & Verdict** |
| Ultimate (Pal) | Avenging Wrath | **Avenging Wrath** | "Одмаздничкиот гнев" | **Avenging Wrath** |

**Lock:** all ability names follow `26 v2` exactly. The Macedonian narration may keep natural Macedonian phrasing (it is voice-over, not a spec token), but the **machine fields (`kf_*`, `continuity`, `motion`) must use the canonical English ability names** so the job builder is unambiguous.

### 1c. Beat order & dialogue

| Axis | `26 v2` (canonical full film) | storyboard `#41` (proof-density) | Note |
| --- | --- | --- | --- |
| Shots | 52 | 20 | storyboard is proof-density by design; expands to 52 at full run |
| Combos | 3 (Freeze-and-Sunder #19, Hoarfrost Judgement #33, Blizzard & Verdict #43–45) | 2 (Freeze-and-Sunder explicit; Blizzard & Verdict condensed as the dual finale S17–S18) | add Hoarfrost Judgement as its own beat on expansion |
| Dialogue lines | 7 (D1–D7) | 6 (missing D3) | add D3 on expansion |

**Missing dialogue line (D3):** the Paladin's under-breath vow in Phase 2 —
> **„Светлината не се гаси."** (Azulon, P2 #26)

Full dialogue lock (from `26 v2 §5`, 7 lines):
1. Boss — „Дојдовте да изгорите, како сите пред вас." (P1)
2. Boss — „Мразот само ја прави пепелта поубава." (P2)
3. Paladin — „Светлината не се гаси." (P2, under breath)
4. Boss — „Од пепел сте — и во пепел ќе ве вратам!" (P3)
5. DD — „Замрзни." (P3)
6. Paladin — „Суди." (P3)
7. DD (epilogue) — „Пепелта е само снег што не стигнал на време."

---

## 2. Authoritative locks (single source of truth)

1. **Identity** — DD = Demon Hunter (ice/arcane); Blagoj (`Blagoj-shaven` `454a359e…`) = Paladin/Azulon (gold light); boss AI-default. *(see §1a)*
2. **Elemental triangle** — ice × fire → shatter; light × fire → purify; ice × light → three tag combos. *(26_v2 §0, §2)*
3. **Ability names** — canonical v2 set only. *(§1b)*
4. **Beat spine** — 52 shots / 3 phases / 3 combos / 7 dialogue lines. *(26_v2 §4–§5)*
5. **Identity gates** — DD ≥ 0.50 vs `dd` centroid; Paladin ≥ 0.50 vs `Blagoj-shaven` centroid; boss = 0 faces. *(26_v2 §8)*
6. **DD look** — glowing blue→teal → weightless under-water-waving hair (never static), SUIT is hooded. *(26_v2 §1)*
6a. **BARE HEAD (absolute)** — DD never wears helmet, hood, bandana, mask, or ANY head/face covering. Reason: the hair IS the signature — teal→blue, magically glowing, waving as if underwater with every move — and it must stay visible in every frame and every asset. Headwear of any kind hides the one feature that makes DD read as DD. (director standing order 2026-11-07)
6b. **Immortal wings** — Diablo-Immortal-style Immortal wings on the hunter, rendered in his own cold/arcane magic energy color (blue→teal), matching the hair and the entire ICE style system. Present in combat states; scale/wing language per Diablo Immortal Immortal-wing reference (internet-sourced prop reference, CC0/PB).
7. **Azulon look** — bald, one-sided molten-gold rune-tattoo maze that surges per ability (SUIT helmed; helm OFF only in Avenging Wrath). *(26_v2 §1, §1b)*
8. **Format** — 1280×720 landscape · 24 fps · photoreal · FLF start+end, single-reference jobs rejected. *(26_v2 §7–§8)*
9. **Audio** — Macedonian-only dialogue; spatial SFX; restrained score. No narrator. *(26_v2 §5–§6)*
10. **No self-made benchmark** — style validated only against external cinematic references (Diablo 2 / WoW / StarCraft / wuxia). *(doctrine + 24 report)*

Open questions carried over from `26_v2 §10` (still pending user):
- Paladin tattoo colour (molten gold confirmed?)
- DD hair blue-to-teal (confirmed?)
- Title card „Исечени во пепелта"
- Proof scene first?
- Runtime lock ~2:30 (52) vs ~3:00 (60+)

---

## 3. File convention (answers: is there a spec.md for every story?)

**Yes — every film gets exactly two artifacts, from one source of truth:**

| Artifact | What it is | Who/what consumes it |
| --- | --- | --- |
| `spec.md` | the **authoritative text contract**: research, identity lock, ability map, beat spine, dialogue, audio, pipeline, acceptance criteria, cost | the **human** for review/approval; git-diffable decision record |
| `storyboard.html` | the **generated visual layer** + embedded machine JSON (`<script id="storyboard-spec">`) | the **human** for spotting + the **AI job builder** for execution |

**The rule that prevents the drift this cross-check caught:**
- The `spec.md` is the **canon**; the HTML is **derived**, never authored independently.
- The HTML reads its shot data from a structured source that **mirrors the spec** (see `tools/build_storyboard_html.py`), so a chance in the spec propagates to the board instead of drifting into a third conflicting copy.
- Naming: `NN_<title>_SPEC.md` + `NN_<title>_storyboard.html` (e.g. `41_Ловецот…_SPEC.md` / `41_…_storyboard.html`).

---

## 4. Corrections applied to the storyboard (#41)

- [x] Cast swapped to match lock: **Hunter = DD**, **Paladin = Blagoj**.
- [x] Machine ability terms aligned to v2 (Glacial Aura, Rime Beams, Freeze-and-Sunder, Hoarfrost Judgement, Glacier Form, Avenging Wrath).
- [ ] D3 „Светлината не се гаси." and a dedicated Combo #2 „Hoarfrost Judgement" beat — **deferred to the 52-shot expansion** (they belong to full-film density, not the 20-shot proof board).

*DEFINE-ONLY. No GPU rented; nothing spends until the §2 open questions are confirmed and an itemized P6 estimate is approved per run.*

## BARE HEAD MANDATE (director standing order, 2026-11-07)

DD NEVER wears a helmet, hood, bandana, mask, or ANY head/face covering —
bare head and face in every shot, every state, every asset. No exceptions.
- Applies to: all keyframes, all look cards, all fused masters, all
  turnarounds, all video frames, all states (idle + glacier).
- Asset rule: any DD reference card or render showing headwear is REJECTED
  and must be re-rendered before use downstream.
- Prompt rule: every DD prompt must carry 'bare head, no helmet, no hood,
  no bandana, no mask' and every DD negative must carry 'helmet, hood,
  bandana, mask, head covering'.

## BACK-PIECE RULE (director, 2026-11-07)
DD may wear a hood ONLY as a back piece — a cowl/cape resting on the
shoulders and back. NEVER a cap, hood, bandana, mask, or any head/face
covering. The head stays bare at all times so the glowing teal-blue
underwater hair is fully visible. Reject and re-render any DD asset
showing headwear.
