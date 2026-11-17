# KARSUS'S FOLLY: Script v3 (revision of v2, 2026-11-01)

> Unofficial Fan Content permitted under the Wizards of the Coast Fan Content Policy. Not approved or endorsed by Wizards. Portions of the materials used are property of Wizards of the Coast. (c) Wizards of the Coast LLC. The film must stay free to watch.

**Format:** 16:9, now **118.1 s** (was 122.1). **Hero:** Karsus, greatest archwizard of Netheril, played by Blagoj Nikolov. **Author's rule, amended 2026-11-01:** Karsus never *walks out* of his tower and is never shown anywhere else alive. He ends the film as stone going over the edge of it — that is not a departure, it is the consequence. Every scene before that is inside the tower.

**Timing of this revision:** written before a single Wan clip was rendered. Every change below is therefore **free** — it costs prompt text, not GPU time. That is the whole reason to revise now and not after spending the credit.

---

## 0. What changed from v2 and why (ranked by impact)

### 1. The people are now on screen (highest impact, 1 clip swapped, net zero cost)

**Problem.** The theme is "a man who tried to save his people". The film is 122 s of architecture and one man. **Not one Netherese citizen appears.** "Save them" has no referent. The audience is asked to care about a motive that is only ever spoken in voice-over.

**Fix.** `sp1c` changes from a third glide over the same cloudscape into the crowd: robed figures on the edge of a white stone terrace, **backs to camera**, looking up at the sky. It ends the opening on anxious people, cuts straight to the monsters, and makes the last shot (statue in the forest, centuries later) mean something.

**Why backs to camera and a concrete count:** Wan's documented failure modes are pulling faces and turning small groups of people into "helicopters and fish" (handover section 11). Rear-facing silhouettes in middle distance, "a dozen", avoid both. **Expect to regenerate this clip once.** Budget for it.

### 2. The three white-outs are broken apart (free, fixes the film's biggest structural flaw)

**Problem.** As written, three consecutive climaxes are the *same image*: the glow becomes blinding white.

| Clip | v2 prompt |
|---|---|
| `sp3e` | "the glow intensifies into a blinding blue-white light" |
| `sp4c` | "a blinding white glow grows around the man until it fills the frame" |
| `sp5sa` | "a blinding white flash grows around the man as grey stone spreads" |

Three false endings of the same visual type, 25 s apart. Each one tells the audience "this is the climax", so the actual climax lands on a shot they have already seen twice.

**Fix.** Reserve white for exactly one moment — the stone.

| Clip | v3 prompt | Effect |
|---|---|---|
| `sp3e` | "The last of the light drains upward out of the clouds into the dark vortex. The man is left standing in darkness, his crown and staff rimmed with a thin blue edge light. The camera holds steady." | **Darkness.** The theft reads as a *taking* |
| `sp4c` | "The vast goddess of light grows faint and transparent as her light pours into the man. Her outline breaks into drifting motes and is gone. The camera holds steady." | **Her death is on screen** |
| `sp5sa` | unchanged — the only white-out in the film | The payoff finally lands |

This also fixes problem 3 below without a new shot: Mystryl's sacrifice is currently invisible. She has 15 s on screen and then stops talking, while the man beside her turns to stone. **She is the one who actually dies for this.** Now the audience sees her go.

### 3. `sp5b` follows the wrong subject (free, prompt edit)

**Problem.** v2: "The camera follows the fall" — of the **city**. Fourteen seconds of falling architecture, and the character we are attached to is a stone object somewhere in it, too small to read. The emotional beat is thrown away on scenery.

**Fix.** "The camera stays locked on the grey statue on the spire as the city tilts and drops beneath it through the sea of clouds. The statue remains in the centre of the frame, small against the falling towers." The audience watches **him** fall, not the real estate.

### 4. Karsus gets one beat of understanding (free, folded into an existing clip)

**Problem.** He is serene (SP3), straining (SP4), then stone. The single most important acting beat in the film — the moment he realises what it cost — is compressed into a VFX transition.

**Fix.** Inside `sp5sa`, before the stone reaches his face: he looks down at his own hand. The author rejected a separate hand-insert shot; this is the same idea with no new clip.

### 5. The optional lines are not optional — I was wrong about this (free text, but needs TTS)

In the previous review I listed these as decoration. Reading the structure again: they are **load-bearing**.

- **"Be unmade."** is the only line where Karsus speaks *as a god*. It is the exact instant of transgression. Without it, the wrath is a silent victory montage and the audience has no signal that it is a crime.
- **"It is too much, Karsus."** is Mystryl's only acknowledgement that he is killing her. Without it she simply stops speaking, for no stated reason.

**Recommendation: include both.** Caveat, honestly: neither line exists in the recorded stems (`K1 K2 K3 M12 M3` cover the 5 v2 lines only). They need new ElevenLabs Voice Design previews, and the handover records that the free tier's saved-voice slots are **full (3/3)**. If TTS fails, fall back to silence — do **not** synthesise a new voice, the two designed voices are the film's continuity.

### 6. The score now fits without the loop hack (free)

**Problem.** v2 was 122.1 s against a 100.1 s score, so section 9.4 looped the climax (55.3–60 s) over the wrath with a 0.3 s crossfade. Looping the emotional peak over the film's moral nadir is backwards, and the loop point is audible.

**Fix.** The v3 cut is shorter, and the wrath is scored with **nothing**:

- 0 → 63.3 s: score plays straight through, no edits.
- 63.3 → 73.3 s (**the wrath**): **score out.** Only the magic, the fire, the dying monsters, and Karsus's "Be unmade."
- 73.3 s (the flash): one sustained sub-bass hit, then dead silence into SP5a.
- 100.9 → 118.1 s: the opening theme reprise under SP6 and the end card.

Total score used: **80.5 s of the available 100.1 s.** No loop, no crossfade, no audible seam. The silence in SP5a only works if the sound *before* it is dense — this is the correct way to earn it.

### 7. Runtime trims (free)

| Item | v2 | v3 | Why |
|---|---|---|---|
| SP5a (lights out) | 8.0 s | **6.0 s** | 8 s of a static dark frame with silence is 6.5% of the film. The beat is strong; it does not need to be long. Compression increases impact. |
| End card | 6.0 s | **4.0 s** | 5% of runtime on a title card. 4 s is still generous. |
| Total | 122.1 s | **118.1 s** | Tighter, and the score fits. |

### 8. Rejected / not recommended

- **Adding an explicit statue-falls-to-ground shot.** The ellipsis into SP6 is fine and arguably better: "moss-covered, roots" already reads as centuries later. Do not spend a clip on it.
- **Cold-open flash-forward on the forest statue.** Tempting, but it would spend the film's final image in the first three seconds for a payoff that SP6 already delivers. Keep the linear structure.
- **Making the monsters attack a person.** The ecological horror (land dying) is more original than a chase, and Wan renders creature-vs-human poorly. The trade-off is a less cathartic wrath — accept it, it is the more interesting film.

---

## 1. Story spine (unchanged from v2)

Netheril: human archwizards in flying cities held aloft by mythallars. Underground predators, inspired by the phaerimm of canon, climb to the surface and drain magic from the land, leaving grey desert. No god answers. Karsus casts *Karsus's Avatar*, taking the divine power of Mystryl. For an instant he is a god and burns the horde from his tower. He cannot hold the Weave. Flash, stone. Mystryl dies, all magic fails, the cities fall. His statue lies in the High Forest.

**Theme:** a man who tried to save his people by taking what can only be given.

---

## 2. Structure (v3 timeline, 118.1 s)

| Set piece | Film time | Length | Content | Wan clips |
|---|---|---|---|---|
| SP1 sky cities **+ the people** | 0–13.3 | 13.3 | Glide above the cloud sea between two floating cities, **ending on a crowd on a terrace looking up** | 3 (a, b, **c = crowd**) |
| SP2 the feeding | 13.3–26.3 | 13.0 | Monsters pull glowing threads out of trees and water; forest greys and collapses into dunes | 3 |
| SP3 the ritual | 26.3–48.3 | 22.0 | Karsus on the balcony, glyph rings, vortex, lightning, the other cities dim as light flows to him, **then darkness** | 5 |
| **SP4 THE ACT — one event** | **48.3–73.3** | **25.0** | **The taking and the killing are the same act, and it plays out while the two of them talk.** | **5 (interleaved)** |
| SP5s the overload | 73.3–83.3 | 10.0 | Magic overflows him: light bursts through his cracks, grey stone climbs his throat, **the statue tips off the balcony and falls** | 2 (first-last-frame) |
| SP5a lights out | 83.3–89.3 | **6.0** | Every light goes out. Absolute silence. | 1 first-last-frame + 1 s hold |
| 1.2 s dissolve | 88.1–89.3 | — | Hides the cut, as in v2 | — |
| SP5b the fall | 88.1–102.1 | 14.0 | **The statue falls through the clouds** while the city drops around it | 3 |
| SP6 epitaph | 102.1–114.1 | 12.0 | Statue in a sunlit forest, moss and roots, push-in to the stone face | 3 |
| End card | 114.1–118.1 | **4.0** | "-339 DR. The year magic died." + notice | none |

### SP4 cut order — one event, five clips

| # | Clip | Start still | What is on screen |
|---|---|---|---|
| 1 | `sp4a` | `k_sp4` | The goddess pours white light into the small man |
| 2 | `sp4b` | chained | The man raises his arms, the beams flow into him, he is already straining |
| 3 | `sp4wa` | `k_sp4w` | **Cut away, same second:** columns of white and gold fall on the desert, monsters vaporising |
| 4 | `sp4c` | `k_sp4` | **Back up:** the goddess goes transparent, breaking into motes |
| 5 | `sp4wb` | `k_sp4w` | **Back down:** golden fire sweeps the desert, the last of the horde burns |

The interleave is moral, not decorative. The audience must hear him say "only for a moment" **while the desert is already burning**. Two sequential blocks let the destruction arrive after the argument, as a consequence he could not foresee, which makes him the magic's victim. Simultaneous cuts make him its author. Same duration, same five clips, opposite verdict on the man.

### Why he turns to stone, and why he leaves the tower

Petrification is the visible result of taking more than a body can hold. The light does not stop at his skin: it keeps arriving until it turns him to stone, and the stone is what leaves the tower. He is not struck down and he does not sit there; **he overloads, stiffens, and tips over the edge still holding the pose.** `sp5sa` is the overload (light bursting through the cracks, stone climbing his throat), `sp5sb` is the fall. One cause and one effect across a first-last-frame pair, so the two clips cannot drift apart.

Still 25 clips. **Net cost of this revision: zero clips** — `sp1c` is a swap, not an addition., because `sp1c` is a swap, not an addition.

---

## 3. Dialogue (film seconds, v3 timeline)

| Time | Where | Voice | Line | Stem |
|---|---|---|---|---|
| 13.6 | SP2 | KARSUS V.O. | "They drink the land. River, forest, city. I have begged every god in the sky... and the sky is silent." | K1 (have) |
| 42.3 | SP3 | KARSUS, whisper | "Then I will stop asking." | K2 (have) |
| 48.6 | SP4 `sp4a` | MYSTRYL | "Karsus. Put it down. You are holding everything." | M12 (have) |
| 53.6 | SP4 `sp4b` | KARSUS | "Only for a moment. Only long enough to save them." | K3 (have) |
| 58.3–63.3 | SP4 `sp4wa` | — | **his excuse still echoing while the desert burns. Nothing is said over it.** | — |
| 63.6 | SP4 `sp4c` | MYSTRYL, fading | "A moment is all it takes." | M3 (have) |
| **68.8** | **SP4 `sp4wb`** | **KARSUS, low, terrible** | **"Be unmade."** | **K4 (needs TTS)** |
| **74.0** | **SP5s** | **MYSTRYL, fading** | **"It is too much, Karsus."** | **M4 (needs TTS)** |
| 83.3–89.3 | SP5a | — | absolute silence | — |
| 100.9 | SP6 | KARSUS, old echo | "I only wanted to save them." | E.wav (have) |

**Dialogue is scoped to the cut order above, not to run time.** "Only for a moment" lands over the man receiving; the burning desert then plays in silence with his words still in the air; Mystryl answers over her own body coming apart; his command falls on the fire. That four-beat ring — excuse, silence, her answer, his word — is the argument, and it only works because the two events are one. The two lines marked TTS are the only audio to record; if the free tier refuses, cut to silence rather than synth a new voice, because a stranger's voice is worse than none.

Audio to be rebuilt from the **individual stems** (`voices/K1..M3.wav`) rather than by re-cutting `dialogue_v6.wav`, which already carries its mix effects and was timed to the v1 positions. Re-timing an effected track compounds artefacts. **The stems are on KVM4 and have not yet been pulled.**

---

## 4. Locks (verbatim from project canon — do not paraphrase)

**Why this section is now the most important one.** The first draft of this file abbreviated the Karsus lock, and the abbreviation silently dropped the two hooked horns, the asymmetric left-shoulder plate, the mail gorget, the ruby brooch, the cyan chest diagram and the staff's orbiting rune ring. That is exactly how wardrobe drift enters a film — `07b` already records the mantle turning green-cream at 6 s in the Seedance draft. **An abbreviated lock is a corrupted lock.** Copy the text below character for character.

- **KARSUS LOCK** — final, from `07b_KARSUS_COSTUME_RESEARCH.md` (Direction A decision, 2026-10-31): the man from the Blagoj-Base reference, unmistakably the same real person, same face, eyes, nose, mouth, jaw and age; hairless shaved head, clean-shaven, light grey-green eyes, real unretouched skin; Karsus, archwizard of Netheril: heavy indigo-to-midnight brocade robe woven with silver geometric patterns, a long open ceremonial over-mantle with an ivory-silk lining and train, a tall flared stiff collar standing high behind the head like a halo, fine silver mail at the forearms and a mail gorget, one asymmetric sculpted steel shoulder piece on the left shoulder with gold scale inlay and pale blue glowing gems, a wide jewelled belt, a ruby brooch clasping the mantle, silver rings on every finger, a glowing cyan spell diagram (nested concentric circles and straight lines) over the chest and down the robe, a small slim fitted crown of mottled silver-steel with two small hooked horns, a short central spike, gold scale inlay and two rubies, a tall silver staff topped by a large pale blue gem with a ring of tiny glowing runes orbiting its head

- **Base prompt block** — from `CHARACTER_SYSTEM.md`, paste *before* the costume text: the man from <<<f5e2e917-3a91-4213-a01a-ffbca43c7d4c>>>, unmistakably the same real person, same face, eyes, nose, mouth, jaw and age; light grey-green eyes; real unretouched skin with pores

- **Do not use the Soul identity for Karsus.** `IDENTITY.md`'s mandatory Soul phrase contains "short ginger-brown moustache and light stubble". Karsus is **clean-shaven from `Blagoj-Base`** (`f5e2e917-…`), not the Soul. Pasting that phrase here grows him a moustache and breaks the character.

- **MONSTER LOCK:** pale grey scorpion-like monsters the size of horses, segmented bodies, many clawed limbs, long tails, mouths ringed with writhing tendrils, drawing glowing blue-white threads of magic from trees and water.
- **ENCLAVE LOCK:** a city of white stone towers and gold domes on a gigantic inverted mountain, floating above a sea of clouds, waterfalls spilling off its edges.
- **STYLE LOCK:** photorealistic AAA game cinematic, volumetric light, natural film grain, anamorphic framing, no text.

- **Render lock** — read from `tools/vast/batch_karsus_v3.py`, not assumed: **832x480, 16 fps**, seed `100 + index`, negative `blurry, distorted, extra objects, helicopters, birds, boats, flickering, text, watermark, jitter, morphing, extra people`.

- **Likeness gate** — from `CHARACTER_SYSTEM.md` rule 3 and `09` section 5.5: mean SFace **≥ 0.50** on the median hero frame of every face set piece (SP3, SP4, SP5s, SP6), worst frame reported; on frontal views every geometry ratio within **±10 %**. A clip below the limit is **rejected no matter how good it looks**, because a beautiful wrong face is the one defect an audience always catches.

---

## 5. The one new keyframe (SP1c, the crowd)

**Status: DONE and verified on screen, 2026-11-01.** Three candidates were generated with `tools/gemimg.py` (model `gemini-2.5-flash-image`, 1344x768, reference `k_sp1.jpg`) and each inspected visually before adoption.

| Candidate | Verdict |
|---|---|
| `k_people_hooded.jpg` — crowd of hooded figures across the full terrace | **Rejected.** Clean anatomy, but it walled off the central avenue, so a push-in had nowhere to travel, and the warm sunrise read as welcoming rather than ominous. |
| `k_people.jpg` (first) — unhooded crowd, backs to camera | **Rejected.** Anatomically clean and no visible faces, but **every figure was bald** — the crowd became ten copies of Karsus's single identifying feature, which both weakens him and reads as a monastery of clones. |
| **`k_people_v3.jpg` — two hooded figures, lower corners, clear central avenue** | **ADOPTED.** Cold desaturated dawn, long empty stone avenue between the figures leading to the towers, obvious push-in path, no faces anywhere. |

The adopted prompt:

> "Photorealistic AAA game cinematic still. Deep-hooded citizens in heavy travelling cloaks of muted brown, grey and dark blue stand in the left and right foreground at the edge of a white stone terrace of a floating city, their backs to the camera, heads covered, no faces visible. A wide clear avenue of empty pale stone runs between them straight toward distant white towers with gold domes, and a second floating city beyond. Cold overcast dawn light, desaturated blue-grey palette, thin mist. Figures are small in the lower corners of the frame. Tense, uneasy, ominous mood. Volumetric light, anamorphic framing, no text."

Saved as `media/stills_v2/k_people.jpg` (SHA-256 `024739872cf0d49af57b6b61bb1505e5a941f01d546c667fcf0f4ab653bab785`).

**Deliberate deviation from this document's own plan: it is two onlookers, not a dozen.** This is the better film *and* the safer render. Two large, separated, hooded figures are dramatically less likely to produce Wan's crowd artefacts than twelve small ones, and two silent witnesses at the edge of a terrace frame the shot better than a wall of backs. The trade-off, stated honestly: it suggests a handful of citizens rather than a population, so SP1c carries "someone is watching" rather than "a city of people is afraid". The monsters in SP2 and the statue epilogue carry the scale. **Accept this or ask for a wider crowd — but do not ask Wan for a dozen in a single shot.**

---

## 6. Wan prompts changed from v2 (one mover each, positive wording, no small objects)

Unchanged: SP1 a/b, SP2 a/b/c, SP3 a/b/c/d, SP4 a/b, SP5sb, SP5a, SP6 a/b/c. **Changed since v3 was written:** SP4 is one 25 s block of five interleaved clips (`sp4a`, `sp4b`, `sp4wa`, `sp4c`, `sp4wb`); petrification is magical overload and `sp5sb` is the fall.

**NEW — `sp1c` (k_people.jpg, two hooded figures):**
> "The camera pushes slowly forward between two hooded figures along the empty stone avenue toward the distant towers. Steady and smooth."

**One mover: the camera.** My earlier draft also moved the cloaks in the wind. Two movers in one Wan prompt is the documented way to get mush — the model splits its budget between them and neither resolves cleanly. The cloaks are already heavy and dark in the keyframe; they do not need to billow. Cut them.

Note the verb from v2's plan: **"looking out"**, not "looking up". The adopted still has them facing the horizon, and Wan follows the first frame. Do not write motion that contradicts the keyframe — the opening frame is the model's strongest instruction.

**CHANGED — `sp3e` (was: blinding blue-white light):**
> "The last of the light drains upward out of the clouds into the dark vortex. The man is left standing in darkness, his crown and staff rimmed with a thin blue edge light. The camera holds steady."

**CHANGED — `sp4c` (was: blinding white glow fills the frame):**
> "The vast goddess of light grows faint and transparent as her light pours into the man. Her outline breaks into drifting motes and is gone. The camera holds steady."

**CHANGED — `sp5sa` (was: blinding white flash as stone spreads):**
> "Grey stone creeps up the man's throat and across his jaw. His eyes stay open. The camera holds steady."

**This prompt was wrong in my first pass and the keyframe proved it.** I wrote "He looks down at his own hand as grey stone spreads up his fingers and arms" — but `k_stone_a.jpg` **already shows cracked stone on both raised arms**, and his arms are raised in the apotheosis pose. The prompt therefore (a) re-animated motion that is already in the first frame, and (b) asked for a pose the frame cannot reach. Wan resolves that by morphing the arms downward into the wound on the chest. The hand-look beat is **dropped**: here it is the wrong beat for this staging. What is left to show is the stone reaching his face while he is still present behind his eyes, which is the more terrible version anyway.

**Transformation now actually spans two clips, correctly:**
- `sp5sa` starts `k_stone_a` (arms already stone) → `sp5sb` ends `k_stone_b` (fully stone). A legitimate first-last-frame pair.
- v2 had no flesh-to-stone clip at all. The audience saw a living god and then a finished statue. That gap is the reason the film's central punishment had no weight.

**CHANGED — `sp5b` a/b/c (camera subject corrected):**
> "The grey stone statue on the balcony stays fixed in the centre of the frame as the city tilts beneath it and drops straight down through the sea of clouds. Small against the falling towers. The camera holds on the statue."

Negative for all, unchanged: "blurry, distorted, extra objects, helicopters, birds, boats, flickering, text, watermark, jitter, morphing, extra people".

---

## 7. Audio plan (v3)

| Segment | Score | Dialogue |
|---|---|---|
| 0–63.3 | score straight, no edits | K1, K2, M12, K3, M3 at the times above |
| 63.3–73.3 | **silent** | K4 "Be unmade." at 65.2 |
| 73.3 | one sub-bass hit | M4 "It is too much" at 74.0, then nothing |
| 83.3–89.3 | silence | silence |
| 100.9–118.1 | score reprise | E.wav echo at 100.9 |

Build from stems, duck the score under dialogue with a sidechain as in the v5 recipe, and finish with `loudnorm=I=-16:TP=-1.5:LRA=11`. Verify with `silencedetect=n=-50dB:d=2` on the SP5a window and `ebur128` for the integrated target; transcribe each line back to confirm placement. Keep the **input-side `-ss`** rule from the handover — output-side seeking breaks later `afade st=` values.

---

## 8. Cost of this revision

| Item | Cost |
|---|---|
| All prompt changes, timeline trims, score removal, camera-subject fix | **$0** — nothing has been rendered yet |
| `k_people.jpg` keyframe (Gemini) | ~$0.00, one API call |
| Crowd clip regeneration risk (Wan renders crowds badly) | +1 clip, ~60 s GPU, **~$0.01** |
| Two new TTS lines | ElevenLabs free tier may refuse — **slots 3/3 full** |

No new GPU budget. The batch stays at **25 clips, ~$0.40–0.55** for the 480p pass.

---

## 9. Open questions for the author

1. **Include "Be unmade." and "It is too much, Karsus."?** Recommended yes (section 0.5), but they need new TTS and the free tier may block them.
2. ~~Accept the 6 s lights-out~~ — **applied**, and the end card is cut to 4 s in the assembler.
3. **Canon check before the end card:** confirm Karsus's canonical fate and the Karse location against a Forgotten Realms source rather than trusting this document. The film is fan content with deliberate liberties, but the epitaph should not contradict canon without the author intending it.

---

## 10. Status

Written 2026-11-01 from the v2 script and the handover. **Nothing rendered.** v2 is untouched at `higgsfield/11_KARSUS_FOLLY_SCRIPT_v2.md`; this file supersedes its prompts and timeline if the author accepts it.

Changes required in `tools/vast/batch_karsus.py` to run v3: add `k_people.jpg` to the upload set, repoint `sp1c` to it with the new prompt key, and replace the prompt text for `sp3e`, `sp4c`, `sp5sa`, `sp5b`.
