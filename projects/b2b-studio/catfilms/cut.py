# Cut engine for the category films: shots (5 s LTX clips) -> film with crossfades (hard cuts for social), Macedonian VO laid out
# over the film, Lyria music ducked under the VO, a 3 s end card (slogan + BIG DOGMA), -14 LUFS. 16:9 1280x720, social 9:16 720x1280.
#   python3 cut.py <clipdir> <outdir> [film ids...]   (skips films whose clips are not all there yet)
import os, sys, json, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
CLIPS, OUT = sys.argv[1], sys.argv[2]; ONLY = set(sys.argv[3:]); os.makedirs(OUT, exist_ok=True); T = f"{OUT}/tmp"; os.makedirs(T, exist_ok=True)
VO, MUS = f"{S}/catfilms/vo", f"{S}/catfilms/music"
FH = f"{S}/brand/fonts/Oswald-600.ttf"; FR = f"{S}/brand/fonts/Oswald-400.ttf"
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "24"]
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def esc(t): return t.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%").replace(",", "\\,")
def card(f, W, H, d, out):
    v = H > W; cy = H // 2 - (60 if v else 40)
    L = [(FH, f["line_mk"], 66 if v else 64, "white", cy, .15), (FR, "BIG DOGMA · AI видео студио · Скопје", 34 if v else 30, "0xf2c14e", cy + (100 if v else 80), .5),
         (FR, "Демо филм. Сите кадри се генерирани со AI.", 24 if v else 19, "0x9a9a9a", H - (120 if v else 40), .3)]
    vf = ",".join(f"drawtext=fontfile={ft}:text='{esc(t)}':fontsize={s}:fontcolor={c}:x=(w-tw)/2:y={y}:alpha='min(1,max(0,(t-{a})/0.3))'" for ft, t, s, c, y, a in L)
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b0d:s={W}x{H}:r=24:d={d:.2f}", "-vf",
         f"drawbox=x=(iw-160)/2:y={cy - 34}:w=160:h=4:color=0xf2c14e:t=fill,{vf}", "-an"] + ENC + [out])
def cut(f):
    n = len(f["shots"]); clips = [f"{CLIPS}/{f['id']}_s{i}.mp4" for i in range(1, n + 1)]
    if not all(os.path.exists(c) for c in clips): return "wait"
    v = f["type"] == "social"; W, H = (720, 1280) if v else (1280, 720); X = 0.0 if v else 0.5; SH = 5.0
    lines = [f"{VO}/{f['id']}_l{i}.wav" for i in range(1, len(f["vo_mk"]) + 1)]
    if not all(os.path.exists(l) for l in lines) or not os.path.exists(f"{MUS}/{f['id']}.wav"): return "no audio yet"
    XE = X or 0.04   # hard cuts are a 1-frame fade (xfade needs a duration)
    main = n * SH - (n - 1) * XE
    # VO layout: evenly spread over the shots, never overlapping, first line after 0.6 s
    starts, t = [], 0.6
    for i, l in enumerate(lines):
        t = max(t, 0.6 + i * main / max(1, len(lines))); starts.append(t); t += dur(l) + 0.35
    cd = max(3.0, t - main + 0.8); total = main + cd - 0.5
    card(f, W, H, cd, f"{T}/{f['id']}_card.mp4")
    a = ["ffmpeg", "-v", "error", "-y"]
    for c in clips: a += ["-i", c]
    a += ["-i", f"{T}/{f['id']}_card.mp4"]
    fc = [f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=24,trim=0:{SH},setpts=PTS-STARTPTS[v{i}]" for i in range(n)]
    fc.append(f"[{n}:v]setsar=1,fps=24,setpts=PTS-STARTPTS[v{n}]")
    cur = "v0"
    for i in range(1, n + 1):
        o = f"x{i}"; d_ = XE if i < n else 0.5; off = i * (SH - XE) if i < n else main - 0.5
        fc.append(f"[{cur}][v{i}]xfade=transition=fade:duration={d_}:offset={off:.3f}[{o}]"); cur = o
    run(a + ["-filter_complex", ";".join(fc), "-map", f"[{cur}]", "-an", "-t", f"{total:.2f}"] + ENC + [f"{T}/{f['id']}_v.mp4"])
    # audio: VO lines + music ducked under them
    a = ["ffmpeg", "-v", "error", "-y", "-i", f"{MUS}/{f['id']}.wav"] + sum([["-i", l] for l in lines], [])
    fc = [f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(s * 1000)}|{int(s * 1000)},volume=1.6[l{i}]" for i, s in enumerate(starts)]
    fc.append("".join(f"[l{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0,apad=whole_dur={total:.2f}[vo]")
    fc.append("[vo]asplit[vo1][vo2]")
    fc.append(f"[0:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,volume=0.55,afade=t=in:d=0.3,afade=t=out:st={total - 1.6:.2f}:d=1.6[m]")
    fc.append("[m][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
    fc.append(f"[md][vo2]amix=inputs=2:normalize=0,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    run(a + ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", f"{T}/{f['id']}_a.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{T}/{f['id']}_v.mp4", "-i", f"{T}/{f['id']}_a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", f"{OUT}/{f['id']}.mp4"])
    for x in ("_card.mp4", "_v.mp4", "_a.wav"): os.remove(f"{T}/{f['id']}{x}")
    return f"OK {total:.1f}s"
films = [f for p in sorted(glob.glob(f"{HERE}/plan/*.json")) for f in json.load(open(p))["films"]]
for f in films:
    if ONLY and f["id"] not in ONLY: continue
    if os.path.exists(f"{OUT}/{f['id']}.mp4"): continue
    r = cut(f)
    if r.startswith("OK"): print(r, f["id"], flush=True)
print("CUT_DONE", len(glob.glob(f"{OUT}/cf_*.mp4")), "/", len(films))
