import base64, difflib, json, os, re, subprocess, urllib.request
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
CHECK_MODEL = "gemini-2.5-flash-lite"
KEYS = ["AZ_GEMINI_API_KEY", "BN_GEMINI_API", "EP_GEMINI_API", "UC_GEMINI_API"]
MODELS = ["gemini-3.8-flash-tts"]  # one model for every part, so the voices stay consistent
PREFIX = {  # inline style tags; this model reads plain-English instructions aloud
    "narrator": "[warmly and gently, like telling a story to small children] ",
    "professor": "[excited, warm, a little funny old professor] ",
}

def tts(text, voice, role):
    import time
    last = None
    for rnd in range(6):
        if rnd:
            time.sleep(20 * rnd)
        try:
            return _tts(text, voice, role)
        except RuntimeError as e:
            last = e
    raise last

def _tts(text, voice, role):
    last = None
    for m in MODELS:
        for k in KEYS:
            body = {"contents": [{"parts": [{"text": PREFIX[role] + text}]}],
                    "generationConfig": {"responseModalities": ["AUDIO"],
                                         "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                         data=json.dumps(body).encode(),
                                         headers={"x-goog-api-key": os.environ[k], "Content-Type": "application/json"})
            try:
                r = json.load(urllib.request.urlopen(req, timeout=180))
                return base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]), m
            except urllib.error.HTTPError as e:
                last = f"{k}/{m} {e.code} {e.read().decode()[:120]}"
            except (KeyError, IndexError):
                last = f"{k}/{m} no audio"
    raise RuntimeError(last)

def words(s):
    return re.sub(r"[^\w\s]", " ", s.lower()).split()

def check(fn, text):
    """Gemini transcription vs script: similarity of word sequences."""
    audio = base64.b64encode(open(fn, "rb").read()).decode()
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": audio}},
                                    {"text": "Transcribe this Macedonian speech exactly, in Macedonian Cyrillic. "
                                             "Output only the transcript."}]}]}
    for k in KEYS:
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{CHECK_MODEL}:generateContent",
                                     data=json.dumps(body).encode(),
                                     headers={"x-goog-api-key": os.environ[k], "Content-Type": "application/json"})
        try:
            heard = json.load(urllib.request.urlopen(req, timeout=180))["candidates"][0]["content"]["parts"][0]["text"]
            return difflib.SequenceMatcher(None, words(text), words(heard)).ratio(), heard
        except (urllib.error.HTTPError, KeyError, IndexError):
            continue
    return 0.0, ""


def render(fn, text, voice, role):
    pcm, model = tts(text, voice, role)
    tmp = fn + ".pcm"
    open(tmp, "wb").write(pcm)
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", tmp,
                    "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                           "silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                    "-b:a", "128k", fn], check=True)
    os.remove(tmp)
    return model

def take(fn, text, voice, role, tries=5):
    """Render and verify; accept a take only if the words match and the pace is natural."""
    n = max(len(words(text)), 1)
    best = (-9, None, None, None)
    for i in range(tries):
        cand = fn.replace(".mp3", f".t{i}.mp3")
        model = render(cand, text, voice, role)
        dur = os.path.getsize(cand) * 8 / 128000
        score, heard = check(cand, text)
        if not heard:
            score, heard = check(cand, text)
        pace_ok = dur <= 1.5 + 0.85 * n
        good = (score >= 0.8 or n <= 1) and pace_ok
        rank = score - (0 if pace_ok else 1)
        if rank > best[0]:
            best = (rank, cand, model, heard)
        if good:
            break
    for i in range(tries):
        c = fn.replace(".mp3", f".t{i}.mp3")
        if c == best[1]:
            os.replace(c, fn)
        elif os.path.exists(c):
            os.remove(c)
    return best[0], best[2], best[3]
