#!/bin/bash
# raw LTX clips -> board-ready assets/video/v3/<id>.mp4 (H.264, faststart, no audio) + .webm (VP9 fallback)
F=/usr/local/lib/python3.13/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2
IN=$1; OUT=$2; mkdir -p "$OUT"
for f in "$IN"/*.mp4; do
  n=$(basename "$f" .mp4)
  [ -s "$OUT/$n.webm" ] && continue
  $F -v error -y -i "$f" -an -c:v libx264 -profile:v high -level 4.1 -crf 21 -preset medium -pix_fmt yuv420p -movflags +faststart "$OUT/$n.mp4" &&
  $F -v error -y -i "$OUT/$n.mp4" -an -c:v libvpx-vp9 -crf 42 -b:v 0 -row-mt 1 -cpu-used 4 -pix_fmt yuv420p "$OUT/$n.webm" && echo "post $n"
done
