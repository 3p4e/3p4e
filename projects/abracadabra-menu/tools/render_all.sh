#!/usr/bin/env sh
# Mac/Linux: renders TV1/TV2 x DAY/NIGHT into ../output. Needs Node 18+, ffmpeg, and one-time: npm install && npx playwright install chromium
set -e
cd "$(dirname "$0")"
mkdir -p ../output
for s in 1 2; do for m in day night; do
  echo "=== TV$s $m ==="
  node render_menu_video.mjs --screen $s --mode $m --out "../output/TV${s}_$(echo $m | tr a-z A-Z).MP4"
done; done
echo "Done. Copy the 4 files from ../output to the USB stick."
