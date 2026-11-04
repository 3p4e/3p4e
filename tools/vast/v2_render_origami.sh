#!/usr/bin/env bash
# SkyReels-V2 DF I2V render driver for the Origami Ascension fight (12 beats).
#
# Corrections applied (18_PROMPT_COMPOSITION_GUIDE.md §2 + 19_ORIGAMI_FIGHT_v5):
#   - I2V parameters: shift 5.0, guidance 5.0, inference_steps 50 (were T2V 8.0/6.0/30).
#   - Per-beat prompt describes its seed keyframe (first-frame agreement).
#   - No --prompt_enhancer.
#   - Wrong-anchor gate: monster beats must NOT use an Azulon hero frame as seed.
#
# Usage: bash v2_render_origami.sh [tag] [tag] ...
#   no args -> render all 12 beats in order.
# Requires on the instance: /workspace/hf/df13b (model), /workspace/SkyReels-V2 (repo),
# /workspace/origami_keyframes/<tag>.png (keyframes), deps + flash-attn (see v2_full3.sh).
set -uo pipefail
export HF_HOME=/workspace/hf
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

JOBS=/workspace/v2_video_jobs.json
KF=/workspace/origami_keyframes
OUT=/workspace/origami_out
mkdir -p "$OUT"
cd /workspace/SkyReels-V2

# The wrong-anchor gate: identity refs whose sha256 NO monster seed may equal.
AZ_BUST_SHA=$(sha256sum /workspace/A_bust.png | cut -d' ' -f1)
AZ_SHEET_SHA=$(sha256sum /workspace/sheet_front.png | cut -d' ' -f1)

# Discover the CHUNK flag from the source (never the bare --num_frames).
CHUNK_FLAG=$(python3 - <<'PY'
import re
src = open("generate_video_df.py").read()
m = re.search(r'add_argument\("--([a-z_]+_num_frames)"', src)
print("--" + m.group(1) if m else "NOFLAG")
PY
)
case "$CHUNK_FLAG" in
  NOFLAG) log "CHUNK_FLAG_FATAL"; exit 7;;
  --num_frames) log "WRONG_FLAG total"; exit 8;;
  *) log "chunk_flag=$CHUNK_FLAG";;
esac

render_one(){
  local tag=$1
  local row seed kf prompt kind
  row=$(python3 - "$JOBS" "$tag" <<'PY'
import json,sys
jobs=json.load(open(sys.argv[1]))
for j in jobs:
    if j["tag"]==sys.argv[2]:
        print(json.dumps(j)); break
PY
)
  [ -n "$row" ] || { log "NO_SUCH_BEAT $tag"; return 9; }
  seed=$(python3 -c "import json,sys;print(json.loads('''$row''')['seed'])")
  kind=$(python3 -c "import json,sys;print(json.loads('''$row''')['kind'])")
  prompt=$(python3 -c "import json,sys;print(json.loads('''$row''')['prompt'])")
  kf="$KF/$tag.png"
  [ -f "$kf" ] || { log "MISSING_KEYFRAME $kf"; return 10; }

  local s=$(sha256sum "$kf" | cut -d' ' -f1)
  if [ "$kind" = "monster" ]; then
    if [ "$s" = "$AZ_BUST_SHA" ] || [ "$s" = "$AZ_SHEET_SHA" ]; then
      log "WRONG_ANCHOR $tag: monster seed is an Azulon identity ref"
      return 11
    fi
  fi

  log "beat $tag seed=$seed kind=$kind sha=$s"
  python3 -u generate_video_df.py \
    --model_id /workspace/hf/df13b \
    --resolution 540P \
    --image "$kf" \
    --num_frames 97 \
    "$CHUNK_FLAG" 97 \
    --overlap_history 17 \
    --addnoise_condition 20 \
    --ar_step 0 \
    --shift 5.0 \
    --guidance_scale 5.0 \
    --inference_steps 50 \
    --offload \
    --fps 24 \
    --seed "$seed" \
    --prompt "$prompt" \
    --outdir "$OUT" 2>&1 | tee "$OUT/$tag.log"
  log "beat $tag exit=$?"
  ls -lh "$OUT" | grep -i "$tag" || true
}

if [ $# -eq 0 ]; then
  TAGS=$(python3 -c "import json;print(' '.join(j['tag'] for j in json.load(open('$JOBS'))))")
else
  TAGS=$*
fi

for t in $TAGS; do
  render_one "$t"
done
log "ORIGAMI_RENDER_DONE"
