# Encodes the approved AI logo films for the fullscreen hero playlist: launch/site/media/intro/<id>.mp4, 1280x704, muted, ~5 s.
# Rejected after frame QC (stained_glass replaced by the real cathedral window): chrome_liquid (logo melts), drone_show (formation falls apart), steel_turntable (shape garbles on orbit).
# sand_dune is played in reverse, so the logo emerges from the sand instead of blowing away.
import sys, os, glob, subprocess
SRC = sys.argv[1]; OUT = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/launch/site/media/intro"
DROP = {"chrome_liquid", "drone_show", "steel_turntable", "stained_glass"}; REV = {"sand_dune"}   # stained_glass: replaced by cathedral_window (owner, 2026-11-26)
os.makedirs(OUT, exist_ok=True)
for f in sorted(glob.glob(f"{SRC}/logo_*.mp4")):
    i = os.path.basename(f)[5:-4]
    if i in DROP: continue
    vf = ("reverse," if i in REV else "") + "format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "25", "-preset", "slow", "-movflags", "+faststart", f"{OUT}/{i}.mp4"], check=True)
    print(i, os.path.getsize(f"{OUT}/{i}.mp4") // 1024, "KB")
