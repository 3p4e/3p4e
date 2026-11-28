# BIG DOGMA outros from the AI logo render (owner 2026-11-27: the drawn canvas ignition is out; "use the much better renders").
# The film is smoke_reveal (the BD mark in smoke igniting to glowing gold on black, LTX render 1280x704, 5.04 s): it is scaled,
# feathered into the background (png/outro_mask_*), and the text layers from static_html.py fade in after it.
#   seg/outro_16x9.mp4      1920x1080, film from 2.0 s: film + BIG DOGMA + studio line + tagline     (how-to, howto169.py)
#   seg/outro_9x16.mp4      1080x1920, film from 2.2 s: film + BIG DOGMA + studio line; reels.py / reels_outro.py add
#                           png/outro_disc_9x16.png (tagline + disclosure)
#   seg/outro_end_9x16.mp4  1080x1920, film from 0.7 s, film only (showreel2.py 9:16 logo close, the end card follows)
# usage: python3 outro_ai.py [film]   (default: the original render cached at /dev/shm/vall/ai/logo_smoke_reveal.mp4,
#                                      else the site's copy media/intro/smoke_reveal.mp4)
import os, sys, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; P = f"{W}/png"; SEG = f"{W}/seg"; FPS = 24
FILM = sys.argv[1] if len(sys.argv) > 1 else next(f for f in ("/dev/shm/vall/ai/logo_smoke_reveal.mp4", f"{S}/launch/site/media/intro/smoke_reveal.mp4") if os.path.exists(f))
ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart"]

def build(out, asp, ss, fw, fh, x, y, layers):
    d = 5.04 - ss
    ins = ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{P}/outro_bg_{asp}.png",
           "-ss", f"{ss:.3f}", "-i", FILM, "-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{P}/outro_mask_{asp}.png"]
    fc = (f"[1:v]fps={FPS},scale={fw}:{fh}:flags=lanczos,unsharp=5:5:0.35,format=rgba[f];[2:v]format=gray,scale={fw}:{fh}[m];"
          f"[f][m]alphamerge[fm];[0:v][fm]overlay={x}:{y}:format=auto:shortest=1[a]")
    last = "a"
    for i, (png, st) in enumerate(layers):
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        fc += f";[{3 + i}:v]format=rgba,fade=t=in:st={st}:d=0.6:alpha=1[t{i}];[{last}][t{i}]overlay=format=auto[o{i}]"; last = f"o{i}"
    fc += f";[{last}]fade=t=in:st=0:d=0.25,format=yuv420p,setsar=1[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}"] + ENC + [out], check=True)
    print("OK", out, f"{d:.2f} s")

build(f"{SEG}/outro_16x9.mp4", "16x9", 2.0, 1400, 770, 260, 0, [(f"{P}/outro_word_16x9.png", 0.5)])
build(f"{SEG}/outro_9x16.mp4", "9x16", 2.2, 1240, 682, -80, 380, [(f"{P}/outro_word_9x16.png", 0.5)])
build(f"{SEG}/outro_end_9x16.mp4", "9x16", 0.7, 1240, 682, -80, 520, [])
