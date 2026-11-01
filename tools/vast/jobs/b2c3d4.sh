echo "== input dir"; ls -la /workspace/ComfyUI_run/input | tail -8
echo "== gpu"; nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader
echo "== comfy"; curl -s -m 3 http://127.0.0.1:8199/system_stats | head -c 120; echo
