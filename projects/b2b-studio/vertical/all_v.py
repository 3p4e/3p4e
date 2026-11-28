# Native 9:16 versions of the 22 films on the 11 company pages (owner, 2026-11-26: "go ahead with verticals for all companies").
# Same method as the Foton pilot (foton_v.py): Gemini 3 Pro Image re-shoots each approved 16:9 keyframe as a portrait photograph, LTX-2.5
# renders it at 704x1280 with the shot's own prompt, seed, strength and length, and cut_v_all.py lays it on the 16:9 film's timeline.
#   python3 all_v.py films              -> the 22 films, their shots and timing rules (also imported by cut_v_all.py)
#   python3 all_v.py kf [ids...]        -> vertical/kf_all/<shot>.jpg (704x1280; kept on disk: paid generation)
#   python3 all_v.py sheet [film...]    -> QC sheets, 16:9 keyframe next to the vertical one, in $VW/sheets
#   python3 all_v.py jobs               -> vertical/jobs_all.json (99 jobs, ids v_<shot>)
#   python3 all_v.py bundle             -> $VW/vbundle.tgz for the Vast runner (jobs.json + kf/*.png)
import sys, os, json, base64, io, time, urllib.request, urllib.error, subprocess, tarfile
from concurrent.futures import ThreadPoolExecutor
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; TR = f"{S}/vo/trim"
KF = f"{S}/vertical/kf_all"; VW = os.environ.get("VW", "/dev/shm/vall")   # working files live in RAM (the session disk is nearly full)
JOB_DIRS = ("cb5", "cb6", "cb7", "cb10", "cb2", "cb9")
ZLOGO, VLOGO = f"{S}/qc/zlogo.png", f"{S}/qc/vlogo.png"
PAGES = {"01_zito_marketi_MK": ["zito_commercial", "zito_opening_film"], "02_alkaloid_MK": ["alkaloid_commercial", "alkaloid_employer_film"],
         "03_replek_MK": ["replek_commercial", "replek_export_film"], "04_vincinni_MK": ["vincinni_factory_ad", "vincinni_family_ad"],
         "06_beograd_na_vodi_RS": ["bw_commercial", "bw_riverside_film"], "07_millennium_team_RS": ["millennium_capability_film", "millennium_commercial"],
         "08_nelt_RS": ["nelt_commercial", "nelt_logistics_film"], "09_gener2_AL": ["gener2_builder_film", "gener2_commercial"],
         "10_concord_AL": ["concord_commercial", "concord_offplan_film"], "11_viva_fresh_XK": ["viva_commercial", "viva_expansion_film"],
         "12_speeex_XK": ["speeex_commercial", "speeex_recruitment_film"]}

def films():
    """Each film exactly as cut.py / cut2.py / zito_cut.py cut its 16:9 version: shots (clip id, voice-over take), card, crossfade, rule."""
    sys.path.insert(0, f"{S}/vo"); cwd = os.getcwd(); os.chdir(f"{S}/vo")
    from vo_lines import VO; from batch2 import CUTS
    os.chdir(cwd)
    F = {}
    COMM = {"bw": ("Beograd na vodi", "Belgrade Waterfront"), "gener2": ("Gener 2", "GENER 2"), "concord": ("Concord Investment", "CONCORD"),
            "viva": ("Viva Fresh", "VIVA FRESH"), "alkaloid": ("Алкалоид", "АЛКАЛОИД"), "replek": ("Реплек", "РЕПЛЕК"),
            "millennium": ("Millennium Team", "MILLENNIUM TEAM"), "nelt": ("Nelt Group", "NELT"), "speeex": ("SPEEEX", "SPEEEX")}
    for cid, (company, title) in COMM.items():   # cut.py
        lang, _, lines = VO[cid]
        F[f"{cid}_commercial"] = dict(lang=lang, company=company, title=title, tagline=lines[-1], logo=None, xf=0.4, rule="cut", trim=None,
                                      shots=[(f"comm_{cid}_{i}", f"{TR}/{cid}_{i}.wav") for i in range(1, 6)])
    F["zito_commercial"] = dict(lang="mk", company="Жито маркети", title="Жито маркети", tagline="Свежината започнува тука.", logo=ZLOGO, xf=0.4,
                                rule="cut", trim=None, shots=[(f"comm_kam_{i}", f"{TR}/zito_{i}.wav") for i in range(1, 6)])   # zito_cut.py
    F["vincinni_family_ad"] = dict(lang="mk", company="Макпрогрес / Vincinni", title="Vincinni", tagline="Секогаш по твој вкус.", logo=VLOGO, xf=0.4,
                                   rule="cut", trim=None, shots=[(f"vc1_{i}", f"{TR}/vincinni_vc1_{i}.wav") for i in (1, 2, 4, 5)])
    F["vincinni_factory_ad"] = dict(lang="mk", company="Макпрогрес / Vincinni", title="Vincinni", tagline="It's Good. It's Vincinni.", logo=VLOGO, xf=0.4,
                                    rule="cut", trim=None, shots=[(f"vc2_{i}", f"{TR}/vincinni_vc2_{i}.wav") for i in range(1, 6)])
    want = {f for fs in PAGES.values() for f in fs}
    for c in CUTS:   # cut2.py
        name, lang, _, company, title, tagline, shots = c[:7]; trim = c[8] if len(c) > 8 else None
        if name not in want or name in F: continue
        li, sh = 0, []
        for cid, line in shots:
            vo = None
            if line:
                li += 1; vo = f"{TR}/b2_{name}_{li}.wav"; vo = vo if os.path.exists(vo) else None
            sh.append((cid, vo))
        F[name] = dict(lang=lang, company=company, title=title, tagline=tagline, logo=None, xf=0.35, rule="cut2", trim=trim, shots=sh)
    F["zito_opening_film"] = dict(lang="mk", company="Жито маркети", title="Жито маркети", tagline="Секогаш блиску до вас.", logo=ZLOGO, xf=0.35,
                                  rule="cut2", trim=None, shots=[(cid, f"{TR}/b2_zito_opening_film_{i + 1}.wav") for i, cid in
                                                                 enumerate(["prop_kam_skopje_s3", "prop_kam_skopje_s1", "prop_kam_skopje_s4", "prop_kam_skopje_s2"])])
    assert set(F) == want, sorted(want ^ set(F))
    return F

def shot_ids(F=None):
    F = F or films(); seen = []
    for k in sorted(F):
        for cid, _ in F[k]["shots"]:
            if cid not in seen: seen.append(cid)
    return seen

def load_jobs(ids):
    J = {}
    for d in JOB_DIRS:
        p = f"{S}/{d}/jobs.json"
        if not os.path.exists(p): continue
        L = json.load(open(p)); L = L if isinstance(L, list) else L.get("jobs", [])
        for j in L:
            if j.get("id") in ids and j["id"] not in J: J[j["id"]] = dict(j, _dir=d)
    miss = [i for i in ids if i not in J]; assert not miss, miss
    return J

def kf_src(j):
    for d in (j["_dir"],) + JOB_DIRS:
        p = f"{S}/{d}/kf/{j['start']}"
        if os.path.exists(p): return p
    raise FileNotFoundError(j["start"])

PROMPT = ("Re-shoot this exact scene as a tall portrait-orientation photograph (aspect ratio 9:16, taller than wide). Keep everything identical to "
          "the reference: the same people (faces, hair, age, clothes), the same products, packaging, buildings, rooms, vehicles, machines and every "
          "visible detail, the same place, time of day, light, weather, colours and photographic style. Do not paste or shrink the reference picture "
          "inside a larger canvas: render the whole scene again from a camera framed for portrait orientation, closer to the main subject, so it is "
          "large and fills most of the frame width, and the scene continues naturally above and below it (sky, ceiling, floor, ground, street, "
          "shelves) with no visible seams or edges. Keep the top eighth and the bottom fifth of the picture free of important detail. The picture is "
          "the photograph only: no device, no phone, no screen frame, no status bar, no icons, no buttons, no borders, no blur bars, no split screen, "
          "no added text, no new logos, no watermark. Photorealistic premium commercial photograph.")

def gem(sid, src):
    out = f"{KF}/{sid}.jpg"
    if os.path.exists(out): return True
    from PIL import Image
    KEY = open(f"{S}/.gemini_paid").read().strip()
    im = Image.open(src).convert("RGB"); b = io.BytesIO(); im.save(b, "PNG")
    body = {"contents": [{"parts": [{"text": PROMPT}, {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(b.getvalue()).decode()}}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY}), timeout=300).read())
            d = [p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p][0]
            g = Image.open(io.BytesIO(base64.b64decode(d["inlineData"]["data"]))).convert("RGB")
            s = max(704 / g.width, 1280 / g.height); g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
            l, t = (g.width - 704) // 2, (g.height - 1280) // 2; g.crop((l, t, l + 704, t + 1280)).save(out, quality=95, subsampling=0)
            print("ok", sid, flush=True); return True
        except urllib.error.HTTPError as e:
            msg = e.read()[:200].decode(errors="ignore"); print("ERR", sid, e.code, msg, flush=True)
            if e.code in (401, 402, 403): return False   # billing / key problem: retrying only spends time
            time.sleep(20)
        except Exception as e: print("ERR", sid, str(e)[:160], flush=True); time.sleep(20)
    return False

def sheet(F, names):
    from PIL import Image, ImageDraw
    os.makedirs(f"{VW}/sheets", exist_ok=True); J = load_jobs(shot_ids(F))
    for n in names:
        ids = [c for c, _ in F[n]["shots"]]; W1, H1, W2, H2 = 400, 220, 124, 220
        g = Image.new("RGB", (len(ids) * (W1 + W2 + 24), H1 + 22), (20, 20, 20)); d = ImageDraw.Draw(g)
        for i, sid in enumerate(ids):
            x = i * (W1 + W2 + 24); d.text((x + 4, 4), sid[-22:], fill=(240, 200, 80))
            g.paste(Image.open(kf_src(J[sid])).convert("RGB").resize((W1, H1)), (x, 22))
            if os.path.exists(f"{KF}/{sid}.jpg"): g.paste(Image.open(f"{KF}/{sid}.jpg").convert("RGB").resize((W2, H2)), (x + W1 + 4, 22))
        g.save(f"{VW}/sheets/{n}.jpg", quality=85); print("sheet", n, g.size)

if __name__ == "__main__":
    F = films(); ids = shot_ids(F); cmd = sys.argv[1]
    if cmd == "films":
        for k in sorted(F): print(k, F[k]["lang"], F[k]["rule"], F[k]["xf"], len(F[k]["shots"]), "logo" if F[k]["logo"] else "-", "|", F[k]["tagline"])
        print(len(F), "films", len(ids), "shots")
    elif cmd == "kf":
        os.makedirs(KF, exist_ok=True); J = load_jobs(ids); only = set(sys.argv[2:]) or set(ids)
        with ThreadPoolExecutor(4) as ex: res = list(ex.map(lambda i: gem(i, kf_src(J[i])), [i for i in ids if i in only]))
        print("KF_DONE", len([i for i in ids if os.path.exists(f"{KF}/{i}.jpg")]), "of", len(ids), "| failed now", res.count(False))
    elif cmd == "sheet": sheet(F, sys.argv[2:] or sorted(F))
    elif cmd == "jobs":
        J = load_jobs(ids)
        out = [dict(id="v_" + i, w=704, h=1280, frames=J[i]["frames"], seed=J[i]["seed"], strength=J[i].get("strength", 0.7), start=f"{i}.png",
                    prompt="Vertical 9:16 phone framing, the main subject large in frame. " + J[i]["prompt"]) for i in ids]
        json.dump(out, open(f"{S}/vertical/jobs_all.json", "w"), indent=1); print("jobs", len(out), "frames", sum(j["frames"] for j in out))
    elif cmd == "bundle":   # PNG keyframes as the runner expects, built in RAM
        from PIL import Image
        jobs = json.load(open(f"{S}/vertical/jobs_all.json")); miss = [j["id"] for j in jobs if not os.path.exists(f"{KF}/{j['id'][2:]}.jpg")]
        assert not miss, f"missing keyframes: {miss}"
        os.makedirs(f"{VW}/vb/kf", exist_ok=True)
        for j in jobs: Image.open(f"{KF}/{j['id'][2:]}.jpg").save(f"{VW}/vb/kf/{j['start']}")
        json.dump({"negative": "watermark, text, logo, letterbox, black bars, blurred borders, phone interface", "steps": 8, "cfg": 1.0, "strength": 0.75,
                   "fps": 24, "jobs": jobs}, open(f"{VW}/vb/jobs.json", "w"), indent=1)
        with tarfile.open(f"{VW}/vbundle.tgz", "w:gz") as t: t.add(f"{VW}/vb", arcname=".")
        print("bundle", len(jobs), os.path.getsize(f"{VW}/vbundle.tgz") // 1024, "KB")
