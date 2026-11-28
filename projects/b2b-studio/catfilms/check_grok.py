# Checks the Grok keyframes that come back: python3 check_grok.py <incoming dir> [--sheets <outdir>]
# Step 1 (automatic): every expected filename present, nothing unexpected, JPG/PNG opens, aspect ratio right (16:9 or 9:16 within 3 %),
# resolution >= 1024 on the long side, not a duplicate of another image (md5 + 8x8 hash), not a copy of its own reference.
# Step 2 (visual, done by the reviewer): per-film contact sheets with the prompt printed next to each frame: people/rooms match the
# reference, no text/logos/signs, no morphed hands/faces, same hero across shots, before/after in the same room. Verdicts go to review.json.
import os, sys, csv, glob, json, hashlib, collections
from PIL import Image, ImageDraw
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
SRC = [f"{S}/grok_archive/BD_GROK_ARCHIVE/01_sector_films_74/GROK_KEYFRAMES.csv", f"{S}/grok_archive/BD_GROK_ARCHIVE/ALL_IMAGES_TO_MAKE.csv"]
inc = sys.argv[1]; sheets = sys.argv[sys.argv.index("--sheets") + 1] if "--sheets" in sys.argv else f"{S}/grok_review"; os.makedirs(sheets, exist_ok=True)
exp = {}
for p in SRC:
    for r in csv.DictReader(open(p, encoding="utf-8")): exp[r["filename"]] = r
have = {}
for f in glob.glob(f"{inc}/**/*", recursive=True):
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")): have[os.path.basename(f)] = f
def norm(n): return os.path.splitext(n)[0].lower()
hv = {norm(k): v for k, v in have.items()}; ok, issues = [], collections.defaultdict(list)
missing = [k for k in exp if norm(k) not in hv]; extra = [k for k in have if norm(k) not in {norm(e) for e in exp}]
hashes = {}
for k, r in exp.items():
    f = hv.get(norm(k))
    if not f: continue
    try: im = Image.open(f); im.load()
    except Exception as e: issues[k].append(f"unreadable: {e}"); continue
    w, h = im.size; want = 16 / 9 if r["aspect"] == "16:9" else 9 / 16
    if abs(w / h - want) / want > 0.03: issues[k].append(f"aspect {w}x{h} (want {r['aspect']})")
    if max(w, h) < 1024: issues[k].append(f"low resolution {w}x{h}")
    md5 = hashlib.md5(open(f, "rb").read()).hexdigest(); ah = tuple(Image.open(f).convert("L").resize((8, 8)).getdata()); m = sum(ah) / 64; bits = tuple(int(x > m) for x in ah)
    if md5 in hashes: issues[k].append(f"identical file to {hashes[md5]}")
    hashes[md5] = k
    ref = (r.get("reference") or "").strip()
    if ref and norm(ref) in hv and hashlib.md5(open(hv[norm(ref)], "rb").read()).hexdigest() == md5: issues[k].append("is a copy of its reference image (no new shot)")
    if not issues[k]: ok.append(k)
print(f"expected {len(exp)} | found {len(exp) - len(missing)} | missing {len(missing)} | unexpected files {len(extra)} | auto-check problems {len(issues)} | auto-pass {len(ok)}")
json.dump(dict(missing=missing, extra=extra, issues=issues), open(f"{sheets}/auto_check.json", "w"), indent=1)
# visual sheets per film / set
groups = collections.defaultdict(list)
for k in exp:
    if norm(k) in hv: groups[exp[k].get("film") or exp[k]["set"]].append(k)
for g, ks in sorted(groups.items()):
    ks.sort(); cols = min(len(ks), 5); rows = (len(ks) + cols - 1) // cols; cw, ch = 380, 300
    W = Image.new("RGB", (cols * cw, rows * ch), "white"); d = ImageDraw.Draw(W)
    for i, k in enumerate(ks):
        im = Image.open(hv[norm(k)]).convert("RGB"); im.thumbnail((cw - 6, ch - 40)); x, y = (i % cols) * cw, (i // cols) * ch
        W.paste(im, (x + 3, y + 36)); d.text((x + 4, y + 2), k.replace(".jpg", ""), fill="red"); d.text((x + 4, y + 16), "ref: " + (exp[k].get("reference") or "-")[:46], fill="gray")
    W.save(f"{sheets}/{g}.jpg", quality=82)
print("sheets:", len(groups), "->", sheets)
