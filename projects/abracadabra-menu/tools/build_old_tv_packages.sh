#!/usr/bin/env sh
# usage: tools/build_old_tv_packages.sh <folder-with-the-4-rendered-MP4s> [out-dir]
# Builds two zips: ABRACADABRA_OLD_TV_VIDEOS.zip (what goes on the USB stick: 4 MP4 + 720p copies + guide)
#              and ABRACADABRA_OLD_TV_PRICE_EDITOR.zip (stays on a computer: admin page, menu data, render tool).
set -e
cd "$(dirname "$0")/.."
VID=${1:?folder with TV1_DAY.MP4 TV1_NIGHT.MP4 TV2_DAY.MP4 TV2_NIGHT.MP4}; OUT=${2:-dist-old-tv}
rm -rf "$OUT"; mkdir -p "$OUT/ABRACADABRA_OLD_TV/720p" "$OUT/PRICE_EDITOR/assets/video/ltx25" "$OUT/PRICE_EDITOR/output"
for f in TV1_DAY TV1_NIGHT TV2_DAY TV2_NIGHT; do
  cp "$VID/$f.MP4" "$OUT/ABRACADABRA_OLD_TV/$f.MP4"
  ffmpeg -v error -y -i "$VID/$f.MP4" -vf "scale=1280:720:flags=lanczos,format=yuv420p" -c:v libx264 -profile:v main -level 3.1 -crf 27 -preset slow -g 60 -c:a aac -b:a 64k -movflags +faststart "$OUT/ABRACADABRA_OLD_TV/720p/$f.MP4"
done
cp usb-old-tv/УПАТСТВО_INSTRUCTIONS.html "$OUT/ABRACADABRA_OLD_TV/"
cp admin.html menu-data.js cinematic-board.html "$OUT/PRICE_EDITOR/"
[ -d assets/css ] && cp -r assets/css "$OUT/PRICE_EDITOR/assets/" || true
cp -r assets/fonts assets/logo.png assets/mascot_day.png assets/mascot_night.png assets/stage_day.jpg assets/stage_night.jpg "$OUT/PRICE_EDITOR/assets/"
cp assets/clip-map-ltx25.js "$OUT/PRICE_EDITOR/assets/"
for n in bg_day bg_night wand_idle_day wand_idle_night wand_burger wand_waffle wand_wrap fx_slash cine_awakening_day cine_neon_night cine_summon_burger cine_summon_waffle cine_summon_wrap; do
  cp "assets/video/ltx25/$n.mp4" "$OUT/PRICE_EDITOR/assets/video/ltx25/"
done
mkdir -p "$OUT/PRICE_EDITOR/tools"; cp tools/render_menu_video.mjs tools/package.json tools/SETUP.bat tools/RENDER_ALL.bat tools/render_all.sh "$OUT/PRICE_EDITOR/tools/"
cp usb-old-tv/УПАТСТВО_INSTRUCTIONS.html "$OUT/PRICE_EDITOR/"
(cd "$OUT" && zip -qr ABRACADABRA_OLD_TV_VIDEOS.zip ABRACADABRA_OLD_TV && zip -qr ABRACADABRA_OLD_TV_PRICE_EDITOR.zip PRICE_EDITOR)
ls -la "$OUT"/*.zip
