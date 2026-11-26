# Web encodes of the finished category films for bigdogma.tech: launch/site/films/<id>.mp4 (720p, crf 26, AAC 128k) + <id>.jpg poster
# (taken from the middle of the film, before the end card). Only films that are cut are encoded; re-runs skip done ones.
import os, glob, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; CUTS = f"{S}/catfilms/cuts"; OUT = f"{S}/launch/site/films"
os.makedirs(OUT, exist_ok=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
n = 0
for src in sorted(glob.glob(f"{CUTS}/cf_*.mp4")):
    k = os.path.basename(src)[:-4]; mp, jp = f"{OUT}/{k}.mp4", f"{OUT}/{k}.jpg"
    if os.path.exists(mp) and os.path.getmtime(mp) > os.path.getmtime(src): continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", mp], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(dur(src) - 3) * 0.45:.2f}", "-i", src, "-frames:v", "1", "-vf", "scale='if(gt(iw,ih),960,-2)':'if(gt(iw,ih),-2,960)'", "-q:v", "4", jp], check=True)
    n += 1
print("encoded", n, "total", len(glob.glob(f"{OUT}/cf_*.mp4")))
