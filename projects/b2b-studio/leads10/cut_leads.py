# Drugi tir concept films (Slovenian VO via Gemini TTS, LTX clips, music from foton_v2/music): 16:9 and 9:16 from one edit.
#   python3 cut_dt.py <clipdir> <outdir>
import os, sys, subprocess, json
sys.path.insert(0, "/home/user/3p4e/projects/b2b-studio/foton_v2")
import requests
def oa_tts(line, path, voice, LANG):
    # Gemini billing returned 402 (2026-11-27), so the Slovenian VO uses OpenAI TTS
    v = {"Charon": "onyx", "Orus": "nova"}.get(voice, "onyx")
    if os.path.exists(path): return
    r = requests.post("https://api.openai.com/v1/audio/speech", headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                      json={"model": "gpt-4o-mini-tts", "voice": v, "input": line, "response_format": "wav",
                            "instructions": f"Speak {LANGX[LANG][2]}, warm and confident commercial narrator. Natural native pronunciation, calm pace."}, timeout=120)
    r.raise_for_status(); open(path + ".raw.wav", "wb").write(r.content)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path + ".raw.wav", "-ar", "48000", "-ac", "2", "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse", path], check=True); os.remove(path + ".raw.wav")
CL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(f"{OUT}/vo", exist_ok=True); T = f"{OUT}/tmp"; os.makedirs(T, exist_ok=True)
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; M = "/home/user/3p4e/projects/b2b-studio/foton_v2/music"
F = lambda w: f"{S}/brand/fonts/Oswald-{w}.ttf"
CFG = json.load(open(f"{S}/leads10/cfg.json", encoding="utf-8"))
MUSIC = {"re": "fv_alpine", "retail": "fv_colour", "fuel": "fv_night", "food": "fv_colour"}
LANGX = {"mk": ("Концепт на BIG DOGMA за презентација. Не е објавен без писмено одобрение.", "Видео изработено со вештачка интелигенција · AI-generated video", "Macedonian"),
         "sq": ("Koncept i BIG DOGMA vetëm për prezantim. Nuk publikohet pa miratim me shkrim.", "Video e krijuar me inteligjencë artificiale · AI-generated video", "Albanian"),
         "sr": ("Koncept BIG DOGMA samo za prezentaciju. Ne objavljuje se bez pisanog odobrenja.", "Video napravljen veštačkom inteligencijom · AI-generated video", "Serbian"),
         "en": ("Concept by BIG DOGMA for presentation only. Not published without written approval.", "AI-generated video", "English")}
ONLY = os.environ.get("ONLY", "").split(",") if os.environ.get("ONLY") else None
FILMS = {}
for c in CFG["companies"]:
    if ONLY and c["key"] not in ONLY: continue
    for n, (fx, sub) in enumerate((("a", c["titles"][0]), ("b", c["titles"][2]))):
        FILMS[f"l_{c['key']}_{fx}"] = dict(title=sub, company=c["name"], lang=c["lang"], music=MUSIC[c["sector"]], voice="Charon" if n == 0 else "Orus",
            clips=[f"{c['key']}_{3*n+k+1}" for k in range(3)], vo=[(k, c["vo"][3*n+k]) for k in range(3)])
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"]
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")
XF, SEG = 0.4, 4.4
for fid, f in FILMS.items():
    for i, (k, line) in enumerate(f["vo"]): oa_tts(line, f"{OUT}/vo/{fid}_{i}.wav", f["voice"], f["lang"])
    for ar, (W, H) in (("16x9", (1280, 720)),):
        parts = []
        for k, c in enumerate(f["clips"]):
            geo = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}" if ar == "16x9" else "scale=-2:1920,crop=1080:1920"
            p = f"{T}/{fid}_{ar}_{k}.mp4"; run(["ffmpeg", "-v", "error", "-y", "-ss", "0.3", "-t", str(SEG), "-i", f"{CL}/l_{c}.mp4", "-vf", f"{geo},fps=24", "-an"] + ENC + [p]); parts.append(p)
        card = f"{T}/{fid}_{ar}_card.mp4"; cy = H // 2 - (120 if ar == "9x16" else 70)
        L = [(F(700), f["company"].upper(), 96 if ar == "9x16" else 72, "white", cy, 0.2), (F(600), f["title"], 44 if ar == "9x16" else 36, "0xf2c14e", cy + (120 if ar == "9x16" else 90), 0.5),
             (F(400), LANGX[f["lang"]][0], 26 if ar == "9x16" else 18, "0x9a9a9a", H - (160 if ar == "9x16" else 62), 0.3),
             (F(400), LANGX[f["lang"]][1], 26 if ar == "9x16" else 18, "0x9a9a9a", H - (120 if ar == "9x16" else 36), 0.3)]
        vf = ",".join(f"drawtext=fontfile={fn}:text='{esc(t)}':fontsize={s}:fontcolor={c}:x=(w-tw)/2:y={y}:alpha='min(1,max(0,(t-{a})/0.3))'" for fn, t, s, c, y, a in L)
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b0d:s={W}x{H}:r=24:d=4", "-vf", vf + ",fade=t=in:st=0:d=0.3", "-an"] + ENC + [card]); parts.append(card)
        ins = sum([["-i", p] for p in parts], []); n = len(parts)
        fc = ""; last = "[0:v]"; off = 0.0
        for k in range(1, n):
            off += (SEG if k <= len(f["clips"]) else SEG) - XF; fc += f"{last}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{k}];"; last = f"[x{k}]"
        silent = f"{T}/{fid}_{ar}_v.mp4"; run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc.rstrip(";"), "-map", last, "-an"] + ENC + [silent]); total = dur(silent)
        step = (total - 4) / len(f["clips"]); vin = []; vf2 = []
        for i, (k, line) in enumerate(f["vo"]): vin += ["-i", f"{OUT}/vo/{fid}_{i}.wav"]
        am = "".join(f"[{i+2}:a]adelay={int((k*step+0.4)*1000)}|{int((k*step+0.4)*1000)},volume=1.6[v{i}];" for i, (k, line) in enumerate(f["vo"]))
        vm = "".join(f"[v{i}]" for i in range(len(f["vo"])))
        fin = f"{OUT}/{fid}_{ar}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", f"{M}/{f['music']}.wav"] + vin + ["-filter_complex",
             f"[1:a]atrim=0:{total},volume=0.45,afade=t=out:st={total-2}:d=2[m];{am}{vm}amix=inputs={len(f['vo'])}:normalize=0[vo];[m][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", fin])
        print(fid, ar, round(total, 1), "s", flush=True)
