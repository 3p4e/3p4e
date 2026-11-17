#!/bin/bash
# ComfyUI main.py imports 'comfy_aimdo', which is absent and NOT declared in
# requirements.txt. Do not install an unknown package blindly: inspect first.
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/inspect_aimdo.log
say(){ echo "[INSP $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

CDIR=/workspace/ComfyUI
cd $CDIR || { say FATAL_NO_DIR; exit 1; }

say "--- git identity ---"
git remote -v 2>&1 | head -4
git log -1 --format='commit %H%nauthor %an <%ae>%ndate %ad%nsubject %s' 2>&1
say "--- branches ---"
git rev-parse --abbrev-ref HEAD 2>&1

say "--- the import in main.py ---"
grep -n 'comfy_aimdo' main.py 2>&1
say "--- surrounding context (lines around each match) ---"
awk '/comfy_aimdo/{for(i=NR-6;i<=NR+10;i++) want[i]=1} {lines[NR]=$0} END{for(i=1;i<=NR;i++) if(i in want) printf "%5d  %s\n", i, lines[i]}' main.py 2>&1 | head -40

say "--- is it declared anywhere in the repo? ---"
grep -rn 'comfy_aimdo' --include='*.txt' --include='*.py' --include='*.toml' --include='*.md' . 2>/dev/null | grep -v '^./main.py' | head -10 || say "no other references"

say "--- does the package exist on PyPI? ---"
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 https://pypi.org/pypi/comfy_aimdo/json 2>/dev/null)
say "pypi_status $code"
if [ "$code" = "200" ]; then
  say "PACKAGE EXISTS on PyPI — inspect its metadata:"
  python3 - <<'PY'
import json,urllib.request
j=json.load(urllib.request.urlopen('https://pypi.org/pypi/comfy_aimdo/json',timeout=20))
i=j['info']
print('name',i.get('name'))
print('version',i.get('version'))
print('author',i.get('author'))
print('home',i.get('home_page'))
print('urls',[u.get('url') for u in (i.get('project_urls') or {}).items()][:3])
PY
else
  say "PACKAGE ABSENT from PyPI — do not pip install; pin a release tag instead"
fi

say "--- available release tags (sanity of this fork) ---"
git ls-remote --tags origin 2>/dev/null | tail -5 || say "no tag access"

say "INSPECT_DONE"
