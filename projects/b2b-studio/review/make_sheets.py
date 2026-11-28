# Contact sheets for the ruthless video review: A = studio site videos (6 frames each, 6 films per sheet), B = company-page films (from the live pages),
# C = company AI shots (one poster frame each, 30 per grid). Output in /dev/shm/review, manifest in the scratchpad (review/manifest.json).
import os, re, sys, json, glob, subprocess, concurrent.futures as cf, urllib.request, html
from PIL import Image, ImageDraw
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; SITE = f"{S}/launch/site"; OUT = "/dev/shm/review"; os.makedirs(OUT, exist_ok=True); os.makedirs(f"{S}/review", exist_ok=True)
def dur(src): 
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    try: return float(r)
    except: return 0.0
def strip(src, name):
    d = dur(src)
    if d <= 0: return None
    p = f"{OUT}/tmp_{abs(hash(name))}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"fps=6/{d:.2f},scale=300:-2,tile=6x1", "-frames:v", "1", p], capture_output=True)
    return (name, p, round(d, 1)) if os.path.exists(p) else None
def sheets(items, prefix, per):
    man = []
    for k in range(0, len(items), per):
        grp = [x for x in items[k:k + per] if x]
        if not grp: continue
        ims = [Image.open(p) for _, p, _ in grp]; W = max(i.width for i in ims); H = sum(i.height + 16 for i in ims)
        o = Image.new("RGB", (W, H), "black"); d = ImageDraw.Draw(o); y = 0
        for (n, _, dd), i in zip(grp, ims): d.text((4, y + 1), f"{n}  ({dd}s)", fill="yellow"); o.paste(i, (0, y + 16)); y += i.height + 16
        fn = f"{prefix}_{k // per:02d}.jpg"; o.save(f"{OUT}/{fn}", quality=80); man.append({"sheet": fn, "items": [n for n, _, _ in grp]})
        for _, p, _ in grp: os.remove(p)
    return man
mode = sys.argv[1]; man = []
if mode == "A":
    files = []
    for d in ("media/intro", "media/bd", "logo_fx/hdr", "films", "media"):
        for f in sorted(glob.glob(f"{SITE}/{d}/*.mp4")): files.append((f"{d}/{os.path.basename(f)}", f))
    seen = set(); files = [x for x in files if not (x[0] in seen or seen.add(x[0]))]
    with cf.ThreadPoolExecutor(6) as ex: items = list(ex.map(lambda x: strip(x[1], x[0]), files))
    man = sheets(items, "A", 6)
elif mode == "B":
    toks = json.load(open(f"{S}/cut/page_tokens.json")); toks.update(json.load(open(f"{S}/cut/page_tokens_new.json")))
    files = []
    for key, tok in toks.items():
        try: h = urllib.request.urlopen(f"https://pitch.bigdogma.tech/{tok}/", timeout=40).read().decode()
        except Exception as e: print("skip", key, e); continue
        fg = re.search(r'<ul class="grid" id="fg">(.*?)</ul>', h, re.S)
        for m in re.finditer(r'data-play="([^"]+\.mp4)"(?:[^>]*data-v="([^"]+\.mp4)")?', fg.group(1) if fg else ""):
            for rel in (m.group(1), m.group(2)):
                if rel and not rel.startswith("http"): files.append((f"{key}/{rel}", f"https://pitch.bigdogma.tech/{tok}/{rel}"))
    seen = set(); files = [x for x in files if not (x[0] in seen or seen.add(x[0]))]
    with cf.ThreadPoolExecutor(6) as ex: items = list(ex.map(lambda x: strip(x[1], x[0]), files))
    man = sheets(items, "B", 6)
else:   # C: shot posters
    toks = json.load(open(f"{S}/cut/page_tokens.json")); n = 0
    for key, tok in toks.items():
        names = []
        for i in range(1, 40):
            u = f"https://pitch.bigdogma.tech/{tok}/x/c{i:02d}.jpg"
            try: b = urllib.request.urlopen(u, timeout=20).read()
            except Exception: continue
            p = f"{OUT}/sh_{key}_{i:02d}.jpg"; open(p, "wb").write(b); names.append((f"c{i:02d}", p))
        if not names: continue
        cols = 6; rows = (len(names) + cols - 1) // cols; o = Image.new("RGB", (cols * 320, rows * 190), "black"); d = ImageDraw.Draw(o)
        for j, (nm, p) in enumerate(names):
            im = Image.open(p).convert("RGB"); im.thumbnail((320, 180)); x, y = (j % cols) * 320, (j // cols) * 190; o.paste(im, (x, y + 10)); d.text((x + 2, y), nm, fill="yellow"); os.remove(p)
        fn = f"C_{key}.jpg"; o.save(f"{OUT}/{fn}", quality=78); man.append({"sheet": fn, "items": [nm for nm, _ in names], "company": key})
json.dump(man, open(f"{S}/review/manifest_{mode}.json", "w"), indent=0); print(mode, len(man), "sheets", sum(len(m["items"]) for m in man), "items")
