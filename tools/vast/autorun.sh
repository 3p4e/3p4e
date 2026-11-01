#!/bin/bash
# Autonomous Wan 2.2 14B I2V test for Vast.ai (vastai/comfy template image).
# Started from the instance's onstart. Logs go to /workspace/autorun.log AND the container log
# (PID 1 stdout), which the Vast API exposes. The clip is returned as base64 blocks in that log.
export LC_ALL=C
LOG=/workspace/autorun.log; mkdir -p /workspace
RAW=https://raw.githubusercontent.com/3p4e/3p4e/claude/elegant-thompson-uqhred/tools/vast
MAXMIN=${MAXMIN:-100}
say(){ m="[AUTORUN $(date -u +%H:%M:%S)] $*"; echo "$m" >> $LOG; echo "$m" > /proc/1/fd/1 2>/dev/null || true; }
stop_self(){ curl -s -X PUT -H "Authorization: Bearer $CONTAINER_API_KEY" -H "Content-Type: application/json" -d '{"state":"stopped"}' "https://console.vast.ai/api/v0/instances/$CONTAINER_ID/" >> $LOG 2>&1; }
say "canary: autorun started on $(hostname); cap ${MAXMIN} min"
( sleep $((MAXMIN*60)); say "hard cap reached -> stopping instance"; stop_self ) &
R=/workspace/ComfyUI_run
if [ -f $R/models/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors ]; then
  say "models present: starting ComfyUI only (no downloads, no tests)"
  (cd $R && setsid nohup /venv/main/bin/python main.py --listen 127.0.0.1 --port 8199 > /workspace/comfy_run.log 2>&1 &)
  for i in $(seq 1 90); do sleep 4; curl -s -m 3 http://127.0.0.1:8199/system_stats >/dev/null && { say "comfyui up"; break; }; done
  say "READY for run_face_tests.sh"
  exit 0
fi
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>&1 | while read l; do say "gpu: $l"; done
df -h /workspace | tail -1 | while read l; do say "disk: $l"; done

# ---- 1) models (parallel), ~38 GB, Apache-2.0 files from Comfy-Org repackage
B=https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files
S=/workspace/stage; mkdir -p $S
get(){ for i in 1 2 3 4; do wget -q -c -O "$S/$(basename $1)" "$B/$1" && { say "ok $(basename $1) $(stat -c%s $S/$(basename $1))"; return 0; }; sleep 5; done; say "FAIL $1"; return 1; }
T0=$(date +%s); PIDS=()
get diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors & PIDS+=($!)
get diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors & PIDS+=($!)
get loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors & PIDS+=($!)
get loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors & PIDS+=($!)
get text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors & PIDS+=($!)
get vae/wan_2.1_vae.safetensors & PIDS+=($!)
wait "${PIDS[@]}"
say "downloads finished in $(( $(date +%s)-T0 )) s"

# ---- 2) our own ComfyUI copy (does not touch the template's /workspace/ComfyUI)
R=/workspace/ComfyUI_run
[ -d $R ] || cp -a /opt/workspace-internal/ComfyUI $R
for d in diffusion_models loras text_encoders vae; do mkdir -p $R/models/$d; done
mv $S/wan2.2_i2v_*_14B_fp8_scaled.safetensors $R/models/diffusion_models/ 2>/dev/null
mv $S/wan2.2_i2v_lightx2v_*.safetensors $R/models/loras/ 2>/dev/null
mv $S/umt5_xxl_fp8_e4m3fn_scaled.safetensors $R/models/text_encoders/ 2>/dev/null
mv $S/wan_2.1_vae.safetensors $R/models/vae/ 2>/dev/null
cd $R && setsid nohup /venv/main/bin/python main.py --listen 127.0.0.1 --port 8199 > /workspace/comfy_run.log 2>&1 &
UP=0
for i in $(seq 1 90); do sleep 4; curl -s -m 3 http://127.0.0.1:8199/system_stats >/dev/null && { UP=1; break; }; done
say "comfyui up=$UP after ~$((i*4)) s"
[ "$UP" = 1 ] || { tail -25 /workspace/comfy_run.log | while read l; do say "comfy: $l"; done; }

# ---- 3) returning a file: base64 blocks in the container log
emit(){ f="$1"; n=$(basename "$f"); out=/workspace/send_$n
  if command -v ffmpeg >/dev/null 2>&1; then ffmpeg -y -loglevel error -i "$f" -c:v libx264 -crf 27 -preset veryfast -pix_fmt yuv420p "$out" || cp "$f" "$out"; else cp "$f" "$out"; fi
  sz=$(stat -c%s "$out"); sha=$(sha256sum "$out" | cut -d' ' -f1)
  say "B64BEGIN $n $sz $sha"
  base64 -w 2000 "$out" | awk '{print "B64 " NR " " $0}' | tee -a $LOG > /proc/1/fd/1 2>/dev/null
  say "B64END $n"; }

# ---- 4) tests
if [ "$UP" = 1 ]; then
  curl -fsSL $RAW/run_wan_i2v.py -o /workspace/run_wan_i2v.py
  for dims in "832 480" "1280 720"; do set -- $dims
    say "run ${1}x${2}"
    /venv/main/bin/python /workspace/run_wan_i2v.py --host http://127.0.0.1:8199 --w $1 --h $2 2>&1 | while read l; do say "run: ${l:0:300}"; done
    f=$(ls -t $R/output/wan22_test_${1}x${2}*.mp4 2>/dev/null | head -1)
    if [ -n "$f" ]; then say "output $f $(stat -c%s $f) bytes"; emit "$f"; else say "no output for ${1}x${2}"; fi
  done
fi
say "AUTORUN DONE (job channel active: set label to job:<hex> to run tools/vast/jobs/<hex>.sh)"

# ---- 5) remote job channel: label "job:<hex>" -> run tools/vast/jobs/<hex>.sh from the public repo
last=""
while [ ! -e /workspace/STOP ]; do
  lab=$(curl -s -m 15 -H "Authorization: Bearer $CONTAINER_API_KEY" https://console.vast.ai/api/v0/instances/ | python3 -c "
import sys,json,os
try:
    d=json.load(sys.stdin); L=d.get('instances',[d]) if isinstance(d,dict) else d
    for x in L:
        if str(x.get('id'))==os.environ.get('CONTAINER_ID'): print(x.get('label') or ''); break
except Exception: print('')" 2>/dev/null)
  if echo "$lab" | grep -Eq '^job:[0-9a-f]{6,12}$' && [ "$lab" != "$last" ]; then
    last="$lab"; say "JOB $lab"
    curl -fsSL "$RAW/jobs/${lab#job:}.sh" -o /workspace/job.sh && bash /workspace/job.sh 2>&1 | head -c 400000 | while read -r l; do say "job: ${l:0:1500}"; done
    say "JOB END $lab"
  fi
  sleep 20
done
