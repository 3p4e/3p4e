#!/bin/bash
# Build the v3 audio track from individual stems, timed to the v3 cut order.
# K4 ("Be unmade.") and M4 ("It is too much, Karsus.") are deliberately absent:
# no TTS yet, and per the script a stranger's synthesised voice is worse than silence.
set -e
A=media/audio
OUT=media/audio/aud_v3.wav
DUR=118.125

filter="[0:a]volume=1.0[sc];\
[sc]volume=0:enable='between(t,58.3,63.3)'[sc2];\
[sc2]volume=0:enable='between(t,83.3,89.3)'[sc3];\
[sc3]volume=0.85,apad,atrim=0:${DUR},asetpts=PTS-STARTPTS[score];\
[1:a]adelay=13600|13600,volume=1.0[d1];\
[2:a]adelay=42300|42300,volume=1.0[d2];\
[3:a]adelay=48600|48600,volume=1.0[d3];\
[4:a]adelay=53600|53600,volume=1.0[d4];\
[5:a]adelay=63600|63600,volume=1.0[d5];\
[6:a]adelay=100900|100900,volume=1.0[d6];\
[d1][d2][d3][d4][d5][d6]amix=inputs=6:duration=longest:normalize=0,apad,atrim=0:${DUR},asetpts=PTS-STARTPTS[dlg];\
[score][dlg]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:${DUR},alimiter=limit=0.95,asetpts=PTS-STARTPTS[a]"

ffmpeg -hide_banner -loglevel error -y \
  -i $A/score_lyria.mp3 \
  -i $A/stems/K1.wav \
  -i $A/stems/K2.wav \
  -i $A/stems/M12.wav \
  -i $A/stems/K3.wav \
  -i $A/stems/M3.wav \
  -i $A/E.wav \
  -filter_complex "$filter" -map "[a]" -ar 48000 -ac 2 "$OUT"

ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
