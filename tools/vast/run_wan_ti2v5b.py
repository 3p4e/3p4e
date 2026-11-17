#!/usr/bin/env python3
"""Run one Wan 2.2 TI2V-5B clip on a local ComfyUI.

Differences from run_wan_i2v.py (14B pair) that matter:
  * ONE transformer, not a high/low-noise pair.
  * VAE is wan2.2_vae.safetensors (high-compression 16x16x4), NOT wan_2.1_vae.
    Using the 2.1 VAE with this model produces garbage.
  * Native 1280x704 @ 24 fps. No 480p render + upscale + 16->24 interpolation.
  * No distill LoRA exists for the 5B in the Comfy repack (all six are 14B),
    so this runs real CFG sampling. Steps are the cost driver here.

Usage on the Vast instance (ComfyUI on :8199):
  /venv/main/bin/python run_wan_ti2v5b.py --imagefile k_sp6.jpg --tag sp6c --prompt '...'
"""
import argparse, json, os, sys, time, urllib.request, urllib.parse, uuid

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:8199")
ap.add_argument("--w", type=int, default=1280)
ap.add_argument("--h", type=int, default=704)
ap.add_argument("--frames", type=int, default=121)   # 121 = 8k+1, 5.04 s @ 24 fps
ap.add_argument("--fps", type=float, default=24.0)
ap.add_argument("--steps", type=int, default=30)
ap.add_argument("--cfg", type=float, default=5.0)
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--imagefile", default=None, help="file already inside ComfyUI input/")
ap.add_argument("--tag", default="ti2v5b")
ap.add_argument("--endimage", default=None, help="file in ComfyUI input/ used as LAST frame")
ap.add_argument("--prompt", required=True)
ap.add_argument("--negative", default="blurry, distorted, extra objects, helicopters, birds, boats, flickering, text, watermark, jitter, morphing, extra people")
a = ap.parse_args()

UNET = "wan2.2_ti2v_5B_fp16.safetensors"
VAE  = "wan2.2_vae.safetensors"
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"

def http(method, path, data=None, headers=None):
    req = urllib.request.Request(a.host + path, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(req, timeout=180).read()

if not a.imagefile:
    sys.exit("--imagefile is required (upload the still into ComfyUI input/ first)")
name = a.imagefile
b = uuid.uuid4().hex

wf = {
 "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
 "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "wan", "device": "default"}},
 "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
 "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": a.prompt}},
 "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": a.negative}},
 "6": {"class_type": "LoadImage", "inputs": {"image": name}},
 "7": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
 "8": {"class_type": "KSampler", "inputs": {"model": ["7", 0], "seed": a.seed, "steps": a.steps, "cfg": a.cfg,
        "sampler_name": "uni_pc", "scheduler": "simple", "positive": ["4", 0], "negative": ["5", 0],
        "latent_image": ["9", 2], "denoise": 1.0}},
 "9": {"class_type": "WanImageToVideo", "inputs": {"positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0],
        "width": a.w, "height": a.h, "length": a.frames, "batch_size": 1, "start_image": ["6", 0]}},
 "10": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
 "11": {"class_type": "CreateVideo", "inputs": {"images": ["10", 0], "fps": a.fps}},
 "12": {"class_type": "SaveVideo", "inputs": {"video": ["11", 0], "filename_prefix": f"ti2v5b_{a.tag}_{a.w}x{a.h}",
        "format": "auto", "codec": "auto"}},
}

# KSampler must read the sampler latent from the WanImageToVideo node, not from itself
wf["8"]["inputs"]["latent_image"] = ["9", 2]

if a.endimage:
    wf["13"] = {"class_type": "LoadImage", "inputs": {"image": a.endimage}}
    wf["9"] = {"class_type": "WanFirstLastFrameToVideo", "inputs": {"positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0],
            "width": a.w, "height": a.h, "length": a.frames, "batch_size": 1,
            "start_image": ["6", 0], "end_image": ["13", 0]}}
    wf["8"]["inputs"]["latent_image"] = ["9", 2]

# preflight against the live ComfyUI
missing = []
try:
    oi = json.loads(http("GET", "/object_info"))
    for nid, n in wf.items():
        c = n["class_type"]
        if c not in oi:
            missing.append(f"node class missing: {c}"); continue
        req_in = set(oi[c].get("input", {}).get("required", {}).keys())
        given = set(n["inputs"].keys())
        if req_in - given: missing.append(f"{c} missing required {sorted(req_in - given)}")
    # model availability
    for node, key, want in (("UNETLoader","unet_name",UNET), ("VAELoader","vae_name",VAE), ("CLIPLoader","clip_name",CLIP)):
        try:
            opts = oi[node]["input"]["required"][key][0]
            if want not in opts: missing.append(f"MODEL NOT ON SERVER: {want}")
        except Exception:
            pass
except Exception as e:
    print("PREFLIGHT skipped:", e)
for m in missing:
    print("PREFLIGHT:", m)
if any("MODEL NOT ON SERVER" in m or "node class missing" in m for m in missing):
    print("PREFLIGHT FAILED - not queueing"); sys.exit(3)

t0 = time.time()
try:
    r = json.loads(http("POST", "/prompt", json.dumps({"prompt": wf, "client_id": b}).encode(), {"Content-Type": "application/json"}))
except urllib.error.HTTPError as e:
    print("PROMPT REJECTED:", e.read().decode()[:2000]); sys.exit(1)
pid = r["prompt_id"]; print("queued", pid, f"({a.w}x{a.h}, {a.frames}f @ {a.fps}fps, {a.steps} steps, cfg {a.cfg})")
while True:
    time.sleep(5)
    h = json.loads(http("GET", f"/history/{pid}"))
    if pid in h:
        st = h[pid].get("status", {})
        if st.get("status_str") == "error":
            print("ERROR:", json.dumps(st)[:3000]); sys.exit(2)
        print(f"DONE in {time.time()-t0:.0f}s")
        print(json.dumps(h[pid].get("outputs", {}))[:1000]); break
    el = time.time() - t0
    if int(el) % 30 < 5: print(f"  ...{el:.0f}s")
