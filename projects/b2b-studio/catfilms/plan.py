# Category films v2: drafts the film plans (shot lists, VO, titles) per category with Gemini Pro (latest), then they are reviewed by hand.
# 19 existing site categories x 2 films + 6 new categories x 3 films; four types: social (15 s, 9:16), explainer (30-40 s, VO),
# story (30 s, brand mood), transform (before/after, start->end keyframes). Output: catfilms/plan/<cat>.json (prompts stay private:
# this folder is in the repo but the site only ever shows titles, lines and short descriptions).
import json, os, sys, urllib.request, concurrent.futures as cf
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KEY = open(f"{S}/.gemini_paid").read().strip()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan"); os.makedirs(OUT, exist_ok=True)
# (key, MK name, EN name, types for the new films, notes)
CATS = [
 ("automotive", "Автомобилска индустрија", "Automotive industry", ["social", "explainer"], "car parts and cable-harness factories in North Macedonia supplying European carmakers"),
 ("food", "Прехранбена индустрија", "Food industry", ["story", "social"], "bakeries, dairies, ajvar and pepper roasting, family food producers"),
 ("pharma", "Фармација", "Pharma", ["explainer", "transform"], "pharmaceutical production, clean rooms, packaging lines, pharmacies"),
 ("wine", "Винарии", "Wineries", ["social", "story"], "Tikveš region vineyards, Vranec grapes, harvest, cellars, tasting rooms"),
 ("steel_cement", "Челик и цемент", "Steel and cement", ["explainer", "social"], "steel mill, rolling mill, cement plant, concrete on building sites"),
 ("real_estate", "Недвижности", "Real estate", ["social", "explainer"], "new apartment buildings in Skopje, show flats, views over the city"),
 ("recruitment", "Вработување", "Recruitment", ["story", "social"], "employer branding: factories, offices and IT firms hiring in Macedonia"),
 ("product_launch", "Лансирање производ", "Product launch", ["social", "explainer"], "generic unbranded consumer products: headphones, sneakers, coffee machine"),
 ("industry_showreel", "Македонска индустрија", "Industry of North Macedonia", ["story", "social"], "a country that makes things: factories, farms, workshops, logistics"),
 ("construction", "Градба", "Construction", ["transform", "social"], "residential building rising from an empty plot in Skopje"),
 ("developer", "Инвеститори", "Property developers", ["explainer", "transform"], "off-plan sales: render to finished building, investor confidence"),
 ("apartment_staging", "Опремување станови", "Apartment staging", ["transform", "social"], "empty flat to furnished, styled home"),
 ("interior_design", "Внатрешен дизајн", "Interior design", ["transform", "story"], "designer interiors, materials, light"),
 ("office_fitout", "Опремување канцеларии", "Office fit-out", ["transform", "explainer"], "empty floor to modern office"),
 ("store_fitout", "Опремување продавници", "Store fit-out", ["transform", "social"], "empty shop unit to opening day"),
 ("expo_stand", "Саемски штандови", "Expo stands", ["transform", "social"], "trade-fair stand built overnight, opening crowd"),
 ("landscaping", "Хортикултура", "Landscaping", ["transform", "story"], "bare yard to garden, seasons"),
 ("solar", "Соларни системи", "Solar systems", ["explainer", "transform"], "rooftop and field solar installation, savings"),
 ("road", "Патна инфраструктура", "Road infrastructure", ["transform", "story"], "new road or highway section through Macedonian hills"),
 # new categories (market research: strongest local B2B video buyers outside the existing set)
 ("tourism", "Туризам и хотели", "Tourism and hotels", ["social", "story", "explainer"], "Lake Ohrid, Mavrovo, Struga, boutique hotels, guesthouses, summer and ski season"),
 ("horeca", "Ресторани и кафулиња", "Restaurants and cafés", ["social", "story", "transform"], "Skopje restaurants, Old Bazaar grills, cafés, chefs, delivery"),
 ("health", "Стоматологија и клиники", "Dental and private clinics", ["explainer", "social", "story"], "dental tourism, private clinics, modern equipment, caring staff"),
 ("agro", "Земјоделство", "Agriculture", ["story", "explainer", "social"], "Resen apples, Strumica vegetables, greenhouses, tobacco fields, modern farming"),
 ("textile", "Текстил и мода", "Textile and fashion", ["explainer", "social", "story"], "Štip garment factories, local fashion labels, design to production"),
 ("it", "ИТ и технологија", "IT and technology", ["story", "social", "explainer"], "Skopje software companies, startups, outsourcing teams, hiring developers"),
]
TYPES = {
 "social": "15-second vertical 9:16 social ad for Reels/TikTok: exactly 3 shots of 5 s, hook in shot 1, fast energy, 1 short VO line in Macedonian (max 8 words), vertical portrait composition with the subject centred",
 "explainer": "35-second horizontal 16:9 product/process explainer: exactly 7 shots of 5 s, Macedonian voice-over of 4-5 short sentences (max 14 words each) explaining how it works and why it is better",
 "story": "30-second horizontal 16:9 cinematic brand story, emotional and human: exactly 6 shots of 5 s, Macedonian VO of 2-3 poetic short lines (max 10 words each), music-led",
 "transform": "25-second horizontal 16:9 before/after transformation: exactly 4 shots; each shot has a START keyframe (before) and an END keyframe (after) of the SAME framing and camera position so the video morphs one into the other (timelapse feel); Macedonian VO of 2 short lines",
}
BRIEF = """You are the creative director of BIG DOGMA, an AI video studio in Skopje, North Macedonia. Write production plans for new demo films
for the category "{en}" ({mk}). Context: {notes}. The films are public studio demos on our website, so: NO real brand names, logos, readable text,
signage or real people; generic but premium and believable, set in North Macedonia (real places are fine). Every shot is generated: a keyframe image
(Gemini) animated by LTX-Video 2.5 for 5 seconds, so describe shots that animate well: one clear subject, simple physical motion, a slow camera move,
no crowds of faces, no hands doing fine work in close-up, no text. Make the two/three films clearly different from each other in look and idea.

Films to write: {films}

Return ONLY JSON: a list, one object per film in the same order:
{{"type": "...", "title_mk": "2-3 words", "title_en": "...", "line_mk": "slogan max 7 words", "line_en": "...",
  "desc_en": "one sentence describing the film for the website (no prompts)", "music": "music mood in 8-12 words incl. bpm",
  "voice": "male|female, tone in 3 words", "vo_mk": ["Macedonian VO lines (Cyrillic, natural, correct grammar)"],
  "shots": [{{"kf": "keyframe image description, 40-70 words: subject, setting, light, lens, composition, colour palette, photorealistic",
             "end_kf": "ONLY for transform: the same framing after the change, 40-70 words, else omit",
             "motion": "what moves in the 5 s and the camera move, 15-30 words"}}]}}"""
def ask(cat):
    key, mk, en, types, notes = cat
    films = "; ".join(f"film {i + 1}: {TYPES[t]}" for i, t in enumerate(types))
    body = {"contents": [{"parts": [{"text": BRIEF.format(en=en, mk=mk, notes=notes, films=films)}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.9}}
    for a in range(3):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={KEY}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=300).read())
            films = json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
            assert len(films) == len(types)
            for i, (f, t) in enumerate(zip(films, types)):
                f["type"] = t; f["id"] = f"cf_{key}_{i + 1}_{t}"; f["cat"] = key
            json.dump({"key": key, "mk": mk, "en": en, "films": films}, open(f"{OUT}/{key}.json", "w"), ensure_ascii=False, indent=1)
            return f"{key} ok {len(films)}"
        except Exception as e: err = e
    return f"{key} FAIL {err}"
if __name__ == "__main__":
    only = set(sys.argv[1:])
    with cf.ThreadPoolExecutor(8) as ex:
        for m in ex.map(ask, [c for c in CATS if not only or c[0] in only]): print(m, flush=True)
