import json, os
from concurrent.futures import ThreadPoolExecutor
from tts import take
from script import SEGMENTS
VOICES = {"narrator": "Leda", "professor": "Gacrux"}
os.makedirs("parts", exist_ok=True)
jobs = [(seg, i, role, text) for seg, parts in SEGMENTS for i, (role, text) in enumerate(parts)]
def run(j):
    seg, i, role, text = j
    fn = f"parts/seg{seg}_{i}_{role}.mp3"
    if os.path.exists(fn):
        return {"seg": seg, "i": i, "role": role, "file": fn, "text": text, "match": None, "cached": True}
    score, model, heard = take(fn, text, VOICES[role], role)
    return {"seg": seg, "i": i, "role": role, "file": fn, "text": text, "match": round(score, 2), "model": model, "heard": heard}
with ThreadPoolExecutor(3) as ex:
    out = list(ex.map(run, jobs))
for o in out:
    print(o["seg"], o["i"], o["role"], o["match"], o.get("model"), flush=True)
json.dump(out, open("parts.json", "w"), ensure_ascii=False, indent=1)
