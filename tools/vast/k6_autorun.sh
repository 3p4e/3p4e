#!/bin/bash
# Kandinsky 6.0 Lite (distilled) + VSR autorun for Vast.ai (vastai/comfy template).
# MIT licence, EU-legal. Prefetches weights, then waits for /workspace/GO.
export LC_ALL=C
export HF_HOME=/workspace/hf
LOG=/workspace/k6.log; mkdir -p /workspace/out /workspace/stills $HF_HOME
MAXMIN=${MAXMIN:-110}
say(){ m="[K6 $(date -u +%H:%M:%S)] $*"; echo "$m" >> $LOG; echo "$m" > /proc/1/fd/1 2>/dev/null || true; }
stop_self(){ curl -s -X PUT -H "Authorization: Bearer $CONTAINER_API_KEY" -H "Content-Type: application/json" -d '{"state":"stopped"}' "https://console.vast.ai/api/v0/instances/$CONTAINER_ID/" >> $LOG 2>&1; }

say "start on $(hostname); hard cap ${MAXMIN} min"
( sleep $((MAXMIN*60)); say "CAP reached -> stop"; stop_self ) &

nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>&1 | while read -r l; do say "gpu: $l"; done
df -h /workspace | tail -1 | while read -r l; do say "disk: $l"; done

P=/venv/main/bin/python

# ---- 1) diffusers with Kandinsky6 pipelines (v0.42.1 predates nothing vital; use main to be safe)
say "installing diffusers from git"
$P -m pip install -q --upgrade 'git+https://github.com/huggingface/diffusers.git' 2>&1 | tail -5 | while read -r l; do say "pip: $l"; done
$P -m pip install -q --upgrade transformers accelerate safetensors imageio imageio-ffmpeg 2>&1 | tail -3 | while read -r l; do say "pip: $l"; done

$P - <<'PY' 2>&1 | while read -r l; do echo "[K6 chk] $l"; done
import torch, diffusers
print("torch", torch.__version__, "cuda", torch.cuda.is_available())
print("diffusers", diffusers.__version__)
try:
    from diffusers import Kandinsky6TI2VAPipeline
    print("Kandinsky6TI2VAPipeline OK")
except Exception as e:
    print("PIPELINE MISSING:", e)
try:
    from diffusers import Kandinsky6SRPipeline
    print("Kandinsky6SRPipeline OK")
except Exception as e:
    print("SR PIPELINE MISSING:", e)
PY

# ---- 2) prefetch weights (26.6 GB Lite + ~2 GB VSR)
say "prefetching weights"
$P - <<'PY' 2>&1 | tail -20 | while read -r l; do say "dl: $l"; done
from huggingface_hub import snapshot_download
for repo in ("kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers",
             "kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers"):
    p = snapshot_download(repo, allow_patterns=["*.json","*.safetensors","*.txt","*.jinja","*.model"])
    print("cached", repo, "->", p)
PY
say "weights ready; WAITING for /workspace/GO"
for i in $(seq 1 400); do [ -e /workspace/GO ] && break; sleep 3; done
if [ ! -e /workspace/GO ]; then say "no GO -> stop"; stop_self; exit 1; fi
say "GO received -> running batch"

# ---- 3) run
ls -la /workspace/stills | while read -r l; do say "still: $l"; done
$P /workspace/paladin_k6_run.py 2>&1 | while read -r l; do say "run: ${l:0:1200}"; done

say "RESULTS:"; cat /workspace/out/results.json 2>/dev/null | while read -r l; do say "res: ${l:0:1200}"; done
ls -la /workspace/out | while read -r l; do say "out: $l"; done
say "K6 DONE (instance left running for pull; destroy manually)"
