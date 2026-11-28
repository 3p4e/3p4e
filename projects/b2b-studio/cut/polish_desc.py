# Proofread the shot descriptions: natural, idiomatic mk / sr (Latin, ekavian) / sq, same meaning, no names, no prompt jargon.
import json, time, urllib.request
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); U = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
F = f"{S}/cut/shot_desc.json"; D = json.load(open(F)); ids = sorted(D)
for i in range(0, len(ids), 20):
    chunk = {k: {l: D[k][l] for l in ("mk", "sr", "sq")} for k in ids[i:i + 20]}
    txt = ("You are a native copy editor for Macedonian (Cyrillic), Serbian (Latin, ekavian) and Albanian. These are short captions "
           "under AI video clips on a business web page, with the English meaning given. Rewrite each so it reads naturally and "
           "idiomatically, like a native ad copywriter would write it, keeping the same meaning and length (8 to 14 words). No names, "
           "no words like 'camera'/'kamera' unless needed, no technical terms. Return JSON with the same ids and keys mk, sr, sq.\n\n"
           + json.dumps({k: dict(v, en=D[k]["en"]) for k, v in chunk.items()}, ensure_ascii=False))
    body = {"contents": [{"parts": [{"text": txt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}}
    for a in range(5):
        try:
            r = json.loads(json.loads(urllib.request.urlopen(urllib.request.Request(U + K, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=180).read())["candidates"][0]["content"]["parts"][0]["text"]); break
        except Exception as e: print("retry", str(e)[:80], flush=True); time.sleep(6 * (a + 1)); r = {}
    for k in chunk:
        v = r.get(k)
        if isinstance(v, dict):
            for l in ("mk", "sr", "sq"):
                if v.get(l): D[k][l] = v[l].strip()
    json.dump(D, open(F, "w"), ensure_ascii=False, indent=1); print(i + len(chunk), flush=True)
print("POLISH_DONE")
