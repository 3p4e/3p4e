#!/usr/bin/env bash
# Deploy the Vast.ai dashboard to KVM4 as a Docker container.
#
# Runs ON KVM4 (or via the runner shell). Builds the image locally from the
# two source files, then starts it with docker compose.
#
#   ./deploy_kvm4.sh            # build + start
#   ./deploy_kvm4.sh logs       # follow logs
#   ./deploy_kvm4.sh stop       # stop and remove
#
# Requires: docker + docker compose plugin, and a .env next to this script.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on this host" >&2
  exit 1
fi

case "${1:-up}" in
  up)
    if [ ! -f .env ]; then
      echo "error: .env missing — copy .env.example and fill in VASTAI_API + VAST_DASH_TOKEN" >&2
      exit 1
    fi
    grep -q '^VAST_DASH_TOKEN=..*' .env || { echo "error: VAST_DASH_TOKEN not set in .env" >&2; exit 1; }
    grep -q '^VASTAI_API=..*' .env || { echo "error: VASTAI_API not set in .env" >&2; exit 1; }
    docker compose up -d --build
    sleep 2
    docker compose ps
    port=$(grep -E '^DASH_PORT=' .env | cut -d= -f2 | tr -d ' ')
    bind=$(grep -E '^DASH_BIND=' .env | cut -d= -f2 | tr -d ' ')
    echo "dashboard -> http://${bind:-127.0.0.1}:${port:-8090}/"
    ;;
  logs)  docker compose logs -f --tail=100 ;;
  stop)  docker compose down ;;
  *)     echo "usage: $0 [up|logs|stop]" >&2; exit 2 ;;
esac
