# Review of the Gemini conversation: what holds up and what doesn't

**Prepared for:** Blagoj Nikolov
**Date:** 2026-10-30
**Scope:** The four cinematic scenarios, the prompt formats Gemini proposed, the identity ("face") workflow, and the AI model advice. Every technical claim was checked against the live Higgsfield MCP tool specifications in this session [R1]. Every lore claim was checked against the published sourcebooks, with page numbers [R2–R12].

---

## 1. Verdict

Gemini got the **creative direction** right. It wrote evocative imagery and reasonable camera language, and it caught the Elune/Selûne name mix-up. Its **technical advice is the weak part**, and three of its errors would have cost you credits or produced unusable output:

| # | Gemini claim | Reality | Severity |
|---|---|---|---|
| 1 | "Append `--soul-id` to the generation requests… bakes your face into the paladin, Norse god and seraph" (video) | A trained Soul works **only with the image models `soul_2` and `soul_cinematic`** [R1]. No video model accepts a `soul_id`. Your face has to reach the video through a **keyframe still (start image)** or a **Reference Element**. | Critical: the pipeline as described does not exist |
| 2 | The final "MCP-ready payloads" merged all 4 shots into **one** positive prompt per scenario | A video call returns one 3–15 s clip [R1]. If you pack orbit + push + strike + incineration into one clip, you get mush. This version was a **regression** from Gemini's own shot lists. | Critical |
| 3 | "Soul ID: gather 20 to 80 photos" | Soul training accepts **5–20 images** [R1]. Anything over 20 is ignored or rejected, so you have to curate rather than send everything. | High |
| 4 | Negative prompt fields for every scenario | Kling 3.0 on Higgsfield has **no negative-prompt parameter** [R1]. The paper-seraph negatives also said "*fire, burning paper*" while the positive prompt asked for "*cold white flame*". The prompt was arguing with itself. | High |
| 5 | "Flux.2 bakes your character into the model weights" | Not available through Higgsfield. Flux LoRAs live on other platforms, and **no Higgsfield video model can load a LoRA**. | Medium |
| 6 | "Unreal Engine 5 render style, 8k resolution" next to "photorealistic" | These conflict. "UE5" pulls toward game-engine CG, and "8k" does nothing for a 720p–4k video model. Keyword soup dilutes the prompt. | Medium |
| 7 | "Higgsfield cinema camera:" prefix | This is not a parameter. It's harmless filler, but it uses up prompt attention. | Low |
| 8 | Your first question, "**describe what style is used**" | **Gemini never answered it.** It never named or described the style of your reference video. | Medium: the style anchor is still missing |

## 2. Challenging *your* assumptions (the mentor part)

**a) "I need a LoRA file for my face."** You don't, and on Higgsfield you can't use one. A LoRA is a weight file for an open model such as Flux or SDXL. Higgsfield's video models (Kling 3.0, Seedance 2.0, Cinema Studio 3.0) cannot load it. Two things would make a LoRA worth the effort:
- you also plan to generate in ComfyUI or Flux outside Higgsfield, or
- you want a portable identity asset that you own.

Neither of those is your stated goal. Also, this container has **no GPU** (4 CPU cores, 15 GB RAM, no `nvidia-smi`). Training a Flux LoRA here would take days on CPU, if it finished at all. The right tool for your goal is **Soul Cinema training (5–20 photos, ~10 min)** plus keyframe-driven video. If you still want a `.safetensors` LoRA later, it has to be trained on a GPU service (fal.ai / Replicate Flux LoRA trainer, or a Hugging Face GPU job). That needs your own account and money, and I won't pretend otherwise.

**b) "The Avatar of Selûne is male, with my face."** That breaks the lore you asked me to respect. Selûne is a **goddess**, and every avatar form in canon is feminine [R3 pp. 134–135; R5 p. 55]. There is a **better, canon-true role** for you: a mortal **Moonsworn champion** wearing *Selûne's scale mail*. Canon says she lends that armour to mortals on a quest for her [R3 p. 134]. The goddess herself appears as a vast feminine presence in the moon. You keep the hero role, the lore holds, and the image gets stronger: a mortal channelling a goddess.

**c) "Elune."** Elune is the Warcraft moon goddess. Selûne is the Forgotten Realms goddess, and Shar is her twin [R4; R5]. Gemini corrected this, and it was right to.

**d) The Norse scenario is not Norse mythology.** Gemini's version had a volcanic wasteland, lightning hands, heavy chains of light and a decaying wolf. That mixes Surtr/Muspelheim, Thor and Ragnarök into a story that is **none of them**. In the *Prose Edda* [R10, ch. 34]:
- the gods first try the iron chains **Lœðingr** and **Drómi**, and Fenrir snaps both;
- they then bind him with **Gleipnir**, a ribbon "smooth and soft as a silken ribbon", made by the dwarves from six impossible things;
- the binding happens on the island **Lyngvi** in the lake **Ámsvartnir**;
- the wolf accepts only if a god puts a hand in his mouth as a pledge, and **Týr** gives his right hand and loses it.

That is a far more cinematic story than "chains erupt from the ground", and it gives your character (Týr) a sacrifice instead of a power-up. I rebuilt Scenario 2 around it.

**e) The Paper Seraph's weapon.** Crystalline shards from a paper being break **material logic**. Viewers feel that even if they can't name it. I replaced them with a storm of **folded paper blades and cranes edged in white light**, and the enemy became **living ink** (ink against parchment is the natural conflict). Crystal remains as an alternative.

**f) Three characters in one shot (Scenario 4).** Soul allows **one `soul_id` per generation** [R1]. That works here because only you carry a trained identity and the two Shards are invented. If you ever want a second real face, such as a friend, you'll need Reference Elements, not Soul.

**g) Intellectual property.** "Inspired by Warcraft" is fine. A skeletal king in a spiked helm with a runeblade named after the real one, posted publicly, is not. The prompts keep the archetype and avoid trademarked names and signature designs.

**h) Your face is biometric data.** Under GDPR, facial images processed to uniquely identify a person are "biometric data" [R11 Art. 4(14)], a special category [R11 Art. 9]. Uploading them to Higgsfield means a third-party processor holds them. That's your decision to make, but make it knowingly:
- read Higgsfield's retention terms;
- don't put the photos in this Git repository (I added a `.gitignore` for this);
- delete the Soul when you're done if you don't need it.

## 3. Gemini's model advice, corrected

| Need | Gemini said | Use instead (verified [R1]) |
|---|---|---|
| Lock your face | "Soul ID, 20+ photos" | **Soul Cinema** (`soul_cinematic`) trained on **15–20** curated photos. It is cinema-grade stills only. |
| Hero keyframes | Flux.2 | **Soul Cinema** + your `soul_id`, 16:9, quality 2k |
| Non-hero keyframes (wolf, demon, angels of decay) | not covered | Soul Cinema *without* `soul_id`, or Nano Banana Pro / Cinema Studio Image 2.5 |
| Shot animation | Kling 3.0 | **Kling 3.0, mode `pro`, `sound: off`**. It takes start **and end** images, which is ideal for transformations, and runs 3–15 s. |
| Premium alternative | not covered | **Cinema Studio Video 3.0**, `genre: epic`, 1080p, start/end image, 4–15 s, supports 21:9 |
| Identity directly inside video | not covered | **Reference Element** (`<<<uuid>>>` in prompt), built from your best keyframe and used with Seedance 2.0 or Cinema Studio Video 3.0 |
| Dialogue / lip-sync | Kling 3.0 | Correct (Kling 3.0 `sound: on`), but none of the four films needs dialogue. Silence plus a score is stronger. |

## 4. What I built for you

1. **`higgsfield/02_PRODUCTION_PROMPTS.md`**: four fully re-written films (16 shots). Each shot has a *keyframe prompt* (appearance), a *motion prompt* (movement only) and exact tool parameters, so Claude Code + Higgsfield MCP can execute them without guessing.
2. **`tools/face_qc.py`**: an identity-QC tool that runs on CPU (OpenCV YuNet detector [R13] + SFace recognizer [R14]).
   - `dataset` mode rejects blurred, too-small, badly exposed, multi-face and wrong-person photos, removes near-duplicates, keeps angle diversity, selects ≤20 and crops them to 1024².
   - `verify` mode scores every generated keyframe against your reference face, so likeness is **measured, not eyeballed**. A frame passes at cosine ≥ 0.50; 0.363 is the published same-person threshold.
3. **`tools/fetch_models.sh`**: re-downloads the face models (they are kept out of git).

Installed in this session: `opencv-python-headless` 5.0, `numpy`, YuNet + SFace ONNX models. `ffmpeg` 6.1 was already present for final assembly. No GPU training stack was installed, because without a GPU it would be dead weight.

## 5. Still missing (I need it from you)

- **The reference video and the screenshot.** Neither Gemini nor I has *seen* them in a form I can analyse. The prompts assume a "photoreal, macro-texture, high-contrast celestial" look. Send the video and I'll extract frames, name the style precisely, and tune all 16 keyframe prompts to it.
- **Your 20+ photos.** Mix: 6 frontal, 4 three-quarter left, 4 three-quarter right, 2 profiles, 4 varied expressions. Use even daylight, no sunglasses or hats, no beauty filters, taken within the last ~6 months, and with your face at least 256 px tall.

---

## References

- **[R1]** Higgsfield MCP server, live tool specifications retrieved 2026-10-30: `show_characters` (Soul training: 5–20 images; usable only with `soul_2` / `soul_cinematic`; one `soul_id` per generation), `manage_reference_elements`, `models_explore` entries for `kling3_0` (3–15 s; std/pro/4k; start_image/end_image; 16:9, 9:16, 1:1; no negative-prompt parameter), `cinematic_studio_3_0` (4–15 s; 480p–4k; genre; start/end image), `seedance_2_0`, `soul_cinematic` (quality 1.5k/2k; `soul_id`).
- **[R2]** Greenwood, E., Reynolds, S. K., Williams, S. & Heinsoo, R. *Forgotten Realms Campaign Setting*, 3rd ed. Wizards of the Coast, 2001, pp. 248–249 (Selûne; the Shards; Conjuring of the Second Moon).
- **[R3]** Martin, J. & Boyd, E. L. *Faiths & Avatars*. TSR, 1996, pp. 134–136 (Selûne's avatar forms; Rod of Four Moons, a four-flanged heavy mace; *Selûne's scale mail* of opalescent circular scales glowing with silver light, lent to beings on a quest for her; Shards: female, long flowing blue hair, pearly white skin, wings displayed or dismissed at will).
- **[R4]** Boyd, E. L. & Mona, E. *Faiths and Pantheons*. Wizards of the Coast, 2002, p. 55 (Selûne; Shards; Shar as twin and arch-enemy).
- **[R5]** Same as R4, pp. 55–58 (Selûne, full entry; holy symbol: a pair of feminine eyes surrounded by seven stars).
- **[R6]** Baker, R., Stout, T. & Wyatt, J. *Player's Guide to Faerûn*. Wizards of the Coast, 2004, p. 154 (Shards dwell at the Gates of the Moon; formed of equal parts moonlight and fire).
- **[R7]** Reid, T. M., Mearls, M. et al. *Champions of Valor*. Wizards of the Coast, 2005, p. 57 (Shards chosen from Selûne's highest-ranked priestesses).
- **[R8]** Collins, A. & Cordell, B. R. *Libris Mortis: The Book of Undead*. Wizards of the Coast, 2004, pp. 83–84 (angel of decay: ~9 ft, 500–700 lb, vaguely humanoid winged undead, constantly rotting and streaming liquid corruption that pools up to 15 ft around it and rots living things; instinctively recognises worshippers of its former deity).
- **[R9]** Wizards of the Coast. *Vanrakdoom* (web enhancement), p. 24 (Shar corrupts some Shards of Selûne into angels of decay). Secondary compilation: Forgotten Realms Wiki, "Shards" and "Angel of decay", retrieved 2026-10-30.
- **[R10]** Snorri Sturluson. *Edda: Prologue and Gylfaginning*, ed. A. Faulkes. Viking Society for Northern Research, 2nd ed., 2005, ch. 34 (binding of Fenrir: Lœðingr, Drómi, Gleipnir, Lyngvi, Ámsvartnir, Týr's hand). English translation: Faulkes, A., *Snorri Sturluson: Edda*, Everyman, 1987 (ch. 34; page numbers differ by edition).
- **[R11]** Regulation (EU) 2016/679 (General Data Protection Regulation), OJ L 119, 4.5.2016, p. 1–88: Art. 4(14) definition of biometric data (p. 34); Art. 9 processing of special categories (pp. 38–39).
- **[R12]** Mearls, M., Schubert, S. & Wyatt, J. *Monster Manual* (4th ed.). Wizards of the Coast, 2008, p. 223 (rot harbinger / angel of decay, origin myth with Orcus).
- **[R13]** Wu, W., Peng, H. & Yu, S. "YuNet: A Tiny Millisecond-level Face Detector." *Machine Intelligence Research* 20, 656–665 (2023). DOI: 10.1007/s11633-023-1423-y.
- **[R14]** Zhong, Y., Deng, W., Hu, J., Zhao, D., Li, X. & Wen, D. "SFace: Sigmoid-Constrained Hypersphere Loss for Robust Face Recognition." *IEEE Transactions on Image Processing* 30, 2587–2598 (2021). DOI: 10.1109/TIP.2020.3048632. Cosine same-person threshold 0.363 per OpenCV Zoo model card.

*Note on your standing instruction:* EU GMP, EudraLex, EMA and ICH guidance don't apply to creative video production, so none is cited here. The one EU regulation that does apply is the GDPR [R11].
