# energetic Macedonian VO for the Foton action films (Gemini TTS, voice Charon as in the other Foton films), with transcript check
import sys, os, json, base64, re, subprocess, time
sys.path.insert(0, "../vo"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open("../vo/gen_vo4.py").read().split("def words")[0].replace("from batch2 import VO\n", "")
exec(src)
def words(s): return re.findall(r"\w+", s.lower())
LINES = {"act_1": "Асфалтот е само почеток!", "act_2": "Песок!", "act_3": "Вода!", "act_4": "Кал!",
         "act_5": "Погон на сите четири тркала. Електрична блокада.", "act_6": "Два литри турбо дизел. Хибридна моќ.",
         "act_7": "Foton Tunland V9. Нема граници!", "act_8": "Закажи тест возење."}
STYLE = ""
for lid, line in LINES.items():
    out, tr = f"vo/{lid}_raw.wav", f"vo/{lid}.wav"
    for attempt in range(6):
        if os.path.exists(tr): break
        try:
            r = call("gemini-3.8-flash-tts", {"contents": [{"parts": [{"text": STYLE + line}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Charon"}}}}})
            raw = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            if raw[:4] != b"RIFF": open("t.pcm", "wb").write(raw); subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "t.pcm", out], check=True)
            else: open(out, "wb").write(raw)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.15,areverse", tr], check=True)
            t = call("gemini-2.5-flash", {"contents": [{"parts": [{"text": "Transcribe exactly every word spoken in this audio in its original language and script. Output only the transcript."}, {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(open(tr, "rb").read()).decode()}}]}]}, 120)["candidates"][0]["content"]["parts"][0]["text"]
            dd = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",tr],capture_output=True,text=True).stdout)
            if dd > 0.11 * len(line) + 0.8: print("too long", lid, round(dd,1), flush=True); os.remove(tr); continue
            if abs(len(words(t)) - len(words(line))) > max(0, len(words(line)) // 5): print("mismatch", lid, t.strip()[:80], flush=True); os.remove(tr)
        except Exception as e:
            body = e.read().decode()[:200] if hasattr(e, "read") else ""
            print("retry", lid, type(e).__name__, str(e)[:80], body.replace("\n", " "), flush=True); time.sleep(8)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", tr], capture_output=True, text=True).stdout.strip() if os.path.exists(tr) else "MISSING"
    print(lid, line, d, flush=True)
print("VO_DONE")
