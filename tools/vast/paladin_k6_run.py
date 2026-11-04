#!/usr/bin/env python3
"""Kandinsky 6.0 Lite (distilled) + VSR for The Paladin's Judgement.
MIT-licensed stack, EU-legal. Image-to-audio-video conditioning from gated keyframes.
"""
import os, sys, json, time, traceback
import torch

OUT    = os.environ.get("OUT_DIR", "/workspace/out")
IN     = os.environ.get("IN_DIR",  "/workspace/stills")
ONLY   = [s for s in os.environ.get("ONLY", "").split(",") if s]
W      = int(os.environ.get("GEN_W", 864))
H      = int(os.environ.get("GEN_H", 480))
FRAMES = int(os.environ.get("FRAMES", 121))
STEPS  = int(os.environ.get("STEPS", 10))
DO_SR  = os.environ.get("DO_SR", "1") == "1"
os.makedirs(OUT, exist_ok=True)

STYLE = ("Photorealistic cinematic still, anamorphic framing, shallow depth of field, "
         "volumetric backlight through blowing snow, fine film grain, muted steel-blue grade, "
         "warm gold light only from the hero's runes. "
         "No dialogue, no text, no subtitles, no logos, no watermark.")

SHOTS = [
  {"id": "p1_1", "img": "p1_1.png", "seed": 1101,
   "prompt": ("cinematic shot: the bald armoured knight stands on a glacier ridge with both hands "
              "resting on the haft of a planted warhammer; wind-driven snow streams past his shoulders "
              "and his wolf-fur mantle lifts in the gusts. The camera holds steady. " + STYLE)},

  {"id": "p1_2", "img": "p1_2.png", "seed": 1202,
   "prompt": ("cinematic shot: a towering skeletal king in rusted frost-rimed plate raises its skull "
              "slowly, pale cyan light swelling in the hollow eye sockets while sickly green light "
              "pulses from the ribcage. The camera holds low and still. " + STYLE)},

  {"id": "p1_3", "img": "p1_3.png", "seed": 1303,
   "prompt": ("cinematic shot: in medium close-up the knight's weathered face stays calm and resolute "
              "while the golden light of the runes on his chest brightens and rims his jaw and cheek. "
              "The camera does not move. " + STYLE)},

  {"id": "p1_4a", "img": "p1_4a.png", "seed": 1404,
   "prompt": ("cinematic shot: a ring of golden runes on the ice ignites and spreads outward in burning "
              "arcs while a column of fine ash rises around the kneeling knight and a shaft of sunlight "
              "breaks through the blizzard above him. The camera pushes in slowly. " + STYLE)},
]

if ONLY:
    SHOTS = [s for s in SHOTS if s["id"] in ONLY]

logf = open(os.path.join(OUT, "run.log"), "a", buffering=1)
def log(*a):
    m = " ".join(str(x) for x in a)
    print(m, flush=True); logf.write(m + "\n")

log("torch", torch.__version__, "cuda", torch.cuda.is_available())
if torch.cuda.is_available():
    p = torch.cuda.get_device_properties(0)
    log(f"GPU {p.name}  {p.total_memory/1e9:.0f}GB")

from diffusers import Kandinsky6TI2VAPipeline
from diffusers.utils import load_image, encode_video

MODEL = "kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers"
log("loading", MODEL)
t0 = time.time()
pipe = Kandinsky6TI2VAPipeline.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
log(f"loaded in {time.time()-t0:.0f}s")

results = {}
for sh in SHOTS:
    sid = sh["id"]
    img_path = os.path.join(IN, sh["img"])
    if not os.path.exists(img_path):
        log(f"[{sid}] MISSING still {img_path}"); results[sid] = {"ok": False, "err": "no still"}; continue
    log(f"[{sid}] start  {W}x{H} frames={FRAMES} steps={STEPS} seed={sh['seed']}")
    try:
        torch.manual_seed(sh["seed"])
        t = time.time()
        out = pipe(
            prompt=sh["prompt"],
            image=load_image(img_path),
            height=H, width=W,
            num_frames=FRAMES,
            num_inference_steps=STEPS,
            guidance_scale=1.0,
            sample_audio=(os.environ.get("GEN_AUDIO","1")=="1"),
        )
        gen_s = time.time() - t
        raw = os.path.join(OUT, f"k6_{sid}_gen.mp4")
        aud = getattr(out, "audio", None)
        if aud is not None:
            try:
                encode_video(out.frames[0], fps=24, output_path=raw,
                             audio=aud[0][None], audio_sample_rate=pipe.audio_sample_rate)
                log(f"[{sid}] native audio muxed @{pipe.audio_sample_rate}Hz")
            except Exception as ae:
                log(f"[{sid}] audio mux fail {ae}; video-only")
                encode_video(out.frames[0], fps=24, output_path=raw)
        else:
            encode_video(out.frames[0], fps=24, output_path=raw)
        log(f"[{sid}] generated in {gen_s:.0f}s -> {raw} ({os.path.getsize(raw)/1e6:.1f} MB)")
        results[sid] = {"ok": True, "gen_s": round(gen_s, 1), "file": raw}
        del out
        torch.cuda.empty_cache()
    except Exception as e:
        log(f"[{sid}] FAILED: {e}")
        log(traceback.format_exc()[-1500:])
        results[sid] = {"ok": False, "err": str(e)[:300]}

if DO_SR and any(r.get("ok") for r in results.values()):
    try:
        import imageio.v3 as iio
        from diffusers import Kandinsky6SRPipeline
        SR = "kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers"
        log("loading SR", SR)
        t0 = time.time()
        sr = Kandinsky6SRPipeline.from_pretrained(SR, torch_dtype=torch.bfloat16)
        sr.enable_model_cpu_offload()
        log(f"SR loaded in {time.time()-t0:.0f}s")
        for sid, r in list(results.items()):
            if not r.get("ok"):
                continue
            try:
                t = time.time()
                frames = [f for f in iio.imiter(r["file"], plugin="pyav")]
                log(f"[{sid}] SR input {len(frames)} frames {frames[0].shape}")
                up = sr(video=[frames], resolution_scale=2.25, num_inference_steps=2).frames[0]
                hd = os.path.join(OUT, f"k6_{sid}_1080.mp4")
                encode_video(up, fps=24, output_path=hd)
                log(f"[{sid}] SR {time.time()-t:.0f}s -> {hd} ({os.path.getsize(hd)/1e6:.1f} MB)")
                r["sr"] = hd
                json.dump(results, open(os.path.join(OUT, "results.json"), "w"), indent=2)
                del up, frames
                torch.cuda.empty_cache()
            except Exception as e:
                log(f"[{sid}] SR FAILED (gen clip kept): {e}")
                log(traceback.format_exc()[-600:])
    except Exception as e:
        log("SR pipeline unavailable:", e)

json.dump(results, open(os.path.join(OUT, "results.json"), "w"), indent=2)
log("DONE", json.dumps({k: bool(v.get('ok')) for k, v in results.items()}))
