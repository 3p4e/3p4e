# Start keyframes for every shot: Gemini 3 Pro Image with the official Tunland photo as the vehicle reference.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from films import FILMS, KF_STYLE
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
os.makedirs(f"{S}/fv2/kf", exist_ok=True)
ONLY = set(sys.argv[1:])
todo = [d for f in FILMS for d in f["shot_defs"] if not ONLY or d["id"] in ONLY or d["id"].split("_s")[0] in ONLY]
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(5) as ex:
    list(ex.map(lambda d: gem(f"{S}/fv2/kf/{d['id']}.png", d["kf"] + KF_STYLE, [f"{S}/{d['ref']}"]), todo))
print("KF_DONE", len(todo))
