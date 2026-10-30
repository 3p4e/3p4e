# Production prompts: four films for Claude Code + Higgsfield MCP

**Hero:** Blagoj Nikolov (trained Soul Cinema identity)
**Format:** 16:9, 4 shots per film, 5–8 s per shot, ~25–30 s per film, silent (score added in post)
**Background reasoning:** see `01_REVIEW_gemini_chat.md`
**Identity (verified 2026-10-30):** Soul Cinema `b3ba42a8-305b-465a-b867-83432e48687c`. The Soul fixes the **face** only. Without an explicit description it invented hair, including long hair and earrings. So every HERO LOCK must keep the phrase *"completely shaved bald head, short ginger-brown moustache and light stubble, eyes open"*. Smoke test with it: likeness 0.87 / 0.86 (without it: 0.79 / 0.74 and wrong hair). See `IDENTITY.md`.

You can paste each block below into Claude Code as written. Block 0 runs once. Blocks 1–4 each produce one film.

---

## How every shot is made (read once)

The face is fixed in the **still image**, not in the video. So each shot is two calls:

1. **KEYFRAME**: `generate_image`, model `soul_cinematic`, with your `soul_id` whenever the hero is in frame. This prompt describes **appearance**: who, what they wear, where, light, lens.
2. **MOTION**: `generate_video`, model `kling3_0`, using the keyframe as `start_image`. For transformation shots, a second keyframe is the `end_image`. This prompt describes **only movement and camera**, because the image already carries the look. Re-describing the look in the motion prompt makes the model redraw the face, and that is how likeness drifts.

**Prompt rules applied below:**
- Positive phrasing only. Kling 3.0 has no negative-prompt field, so "no X" is written as "only Y".
- One camera move per shot.
- Each character has a LOCK block that is repeated word for word in every keyframe.
- No engine names ("UE5") and no fake resolutions ("8k").

---

## BLOCK 0: Identity setup (run once)

```text
TASK: Train my Soul Cinema identity on Higgsfield and prepare the QC baseline.

1. My photos are in ./faces/ (do NOT commit them; .gitignore covers it).
   ALREADY DONE 2026-10-30: soul_id b3ba42a8-305b-465a-b867-83432e48687c (ready, smoke test passed).
   Skip to the film blocks unless retraining. To retrain, run:
   bash tools/fetch_models.sh
         python3 tools/face_qc.py dataset ./faces ./face_dataset
   Show me the QC report (face_dataset/qc_report.csv): every REJECT/SPARE with its reason,
   and the yaw spread. If fewer than 15 photos are SELECTED, stop and tell me what kind of
   photos to add (angle, lighting) instead of training on a weak set.

2. Check my credit balance (balance tool) and report it before spending anything.

3. Upload the SELECTED 1024px crops from ./face_dataset/ with media_upload -> PUT bytes ->
   media_confirm. Collect the media_id UUIDs.

4. Train: show_characters  action=train  type=soul_cinematic  name="Blagoj"  images=[all media_ids]
   Wait until status=ready (about 10 min). Report the soul_id.

5. Identity smoke test: generate_image model=soul_cinematic soul_id=<id> aspect_ratio=16:9 quality=2k
   prompt: "Cinematic medium close-up portrait of a man, neutral expression, soft overcast
   daylight from camera left, plain dark grey backdrop, 85mm lens, natural skin texture."
   Generate 2 variants, download them to ./keyframes/_smoketest/ and run
         python3 tools/face_qc.py verify ./face_dataset ./keyframes/_smoketest
   Pass criterion: both >= 0.50. If not, stop and report; do not continue to the films.

Rules for all later blocks:
- Download every keyframe to ./keyframes/<film>/<shot>/ and run face_qc.py verify on hero
  keyframes. Only a keyframe scoring >= 0.50 may go on to video. Show me the 2-4 candidates
  and scores, and let me pick unless one is clearly best.
- Before each film, state the estimated credit cost and wait for my OK.
- Video defaults: generate_video model=kling3_0 mode=pro sound=off aspect_ratio=16:9.
  Fallback if Kling rejects or quality is poor: model=cinematic_studio_3_0 genre=epic
  resolution=1080p with the same start/end images.
```

---

## BLOCK 1: *The Paladin's Judgement* (Warcraft-inspired, no trademarks)

**Logline:** On a glacier under a killing blizzard, a lone holy warrior faces a skeletal frost-king. He doesn't charge. He consecrates the ground, and the king burns.
**Palette:** blizzard steel-blue and black; necrotic sick-green from the king; the warrior's light is **warm gold**, the only warm colour in the film.

```text
FILM 1 — THE PALADIN'S JUDGEMENT. Use my soul_id for every shot marked HERO.

HERO LOCK (repeat verbatim in every HERO keyframe):
"a broad-shouldered man, completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, snow settling on his scalp,
wearing heavy articulated silver plate armour with deep-etched flowing golden runes along
the pauldrons and breastplate, a thick white wolf-fur mantle over the shoulders, a long
weathered white tabard with a gold sunburst, a massive two-handed warhammer with a
gold-inlaid square head"

ANTAGONIST LOCK:
"a towering skeletal king, three metres tall, blackened bones bound in rusted frost-rimed
plate, a jagged iron crown fused to the skull, hollow eye sockets glowing pale cyan, an
exposed ribcage pulsing with sickly green necrotic light, dragging a huge rune-etched
broadsword whose blade steams with cold"

STYLE LOCK (append to every keyframe):
"photorealistic cinematic still, anamorphic 2.39 framing inside 16:9, shallow depth of
field, real snow particles, volumetric backlight through blizzard, rich film grain,
practical-effects realism, muted steel-blue grade"

SHOT 1.1 — HERO — 6 s
KEYFRAME: "Wide shot, eye level. [HERO LOCK] stands alone on a shattered glacier ridge,
hammer head resting on the ice, both hands on the haft, head bowed against a violent
blizzard. Cracked blue ice plates around his boots, snow streaming horizontally left to
right, a faint warm glow leaking from the runes of his breastplate. [STYLE LOCK]"
MOTION: start_image=1.1 | "Slow steady dolly-in toward the man. Snow streams horizontally
across frame, his fur mantle whips in the wind. He slowly raises his head and looks
straight ahead. The runes on his armour brighten slightly. Camera stays at eye level."

SHOT 1.2 — no hero — 6 s
KEYFRAME: "Low-angle side shot close to the ice. [ANTAGONIST LOCK] strides through the
blizzard, the broadsword tip carving a glowing frost trail in the glacier. Green light from
the ribcage lights the snow around it. [STYLE LOCK]"
MOTION: start_image=1.2 | "Low tracking shot moving left to right alongside the striding
skeletal king, one continuous pass. The sword tip drags through the ice throwing frost
sparks. Heavy footsteps crack the ice. Snow whips past the lens."

SHOT 1.3 — HERO — 6 s
KEYFRAME: "Medium shot, chest height. [HERO LOCK] raises his left gauntlet, palm open
toward camera, calm and resolved. Warm gold light radiates from his chest runes and his
eyes, cutting a visible shaft through the blizzard. In the soft-focus background the
skeletal king recoils, raising a bony arm against the light. [STYLE LOCK]"
MOTION: start_image=1.3 | "Slow push-in toward the man's face. The gold light from his
chest intensifies and spreads, shafts of light cutting through falling snow. In the
background the skeletal king staggers back shielding its skull. The man's expression
stays calm."

SHOT 1.4 — HERO — 8 s — TRANSFORMATION (start + end image)
KEYFRAME A (start): "Wide low-angle shot. [HERO LOCK] brings the warhammer down onto the
ice with both hands at the moment of impact, a ring of golden holy light just bursting
from the strike point. The skeletal king stands three metres away, mid-lunge. [STYLE LOCK]"
KEYFRAME B (end): "Same wide low-angle composition. [HERO LOCK] kneels on one knee, hammer
head planted in a glowing circle of golden runes burned into the ice. Where the skeletal
king stood, only a drifting column of glowing embers and ash and a fallen iron crown.
The blizzard has parted, a shaft of pale sunlight falls on him. [STYLE LOCK]"
MOTION: start_image=1.4A end_image=1.4B | "Slow 180-degree orbit around the man as the
hammer strikes. A perfect ring of golden fire expands outward across the ice in slow
motion, reaching the skeletal king and burning it from the feet upward into glowing ash
that spirals away in the wind. The blizzard is pushed back by the shockwave."
```

---

## BLOCK 2: *Gleipnir: The Pledge of Týr* (Norse myth, faithful to *Gylfaginning* ch. 34)

**Logline:** Two iron chains already lie shattered. To bind the wolf that will one day devour the gods, Týr, played by you, places his right hand in the beast's jaws as a pledge of good faith while a ribbon thin as silk tightens around it. The film cuts to black before the bite. The audience knows what it cost.
**Palette:** storm-grey and black water, silver mist, the ribbon's faint pearl-gold glow. Grim, not hellish.

```text
FILM 2 — GLEIPNIR: THE PLEDGE OF TÝR. Use my soul_id for every HERO shot.

HERO LOCK:
"a tall man, completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, weathered skin, wearing a dark iron-ringed mail shirt over blackened
leather stamped with interlaced Norse knotwork, a heavy brown bearskin cloak clasped with
a bronze ring-brooch, no helmet, bare forearms with faded runic tattoos, calm grave eyes"

WOLF LOCK:
"a colossal grey-black wolf the size of a longhouse, matted storm-soaked fur, scarred
muzzle, enormous yellow eyes with intelligent malice, steaming breath, lips pulled back
over teeth like spearheads"

RIBBON LOCK:
"Gleipnir, a ribbon as thin and smooth as silk, faintly luminous pale gold, impossibly
fine, wound many times around the wolf's legs and neck"

STYLE LOCK:
"photorealistic cinematic still, overcast storm light, cold silver mist over black water,
wet textures, natural colour, heavy atmosphere, film grain, historically grounded Viking
Age materials"

SHOT 2.1 — no hero — 6 s
KEYFRAME: "Wide establishing shot of a small barren black-rock island, Lyngvi, in a dark
lake, Ámsvartnir, under a churning storm sky. On the shore lie two enormous shattered iron
chains, links burst open. In the mist beyond, the silhouette of [WOLF LOCK] pacing.
[STYLE LOCK]"
MOTION: start_image=2.1 | "Slow chest-height dolly forward across the wet rocks past the
broken iron chains. Mist rolls over the black water. In the distance the giant wolf turns
its head toward camera, eyes catching the light."

SHOT 2.2 — HERO — 6 s
KEYFRAME: "Medium-wide shot. [HERO LOCK] walks out of the mist along the shore, holding a
coiled length of [RIBBON LOCK] loosely in his left hand. His expression is stoic, knowing.
Wind pulls at the bearskin. [STYLE LOCK]"
MOTION: start_image=2.2 | "Slow dolly-in as the man walks steadily toward camera. The fine
golden ribbon trails from his hand and flutters in the wind. Mist swirls around his legs.
He does not break stride."

SHOT 2.3 — HERO — 7 s
KEYFRAME: "Over-the-shoulder shot from behind the man. [HERO LOCK] stands before
[WOLF LOCK] whose head looms above him, jaws half open, snarling. The man extends his bare
right arm forward, hand open, toward the wolf's mouth. [STYLE LOCK]"
MOTION: start_image=2.3 | "Over-the-shoulder follow at walking pace as the man steps
forward. The wolf snaps its jaws a hand's width from his chest, spittle flying in slow
motion, then pauses, studying him. The man slowly places his open right hand between the
wolf's teeth. Stillness."

SHOT 2.4 — HERO + WOLF — 8 s — TRANSFORMATION (start + end image)
KEYFRAME A (start): "Medium shot, slightly low angle. [HERO LOCK] stands with his right
hand resting inside the jaws of [WOLF LOCK]. [RIBBON LOCK] lies loosely around the wolf's
legs and neck. The man's face is utterly calm, eyes closed. [STYLE LOCK]"
KEYFRAME B (end): "Same composition. The wolf strains with all its strength, every muscle
taut, [RIBBON LOCK] now pulled tight and blazing pale gold, cutting into the fur, the wolf
pinned low to the rocks. The man's hand is still in its jaws, his eyes open, jaw clenched,
accepting. [STYLE LOCK]"
MOTION: start_image=2.4A end_image=2.4B | "Slow push down toward the man and the wolf. The
wolf feels the ribbon and begins to struggle, thrashing; the thin golden ribbon tightens
with every pull and glows brighter, pinning the beast to the rocks. The wolf's eyes turn
to the man. The man opens his eyes and holds its gaze. Hard cut to black at the end."
(Post: end on 1 s of black + the sound of jaws closing. Never show the injury.)
```

---

## BLOCK 3: *The Origami Ascension* (paper seraph against living ink)

**Logline:** In an endless void a seraph made of folded parchment stands as the only light. A many-armed thing of living ink crawls toward him, staining what it touches. He doesn't burn. He **re-folds** himself clean and answers with a storm of folded light.
**Palette:** pure black void, warm ivory parchment, cold white flame. The ink is matte black with an oily iridescent sheen.

> ⚠️ I haven't seen your reference screenshot of the paper seraph. Attach it to this block. Claude Code should upload it and create a **Reference Element** (`category: prop` or `character`) for the paper costume, then add `<<<element_uuid>>>` to the keyframes. This only works with Nano Banana Pro or Seedream, because Soul Cinema accepts 1 image reference. Alternatively, pass it as the single `medias` image in Soul Cinema. Without it, the text below has to carry the look.

```text
FILM 3 — THE ORIGAMI ASCENSION. Use my soul_id for every HERO shot.
If I attached the seraph reference image: upload it and pass it as the image reference in
the hero keyframes.

HERO LOCK:
"a male seraph with his own human face, completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, natural skin, serene gaze; from
the neck down his entire body and armour are made of immaculate folded ivory parchment —
crisp geometric origami plates forming pauldrons, breastplate and a long pleated robe;
six enormous wings built from hundreds of layered folded-paper feathers, each with sharp
creases and visible paper fibre; a thin crown of folded paper thorns glowing pale blue"

ANTAGONIST LOCK:
"a sprawling multi-armed entity of living black ink, liquid and glossy with an oily
iridescent sheen, its limbs dripping and re-forming, its surface crawling with fragments
of decaying handwritten script that smear and bleed"

STYLE LOCK:
"photorealistic macro cinematography, absolute black void, single soft key light from
above, extreme detail of paper fibre and folds, high contrast, shallow depth of field,
subtle floating dust motes"

SHOT 3.1 — HERO — 7 s
KEYFRAME: "Medium shot. [HERO LOCK] stands in an endless starless void, wings folded,
eyes lowered, the only illuminated object in existence. [STYLE LOCK]"
MOTION: start_image=3.1 | "Begin as an extreme macro close-up on the folded paper
feathers, creases sharp, paper fibre visible, then a slow continuous pull-back revealing
the seraph standing in the void. He raises his eyes to the camera. The feathers rustle
softly like turning pages."

SHOT 3.2 — no hero — 6 s
KEYFRAME: "Low wide shot. [ANTAGONIST LOCK] crawls across an invisible floor toward a
distant point of white light, ink pooling and spreading in its wake. [STYLE LOCK]"
MOTION: start_image=3.2 | "Low tracking shot alongside the ink entity as it crawls
forward, limbs splitting and re-forming, droplets of ink falling upward, handwritten
script sliding across its skin. Steady pace."

SHOT 3.3 — HERO — 7 s
KEYFRAME: "Medium-wide lateral shot. [HERO LOCK] spreads all six wings fully; one lower
wing tip is stained black where ink has touched it. Along every feather edge burns a cold
white flame that does not consume the paper. [STYLE LOCK]"
MOTION: start_image=3.3 | "Slow lateral track along the seraph as he spreads his wings.
The stained feathers unfold flat, then re-fold themselves clean and white, the ink sliding
off in drops. A cold white flame ignites along every feather edge and the paper stays
whole. Light intensifies."

SHOT 3.4 — HERO — 8 s — TRANSFORMATION (start + end image)
KEYFRAME A (start): "Wide shot. [HERO LOCK] with wings fully extended and blazing white,
right hand raised; [ANTAGONIST LOCK] rears up before him, arms spread to engulf.
[STYLE LOCK]"
KEYFRAME B (end): "Same wide composition. [HERO LOCK] stands alone, wings lowering; where
the entity was, a slow cloud of glowing white paper dust and drifting folded paper cranes
hangs in the void. [STYLE LOCK]"
MOTION: start_image=3.4A end_image=3.4B | "Locked shot holding still for one second, then
a straight track forward. The seraph releases a storm of thousands of folded paper blades
and paper cranes edged in white light that pierce the ink entity. The ink turns white
where it is struck, and the entity crumbles into glowing paper dust that drifts upward."
(Alternative weapon if you prefer Gemini's original: replace "folded paper blades and
paper cranes" with "crystalline geometric shards".)
```

---

## BLOCK 4: *The Lunar Purge* (Forgotten Realms, faithful to canon)

**Lore spine (sourced in the review, R2–R9):**
- The **Shards** are seven female planetars of Selûne, former high priestesses. They have long flowing blue hair, pearly-white skin, and wings they can show or dismiss, and they are formed of moonlight and fire.
- **Shar** sometimes corrupts Shards into **angels of decay**. These are ~2.7 m winged undead that constantly rot and stream liquid corruption, which pools around them and rots living things. They **instinctively recognise a worshipper of their former deity**.
- Selûne's holy symbol is two feminine eyes ringed by **seven stars**, one for each Shard. In this film **two of the stars are dark**, and they reignite at the end.
- Your role is a mortal **Moonsworn champion**. You wear *Selûne's scale mail*, opalescent circular scales glowing faintly silver, which she lends to those on a quest for her. You carry a four-flanged heavy mace made in the image of her *Rod of Four Moons*. **The goddess herself appears only as a vast feminine presence in the moon.**

**Logline:** In a cathedral Shar has drowned in shadow, two fallen Shards feed on rot. A Moonsworn champion comes to purge them. They recognise their own faith in him and hesitate. He doesn't strike them. He strikes the floor, and moonlight remembers them.
**Palette:** Shar = black and deep violet; corruption = oily purple-black; Selûne = silver, pearl, pale blue. No warm light until the final restored glow, which is a soft moon-white.

```text
FILM 4 — THE LUNAR PURGE. Use my soul_id for every HERO shot. The two Shards are
fictional; do NOT use my soul_id for them.

HERO LOCK:
"a man, completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, wearing asymmetric armour of
opalescent circular silver scales that glow faintly with moonlight — a full scale-mail
hauberk with a single sculpted crescent-moon pauldron on the left shoulder — over flowing
layered silks of deep midnight blue shot through with tiny points of starlight; on his
chest a silver disc engraved with two serene feminine eyes ringed by seven small stars,
five glowing and two dark; he carries a heavy four-flanged silver mace whose head is
shaped like four crescent moons, pulsing with pale blue light"

ANGEL OF DECAY LOCK (x2):
"a nine-foot gaunt winged undead angel, once female, rotting grey-violet flesh constantly
sloughing and streaming thick oily purple-black liquid corruption that pools around it,
ragged wings of rotting black feathers and exposed bone, long matted hair that was once
blue now grey-black and slick, the ruined remains of a silver priestess circlet on its
brow, a face still recognisably that of a beautiful woman beneath the decay, eyes glowing
dull violet"

RESTORED SHARD LOCK (x2):
"a radiant female planetar, the same face now flawless, pearly-white luminous skin, long
flowing blue hair moving as if underwater, eyes of soft silver light, wearing flowing
pale robes of moonlight with fine silver filigree, vast translucent pearlescent wings of
light, a silver circlet on her brow, her body glowing like moonlight and banked white fire"

SET LOCK:
"a vast ruined Gothic cathedral overgrown with creeping black thorns, shattered rose
window, columns wrapped in violet-black shadow, a desecrated altar, floor flooded with a
shallow pool of oily purple-black corruption, moonlight barely reaching through"

STYLE LOCK:
"photorealistic cinematic still, dark-fantasy realism, moonlight volumetrics, wet
reflective surfaces, deep violet-black shadows with silver highlights, film grain,
practical-effects realism"

SHOT 4.1 — no hero — 7 s
KEYFRAME: "Low-angle wide shot. [SET LOCK]. Two [ANGEL OF DECAY LOCK] crouch over the
altar, wings half spread, corruption pooling and spreading across the floor; thorns near
the pool wither and blacken. [STYLE LOCK]"
MOTION: start_image=4.1 | "Low-angle tracking shot gliding forward between thorn-wrapped
columns toward the altar. The two decayed angels feed hunched over the altar; liquid
corruption streams from their bodies and spreads across the floor; their rotting wings
twitch. Dust and ash drift through faint moonbeams."

SHOT 4.2 — HERO — 7 s
KEYFRAME: "Medium-wide shot from the cathedral floor looking up. [HERO LOCK] descends
slowly through the shattered rose window in a column of pale moonlight; behind him, in
the full moon framed by the broken window, the faint luminous outline of a vast serene
woman's face with long ivory hair, watching. His expression is sorrowful resolve.
[STYLE LOCK] [SET LOCK]"
MOTION: start_image=4.2 | "Slow dolly-in as the man descends through the column of
moonlight and lands softly on the flooded floor; the corruption pulls back from his feet
in a ring of clean stone. His silks settle. The mace head pulses pale blue. Behind him the
woman's face in the moon slowly fades."

SHOT 4.3 — HERO — 7 s
KEYFRAME: "Medium shot, chest height, facing the man. [HERO LOCK] stands firm as the two
[ANGEL OF DECAY LOCK] lunge toward him from both sides wielding blades of condensed violet
shadow — but both have frozen mid-lunge, violet eyes fixed on the seven-star symbol on his
chest, recognising it. [STYLE LOCK]"
MOTION: start_image=4.3 | "Slow push-in toward the man. The two decayed angels lunge at
him with shadow blades, then falter and halt a metre away, staring at the seven-star
symbol on his chest, their heads tilting as if remembering. The man lowers the mace and
in one motion slams its haft down into the stone floor."

SHOT 4.4 — HERO + 2 — 10 s — TRANSFORMATION (start + end image)
KEYFRAME A (start): "Wide shot at floor level. [HERO LOCK] kneels on one knee, mace haft
planted in the stone, a shockwave of crystalline silver moonlight bursting outward from
the impact; the two [ANGEL OF DECAY LOCK] caught in the wave, corruption beginning to
boil off them as silver mist. [STYLE LOCK] [SET LOCK]"
KEYFRAME B (end): "Same wide composition. [HERO LOCK] rises to his feet. Before him the two
[RESTORED SHARD LOCK] kneel with heads bowed, translucent wings spread, bathing the
cathedral in soft moonglow; the black thorns have turned to pale silver vines, the
corruption pool is now clear water reflecting the moon; on his chest all seven stars
glow. [STYLE LOCK]"
MOTION: start_image=4.4A end_image=4.4B | "Slow sweeping 180-degree orbit around the three
figures in slow motion. The silver shockwave washes over the two decayed angels; the
rotting crust cracks and shatters off them in flakes that dissolve into silver mist,
revealing pearly-white skin, blue hair unfurling, rotting feathers replaced by
translucent pearlescent wings of light. They sink to their knees before the man. The
darkness of the cathedral recedes as moonglow fills the vault; the two dark stars on his
chest ignite."

OPTIONAL SHOT 4.5 — HERO + 2 — 5 s — coda (Kling 3.0 start image = 4.4B)
MOTION: "Slow crane up and back away from the three figures. One Shard raises her head and
looks at the man with recognition and gratitude; the other folds her wings. Moonlight
pours through the shattered rose window."
```

---

## Post-production (Claude Code can do this locally with ffmpeg)

```text
For each film: upscale each accepted clip with upscale_video if under 1080p, then
concatenate shots in order with 8-frame crossfades only between 1.2/1.3-type cuts (hard
cuts elsewhere), add 1 s black head and tail, export H.264 1080p 24 fps, CRF 18:
  ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 18 -r 24 -pix_fmt yuv420p out.mp4
Optional score: generate_audio (orchestral, choir, 30 s, mood per film) and mux it in.
```

## Acceptance criteria (QC before you call a film "done")

| Check | Limit |
|---|---|
| Hero identity per keyframe (`face_qc.py verify`) | ≥ 0.50 cosine; 0.363–0.50 = re-roll |
| Identity in motion | Extract 1 frame/s (`ffmpeg -vf fps=1`) and verify. No frame with the hero's face visible may score < 0.363. |
| Anatomy | 5 fingers, no fused weapons and hands, wings attached at the shoulder blades |
| Continuity | Armour, cloak and weapon identical across shots (compare against the LOCK block) |
| Lore (Film 2/4) | Ribbon thin, not chains; Shards female with blue hair and pearly skin; seven stars on the symbol |
