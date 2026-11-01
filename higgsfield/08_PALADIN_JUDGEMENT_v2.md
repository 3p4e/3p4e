# The Paladin's Judgement v2: open-source batch (Wan 2.2 + FLUX.2 klein)

Source: Block 1 of `02_PRODUCTION_PROMPTS.md` (Gemini draft). Review date 2026-11-01.
Target stack: rented GPU on Vast.ai, ComfyUI, **Wan 2.2 14B I2V** (Apache-2.0, tested: 55-185 s per 5 s clip, face likeness held at SFace 0.51-0.57 on Karsus), keyframes with **FLUX.2 klein 4B** (Apache-2.0, ungated). Fan content, not monetised.

## 1. Review: what is wrong with v1

| # | Problem | Why it matters on this stack | Fix in v2 |
|---|---|---|---|
| 1 | Every shot stacks 3-4 movers (snow streaming + fur whipping + dolly + runes brightening + head raising) | Wan/Seedance obey one clear mover and smear the rest (our Karsus rule 1) | **One mover per shot**: camera OR subject OR light |
| 2 | Shots are 6-8 s | Wan I2V is 81 frames = 5.06 s at 16 fps | All clips 5 s; 1.4 is one FLF clip |
| 3 | 1.3 has two subjects: hero glowing + skeleton king recoiling in the background | Two movers, soft-focus second subject morphs | Hero only; the king's reaction moves into 1.4 |
| 4 | 1.2 has a 3 m skeleton striding while dragging a sword | Locomotion and foot contact fail in I2V; sword-in-ice trail is a small-object effect | Low-angle, king nearly still, slow forward lean; camera does the work |
| 5 | 1.4 asks for a 180 deg orbit, an expanding ring, and a burning king in one 8 s clip | Camera + ring + burn = three movers; no model does this reliably | Start/end frames carry the change (first-last-frame); static wide camera; ring bursting in keyframe A, ash column in keyframe B |
| 6 | Hero locked as bald + ginger-brown moustache + stubble | Our authentic base (`Blagoj-Base`) is clean-shaven; you asked for that earlier | Default: clean-shaven bald, light stubble optional (decision below) |
| 7 | "Use my soul_id" | Higgsfield-only; not available here | Reference-image edit from `Blagoj-Base` + SFace gate |
| 8 | No reason the light kills the king | Same weakness we fixed in Karsus | One beat: the iron crown is the source; the light burns it first (ends as the fallen crown in keyframe B) |
| 9 | Silent | Film needs sound to read as finished | Procedural wind, drone, impact hit and ember hiss from ffmpeg (no model, no cost); music optional later |
| 10 | Two lock-text blocks repeated in every prompt | Long prompts dilute the one instruction | Keyframe prompts keep the lock; motion prompts stay under 40 words |

## 2. v2 shot list (20 s)

Rules: positive wording, one mover, concrete counts, no small objects (no birds, sparks as objects, banners), faces only in medium or close shots, no hand gestures unless requested (the Karsus close-up grew hands).

**HERO LOCK (v2):** "a broad-shouldered man, completely shaved bald head, clean-shaven, weathered skin, calm grave eyes, wearing heavy articulated silver plate armour with gold runes along the pauldrons and breastplate, a thick white wolf-fur mantle, a long white tabard with a gold sunburst, a two-handed warhammer with a gold-inlaid square head"
**KING LOCK:** "a towering skeletal king, blackened bones in rusted frost-rimed plate, a jagged iron crown fused to the skull, hollow eye sockets glowing pale cyan, ribcage lit sickly green, a rune-etched broadsword"
**STYLE LOCK:** "photorealistic cinematic still, anamorphic framing, shallow depth of field, volumetric backlight through blizzard, film grain, muted steel-blue grade, warm gold only from the hero"

| Shot | Time | Keyframe(s) | Motion prompt (one mover) |
|---|---|---|---|
| 1.1 hero wide | 5 s | Wide shot, hero standing on a glacier ridge, head bowed, both hands on the hammer haft, snow settling | "Camera slowly pushes in toward the man. He stands completely still." (mover: camera) |
| 1.2 king | 5 s | Low-angle, king standing in the blizzard, sword point in the ice, green ribcage light | "The camera holds low and still. The king slowly raises its head." (mover: head) |
| 1.3 hero medium | 5 s | Medium shot, hero's head raised, gold light from the chest runes, calm | "The gold light from his chest slowly brightens. The camera does not move." (mover: light) |
| 1.4 judgement | 5 s | FLF: A = hammer striking the ice, gold ring bursting, king 3 m away. B = same framing, hero kneeling in a circle of gold runes, column of ash and a fallen iron crown, shaft of sunlight | First-last-frame, static wide camera, "the golden ring spreads across the ice and the king burns to ash" (change carried by the end frame) |

Order and timing: 1.1 (5 s) > 1.2 (5 s) > 1.3 (5 s) > 1.4 (5 s). Hard cuts. Sound: wind bed throughout, low drone rising through 1.3, impact hit + ember hiss on 1.4.

## 3. Batch design (one GPU session, no human steps)

1. Rent on-demand 32 GB card (about $0.41/h), start ComfyUI.
2. Download once: Wan 2.2 14B I2V fp8 + lightx2v LoRAs (38 GB, already scripted), FLUX.2 klein 4B (about 12 GB) and its text encoder and VAE.
3. **Keyframes**: 4 seeds per keyframe (A+B for 1.4). Hero shots via reference edit from the `Blagoj-Base` render. Best seed picked by SFace against the base render (no real photos go to the GPU).
4. **Video**: Wan 2.2 I2V per shot at 832x480 (draft), then 1280x720 for the winner; FLF graph for 1.4.
5. Return keyframes and clips to KVM4 over SSH, pull here, run the real-photo likeness check on all hero frames.
6. Assemble with ffmpeg (cuts, grade, procedural sound), save to KVM4 and send to you.
7. Destroy the instance only after the files are verified.

Quality gates: hero keyframe SFace >= 0.50 vs the base render, then >= 0.50 vs real photos on the final frames (worst frame reported). Any clip with new objects (people, birds, vehicles) is regenerated with a new seed, once.

## 4. Risks (honest)

- FLUX.2 klein 4B reference editing may not hold identity as well as Qwen-Image-Edit-2511 (20 GB, also Apache-2.0). The seed gate will tell; fallback is Qwen.
- Node names for FLUX.2 klein and Wan first-last-frame in ComfyUI 0.43 are unverified; the preflight prints mismatches and I adjust through the job channel.
- A skeleton king is far from our tested face scenes: expect one regeneration.
- 5 s per shot: no continuous action across a cut.

## 5. Cost estimate

About 1.5-2 GPU hours at $0.41/h = $0.60-0.85, plus storage. Credit now $2.10.

## References

- Wan-AI. Wan2.2 (Apache-2.0). https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- Black Forest Labs. FLUX.2 [klein] 4B (Apache-2.0). https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
- Comfy-Org. Wan 2.2 and FLUX.2 klein repackaged files. https://huggingface.co/Comfy-Org
- Zhong et al. 2021, SFace, IEEE Trans. Image Process. 30:2587-2598. DOI 10.1109/TIP.2020.3048632.
