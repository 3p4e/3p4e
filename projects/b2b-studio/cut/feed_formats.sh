#!/bin/bash
# 1:1 (1080x1080) and 4:5 (1080x1350) feed versions of every clean LTX master (final_music), blurred-fill background
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad; mkdir -p $S/final_1x1 $S/final_4x5
for f in $S/final_music/*.mp4; do n=$(basename $f .mp4)
  for spec in "1x1 1080 1080" "4x5 1080 1350"; do set -- $spec; o=$S/final_$1/${n}_$1.mp4; [ -s $o ] && continue
    nice -n 12 ffmpeg -v error -y -i $f -filter_complex "[0:v]split[a][b];[a]scale=$2:$3:force_original_aspect_ratio=increase,crop=$2:$3,gblur=sigma=36,eq=brightness=-0.14:saturation=0.9[bg];[b]scale=$2:-2[fg];[bg][fg]overlay=0:(H-h)/2" \
      -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart $o && echo "OK $n $1"
  done
done
echo FEED_DONE
