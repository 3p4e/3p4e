# Karsus's Folly: Wan 2.2 batch on Vast.ai (plan, 2026-11-01)

Goal: regenerate the whole film with the open stack (Wan 2.2 14B I2V + lightx2v, ComfyUI on a rented GPU) and compare with the Seedance cut (`Karsus_Folly_v3`). Same story, same dialogue, same score and mix (`aud_v3.wav`), new picture.

## 1. Scenario (canon spine, unchanged)
Netheril's flying cities hang over a sea of cloud. The phaerimm drain the land into grey desert. Karsus casts *Karsus's Avatar* to take the power of Mystryl, goddess of magic. He becomes a god for an instant, cannot hold the Weave, Mystryl dies, all magic fails, the cities fall, Karsus is turned to stone. Theme: a man who tried to save his people by taking what can only be given.

## 2. Dialogue and sound (unchanged)
SP2 Karsus: "They drink the land. River, forest, city. I have begged every god in the sky... and the sky is silent." | SP3 Karsus (whisper): "Then I will stop asking." | SP4 Mystryl: "Karsus. Put it down. You are holding everything." Karsus: "Only for a moment. Only long enough to save them." Mystryl: "A moment is all it takes." | SP5 silence, then groan of falling stone | SP6 old echo: "I only wanted to save them." | End card: "-339 DR. The year magic died." + Fan Content notice (free to watch).

## 3. Timeline to match the existing mix (`aud_v3.wav`, 102.1 s)
| Set piece | Seconds in film | Wan segments (5.06 s each) | Start frame (from our stills) | Joins |
|---|---|---|---|---|
| SP1 sky cities | 0-13.3 | 3 | sky-cities still (1.7 s into the Seedance clip) | last frame -> next start |
| SP2 grey hunger | 13.3-26.3 | 3 | top-down valley still | chain |
| SP3 ritual | 26.3-48.3 (22 s) | 5 | Karsus front still, staff and runes | chain, cut points on music hits |
| SP4 apotheosis | 48.3-63.3 (15 s) | 3 | Karsus + solid goddess still | chain |
| SP5a lights out | 63.3-71.3 | 1 first-last-frame (lit -> dark) + 3 s hold | `city_lit` and `city_dark` | FLF |
| SP5b the fall | 71.3-85.3 (14 s) | 3 | `city_dark` | chain, 1.2 s dissolve at the join |
| SP6 epitaph | 85.3-97.3 | 3 | statue clearing still | chain |
| End card | 97.3-103.3 | none | ffmpeg card | |
Total: 21 Wan clips (about 106 s raw, trimmed to fit). Inserts i1-i4 are skipped in this first batch (the v3 cut also dropped them).

## 4. Wan-ready prompts (one mover per segment, positive wording, no small objects)
- SP1 a/b/c: "The camera glides slowly forward above the cloud sea. Three white stone cities with gold domes hang motionless on inverted rock mountains. Warm sunrise light." (c adds "and finishes facing the tallest spire")
- SP2 a/b/c: "Looking straight down. A smooth even front of grey sand spreads slowly from the right, burying the green forest and the river. Only the sand moves."
- SP3 a-e: "The man stands with arms spread. Concentric rings of glowing blue-white glyphs expand slowly outward across the clouds. The camera pushes slowly in." (b-e step the sky darker, then the vortex, then lightning into the rings, as separate movers)
- SP4 a-c: "The man lifts slowly into the air with open arms. Cyan threads glow across the sky behind him. A vast calm outline of a woman made of pale light forms behind him. The camera pushes in."
- SP5a: first-last-frame, locked camera: "Every light in the city goes out at once."
- SP5b a-c: "A vast white stone city on an inverted mountain tilts slowly and drops straight down through a sea of clouds. The camera follows the fall."
- SP6 a-c: "The camera pushes slowly in through a sunlit forest clearing toward a moss-covered grey stone statue of a man with raised arms, finishing on the calm carved face."

## 5. Review: what is weak, honestly
1. The script's pipeline and budget sections (Higgsfield credits, GPT Image 2.5, Seedance 2.5) are obsolete here; the story and prompts are not.
2. Wan makes 5 s clips. A 22 s ritual becomes five seams. Chained last-frame clips drift in colour and detail. Mitigation: 1.2 s dissolves at the weakest joins and cuts on music hits.
3. Wan I2V has no end frame except the first-last-frame graph. State changes (lights out) use that; the others rely on prompt motion.
4. Known weak spots from the Seedance cut stay: SP3 started at 480p; the sky-cities towers; the goddess leaving frame; faces drop when small (SFace below 0.50 under 100 px).
5. Faces appear only in SP3, SP4 and SP6 (medium or push-in). Gate: SFace >= 0.50 on the median hero frame, worst frame reported.
6. This tests Wan as an I2V renderer from our existing stills, not as a text-to-video model. That is the realistic production path.

## 6. Batch run (one GPU session)
1. Rent a 32 GB on-demand card, load models (about 15 min, already scripted).
2. Stills are copied from this sandbox to the instance via KVM4 (private, no public repo).
3. For each segment: render at 832x480, extract the last frame, feed the next. About 60 s each, 21 clips = about 21 min.
4. Pull all clips back via KVM4; assemble with ffmpeg on the v3 timeline; reuse `aud_v3.wav`.
5. Optional second pass at 1280x720 for the best set pieces (about 185 s each).
6. Likeness check on SP3/SP4/SP6 frames against real photos; report worst frames.
7. Save to KVM4, send to you, destroy the instance only after verification.

Cost: about 0.5 h at 480p plus setup = $0.40-0.60. A full 720p pass adds about 1 h (about $0.45). Credit now $2.10.

## References
- Wan-AI. Wan2.2 (Apache-2.0). https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- Comfy-Org. Wan 2.2 repackaged files. https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged
- Zhong et al. 2021, SFace, IEEE Trans. Image Process. 30:2587-2598. DOI 10.1109/TIP.2020.3048632.
