#!/usr/bin/env bash
set -euo pipefail

# Completes `higgsfield auth login` on a headless or remote machine
# (VPS, code-server, container) where the browser runs somewhere else.
#
# Why: the CLI's OAuth flow redirects to http://localhost:8765/callback.
# When you sign in from your own browser, that redirect lands on YOUR
# machine — not this one — so the CLI waits forever. This script bridges
# the gap: you sign in, then paste the resulting callback URL back here
# and it is delivered to the waiting CLI listener locally.

if higgsfield auth token >/dev/null 2>&1; then
  echo "Already authenticated:"
  higgsfield account status 2>/dev/null || true
  exit 0
fi

LOG="$(mktemp)"
higgsfield auth login >"$LOG" 2>&1 &
PID=$!
trap 'kill "$PID" 2>/dev/null || true' EXIT

URL=""
for _ in $(seq 1 30); do
  URL=$(grep -oE 'https://clerk\.higgsfield\.ai/oauth/authorize\?[^ ]+' "$LOG" || true)
  [ -n "$URL" ] && break
  sleep 1
done
if [ -z "$URL" ]; then
  echo "Could not obtain the auth URL. CLI output:" >&2
  cat "$LOG" >&2
  exit 1
fi

cat <<EOF

1) Open this URL in your browser and sign in:

$URL

2) After approving, the browser will FAIL to load
   http://localhost:8765/callback?... — that is expected.
   Copy the FULL URL from the address bar and paste it below.
   (Codes expire after a few minutes, so do this in one sitting.)

EOF
read -r -p "Paste callback URL: " CB
curl -sS --max-time 15 "$CB" >/dev/null
sleep 3

if higgsfield auth token >/dev/null 2>&1; then
  echo "Authenticated."
  # Select a workspace if none is set (picks the first if there are several).
  if ! higgsfield account status >/dev/null 2>&1; then
    WS_ID=$(higgsfield workspace list 2>/dev/null \
      | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' \
      | head -1 || true)
    if [ -n "$WS_ID" ]; then
      higgsfield workspace set "$WS_ID"
    fi
  fi
  higgsfield account status || true
else
  echo "Authentication did not complete. CLI output:" >&2
  tail -5 "$LOG" >&2
  exit 1
fi
