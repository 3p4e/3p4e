# Still BIG DOGMA outros (owner 2026-11-27: the drawn logo ignition with sparks, rays and rings is gone everywhere).
# Layers from static_html.py (png/outro_*): a dark background with the soft gold glow, the lockup fading in, the tagline after it.
#   seg/outro_16x9.mp4      1920x1080: lockup + "BREAK THE DOGMA."           (how-to outro, howto169.py)
#   seg/outro_9x16.mp4      1080x1920: lockup only, tagline + disclosure come from png/outro_disc_9x16.png (reels.py, reels_outro.py)
#   seg/outro_end_9x16.mp4  1080x1920: the 9:16 end card's own lockup layer (end_9x16_A) fading in (showreel2.py 9:16 logo close)
# usage: python3 outro_still.py
import subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; P = f"{W}/png"; SEG = f"{W}/seg"; FPS = 24; D = 4.6
ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart"]
def still(png): return ["-loop", "1", "-framerate", str(FPS), "-t", str(D), "-i", png]
def run(inputs, fc, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-t", str(D)] + ENC + [out], check=True); print("OK", out)
fade = lambda i, st, d: f"[{i}:v]format=rgba,fade=t=in:st={st}:d={d}:alpha=1[l{i}]"
run(still(f"{P}/outro_bg_16x9.png") + still(f"{P}/outro_logo_16x9.png") + still(f"{P}/outro_tag_16x9.png"),
    f"{fade(1, 0.15, 0.75)};{fade(2, 0.75, 0.6)};[0:v][l1]overlay=format=auto[a];[a][l2]overlay=format=auto,format=yuv420p,setsar=1[v]", f"{SEG}/outro_16x9.mp4")
run(still(f"{P}/outro_bg_9x16.png") + still(f"{P}/outro_logo_9x16.png"),
    f"{fade(1, 0.15, 0.75)};[0:v][l1]overlay=format=auto,format=yuv420p,setsar=1[v]", f"{SEG}/outro_9x16.mp4")
run(still(f"{P}/end_9x16_A.png"), "[0:v]fade=t=in:st=0:d=0.6,format=yuv420p,setsar=1[v]", f"{SEG}/outro_end_9x16.mp4")
