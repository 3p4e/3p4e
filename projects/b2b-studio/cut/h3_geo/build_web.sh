#!/bin/bash
# Runs ON the India server: web versions of the H3 pitch films per company page (/opt/h3/web/<page token>/), 720p, plus posters.
# Source: /opt/h3/BIG_DOGMA_H3_part5_new_contact (studio email version) + Foton action set (part 2). Nothing leaves the server.
set -e; SRC=/opt/h3/BIG_DOGMA_H3_part5_new_contact; A=/opt/h3/BIG_DOGMA_H3_part2_foton_action/foton_action; W=/opt/h3/web
declare -A MAP=( [mh40CJuLNCeMzLTm]="zito_commercial zito_opening_film" [i74MTMTJekUSYz2u]="alkaloid_commercial alkaloid_employer_film"
 [5tkydceqTrM71scq]="replek_commercial replek_export_film" [h0JdjqNfAduvHnbi]="vincinni_factory_ad vincinni_family_ad"
 [t-pjg2dGccmtOp4M]="foton_tunland_v9_specs foton_showreel_v2" [qF6rpuvU2It2Vhuu]="bw_commercial bw_riverside_film"
 [PwJCNU7XqCl7qemN]="millennium_commercial millennium_capability_film" [omhXHETbScMqI9fQ]="nelt_commercial nelt_logistics_film"
 [5hrXPXG9VgvRb6Zv]="gener2_commercial gener2_builder_film" [CgkdpzGtS0AYMLuG]="concord_commercial concord_offplan_film"
 [GScktP6h2Xg5Z2Qt]="viva_commercial viva_expansion_film" [T3yr_acSjgRXjO8A]="speeex_commercial speeex_recruitment_film" )
enc() { [ -s "$2" ] || ffmpeg -v error -y -i "$1" -vf "scale='if(gt(iw,ih),1280,-2)':'if(gt(iw,ih),-2,1280)'" -c:v libx264 -crf 24 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$2"
        [ -s "${2%.mp4}.jpg" ] || ffmpeg -v error -y -ss 3 -i "$2" -frames:v 1 -vf "scale='if(gt(iw,ih),960,-2)':'if(gt(iw,ih),-2,960)'" -q:v 4 "${2%.mp4}.jpg"; }
for tok in "${!MAP[@]}"; do mkdir -p $W/$tok
  for f in ${MAP[$tok]}; do enc $SRC/pitch_16x9/${f}_H3_pitch.mp4 $W/$tok/${f}.mp4; [ -f $SRC/pitch_9x16/${f}_H3_pitch_9x16.mp4 ] && enc $SRC/pitch_9x16/${f}_H3_pitch_9x16.mp4 $W/$tok/${f}_9x16.mp4 || true; done
  if [ $tok = t-pjg2dGccmtOp4M ]; then for f in foton_action_30s foton_action_reel_15s_9x16; do enc $A/$f.mp4 $W/$tok/$f.mp4; done; fi
  echo "$tok $(ls $W/$tok/*.mp4 | wc -l)"; done
chmod -R a+rX $W; du -sh $W
