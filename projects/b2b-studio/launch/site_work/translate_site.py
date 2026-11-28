# Translates the site strings (tx_src.json, written by gen_site.py) into Albanian, Serbian (Latin), Croatian, Slovenian and Bulgarian
# with Gemini Pro; cache: i18n_extra.json {lang: {key: text}} plus the English source each was made from, so only new or changed
# strings are sent again. HTML tags, placeholders, numbers, prices and brand names are kept.
import json, os, re, sys, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip()
LANG = {"sq": "Albanian", "sr": "Serbian (Latin script)", "hr": "Croatian", "sl": "Slovenian", "bg": "Bulgarian (Cyrillic)", "zh": "modern Simplified Chinese (Mandarin, as used in mainland China; natural marketing copy, not word-for-word)"}
WORK = f"{S}/launch/site_work"   # gen_site.py builds from this copy
src = json.load(open(f"{WORK}/tx_src.json", encoding="utf-8"))
cp = f"{HERE}/i18n_extra.json"; X = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else {}
SRC = X.setdefault("_src", {})
CYR = re.compile("[\u0400-\u04FF]")
def ok(lang, k, v, items):
    mk, en = dict(items)[k]
    if lang in ("sq", "sr", "hr", "sl") and CYR.search(v) and not CYR.search(en): return False
    if lang != "bg" and v.strip() == mk.strip() and mk.strip() != en.strip(): return False
    return True
def ask(lang, items, tries=3):
    got = ask1(lang, items); good = {k: v for k, v in got.items() if ok(lang, k, v, items)}
    rest = [(k, v) for k, v in items if k not in good]
    if rest and tries > 1:
        print("retry", lang, len(rest), flush=True); good.update(ask(lang, rest, tries - 1))
    return good
def ask1(lang, items):
    prompt = (f"Translate these website strings of BIG DOGMA, an AI video studio in Skopje, into {LANG[lang]}. Each item gives the Macedonian "
              "original and the English version; translate from the English, write every string fully in {LANG[lang]} (never copy the Macedonian), "
              "and translate the meaning naturally for business customers (short, clear, same tone). Keep every HTML tag, "
              "entity, placeholder like {c} or {n}, number, price, currency, email, URL, and brand/product names (BIG DOGMA, LTX, Foton, Tunland, AI) unchanged. "
              "For names of North Macedonian places keep the usual local spelling in that language. Return ONLY a JSON object {key: translation}.\n\n"
              + json.dumps({k: {"mk": v[0], "en": v[1]} for k, v in items}, ensure_ascii=False))
    if os.environ.get("TRANSLATE_WITH") == "openai":   # owner, 2026-11-26: "use open ai api" while Gemini has no credit
        import requests
        for a in range(4):
            try:
                r = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, timeout=400,
                                  json={"model": "gpt-5.4-mini", "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": prompt}]})
                r.raise_for_status(); out = json.loads(r.json()["choices"][0]["message"]["content"]); return {k: out[k] for k, _ in items if isinstance(out.get(k), str)}
            except Exception as e: err = e
        print("FAIL", lang, len(items), err, flush=True); return {}
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={K}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=400).read())
            out = json.loads(r["candidates"][0]["content"]["parts"][0]["text"]); return {k: out[k] for k, _ in items if isinstance(out.get(k), str)}
        except Exception as e: err = e
    print("FAIL", lang, len(items), err, flush=True); return {}
jobs = []
for lang in LANG:
    have = X.setdefault(lang, {})
    todo = [(k, v) for k, v in src.items() if k not in have or SRC.get(k) != v[1]]
    for i in range(0, len(todo), 70): jobs.append((lang, todo[i:i + 70]))
print("chunks", len(jobs), flush=True)
with cf.ThreadPoolExecutor(6) as ex:
    for (lang, items), res in zip(jobs, ex.map(lambda j: ask(*j), jobs)):
        X[lang].update(res)
for k, v in src.items():
    if all(k in X[l] for l in LANG): SRC[k] = v[1]
json.dump(X, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
import shutil; shutil.copy(cp, f"{WORK}/i18n_extra.json")
print("done", {l: len(X[l]) for l in LANG}, "of", len(src))
