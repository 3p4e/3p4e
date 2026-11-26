# Category films v3 (owner, 2026-11-26): 2 new 30-second commercials for each of the 25 existing site industries, and 12 new industries
# with 5 films each (2 commercials + social 9:16 + explainer + story or transform). Same planner as plan.py (Gemini Pro writes, then
# reviewed by hand); new films are appended to plan/<cat>.json with "batch": "v3", existing films are never touched.
#   python3 plan_v3.py [cat ...]
import json, os, sys, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); g = {"__file__": os.path.join(HERE, "plan.py")}
exec(open(f"{HERE}/plan.py", encoding="utf-8").read().split("def ask")[0], g)
S, KEY, OUT, CATS, TYPES, BRIEF = g["S"], g["KEY"], g["OUT"], g["CATS"], dict(g["TYPES"]), g["BRIEF"]
TYPES["commercial"] = ("30-second horizontal 16:9 commercial for a typical local business in this industry (unbranded): exactly 5 shots of 5 s with "
                       "a clear arc (hook, desire or problem, the service or product in action, people benefiting, payoff). ONE recurring main "
                       "character (describe the same age, hair and clothes in every shot where they appear) or one hero product. Macedonian "
                       "voice-over of exactly 5 short lines, one per shot, max 10 words each; the last line is the slogan")
NEW = [
 ("banking", "Банкарство и финансии", "Banking and finance", ["commercial", "commercial", "social", "explainer", "story"], "retail and business banking in Skopje: a first home loan, a small business growing, a branch adviser, paying by phone (screens never readable)"),
 ("insurance", "Осигурување", "Insurance", ["commercial", "commercial", "social", "explainer", "story"], "car, home, health and travel insurance; a claim handled fast; families and small businesses protected"),
 ("telecom", "Телекомуникации и интернет", "Telecom and internet", ["commercial", "commercial", "social", "explainer", "story"], "fibre and 5G across Macedonian towns and villages, families streaming, remote work, technicians on masts (no operator brands)"),
 ("logistics", "Логистика и транспорт", "Logistics and transport", ["commercial", "commercial", "social", "explainer", "story"], "warehouses, trucks on the Corridor 10 highway, last-mile delivery vans in Skopje, cold chain, border crossings"),
 ("beverages", "Пијалоци", "Beverages", ["commercial", "commercial", "social", "explainer", "story"], "mineral water from mountain springs, fruit juices, local craft breweries, bottling lines, summer refreshment (no labels)"),
 ("retail", "Супермаркети и малопродажба", "Supermarket and retail chains", ["commercial", "commercial", "social", "explainer", "story"], "neighbourhood supermarkets, fresh produce and bakery counters, friendly cashiers, a new store opening"),
 ("beauty", "Убавина и козметика", "Beauty and cosmetics", ["commercial", "commercial", "social", "explainer", "transform"], "beauty salons, barbershops, skincare and cosmetics, spa treatments (no fine close-up hand work)"),
 ("fitness", "Фитнес и спорт", "Fitness and sport", ["commercial", "commercial", "social", "explainer", "story"], "gyms, personal trainers, running along the Vardar quay, football academies for kids, sports clubs"),
 ("education", "Образование", "Education", ["commercial", "commercial", "social", "explainer", "story"], "private schools and kindergartens, universities, language and coding schools, campus life in Skopje, Bitola, Štip"),
 ("furniture", "Мебел и дом", "Furniture and home", ["commercial", "commercial", "social", "explainer", "transform"], "Macedonian furniture makers, wood workshops, showrooms, kitchens and living rooms"),
 ("energy", "Енергија и е-полнење", "Energy and EV charging", ["commercial", "commercial", "social", "explainer", "story"], "electricity for homes and factories, heat pumps, EV chargers in Skopje and along highways, smart home energy"),
 ("events", "Настани и свадби", "Events and weddings", ["commercial", "commercial", "social", "explainer", "transform"], "wedding venues by Lake Ohrid, event halls, catering, decor, concerts and corporate events"),
]
EXTRA = "\nThese are NEW films for this category; the site already has these, so make the new ones clearly different in story and look: {have}."

def ask(key, mk, en, types, notes, have):
    films = "; ".join(f"film {i + 1}: {TYPES[t]}" for i, t in enumerate(types))
    text = BRIEF.format(en=en, mk=mk, notes=notes, films=films) + (EXTRA.format(have=have) if have else "")
    text += ('\nFor commercial films add to every shot "char": true when the recurring main character or hero product is visible in it '
             '(so the keyframe can be generated from the first shot of that character), else false.')
    body = {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.9}}
    for a in range(3):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY}), timeout=300).read())
            films = json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
            assert len(films) == len(types)
            for f, t in zip(films, types):
                assert len(f["shots"]) == {"commercial": 5, "social": 3, "explainer": 7, "story": 6, "transform": 4}[t], (t, len(f["shots"]))
                if t == "commercial": assert len(f["vo_mk"]) == 5
            return films
        except Exception as e: err = e
    raise RuntimeError(f"{key}: {err}")

def one(cat):
    key, mk, en, types, notes = cat; p = f"{OUT}/{key}.json"
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"key": key, "mk": mk, "en": en, "films": []}
    if any(f.get("batch") == "v3" for f in d["films"]): return f"{key} already planned"
    have = "; ".join(f"{f['type']} '{f['title_en']}' ({f['desc_en']})" for f in d["films"])
    films = ask(key, mk, en, types, notes, have); n0 = len(d["films"])
    for i, (f, t) in enumerate(zip(films, types)):
        f.update(type=t, id=f"cf_{key}_{n0 + i + 1}_{t}", cat=key, batch="v3")
    d["films"] += films; json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return f"{key} +{len(films)} ({', '.join(f['title_en'] for f in films)})"

if __name__ == "__main__":
    only = set(sys.argv[1:])
    todo = [(c[0], c[1], c[2], ["commercial", "commercial"], c[4]) for c in CATS] + NEW
    with cf.ThreadPoolExecutor(8) as ex:
        for m in ex.map(one, [c for c in todo if not only or c[0] in only]): print(m, flush=True)
