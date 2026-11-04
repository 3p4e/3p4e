#!/usr/bin/env bash
# SkyReels-V2 DF retry #3 FULL: fresh instance -> setup -> fetch -> corrected 377f render.
# Merges v2_retry.sh's proven setup (deps/repo/flash-attn) with v2_run3.sh's corrected
# curl-fetch + dynamic chunk-flag discovery. NO in-instance watchdog.
set -uo pipefail
export HF_HOME=/workspace/hf
export PIP_DISABLE_PIP_VERSION_CHECK=1
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

[ -f /workspace/seed.png ] || { log "MISSING_SEED"; exit 3; }

# ---------- 1. deps ----------
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

# ---------- 3. flash-attn ----------
log "flash-attn"
python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" 2>/dev/null || {
  log "building flash-attn (--no-build-isolation)"
  pip install --no-build-isolation -q flash-attn 2>&1 | tail -3
  python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" || { log "FLASHA_FATAL"; exit 5; }
}

# ---------- 4. model files (curl; bypasses broken huggingface_hub httpx2 gzip) ----------
log "models"
BASE="https://huggingface.co/Skywork/SkyReels-V2-DF-1.3B-540P/resolve/main"
DST=/workspace/hf/df13b
mkdir -p "$DST/google/umt5-xxl"
[ -f "$DST/models_t5_umt5-xxl-enc-bf16.pth" ] && \
  [ "$(stat -c%s "$DST/models_t5_umt5-xxl-enc-bf16.pth")" -eq 11361920418 ] || \
  curl -L -f --retry 8 --retry-delay 3 -C - -o "$DST/models_t5_umt5-xxl-enc-bf16.pth" "$BASE/models_t5_umt5-xxl-enc-bf16.pth"
sz=$(stat -c%s "$DST/models_t5_umt5-xxl-enc-bf16.pth" 2>/dev/null || echo 0)
[ "$sz" -eq 11361920418 ] || { log "T5_SIZE_BAD $sz"; exit 6; }
[ -f "$DST/model.safetensors" ] || curl -L -f --retry 5 -o "$DST/model.safetensors" "$BASE/model.safetensors"
[ -f "$DST/Wan2.1_VAE.pth" ] || curl -L -f --retry 5 -o "$DST/Wan2.1_VAE.pth" "$BASE/Wan2.1_VAE.pth"
curl -sL -f --retry 5 -o "$DST/config.json" "$BASE/config.json"
curl -sL -f --retry 5 -o "$DST/google/umt5-xxl/special_tokens_map.json" "$BASE/google/umt5-xxl/special_tokens_map.json"
curl -sL -f --retry 5 -o "$DST/google/umt5-xxl/spiece.model" "$BASE/google/umt5-xxl/spiece.model"
curl -sL -f --retry 5 -o "$DST/google/umt5-xxl/tokenizer.json" "$BASE/google/umt5-xxl/tokenizer.json"
curl -sL -f --retry 5 -o "$DST/google/umt5-xxl/tokenizer_config.json" "$BASE/google/umt5-xxl/tokenizer_config.json"
log "fetch_done"
ls -lh "$DST/models_t5_umt5-xxl-enc-bf16.pth" "$DST/model.safetensors" "$DST/Wan2.1_VAE.pth"

# ---------- 5. render: 377 total frames, chunk flag discovered at runtime ----------
# Match ONLY a prefixed *_num_frames arg (excludes bare --num_frames). Hard-fail otherwise.
CHUNK_FLAG=$(python3 - <<'PY'
import re
src = open("generate_video_df.py").read()
m = re.search(r'add_argument\("--([a-z_]+_num_frames)"', src)
print("--" + m.group(1) if m else "NOFLAG")
PY
)
case "$CHUNK_FLAG" in
  NOFLAG)       log "CHUNK_FLAG_FATAL"; exit 7;;
  --num_frames) log "WRONG_FLAG total"; exit 8;;
  *)            log "chunk_flag=$CHUNK_FLAG";;
esac

OUT=/workspace/out3; mkdir -p "$OUT"
log "render total=377 chunk=97 overlap=17 fps=24"
python3 -u generate_video_df.py \
  --model_id /workspace/hf/df13b \
  --resolution 540P \
  --image /workspace/seed.png \
  --num_frames 377 \
  "$CHUNK_FLAG" 97 \
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
log "V2_FULL3_DONE"
