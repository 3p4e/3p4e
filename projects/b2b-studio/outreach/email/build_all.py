"""Builds the day-0 pitch email for every company with a private page: <out>/<key>.html, .txt, .json (subject).
Words come from outreach/<key>.md (section 1: subject + text, in the company's language); the private page link comes from
the scratchpad's cut/page_tokens.json (never stored in the repo), the film thumbnails from <page>/email/<film>.jpg
(email_thumbs.sh on the server: poster + gold play button) and the film list from films.jsonl (film file, duration).
Foton keeps its hand-written version (foton.py content, approved on 2026-11-26).
usage: python3 build_all.py <films.jsonl> <out_dir>
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import bd_email as M
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUTR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pitch.bigdogma.tech"
TOK = json.load(open(f"{S}/cut/page_tokens.json"))
FILMS = {}
for l in open(sys.argv[1]):
    d = json.loads(l); FILMS.update(d)
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)

L = {  # per language: button, note, opt-out, preheader, signature role, duration unit, voice
 "mk": dict(cta="Погледнете ги филмовите", note="Приватна страница само за {n}: филмовите, сите AI кадри, предлог-распоред за објава и понуда во PDF.",
            optout="Оваа порака е испратена само до {n}. Ако не сакате повеќе пораки од нас, одговорете со „не, благодарам“ и нема повторно да ви пишеме.",
            pre="Два кратки AI филма направени само за {n}, без снимање. Приватна страница, 2 минути.", role="Основач и креативен директор",
            sec="сек.", voice="глас на македонски"),
 "sr": dict(cta="Pogledajte filmove", note="Privatna stranica samo za {n}: filmovi, svi AI kadrovi, predlog rasporeda objava i ponuda u PDF-u.",
            optout="Ova poruka je poslata samo kompaniji {n}. Ako ne želite više poruka od nas, odgovorite sa „ne, hvala“ i nećemo vam ponovo pisati.",
            pre="Dva kratka AI filma napravljena samo za {n}, bez snimanja. Privatna stranica, 2 minuta.", role="Osnivač i kreativni direktor",
            sec="sek.", voice="glas na srpskom"),
 "sq": dict(cta="Shikoni filmat", note="Faqe private vetëm për {n}: filmat, të gjitha pamjet AI, një propozim për kalendarin e publikimeve dhe oferta në PDF.",
            optout="Ky mesazh u dërgua vetëm për {n}. Nëse nuk dëshironi më mesazhe nga ne, përgjigjuni me „jo, faleminderit“ dhe nuk do t'ju shkruajmë më.",
            pre="Dy filma të shkurtër AI, të krijuar vetëm për {n}, pa xhirime. Faqe private, 2 minuta.", role="Themelues dhe drejtor kreativ",
            sec="sek.", voice="zë në shqip"),
}
SIGN = "Blagoj N."

def parse(md):
    t = open(md, encoding="utf-8").read()
    name = re.match(r"# (.+?) · outreach", t).group(1).strip()
    lang = re.search(r"Language: (\w+)", t).group(1)
    titles = [x.strip() for x in re.findall(r"\s*(.+?)\s*\([^)]*\)\s*(?:,|$)", re.search(r"- Films: (.+)", t).group(1))]   # "Title (33 сек.), Title, with comma (24 сек.)"
    sec1 = t.split("## 1.", 1)[1].split("## 2.", 1)[0]
    subject = re.search(r"\*\*[^*]+:\*\*\s*(.+)", sec1).group(1).strip()
    body = re.search(r"```\n(.*?)\n```", sec1, re.S).group(1)
    blocks = [b.strip() for b in body.split("\n\n") if b.strip()]
    greeting = blocks[0]; paras = []; closing = None
    for b in blocks[1:]:
        if "[PITCH_PAGE_LINK]" in b: continue                      # the button carries the link
        if "BIG DOGMA" in b and "\n" in b: closing = b.split("\n")[0]; break   # sign-off block
        paras.append(b)
    return dict(name=name, lang=lang, titles=titles, subject=subject, greeting=greeting, paras=paras, closing=closing)

def match_films(key, titles):
    tok = TOK[key]; got = sorted(FILMS[tok], key=lambda x: x[1])         # shortest first
    if key.startswith("13_"):                                             # Telekom: match by name
        order = {"magenta": 0, "network": 1}
        got = sorted(FILMS[tok], key=lambda x: min(v for k, v in order.items() if k in x[0]))
        return list(zip(titles, got))
    # the outreach texts list the longer commercial first except Vincinni (family ad first): pair by length rank
    md_len = [int(x) for x in re.findall(r"\((\d+)", open(f"{OUTR}/{key}.md", encoding="utf-8").read().split("- Films:", 1)[1].split("\n", 1)[0])]
    rank = sorted(range(len(titles)), key=lambda i: md_len[i])
    pairs = [None] * len(titles)
    for r, i in enumerate(rank): pairs[i] = (titles[i], got[r])
    return pairs

for key, tok in TOK.items():
    if key.startswith("05_"): continue                                    # Foton: hand-written content (email/foton_test.py)
    c = parse(f"{OUTR}/{key}.md"); x = L[c["lang"]]; page = f"{BASE}/{tok}/"; n = c["name"]
    films = [dict(title=t, meta=f'{round(d)} {x["sec"]} · {x["voice"]}', img=f"{page}email/{f}.jpg", href=page + "#films")
             for t, (f, d) in match_films(key, c["titles"])]
    content = dict(lang=c["lang"], subject=c["subject"], preheader=x["pre"].format(n=n), greeting=c["greeting"], paras=c["paras"], films=films,
                   cta=dict(label=x["cta"], href=page), note=x["note"].format(n=n), sign=dict(name=SIGN, role=x["role"]),
                   closing=c["closing"], optout=x["optout"].format(n=n), video_word="video" if c["lang"] != "mk" else "видео")
    h, t = M.render(content)
    open(f"{OUT}/{key}.html", "w").write(h); open(f"{OUT}/{key}.txt", "w").write(t)
    json.dump({"subject": c["subject"], "lang": c["lang"], "name": n, "films": [f["title"] for f in films]}, open(f"{OUT}/{key}.json", "w"), ensure_ascii=False)
    print(key, c["lang"], "|", c["subject"][:60], "|", [f["title"] + " = " + f["img"].rsplit("/", 1)[1] for f in films])
