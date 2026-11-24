# Score every ACE-Step take against its mood brief with Gemini and copy the best take per mood to ace_final/.
import json, urllib.request, base64, glob, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from moods2 import MOODS2
k = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.gemini_paid")).read().strip()
SRC = "ace2"; DST = "ace_final"; os.makedirs(DST, exist_ok=True)
def ask(path, brief):
    q = (f"You are choosing background music for a TV commercial. The brief is: '{brief}', instrumental only. "
         "Reply with exactly one line: MATCH=<1-10> QUALITY=<1-10> VOCALS=<yes/no> ISSUES=<none or short>. "
         "MATCH is how well the mood, instruments and energy fit the brief.")
    b = {"contents": [{"parts": [{"text": q}, {"inline_data": {"mime_type": "audio/mpeg", "data": base64.b64encode(open(path, "rb").read()).decode()}}]}]}
    r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={k}",
        data=json.dumps(b).encode(), headers={"Content-Type": "application/json"}), timeout=200).read())
    return r["candidates"][0]["content"]["parts"][0]["text"].strip().splitlines()[0]
for name, m in MOODS2.items():
    best = None
    for f in sorted(glob.glob(f"{SRC}/{name}_t*.mp3")):
        t = ask(f, m["brief"])
        mt = re.search(r"MATCH=(\d+)", t); qt = re.search(r"QUALITY=(\d+)", t); vo = "VOCALS=yes" in t.replace(" ", "")
        score = (int(mt.group(1)) if mt else 0) * 2 + (int(qt.group(1)) if qt else 0) - (20 if vo else 0)
        print(os.path.basename(f), "|", t, "| score", score, flush=True)
        if best is None or score > best[0]: best = (score, f)
    if best: shutil.copy(best[1], f"{DST}/{name}.mp3"); print("  -> BEST", os.path.basename(best[1]), flush=True)
print("PICK_DONE")
