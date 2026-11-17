#!/bin/bash
# Stop/destroy a Vast.ai instance immediately to stop billing.
# Usage: stop_instance.sh <instance_id> [destroy|stop]   (default: destroy)
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "usage: stop_instance.sh <instance_id> [destroy|stop]" >&2
  exit 2
fi
ID="$1"
MODE="${2:-destroy}"
cd /a0/usr/projects/vast
export VASTAI_API="$(grep -E '^VASTAI_API=' .a0proj/secrets.env | head -1 | cut -d= -f2- | tr -d '\r')"
if [ "$MODE" = "destroy" ]; then
  python3 tools/vast/vast_ctl.py destroy "$ID" --yes
else
  python3 tools/vast/vast_ctl.py stop "$ID"
fi
