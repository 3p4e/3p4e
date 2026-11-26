# Media for the "BD logo" gallery: posters for the scene films (media/intro/<id>.jpg, logo formed near the end) and the logo-only
# effects at full size (media/bd/<id>.mp4 + .jpg, from the hdr_* LTX clips). Re-runs skip what exists.
import os, glob, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from bd_titles import FX
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; SITE = f"{S}/launch/site/media"; CL = f"{S}/logo_ai/clips"
os.makedirs(f"{SITE}/bd", exist_ok=True)
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y"] + a, check=True)
for f in sorted(glob.glob(f"{SITE}/intro/*.mp4")):
    j = f[:-4] + ".jpg"
    if not os.path.exists(j) or os.path.getmtime(j) < os.path.getmtime(f): run(["-ss", "4.3", "-i", f, "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "4", j])
n = 0
for k in FX:
    src = f"{CL}/hdr_{k}.mp4"; mp = f"{SITE}/bd/{k}.mp4"
    if not os.path.exists(src) or os.path.exists(mp): continue
    run(["-i", src, "-an", "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp])
    run(["-ss", "2", "-i", mp, "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "4", mp[:-4] + ".jpg"]); n += 1
print("bd effects encoded", n, "total", len(glob.glob(f"{SITE}/bd/*.mp4")), "| intro posters", len(glob.glob(f"{SITE}/intro/*.jpg")))
