#!/bin/bash
# Runs ON the India server: web copies of the H3 versions of the 19 public studio films for bigdogma.tech/h3/ (geo-gated),
# 720p with the MiniMax H3 corner credit, plus posters. timelapse_renovation stays out, as on the site.
set -e; O=${O:-/opt/h3/web/_site}; MK=/opt/h3/tools/h3_mark.png; BD=/opt/h3/tools/bd_logo.png; P1=/opt/h3/BIG_DOGMA_H3_part1/films_16x9; mkdir -p $O
src() { case $1 in timelapse_office_fitout) echo /opt/h3/BIG_DOGMA_H3_part3/films_16x9/$1_H3.mp4;;
  showreel_macedonian_industry|timelapse_apartment_staging|timelapse_construction) echo /opt/h3/japan_films/$1_H3.mp4;; *) echo $P1/$1_H3.mp4;; esac; }
for f in sector_automotive sector_food sector_pharma sector_wine sector_steel_cement sector_real_estate sector_recruitment sector_product_launch \
  showreel_macedonian_industry timelapse_construction timelapse_developer timelapse_apartment_staging timelapse_interior_design timelapse_office_fitout \
  timelapse_store_fitout timelapse_expo_stand timelapse_landscaping timelapse_solar timelapse_road; do
  [ -s $O/$f.mp4 ] || nice -n 5 ffmpeg -nostdin -v error -y -i "$(src $f)" -i $MK -i $BD -filter_complex "[0]scale=1280:-2[v];[1]scale=-1:22[m];[2]scale=-1:34,format=rgba,colorchannelmixer=aa=0.85[b];[v][m]overlay=W-w-18:H-h-16[vm];[vm][b]overlay=16:14[o]" \
    -map "[o]" -map 0:a? -c:v libx264 -crf 24 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $O/$f.mp4
  [ -s $O/$f.jpg ] || ffmpeg -nostdin -v error -y -ss 4 -i $O/$f.mp4 -frames:v 1 -vf scale=960:-2 -q:v 4 $O/$f.jpg; echo "ok $f"
done; chmod -R a+rX $O; echo SITE_WEB_DONE $(ls $O/*.mp4 | wc -l)
