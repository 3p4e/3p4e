# Lays the studio sign-off "BREAK THE DOGMA." (png/outro_tag_9x16.png from static_html.py) over the outro of reels that were
# already built (owner 2026-11-27): their 9:16 film masters are archived off this machine, so a full reels.py rebuild is not
# possible here. The tagline fades in 0.5 s into the 2.79 s outro, between the lockup subline and the disclosure, and fades
# out with the outro's own 0.3 s fade. Audio is copied untouched. A fresh reels.py run gets the same line from outro_disc_9x16.
# usage: python3 reels_tagline.py [out_dir]   (default /dev/shm/vall/reels_tag; the originals in launch/video are not touched)
import os, sys, glob, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; TAG = f"{W}/png/outro_tag_9x16.png"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/vall/reels_tag"; os.makedirs(OUT, exist_ok=True)
FPS = 24; OUTRO_F = 67                                    # same as reels.py
def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout.strip())
for src in sorted(glob.glob(f"{S}/launch/video/reel_0*.mp4")):
    d = dur(src); t0 = d - OUTRO_F / FPS; out = f"{OUT}/{os.path.basename(src)}"
    fc = (f"[1:v]format=rgba,fade=t=in:st={t0 + 0.5:.3f}:d=0.4:alpha=1,fade=t=out:st={d - 0.3:.3f}:d=0.3:alpha=1[t];"
          f"[0:v][t]overlay=0:0:format=auto:enable='gte(t,{t0 + 0.45:.3f})',format=yuv420p[v]")
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", TAG,
                    "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    print("OK", out, f"{dur(out):.2f} s (was {d:.2f})", flush=True)
