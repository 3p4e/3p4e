# Original music bed per category film with Lyria 3 Pro (Gemini API): instrumental, from the film's music mood; mp3 -> 48 kHz wav.
import os, json, glob, base64, subprocess, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); OUT = f"{S}/catfilms/music"; os.makedirs(OUT, exist_ok=True)
LEN = {"social": 20, "transform": 30, "story": 35, "explainer": 40}
def one(f):
    out = f"{OUT}/{f['id']}.wav"
    if os.path.exists(out): return "skip"
    txt = (f"Instrumental only, no vocals, about {LEN[f['type']]} seconds with a clear ending: {f['music']}. Premium commercial music bed "
           f"for a {f['type']} film about {f['title_en']} ({f['line_en']}), mixed to sit under a voice-over.")
    body = {"contents": [{"parts": [{"text": txt}]}], "generationConfig": {"responseModalities": ["AUDIO"]}}
    for a in range(5):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/lyria-3-pro-preview:generateContent?key={K}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=400).read())
            p = next(p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p)
            mp = out[:-4] + ".mp3"; open(mp, "wb").write(base64.b64decode(p["inlineData"]["data"]))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp, "-ar", "48000", "-ac", "2", out], check=True); os.remove(mp); return "ok"
        except urllib.error.HTTPError as e:
            if e.code == 402: return "402"
            time.sleep(15 * (a + 1))
        except Exception: time.sleep(10)
    return "FAIL"
films = [f for p in sorted(glob.glob(f"{HERE}/plan/*.json")) for f in json.load(open(p))["films"]]
with cf.ThreadPoolExecutor(4) as ex:
    for f, r in zip(films, ex.map(one, films)):
        if r not in ("ok", "skip"): print(f["id"], r, flush=True)
print("MUSIC_DONE", len(glob.glob(f"{OUT}/cf_*.wav")), "/", len(films))
