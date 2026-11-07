#!/bin/bash
# Start the Vast.ai dashboard locally (no Docker).
# The API key is read server-side from .a0proj/secrets.env and never leaves the process.
#
#   ./run.sh                        # loopback only, no login required
#   VAST_DASH_TOKEN=secret ./run.sh # login required, still loopback
#   HOST=0.0.0.0 VAST_DASH_TOKEN=secret ./run.sh   # LAN/public (token mandatory)
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root

PORT="${PORT:-8090}"
HOST="${HOST:-127.0.0.1}"

# load the key without printing it
if [ -z "${VASTAI_API:-}" ] && [ -f .a0proj/secrets.env ]; then
  VASTAI_API="$(grep -E '^VASTAI_API=' .a0proj/secrets.env | head -1 | cut -d= -f2- | tr -d '\r"')"
fi
export VASTAI_API

ARGS=(--host "$HOST" --port "$PORT")
if [ -n "${VAST_DASH_TOKEN:-}" ]; then
  ARGS+=(--token "$VAST_DASH_TOKEN")
fi

if [ "$HOST" != "127.0.0.1" ] && [ "$HOST" != "localhost" ] && [ -z "${VAST_DASH_TOKEN:-}" ]; then
  echo "refusing: HOST=$HOST without VAST_DASH_TOKEN" >&2
  echo "set one:  export VAST_DASH_TOKEN=\$(openssl rand -hex 24)" >&2
  exit 1
fi

exec python3 tools/vast_dashboard/server.py "${ARGS[@]}"
