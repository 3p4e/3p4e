#!/bin/bash
# Kill any stale upgrade/boot processes, then start the patched torch upgrade.
# Written as a file because inline SSH heredocs kept vanishing silently.
set -uo pipefail
export LC_ALL=C.UTF-8

echo "[L $(date -u +%H:%M:%S)] killing stale processes"
pkill -9 -f upgrade_torch.sh 2>/dev/null || true
pkill -9 -f 'main.py.*8188' 2>/dev/null || true
sleep 2

rm -f /workspace/torch_up.log /workspace/torch_up_pip.log

echo "[L $(date -u +%H:%M:%S)] pin in script:"
grep -n 'torch==' /workspace/upgrade_torch.sh

echo "[L $(date -u +%H:%M:%S)] launching"
setsid nohup bash /workspace/upgrade_torch.sh < /dev/null > /workspace/launch.out 2>&1 &
disown

sleep 10
echo "[L $(date -u +%H:%M:%S)] running processes:"
pgrep -af upgrade_torch.sh | head -3
echo "[L $(date -u +%H:%M:%S)] pip running:"
pgrep -af 'pip install' | head -3
echo "[L $(date -u +%H:%M:%S)] log so far:"
tail -5 /workspace/torch_up.log 2>/dev/null || echo "no log yet"
echo "[L $(date -u +%H:%M:%S)] LAUNCH_DONE"
