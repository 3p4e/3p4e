#!/usr/bin/env python3
"""Assemble the 65-clip K6 master in picture-lock order + verify joins."""
import os, subprocess, sys, glob
ORDER = ([f's{i:02d}' for i in range(1,21)] + [f'f{i:02d}' for i in range(1,11)]
         + [f's{i}' for i in range(26,61)])
SRC = 'media/perseus_assets/k6_clips'
def name(t): return f'{SRC}/p23_{t}_k6.mp4'
missing = [t for t in ORDER if not (os.path.exists(name(t)) and os.path.getsize(name(t))>100000)]
if missing:
    print(f'INCOMPLETE {len(ORDER)-len(missing)}/{len(ORDER)} | missing: {missing}'); sys.exit(2)
with open('/tmp/k6_concat.txt','w') as f:
    for t in ORDER: f.write(f"file '{os.path.abspath(name(t))}'\n")
os.makedirs('media/perseus_assets/k6_master', exist_ok=True)
out='media/perseus_assets/k6_master/p23_master_k6_v1.mp4'
r=subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','/tmp/k6_concat.txt',
  '-c:v','copy','-c:a','aac','-b:a','192k',out],capture_output=True,text=True)
if r.returncode: print('FFMPEG FAIL', r.stderr[-400:]); sys.exit(1)
pr=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,width,height,r_frame_rate','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True)
print('MASTER_OK', out, '| frames/dur:', pr.stdout.strip())
