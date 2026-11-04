#!/usr/bin/env bash
# SkyReels-V2 DF retry #3: CORRECT long-video run (377 total frames in 97-frame chunks).
# Root cause of retry #2: the script resolved the TOTAL-frames flag instead of the
# CHUNK-SIZE flag, so argparse silently took the duplicate (97) and rendered 4s.
# Fix: discover the chunk arg dynamically by matching ONLY a prefixed *_num_frames
# argument (excludes the bare --num_frames), and hard-fail on any wrong resolution.
set -uo pipefail
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HOME=/workspace/hf
BASE="https://huggingface.co/Skywork/SkyReels-V2-DF-1.3B-540P/resolve/main"
DST=/workspace/hf/df13b
mkdir -p "$DST/google/umt5-xxl"

log "curl-fetch models"
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

# Discover the CHUNK-SIZE flag from the actual source: match only a prefixed
# *_num_frames argument, never the bare --num_frames. Hard-fail on wrong/absent.
cd /workspace/SkyReels-V2
CHUNK_FLAG=$(python3 - <<'PY'
import re
src = open("generate_video_df.py").read()
m = re.search(r'add_argument\("--([a-z_]+_num_frames)"', src)
print("--" + m.group(1) if m else "NOFLAG")
PY
)
case "$CHUNK_FLAG" in
  NOFLAG)        log "CHUNK_FLAG_FATAL"; exit 7;;
  --num_frames)  log "WRONG_FLAG=$CHUNK_FLAG (matched total)"; exit 8;;
  *)             log "chunk_flag=$CHUNK_FLAG";;
esac

OUT=/workspace/out3; mkdir -p "$OUT"
log "render: total=377 frames, chunk=97, overlap=17, fps=24"
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
log "V2_RUN3_DONE"
