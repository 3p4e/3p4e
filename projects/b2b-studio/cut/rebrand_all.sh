#!/bin/bash
set -e
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad; cd $S
echo "start $(date -u +%H:%M)"
bash fx/export.sh > rb_anim.log 2>&1; grep -q EXPORT_DONE rb_anim.log; echo "logo_anim $(date -u +%H:%M)"
python3 cut/posters_teasers.py > rb_previews.log 2>&1; echo "previews $(date -u +%H:%M)"
python3 cut/pitch_versions.py > rb_pitch.log 2>&1; echo "pitch $(date -u +%H:%M)"
python3 cut/explainers.py > rb_expl.log 2>&1; echo "explainers $(date -u +%H:%M)"
node cut/gen_pdfs.js > rb_pdf.log 2>&1; echo "pdfs $(date -u +%H:%M)"
python3 cut/gen_sites.py > rb_sites.log 2>&1; echo "sites $(date -u +%H:%M)"
echo REBRAND_RENDER_DONE
cd $S/pitch_site && tar cf $S/pitch_site.tar site nginx.conf docker-compose.yml && cd $S
python3 rput_par.py pitch_site.tar /opt/stacks/_upload pitch_site.tar > rb_up_site.log 2>&1; grep -q "CHECKSUM MATCH" rb_up_site.log
python3 rsh.py "set -e; cd /opt/stacks/ai-studio-pitch && rm -rf site && tar xf /opt/stacks/_upload/pitch_site.tar && rm /opt/stacks/_upload/pitch_site.tar && cp nginx.conf nginx.conf.bak 2>/dev/null; chmod -R a+rX site && docker compose up -d && docker compose restart >/dev/null 2>&1; sleep 3; docker ps --filter name=ai-studio-pitch --format '{{.Status}}'" 600 > rb_deploy.log
rm -f pitch_site.tar; echo "deployed $(date -u +%H:%M)"
rm -rf pkg_pm PITCH_MATERIALS_LTX.zip; mkdir -p pkg_pm/BIG_DOGMA_PITCH_MATERIALS_LTX/{brand,gfx,logo_animation}; P=pkg_pm/BIG_DOGMA_PITCH_MATERIALS_LTX
ln -s $S/pitch $P/1_pitch_16x9; ln -s $S/pitch_9x16 $P/2_pitch_9x16; ln -s $S/previews $P/3_posters_teasers; ln -s $S/offers_pdf $P/4_offer_pdfs; ln -s $S/explainers $P/5_how_its_made
cp brand/{logo.png,mark.svg,mark_bold.svg,mark_gold.png,mark_white.png,mark_black.png,icon_512.png,brand.json} $P/brand/; cp brand/fonts/RussoOne-400.ttf $P/brand/
cp brand/gfx/*.mov $P/gfx/; cp brand/anim/{dogma_logo_intro_1080p.mp4,dogma_logo_loop_1080p.mp4,dogma_logo_loop_36s_1080p.mp4,dogma_logo_loop.gif,dogma_logo_loop_alpha.webm,dogma_mark_loop_1080x1080.mp4} $P/logo_animation/
cp /home/user/3p4e/projects/b2b-studio/DELIVERY_AND_LICENCE.md $P/
B=https://pitch.bigdogma.tech; python3 -c "
import json;[print(k,'$B/'+v+'/') for k,v in json.load(open('cut/page_tokens.json')).items()]" > $P/PITCH_PAGE_LINKS.txt
cd pkg_pm && zip -q -r -0 ../BIG_DOGMA_PITCH_MATERIALS_LTX.zip BIG_DOGMA_PITCH_MATERIALS_LTX && cd ..
python3 rput_par.py BIG_DOGMA_PITCH_MATERIALS_LTX.zip /opt/stacks/abracadabra-v3/site/_dl_$(cat dltok) BIG_DOGMA_PITCH_MATERIALS_LTX.zip > rb_up_zip.log 2>&1; grep -q "CHECKSUM MATCH" rb_up_zip.log
echo "ALL_DONE $(date -u +%H:%M)"
