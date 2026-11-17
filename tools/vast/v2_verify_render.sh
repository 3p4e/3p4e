#!/usr/bin/env bash
# Verify the three SkyReels-V2 weights (hardcoded authoritative sizes) and,
# if valid, start the 12-beat Origami render directly (setup already done).
set -uo pipefail
export LC_ALL=C
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

DST=/workspace/hf/df13b
log "kill stale"
pkill -9 -f v2_repair_dl 2>/dev/null || true
pkill -9 -f aria2c 2>/dev/null || true
pkill -9 -f 'curl.*huggingface' 2>/dev/null || true
pkill -9 -f v2_origami_setup 2>/dev/null || true
pkill -9 -f generate_video 2>/dev/null || true
sleep 2

MODEL_SZ=5742186488
VAE_SZ=507609880
T5_SZ=11361920418

check_sz(){ local f=$1 want=$2; local s=$(stat -c%s "$f" 2>/dev/null || echo 0); if [ "$s" -eq "$want" ]; then log "OK $f $s"; else log "BAD $f got=$s want=$want"; return 1; fi; }
ok=1
check_sz "$DST/model.safetensors" $MODEL_SZ || ok=0
check_sz "$DST/Wan2.1_VAE.pth" $VAE_SZ || ok=0
check_sz "$DST/models_t5_umt5-xxl-enc-bf16.pth" $T5_SZ || ok=0

log "validate safetensors header"
python3 - <<'PY'
import struct, json
p='/workspace/hf/df13b/model.safetensors'
with open(p,'rb') as f:
    n = struct.unpack('<Q', f.read(8))[0]
    json.loads(f.read(n))
print('SAFETENSORS_HEADER_OK', n)
PY

[ "$ok" -eq 1 ] || { log "SIZE_VERIFY_FAIL"; exit 9; }

log "weights verified; starting 12-beat render"
bash /workspace/v2_render_origami.sh 2>&1 | tee /workspace/origami_render.log
log "RENDER_DONE exit=$?"
