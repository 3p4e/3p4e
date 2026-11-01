#!/usr/bin/env python3
"""Assemble the Wan 2.2 Karsus's Folly film on the Seedance new story timeline (about 122 s).
  assemble_wan_karsus.py --clips DIR --audio aud_v3.wav --endcard endcard6.mp4 --out OUT.mp4
Clips: DIR/wan22_<id>_832x480_*.mp4 (ids as in tools/vast/batch_karsus.py). 16 fps -> 24 fps, upscaled to 1280x720.
"""
import argparse, glob, os, subprocess, sys, tempfile
ap = argparse.ArgumentParser()
ap.add_argument("--clips", required=True); ap.add_argument("--audio", required=True); ap.add_argument("--endcard", required=True)
ap.add_argument("--out", required=True); ap.add_argument("--xf", type=float, default=0.25)
a = ap.parse_args()
SETS = [("sp1", ["sp1a","sp1b","sp1c"], 13.3), ("sp2", ["sp2a","sp2b","sp2c"], 13.0),
        ("sp3", ["sp3a","sp3b","sp3c","sp3d","sp3e"], 22.0), ("sp4", ["sp4a","sp4b","sp4c"], 15.0),
        ("sp4w", ["sp4wa","sp4wb"], 10.0), ("sp5s", ["sp5sa","sp5sb"], 10.0),
        ("sp5a", ["sp5a"], 8.0), ("sp5b", ["sp5b1","sp5b2","sp5b3"], 14.0), ("sp6", ["sp6a","sp6b","sp6c"], 12.0)]
def find(i):
    f = sorted(glob.glob(os.path.join(a.clips, f"wan22_{i}_*.mp4")) + glob.glob(os.path.join(a.clips, f"*{i}*.mp4")))
    if not f: sys.exit(f"missing clip {i}")
    return f[0]
def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def run(cmd): subprocess.run(cmd, check=True)
T = tempfile.mkdtemp(); parts = {}
NORM = "fps=24,scale=1280:720:flags=lanczos,setsar=1,format=yuv420p"
for name, ids, target in SETS:
    files = [find(i) for i in ids]; d = [dur(f) for f in files]
    ins = sum([["-i", f] for f in files], []); fc = []
    for k in range(len(files)): fc.append(f"[{k}:v]{NORM}[v{k}]")
    last = "v0"; acc = d[0]
    for k in range(1, len(files)):
        off = acc - a.xf
        fc.append(f"[{last}][v{k}]xfade=transition=fade:duration={a.xf}:offset={off:.4f}[x{k}]"); last = f"x{k}"; acc = off + d[k]
    total = acc
    if total < target: fc.append(f"[{last}]tpad=stop_mode=clone:stop_duration={target-total+0.1:.3f}[pad]"); last = "pad"
    fc.append(f"[{last}]trim=0:{target},setpts=PTS-STARTPTS[out]")
    out = os.path.join(T, f"{name}.mp4")
    run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[out]","-r","24","-c:v","libx264","-crf","16","-pix_fmt","yuv420p",out])
    parts[name] = out; print(f"{name}: raw {total:.2f}s -> {target}s")
# head = sp1..sp5a hard cuts (91.3 s), then 1.2 s dissolve into sp5b, then sp6 and the end card
lst = os.path.join(T, "head.txt"); open(lst, "w").write("".join(f"file '{parts[n]}'\n" for n in ["sp1","sp2","sp3","sp4","sp4w","sp5s","sp5a"]))
head = os.path.join(T, "head.mp4"); run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-r","24",head])
tail = os.path.join(T, "tail.txt"); open(tail, "w").write(f"file '{parts['sp6']}'\nfile '{os.path.abspath(a.endcard)}'\n")
tailv = os.path.join(T, "tail.mp4"); run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",tail,"-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-r","24",tailv])
hd = dur(head)
run(["ffmpeg","-v","error","-y","-i",head,"-i",parts["sp5b"],"-i",tailv,"-filter_complex",
     f"[0:v][1:v]xfade=transition=fade:duration=1.2:offset={hd-1.2:.3f},fps=24[x];[x][2:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
     "-map","[v]","-c:v","libx264","-crf","15","-r","24",os.path.join(T,"pic.mp4")])
run(["ffmpeg","-v","error","-y","-i",os.path.join(T,"pic.mp4"),"-i",a.audio,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",a.out])
print("wrote", a.out, f"{dur(a.out):.1f}s")
