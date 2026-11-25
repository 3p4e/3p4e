# Subtitles for every LTX film in mk / sr (Latin) / sq / en from subs/timing.json (exact VO positions).
# Lines are translated with Gemini (text only), one request per film, JSON out; then SRT files are written.
import os, json, re, urllib.request, time
from concurrent.futures import ThreadPoolExecutor
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); U = "https://generativelanguage.googleapis.com/v1beta/models/"
T = json.load(open(f"{S}/subs/timing.json")); OUT = f"{S}/subs/srt"; os.makedirs(OUT, exist_ok=True)
NAMES = {"mk": "Macedonian (Cyrillic)", "sr": "Serbian (Latin script, ekavian)", "sq": "Albanian (standard)", "en": "English"}
CACHE = f"{S}/subs/translations.json"; TR = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def gem(prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}
    for a in range(6):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"{U}gemini-2.5-flash:generateContent?key={K}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=180).read())
            return json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
        except Exception as e: print("retry", str(e)[:100], flush=True); time.sleep(8 * (a + 1))
    raise RuntimeError("gemini failed")
def translate(film):
    if film in TR: return
    src = T[film]["lang"]; lines = [l["text"] for l in T[film]["lines"]]; targets = [k for k in NAMES if k != src]
    p = (f"You are subtitling a short TV commercial. The voice-over lines below are in {NAMES[src]}. Translate each line into "
         + ", ".join(f"{k} = {NAMES[k]}" for k in targets) + ". Keep them short, natural and punchy like advertising copy, same meaning, "
         "keep brand and product names unchanged (e.g. Foton, Tunland V9, Vincinni, Alkaloid, Replek, Žito/Жито, Nelt, SPEEEX, Viva Fresh, Gener 2, Concord, Millennium Team, Beograd na vodi). "
         "Return JSON: {\"" + "\": [..], \"".join(targets) + "\": [..]} with exactly " + str(len(lines)) + " strings per language, in order.\n\n"
         + "\n".join(f"{i+1}. {l}" for i, l in enumerate(lines)))
    r = gem(p)
    assert all(len(r[k]) == len(lines) for k in targets), (film, {k: len(r.get(k, [])) for k in targets})
    r[src] = lines; TR[film] = r; print("ok", film, flush=True)
def wrap(t, n=42):
    if len(t) <= n: return t
    mid = len(t) // 2; sp = [i for i, c in enumerate(t) if c == " "]
    if not sp: return t
    i = min(sp, key=lambda x: abs(x - mid)); return t[:i] + "\n" + t[i + 1:]
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"
with ThreadPoolExecutor(6) as ex: list(ex.map(translate, sorted(T)))
json.dump(TR, open(CACHE, "w"), ensure_ascii=False, indent=1)
n = 0
for film, d in T.items():
    L = d["lines"]
    for lang in NAMES:
        out = []
        for i, l in enumerate(L):
            st = l["t0"]; en = max(l["t1"] + 0.35, st + 1.0)
            if i + 1 < len(L): en = min(en, L[i + 1]["t0"] - 0.05)
            out.append(f"{i+1}\n{ts(st)} --> {ts(en)}\n{wrap(TR[film][lang][i])}\n")
        open(f"{OUT}/{film}.{lang}.srt", "w").write("\n".join(out)); n += 1
print("SRT_DONE", n)
