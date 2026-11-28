# Native 9:16 versions of the Foton pitch films (owner, 2026-11-26: "a real mobile generated version, not the desktop video reused").
# 1) keyframes: Gemini 3 Pro Image recomposes each approved 16:9 keyframe as a vertical phone frame (same vehicle, place, light);
# 2) jobs: the same LTX-2.5 prompt, seed, strength and length as the 16:9 shot, rendered at 704x1280;
# 3) the vertical cut reuses the films' voice-over and music (cut_v.py).
#   python3 foton_v.py kf [ids...]   -> vertical/kf/<id>.png (704x1280) + full-size copy
#   python3 foton_v.py jobs          -> vertical/jobs_foton.json
import sys, os, json, base64, io, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; OUT = f"{S}/vertical"; os.makedirs(f"{OUT}/kf", exist_ok=True); os.makedirs(f"{OUT}/kf_full", exist_ok=True)
SHOWREEL = ["foton_A1_dawn-teaser", "foton_A2_drive-by", "foton_A3_studio-turn", "foton_B1_v9-character", "foton_B2_v7_fix", "foton_B3_g7_fix",
            "foton_C1_approach_fix", "foton_C2_climb", "foton_C3_summit", "foton_D1_cockpit-reveal", "foton_D2_details", "foton_D3_seats",
            "foton_E1_auman-tractor", "foton_E2_aumark_fix", "foton_E3_eme4-electric", "foton_E4_cargo-van",
            "foton_F1_showroom-arrival", "foton_F2_test-drive", "foton_F3_key-handover", "foton_G1_service-bay", "foton_G2_fleet-lineup"]
SPECS = [f"fs{i}" for i in range(1, 7)]

def load_jobs():
    J = {}
    for d in ("cb2", "cb9", "cb10"):
        L = json.load(open(f"{S}/{d}/jobs.json")); L = L if isinstance(L, list) else L["jobs"]
        for j in L: J[j["id"]] = dict(j, _dir=d)
    return J

def kf_src(j):
    for d in (j["_dir"], "cb2", "cb9"):
        p = f"{S}/{d}/kf/{j['start']}"
        if os.path.exists(p): return p
    raise FileNotFoundError(j["start"])

PROMPT = ("Re-shoot this exact scene as a tall portrait-orientation photograph (aspect ratio 9:16, taller than wide). Keep everything identical to "
          "the reference: the same vehicle (model, body colour, grille, badges, wheels and every detail), the same people, place, time of day, light, "
          "weather, colours and photographic style. Do not paste or shrink the reference picture inside a larger canvas: render the whole scene again "
          "from a camera framed for portrait orientation, closer to the subject, so the main subject is large and fills most of the frame width, and "
          "the scene continues naturally above and below it (sky, ground, road, studio floor or interior) with no visible seams or edges. Keep the top "
          "eighth and the bottom fifth of the picture free of important detail. The picture is the photograph only: no device, no phone, no screen, "
          "no status bar, no icons, no buttons, no borders, no blur bars, no split screen, no text, no new logos, no watermark. Photorealistic premium "
          "automotive commercial photograph.")

def gem(out, src):
    if os.path.exists(f"{OUT}/kf/{out}.png"): return
    KEY = open(f"{S}/.gemini_paid").read().strip()
    im = Image.open(src).convert("RGB"); b = io.BytesIO(); im.save(b, "PNG")
    body = {"contents": [{"parts": [{"text": PROMPT}, {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(b.getvalue()).decode()}}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={KEY}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=300).read())
            d = [p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p][0]
            g = Image.open(io.BytesIO(base64.b64decode(d["inlineData"]["data"]))).convert("RGB"); g.save(f"{OUT}/kf_full/{out}.png")
            s = max(704 / g.width, 1280 / g.height); g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
            l, t = (g.width - 704) // 2, (g.height - 1280) // 2; g.crop((l, t, l + 704, t + 1280)).save(f"{OUT}/kf/{out}.png")
            print("ok", out, flush=True); return
        except urllib.error.HTTPError as e: print("ERR", out, e.code, e.read()[:200].decode(errors="ignore"), flush=True); time.sleep(20)
        except Exception as e: print("ERR", out, str(e)[:160], flush=True); time.sleep(20)

if __name__ == "__main__":
    J = load_jobs(); ids = SHOWREEL + SPECS
    if sys.argv[1] == "kf":
        only = set(sys.argv[2:]) or set(ids)
        with ThreadPoolExecutor(4) as ex: list(ex.map(lambda i: gem(i, kf_src(J[i])), [i for i in ids if i in only]))
        print("KF_DONE", len([i for i in ids if os.path.exists(f"{OUT}/kf/{i}.png")]), "of", len(ids))
    elif sys.argv[1] == "jobs":
        out = [dict(id="v_" + i, w=704, h=1280, frames=J[i]["frames"], seed=J[i]["seed"], strength=J[i].get("strength", 0.7), start=f"{i}.png",
                    prompt=J[i]["prompt"].replace("Photorealistic", "Vertical 9:16 phone framing. Photorealistic", 1)) for i in ids]
        json.dump(out, open(f"{OUT}/jobs_foton.json", "w"), indent=1); print("jobs", len(out))
