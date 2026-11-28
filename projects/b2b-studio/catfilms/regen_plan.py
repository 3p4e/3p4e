# Review 2026-11-27 regeneration: asks gpt-5.2 to rewrite the shot plans of the weak sector films from the reviewers' notes.
# Output: plan_regen/<film id>.json (same schema as plan/<cat>.json films, plus "regen": true). Prompts stay private in the repo like plan/.
#   python3 regen_plan.py [film ids]   (default: the priority-1 list)
import json, os, sys, re, glob, requests, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = f"{HERE}/plan_regen"; os.makedirs(OUT, exist_ok=True)
P1 = open(f"{HERE}/../review/REVIEW_2026-11-27.md", encoding="utf-8").read().split("Priority 1")[1].split("\n")[0]
IDS = sys.argv[1:] or re.findall(r"cf_[a-z_]+_\d_[a-z]+", P1)
V = {re.sub(r".*/|\.mp4", "", x["item"]): x for x in json.load(open(f"{S}/review/all_verdicts.json")) if "cf_" in x["item"]}
RULES = """You are a senior commercial director rewriting a weak AI-generated 30-second film plan for a Skopje studio. Reviewers found the film generic, stock-looking and disconnected. Rewrite the shot list so it is clearly better:
- ONE coherent story in ONE or TWO specific North Macedonian locations (Skopje old bazaar, Vardar quay, Kale, Mavrovo, Ohrid, Tikves, Kumanovo, Veles, real Balkan streets, signage-free). Avoid generic Western stock look.
- A single recurring hero (same age, hair, clothes, in every shot where visible) or a single hero object; keep props, colours and the room IDENTICAL across shots. Explainers: one process shown step by step with one person and one product, not five unrelated stock shots. Transform films: the SAME room and camera angle in start and end frames (kf = before, end_kf = after, only the changes that matter).
- Every shot keyframe prompt must be concrete: subject, action, framing, lens, light, time of day, colour palette, 40-70 words, photorealistic, NO readable text, signs or logos anywhere. Hands and faces simple and unambiguous.
- Motion prompt per shot: ONE clear physical action plus ONE camera move, 20-35 words, physically plausible in 5 seconds.
- Exactly 5 shots for commercial/explainer/story/transform, 3 for social (9:16). Keep the same number of vo_mk lines as shots (explainer may keep its count). Macedonian voice-over, short, natural, max 10 words per line; the last line is a slogan matching line_mk (<= 28 characters so it fits the end card).
- Keep keys exactly: type,title_mk,title_en,line_mk,line_en,desc_en,music,voice,vo_mk,shots[{kf,motion,char,end_kf?}]. 'char': true when the hero is visible. Return ONLY JSON for one film."""
def one(fid):
    m = re.match(r"cf_(.+)_(\d)_([a-z]+)$", fid); cat, n = m.group(1), int(m.group(2))
    f = json.load(open(f"{HERE}/plan/{cat}.json", encoding="utf-8"))["films"][n - 1]; assert f["id"] == fid, (f["id"], fid)
    v = V.get(fid, {}); old = {k: f[k] for k in f if k not in ("id", "cat", "batch")}
    msg = RULES + f"\n\nREVIEWER NOTE (score {v.get('score')}): {v.get('issues')}\nSUGGESTED FIX: {v.get('fix')}\n\nCURRENT PLAN:\n" + json.dumps(old, ensure_ascii=False)
    for a in range(3):
        try:
            r = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                json={"model": "gpt-5.2", "messages": [{"role": "user", "content": msg}], "response_format": {"type": "json_object"}}, timeout=300).json()
            nf = json.loads(r["choices"][0]["message"]["content"]); assert nf["type"] == f["type"] and len(nf["shots"]) in (3, 5)
            nf.update(id=fid, cat=cat, batch="v3", regen=True); json.dump(nf, open(f"{OUT}/{fid}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1); return fid, "ok"
        except Exception as e: err = str(e)[:150]
    return fid, "FAIL " + err
if __name__ == "__main__":
    todo = [i for i in IDS if not os.path.exists(f"{OUT}/{i}.json")]
    with cf.ThreadPoolExecutor(6) as ex:
        for fid, st in ex.map(one, todo): print(fid, st, flush=True)
    print("DONE", len(glob.glob(f"{OUT}/*.json")), "/", len(IDS))
