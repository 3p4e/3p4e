# Makedonski Telekom pitch (owner, 2026-11-26): two concept films in Macedonian, 16:9 + native 9:16.
#  A "Magenta 1" (Kore): one family, connected across Macedonia (Magenta 1 Unlimited bundle: mobile, fibre, MagentaTV).
#  B "Мрежата" (Charon): the people who build the network (5G masts, fibre, rural farming and telemedicine).
# Research basis: Deutsche Telekom company profile (5G ~97 % population, fibre ~60 % of households), MagentaTV launch 2024, Magenta 1
# Unlimited bundles, 2025 #MakeSpace purpose campaign (warm, human tone). No Telekom logo or "T" is generated (AI garbles trademarks);
# magenta (#E20074) appears only as an accent in clothes, light and objects. Client logo goes on the end card only, by hand, if wanted.
#   python3 tk.py kf      -> telekom/kf/<id>.png (16:9 1280x704) + telekom/kfv/<id>.png (9:16 704x1280)
#   python3 tk.py jobs    -> telekom/jobs.json (16:9 + 9:16 LTX jobs)
import sys, os, json, base64, io, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; D = f"{S}/telekom"
for d in ("kf", "kfv", "kf_full"): os.makedirs(f"{D}/{d}", exist_ok=True)
STYLE = (" Photorealistic premium telecom commercial photograph, natural cinematic light, real Macedonian people and places, a subtle magenta "
         "(#E20074) accent in the scene (clothing, light or an object), no logos, no brand marks, no text, no watermark.")
LTX = " Photorealistic telecom commercial cinematography, natural light, warm human mood, crisp detail, calm premium pacing."
FILMS = [
 dict(id="telekom_magenta1", voice="Kore", title="Magenta 1 Unlimited", tagline="Поврзани со она што е важно.", shots=[
  dict(kf="Sunrise over Skopje seen from Vodno: the city waking up, the Vardar river shining, soft morning mist; in the foreground a young woman on a terrace in a magenta scarf holds a smartphone and looks over the city.",
       ltx="Slow push-in past the woman toward the city. Sunlight spreads across the rooftops and the river, the mist lifts and she smiles at her phone. The city in morning light holds on the final frame.",
       vo="Секое утро, цела Македонија се буди поврзана."),
  dict(kf="A cosy village kitchen in the Mavrovo region: an elderly Macedonian grandmother at a wooden table laughing during a video call on a tablet, homemade bread and jars of red peppers, warm window light, a magenta knitted shawl on her shoulders.",
       ltx="Gentle push-in. The grandmother laughs and waves at the tablet, steam rises from her tea and the window light warms. Her happy face holds on the final frame.",
       vo="Баба е на еден допир од внуците."),
  dict(kf="Evening on the Ohrid lakeside promenade: friends in their twenties cheering at a football match streaming on a smartphone held up between them, the lake and the old town lights behind, one of them in a magenta jersey.",
       ltx="Slow drift around the group. The friends jump and cheer at a goal on the phone, arms in the air, the lake lights shimmer behind them. Their celebration holds on the final frame.",
       vo="Натпреварот е таму каде што сте вие."),
  dict(kf="A modern Skopje apartment living room at night, the whole family online at once: a teenage daughter gaming, the father in a laptop video meeting, the mother watching a series on a big TV, a small boy with a tablet, warm lamps, a white fibre router with a soft magenta light on a shelf.",
       ltx="Slow lateral dolly across the room. The game, the call and the series all play smoothly, the boy laughs at his tablet. The whole family in the warm room holds on the final frame.",
       vo="Брз оптички интернет за целиот дом, истовремено."),
  dict(kf="Night view of Skopje from an apartment balcony: three generations of one family together looking at the city lights, the lit cross on Vodno in the distance, a soft magenta glow along the horizon.",
       ltx="Slow pull-back from the family to the wide night skyline. City lights twinkle and a soft magenta glow rises along the horizon. The family against the lit city holds on the final frame.",
       vo="Magenta 1 Unlimited. Поврзани со она што е важно.")]),
 dict(id="telekom_network", voice="Charon", title="МАКЕДОНСКИ ТЕЛЕКОМ", tagline="Ја градиме мрежата на Македонија.", shots=[
  dict(kf="A telecom technician in a white hard hat and climbing harness on a mobile mast on a mountain ridge above Lake Ohrid at sunrise, antenna panels on the mast, magenta details on his work jacket, the vast lake below.",
       ltx="Slow aerial orbit around the mast. The technician climbs and tightens a bolt on an antenna as the sun rises over the lake. The mast against the sunrise holds on the final frame.",
       vo="Од Охрид до Делчево, мрежата расте секој ден."),
  dict(kf="Close-up inside a service van: the gloved hands of a technician splicing a fibre-optic cable with a fusion splicer, thin glass fibres glowing with light, a magenta tool case, shallow depth of field.",
       ltx="Macro push-in. The fibres align, the splicer fuses them and light runs along the glass strand. The glowing fibre holds on the final frame.",
       vo="Оптика, до вашата врата."),
  dict(kf="A young farmer in a greenhouse in the Strumica valley in the morning, checking irrigation and soil data on a smartphone between rows of tomato plants, sunlight through the plastic roof, a magenta cap.",
       ltx="Slow push-in. The farmer taps the phone, sprinklers switch on along the rows and he nods. The farmer in the green rows holds on the final frame.",
       vo="Земјоделецот ја следи нивата од телефон."),
  dict(kf="A small village health clinic in eastern Macedonia: a doctor in a white coat on a video consultation with a specialist in a city hospital on a large screen, an elderly patient seated beside him, calm daylight, a magenta folder on the desk.",
       ltx="Gentle push-in. The specialist on screen explains, the doctor nods and the patient smiles with relief. The three of them in the bright room hold on the final frame.",
       vo="Специјалистот е блиску, и кога е далеку."),
  dict(kf="Night aerial over the mountains and valleys of North Macedonia: towns and villages glowing, thin lines of light connecting them along the roads and ridges like a network, a soft magenta tint in the sky.",
       ltx="Slow high aerial glide forward. Lines of light connect town after town across the valleys and the sky deepens. The connected, glowing country holds on the final frame.",
       vo="Македонски Телеком. Ја градиме мрежата на Македонија.")]),
]
def shots():
    for f in FILMS:
        for i, sh in enumerate(f["shots"], 1): yield f, i, f"{f['id']}_{i}", sh

def gem(out, prompt, aspect, size, src=None):
    if os.path.exists(out): return
    KEY = open(f"{S}/.gemini_paid").read().strip(); parts = [{"text": prompt}]
    if src:
        b = io.BytesIO(); Image.open(src).convert("RGB").save(b, "PNG"); parts.append({"inline_data": {"mime_type": "image/png", "data": base64.b64encode(b.getvalue()).decode()}})
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    W, H = size
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={KEY}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=300).read())
            d = [p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p][0]
            g = Image.open(io.BytesIO(base64.b64decode(d["inlineData"]["data"]))).convert("RGB"); g.save(f"{D}/kf_full/{os.path.basename(os.path.dirname(out))}_{os.path.basename(out)}")
            s = max(W / g.width, H / g.height); g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
            l, t = (g.width - W) // 2, (g.height - H) // 2; g.crop((l, t, l + W, t + H)).save(out); print("ok", out[len(D) + 1:], flush=True); return
        except urllib.error.HTTPError as e: print("ERR", out, e.code, e.read()[:200].decode(errors="ignore"), flush=True); time.sleep(20)
        except Exception as e: print("ERR", out, str(e)[:160], flush=True); time.sleep(20)

if __name__ == "__main__":
    if sys.argv[1] == "kf":
        with ThreadPoolExecutor(5) as ex:
            list(ex.map(lambda x: gem(f"{D}/kf/{x[2]}.png", x[3]["kf"] + STYLE + " Wide 16:9 frame.", "16:9", (1280, 704)), list(shots())))
        sys.path.insert(0, "/home/user/3p4e/projects/b2b-studio/vertical"); from foton_v import PROMPT as VPROMPT
        VP = VPROMPT.replace(" Photorealistic premium automotive commercial photograph.", " Photorealistic premium telecom commercial photograph.").replace(
             "the same vehicle (model, body colour, grille, badges, wheels and every detail), ", "")
        with ThreadPoolExecutor(5) as ex:
            list(ex.map(lambda x: gem(f"{D}/kfv/{x[2]}.png", VP, "9:16", (704, 1280), f"{D}/kf/{x[2]}.png"), list(shots())))
        print("KF_DONE", len(os.listdir(f"{D}/kf")), len(os.listdir(f"{D}/kfv")))
    elif sys.argv[1] == "jobs":
        J = []
        for f, i, sid, sh in shots():
            seed = 52000 + len(J) * 37
            J.append(dict(id=sid, w=1280, h=704, frames=121, seed=seed, strength=0.7, start=f"{sid}.png", prompt=sh["ltx"] + LTX))
            J.append(dict(id="v_" + sid, w=704, h=1280, frames=121, seed=seed, strength=0.7, start=f"v_{sid}.png", prompt=sh["ltx"] + " Vertical 9:16 phone framing." + LTX))
        json.dump(J, open(f"{D}/jobs.json", "w"), indent=1); print("jobs", len(J))
