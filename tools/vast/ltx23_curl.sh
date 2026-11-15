#!/bin/bash
# Pull LTX-2.3 22B weights with curl (the PROVEN method from curl_weights.sh:
# hf_hub_download died silently; curl resumes with -C -, retries, visible bytes).
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/logs/ltx23_curl.log
say(){ echo "[LTX23 $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

if [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
if [ -z "${HF_TOKEN:-}" ]; then say "FATAL_NO_TOKEN"; exit 1; fi
say "token len ${#HF_TOKEN}"

DEST=/workspace/models/ltx23
mkdir -p "$DEST"

fetch(){
  repo="$1"; path="$2"; name="${path##*/}"; out="$DEST/$name"
  url="https://huggingface.co/$repo/resolve/main/$path"
  say "GET $name"
  for attempt in $(seq 1 12); do
    curl -L --fail --retry 0 --connect-timeout 20 --max-time 5400 \
      -C - -H "Authorization: Bearer $HF_TOKEN" \
      -o "$out" "$url" 2>>/workspace/logs/ltx23_curl_dl.log
    rc=$?
    sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
    say "attempt $attempt rc=$rc size=$sz"
    [ "$rc" = "0" ] && break
    if [ "$rc" = "33" ]; then say "resume unsupported, restart"; rm -f "$out"; fi
    sleep 5
  done
  say "DONE $name bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)"
}

fetch LTX-Video/ltx-2.3-22b-distilled-1.1 ltx-2.3-22b-distilled-1.1.safetensors
fetch LTX-Video/ltx-2.3-22b-distilled-1.1 ltx-2.3-22b-384-distilled-lora.safetensors
fetch Comfy-Org/comfy_gemma_3_12B_it split_files/text_encoder/1-gemma_3_12B_it_fp8_e4m3fn.safetensors

say "SUMMARY"
ls -lh "$DEST"
say "LTX23_CURL_ALL_DONE"
