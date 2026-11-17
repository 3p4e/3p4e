# SkyReels-V2 Archive — setup, use, and failure ledger

> Archived 2026-11-04 when the stack moved to SkyReels-V3 for the quality path.
> Keep this for future long-video / continuous-generation work. V2 is the ONLY
> model in the stack that does rolling long-form generation (Diffusion Forcing).

## What it is

- **Model:** `Skywork/SkyReels-V2-DF-1.3B-540P` (the variant we actually ran).
  A 14B / 720P variant also exists (`SkyReels-V2-DF-14B-720P`) but was never tested.
- **Repo:** https://github.com/SkyworkAI/SkyReels-V2 (`generate_video_df.py`)
- **Architecture:** AutoRegressive Diffusion Forcing — rolls video forward in
  overlapping chunks, so a single generation can run for minutes with no hard cuts.
- **License:** Skywork Community License (EU-legal).
- **Known for:** infinite-length / long-video generation, NOT clip quality or
  face-locking.

## Footprint + GPU

```
weights            ~16 GB resolved to /workspace/hf/df13b
  model.safetensors   ~5.3 GB
  umt5-xxl encoder    ~11 GB  (UMT5-XXL text encoder)
  Wan2.1_VAE.pth      ~1.5 GB
  + config.json + google/umt5-xxl tokenizer (SMALL but MANDATORY — see failures)
GPU                24 GB (RTX 3090) — never OOM'd at 540P
template           vastai/comfy or pytorch base + sshd
render speed       ~3.7 min wall-clock per 1 s of video (30 steps)
```

## Dependencies (exact, from the working retry)

```bash
pip install -q --upgrade pip
pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121 || true
pip install -q "diffusers>=0.32" "transformers<5" accelerate imageio imageio-ffmpeg \
  decord ftfy sentencepiece omegaconf timm "moviepy==1.0.3" "numpy<2" \
  opencv-python-headless tqdm huggingface_hub hf_transfer
# flash-attn: NO prebuilt cu128 wheel existed; build from source:
pip install -q --no-build-isolation flash-attn
```

`moviepy` must be pinned to `1.0.3` — 2.x removes `moviepy.editor`. flash-attn is
HARD-required (the pipeline `assert`s `FLASH_ATTN_2_AVAILABLE`, no SDPA fallback).

## Corrected I2V parameters (verified working)

```
python generate_video_df.py \
  --model_id /workspace/hf/df13b \
  --resolution 540P \
  --image <seed.png> \
  --num_frames 377 \
  --<chunk-size-flag> 97 \          # DISCOVER dynamically, see failures
  --overlap_history 17 \
  --addnoise_condition 20 \
  --ar_step 0 \
  --shift 5.0 \
  --guidance_scale 5.0 \
  --inference_steps 50 \
  --offload \
  --fps 24 \
  --seed 808
```

377 frames @ 24 fps = **15.708 s**. 97-frame chunks × 5 = one continuous 15.7 s shot.
Short path = 97 frames = 4.04 s.

## The prompt rule that matters most

**Describe the FIRST FRAME (the seed image) in the prompt, then add motion + camera.**
The text must agree with the anchor image; if it contradicts it, the image wins and
the text is ignored. This is the official README rule and the root cause of the
"Azulon background" failure (a stale `tools/vast/seed.png` that was byte-identical
to `media/azulon_keyframes/az_2_hero.png` seeded a seraph prompt).

## Failure ledger (each one cost time or money)

1. **Stale watchdog self-stop** — v2gen.sh spawned `sleep N ... stop` watchers on
every launch; earlier failed launches left them counting down. One fired mid-chunk-2
and hard-stopped the contract before an mp4 was written. Fix: named PID tracking +
`pkill -f` sweep before relaunch. Never leave background watchers alive.
2. **Missing config.json + umt5 tokenizer** — snapshot_download got the big weights
but not the small files; pipeline died with `OSError: config.json is not the path to
a directory`. This is the single most important gotcha: fetch the SMALL files too.
3. **--num_frames flag collision** — the flag-resolver regex matched the main
`--num_frames` argument instead of the chunk-size flag; argparse took the LAST value
so `377` was overridden by `97`. Fix: discover the chunk-size flag independently and
hard-fail if it resolves to the wrong one.
4. **Wrong seed anchor** — seed.png was an Azulon keyframe, not the seraph ref.
Always hash-verify the seed against the intended reference before rendering.
5. **Throttled HuggingFace download** — 2-4 MB/s despite a 3.6 Gbps link; 16 GB took
~40-60 min. The proposed KVM4 model-cache (deferred) removes this per-deploy cost.
6. **Transfer truncation** — a clip copied mid-write truncated; always scp-then-
md5/sha256-verify before destroy.
7. **httpx2 gzip crash** — huggingface_hub's httpx2 decoder raised
`TypeError: process() takes no keyword arguments` during fetch; fixed by curl-fetching
with resume + exact-size checks (`v2_retry2.sh`).

## Measuring / performance

```
15.7 s (377 f, 5 chunks)  ≈ 58-64 min @ 30 steps
          ≈ 3.7 min per second of video
3-min film  ≈ ~11 h      5-min film ≈ ~18.5 h   (540P on RTX 3090)
```

720P / 14B is several times slower — not measured.

## When to use V2 again

- A shot that MUST be one continuous take longer than ~5 s (V3 caps at ~5 s).
- Background plates / establishing shots where no face-lock is needed.
- NOT for hero/monster identity shots — V3's reference-to-video wins there.

## Relevant scripts (still in tools/vast, left in place)

```
rent_v2.py              rental builder (24GB, RTX 3090 allowlist)
v2_df_autorun.sh        full autorun (deps → clone → weights → render)
v2_origami_setup.sh     origami-specific setup
v2_render_origami.sh    beat renderer with hash gate
v2_retry.sh / retry2.sh / full3.sh / run3.sh   recovery scripts
v2_verify_render.sh     post-render check
build_origami_video_jobs.py   V2 beat manifest (replaced by V3 builder)
```
