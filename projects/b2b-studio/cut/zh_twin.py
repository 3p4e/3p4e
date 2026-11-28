# Chinese twin for a live pitch page (owner 2026-11-28: every Chinese client page is ONE page, English by default, with an EN | 中文 switch).
# For each token: fetch the live index.html, translate its visible text and labels into Simplified Chinese (OpenAI, cached),
# write zh.html next to it, add the switch to both and a ?lang=zh redirect to the English page, then upload both into the same folder
# (the old index.html is backed up on the server first, so links already sent keep working).
#   python3 zh_twin.py <token> [<token> ...]        (OPENAI_API_KEY in the environment; tokens are never stored in the repo)
import os, sys, re, json, html, urllib.request, subprocess, requests
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
CACHE = f"{S}/zh_twin_cache.json"; W = "/dev/shm/zh_twin"; os.makedirs(W, exist_ok=True)
C = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
KEEP = ("BIG DOGMA", "AI STUDIO", "bigdogma.tech", "inf.unit@bigdogma.tech")
SW = ('<span class="lsw" style="display:inline-flex;gap:8px;align-items:center;white-space:nowrap;flex:none;margin-right:12px;'
      'font:600 13px/1 Inter,system-ui,sans-serif"><b style="color:var(--ac,#f2c14e)">{cur}</b><span style="opacity:.4">|</span>'
      '<a href="{href}" lang="{hl}" style="color:inherit;text-decoration:none">{other}</a></span>')
REDIR = "<script>if(/[?&]lang=zh/.test(location.search))location.replace('zh.html'+location.hash)</script>"
LAT = re.compile(r"[A-Za-z]{2,}")

def strip_switch(h):
    h = re.sub(r'<span class="lsw".*?</a></span>', "", h, flags=re.S)
    return h.replace(REDIR, "")

def segments(h):
    """visible text nodes and translatable attributes, outside <script>/<style>"""
    out = set(); body = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S | re.I)
    for t in re.findall(r">([^<>]+)<", body):
        t = html.unescape(t).strip()
        if LAT.search(t) and t not in KEEP and not re.fullmatch(r"[\w.+-]+@[\w.-]+|https?://\S+|[#€$\d\s.,:/–-]+\w{0,3}", t): out.add(t)
    for a in re.findall(r'\b(?:data-t|alt|aria-label|title|content)="([^"]+)"', body):
        a = html.unescape(a).strip()
        if LAT.search(a) and " " in a and a not in KEEP and not a.startswith(("http", "width=", "light", "#")): out.add(a)
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    if t: out.add(html.unescape(t.group(1)).strip())
    return sorted(out)

def translate(items, company):
    todo = [x for x in items if x not in C]
    for i in range(0, len(todo), 80):
        chunk = todo[i:i + 80]
        prompt = ("Translate these strings of a private business web page from BIG DOGMA (an AI video studio in Skopje, North Macedonia) to " + company +
                  ", a Chinese company, into natural, professional Simplified Chinese for mainland business readers. Keep unchanged: BIG DOGMA, AI STUDIO | MK, "
                  "the company's own name in Latin letters, product/series names, prices, currencies, numbers, units, e-mail addresses, URLs, '16:9', '9:16', 'AI', "
                  "and the 'BD · ' prefix. 'I WANT IT!' becomes '我要！'. Keep any leading/trailing punctuation. Return ONLY a JSON object {original: translation}.\n\n"
                  + json.dumps(chunk, ensure_ascii=False))
        for a in range(4):
            try:
                r = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, timeout=300,
                                  json={"model": "gpt-5.4-mini", "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": prompt}]})
                r.raise_for_status(); got = json.loads(r.json()["choices"][0]["message"]["content"])
                C.update({k: v for k, v in got.items() if k in chunk and isinstance(v, str) and v.strip()}); break
            except Exception as e: print("retry", e, flush=True)
        json.dump(C, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

def apply(h, items):
    m = {x: C[x] for x in items if x in C}
    def tx(mo):
        raw = mo.group(1); s = html.unescape(raw); k = s.strip()
        return ">" + (s.replace(k, html.escape(m[k], quote=False)) if k in m else raw) + "<"
    def ta(mo):
        k = html.unescape(mo.group(2)).strip()
        return f'{mo.group(1)}="{html.escape(m[k]) if k in m else mo.group(2)}"'
    parts = re.split(r"(<(?:script|style)\b.*?</(?:script|style)>)", h, flags=re.S | re.I)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r">([^<>]+)<", tx, parts[i])
        parts[i] = re.sub(r'\b(data-t|alt|aria-label|title|content)="([^"]+)"', ta, parts[i])
    h = "".join(parts)
    h = re.sub(r"<title>(.*?)</title>", lambda mo: "<title>" + html.escape(m.get(html.unescape(mo.group(1)).strip(), html.unescape(mo.group(1)))) + "</title>", h, count=1, flags=re.S)
    return re.sub(r'<html lang="\w+"', '<html lang="zh"', h, count=1)

def twin(tok):
    en = strip_switch(urllib.request.urlopen(f"https://pitch.bigdogma.tech/{tok}/", timeout=60).read().decode("utf-8"))
    company = re.sub(r"^BIG DOGMA\s*×\s*", "", html.unescape(re.search(r"<title>(.*?)</title>", en, re.S).group(1))).strip()
    items = segments(en); translate(items, company); zh = apply(en, items)
    miss = [x for x in items if x not in C]
    en2 = en.replace('<a class="btn a want"', SW.format(cur="EN", other="中文", href="zh.html", hl="zh") + '<a class="btn a want"', 1).replace("</head>", REDIR + "</head>", 1)
    zh2 = zh.replace('<a class="btn a want"', SW.format(cur="中文", other="EN", href="./", hl="en") + '<a class="btn a want"', 1)
    assert 'class="lsw"' in en2 and 'class="lsw"' in zh2, "no nav button to attach the switch to"
    d = f"{W}/{tok}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8").write(en2); open(f"{d}/zh.html", "w", encoding="utf-8").write(zh2)
    return company, len(items), miss

if __name__ == "__main__":
    for tok in sys.argv[1:]:
        co, n, miss = twin(tok); print("built", tok, co, n, "strings", "missing:", len(miss), flush=True)
    # upload: back up the live index.html on the server, then write both files into the same token folder
    tar = f"{W}.tar"; subprocess.run(["tar", "cf", tar, "-C", W] + sys.argv[1:], check=True)
    for a in range(3):
        r = subprocess.run(["python3", f"{S}/rput_par.py", tar, "/opt/stacks/_upload", "zh_twin.tar"], cwd=S, capture_output=True, text=True)
        if "CHECKSUM MATCH" in r.stdout + r.stderr: break
    toks = " ".join(sys.argv[1:])
    cmd = ("cat /opt/stacks/_upload/zh_twin.tar | /opt/bigdogma_vps/bd.sh 'set -e; R=/opt/stacks/ai-studio-pitch/site; B=/opt/bd_work/zh_twin_backup; mkdir -p $B; "
           f"for t in {toks}; do mkdir -p $B/$t; [ -f $B/$t/index.html ] || cp $R/$t/index.html $B/$t/index.html; done; "
           "tar xf - -C $R; for t in " + toks + "; do chmod a+r $R/$t/index.html $R/$t/zh.html; done; echo uploaded'; rm -f /opt/stacks/_upload/zh_twin.tar")
    print(subprocess.run(["python3", f"{S}/rsh.py", cmd, "600"], cwd=S, capture_output=True, text=True).stdout.strip().splitlines()[-1:])
    for tok in sys.argv[1:]:
        codes = [urllib.request.urlopen(f"https://pitch.bigdogma.tech/{tok}/{p}", timeout=60).status for p in ("", "zh.html")]
        print("live", tok, codes, flush=True)
