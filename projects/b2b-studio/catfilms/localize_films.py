# Language versions of the bigdogma.tech example films for non-Macedonian pitch pages (owner 2026-11-28: no Macedonian films on
# Albanian/Serbian/English/... pages). Phase 1: picture of the published film up to its end card, music only (no Macedonian voice),
# a new end card in the page language. Optional English narration (Kokoro, open source) from vo_en/<id>_l<n>.wav (phase 2).
#   python3 localize_films.py <lang> <film_id> [...]     -> /dev/shm/loc/<lang>/<film_id>.mp4 (+ .jpg)
import os, sys, json, subprocess, urllib.request, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = "/dev/shm/loc"; SRC = "/dev/shm/loc/src"; os.makedirs(SRC, exist_ok=True)
FH, FR = f"{S}/brand/fonts/Oswald-600.ttf", f"{S}/brand/fonts/Oswald-400.ttf"; FZ = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
STUDIO = {"en": "BIG DOGMA · AI video studio · Skopje", "sr": "BIG DOGMA · AI video studio · Skoplje", "sq": "BIG DOGMA · Studio video AI · Shkup",
          "sl": "BIG DOGMA · AI video studio · Skopje", "zh": "BIG DOGMA · AI 视频工作室 · 斯科普里"}
DEMO = {"en": "Demo film. Every shot is AI-generated.", "sr": "Demo film. Svi kadrovi su generisani pomoću AI.", "sq": "Film demonstrues. Të gjitha pamjet janë krijuar me AI.",
        "sl": "Predstavitveni film. Vsi kadri so ustvarjeni z AI.", "zh": "演示影片，所有镜头均由 AI 生成。"}
PLAN = {f["id"]: f for p in sorted(__import__("glob").glob(f"{HERE}/plan/*.json")) for f in json.load(open(p, encoding="utf-8"))["films"]}
XL = json.load(open(f"{P}/launch/site_work/i18n_extra.json", encoding="utf-8"))
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "24"]
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def esc(t): return t.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%").replace(",", "\\,")
def size(f): return [int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip().split(",")[:2]]

def card_start(src):
    """first time in the last 7 s where the frame is the flat dark end card (mean < 16, little texture)"""
    d = dur(src); W, H = 64, 36; t0 = max(0, d - 7)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.2f}", "-i", src, "-vf", f"fps=10,scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)
    me, se = fr[-1].mean(), fr[-1].std(); k = len(fr) - 1
    while k > 0 and fr[k - 1].mean() <= me + 8 and fr[k - 1].std() <= se + 10: k -= 1   # walk back over the stable end card
    if k >= len(fr) - 5: return d - 3.0
    return max(1.0, t0 + k / 10 - 0.55)   # cut just before the old card's crossfade starts

def line(fid, lang):
    f = PLAN.get(fid, {})
    if lang == "en": return f.get("line_en") or f.get("title_en", "")
    return XL.get(lang, {}).get(f"{fid}.l") or f.get("line_en", "")

def card(fid, lang, W, H, d, out):
    v = H > W; cy = H // 2 - (60 if v else 40); t = line(fid, lang); fh = FZ if lang == "zh" else FH; fr = FZ if lang == "zh" else FR
    fs = 66 if v else 64; L = []; maxw = W - 80; cw = 1.0 if lang == "zh" else 0.55
    if len(t) * cw * fs > maxw:
        fs = max(40, int(maxw / (cw * len(t))))
        if len(t) * cw * fs > maxw:
            sp = [i for i, ch in enumerate(t) if ch == " "]; k = min(sp, key=lambda i: abs(i - len(t) / 2)) if sp else len(t) // 2
            L.append((fh, t[:k].strip(), 48, "white", cy - 56, .15)); t = t[k:].strip(); fs = 48
    L += [(fh, t, fs, "white", cy, .15), (fr, STUDIO[lang], 34 if v else 30, "0xf2c14e", cy + (100 if v else 80), .5),
          (fr, DEMO[lang], 24 if v else 19, "0x9a9a9a", H - (120 if v else 40), .3)]
    vf = ",".join(f"drawtext=fontfile={ft}:text='{esc(x)}':fontsize={s}:fontcolor={c}:x=(w-tw)/2:y={y}:alpha='min(1,max(0,(t-{a})/0.3))'" for ft, x, s, c, y, a in L)
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b0d:s={W}x{H}:r=24:d={d:.2f}", "-vf",
         f"drawbox=x=(iw-160)/2:y={cy - 34}:w=160:h=4:color=0xf2c14e:t=fill,{vf}", "-an"] + ENC + [out])

def build(lang, fid, variant=""):
    name = fid + variant; src = f"{SRC}/{name}.mp4"; os.makedirs(f"{OUT}/{lang}", exist_ok=True); out = f"{OUT}/{lang}/{name}.mp4"
    if os.path.exists(out): return "exists"
    if not os.path.exists(src):   # atomic: parallel workers must never read a half-downloaded file
        tmp = f"{src}.{os.getpid()}.part"; urllib.request.urlretrieve(f"https://bigdogma.tech/films/{name}.mp4", tmp); os.replace(tmp, src)
    W, H = size(src); cs = card_start(src); cd = 3.2; T = f"/dev/shm/loc/tmp_{lang}_{name}"; os.makedirs(T, exist_ok=True)
    card(fid, lang, W, H, cd, f"{T}/card.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", f"{T}/card.mp4", "-filter_complex",
         f"[0:v]trim=0:{cs:.3f},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1,settb=AVTB[a];[1:v]fps=24,format=yuv420p,setsar=1,settb=AVTB[b];[a][b]xfade=transition=fade:duration=0.4:offset={cs - 0.4:.3f}[v]",
         "-map", "[v]", "-an"] + ENC + [f"{T}/v.mp4"])
    total = dur(f"{T}/v.mp4")
    mus = f"{S}/catfilms/music/{fid}.wav"
    if not os.path.exists(mus): mus = f"{S}/music/ace_final/" + {"commercial": "8_showreel", "story": "1_family", "explainer": "2_corporate", "social": "7_upbeat", "transform": "3_construction"}.get(PLAN.get(fid, {}).get("type"), "8_showreel") + ".mp3"
    vo = sorted(__import__("glob").glob(f"{HERE}/vo_{'en' if lang in ('en', 'zh') else lang}/{fid}_l*.wav")) if os.environ.get("NARRATE") else []
    a = ["ffmpeg", "-v", "error", "-y", "-i", mus] + sum([["-i", l] for l in vo], []); fc = []
    if vo:   # same layout as cut.py: lines spread over the film, music ducked under them
        main = cs; starts, t = [], 0.6
        for i, l in enumerate(vo): t = max(t, 0.6 + i * main / len(vo)); starts.append(t); t += dur(l) + 0.35
        fc += [f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(s * 1000)}|{int(s * 1000)},volume=1.6[l{i}]" for i, s in enumerate(starts)]
        fc.append("".join(f"[l{i}]" for i in range(len(vo))) + f"amix=inputs={len(vo)}:normalize=0,apad=whole_dur={total:.2f}[vo]")
        fc.append("[vo]asplit[vo1][vo2]")
        fc.append(f"[0:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,volume=0.55,afade=t=in:d=0.3,afade=t=out:st={total - 1.6:.2f}:d=1.6[m]")
        fc.append("[m][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
        fc.append(f"[md][vo2]amix=inputs=2:normalize=0,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    else:
        fc.append(f"[0:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={total - 1.8:.2f}:d=1.8,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    run(a + ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", f"{T}/a.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{T}/v.mp4", "-i", f"{T}/a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out])
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(3, cs / 3):.2f}", "-i", out, "-frames:v", "1", "-q:v", "4", out[:-4] + ".jpg"])
    subprocess.run(["rm", "-rf", T]); return f"ok {total:.1f}s card@{cs:.1f}"

if __name__ == "__main__":
    lang = sys.argv[1]
    for x in sys.argv[2:]:
        fid, var = (x[:-5], "_9x16") if x.endswith("_9x16") else (x, "")
        try: print(lang, x, build(lang, fid, var), flush=True)
        except Exception as e: print(lang, x, "FAIL", str(e)[:200], flush=True)
