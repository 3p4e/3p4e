#!/bin/bash
set -e
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad; F=$S/fx; O=$S/brand/anim; mkdir -p $O; cd $F
node render_logo_anim.js $S frames 0 6 30 $F/fr_intro 0 lockup > ex_intro.log
ffmpeg -v error -y -framerate 30 -i fr_intro/f_%05d.png -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -movflags +faststart $O/dogma_logo_intro_1080p.mp4
node render_logo_anim.js $S frames 15.5 27.5 30 $F/fr_loop 0 lockup > ex_loop.log
ffmpeg -v error -y -framerate 30 -i fr_loop/f_%05d.png -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -movflags +faststart $O/dogma_logo_loop_1080p.mp4
ffmpeg -v error -y -stream_loop 2 -i $O/dogma_logo_loop_1080p.mp4 -c copy $O/dogma_logo_loop_36s_1080p.mp4
ffmpeg -v error -y -i $O/dogma_logo_loop_1080p.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3" $O/dogma_logo_loop.gif
node render_logo_anim.js $S frames 15.5 27.5 30 $F/fr_alpha 1 lockup > ex_alpha.log
ffmpeg -v error -y -framerate 30 -i fr_alpha/f_%05d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le $O/dogma_logo_loop_alpha.mov
ffmpeg -v error -y -framerate 30 -i fr_alpha/f_%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 3M -auto-alt-ref 0 $O/dogma_logo_loop_alpha.webm
node render_logo_anim.js $S frames 15.5 27.5 30 $F/fr_sq 0 mark 1080 1080 > ex_sq.log
ffmpeg -v error -y -framerate 30 -i fr_sq/f_%05d.png -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -movflags +faststart $O/dogma_mark_loop_1080x1080.mp4
rm -rf fr_intro fr_loop fr_alpha fr_sq
echo EXPORT_DONE
