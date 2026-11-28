# Macedonian voice-over for the 10 Foton v2 films: Gemini TTS, voice Charon (as in the other Foton films),
# silence-trimmed, transcript-checked by Gemini (word count) and length-checked. Brand names are spelled for the TTS.
import os, sys, json, base64, re, subprocess, time, urllib.request, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); U = "https://generativelanguage.googleapis.com/v1beta/models/"
TTS = ["gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-pro-preview-tts"]
V9, G7, V7 = "Фотон Тунланд Ве-девет.", "Фотон Тунланд Ге-седум.", "Фотон Тунланд Ве-седум."
LINES = {
 "fv01_probij": {"l1": "Секоја граница е покана.", "l2": "Четиристотини педесет њутн-метри. Погон на сите четири тркала.", "l3": V9 + " Пробиј."},
 "fv02_nokjen_grad": {"l1": "Градот спие.", "l2": "Ти не.", "l3": "Тивка хибридна моќ. Осумстепен автоматски менувач.", "l4": V9 + " Ноќта е твоја."},
 "fv03_reka": {"l1": "Каде што патот завршува...", "l2": "...почнува приказната.", "l3": V9 + " Погон на сите четири тркала."},
 "fv04_nevreme": {"l1": "Надвор: невреме.", "l2": "Внатре: тишина.", "l3": "Пет години гаранција.", "l4": V9 + " Мирен во секое невреме."},
 "fv05_zima": {"l1": "Минус десет.", "l2": "Нула изговори.", "l3": "Погон на сите четири тркала. Секое утро.", "l4": V9 + " Подготвен за зима."},
 "fv06_detali": {"l1": "Секој детал.", "l2": "Со причина.", "l3": "Сто дваесет и девет киловати. Четиристотини педесет њутн-метри.", "l4": V9 + " Изграден до детал."},
 "fv07_molnja": {"l1": "Зошто да бидеш како сите?", "l2": "Осум бои. Една е твоја.", "l3": V9 + " Во боја на молња."},
 "fv08_vlecna_sila": {"l1": "Твојот викенд. Без компромис.", "l2": "Четиристотини педесет њутн-метри влечна сила.", "l3": V9 + " Влече без напор."},
 "fv09_raboten_den": {"l1": "Пет часот наутро.", "l2": "Работата не чека.", "l3": "Каминс дизел. Четиристотини педесет њутн-метри.", "l4": G7 + " Работи колку и ти."},
 "fv10_osum_boi": {"l1": "Осум бои.", "l2": "Еден карактер.", "l3": V9 + " Која боја е твоја?"},
 "fv11_pelisterski_oci": {"l1": "Над облаците.", "l2": "Таму каде што планината гледа.", "l3": V7 + " Погледни подалеку."},
}
CTA = "Закажи тест возење."
# a different Gemini voice for every film (owner's request), matched to the mood
VOICE = {"fv01_probij": "Fenrir", "fv02_nokjen_grad": "Algenib", "fv03_reka": "Puck", "fv04_nevreme": "Orus", "fv05_zima": "Kore",
         "fv06_detali": "Alnilam", "fv07_molnja": "Zephyr", "fv08_vlecna_sila": "Sadachbia", "fv09_raboten_den": "Iapetus",
         "fv10_osum_boi": "Laomedeia", "fv11_pelisterski_oci": "Aoede"}


def call(model, body, t=200):
    for a in range(40):
        m = TTS[a % len(TTS)] if model in TTS else model
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(f"{U}{m}:generateContent?key={K}", data=json.dumps(body).encode(),
                                                                             headers={"Content-Type": "application/json"}), timeout=t).read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503): time.sleep(15); continue
            raise
        except Exception: time.sleep(10)
    raise RuntimeError("TTS unavailable")


def words(s): return re.findall(r"\w+", s.lower())
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def tts(line, tr, voice="Charon"):
    raw_p = tr.replace(".wav", "_raw.wav"); pcm = tr.replace(".wav", ".pcm")
    for attempt in range(6):
        if os.path.exists(tr): return
        try:
            r = call("gemini-3.8-flash-tts", {"contents": [{"parts": [{"text": line}]}], "generationConfig": {"responseModalities": ["AUDIO"],
                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}})
            raw = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            if raw[:4] != b"RIFF":
                open(pcm, "wb").write(raw); subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", pcm, raw_p], check=True); os.remove(pcm)
            else: open(raw_p, "wb").write(raw)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw_p, "-af", "silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.05,"
                            "areverse,silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.15,areverse", tr], check=True); os.remove(raw_p)
            d = dur(tr)
            if d > 0.1 * len(line) + 0.9: print("too long", tr, round(d, 1), flush=True); os.remove(tr); continue
            t = call("gemini-2.5-flash", {"contents": [{"parts": [{"text": "Transcribe exactly every word spoken in this audio in its original language and script. Output only the transcript."},
                     {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(open(tr, "rb").read()).decode()}}]}]}, 120)["candidates"][0]["content"]["parts"][0]["text"]
            if re.search(r"\d", t): t = re.sub(r"[\d.,]+\s*(kW|Nm|кW)?", " x x x ", t)   # digits for spoken numbers
            if abs(len(words(t)) - len(words(line))) > max(1, len(words(line)) // 4) and not re.search(r"\d", line + t) and "x x x" not in t: print("mismatch", tr, "|", t.strip()[:90], flush=True); os.remove(tr)
        except Exception as e: print("retry", tr, type(e).__name__, str(e)[:100], flush=True); time.sleep(8)


if __name__ == "__main__":
    os.makedirs(f"{HERE}/vo", exist_ok=True)
    for fid, L in LINES.items():
        for lid, line in list(L.items()) + [("cta", CTA)]: tts(line, f"{HERE}/vo/{fid}_{lid}.wav", VOICE[fid])
    for fid, L in LINES.items():
        print(fid, VOICE[fid], " ".join(f"{lid}:{dur(f'{HERE}/vo/{fid}_{lid}.wav'):.1f}s" if os.path.exists(f"{HERE}/vo/{fid}_{lid}.wav") else f"{lid}:MISSING" for lid in list(L) + ["cta"]))
    print("VO_DONE")
