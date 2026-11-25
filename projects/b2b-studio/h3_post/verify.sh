#!/bin/bash
# Text-only checks of the H3 finishing outputs on the box (counts, durations, streams, subtitle hits).
cd /workspace
for d in h3_commercials h3_commercials_9x16 h3_pitch h3_pitch_9x16 h3_feed_1x1 h3_feed_4x5; do
  n=$(ls $d/*.mp4 2>/dev/null | wc -l); bad=0; dims=""
  for f in $d/*.mp4; do
    s=$(ffprobe -v error -show_entries stream=codec_type,width,height -of csv=p=0 "$f" | tr '\n' ' ')
    echo "$s" | grep -q audio || bad=$((bad+1)); dims="$dims$(echo "$s" | grep -oE '[0-9]+,[0-9]+' | head -1)\n"
  done
  echo "$d n=$n noaudio=$bad dims=$(printf "$dims" | sort | uniq -c | tr '\n' ' ')"
done
echo "subs: $(ls h3_subs/*.srt 2>/dev/null | wc -l) files"; grep ^SUBS h3post.log | awk '{print $2, $3"/"$5}' | tr '\n' ' '; echo
for f in h3_commercials/*_H3.mp4; do n=$(basename $f _H3.mp4)
  a=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f); b=$(ffprobe -v error -show_entries format=duration -of csv=p=0 h3_pitch/${n}_H3_pitch.mp4 2>/dev/null)
  printf "%s %.1f->%.1f  " $n $a $b; done; echo
grep -E "^(ERR|SKIP)" h3post.log h3cut_now.log | head
du -sh h3_commercials h3_commercials_9x16 h3_pitch h3_pitch_9x16 h3_feed_1x1 h3_feed_4x5 h3_subs | tr '\n' ' '; echo
