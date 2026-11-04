#!/usr/bin/env bash
# SkyReels-V2 DF retry #2: curl-based model fetch + render.
# Fix for retry #1 crash: huggingface_hub's httpx2 gzip decoder is broken
# (TypeError: process() takes no keyword arguments), so fetch files with curl instead.
# Deps, flash-attn (fa_ok), and the repo clone are already proven on this instance.
set -uo pipefail
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HOME=/workspace/hf
BASE="https://huggingface.co/Skywork/SkyReels-V2-DF-1.3B-540P/resolve/main"
DST=/workspace/hf/df13b
mkdir -p "$DST/google/umt5-xxl"

log "curl-fetch models"
# big text encoder (resume-able), exact-size verified
curl -L -f --retry 8 --retry-delay 3 -C - -o "$DST/models_t5_umt5-xxl-enc-bf16.pth" \
  "$BASE/models_t5_umt5-xxl-enc-bf16.pth"
gsize=$(stat -c%s "$DST/models_t5_umt5-xxl-enc-bf16.pth" 2>/dev/null || echo 0)
log "t5 size=$gsize (expect 11361920418)"
[ "$gsize" -eq 11361920418 ] || { log "T5_SIZE_BAD"; exit 6; }

curl -L -f --retry 5 -o "$DST/config.json" "$BASE/config.json"
curl -L -f --retry 5 -o "$DST/google/umt5-xxl/special_tokens_map.json" "$BASE/google/umt5-xxl/special_tokens_map.json"
curl -L -f --retry 5 -o "$DST/google/umt5-xxl/spiece.model" "$BASE/google/umt5-xxl/spiece.model"
curl -L -f --retry 5 -o "$DST/google/umt5-xxl/tokenizer.json" "$BASE/google/umt5-xxl/tokenizer.json"
curl -L -f --retry 5 -o "$DST/google/umt5-xxl/tokenizer_config.json" "$BASE/google/umt5-xxl/tokenizer_config.json"
log "fetch sizes:"; ls -lh "$DST" "$DST/google/umt5-xxl"
log "fetch_done"

# ---------- render: ONE continuous 15s clip ----------
cd /workspace/SkyReels-V2
OUT=/workspace/out2; mkdir -p "$OUT"
BASE_FLAG=$(python3 - <<'PY'
import re
src = open("generate_video_df.py").read()
m = re.search(r'add_argument\("--([a-z_]*num_frames)"', src)
if not m:
    print("NOFLAG")
else:
    print("--" + m.group(1))
PY
)
[ "$BASE_FLAG" != "NOFLAG" ] || { log "FLAG_FATAL"; exit 7; }
log "flag=$BASE_FLAG"
log "render 377f"
python3 -u generate_video_df.py \
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
log "V2_RETRY2_DONE"
