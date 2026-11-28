# Macedonian VO for the category films: Gemini TTS with the Foton v2 checks (silence trim, length and transcript check),
# voice picked per film from its plan ("male"/"female") and rotated so neighbouring films sound different.
import os, sys, json, glob, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "foton_v2")); from gen_vo import tts, dur
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; OUT = f"{S}/catfilms/vo"; os.makedirs(OUT, exist_ok=True)
FEM = ["Kore", "Aoede", "Leda", "Despina", "Callirrhoe", "Autonoe", "Erinome", "Vindemiatrix", "Sulafat", "Laomedeia", "Achernar", "Pulcherrima"]
MAL = ["Charon", "Orus", "Iapetus", "Alnilam", "Enceladus", "Fenrir", "Puck", "Algenib", "Sadachbia", "Schedar", "Umbriel", "Achird"]
films = [f for p in sorted(glob.glob(f"{HERE}/plan/*.json")) for f in json.load(open(p))["films"]]
jobs, voices = [], {}
for k, f in enumerate(films):
    pool = FEM if f.get("voice", "").lower().startswith("female") else MAL; v = pool[k % len(pool)]; voices[f["id"]] = v
    for n, line in enumerate(f["vo_mk"], 1): jobs.append((line, f"{OUT}/{f['id']}_l{n}.wav", v))
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(lambda j: tts(*j), jobs))
json.dump(voices, open(f"{OUT}/voices.json", "w"), indent=1)
miss = [os.path.basename(j[1]) for j in jobs if not os.path.exists(j[1])]
print("lines", len(jobs), "missing", len(miss), miss[:10]); print("VO_DONE")
