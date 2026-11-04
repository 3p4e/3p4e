# Prompt Composition Guide — Keyframes and Video

Grounded in the official model docs (fetched 2026-11-04), plus project-specific
empirical lessons marked **[observed]** where they were learned from failure and
are NOT documented upstream.

Sources fetched and read:
- `huggingface.co/Qwen/Qwen-Image/raw/main/README.md`
- `huggingface.co/Qwen/Qwen-Image-Edit/raw/main/README.md`
- `raw.githubusercontent.com/SkyworkAI/SkyReels-V2/main/README.md`

---

## 0. The core idea: two prompts, two different masters

A keyframe prompt and a video prompt are NOT the same prompt at different
lengths. They answer to different mechanisms:

| | Keyframe (Qwen-Image-Edit) | Video (SkyReels-V2 DF / R2V) |
|---|---|---|
| Dominant signal | The **reference image(s)** + instruction | The **first-frame image** (anchor) + motion text |
| What text must do | Say WHAT changes / WHAT stays, control density | Describe the **first frame** + **camera & motion** |
| Failure mode | Wrong edit-mode wording → slop / face bleed | Text contradicts anchor → anchor wins, text ignored |

---

## 1. KEYFRAME prompt composition (Qwen-Image-Edit)

### 1a. Pick the edit MODE first — it changes the wording

Qwen-Image-Edit has two documented modes (from model card):

- **Appearance editing** — add/remove/modify an element, all OTHER regions stay
  unchanged. Wording = an **instruction** to change one thing.
- **Semantic editing** — IP creation, rotation, style transfer: overall pixels
  change while **semantic identity** is preserved. Wording = **describe the
  full target scene**, letting identity carry from the reference image.

**For our face-locked regenerations, we want SEMANTIC editing.**
Write the complete desired tableau (new staging, new pose, new environment) and
let the identity come from `image1/image2/image3`. Do NOT write appearance-edit
phrasing like "change only the background, keep the face identical" — that
language freezes the wrong thing for a full restage.

### 1b. Prompt structure (semantic-staging jobs)

1. **Subject + identity anchor** — who, from which reference, invariant traits
   (*"Azulon: clean-shaven jaw, long high-elf ears, silver crescent on forehead"*).
2. **Action / pose** — what the figure does, body geometry.
3. **Staging / environment** — where, light source, time-of-day, depth.
4. **COMPOSITION DENSITY** — foreground + midground + background objects,
   explicit frame edges. [observed: sparse single-figure compositions read as
   "slop"; every frame needs near/mid/far layers and props]
5. **Style / mood** — palette, atmosphere, lens. Keep this SHORT.
6. **Negative** — what must never appear.

### 1c. The truncation rule [observed — NOT documented]

The Qwen 2.5-VL encoder **truncates long captions from the END** and
`run_qwen_edit_full.py` passes **no max_length**. So trailing style words —
"volumetric light, ultra detailed" — are the FIRST thing eaten on long prompts.

Rule:
- Keep the prompt **≤ 1400 chars**.
- Put IDENTITY and ACTION **early** (they survive).
- Do not depend on a trailing style suffix; fold the 2–3 most important style
  terms into the MIDDLE of the prompt.
- Highest-quality prior renders clustered at ~1080–1150 chars, peaked 1496.

### 1d. Negative prompt

Use an explicit, short negative. Never let "duplicate face / extra face /
two heads" be omitted on hero shots (face-bleed prevention). The official T2I
card defaults `negative_prompt` to a single space when nothing to remove.

### 1e. T2I (Qwen-Image, no edit)

Official card appends a positive magic suffix per language:
- English: `", Ultra HD, 4K, cinematic composition."`
- Chinese: `", 超清，4K，电影级构图."`

Text rendering is a strength: Qwen-Image reproduces glyphs accurately, so do
NOT try to fake text with prompt prose — if a frame needs lettering, spell it.

---

## 2. VIDEO prompt composition (SkyReels-V2 Diffusion Forcing, I2V)

### 2a. THE rule that fixes the anchor failure

Official README (line ≈308), verbatim intent:

> For image-to-video (I2V), add `--image ${path}` AND use a **T2V-like prompt
> that includes a description of the first-frame image**.

That is the prescription for the exact failure we hit: I rendered with an
Azulon seed while the text described a parchment seraph. The text **contradicted**
the anchor, so the anchor won and the text was ignored. The fix is not
"describe the desired result harder" — it is **describe the seed frame** so text
and anchor agree, then add motion.

### 2b. Prompt structure (I2V)

1. **First-frame description** — WHAT IS IN THE SEED IMAGE (subject, palette,
   key objects). Must match the actual anchor file.
2. **Motion / action** — what moves, direction, body dynamics.
3. **CAMERA** — SkyReels-V2 is explicitly trained on camera grammar; the
   highest-scoring dimensions are shot position (83%), camera motion (85%),
   shot angle (90%). State it plainly: "slow push-in", "low-angle tracking shot",
   "crane down".
4. **Continuity** — what persists across chunks (a static element that must not
   drift).
5. **Style / mood** — SHORT.

### 2c. Length and the enhancer

Official: `--prompt_enhancer` (Qwen2.5-32B) works **ideally for SHORT prompts**;
**long prompts get over-saturated** and the enhancer needs 64G+ peak VRAM.
Choose ONE path:
- Short base prompt + `--prompt_enhancer`, OR
- Hand-written detailed prompt, NO enhancer.
Do not write a long prompt AND enhance it.

### 2d. Parameter corrections [official values we were NOT using]

| Param | Official I2V value | Our last run |
|---|---|---|
| `--shift` | **5.0** (I2V) | 8.0 |
| `--guidance_scale` | **5.0** (I2V) | 6.0 |
| `--inference_steps` | **50** | 30 |
| `--num_frames` | 97 (540P) / 121 (720P) per chunk | 97 ✓ |

These are free quality levers — no extra cost beyond render time.

---

## 3. Templates

### Keyframe (semantic staging, face-locked) — skeleton

```text
{SUBJECT}, {invariant identity traits}. {ACTION + full-body pose}. Set in
{ENVIRONMENT with light source and depth layers}. Foreground: {...}; midground:
{...}; background: {...}. {2-3 style words mid-prompt}. Palette: {...}.
Negative: duplicate face, extra face, two heads, extra limbs, text, watermark.
```

### Video (I2V, Diffusion Forcing) — skeleton

```text
The first frame shows {EXACT seed-frame content}. Then {motion: what moves,
how, in what direction}. Camera: {shot size + camera movement}. {Continuity:
what stays fixed}. Light and mood: {short palette note}.
```

---

## 4. Pipeline changes these findings mandate

1. `run_qwen_edit_full.py` — enforce ≤1400-char prompt cap at emit time
   (already enforced in `build_origami_jobs.py`; mirror it everywhere).
2. Video scripts (`v2_*.sh`) — use shift 5.0, guidance 5.0, steps 50 for I2V.
3. **Build the seed frame from `seraph_ref.png`** (hash-verify it is NOT any
   Azulon/hero frame) before any re-render. The seed-correctness check is the
   single most important preflight gate.
4. Keyframe jobs: choose edit mode explicitly in the builder (semantic vs
   appearance) and word the prompt accordingly — do not leave it implicit.
