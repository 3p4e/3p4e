#!/usr/bin/env python3
import os, subprocess, json, sys

CLIPS = os.environ.get("CLIPS", "/workspace/out")
OUTD  = os.environ.get("OUTD", "/workspace/film")
os.makedirs(OUTD, exist_ok=True)
ORDER = ["p1_1", "p1_2", "p1_3", "p1_4a"]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stderr or "")

sel = []
for sid in ORDER:
    pick = None
    for cand in (f"k6_{sid}_1080.mp4", f"k6_{sid}_gen.mp4"):
        p = os.path.join(CLIPS, cand)
        if os.path.exists(p) and os.path.getsize(p) > 20000:
            pick = p; break
    if not pick:
        print(f"MISSING {sid}"); sys.exit(2)
    print(f"use {sid}: {pick} {os.path.getsize(pick)/1e6:.1f}MB")
    sel.append((sid, pick))

# normalize -> uniform 1920x1080 24fps stereo 48k
norm = []
for i, (sid, c) in enumerate(sel):
    n = os.path.join(OUTD, f"n{i}_{sid}.mp4")
    rc, err = run(["ffmpeg","-y","-i",c,
        "-vf","scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=24",
        "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
        "-af","aresample=48000,aformat=channel_layouts=stereo",
        "-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-shortest",n])
    if rc != 0:
        print(f"norm fail {sid}: {err[-900:]}"); sys.exit(3)
    norm.append(n); print(f"norm ok {sid}")

lst = os.path.join(OUTD,"c1.txt")
open(lst,"w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in norm))
body = os.path.join(OUTD,"body.mp4")
rc, err = run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",body])
if rc != 0:
    print("concat fail", err[-900:]); sys.exit(4)
print("body ok")

# title card from textfiles
t1 = os.path.join(OUTD,"t1.txt"); open(t1,"w").write("THE PALADIN'S JUDGEMENT")
t2 = os.path.join(OUTD,"t2.txt"); open(t2,"w").write("-339 DR  \u00b7  the day the runes answered")
t3 = os.path.join(OUTD,"t3.txt"); open(t3,"w").write("a fan work  \u00b7  unofficial  \u00b7  not for sale")
vf = (",".join([
  f"drawtext=textfile={t1}:fontcolor=0xF2E4C0:fontsize=76:x=(w-text_w)/2:y=(h-text_h)/2-70:shadowcolor=black@0.9:shadowx=3:shadowy=3",
  f"drawtext=textfile={t2}:fontcolor=0xB8C2CC:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2+70:shadowcolor=black@0.9:shadowx=2:shadowy=2",
  f"drawtext=textfile={t3}:fontcolor=0x8892A0:fontsize=22:x=(w-text_w)/2:y=h-96",
  "fade=t=in:st=0:d=0.5",
]))
card = os.path.join(OUTD,"card.mp4")
rc, err = run(["ffmpeg","-y","-f","lavfi","-i","color=c=0x0B1016:s=1920x1080:d=2.4:r=24",
    "-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-vf",vf,
    "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
    "-c:a","aac","-b:a","192k","-ac","2","-ar","48000","-shortest",card])
if rc != 0:
    print("card fail", err[-900:]); card = None
else:
    print("card ok")

final = os.path.join(OUTD,"THE_PALADINS_JUDGEMENT_1080p24.mp4")
if card:
    lst2 = os.path.join(OUTD,"c2.txt")
    open(lst2,"w").write(f"file '{os.path.abspath(body)}'\nfile '{os.path.abspath(card)}'\n")
    rc, err = run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst2,
        "-c:v","libx264","-preset","slow","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",final])
else:
    rc, err = run(["ffmpeg","-y","-i",body,"-c:v","libx264","-preset","slow","-crf","18",
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000",
        "-movflags","+faststart",final])
if rc != 0:
    print("final fail", err[-1200:]); sys.exit(5)

pr = subprocess.run(["ffprobe","-v","error","-show_entries",
    "format=duration,size:stream=codec_name,width,height,r_frame_rate,channels,sample_rate",
    "-of","json",final], capture_output=True, text=True)
print("FINAL", final, os.path.getsize(final))
print(pr.stdout)
json.dump({"final":final,"probe":json.loads(pr.stdout)}, open(os.path.join(OUTD,"assemble.json"),"w"), indent=2)
print("ASSEMBLE OK")
