# usage: frames.py clip.mp4 out.jpg  -> 4-frame strip to judge motion
import subprocess, sys, re, imageio_ffmpeg
from PIL import Image
FF = imageio_ffmpeg.get_ffmpeg_exe()
src, out = sys.argv[1], sys.argv[2]
e = subprocess.run([FF, "-i", src], capture_output=True, text=True).stderr
h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e).groups()
d = int(h) * 3600 + int(m) * 60 + float(s)
ims = []
for k in range(4):
    t = d * (k + 0.5) / 4
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", f"/tmp/f{k}.png"], check=True)
    ims.append(Image.open(f"/tmp/f{k}.png").convert("RGB").resize((480, 270)))
strip = Image.new("RGB", (960, 540))
for k, im in enumerate(ims):
    strip.paste(im, ((k % 2) * 480, (k // 2) * 270))
strip.save(out, quality=80)
print(f"{src}: {d:.1f}s")
