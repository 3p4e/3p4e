#!/bin/bash
# Run on the owner's computer. Arranges the downloaded H3 parts (+ the 12 Japan-box films) into
# ~/Videos/BIG_DOGMA/H3 with the same folder layout as the LTX package. Uses hard links: no extra disk
# space, and the original part folders stay untouched (delete them yourself once the counts below match).
set -e
SRC=${1:-$HOME/Videos/H3_Assets/BIG_DOGMA_H3}
DST=$HOME/Videos/BIG_DOGMA/H3
mkdir -p "$DST" "$HOME/Videos/BIG_DOGMA/LTX"
put() { mkdir -p "$DST/$2"; for f in "$1"/*; do [ -f "$f" ] || continue; [ -e "$DST/$2/$(basename "$f")" ] || cp -l "$f" "$DST/$2/" 2>/dev/null || cp "$f" "$DST/$2/"; done; }
for p in "$SRC"/BIG_DOGMA_H3_part*; do
  [ -d "$p/films_16x9" ] && put "$p/films_16x9" 01_films_16x9
  [ -d "$p/films_9x16" ] && put "$p/films_9x16" 02_films_9x16
  [ -d "$p/pitch_16x9" ] && put "$p/pitch_16x9" 03_pitch_16x9
  [ -d "$p/pitch_9x16" ] && put "$p/pitch_9x16" 04_pitch_9x16
  [ -d "$p/feed_1x1" ] && put "$p/feed_1x1" 05_feed_1x1
  [ -d "$p/feed_4x5" ] && put "$p/feed_4x5" 06_feed_4x5
  [ -d "$p/subtitles" ] && put "$p/subtitles" 07_subtitles
  [ -d "$p/foton_action" ] && put "$p/foton_action" 08_foton_action
  [ -d "$p/raw_clips" ] && put "$p/raw_clips" 09_raw_clips/films
  [ -d "$p/raw_clips_foton_action" ] && put "$p/raw_clips_foton_action" 09_raw_clips/foton_action
  true
done
# the 12 films cut on the Japan box (finished films you already had)
for n in bw_commercial gener2_commercial concord_commercial viva_commercial zito_commercial vincinni_family_ad vincinni_factory_ad foton_tunland_v9_specs timelapse_construction timelapse_apartment_staging showreel_macedonian_industry foton_showreel_v2; do
  for v in "" _9x16; do
    d=01_films_16x9; [ "$v" = "_9x16" ] && d=02_films_9x16
    [ -e "$DST/$d/${n}_H3${v}.mp4" ] && continue
    f=$(find "$HOME/Videos" -type f -name "${n}_H3${v}.mp4" ! -path "$DST/*" 2>/dev/null | head -1)
    if [ -n "$f" ]; then cp -l "$f" "$DST/$d/" 2>/dev/null || cp "$f" "$DST/$d/"; else echo "not found: ${n}_H3${v}.mp4"; fi
  done
done
cat > "$DST/README.txt" <<'T'
BIG DOGMA - H3 version (Made with MiniMax H3). Concepts only, not for publication.
Licence: show only in person, outside the EU, UK, USA and South Korea. Do not upload, post, email or link these
files, do not put them on Google Drive or any cloud, do not let an AI assistant open them, do not train on them.
Same layout as the LTX package (BIG_DOGMA/LTX), folder for folder:
01_films_16x9  02_films_9x16  03_pitch_16x9  04_pitch_9x16  05_feed_1x1  06_feed_4x5  07_subtitles
08_foton_action (FALCON action film, reel, bumpers)  09_raw_clips (source clips)
For anything online, use the LTX version.
T
echo; echo "Expected: 01-06 = 44 each, 07 = 176, 08 = 4, 09 = 51"
for d in "$DST"/*/; do echo "$(basename "$d") $(find "$d" -type f | wc -l)"; done
