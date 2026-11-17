#!/usr/bin/env bash
# Repair the corrupted SkyReels-V2 weight download on the video instance.
# T5 (11GB) is INTACT and left alone. model.safetensors + Wan2.1_VAE.pth were
# corrupted by an aria2c multi-URL collision; re-fetch each SEPARATELY.
set -uo pipefail
export LC_ALL=C
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

DST=/workspace/hf/df13b
BASE="https://huggingface.co/Skywork/SkyReels-V2-DF-1.3B-540P/resolve/main"
SIZES=/workspace/hf/sizes.json

log "kill stale"
pkill -9 -f aria2c 2>/dev/null || true
pkill -9 -f 'curl.*huggingface' 2>/dev/null || true
pkill -9 -f v2_origami_setup 2>/dev/null || true
pkill -9 -f generate_video 2>/dev/null || true
sleep 2
log "stale procs now: $(ps aux | grep -E 'aria2c|curl|v2_origami|generate_video' | grep -v grep | wc -l)"

log "fetch authoritative sizes"
python3 - <<'PY'
import json, urllib.request
r = urllib.request.urlopen('https://huggingface.co/api/models/Skywork/SkyReels-V2-DF-1.3B-540P', timeout=60)
d = json.load(r)
want = {'model.safetensors', 'Wan2.1_VAE.pth', 'models_t5_umt5-xxl-enc-bf16.pth'}
out = {}
for s in d.get('siblings', []):
    if s.get('rfilename') in want:
        out[s['rfilename']] = s.get('size')
json.dump(out, open('/workspace/hf/sizes.json', 'w'))
print(json.dumps(out, indent=2))
PY
log "sizes saved"

log "remove corrupt files (keep T5)"
rm -f "$DST/model.safetensors" "$DST/Wan2.1_VAE.pth" "$DST"/*.aria2
ls -la "$DST"

MODEL_SZ=$(python3 -c "import json;print(json.load(open('/workspace/hf/sizes.json')).get('model.safetensors','0'))")
VAE_SZ=$(python3 -c "import json;print(json.load(open('/workspace/hf/sizes.json')).get('Wan2.1_VAE.pth','0'))")
log "expected model=$MODEL_SZ vae=$VAE_SZ"

log "download model.safetensors (aria2c, 16 connections, resume on control file)"
cd "$DST"
nohup aria2c -x16 -s16 -c -o model.safetensors "$BASE/model.safetensors" > /workspace/aria_model.log 2>&1 &
log "download Wan2.1_VAE.pth (separate invocation)"
nohup aria2c -x16 -s16 -c -o Wan2.1_VAE.pth "$BASE/Wan2.1_VAE.pth" > /workspace/aria_vae.log 2>&1 &

# poll until both sizes match (or a hard timeout of 45 min)
for i in $(seq 1 270); do
  sleep 10
  m=$(stat -c%s "$DST/model.safetensors" 2>/dev/null || echo 0)
  v=$(stat -c%s "$DST/Wan2.1_VAE.pth" 2>/dev/null || echo 0)
  if [ "$m" -ge "$MODEL_SZ" ] && [ "$v" -ge "$VAE_SZ" ]; then
    log "BOTH SIZES MATCH model=$m vae=$v"
    break
  fi
  # log every 60s
  if [ $((i % 6)) -eq 0 ]; then log "progress model=$m/$MODEL_SZ vae=$v/$VAE_SZ"; fi
done

m=$(stat -c%s "$DST/model.safetensors" 2>/dev/null || echo 0)
v=$(stat -c%s "$DST/Wan2.1_VAE.pth" 2>/dev/null || echo 0)
pkill -9 -f aria2c 2>/dev/null || true
if [ "$m" -ge "$MODEL_SZ" ] && [ "$v" -ge "$VAE_SZ" ]; then
  log "REPAIR_DOWNLOAD_OK model=$m vae=$v"
  exit 0
else
  log "REPAIR_DOWNLOAD_INCOMPLETE model=$m/$MODEL_SZ vae=$v/$VAE_SZ"
  exit 9
fi
