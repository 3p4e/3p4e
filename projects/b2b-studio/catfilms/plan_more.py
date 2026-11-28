# "2 more videos for each sector" (owner, 2026-11-27): writes 2 NEW film plans per sector with gpt-5.2 using the same director rules as regen_plan.py.
# Output plan_more/<film id>.json (same schema as plan/<cat>.json films + "more": true). Merged into plan/<cat>.json after the films are cut.
import json, os, sys, re, glob, requests, collections, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/plan_more"; os.makedirs(OUT, exist_ok=True)
RULES = open(f"{HERE}/regen_plan.py", encoding="utf-8").read().split('RULES = """')[1].split('"""')[0].replace("rewriting a weak AI-generated 30-second film plan", "writing a NEW 30-second film plan").replace("Reviewers found the film generic, stock-looking and disconnected. Rewrite the shot list so it is clearly better:", "Make it specific, cinematic and clearly NOT stock-looking:")
TYPES = {"commercial": "30-second 16:9 commercial for a typical local business of this sector (unbranded, no readable text): 5 shots", "social": "15-second vertical 9:16 social spot: 3 shots, hook in the first second",
         "explainer": "30-40 second 16:9 process explainer with Macedonian voice-over: 5 shots following ONE person and ONE product/process", "story": "30-second 16:9 brand-mood story, emotional, 5 shots, one hero",
         "transform": "before/after 16:9 film: 5 shots, each with kf (before) and end_kf (after) of the SAME room and camera angle"}
PHYS = {"apartment_staging", "construction", "developer", "expo_stand", "interior_design", "landscaping", "office_fitout", "road", "solar", "store_fitout", "furniture", "beauty", "events", "horeca", "pharma", "real_estate"}
def pick(cat, have):
    c = collections.Counter(f["type"] for f in have); order = ["story", "explainer", "social", "commercial"] + (["transform"] if cat in PHYS else [])
    base = list(order); return sorted(order, key=lambda t: (c[t], base.index(t)))[:2]
def one(job):
    cat, k, typ, d = job; fid = f"cf_{cat}_{k}_{typ}"
    if os.path.exists(f"{OUT}/{fid}.json"): return fid, "skip"
    have = "; ".join(f["title_en"] for f in d["films"])
    msg = RULES + f"\n\nSECTOR: {d['en']} ({d['mk']}). FILM TYPE: {typ}: {TYPES[typ]}.\nThe site already has these films for this sector, so the new one must be clearly different in story, hero, place and look: {have}.\nReturn JSON for one film with keys type,title_mk,title_en,line_mk,line_en,desc_en,music,voice,vo_mk,shots."
    for a in range(3):
        try:
            r = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                json={"model": "gpt-5.2", "messages": [{"role": "user", "content": msg}], "response_format": {"type": "json_object"}}, timeout=300).json()
            nf = json.loads(r["choices"][0]["message"]["content"]); nf["type"] = typ; assert len(nf["shots"]) in (3, 5) and nf["vo_mk"] and all(s.get("kf") and s.get("motion") for s in nf["shots"])
            if typ == "transform": assert all(s.get("end_kf") for s in nf["shots"])
            nf.update(id=fid, cat=cat, batch="v3", more=True); json.dump(nf, open(f"{OUT}/{fid}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1); return fid, "ok"
        except Exception as e: err = str(e)[:120]
    return fid, "FAIL " + err
if __name__ == "__main__":
    jobs = []
    for p in sorted(glob.glob(f"{HERE}/plan/*.json")):
        d = json.load(open(p, encoding="utf-8"))
        if d["key"] == "oled": continue
        n = len(d["films"])
        for i, t in enumerate(pick(d["key"], d["films"])): jobs.append((d["key"], n + 1 + i, t, d))
    with cf.ThreadPoolExecutor(6) as ex:
        for fid, st in ex.map(one, jobs):
            if st != "skip": print(fid, st, flush=True)
    print("DONE", len(glob.glob(f"{OUT}/*.json")), "/", len(jobs))
