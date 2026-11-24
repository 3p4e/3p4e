#!/bin/bash
# 9:16 (1080x1920) versions: blurred full-bleed background + the 16:9 film centred; audio unchanged.
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad
for d in final_commercials final_commercials_b2; do
  for f in $S/$d/*.mp4; do
    o=$S/vertical/$(basename $f .mp4)_9x16.mp4; [ -f $o ] && continue
    ffmpeg -v error -y -i $f -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart $o && echo "OK $(basename $o)"
  done
done
echo VERTICAL_DONE
