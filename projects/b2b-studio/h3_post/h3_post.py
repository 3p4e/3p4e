# ON THE H3 BOX ONLY. For every finished H3 film in /workspace/h3_commercials: pitch version (BIG DOGMA intro + КОНЦЕПТ
# watermark + email outro) 16:9 + 9:16, feed versions 1:1 + 4:5, subtitles mk/sr/sq/en timed by cross-correlating the
# film soundtrack with the voice-over files on the box. Idempotent: skips outputs that exist. Nothing leaves the box.
import os, json, subprocess, numpy as np
W = "/workspace"; P = f"{W}/h3post"; SRC = f"{W}/h3_commercials"; TR = f"{W}/h3cut/vo/trim"
OUT = {k: f"{W}/{k}" for k in ("h3_pitch", "h3_pitch_9x16", "h3_feed_1x1", "h3_feed_4x5", "h3_subs")}
for d in list(OUT.values()) + [f"{P}/tmp"]: os.makedirs(d, exist_ok=True)
FONT = f"{P}/RussoOne-400.ttf"; MAP = json.load(open(f"{P}/sub_map.json"))
WM = {"mk": "КОНЦЕПТ · НЕ Е ЗА ОБЈАВА", "sr": "KONCEPT · NIJE ZA OBJAVU", "sq": "KONCEPT · JO PËR PUBLIKIM"}
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
def run(a): subprocess.run(a, check=True)
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")
def pcm(f, sr=8000):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32) / 32768
def ts(x): return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x - int(x)) * 1000)) % 1000:03d}"
def wrap(t, n=42):
    if len(t) <= n or " " not in t: return t
    sp = [i for i, c in enumerate(t) if c == " "]; i = min(sp, key=lambda x: abs(x - len(t) // 2)); return t[:i] + "\n" + t[i + 1:]
def subs(name, src):
    if name not in MAP or os.path.exists(f"{OUT['h3_subs']}/{name}_H3.en.srt"): return
    a = pcm(src); n = len(a); found = []
    for l in MAP[name]["lines"]:
        wf = f"{TR}/{l['wav']}"
        if not os.path.exists(wf): continue
        v = pcm(wf); m = len(v)
        if m >= n: continue
        N = 1 << int(np.ceil(np.log2(n + m)))
        cc = np.fft.irfft(np.fft.rfft(a, N) * np.conj(np.fft.rfft(v, N)), N)[: n - m + 1]
        e = np.sqrt(np.convolve(a * a, np.ones(m, np.float32), "valid")) * np.linalg.norm(v) + 1e-9
        sc = cc / e; k = int(np.argmax(sc))
        if sc[k] > 0.25: found.append((k / 8000, (k + m) / 8000, l["tx"]))
    found.sort(key=lambda x: x[0])
    for lang in ("mk", "sr", "sq", "en"):
        rows = []
        for i, (t0, t1, tx) in enumerate(found):
            en = max(t1 + 0.35, t0 + 1.0)
            if i + 1 < len(found): en = min(en, found[i + 1][0] - 0.05)
            rows.append(f"{i+1}\n{ts(t0)} --> {ts(en)}\n{wrap(tx[lang])}\n")
        open(f"{OUT['h3_subs']}/{name}_H3.{lang}.srt", "w").write("\n".join(rows))
    print("SUBS", name, len(found), "/", len(MAP[name]["lines"]), flush=True)
def blurfill(src, out, W_, H_):
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex",
         f"[0:v]split[a][b];[a]scale={W_}:{H_}:force_original_aspect_ratio=increase,crop={W_}:{H_},gblur=sigma=36,eq=brightness=-0.14:saturation=0.9[bg];[b]scale={W_}:-2[fg];[bg][fg]overlay=0:(H-h)/2",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out])
for f in sorted(os.listdir(SRC)):
    if not f.endswith("_H3.mp4"): continue
    name = f[:-7]; src = f"{SRC}/{f}"; lang = MAP.get(name, {}).get("lang", "mk")
    try:
        subs(name, src)
        pv = f"{OUT['h3_pitch']}/{name}_H3_pitch.mp4"
        if not os.path.exists(pv):
            body = f"{P}/tmp/{name}_body.mp4"
            vf = f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,drawtext=fontfile={FONT}:text='{esc(WM[lang])}':fontsize=20:fontcolor=white@0.55:x=w-tw-24:y=22:box=1:boxcolor=black@0.25:boxborderw=8"
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf] + ENC + [body])
            run(["ffmpeg", "-v", "error", "-y", "-i", f"{P}/intro.mp4", "-i", body, "-i", f"{P}/outro_{lang}.mp4", "-filter_complex",
                 "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]"] + ENC + ["-movflags", "+faststart", pv])
            os.remove(body)
        pv9 = f"{OUT['h3_pitch_9x16']}/{name}_H3_pitch_9x16.mp4"
        if not os.path.exists(pv9): blurfill(pv, pv9, 1080, 1920)
        for k, (w, h) in (("h3_feed_1x1", (1080, 1080)), ("h3_feed_4x5", (1080, 1350))):
            o = f"{OUT[k]}/{name}_H3_{k[-3:]}.mp4"
            if not os.path.exists(o): blurfill(src, o, w, h)
        print("OK", name, lang, flush=True)
    except Exception as e:
        print("ERR", name, str(e)[:200], flush=True)
print("H3POST_DONE", len([x for x in os.listdir(OUT["h3_pitch"]) if x.endswith(".mp4")]), "pitch films")
