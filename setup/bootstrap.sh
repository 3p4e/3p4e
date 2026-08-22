#!/usr/bin/env bash
set -euo pipefail

# 3p4e workspace bootstrap — one command to a fully equipped dev box.
# Target: Ubuntu/Debian (e.g. a Hostinger VPS running code-server).
# Idempotent: safe to re-run any time; it skips what is already installed.
#
# Usage (from the code-server terminal):
#   git clone https://github.com/3p4e/3p4e && cd 3p4e && ./setup/bootstrap.sh

log() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else
    echo "This script needs root or sudo for system packages." >&2; exit 1
  fi
fi

log "System packages (git, build tools, python, media tooling)"
export DEBIAN_FRONTEND=noninteractive
$SUDO apt-get update -y -qq
$SUDO apt-get install -y -qq \
  git curl wget unzip jq ripgrep tmux htop \
  build-essential pkg-config \
  python3 python3-pip python3-venv \
  ffmpeg imagemagick

log "Node.js 22 via nvm (user-local, no sudo for npm -g)"
export NVM_DIR="$HOME/.nvm"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
# shellcheck disable=SC1091
. "$NVM_DIR/nvm.sh"
nvm install 22 >/dev/null 2>&1 || nvm install 22
nvm alias default 22 >/dev/null
echo "node $(node --version) / npm $(npm --version)"

log "Global CLIs: Higgsfield + Claude Code"
npm install -g @higgsfield/cli @anthropic-ai/claude-code
higgsfield version || true
claude --version || true

log "Higgsfield companion skills"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
if [ -d .agents/skills/higgsfield-generate ]; then
  echo "skills already vendored in repo — nothing to do"
else
  npx --yes skills add higgsfield-ai/skills
fi

log "code-server extensions (skipped if code-server not on PATH)"
if command -v code-server >/dev/null 2>&1; then
  for ext in ms-python.python dbaeumer.vscode-eslint esbenp.prettier-vscode; do
    code-server --install-extension "$ext" >/dev/null 2>&1 || true
  done
  echo "extensions installed"
else
  echo "code-server not found on PATH — skipping extensions"
fi

log "Done"
cat <<'EOF'

Next steps:
  1. Authenticate the Higgsfield CLI (headless-safe):
       ./setup/hf-auth-remote.sh
  2. Authenticate Claude Code: run `claude` and follow the login prompt.
  3. Work from this folder in code-server. With Claude Code running in the
     terminal, project dependencies get installed on demand as you build —
     there is no need to pre-install every language runtime up front.
EOF
