#!/bin/bash
# Runs ON the India server: a marked copy of every H3 master (/opt/h3/marked/<same path>), MiniMax H3 credit bottom right,
# ~3 % of the short side high, original resolution and audio. Originals stay untouched as clean masters; hand out only marked copies.
MK=/opt/h3/tools/h3_mark.png; O=/opt/h3/marked; cd /opt/h3
find BIG_DOGMA_H3_* japan_films repitch -name "*.mp4" | sort | while read f; do
  t=$O/$f; [ -s "$t" ] && continue; mkdir -p "$(dirname "$t")"
  read w h < <(ffprobe -v 0 -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=" " "$f" </dev/null); m=$(( (w<h?w:h) * 3 / 100 )); g=$(( (w<h?w:h) * 15 / 1000 ))
  nice -n 15 ffmpeg -nostdin -v error -y -i "$f" -i $MK -filter_complex "[1]scale=-1:$m[m];[0][m]overlay=W-w-$g:H-h-$g[o]" \
    -map "[o]" -map 0:a? -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart -f mp4 "$t.part" && mv "$t.part" "$t" || echo "FAIL $f"
done; chmod -R a+rX $O; echo MARK_DONE $(find $O -name "*.mp4" | wc -l)
