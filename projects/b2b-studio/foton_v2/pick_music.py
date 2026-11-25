# Scores both ACE-Step takes per film mood with Gemini (mood match, quality, no vocals) and writes the winner to music/<mood>.wav.
import json, urllib.request, base64, glob, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from moods_fv import MOODS2
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; K = open(f"{S}/.gemini_paid").read().strip()
SRC = f"{S}/fv2/music"; DST = f"{HERE}/music"; os.makedirs(DST, exist_ok=True)
def ask(path, brief):
    q = (f"You are choosing background music for an energetic pickup-truck TV commercial. The brief is: '{brief}', instrumental only. "
         "Reply with exactly one line: MATCH=<1-10> QUALITY=<1-10> ENERGY=<1-10> VOCALS=<yes/no> ISSUES=<none or short>.")
    b = {"contents": [{"parts": [{"text": q}, {"inline_data": {"mime_type": "audio/mpeg", "data": base64.b64encode(open(path, "rb").read()).decode()}}]}]}
    r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={K}",
        data=json.dumps(b).encode(), headers={"Content-Type": "application/json"}), timeout=200).read())
    return r["candidates"][0]["content"]["parts"][0]["text"].strip().splitlines()[0]
for name, m in MOODS2.items():
    best = None
    for f in sorted(glob.glob(f"{SRC}/{name}_t*.mp3")):
        try: t = ask(f, m["brief"])
        except Exception as e: t = f"ERR {e}"
        g = lambda k: int(re.search(k + r"=(\d+)", t).group(1)) if re.search(k + r"=(\d+)", t) else 0
        score = g("MATCH") * 2 + g("QUALITY") + g("ENERGY") - (25 if "VOCALS=yes" in t.replace(" ", "") else 0)
        print(os.path.basename(f), "|", t[:110], "| score", score, flush=True)
        if best is None or score > best[0]: best = (score, f)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", best[1], "-ar", "48000", "-ac", "2", f"{DST}/{name}.wav"], check=True)
    print("  ->", name, os.path.basename(best[1]), flush=True)
print("PICK_DONE")
