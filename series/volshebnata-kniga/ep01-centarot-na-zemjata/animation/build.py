"""Build the animated episode: clips laid on the narration timeline, crossfaded, title, music, narration.
usage: build.py <timeline.json> <narration.mp3> <out.mp4>"""
import json, os, re, subprocess, sys
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H, XF = 24, 1920, 1080, 0.5
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CLIPS = {"01": ["01"], "02": ["02"], "04": ["04", "04x"], "05": ["05", "05b"], "06": ["06"], "07": ["07"],
         "08": ["08", "08b"], "09": ["09", "09x"], "10": ["10"], "11": ["11"], "12": ["12", "12x"], "13": ["13", "13b"],
         "14": ["14", "14x"], "15": ["15"], "16": ["16", "16b"], "17": ["17"], "18": ["18", "18x"], "19": ["19"],
         "20": ["20", "20b"], "21": ["21", "21b"], "22": ["22"], "23": ["23"], "24": ["24"]}
TITLE = [("Патување во центарот", 96, 0.30), ("на Земјата", 96, 0.43)]

def dur(fn):
    e = subprocess.run([FF, "-i", fn], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

tl_path, narr, out = sys.argv[1:4]
tl = json.load(open(tl_path))
segs = tl["segments"]
# window per segment = its start .. next segment's start (first starts at 0, last runs to the end)
shots = []  # (clip, window seconds)
for k, s in enumerate(segs):
    a = 0.0 if k == 0 else s["start"]
    b = segs[k + 1]["start"] if k + 1 < len(segs) else tl["total"]
    if s["seg"] == "02":            # the title shot (03) takes the pause after segment 02
        b2 = s["end"] + 0.6
        shots.append(("02", b2 - a)); shots.append(("03", b - b2)); continue
    ids = [c for c in CLIPS[s["seg"]] if os.path.exists(f"clip_{c}.mp4")]
    lens = [dur(f"clip_{c}.mp4") for c in ids]
    for c, L in zip(ids, lens):
        shots.append((c, (b - a) * L / sum(lens)))
os.makedirs("norm", exist_ok=True)

def title_png():
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for text, size, y in TITLE:
        f = ImageFont.truetype(FONT, size); tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, H * y), text, font=f, fill="white", stroke_width=8, stroke_fill=(60, 40, 110))
    im.save("norm/title.png"); return "norm/title.png"

def norm(i, c, win):
    """Scale to 1080p and fit the clip to its window: gentle slow-down up to 1.5x, then boomerang if still short."""
    src = f"clip_{c}.mp4"; L = dur(src)
    need = win + (XF if i < len(shots) - 1 else 0)
    f = min(max(need / L, 1.0), 1.5)
    chain = f"setpts={f:.4f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1"
    if L * f < need:   # boomerang: forward then reversed, enough to cover the window
        chain = f"split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,{chain}"
    o = f"norm/{i:02d}_{c}.mp4"
    cmd = [FF, "-loglevel", "error", "-y", "-i", src]
    if c == "03":
        cmd += ["-loop", "1", "-i", title_png(), "-filter_complex",
                f"[0:v]{chain}[v];[1:v]format=rgba,fade=in:st=0.3:d=0.8:alpha=1[t];[v][t]overlay=0:0,format=yuv420p",
                ]
    else:
        cmd += ["-vf", chain + ",format=yuv420p"]
    cmd += ["-t", f"{need:.3f}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), o]
    subprocess.run(cmd, check=True)
    return o

files = [norm(i, c, w) for i, (c, w) in enumerate(shots)]
inputs, chain, prev, off = [], "", "[0:v]", 0.0
for f in files:
    inputs += ["-i", f]
for k in range(1, len(files)):
    off += shots[k - 1][1]
    chain += f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v{k}];"
    prev = f"[v{k}]"
subprocess.run([FF, "-loglevel", "error", "-y", *inputs, "-filter_complex", chain.rstrip(";"), "-map", prev,
                "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "video_only.mp4"], check=True)
total = tl["total"]
subprocess.run([sys.executable, "music.py", f"{total:.3f}", str(tl["intro"]), f"{total - tl['outro']:.3f}", "music.wav"], check=True)
subprocess.run([FF, "-loglevel", "error", "-y", "-i", "video_only.mp4", "-i", narr, "-i", "music.wav", "-filter_complex",
                "[1:a]volume=1.0[n];[2:a]volume=0.5[m];[n][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("shots:", len(shots), " video:", round(dur("video_only.mp4"), 1), " final:", round(dur(out), 1))
for c, w in shots:
    print(f"  {c:4s} {w:5.1f}s")
