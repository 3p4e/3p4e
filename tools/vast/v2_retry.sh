#!/usr/bin/env bash
# SkyReels-V2 Diffusion-Forcing long-video retry (15s = 377 frames, 540P).
# Single consolidated, resumable script that runs ON the rented instance.
#
# Fixes vs the first attempt (which rendered correctly then got killed):
#  1. NO leaked self-stop watchdog. The prior failure was a stale `sleep N; stop`
#     timer from an earlier failed launch firing mid-render. I manage teardown
#     from the host side, not from a detached in-instance timer.
#  2. flash-attn built with --no-build-isolation (needs nvcc; devel image has it).
#  3. Model files fetched per-file via hf_hub_download (snapshot_download stalled).
#  4. moviepy pinned to 1.0.3 (2.x removed moviepy.editor).
#  5. The base-frames flag is extracted from the repo argparse at run time so no
#     transcription/redaction artifact can corrupt it.
set -uo pipefail
export HF_HOME=/workspace/hf
export PIP_DISABLE_PIP_VERSION_CHECK=1
OUT=/workspace/out2
mkdir -p "$OUT"
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

[ -f /workspace/seed.png ] || { echo "MISSING_SEED"; exit 3; }

# ---------- 1. deps (idempotent) ----------
log "deps"
pip install -q --upgrade pip 2>&1 | tail -1 || true
pip install -q "moviepy==1.0.3" decord ftfy sentencepiece omegaconf timm \
  imageio imageio-ffmpeg huggingface_hub hf_transfer transformers diffusers \
  accelerate einops safetensors opencv-python-headless tqdm 2>&1 | tail -3 || true
python -c "import torch,diffusers,transformers,accelerate,einops,ftfy,sentencepiece,omegaconf,timm,imageio,imageio_ffmpeg,decord,moviepy.editor,safetensors,huggingface_hub;print('deps_ok')" || { log "DEPS_FATAL"; exit 4; }

# ---------- 2. repo ----------
log "repo"
[ -d /workspace/SkyReels-V2 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V2 /workspace/SkyReels-V2
cd /workspace/SkyReels-V2
pip install -q -r requirements.txt 2>&1 | tail -2 || log "reqs partial (continuing)"

# ---------- 3. flash-attn (source, no build isolation; skip if present) ----------
log "flash-attn"
python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" 2>/dev/null || {
  log "building flash-attn (--no-build-isolation)"
  pip install --no-build-isolation -q flash-attn 2>&1 | tail -3
  python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" || { log "FLASHA_FATAL"; exit 5; }
}

# ---------- 4. model files (resume-able per-file fetch) ----------
log "models"
python /workspace/fetch_v2_full.py || { log "FETCH_FATAL"; exit 6; }

# ---------- 5. render: ONE continuous 15s clip ----------
log "render 377f"
BASE_FLAG=$(python - <<'PY'
import re
src = open("/workspace/SkyReels-V2/generate_video_df.py").read()
m = re.search(r'add_argument\("--([a-z_]*num_frames)"', src)
print("--" + m.group(1) if m else "--base_num_frames")
PY
)
log "base_flag=$BASE_FLAG"
python -u generate_video_df.py \
  --model_id /workspace/hf/df13b \
  --resolution 540P \
  --image /workspace/seed.png \
  --num_frames 377 \
  "$BASE_FLAG" 97 \
  --overlap_history 17 \
  --addnoise_condition 20 \
  --ar_step 0 \
  --guidance_scale 6.0 \
  --inference_steps 30 \
  --offload \
  --fps 24 \
  --seed 800 \
  --prompt "Cinematic photorealistic film still in motion: a clean ivory parchment seraph with folded paper wings edged in cold white flame, hairless shaven head, long high-elf ears, a faint silver crescent on the forehead, hovering in a starless black void as black tar-like corruption drips from the ragged wings of a colossal corrupted paper seraph below him, white fire igniting along every crease, drifting loose pages, dense maximalist composition, volumetric light, ultra detailed" \
  --outdir "$OUT" 2>&1 | tee "$OUT/gen.log"
log "render_exit=$?"
ls -lh "$OUT"
log "V2_RETRY_DONE"
