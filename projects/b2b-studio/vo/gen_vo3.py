import json, base64, urllib.request, os, time, subprocess, re
from vo_extra import VO
k = os.environ.get("GEMINI_API_KEY") or open("../.gemini_paid").read().strip()
U = "https://generativelanguage.googleapis.com/v1beta/models/"
TTS = ["gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-pro-preview-tts", "gemini-3.8-flash-lite-tts"]
def call(model, body, t=200):
    for a in range(40):
        m = TTS[a % len(TTS)] if model in TTS else model
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(f"{U}{m}:generateContent?key={k}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=t).read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503): time.sleep(15); continue
            raise
        except Exception: time.sleep(10)
    raise RuntimeError("429 limit")
def words(s): return re.findall(r"\w+", s.lower())
os.makedirs("lines", exist_ok=True); os.makedirs("trim", exist_ok=True); bad = []
for cid, (lang, voice, lines) in VO.items():
    for i, line in enumerate(lines, 1):
        out = f"lines/{cid}_{i}.wav"; tr = f"trim/{cid}_{i}.wav"; ok = os.path.exists(tr)
        for attempt in range(6):
            if ok: break
            try:
                time.sleep(6)
                r = call("gemini-3.8-flash-tts", {"contents": [{"parts": [{"text": line}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}})
                open(out, "wb").write(base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))
                raw = open(out, "rb").read()
                if raw[:4] != b"RIFF":
                    open("t.pcm", "wb").write(raw); subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "t.pcm", out], check=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.2,areverse", tr], check=True)
                t = call("gemini-2.5-flash", {"contents": [{"parts": [{"text": "Transcribe exactly every word spoken in this audio in its original language and script. Output only the transcript."}, {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(open(tr, "rb").read()).decode()}}]}]}, 120)["candidates"][0]["content"]["parts"][0]["text"]
                ok = abs(len(words(t)) - len(words(line))) <= max(1, len(words(line))//5)
                if not ok: os.remove(tr)
            except Exception as e:
                print('retry', cid, i, type(e).__name__, flush=True); time.sleep(10)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", tr], capture_output=True, text=True).stdout or 0) if ok else 0
        print(cid, i, "OK" if ok else "BAD", round(d, 1), flush=True)
        if not ok: bad.append((cid, i))
print("VO3_DONE bad:", bad)
