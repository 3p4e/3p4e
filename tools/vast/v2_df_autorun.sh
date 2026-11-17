#!/usr/bin/env bash
# SkyReels-V2 Diffusion-Forcing long-video test. Runs ON the rented instance.
# Goal: ONE continuous image-to-video generation seeded from a face-locked Azulon
# keyframe, long enough to prove V2 holds continuity (15s = 377 frames per README).
set -euo pipefail
export HF_HOME=/workspace/hf
export HF_HUB_ENABLE_HF_TRANSFER=1
OUT=/workspace/out; mkdir -p "$OUT"
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

# ---------- 1. deps ----------
log "installing deps"
pip install -q --upgrade pip
pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121 || true
pip install -q "diffusers>=0.32" "transformers<5" accelerate imageio imageio-ffmpeg \
  "numpy<2" opencv-python-headless tqdm wget huggingface_hub hf_transfer safetensors \
  sentencepiece protobuf moviepy

# ---------- 2. repo ----------
log "cloning SkyReels-V2"
[ -d /workspace/SkyReels-V2 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V2 /workspace/SkyReels-V2
cd /workspace/SkyReels-V2
pip install -q -r requirements.txt || log "requirements partial (continuing)"

# ---------- 3. weights (DF 1.3B 540P = the infinite-length checkpoint) ----------
log "downloading DF-1.3B-540P"
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("Skywork/SkyReels-V2-DF-1.3B-540P", local_dir="/workspace/hf/df13b",
                  allow_patterns=["*.json","*.safetensors","*.txt","*.py","*/*.json"],
                  max_workers=8)
print("weights ready")
PY

# ---------- 4. seed frame ----------
SEED=/workspace/seed.png
[ -f "$SEED" ] || { log "ERROR: seed frame missing at $SEED"; exit 3; }
log "seed: $(ls -l $SEED | awk '{print $5}') bytes"

# ---------- 5. generate ONE continuous 15s clip ----------
# README: num_frames 377 = 15s, 737 = 30s, 1457 = 60s.
# overlap_history 17 + addnoise_condition 20 are the documented long-video values.
log "generating 15s continuous (377 frames)"
set +e
python generate_video_df.py \
  --model_id /workspace/hf/df13b \
  --resolution 540P \
  --image "$SEED" \
  --num_frames 377 \
  --base_num_frames 97 \
  --overlap_history 17 \
  --addnoise_condition 20 \
  --ar_step 0 \
  --guidance_scale 6.0 \
  --inference_steps 30 \
  --offload \
  --fps 24 \
  --seed 800 \
  --prompt "Cinematic photorealistic film still in motion: a clean ivory parchment seraph with folded paper wings edged in cold white flame, hairless shaven head, long high-elf ears, a faint silver crescent on the forehead, hovering in a starless black void as black tar-like corruption drips from the ragged wings of a colossal corrupted paper seraph below him, white fire igniting along every crease, drifting loose pages, dense maximalist composition, volumetric light, ultra detailed" \
  --outdir "$OUT" 2>&1 | tee /workspace/out/gen.log
rc=$?
set -e
log "generator exit=$rc"

# ---------- 6. collect + report ----------
find /workspace -name '*.mp4' -newermt '-6 hours' -not -path '*/hf/*' -exec cp -v {} "$OUT"/ \; || true
log "outputs:"; ls -lh "$OUT" || true
for f in "$OUT"/*.mp4; do
  [ -e "$f" ] || continue
  log "probe $f"
  ffprobe -v error -show_entries format=duration,size:stream=width,height,r_frame_rate,nb_frames -of default=noprint_wrappers=1 "$f" || true
done
log "V2_DF_DONE"
