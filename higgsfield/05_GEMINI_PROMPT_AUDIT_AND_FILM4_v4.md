# Part A: audit of every prompt Gemini wrote. Part B: Film 4 v4, an original script with voices

**Date:** 2026-10-30. **Status:** for approval. **Nothing will be generated until you approve Part B.**
**Brief (your words):** don't copy the reference; English voices whose colour suits each character; 60–100 s; the paper seraph is optional; start with the D&D theme of the angels of decay, their liberation and the curing of the corruption.

---

## PART A: prompt-by-prompt audit of the Gemini conversation

Gemini wrote **15 prompt units in 5 rounds**. Each is scored on six criteria:
- **Lore**: faithful to its source myth or setting.
- **Engine fit**: uses parameters the Higgsfield/Kling models actually have.
- **Identity**: handles your face correctly.
- **Shot craft**: one camera move and one action per clip.
- **Coherence**: no internal contradictions.
- **Originality**: not a trademark copy.

Scale: ● good, ◐ partial, ○ failing.

### Round 1: "Paper seraph is you" (3 scripts × 4 shots)

| # | Prompt | Lore | Engine | Identity | Shot craft | Coherence | Original | Verdict |
|---|---|---|---|---|---|---|---|---|
| R1.1 | *Purging of the Frozen Crown* (WoW) | ◐ Lich-King archetype, but a paper angel doesn't belong in Warcraft | ○ "Higgsfield cinema camera:" is not a parameter | ○ "his face is yours" with no mechanism | ● one move per shot | ◐ blue thorn crown + gold light + green ribcage = three competing palettes | ◐ skeletal king + frost-runed sword ≈ Frostmourne/Arthas | Strong shot list, weak everything else |
| R1.2 | *Binding of the Fenrir Beast* (Norse) | ○ volcanic wasteland + glowing chains contradict *Gylfaginning* ch. 34 (Gleipnir is a silk-thin ribbon; Lyngvi island) | ○ same | ○ same | ● | ◐ "decaying wolf": Fenrir isn't undead | ● | Rewritten in my Film 2 (Týr & Gleipnir) |
| R1.3 | *Origami Ascension* (void) | n/a (original) | ○ same | ○ same | ● ECU→pull-back is good craft | ● | ● | **The best of Round 1.** "Fire that does not consume the paper" is a genuinely good image. |

**Round 1 lesson:** good camera language, but no working identity method and loose lore.

### Round 2: "different costume per world" (3 scripts)

| # | Prompt | Changes vs R1 | Verdict |
|---|---|---|---|
| R2.1 | *Paladin's Judgement* | Paper robe → silver plate, gold runes, wolf-fur mantle, warhammer | ● Costume now fits the world. ○ Still "his face is your exact likeness" with no mechanism. ◐ The hammer + ring of holy fire is a standard paladin beat: fine, but generic. |
| R2.2 | *Aesir's Chain* | Bearskin, Yggdrasil leather, **lightning hands** | ○ Lightning makes him Thor, yet the beast-binding is Týr's story. ○ Lore still wrong (chains of light, volcano). |
| R2.3 | *Origami Ascension* | Adds the "glowing crown of thorns" | ◐ Unchanged otherwise. The crown of thorns is a strong Christian icon; it's fine, but it's what the reference uses, so it reads as a copy. |

**Round 2 lesson:** the right instinct (costume suited to each world), still no technical spine.

### Round 3: *The Lunar Purge*, first D&D draft (4 shots); **the most important for us**

| Shot | What Gemini wrote | Assessment | Keep for v4? |
|---|---|---|---|
| 1 | Low-angle track through a ruined, thorn-choked cathedral; two angels of decay over a desecrated altar; raven feathers, "weeping obsidian", purple-black Shadow Weave ichor; **cracked porcelain masks** | ● Strong mood. ◐ Shadow Weave is real FR lore (Shar's), but "angels of decay" in canon are rotting undead streaming liquid corruption [Libris Mortis pp. 83–84], not obsidian. ○ The masks hide the faces, which **kills the climax**: we must see the priestess's face under the rot to feel the restoration. | Keep: purple-black corruption, the desecrated sanctum. **Drop the masks.** |
| 2 | Male "Avatar of Selûne" descends; asymmetric moon-forged plate; starlight silks; **crescent-moon mace** | ○ Selûne's avatars are all female [Faiths & Avatars pp. 134–135]. ● The costume idea is good. ◐ The mace echoes her real weapon, the Rod of Four Moons (four-flanged heavy mace) [F&A p. 134]. | Keep the costume language. Recast the role as a **mortal Selûnite**. The mace is optional. |
| 3 | Angels lunge; he **does not strike them**, slams the mace into the floor; crystalline moonlight shockwave; ichor boils into silver mist | ● **The best idea in the whole conversation:** a cure, not a kill. ◐ Still a power move rather than a reason the cure works. | Keep: non-violence and silver mist. **Add a reason** (see v4: remembering). |
| 4 | 180° orbit; crust shatters; pearlescent wings; restored Shards kneel; moonglow fills the vault | ● Visually right. ● Canon-accurate result (blue hair and pearly skin, added in Round 4) [F&A p. 135]. ○ Kneeling to a mortal is odd for planetars. | Keep the transformation. **Change kneeling to recognition** (they rise and name him). |

### Round 4: "optimised" four prompts (Paladin, Beast, Origami, Lunar Purge)

| # | Change vs earlier rounds | Assessment |
|---|---|---|
| R4.1–R4.3 | Removed "your face is…", added "volumetric lighting", "saliva in slow motion", "perfect ring" | ◐ Richer visuals. ○ Identity still undefined. ○ Lore errors carried over. |
| R4.4 *Lunar Purge* | Added "pearly white skin and long, flowing blue hair" | ● Lore fix (correct). ○ Still "male Avatar of Selûne". ○ Still four beats in ~20 s with no story reason for the cure. |

### Round 5: "MCP-ready payloads" (positive / negative / camera / character ID)

| Issue | Effect |
|---|---|
| All 4 shots merged into **one** positive prompt per film | ○ One 3–15 s clip cannot carry an orbit, a strike, a shockwave and a transformation. **Regression.** |
| Negative prompts | ○ Kling 3.0 on Higgsfield has no negative-prompt field. The Origami negative ("fire, burning paper") **contradicts** its positive ("cold white flame"). |
| "Unreal Engine 5 render style, 8k" | ○ Pulls toward game-CG, against "photorealistic"; "8k" is meaningless for 720p–4k video. |
| "Character ID: [Insert User Face…]" | ○ Placeholder. The real mechanism is Soul for stills only (verified 2026-10-30), with stills then used as start frames. |
| "high motion scale" | ○ Not a parameter of any model on the account. |

**Round 5 lesson:** the format *looks* technical but would have failed in execution.

### Audit summary: what survives into v4
1. **The cure, not the kill** (R3.3): the moral and visual core.
2. **Purple-black corruption → silver mist** (R3.1, R3.3).
3. **Canon Shard appearance** (R4.4): blue hair, pearly skin, wings of light.
4. **The ECU→pull-back reveal and "fire that doesn't consume"** (R1.3): reused as *moonlight-and-fire*, which is canon for Shards [Player's Guide to Faerûn p. 154].
5. **Dropped:** porcelain masks, male avatar, kneeling, chains of light, merged payloads, negative prompts, engine names.

---

## PART B: Film 4 v4, *THE REMEMBERING* (original, ~85 s, 18 shots)

### B.1 What makes it original (not the reference)

| Reference video | v4 |
|---|---|
| A single hero speaking to camera | **Dialogue between five characters** (hero, two fallen Shards, Shar, Selûne); nobody addresses the lens |
| A litany of seven archangel names, each firing a weapon-like element | No litany. **Three-act drama** whose cure is **remembering names**; no elemental attacks |
| Black void stage with a mirror floor | **A real place:** a ruined Selûnite shrine of **seven white pillars** on a **tidal flat at low tide**, under an eclipsed moon |
| Crown of thorns, embroidered saint robe, chest gem | **Moon-pilgrim's attire:** a weathered grey-white hooded travelling cloak over silver moon-scale mail; **no crown, no gem** |
| Paper monster | **Rotting undead angels** per D&D canon; no paper (paper stays available for Film 3 if you want it) |
| Punishment → purification | **Forgetting → remembering:** the theme comes from canon, since Shar's portfolio *is* forgetfulness and loss [Faiths & Pantheons p. 58; PHB 5e pp. 62–63] |

**What I do borrow from the reference as general film craft (not its content):** the hero is a source of light; a strong scale contrast between him and the angels; a mix of intimate close-ups and very wide shots; spoken word over a choral score.

### B.2 Lore spine (every element sourced)
- Shards: seven female planetars of Selûne, chosen from her **highest-ranked priestesses**; long flowing blue hair, pearly-white skin, wings shown at will; **formed of moonlight and fire** [Faiths & Avatars p. 135; Champions of Valor p. 57; Player's Guide to Faerûn p. 154].
- Shar corrupts some Shards into **angels of decay** [Vanrakdoom p. 24]: rotting undead angels streaming liquid corruption that rots what it touches [Libris Mortis pp. 83–84]; **slurred, muddy voice** [Unclean p. 82]. They **instinctively recognise worshippers of their former deity** [Libris Mortis pp. 83–84]. **That is the hinge of our story.**
- Shar: "Mistress of the Night", "the Lady of Loss"; portfolio darkness, loss, **forgetfulness**; symbol a black disk with a deep purple border [Faiths & Pantheons p. 58; PHB 5e pp. 62–63].
- Selûne: "Our Lady of Silver", "the Moonmaiden"; her holy symbol, a pair of eyes ringed by **seven stars**; she **governs the tides** [Faiths & Pantheons p. 55; Forgotten Realms Campaign Guide p. 80].

**Invented, for story (clearly not canon):** the two Shards' mortal names, **Aelyra** and **Ysolde**, and that they once taught the hero. Canon gives the Shards no individual names, so this conflicts with nothing.

### B.3 Story in three acts
- **I · The Forgetting (0–25 s).** The moon is eclipsed by a black disk with a violet rim (Shar's symbol made literal). On a tidal flat stands a shrine of seven white pillars; **two are toppled and black**. Two angels of decay drink the moon's reflection from a tide pool, and wherever they drink, the reflection dies. Shar's voice: forgetting is a mercy.
- **II · The Recognition (25–55 s).** A lone pilgrim crosses the wet sand, the only light in the scene a soft silver glow from his open palm. He calls them by their mortal names. They don't know the names; they attack. A wave of corruption rolls across the flat and stops at his feet. Shar urges him to let them forget. He kneels and speaks the prayer they taught him as a boy. Canon: they *recognise a worshipper of their goddess*. Their violet eyes flicker silver.
- **III · Moonlight and Fire (55–85 s).** The eclipse slips. The **tide returns**, glowing silver: Selûne's tide. Where the silver water touches the angels, they ignite in **white fire that does not consume them**. Rot burns away like ash; blue hair and wings of light emerge, **moonlight and fire**, exactly what a Shard is made of. The two black pillars stand white again. A Shard opens her eyes and says **his** name: they remember him. Selûne's voice closes the film.

### B.4 Voice casting (English; to be designed with ElevenLabs Voice Design, 3 previews each, you pick)

| Character | Voice colour (description sent to the voice designer) | Delivery |
|---|---|---|
| **The Pilgrim (you)** | Adult man around 40, warm low baritone, slight natural gravel, unhurried, gentle but unbreakable; neutral international English accent; close-mic, intimate | Quiet, never shouting; the prayer almost whispered |
| **Aelyra (fallen)** | Female, low, wet and rasping, **slurred and muddy** as if speaking through water and rot; long pauses; a faint echo of a once-beautiful voice underneath | Broken phrases |
| **Ysolde (fallen)** | Female, higher and thinner, cracked whisper, trembling, with a faint childlike fear under the rasp | Overlaps Aelyra, half a beat behind |
| **Shar** | Female, deep velvet contralto, very close whisper, cold and kind at the same time, seductive calm, no reverb (she is *inside* your ear) | Slow, soothing, dangerous |
| **Aelyra and Ysolde (restored)** | The **same two voices, cleaned**: clear, bright, warm young-adult women, a subtle choral shimmer | Soft wonder |
| **Selûne** | Mature woman, luminous mezzo-soprano speaking voice, serene, ancient, motherly warmth, distant spacious reverb | One sentence only |

**Option:** if you'd rather the Pilgrim had **your real voice**, record ~1 minute of clean speech on your phone and I'll clone it (Higgsfield Create Voice) instead of designing one.

### B.5 Dialogue (complete)
1. **SHAR** *(whisper, over the eclipse)*: "Every light forgets, in the end. I only make it gentle."
2. **PILGRIM** *(calling across the sand)*: "Aelyra. Ysolde."
3. **AELYRA (fallen)**: "…no… names… here…"
4. **YSOLDE (fallen)**: "…nothing… here…"
5. **PILGRIM**: "You taught me the night prayer. On this shore. I was seven."
6. **SHAR**: "They chose to forget. Let them rest."
7. **PILGRIM** *(kneeling, palms on the sand, the prayer)*: "Lady of Silver, keep the drowned and the lost. Turn the tide. Bring them home."
8. **AELYRA (fallen)** *(confused)*: "…that… prayer…"
9. **YSOLDE (restored)** *(eyes opening)*: "…Blagoj?" *(or any name you choose for your character)*
10. **SELÛNE** *(final)*: "Nothing I love is ever truly lost."

### B.6 Shot list (18 shots ≈ 85 s)

Identity rule: **your face appears only in shots where you're alone in frame (★)**. In shared shots you're seen from behind, in silhouette, or too small to show a face. **Soul bleed cannot occur.**

| # | ★ | s | Shot (keyframe description, short form) | Motion (Kling 3.0 Pro) | Audio |
|---|---|---|---|---|---|
| 1 | | 5 | Extreme wide: tidal flat at night, wet sand mirroring the sky; the moon eclipsed by a black disk with a thin violet rim; on the horizon the shrine of seven white pillars, two toppled and black | Very slow push-in; a violet shimmer crawls round the eclipse | Shar 1 |
| 2 | | 4 | Medium: inside the shrine, two angels of decay crouched over a tide pool, drinking the moon's reflection; where their lips touch, the reflection blackens | Slow lateral track; corruption spreads through the pool | – |
| 3 | | 3 | Macro: a cracked silver priestess circlet half-sunk in black ooze; engraved letters being eaten by rot | Rot creeps over the last letters | – |
| 4 | | 5 | Wide, low: a lone hooded figure walking across the wet flat toward the shrine, a soft silver glow in his open left palm, his reflection beneath him | Tracking alongside at walking pace | ambience |
| 5 | ★ | 4 | Close-up: the Pilgrim (HERO LOCK) lowers his hood; moonlight on his scalp; looking ahead with grief and resolve | Slow push-in; breath visible in cold air | Pilgrim 2 |
| 6 | | 4 | Medium over the Pilgrim's shoulder (back of head only): both angels rise, towering half again his height, rot streaming | Angels unfold rotting wings | Aelyra 3, Ysolde 4 |
| 7 | | 4 | Wide: a black wave of corruption rolls across the flat toward the small figure | Wave surges; stops a pace from his feet; a ring of clean silver sand | – |
| 8 | ★ | 4 | Close-up: the Pilgrim, light from his palm flickering, sweat and strain, but speaking softly | Locked; the light steadies | Pilgrim 5 |
| 9 | | 3 | Insert: the black disk of the eclipse, violet rim pulsing like a heartbeat | Pulse | Shar 6 |
| 10 | ★ | 5 | Medium: the Pilgrim kneels, both palms flat on wet sand, eyes closed, praying | Slow push-in; silver light spreads from his palms into the sand | Pilgrim 7 |
| 11 | | 3 | Macro: an angel's rotted face, a beautiful woman's features beneath; violet eyes flickering silver | Eyes flicker; lips part | Aelyra 8 |
| 12 | | 4 | Extreme wide: the eclipse slips; the first edge of full moonlight breaks; far out, a silver line of returning tide | The tide line rushes in, glowing | choir rises |
| 13 | | 5 | Low wide: silver tide water washes around the angels' feet; white fire ignites on them **that does not burn** | Fire climbs their bodies; rot lifts away like ash | – |
| 14 | | 8 | **TRANSFORMATION** start = 13's end state (angels in white fire); end = Nano Banana Pro edit of start → two restored Shards (blue hair, pearly skin, wings of light), same composition | Slow 180° orbit; crust cracks and drifts up as silver ash; wings of light open | music peak |
| 15 | | 3 | Macro: Ysolde's restored face, eyes opening, silver light in them | Eyes open; recognition | Ysolde 9 |
| 16 | ★ | 4 | Close-up: the Pilgrim, tears, a small unbelieving smile | Locked; moonlight brightens his face | – |
| 17 | | 4 | Wide: the two black pillars stand white again; seven stars visible above the shrine | Slow tilt up to the seven stars and the full moon | Selûne 10 |
| 18 | | 4 | Extreme wide: three small figures on the silver tide, the moon full | Slow pull-back; fade to black | music out |

### B.7 Locks (repeat verbatim)
- **HERO (Pilgrim):** *"a man with a completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, wearing a weathered grey-white hooded pilgrim's travelling cloak over a shirt of small overlapping silver scales that shimmer faintly pale blue, a plain silver pendant of a pair of eyes ringed by seven tiny stars at his throat"*
- **ANGEL OF DECAY:** *"a gaunt undead winged angel half again the height of a man, once a beautiful priestess, rotting grey-violet skin constantly streaming thick oily purple-black liquid corruption that pools and spreads, ragged wings of rotting black feathers and bare bone, long matted hair once blue now grey-black, a cracked silver circlet, dull violet eyes"*
- **SHARD (restored):** *"a radiant female planetar with the same face now flawless, pearly-white luminous skin, long flowing blue hair drifting as if underwater, silver-glowing eyes, simple pale robes of moonlight, vast translucent wings made of light rather than feathers, a faint inner glow of moonlight over white fire"*
- **SET:** *"a ruined shrine of seven white marble pillars on a wide tidal flat at low tide, wet sand mirroring the sky, two pillars toppled and stained black"*
- **STYLE:** *"photorealistic cinematic film still, anamorphic, natural night exposure, cold silver-blue moonlight versus violet-black corruption, practical haze, fine film grain"*

### B.8 Models
| Step | Model |
|---|---|
| Your close-ups (★) | Soul Cinema + soul_id `b3ba42a8…` + mandatory head phrase |
| Everything else | Soul Cinema without soul_id |
| Transformation end frame (14) | Nano Banana Pro edit of the start frame |
| Animation | Kling 3.0 Pro, sound off (start frame; start+end frames for 14) |
| Voices | ElevenLabs Voice Design (eleven_ttv_v3) → lines rendered with Eleven v4 dialogue (multi-voice, inline emotion tags like [whispering]) |
| Score | Suno/Higgsfield music if available on the account, otherwise ElevenLabs music; choral and ambient |
| Edit and mix | ffmpeg locally (cut list, VO placement, music ducking, fade) |

**Lip-sync:** none needed. The Pilgrim speaks only in shots where his mouth isn't the focus, or the shot holds while he speaks off-screen. This avoids the most fragile step and keeps the film natural.

### B.9 Budget (live prices; voice prices to be quoted before generating)
| Item | Credits |
|---|---|
| 18 keyframes × 2 variants + 2 end-frame edits | ~45 |
| 18 Kling 3.0 Pro clips, 85 s total (~1.75 cr/s) | ~150 |
| Re-roll reserve ~25 % | ~45 |
| **Higgsfield subtotal** | **≈ 240 of ~700** |
| Voices + score | quoted separately before generating |

### B.10 What I need from you (approval gate)
1. Approve the **story and dialogue** (B.3, B.5), or change any line.
2. **The Pilgrim's voice:** designed (B.4) or cloned from your recording?
3. **The name** the restored Shard says at the climax: "Blagoj", or another name for your character?
4. Approve the **≈ 240-credit** video budget.

---

## References
- Snorri Sturluson. *Edda: Prologue and Gylfaginning*, ed. A. Faulkes. Viking Society for Northern Research, 2005, ch. 34.
- Martin, J. & Boyd, E. L. *Faiths & Avatars*. TSR, 1996, pp. 134–136.
- Boyd, E. L. & Mona, E. *Faiths and Pantheons*. WotC, 2002, p. 55 (Selûne), p. 58 (Shar).
- Baker, R., Stout, T. & Wyatt, J. *Player's Guide to Faerûn*. WotC, 2004, p. 154.
- Reid, T. M., Mearls, M. et al. *Champions of Valor*. WotC, 2005, p. 57.
- Collins, A. & Cordell, B. R. *Libris Mortis*. WotC, 2004, pp. 83–84.
- Byers, R. L. *Unclean* (The Haunted Lands, Book I). WotC, 2007, p. 82 (angel of decay's slurred, muddy voice).
- Wizards of the Coast. *Vanrakdoom* (web enhancement), p. 24.
- Crawford, J., Mearls, M. & Wyatt, J. *Player's Handbook* (5th ed.). WotC, 2014, pp. 62–63, 294 (Shar: darkness, loss, forgetfulness).
- Cordell, B. R., Greenwood, E. & Sims, C. *Forgotten Realms Campaign Guide* (4th ed.). WotC, 2008, p. 80 (Selûne and the tides).
- Higgsfield MCP model specifications and live credit prices, queried 2026-10-30.
