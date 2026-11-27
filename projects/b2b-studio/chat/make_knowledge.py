# Builds chat/knowledge.md, the studio facts the chat avatar may use, from the site's own texts (launch/site_work/tx_src.json, written by
# gen_site.py), so prices, packages, process and FAQ in the chat always match bigdogma.tech. English only; the avatar answers in the
# visitor's language.   python3 make_knowledge.py
import json, os, re, html
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
src = json.load(open(f"{S}/launch/site_work/tx_src.json", encoding="utf-8"))
brand = json.load(open(f"{S}/brand/brand.json", encoding="utf-8"))
def en(k): return re.sub(r"<[^>]+>", "", html.unescape(src[k][1])).strip() if k in src else ""
def block(title, keys): return f"## {title}\n" + "\n".join(f"- {en(k)}" for k in keys if en(k)) + "\n"
out = ["# BIG DOGMA - studio facts for the chat assistant\n",
       f"Studio: BIG DOGMA, AI video studio in Skopje, North Macedonia. Website: bigdogma.tech. Contact email: {brand.get('email', '')}.",
       "Every film is generated with AI (no camera, no crew, no location) and carries an AI disclosure.\n",
       block("What we say about ourselves", ["meta.desc", "hero.h1", "hero.sub", "reel.p", "work.p", "cf.p", "ai.note"]),
       block("How it works", ["how.p", "s1.h", "s1.p", "s2.h", "s2.p", "s3.h", "s3.p", "s4.h", "s4.p"]),
       "## Prices (only these; every quote is confirmed by the team)\n" +
       "\n".join(f"- {en(f'p{i}.n')}: {en(f'p{i}.a')} {en(f'p{i}.per')} - " + "; ".join(en(f"p{i}.l{j}") for j in range(1, 5) if en(f"p{i}.l{j}")) for i in (1, 2, 3)) +
       f"\n- {en('price.vat')}\n- {en('price.terms')}\n",
       "## Ready-made packages\n" + en("bund.p") + "\n" +
       "\n".join(f"- {en(f'b{i}.n')}: {en(f'b{i}.a')} {en(f'b{i}.u')} - " + "; ".join(en(f"b{i}.l{j}") for j in range(1, 4) if en(f"b{i}.l{j}")) for i in range(1, 7) if en(f"b{i}.n")) + "\n",
       "## FAQ\n" + "\n".join(f"Q: {en(f'q{i}')}\nA: {en(f'a{i}')}" for i in range(1, 10) if en(f"q{i}")) + "\n",
       "## Industries with demo films on the site\n" + ", ".join(sorted({en(k) for k in src if k.startswith("cc.") and k != "cc.bd"})) + "\n",
       "## Film types\nCommercials (about 25-40 s), story films, explainers, before/after transformations, 9:16 social videos, logo films.\n",
       "## Contact\n" + f"- Email: {brand.get('email', '')}\n- Contact form on bigdogma.tech (section Contact).\n- {en('c.where')}: {en('c.where.v')}\n"]
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.md"); open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, len("\n".join(out)), "chars")
