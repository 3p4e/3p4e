# Macedonian VO for the v3 site films that have no voice yet, with OpenAI gpt-audio-1.5 (owner, 2026-11-26: "use open ai api" while
# Gemini has no credit; gpt-4o-mini-tts mispronounced Macedonian in tests, gpt-audio-1.5 read it correctly). Checks: silence trim, length
# limit, transcript (gpt-4o-transcribe) must be Cyrillic with at most one unclear word (lines of 4+ words), else the line is redone.
# A film is voiced by one voice only: films with some Gemini lines are re-voiced completely.
#   python3 gen_vo_oa.py [film_id ...]
import os, sys, json, glob, re, subprocess, time, concurrent.futures as cf
import requests
HERE = os.path.dirname(os.path.abspath(__file__)); S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; REGEN = bool(os.environ.get("REGEN")); OUT = f"{S}/catfilms/" + ("vo_regen" if REGEN else "vo"); os.makedirs(OUT, exist_ok=True)
H = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
FEM, MAL = ["marin"], ["ash"]   # voice test on hard Macedonian lines: ash 92 %, marin 67 % (best female), the others 28-72 %
SYS = ("You are a native Macedonian voice actor recording a TV commercial ({tone}). Read the user's Macedonian text aloud exactly, word for word, "
       "with native Macedonian pronunciation and stress (not Serbian, not Bulgarian, not English). Say nothing else.")
STYLE = ("Speak Macedonian (Cyrillic text) with a natural native Macedonian accent and correct stress, as a premium TV commercial voice-over: "
         "{tone}. Calm, clear pacing, no English pronunciation.")
def words(s): return re.findall(r"\w+", s.lower())
_LAT = [("dž", "џ"), ("lj", "љ"), ("nj", "њ"), ("gj", "ѓ"), ("kj", "ќ"), ("dz", "ѕ"), ("š", "ш"), ("č", "ч"), ("ž", "ж"), ("ć", "ќ"), ("ḱ", "ќ"), ("đ", "ѓ"), ("ǵ", "ѓ"),
        ("a", "а"), ("b", "б"), ("c", "ц"), ("d", "д"), ("e", "е"), ("f", "ф"), ("g", "г"), ("h", "х"), ("i", "и"), ("j", "ј"), ("k", "к"), ("l", "л"), ("m", "м"),
        ("n", "н"), ("o", "о"), ("p", "п"), ("r", "р"), ("s", "с"), ("t", "т"), ("u", "у"), ("v", "в"), ("z", "з")]
def cyr(t):   # the transcriber sometimes writes Macedonian speech in Latin letters: compare it in Cyrillic
    t = t.lower()
    for a_, b_ in _LAT: t = t.replace(a_, b_)
    return t
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

def tts(line, tr, voice, tone):
    raw = tr.replace(".wav", "_raw.wav")
    for a in range(int(os.environ.get("VO_TRIES", "8"))):
        if os.path.exists(tr): return "ok"
        try:
            r = requests.post("https://api.openai.com/v1/chat/completions", headers=H, timeout=180, json={
                "model": "gpt-audio-1.5", "modalities": ["text", "audio"], "audio": {"voice": voice, "format": "wav"},
                "messages": [{"role": "system", "content": SYS.format(tone=tone)}, {"role": "user", "content": line}]})
            r.raise_for_status(); open(raw, "wb").write(__import__("base64").b64decode(r.json()["choices"][0]["message"]["audio"]["data"]))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.05,"
                            "areverse,silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.15,areverse", "-ar", "24000", "-ac", "1", tr], check=True); os.remove(raw)
            if dur(tr) > 0.1 * len(line) + 0.9: print("too long", os.path.basename(tr), round(dur(tr), 1), flush=True); os.remove(tr); continue
            with open(tr, "rb") as fh:
                t = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=H, timeout=120, files={"file": ("a.wav", fh, "audio/wav")},
                                  data={"model": "gpt-4o-transcribe", "language": "mk"}).json().get("text", "")
            t = cyr(t) if not re.search(r"[а-шА-Ш]", t) else t
            want, got = words(line), set(words(t)); miss = sum(w not in got for w in want); hit = 1 - miss / max(1, len(want))
            if not re.search(r"[а-шА-Ш]", t) or miss > (1 if len(want) >= 4 else 0) or len(words(t)) > len(want) + 2: print("mismatch", os.path.basename(tr), f"{hit:.0%}", "|", t[:80], flush=True); os.remove(tr); continue
            return "ok"
        except Exception as e: print("retry", os.path.basename(tr), str(e)[:120], flush=True); time.sleep(6 * (a + 1))
    return "FAIL"

films = ([json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(f"{HERE}/plan_regen/*.json"))] if REGEN else [f for p in sorted(glob.glob(f"{HERE}/plan/*.json")) for f in json.load(open(p, encoding="utf-8"))["films"] if f.get("batch") == "v3"])
only = set(sys.argv[1:]); voices = json.load(open(f"{OUT}/voices.json")) if os.path.exists(f"{OUT}/voices.json") else {}
jobs = []
for k, f in enumerate(films):
    if only and f["id"] not in only: continue
    paths = [f"{OUT}/{f['id']}_l{n}.wav" for n in range(1, len(f["vo_mk"]) + 1)]
    if all(os.path.exists(p) for p in paths): continue
    if not str(voices.get(f["id"], "")).startswith("openai:"):   # one voice per film: drop the Gemini lines of a partly voiced film
        for p in paths:
            if os.path.exists(p): os.remove(p)
    fem = f.get("voice", "").lower().startswith("female"); pool = FEM if fem else MAL; v = pool[k % len(pool)]; voices[f["id"]] = "openai:" + v
    tone = f.get("voice", "warm, confident").split(",", 1)[-1].strip() or "warm, confident"
    jobs += [(line, p, v, tone) for line, p in zip(f["vo_mk"], paths) if not os.path.exists(p)]
with cf.ThreadPoolExecutor(4) as ex: res = list(ex.map(lambda j: tts(*j), jobs))
json.dump(voices, open(f"{OUT}/voices.json", "w"), indent=1)
print("VO_OA lines", len(jobs), "failed", res.count("FAIL"))
