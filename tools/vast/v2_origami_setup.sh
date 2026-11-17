#!/usr/bin/env bash
# SkyReels-V2 DF setup + 12-beat Origami fight render (Phase 2).
# Reuses v2_full3.sh's proven setup/fetch; rendering delegated to v2_render_origami.sh
# (per-beat keyframe conditioning + wrong-anchor gate + corrected I2V params).
# NO in-instance watchdog: teardown is controlled from the host after copy-verify.
set -uo pipefail
export HF_HOME=/workspace/hf
export PIP_DISABLE_PIP_VERSION_CHECK=1
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

# ---------- 1. deps ----------
log "deps"
pip install -q --upgrade pip 2>&1 | tail -1 || true
pip install -q "moviepy==1.0.3" decord ftfy sentencepiece omegaconf timm \
  imageio imageio-ffmpeg huggingface_hub hf_transfer transformers diffusers \
  accelerate einops safetensors opencv-python-headless tqdm 2>&1 | tail -3 || true
python -c "import torch,diffusers,transformers,accelerate,einops,ftfy,sentencepiece,omegaconf,timm,imageio,imageio_ffmpeg,decord,moviepy.editor,safetensors,huggingface_hub;print('deps_ok')" || { log "DEPS_FATAL"; exit 4; }
log "deps_ok"

# ---------- 2. repo ----------
log "repo"
[ -d /workspace/SkyReels-V2 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V2 /workspace/SkyReels-V2
cd /workspace/SkyReels-V2
pip install -q -r requirements.txt 2>&1 | tail -2 || log "reqs partial (continuing)"
log "repo_ok"

# ---------- 3. flash-attn ----------
log "flash-attn"
python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" 2>/dev/null || {
  log "building flash-attn (--no-build-isolation)"
  pip install --no-build-isolation -q flash-attn 2>&1 | tail -3
  python -c "from flash_attn import flash_attn_varlen_func; import flash_attn_2_cuda; print('fa_ok')" || { log "FLASHA_FATAL"; exit 5; }
}
log "fa_ok"

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

# ---------- 5. render all 12 beats via the per-beat driver ----------
log "render 12 beats"
bash /workspace/v2_render_origami.sh 2>&1 | tee /workspace/origami_render.log
log "ORIGAMI_SETUP_DONE"
