# Header-logo effect loops: crops each hdr_* LTX clip around the logo (bbox from the first frame), aspect 1.5 to match the header slot,
# logo ~58% of the width like the canvas engine, scales to 330x220, h264 mp4 without audio, and writes logo_fx/hdr/list.js.
#   python3 fx_header.py <clipdir> [ids...]
import sys, os, glob, json, subprocess, numpy as np
from PIL import Image
SRC = sys.argv[1]; OUT = "/home/user/3p4e/projects/b2b-studio/launch/site_work/logo_fx/hdr"; os.makedirs(OUT, exist_ok=True)
W, H, FILL = 330, 220, .58
ids = sys.argv[2:] or sorted(os.path.basename(f)[4:-4] for f in glob.glob(f"{SRC}/hdr_*.mp4"))
for i in ids:
    src = f"{SRC}/hdr_{i}.mp4"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    f0 = np.frombuffer(raw, np.uint8).reshape(704, 1280, 3).max(axis=2)
    ys, xs = np.where(f0 > 60); x0, x1, y0, y1 = np.percentile(xs, 1), np.percentile(xs, 99), np.percentile(ys, 1), np.percentile(ys, 99)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; cw = max((x1 - x0) / FILL, (y1 - y0) / .62 * 1.5); ch = cw / 1.5
    cw, ch = min(cw, 1280, 704 * 1.5), min(ch, 704, 1280 / 1.5); cw = ch * 1.5
    cx = min(max(cx, cw / 2), 1280 - cw / 2); cy = min(max(cy, ch / 2), 704 - ch / 2)
    vf = f"crop={cw:.0f}:{ch:.0f}:{cx - cw / 2:.0f}:{cy - ch / 2:.0f},scale={W}:{H}:flags=lanczos,format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-profile:v", "high", "-crf", "24", "-preset", "slow",
                    "-movflags", "+faststart", f"{OUT}/{i}.mp4"], check=True)
    print(i, f"crop {cw:.0f}x{ch:.0f}", os.path.getsize(f"{OUT}/{i}.mp4") // 1024, "KB")
have = sorted(os.path.basename(f)[:-4] for f in glob.glob(f"{OUT}/*.mp4"))
open(f"{OUT}/list.js", "w").write("window.DOGMA_HDR=" + json.dumps(have) + ";\n"); print("list", len(have))
