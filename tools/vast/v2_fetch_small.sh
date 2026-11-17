#!/usr/bin/env bash
# Fetch the SMALL SkyReels-V2 files missing from /workspace/hf/df13b:
# config.json + google/umt5-xxl tokenizer files. Big weights are already verified.
set -uo pipefail
export LC_ALL=C
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }
DST=/workspace/hf/df13b
BASE="https://huggingface.co/Skywork/SkyReels-V2-DF-1.3B-540P/resolve/main"
log "fetch small files"

fetch(){ # $1 = relpath
  local rel="$1"
  mkdir -p "$(dirname "$DST/$rel")"
  curl -sL -f --retry 6 --retry-delay 2 -o "$DST/$rel" "$BASE/$rel" || { log "FETCH_FAIL $rel"; return 1; }
  local sz=$(stat -c%s "$DST/$rel" 2>/dev/null || echo 0)
  log "$rel -> $sz bytes"
}

fetch config.json
fetch google/umt5-xxl/special_tokens_map.json
fetch google/umt5-xxl/spiece.model
fetch google/umt5-xxl/tokenizer.json
fetch google/umt5-xxl/tokenizer_config.json

log "validate config.json"
python3 -c "import json; d=json.load(open('/workspace/hf/df13b/config.json')); print('CONFIG_JSON_OK keys:', list(d.keys())[:8])" || { log "CONFIG_JSON_INVALID"; exit 3; }

log "SMALL_FILES_DONE"
ls -la "$DST" "$DST/google/umt5-xxl"
