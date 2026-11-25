# Verifies burned-in subtitle placement: at each subtitle midpoint, the reel frame is compared with the clean 9:16 master
# below the picture band (y >= 1264; the band, the watermark and the top-band AI disclosure are ignored). Subtitle pixels =
# changed by more than 60 AND white (L > 200, the text fill); the box is grown by 4 px for the 3.5 px outline. The white test
# keeps the check valid where reels.py replaces the master's picture (reel_01 0-4.7 s, reel_04 4.3-10.2 s), whose blurred
# cover then differs from the master's. Target zone: y 1264..1436 (under the picture band, above TikTok's bottom ad zone),
# x 160..920 (clear of the right-hand action rail).
import subprocess, re, io, sys
import numpy as np
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
R = [("reel_01_construction", "timelapse_construction"), ("reel_02_real_estate", "sector_real_estate"), ("reel_03_food", "sector_food"),
     ("reel_04_automotive", "sector_automotive"), ("reel_05_interior_design", "timelapse_interior_design")]
Y0, Y1, X0, X1 = 1264, 1436, 160, 920
def frame(f, t):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", f, "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(b)).convert("L")
ok = True
for reel, film in R:
    txt = open(f"{S}/subs/srt/{film}.mk.srt", encoding="utf-8-sig").read()
    for m in re.finditer(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", txt):
        g = [int(x) for x in m.groups()]; a = g[0]*3600+g[1]*60+g[2]+g[3]/1000; b = g[4]*3600+g[5]*60+g[6]+g[7]/1000; t = (a + b) / 2
        r = np.asarray(frame(f"{S}/launch/video/{reel}.mp4", t), int); c = np.asarray(frame(f"{S}/final_music_9x16/{film}_9x16.mp4", t), int)
        m = (np.abs(r - c) > 60) & (r > 200); m[:Y0] = False
        ys, xs = np.where(m)
        bb = (int(xs.min()) - 4, int(ys.min()) - 4, int(xs.max()) + 5, int(ys.max()) + 5) if len(xs) else None
        good = bb is not None and bb[1] >= Y0 and bb[3] <= Y1 and bb[0] >= X0 and bb[2] <= X1
        ok &= good; print(f"{reel:26s} t={t:6.2f} bbox={bb} {'OK' if good else 'CHECK'}")
print("ALL_OK" if ok else "SOME_CHECK")
