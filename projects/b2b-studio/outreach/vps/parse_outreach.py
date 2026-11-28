# Turns the private outreach files (real page links) into emails/<cid>.json for outreach.py: steps 1 (day 0), 4 (day 4), 5 (day 10).
import re, json, sys, os, glob
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
for p in sorted(glob.glob(f"{src}/[0-9][0-9]_*.md")):
    cid = os.path.basename(p)[:-3]; t = open(p, encoding="utf-8").read(); E = {}
    for blk in re.split(r"\n(?=## )", t):
        m = re.match(r"## (\d)\.", blk)
        if not m or m.group(1) not in ("1", "4", "5"): continue
        subj = re.search(r"\*\*[^*]+:\*\* (.+)", blk).group(1).strip(); body = re.search(r"```\n(.*?)\n```", blk, re.S).group(1).strip()
        assert "pitch.bigdogma.tech/" in body or m.group(1) != "1", (cid, "no link")
        E[m.group(1)] = {"subject": subj, "body": body + "\n"}
    assert set(E) == {"1", "4", "5"}, (cid, list(E)); json.dump(E, open(f"{out}/{cid}.json", "w"), ensure_ascii=False, indent=1)
    print("OK", cid)
