#!/bin/bash
# Hard-link finished H3 outputs into one download folder (no extra disk). Usage: pack.sh <folder name>; only files
# not already in an earlier BIG_DOGMA_H3_* folder are linked, so each part holds only what is new.
cd /workspace; P=$1; mkdir -p $P
declare -A M=([h3_commercials]=films_16x9 [h3_commercials_9x16]=films_9x16 [h3_pitch]=pitch_16x9 [h3_pitch_9x16]=pitch_9x16 [h3_feed_1x1]=feed_1x1 [h3_feed_4x5]=feed_4x5 [h3_subs]=subtitles [h3_foton_action]=foton_action)
n=0
for s in "${!M[@]}"; do [ -d $s ] || continue; for f in $s/*; do [ -f "$f" ] || continue; b=$(basename "$f")
  ls BIG_DOGMA_H3_*/${M[$s]}/"$b" >/dev/null 2>&1 && continue
  mkdir -p $P/${M[$s]}; ln "$f" $P/${M[$s]}/"$b" && n=$((n+1)); done; done
cat > $P/README.txt <<'T'
BIG DOGMA - H3 films (Made with MiniMax H3). Concepts only, not for publication.
Licence: show only in person, outside the EU, UK, USA and South Korea. Do not upload, post, email or link these
files, do not put them on Google Drive or any cloud, and do not use them to train models. Keep the "Made with
MiniMax H3" credit. For anything online use the LTX versions.
films_*: the films. pitch_*: with the BIG DOGMA intro, concept watermark and contact outro (for meetings).
feed_*: 1:1 and 4:5. subtitles: .srt in mk / sr / sq / en, same timing as films_* (pitch adds 2.2 s intro).
T
echo "$P files=$n $(du -sh $P | cut -f1)"; find $P -mindepth 1 -maxdepth 1 -type d -printf "%f " ; echo
