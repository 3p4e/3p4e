import json, re, subprocess
import imageio_ffmpeg
from script import SEGMENTS
FF = imageio_ffmpeg.get_ffmpeg_exe()
INTRO, OUTRO, BREATH, INNER = 3.0, 8.0, 0.8, 0.35
PAUSE_AFTER = {"01": 1.5, "02": 6.5, "11": 1.5, "13": 2.0, "15": 1.5, "18": 2.0, "20": 1.0, "22": 1.0, "23": 1.0}
INNER_PAUSE = {("06", 1): 1.0}   # pause before "Ууу!"

def dur(fn):
    err = subprocess.run([FF, "-i", fn], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

def ts(t, srt=False):
    m, s = divmod(t, 60)
    return f"00:{int(m):02d}:{s:06.3f}".replace(".", ",") if srt else f"{int(m)}:{s:04.1f}"

pieces, timeline, srt, t = [("sil", INTRO)], [], [], INTRO
for k, (seg, parts) in enumerate(SEGMENTS):
    start = t
    for i, (role, text) in enumerate(parts):
        fn = f"parts/seg{seg}_{i}_{role}.mp3"
        d = dur(fn)
        pieces.append(("file", fn))
        srt.append((t, t + d, text))
        t += d
        if i < len(parts) - 1:
            g = INNER_PAUSE.get((seg, i), INNER)
            pieces.append(("sil", g)); t += g
    timeline.append((seg, start, t, " / ".join(f"[{'Л' if r == 'professor' else 'Н'}] {x}" for r, x in parts)))
    g = PAUSE_AFTER.get(seg, BREATH) if k < len(SEGMENTS) - 1 else OUTRO
    pieces.append(("sil", g)); t += g

inputs, labels = [], []
for n, (kind, v) in enumerate(pieces):
    if kind == "sil":
        inputs += ["-f", "lavfi", "-t", f"{v:.3f}", "-i", "anullsrc=r=24000:cl=mono"]
    else:
        inputs += ["-i", v]
    labels.append(f"[{n}:a]")
flt = "".join(f"{l}aresample=24000,aformat=channel_layouts=mono[a{n}];" for n, l in enumerate(labels))
flt += "".join(f"[a{n}]" for n in range(len(labels))) + f"concat=n={len(labels)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[out]"
subprocess.run([FF, "-loglevel", "error", "-y", *inputs, "-filter_complex", flt, "-map", "[out]",
                "-ar", "44100", "-b:a", "192k", "Ep01_narration_full.mp3"], check=True)

with open("Ep01_timeline.md", "w") as f:
    f.write("# Ep01 narration timeline (Н = narrator Leda, Л = Лиденброк Gacrux)\n\n| Seg | Start | End | Text |\n|---|---|---|---|\n")
    for seg, a, b, x in timeline:
        f.write(f"| {seg} | {ts(a)} | {ts(b)} | {x} |\n")
    f.write(f"\n**Total: {ts(t)}**\n")
with open("Ep01_narration.srt", "w") as f:
    for n, (a, b, x) in enumerate(srt, 1):
        f.write(f"{n}\n{ts(a, True)} --> {ts(b, True)}\n{x}\n\n")
json.dump({"segments": [{"seg": s, "start": a, "end": b} for s, a, b, _ in timeline], "total": t, "intro": INTRO, "outro": OUTRO}, open("timeline.json", "w"), indent=1)
print(f"total {ts(t)}  file {dur('Ep01_narration_full.mp3'):.1f}s")
