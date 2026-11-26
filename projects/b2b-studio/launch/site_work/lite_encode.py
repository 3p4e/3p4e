# Light copies of the BD videos for the hero background, the splash and the screensaver (owner, 2026-11-26: "too high quality, they load
# slowly and play like a slideshow"): 960x528, H.264 main profile, a keyframe every second (playback starts at once), capped bitrate,
# no audio. The BD gallery keeps the full-quality files (media/intro, media/bd).  ->  media/lite/intro/<id>.mp4, media/lite/bd/<id>.mp4
import os, glob, subprocess, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/launch/site"
n = 0
for kind, rate in (("intro", "1100k"), ("bd", "700k")):
    os.makedirs(f"{OUT}/media/lite/{kind}", exist_ok=True)
    for f in sorted(glob.glob(f"{OUT}/media/{kind}/*.mp4")):
        o = f"{OUT}/media/lite/{kind}/{os.path.basename(f)}"
        if os.path.exists(o) and os.path.getmtime(o) >= os.path.getmtime(f): continue
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-an", "-vf", "scale=960:-2:flags=lanczos,fps=24", "-c:v", "libx264", "-profile:v", "main",
                        "-preset", "slow", "-crf", "27", "-maxrate", rate, "-bufsize", "2M", "-g", "24", "-keyint_min", "24", "-sc_threshold", "0",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", o], check=True); n += 1
tot = lambda k: sum(os.path.getsize(p) for p in glob.glob(f"{OUT}/media/{k}/*.mp4")) // 1024
print("lite encoded", n, "| intro", tot("intro"), "KB ->", tot("lite/intro"), "KB | bd", tot("bd"), "KB ->", tot("lite/bd"), "KB")
