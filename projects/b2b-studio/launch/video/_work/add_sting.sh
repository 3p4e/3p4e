#!/bin/bash
# Appends the BIG DOGMA logo outro (AI smoke_reveal render, seg/outro_16x9.mp4 / outro_9x16.mp4) to a finished film (owner 2026-11-27:
# the company films' last frame had no studio logo). usage: add_sting.sh <film.mp4> <out.mp4> <sting16x9.mp4> <sting9x16.mp4>
set -e
F="$1"; O="$2"; ST16="$3"; ST9="$4"
read W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$F" | tr x ' ')
if [ "$H" -gt "$W" ]; then ST="$ST9"; else ST="$ST16"; fi
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$F" | head -1)
HAS_A=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$F" | head -1)
SD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ST")
if [ -n "$HAS_A" ]; then
  ffmpeg -nostdin -v error -y -i "$F" -i "$ST" -f lavfi -t "$SD" -i anullsrc=r=48000:cl=stereo -filter_complex \
   "[1:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=${FPS},setsar=1,format=yuv420p[s];[0:v]fps=${FPS},setsar=1,format=yuv420p[m];[0:a]aresample=48000,aformat=channel_layouts=stereo[ma];[m][ma][s][2:a]concat=n=2:v=1:a=1[v][a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$O"
else
  ffmpeg -nostdin -v error -y -i "$F" -i "$ST" -filter_complex "[1:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=${FPS},setsar=1,format=yuv420p[s];[0:v]fps=${FPS},setsar=1,format=yuv420p[m];[m][s]concat=n=2:v=1:a=0[v]" \
   -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart "$O"
fi
