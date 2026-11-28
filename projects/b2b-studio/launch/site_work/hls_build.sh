#!/bin/bash
# Adaptive streaming copies (HLS) of every film with a player, built ON the Mumbai server (it holds all sources; owner 2026-11-27:
# "720p versions and one or two lower resolutions, the real originals never on the web page"):
#   <dir>/<name>.mp4  ->  <dir>/hls/<name>/master.m3u8 + v0 (720p) v1 (480p) v2 (360p), 4 s segments, keyframe every 2 s.
# Sources: the v3 category-film masters (/opt/bd_masters/catfilms_v3) where they exist, else the 720p web copy itself.
# Identical sources (company pages share files) are encoded once (cache by md5) and hard-linked. Loops under 8 s are skipped.
# Runs at the lowest CPU/IO priority with one thread so the site keeps answering.   bash hls_build.sh [list-file]
SITE=/opt/stacks/bigdogma-site/site; PITCH=/opt/stacks/ai-studio-pitch/site; MAST=/opt/bd_masters/catfilms_v3
CACHE=/opt/stacks/hls_cache; LOG=/opt/stacks/hls_build.log; mkdir -p $CACHE
list() {   # priority: studio site films, showreel and how-to, then the company pages
  ls $SITE/films/*.mp4
  for n in showreel showreel_9x16 howto; do [ -f $SITE/media/$n.mp4 ] && echo $SITE/media/$n.mp4; done
  ls $PITCH/*/*.mp4 2>/dev/null
}
enc() {   # $1 source  $2 output dir (built in a temp dir, moved into place when complete)
  local src=$1 out=$2 tmp=$2.tmp.$$ wh w h a vs
  wh=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$src"); w=${wh%,*}; h=${wh#*,}
  if [ "$w" -ge "$h" ]; then vs="[a]scale=1280:-2[v0];[b]scale=854:-2[v1];[c]scale=640:-2[v2]"; else vs="[a]scale=-2:1280[v0];[b]scale=-2:854[v1];[c]scale=-2:640[v2]"; fi
  a=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src" | head -1)
  rm -rf "$tmp"; mkdir -p "$tmp"
  local AM=() VM="v:0 v:1 v:2" AC=()
  if [ -n "$a" ]; then AM=(-map 0:a:0 -map 0:a:0 -map 0:a:0); VM="v:0,a:0 v:1,a:1 v:2,a:2"
    AC=(-c:a aac -ar 48000 -ac 2 -b:a:0 128k -b:a:1 96k -b:a:2 64k); fi
  nice -n 19 ionice -c3 ffmpeg -v error -y -threads 1 -i "$src" -filter_complex "[0:v]fps=24,split=3[a][b][c];$vs" \
    -map "[v0]" -map "[v1]" -map "[v2]" "${AM[@]}" -c:v libx264 -preset veryfast -profile:v main -pix_fmt yuv420p \
    -g 48 -keyint_min 48 -sc_threshold 0 -crf:v:0 23 -maxrate:v:0 1400k -bufsize:v:0 2800k -crf:v:1 24 -maxrate:v:1 750k -bufsize:v:1 1500k \
    -crf:v:2 25 -maxrate:v:2 420k -bufsize:v:2 840k "${AC[@]}" -f hls -hls_time 4 -hls_playlist_type vod \
    -hls_segment_filename "$tmp/v%v/s%03d.ts" -master_pl_name master.m3u8 -var_stream_map "$VM" "$tmp/v%v/index.m3u8" || { rm -rf "$tmp"; return 1; }
  chmod -R a+rX "$tmp"; rm -rf "$out"; mv "$tmp" "$out"
}
n=0; ok=0; skip=0
for f in $( [ -n "$1" ] && cat "$1" || list ); do
  n=$((n+1)); d=$(dirname $f); b=$(basename $f .mp4); out=$d/hls/$b
  [ -f $out/master.m3u8 ] && [ $out/master.m3u8 -nt $f ] && { skip=$((skip+1)); continue; }
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f | cut -d. -f1); [ "${dur:-0}" -lt 8 ] && { skip=$((skip+1)); continue; }
  src=$f; [ -f $MAST/$b.mp4 ] && src=$MAST/$b.mp4
  key=$(md5sum $src | cut -c1-16)
  if [ ! -f $CACHE/$key/master.m3u8 ]; then enc $src $CACHE/$key || { echo "$(date +%T) FAIL $f" >> $LOG; continue; }; fi
  mkdir -p $d/hls; rm -rf $out; cp -al $CACHE/$key $out && ok=$((ok+1)) && echo "$(date +%T) OK $out" >> $LOG
done
echo "$(date +%T) HLS_DONE files $n built/linked $ok skipped $skip" >> $LOG
