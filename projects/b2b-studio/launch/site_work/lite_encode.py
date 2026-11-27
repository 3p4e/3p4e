# Light copies of the BD videos for the page background, the splash and the screensaver.
# 2026-11-26 (owner: "too high quality, they load slowly and play like a slideshow"): 960x528 capped copies.
# 2026-11-27 (owner: "poor resolution and takes time to load"): the slowness was the server's ~1 s wait per request, not the size, and
# hero_bg.js now downloads each next film completely before showing it. So the background films are 720p again at a good quality
# (media/lite/intro, 1280x704, ~1 MB per 5 s film) for desktops, plus 480p copies (media/lite480/intro, 854x470) for phones and slow
# connections. H.264 main profile, a keyframe every second, no audio, +faststart. The BD gallery keeps media/intro and media/bd.
# The logo-effect loops stay at 960x528 (media/lite/bd).
import os, glob, subprocess, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/launch/site"
JOBS = [("intro", "lite", "1280:-2", "22", "2000k", "3M"), ("intro", "lite480", "854:-2", "24", "900k", "1400k"), ("bd", "lite", "960:-2", "27", "700k", "2M")]
VER = "v2"   # bump to re-encode everything after a settings change
n = 0
for kind, dst, scale, crf, rate, buf in JOBS:
    od = f"{OUT}/media/{dst}/{kind}"; os.makedirs(od, exist_ok=True); stamp = f"{od}/.settings"
    same = os.path.exists(stamp) and open(stamp).read() == f"{VER} {scale} {crf} {rate}"
    for f in sorted(glob.glob(f"{OUT}/media/{kind}/*.mp4")):
        o = f"{od}/{os.path.basename(f)}"
        if same and os.path.exists(o) and os.path.getmtime(o) >= os.path.getmtime(f): continue
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-an", "-vf", f"scale={scale}:flags=lanczos,fps=24", "-c:v", "libx264", "-profile:v", "main",
                        "-preset", "slow", "-crf", crf, "-maxrate", rate, "-bufsize", buf, "-g", "24", "-keyint_min", "24", "-sc_threshold", "0",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", o], check=True); n += 1
    open(stamp, "w").write(f"{VER} {scale} {crf} {rate}")
tot = lambda k: sum(os.path.getsize(p) for p in glob.glob(f"{OUT}/media/{k}/*.mp4")) // 1024
print("lite encoded", n, "| intro", tot("intro"), "KB -> 720p", tot("lite/intro"), "KB, 480p", tot("lite480/intro"), "KB | bd", tot("bd"), "KB ->", tot("lite/bd"), "KB")
