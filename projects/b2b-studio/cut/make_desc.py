# Short public descriptions of each LTX shot (what is shown + what moves), written fresh from the prompt so the pages never
# show the prompt itself. Text only goes to Gemini. Output: cut/shot_desc.json {shot id: {mk, sr, sq, en}}.
import json, os, time, urllib.request
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); U = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
OUT = f"{S}/cut/shot_desc.json"; D = json.load(open(OUT)) if os.path.exists(OUT) else {}
P = {}
for b in ("cb2", "cb5", "cb6", "cb7", "cb9", "cb10"):
    for j in json.load(open(f"{S}/{b}/jobs.json"))["jobs"]: P[j["id"]] = j.get("prompt", "")
todo = [k for k in P if k not in D and P[k]]
def gem(items):
    txt = ("For each video shot below, write ONE short caption for a client-facing web page (8 to 14 words): what the viewer sees "
           "and what moves (camera move or action), in plain natural language. Do NOT copy or quote the prompt wording, no technical "
           "terms (no 'shot', 'prompt', 'cinematic', lens, fps, style words), NO company, brand, product or person names, no numbers. "
           "Give it in four languages: mk = Macedonian (Cyrillic), sr = Serbian (Latin script, ekavian), sq = Albanian, en = English. "
           "Return JSON {id: {\"mk\": .., \"sr\": .., \"sq\": .., \"en\": ..}} for exactly these ids.\n\n"
           + "\n".join(f"[{k}] {v[:700]}" for k, v in items))
    body = {"contents": [{"parts": [{"text": txt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.4}}
    for a in range(5):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(U + K, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=180).read())
            return json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
        except Exception as e: print("retry", str(e)[:80], flush=True); time.sleep(6 * (a + 1))
    return {}
for i in range(0, len(todo), 15):
    chunk = [(k, P[k]) for k in todo[i:i + 15]]; r = gem(chunk)
    for k, _ in chunk:
        v = r.get(k)
        if isinstance(v, dict) and all(v.get(l) for l in ("mk", "sr", "sq", "en")): D[k] = {l: v[l].strip() for l in ("mk", "sr", "sq", "en")}
    json.dump(D, open(OUT, "w"), ensure_ascii=False, indent=1); print(len(D), "/", len(P), flush=True)
print("DESC_DONE", len(D), "missing", [k for k in P if k not in D and P[k]])
