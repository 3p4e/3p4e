#!/bin/bash
# ACE-Step 1.5 box setup (ffmpeg included), API server, then the v2 run.
cd /workspace
(apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg git curl python3 ca-certificates) >/dev/null 2>&1
command -v uv >/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh); export PATH=$HOME/.local/bin:$PATH
[ -d ACE-Step-1.5 ] || git clone -q https://github.com/ace-step/ACE-Step-1.5.git
cd ACE-Step-1.5 && uv sync 2>&1 | tail -2
nohup uv run acestep-api > /workspace/ace_api.log 2>&1 &
python3 /workspace/ace_run2.py > /workspace/ace_run2.log 2>&1
echo SETUP_AND_RUN_DONE
