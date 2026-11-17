# KARSUS'S FOLLY: Script v2 (story revision, 2026-11-01)

> Unofficial Fan Content permitted under the Wizards of the Coast Fan Content Policy. Not approved or endorsed by Wizards. Portions of the materials used are property of Wizards of the Coast. (c) Wizards of the Coast LLC. The film must stay free to watch.

**Format:** 16:9, about 122 s. **Hero:** Karsus, greatest archwizard of Netheril, played by Blagoj Nikolov from the authentic base face (`Blagoj-Base`). **Rule set by the author:** Karsus never leaves his tower. He stands on the high balcony of the tallest spire of his floating city for the whole film.

## 1. What changed from v1/v4 (author's direction, 2026-11-01)
1. **The "moving sand" scene is removed completely.**
2. **Replaced by the cause:** monsters from underground have climbed to the surface and are **feeding on magic**, sucking the life out of forests, rivers and lakes and turning everything into desert and sand. "They were eating the magic out of the world."
3. **Motive:** that is why Karsus steals Mystryl's power: to destroy them all in one stroke.
4. **New set piece, the wrath:** once he has the power he delivers **divine wrath**, destroying the monsters with terrible, prolific, explicit **long-shot** magic. He is on the tower the whole time.
5. **The strain:** the Weave cannot bear it. In a **blinding flash and release of enormous magic he turns to stone** on the tower. The statue falls with the city when the magic dies, and reaches the ground when the cities fall.
6. The short insert of Karsus's hands turning to stone is dropped (author disliked it).

## 2. Story spine
Netheril: human archwizards in flying cities held aloft by mythallars. Underground predators (our design, inspired by the phaerimm of canon: aberrations that feed on magic) climb to the surface and drain magic from the land, leaving grey desert. No god answers. Karsus writes *Karsus's Avatar*, which takes the divine power of Mystryl, goddess of magic. For an instant he is a god and burns the horde from the tower. He cannot hold the Weave. Flash, stone. Mystryl dies, all magic fails, the cities fall. His statue lies in the High Forest, where the town of Karse later grows.
Theme: a man who tried to save his people by taking what can only be given.

## 3. Structure (new timeline, 122.1 s)
| Set piece | Film time | Length | Content | Wan clips (5.06 s each) |
|---|---|---|---|---|
| SP1 sky cities | 0-13.3 | 13.3 | Slow glide above a cloud sea between three floating cities, ending on the tallest spire | 3 |
| SP2 the feeding (new) | 13.3-26.3 | 13.0 | Scorpion-like monsters pull glowing threads of magic out of trees and water; forest greys and collapses into dunes; desert spreads | 3 |
| SP3 the ritual | 26.3-48.3 | 22.0 | Karsus on the balcony, rings of glyphs expand across the clouds, vortex, lightning, the other cities dim as their light flows to him | 5 |
| SP4 apotheosis | 48.3-63.3 | 15.0 | The goddess made of light, beams flow into Karsus; the Weave visible; dialogue with Mystryl | 3 |
| SP4w the wrath (new) | 63.3-73.3 | 10.0 | Over his shoulder from the balcony: columns of white and golden magic fall on the desert far below and vaporise the horde; waves of golden fire | 2 |
| SP5s the strain (new) | 73.3-83.3 | 10.0 | Blinding flash, shock ring; stone spreads up his body on the balcony; he stands as a grey statue with raised arms, light dying | 2 (second is first-last-frame) |
| SP5a lights out | 83.3-91.3 | 8.0 | Every light goes out; absolute silence | 1 first-last-frame + 3 s hold |
| SP5b the fall | 91.3-105.3 | 14.0 | The cities fall through the clouds | 3 |
| SP6 epitaph | 105.3-117.3 | 12.0 | The statue in a sunlit forest, moss and roots, push-in to the stone face | 3 |
| End card | 117.3-123.3 | 6.0 | "-339 DR. The year magic died." + notice | none |
Join: 1.2 s dissolve between SP5a and SP5b (fixes the earlier glitch at the blackout-to-fall cut), 0.25 s crossfades between chained clips.

## 4. Dialogue (original English; voices already designed)
| Where | Voice | Line |
|---|---|---|
| SP2 (opening) | KARSUS V.O., low, controlled | "They drink the land. River, forest, city. I have begged every god in the sky... and the sky is silent." |
| SP3, as rings ignite | KARSUS, whisper | "Then I will stop asking." |
| SP4 | MYSTRYL, vast, gentle | "Karsus. Put it down. You are holding everything." |
| SP4 | KARSUS, straining, almost tender | "Only for a moment. Only long enough to save them." |
| SP4 | MYSTRYL | "A moment is all it takes." |
| SP4w, SP5s | none (proposal, needs your OK) | optional KARSUS, low: "Be unmade." / optional MYSTRYL at the flash: "It is too much, Karsus." |
| SP5a | none: absolute silence | |
| SP6 | KARSUS, old echo | "I only wanted to save them." |
Voices: Karsus `eRZqsCTgtEziOSM3QNPu`, Mystryl `Q3LkydeY4oUZN16c5aMd` (ElevenLabs Voice Design previews; saved-voice slots full). Existing line audio: `keyframes/karsus/voices/{K1,K2,K3,M12,M3}.wav`, echo `video/E.wav`.

## 5. Locks (repeat verbatim)
- **KARSUS LOCK:** the man from the Blagoj-Base reference, same face, completely hairless shaved head, clean-shaven, light grey-green eyes, real skin; Netherese archwizard in floor-length high-collared indigo silk robes with silver glyphs, layered dark-blue mantle with silver edging, small silver crown, silver rings on every finger.
- **MONSTER LOCK:** pale grey scorpion-like monsters the size of horses, segmented bodies, many clawed limbs, long tails, mouths ringed with writhing tendrils, drawing glowing blue-white threads of magic from trees and water.
- **ENCLAVE LOCK:** a city of white stone towers and gold domes on a gigantic inverted mountain, floating above a sea of clouds, waterfalls spilling off its edges.
- **STYLE LOCK:** photorealistic AAA game cinematic, volumetric light, natural film grain, anamorphic framing, no text.

## 6. Keyframes made for the new scenes (Gemini image API, key `BN_GEMINI_API`, model `gemini-2.5-flash-image`, `imageConfig.aspectRatio = "16:9"`)
References passed for Karsus shots: `sheet_front.png`, `A_bust.png`. Files in `keyframes/karsus/new/` (git-ignored media).
- **kf_monsters (SP2 start; later cropped 1024x1024 to 16:9):** "Photorealistic AAA game cinematic still, wide aerial view at dusk of a green forest valley with a river and a lake being devoured. Dozens of pale grey scorpion-like monsters the size of horses, segmented bodies, many clawed limbs, long tails, mouths ringed with writhing tendrils, have burst up out of the ground and are feeding on glowing blue-white threads of magic that they pull out of the trees and the water. The trees nearest the monsters are grey, dry and collapsing into sand; a wide front of pale desert dunes spreads out behind them while the far forest is still green. Cold overcast light, volumetric dust, anamorphic framing, no text, no people."
- **kf_wrath2 (SP4w start):** "...Wide shot seen from slightly behind and above. The archwizard from the reference images stands on the white marble balcony at the very top of a tall spire of a floating city high above the clouds, both arms raised toward the sky. Far below him, miles down, a vast desert plain at dusk is covered by a swarm of pale grey scorpion-like monsters. From his raised hands and from the black storm sky above, enormous columns of blinding white and golden magic fall straight down onto the desert, vaporising rows of monsters into light and ash. Apocalyptic scale, volumetric light, anamorphic framing, no text."
- **kf_stone_a2 (SP5s start):** archwizard on the white marble balcony at the top of a spire, arms spread, in the centre of a colossal blinding white-gold explosion of magic with a shockwave ring; body turning to pale grey stone from the feet and hands upward, cracks of white light, face still human, eyes closed in anguish; other white towers around.
- **kf_stone_b2 (SP5s end):** a statue carved entirely from weathered grey stone (no colour anywhere) of the archwizard, on the balcony of the spire, both stone arms raised and frozen, small cracks with fading white light, embers and white dust, the city lights behind it dimming, tragic quiet mood.
Reused stills: sky cities, Karsus front, goddess/apotheosis, `city_lit`/`city_dark`, forest statue (extracted from the earlier Seedance clips).

## 7. Wan 2.2 prompts per clip (one mover each, positive wording, no small objects)
Negative for all: "blurry, distorted, extra objects, helicopters, birds, boats, flickering, text, watermark, jitter, morphing, extra people". Each chained clip starts from the last frame of the previous one; set-piece starts and first-last-frame pairs use the stills above. The exact table is `tools/vast/batch_karsus.py` (25 segments).
- SP1 (3): "The camera glides slowly forward above a calm ocean of white clouds. Three white stone cities with gold domes hang motionless on huge inverted mountains of dark rock. The clouds stay flat and unchanged far below. Warm sunrise light."
- SP2 a/b/c: "Pale scorpion-like monsters feed on glowing threads of magic that they pull out of the trees and the river. A pale desert spreads outward from them. The camera pushes slowly forward." / "The monsters keep feeding. The green forest in front of them turns grey and collapses into sand. The camera holds steady." / "More monsters pour out of the sand across the valley while the land behind them turns to desert. The camera rises slowly."
- SP3 a-e: rings expand and camera pushes in; sky darkens into a vortex; lightning falls into the rings; distant cities dim as streams of light flow to the man; the glow becomes a blinding blue-white light.
- SP4 a-c: white light streams from the goddess into the small man in the blue cloak (camera pushes in); his arms raise and the beams flow into him; a blinding white glow fills the frame.
- SP4w a/b: "Columns of white and golden magic fall from the sky and from the man's raised hands onto the desert far below and vaporise the swarm of monsters into light. The camera holds steady." / "Waves of golden fire sweep outward across the desert far below and burn the remaining monsters to ash. The camera holds steady."
- SP5s a/b: "A blinding white flash grows around the man as grey stone spreads up his body from his feet and hands. The camera pushes slowly in." / first-last-frame to the statue still: "The man is now a grey stone statue with raised arms and the white light fades around it. The camera holds steady."
- SP5a (first-last-frame, lit to dark city): "Every light in the city goes out at once. The camera does not move."
- SP5b (3): "A vast white stone city on an inverted mountain tilts slowly and drops straight down through the sea of clouds. The camera follows the fall."
- SP6 (3): "The camera pushes slowly in through a sunlit green forest clearing toward a moss-covered grey stone statue of a man with raised arms."

## 8. Audio on the new timeline
Reuse the existing dialogue stems and score. Offsets (film seconds): K1 at 13.6; K2 at about 42.3 (16 s into the ritual); M12 at 48.6; K3 at 55.1; M3 at 61.0 (as in the v5 mix); silence from the first frame of SP5a (83.3) to the dissolve (about 90.1); the old-echo line and the theme reprise start with SP6 (105.3 minus 1.2 for the dissolve = 104.1). The score needs about 20 s more than the existing 100.1 s: loop the climax (score 55.3-60 s) over the wrath, with a 0.3 s crossfade, and mute it at the flash for the hard silence. The proven ffmpeg graph is in the handover file (section "Audio mix recipe").

## 9. Review: honest assessment
Strengths: the new causal chain fixes the weakest part of v1 (why Karsus does it); the wrath and the stone give two big visual payoffs; Karsus on the tower keeps him small and the faces safe.
Weaknesses and risks:
1. **Wan has never been tested on monster swarms or fire waves.** Expect one regeneration of SP2 and SP4w.
2. **Chained clips drift** (colour, detail) and restart motion every 5 s. Mitigation: crossfades, cuts on music hits.
3. **16 fps source** converted to 24 fps without frame interpolation: slight judder.
4. **The statue "falls to the ground" is implied** (it falls with the city, lands in SP6), not shown as a shot. If you want an explicit fall shot, add one first-last-frame clip.
5. **Faces are small or absent** in the new scenes, so likeness risk is low; SP3 and SP6 are the checks.
6. Canon: Mystryl's death and the fall of the cities are canon; the monsters feeding on magic loosely follow the phaerimm; the wrath and the flash are original.

## 10. Status (end of session)
Done: story v2, 4 new keyframes, 25-clip manifest, assembler tested on dummy clips, handover written. **Not done:** the GPU batch itself. The Vast run was stopped at the author's request while models downloaded slowly (about 6.5 MB/s on that host). The instance was stopped, not destroyed.
