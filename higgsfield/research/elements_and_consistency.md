# The Elements System & Character Consistency Master Guide

> Compiled July 2026 from Higgsfield official blog guides: the 3-Step Ultra-Realistic AI Ads workflow, the Seedance 4K VFX guide, the Seedance 4K film breakdown, the Soul ID guide, the "7 Tools for Consistent AI Characters" comparison, and the Zephyr K-Pop series breakdown.

This guide answers the two hardest problems in AI video production: **how to reuse the same asset across every generation (Elements)** and **how to keep a character identical across every shot (consistency stack)**.

---

## 1. What Elements Are

**Elements** is Higgsfield's reusable asset library. Instead of re-uploading reference images for every generation, you save an asset (character, product, prop, location, schematic) once as a named Element, and reference it by name in any prompt.

Elements exist to solve one specific failure mode: cross-generation drift. A character or product that recurs in every scene must come from ONE locked reference, or the model reinvents it slightly each time.

### The core mechanic: exact name matching

1. Build the asset image (see Section 3 for which tool to use per asset type).
2. In Higgsfield, add the asset under **Elements** and give it a name, e.g. `hero`, `sneakers`, `kitchen`.
3. In your prompt, reference it with the `@` prefix: `@hero`, `@sneakers`, `@kitchen`.
4. **The Element name and the @ reference must match exactly.** When they match, the correct image auto-attaches to every generation that mentions it — no manual re-uploading.

This pairs directly with the Claude shotlist skill workflow: you give Claude an element list, Claude writes prompts using those names, and because the names match the Elements in Higgsfield, every generated prompt pulls the right assets automatically.

### The element list convention

When briefing Claude (or writing your own shotlist), declare every asset up front with its role:

```
@hero — main character
@boss — side character
@headphones — product, cream with orange ring
@sneakers — prop
@bag — prop
@skydancer — inflatable tube dancer
@kitchen — apartment kitchen, stove + door
@stadium — running track
@street — Brooklyn corner
@office — boss's office
```

Rules that make this work:
- **One Element per recurring thing.** Product, each character, each wardrobe state, each location, each prop.
- **Names are roles, not descriptions.** Short, unambiguous, stable across the whole project.
- **State variants get their own Elements.** The headphones ad used `@s_hero` (athletic outfit, dry) and `@s_hero_wet` (sweat-soaked, damp hair) as *separate* Elements — baking the physical state into a locked reference prevents face drift during dry-to-wet transitions. Same for outfit changes: don't ask the model to "make him sweaty," swap to the pre-built wet Element.

### Appearance-only referencing

When an Element is meant to define *what something looks like* (not the scene around it), say so explicitly. From the official VFX guide's `@LIZARD` example:

```
@LIZARD: Reference of a real large monitor lizard — pebbled scaly skin, long claws, heavy tail.
Appearance, scale-texture and color reference only; ignore the photo's background
and lighting, do not use it for the environment.
```

The model uses the Element's appearance and texture and discards its background/lighting. Always add this clause for creature/object Elements photographed against unrelated backdrops.

### Schematic-map Elements (spatial locking)

Text can't hold a location down; a map can. For scenes where prop positions must stay identical across cuts, build a top-down schematic as an Element:

```
make a schematic - mark the fire hydrant, and lock the skydancer to its right,
it should be two times a person's height, located on the same line.
```

Then reference it in scene prompts (`@street_schematic`) and restate the lock in text:

```
@skydancer POSITION LOCKED: on the sidewalk immediately to the right of the fire
hydrant. This position is fixed and identical across all cuts.
```

---

## 2. The Consistency Stack — Three Layers

Higgsfield offers three distinct consistency mechanisms. They are not interchangeable — they operate at different scopes:

| Layer | Scope | Mechanism |
|---|---|---|
| **@ references / Elements** | Within one generation (and reusable across a project via Elements) | Model reads uploaded reference images at generation time |
| **Soul ID** | Across every generation on the platform, all models | Trained identity model — internalizes facial structure once |
| **Reference sheets + visual anchors** | Prompt-level insurance | Detailed geometric descriptors keep text and image agreeing |

Use all three together for production work: Soul ID (or a fused master sheet) for the face, Elements for wardrobe/props/locations, and 3–5 visual anchors in every prompt.

### Layer 1 — @ references and Elements (per-generation)

Character references hold faces consistent **within single generations only**. Every new generation re-reads the image, so quality of the reference is everything: sharp, front-facing, well-lit, grey background (see Section 3).

### Layer 2 — Soul ID (persistent identity)

Soul ID trains a digital identity once from reference photos; the same face then holds across every image and video you generate — no re-uploading, no re-describing.

**How it differs from reference matching:** a reference image anchors to *that specific image at that specific angle in that specific lighting*. Soul ID instead internalizes facial structure, proportions, and identifying features as a coherent whole, so it survives dramatic changes in scene, lighting, and camera angle where reference matching breaks down.

**Training requirements:**
- **20+ photos recommended; up to 80 accepted**
- Resolution **960px or higher**
- Different angles and expressions; consistent lighting across the set
- Avoid sunglasses, masks, extreme expressions
- Training takes **3–5 minutes**, costs **25 credits (~$1.25, June 2026)**
- Runs in Soul 2.0 on any paid plan

**Workflow:** upload photos → system builds the digital twin → pick from 50+ style presets → generate; reuse indefinitely across Soul, Seedance 2.0, Kling 3.0, Veo 3.1, WAN 2.6 — stable across sessions and models.

**Practical tips:**
- Works for real people AND AI-generated characters (generate a character, then train a Soul ID on its renders).
- Pick a style preset early and stay with it — switching presets too often erodes audience recognition.
- Treat the trained ID as a core production asset, not a one-off.
- Pair with Cinema Studio: one trained identity + one camera-control layer across all video models.

### Layer 3 — Visual anchors (prompt-level)

Even with references attached, restate 3–5 distinctive geometric anchors in the prompt:
- ❌ "brown hair" → ✅ "short asymmetrical bob with bright magenta tips"
- ❌ "a jacket" → ✅ "black leather jacket with three silver zippers on the left sleeve"

Cap it at 3–5. Overloaded descriptions (8+) make the model choose motion over identity, and drift returns.

---

## 3. Building Element Assets — Tool Selection & Prompts

From the Seedance 4K film breakdown and the ads workflow — different image models excel at different asset types:

| Asset type | Best tool | Why |
|---|---|---|
| Character faces & cinematic shots | **Soul Cinema** | Photoreal identity; 1 credit for 8 images |
| Character sheets at 4K | **GPT Image 2** | Sharpest multi-view sheets |
| Props & product sheets | **Nano Banana Pro** | Better depth and realistic highlights than GPT Image 2 |
| Face + outfit fusion | **Nano Banana Pro** | "The character from image 1 wearing this outfit from image 2" |
| Locations | **Soul Cinematic Locations / Cinema Studio** | Cinematic stills, 3/4 angle |
| Side characters / archetypes | **Soul Cast** | Fast pre-built casting |

**The better the input image, the sharper the final video.** Regenerate the Element until reference details look natural — asset quality compounds through every downstream generation.

### Asset-building rules (all verbatim-tested)

1. **Grey backgrounds win.** Neutral grey character sheets outperform white and black — nothing competes with the character, and the win rate goes up.
2. **Locations always at 3/4 angle.** Flat head-on location shots collapse when the camera moves; 3/4 framing gives the model depth to work with.
3. **Erase duplicate faces.** On any character sheet with multiple views, erase the face from all but one view (`"Erase the face from the full-body shot on the right panel."`). Multiple faces confuse the model about which one to track.
4. **Bake physical states into separate Elements** (dry/wet, clean/damaged, day/night outfits).
5. **Explicit NO-branding block on products:** `"STRICTLY NO branding: no brand names, logos, swooshes, stripe-logos, wordmarks, text, trademarks, or brand-resembling motifs"` — keeps outputs usable and compliant (the NON-IP directive).

### Verbatim asset prompts from the official ad workflow

**Product sheet (GPT Image 2):**
```
Make a product sheet with front and 3/4 perspective views of the headphones from @image_1.
```

**Hero character sheet (Soul Cinema):** split-frame layout — facial close-up (85mm, shallow depth of field) + full-body front/back on grey background, "consistent character across all views, soft diffused cinematic lighting."

**Outfit variant (edit an existing sheet):**
```
Edit this character sheet so he's wearing a blue athletic outfit, with these sneakers (@sneakers).
```

**State variant:**
```
same character sheet, post-run, sweaty chest, sweat stains on the shirt.
```

**Location:**
```
Modern apartment kitchen, 3/4 angle, bright clean daylight, high-end commercial look.
```

**Prop sheet (multi-view, orthographic):** lateral side, medial side, top-down, front 3/4 hero angle, rear/heel, bottom — on flat neutral light-gray studio background, with material/color/mood description and the NO-branding block.

---

## 4. The Complete 3-Stage Production Workflow (Official)

This is Higgsfield's own pipeline for broadcast-grade ads, and it generalizes to any narrative project.

### Stage 1 — Build ALL assets first

Product sheet, hero sheet, wardrobe/state variants, side characters, every location (3/4 angle), every prop, schematic maps for spatially-locked scenes. **Nothing gets animated until every recurring thing is a locked Element.** "They recur in every scene, and locking them up front is what keeps everything consistent once the camera starts moving."

### Stage 2 — Prompting framework (Claude skill + Elements)

1. Download `higgsfield-seedance-shotlist-director.skill` → Claude → Customize → Skills → upload.
2. Fresh chat: attach the video script + every Stage 1 asset image + the element list (Section 1).
3. Add each asset under **Elements** in Higgsfield with the **identical name**.
4. The skill returns one **connected shotlist**:
   - a **style prefix** glued to every prompt — change it once, it updates everywhere;
   - **named per-cut prompts** (1a, 1b, 2a, 2b…) — edit one, the rest stay locked.

### Stage 3 — Generate scene by scene

- Minimum ~5 scenes for an ad (e.g. kitchen, stadium, street, office, packshot).
- Each scene generates as multiple named cuts; keep a naming convention (1a, 1b…).
- Expect to edit keeper seconds out of dozens of generations (~100 kept generations for a trailer; hundreds discarded).

### The universal style header (verbatim, from the headphones ad)

```
8K IMAX commercial, 16:9 widescreen. Photorealistic — no 3D render, no game engine.
Lighting: Natural light only — soft, even morning daylight, gentle atmospheric haze
throughout. Key light from sky. No contre-jour, no rim backlight, no forced
shadow-side framing. No artificial lightning.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush,
pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, living eyes
with catch-lights, chest rise from breathing. Characters never standing, always reacting.
Physics: Gravity and inertia respected — mass has real weight, correct contact
shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Diegetic dialogue and environmental SFX only. No music. No subtitles.
```

The style header locks the look; per-scene prompts only override lighting/environment for that location.

### Advanced scene techniques proven in the official ad

- **Beat-locked choreography:** "he dances" produces flailing. Write the movement beat by beat: "first two crisp head nods, chin dipping on each beat; then his shoulders roll back one at a time — right, then left… a light quarter-spin on the ball of his foot."
- **Match-cut planning at the prompt stage:** end Scene 1 on a double ear-cup tap, open Scene 2 on the same tap — the edit stitches itself.
- **Snorricam / body-rig shots:** "The camera is rigged to Hero's body, snorricam-style — zero relative motion between the lens and his head" — locks the product rock-steady while the world blurs past. Killer product-shot technique.
- **FOV-specified cameras:** the pro prompts specify fields of view (8° super-telephoto broadcast, 12° tele detail, 29° portrait, 47° standard, 63° wide, 84° worm's-eye, 107° rectilinear low angle) instead of vague "close-up/wide."
- **Precise speed callouts:** "sprints at around 25 km/h" — numbers beat adjectives.
- **Diegetic-only audio in generation;** music and sound design are added in post.

---

## 5. Consistency Tool Comparison (2026 Landscape)

From Higgsfield's official comparison of 7 tools:

| Tool | Mechanism | Best for | Limits |
|---|---|---|---|
| **Soul ID** | Trains persistent identity from 20+ photos in 3–5 min | Real people, photoreal faces, any format; works across Kling 3.0 / Veo 3.1 / Seedance 2.0 | Separate training step first |
| **Flux.2 fine-tune** | Bakes identity into model weights (15–30 refs) | 20+ clip series; extreme angle changes; fictional characters | Setup time; one fine-tune per character |
| **LoRA (IC-LoRA / ComfyUI)** | Adapters lock body structure + camera from reference footage | Per-shot camera/motion control, technical pipelines | Requires ComfyUI; not for non-technical creators |
| **Seedance 2.0** | Strongest prompt adherence; up to 9+3+3 reference inputs; native audio | Commercial video, spokesperson variations (pair with Soul ID) | Sparse briefs → weak output |
| **Kling 3.0** | Native lip-sync in 8+ languages; multi-shot consistency | Dialogue-heavy, international content | Quality degrades past ~30s |
| **Midjourney** | Character-ref + style-ref params per generation | Illustrated/stylized mascots, stills | Images only; weaker lock at high shot counts |
| **Runway Gen-4.5** | Single portrait applied at generation time; Director Mode | Quick 3–5 shot narratives, zero training | 16s native; Extend degrades consistency; no native audio |

**Routing guide:** real person → Soul ID · deep lock for 20+ clips → Flux.2 · illustrated stills → Midjourney · quick multi-shot, no training → Runway · commercial spokesperson → Seedance 2.0 + Soul ID · spoken lip-sync → Kling 3.0.

**Universal principles (all tools):**
1. Start with an anchor scene — a clean close-up showing key features.
2. Restate the character's visual anchors in every subsequent prompt.
3. Change ONE variable at a time (setting alone, then angle alone). Changing several at once is the #1 cause of identity drift.

---

## 6. Supporting Platform Systems

### Canvas (node-based pipelines)

Canvas is Higgsfield's infinite node board: a prompt feeds an image, the image feeds a video, models chain freely (Soul 2.0 / GPT Image 2.0 / Nano Banana Pro → Seedance 2.0 / Kling 3.0 / Wan 2.7 / Veo 3.1). Relevant to consistency because:
- **Soul ID characters, uploaded products, and brand references integrate as nodes** — consistent visuals across a campaign without re-uploading.
- **Canvases save as reusable templates** — duplicate, swap the inputs, and a new campaign spins up in minutes (ad variants, character sheets, storyboards).
- Team-collaborative like Figma; you pay only for nodes you actually run.

### Cinema Studio (camera-control layer)

- **2.5:** Soul Cast AI actors, built-in color grading, 3D Mode (Gaussian splatting), grid generation, frame-extraction loop, object & person insertion, per-character emotions, five-view location reference sheets, and the **Elements library surface (5 source tabs × 6 element categories)**.
- **3.0:** native stereo audio, smart shot control, 15s max, 7 genres, @ reference patterns, Soul Cast 3.0.
- **3.5:** Genre/Style/Camera three-pill UI; Style panel (8 color palettes, 6 lighting modes, 9 camera moveset styles + manual); four-axis Camera panel (3 bodies, 5 lenses, 5 focal lengths incl. 75mm, 3 apertures); Image Mode with four cinematic model pickers.

Pair one trained Soul ID with Cinema Studio's camera layer and any video model underneath.

### Pricing anchors (mid-2026)

- Starter $15/mo (200 credits); Plus $49/mo (1,000 credits).
- 720p 8s clip ≈ $1.55 (36 credits); 1080p ≈ $2.00; audio adds 50–100%.
- Soul ID training: 25 credits.
- Seedance Unlimited / Enhanced Fast tiers exist for volume iteration at 480/720p.

---

## 7. Consistency Failure → Fix Cheat Sheet

| Symptom | Root cause | Fix |
|---|---|---|
| Face drifts mid-clip (5–8s mark) | Model prioritizes motion over identity | Better reference (fix the image, not the prompt); Soul ID; fewer, sharper anchors |
| Character looks different between scenes | Per-generation references only | Elements with exact name matching + Soul ID |
| Outfit changes between cuts | Outfit described in text only | Separate wardrobe-state Elements (`@s_hero`, `@s_hero_wet`) |
| Model tracks the wrong face on a sheet | Multiple faces on reference sheet | Erase all faces except one front view |
| Prop moves/resizes between cuts | No spatial anchor | Schematic-map Element + "POSITION LOCKED" text |
| Element's background bleeds into scene | Reference role not scoped | Add "appearance/texture reference only; ignore background and lighting" |
| Product warps during fast motion | Camera and subject move independently | Body-rig/snorricam prompt: "zero relative motion between the lens and his head" |
| Reference images ignored entirely | No @ text anchor mapping them | Every upload must be named in the prompt (`@hero`, `wearing the outfit from @Image2`) |

---

## Sources

- [3-Step Workflow To Make Ultra-Realistic AI Ads](https://higgsfield.ai/blog/cinematic_headphones) — the definitive Elements + naming workflow
- [AI VFX Just Got Insane — Seedance 2.0 in 4K](https://higgsfield.ai/blog/vfx_4k) — named Elements (`@LIZARD`), lock headers, NON-IP
- [Recreate Our 1-Minute Seedance 4K Film](https://higgsfield.ai/blog/seedance4k-breakdown) — tool selection per asset, grey backgrounds
- [Soul ID Explained](https://higgsfield.ai/blog/sould-id-best-character-consistency) — training specs and workflow
- [7 Tools for Consistent AI Characters (2026)](https://higgsfield.ai/blog/tools-for-consistent-ai-characters) — tool comparison
- [Zephyr K-Pop Series Breakdown](https://higgsfield.ai/blog/guide-youtube-seedance2.0) — 3-step character pipeline at series scale
- [Generating with Seedance 2.0: Full Tutorial](https://higgsfield.ai/blog/generating-with-seedance-2-0) — @character/@style/@motion/@audio, Soul ID vs references
- [AI Canvas — Node-Based Workflow](https://higgsfield.ai/canvas-intro) — reusable pipelines
- [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) — MCSLA, Cinema Studio versions, Elements library surface
