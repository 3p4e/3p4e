#!/bin/bash
# Runs three Wan 2.2 image-to-video tests on Karsus renders already placed in ComfyUI input/.
R=/workspace/ComfyUI_run; PY=/venv/main/bin/python
RAW=https://raw.githubusercontent.com/3p4e/3p4e/claude/elegant-thompson-uqhred/tools/vast
if ! curl -s -m 3 http://127.0.0.1:8199/system_stats >/dev/null; then
  echo "starting ComfyUI..."; (cd $R && setsid nohup $PY main.py --listen 127.0.0.1 --port 8199 > /workspace/comfy_run.log 2>&1 &)
  for i in $(seq 1 90); do sleep 4; curl -s -m 3 http://127.0.0.1:8199/system_stats >/dev/null && break; done
fi
curl -fsSL $RAW/run_wan_i2v.py -o /workspace/run_wan_i2v.py
NEG="blurry, distorted, morphing face, changing face, extra people, extra objects, flickering, text, watermark, jitter"
t(){ echo "=== $2"; $PY /workspace/run_wan_i2v.py --host http://127.0.0.1:8199 --imagefile "$1" --tag "$2" --w 832 --h 480 --negative "$NEG" --prompt "$3" 2>&1 | grep -E "DONE|ERROR|REJECTED|PREFLIGHT|queued"; }
ls $R/input/karsus_*.png || { echo "NO INPUT IMAGES in $R/input - upload the three karsus_*.png first"; exit 1; }
t karsus_closeup.png face_closeup "Close-up portrait of the king facing the camera, calm steady gaze, very subtle breathing, one slow blink, the jeweled crown glints softly, camera slowly pushes in, smooth and steady, no other moving objects."
t karsus_bust.png face_bust "Medium close-up of the archmage facing the camera, calm expression, a slight slow turn of the head to the left, the metal staff stays still, chain mail and cloak collar shimmer subtly, camera slowly pushes in, steady and smooth."
t karsus_medium.png face_medium "The archmage stands facing the camera against a stormy cloudy sky, calm expression, his cloak moves gently in the wind, the runes on the staff glow softly, camera slowly pushes in, steady and smooth, no other moving objects."
echo "FINISHED. Download these from $R/output : wan22_face_*.mp4"; ls -la $R/output/wan22_face_*.mp4
