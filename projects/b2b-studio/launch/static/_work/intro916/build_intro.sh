#!/bin/bash
# post_hello_intro_9x16.mp4: 1080x1920 BD monogram ignition (0-7 s) + wordmark/tagline + AI disclosure.
# post_hello_intro_16x9.mp4: 1920x1080 horizontal lockup (0-6 s) + AI disclosure.
# Both are rendered by the video kit's renderer (launch/video/_work/logo_pipe.js + dogma_logo_kit.js): PNG frames are piped
# straight into ffmpeg (nothing is written to disk). The kit renderer keeps the wordmark's letter-spacing sweep small, so the
# 16:9 lockup stays inside the frame (the original brand/anim/dogma_logo_intro_1080p.mp4 sweeps the final "A" off the right edge).
# The AI line is on screen from the first frame (no fade-in).
# usage: bash build_intro.sh <S> [9x16|16x9|all]
set -e
S="$1"; WHAT="${2:-all}"; T="$S/launch/static/_work/intro916"; PIPE="$S/launch/video/_work/logo_pipe.js"
/usr/bin/python3 "$T/make_overlays.py" "$S"

if [ "$WHAT" = "all" ] || [ "$WHAT" = "9x16" ]; then
  OUT="$S/launch/static/post_hello_intro_9x16.mp4"
  # layout "mark" at 1080x2640 (identical in the kit and in fx/dogma_logo.js): the mark is centred at y=1320,
  # crop y 710..2630 puts it at y=610 (above the Reels/TikTok UI)
  nice -n 10 node "$PIPE" "$S" 0 7 30 mark 1080 2640 | nice -n 10 ffmpeg -v error -y -f image2pipe -framerate 30 -c:v png -i - \
    -loop 1 -framerate 30 -i "$T/ov_name.png" -loop 1 -framerate 30 -i "$T/ov_tag.png" -loop 1 -framerate 30 -i "$T/ov_ai.png" \
    -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -filter_complex "[0]crop=1080:1920:0:710,format=rgba[b];[1]format=rgba,fade=in:st=2.2:d=1.1:alpha=1[n];[2]format=rgba,fade=in:st=3.0:d=1.0:alpha=1[g];[3]format=rgba[a];[b][n]overlay=shortest=1[x];[x][g]overlay=shortest=1[y];[y][a]overlay=shortest=1,format=yuv420p[v]" \
    -map "[v]" -map 4:a -t 7 -r 30 -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart "$OUT"
  echo "wrote $OUT"
fi

if [ "$WHAT" = "all" ] || [ "$WHAT" = "16x9" ]; then
  # 16:9 companion for LinkedIn / Facebook / X: layout "lockup" (mark left, wordmark right), same timing as the brand intro
  OUT2="$S/launch/static/post_hello_intro_16x9.mp4"
  nice -n 10 node "$PIPE" "$S" 0 6 30 lockup 1920 1080 | nice -n 10 ffmpeg -v error -y -f image2pipe -framerate 30 -c:v png -i - \
    -loop 1 -framerate 30 -i "$T/ov_ai_169.png" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -filter_complex "[1]format=rgba[a];[0]format=rgba[b];[b][a]overlay=shortest=1,format=yuv420p[v]" \
    -map "[v]" -map 2:a -t 6 -r 30 -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart "$OUT2"
  echo "wrote $OUT2"
fi
