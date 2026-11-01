#!/usr/bin/env python3
"""Run one Wan 2.2 14B image-to-video test on a local ComfyUI (Lightning 4-step).

Usage on the Vast instance (after ComfyUI is running on :8188):
  source /venv/main/bin/activate
  python /workspace/run_wan_i2v.py                 # 480p, 81 frames
  python /workspace/run_wan_i2v.py --w 1280 --h 720
Uses only the standard library. Prints wall-clock time and the output path.
"""
import argparse, json, os, sys, time, urllib.request, urllib.parse, uuid

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:8188")
ap.add_argument("--w", type=int, default=832)
ap.add_argument("--h", type=int, default=480)
ap.add_argument("--frames", type=int, default=81)
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--imagefile", default=None, help="file name already inside ComfyUI input/ (skips download+upload)")
ap.add_argument("--tag", default="test")
ap.add_argument("--image", default="https://raw.githubusercontent.com/3p4e/3p4e/claude/elegant-thompson-uqhred/tools/vast/assets/city_lit_test.jpg")
ap.add_argument("--prompt", default="The camera slowly pushes forward toward a single floating city on a rocky island above dark storm clouds, steady and smooth, no other moving objects.")
ap.add_argument("--negative", default="blurry, distorted, extra objects, birds, helicopters, flickering, text, watermark, jitter")
a = ap.parse_args()

def http(method, path, data=None, headers=None):
    req = urllib.request.Request(a.host + path, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(req, timeout=120).read()

# 1) start image: a file already in ComfyUI's input folder, or download + upload the default test image
if a.imagefile:
    name = a.imagefile; b = uuid.uuid4().hex
else:
    img_bytes = urllib.request.urlopen(a.image, timeout=60).read()
    name = "city_lit_test.jpg"
    b = uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Disposition: form-data; name="image"; filename="{name}"\r\nContent-Type: image/jpeg\r\n\r\n').encode() + img_bytes + (f'\r\n--{b}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{b}--\r\n').encode()
    print("upload:", json.loads(http("POST", "/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={b}"})))

H_UNET = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
L_UNET = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
H_LORA = "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors"
L_LORA = "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors"

wf = {
 "1": {"class_type": "UNETLoader", "inputs": {"unet_name": H_UNET, "weight_dtype": "default"}},
 "2": {"class_type": "UNETLoader", "inputs": {"unet_name": L_UNET, "weight_dtype": "default"}},
 "3": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": H_LORA, "strength_model": 1.0}},
 "4": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["2", 0], "lora_name": L_LORA, "strength_model": 1.0}},
 "5": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["3", 0], "shift": 5.0}},
 "6": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["4", 0], "shift": 5.0}},
 "7": {"class_type": "CLIPLoader", "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default"}},
 "8": {"class_type": "VAELoader", "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
 "9": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["7", 0], "text": a.prompt}},
 "10": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["7", 0], "text": a.negative}},
 "11": {"class_type": "LoadImage", "inputs": {"image": name}},
 "12": {"class_type": "WanImageToVideo", "inputs": {"positive": ["9", 0], "negative": ["10", 0], "vae": ["8", 0], "width": a.w, "height": a.h, "length": a.frames, "batch_size": 1, "start_image": ["11", 0]}},
 "13": {"class_type": "KSamplerAdvanced", "inputs": {"model": ["5", 0], "add_noise": "enable", "noise_seed": a.seed, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "positive": ["12", 0], "negative": ["12", 1], "latent_image": ["12", 2], "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable"}},
 "14": {"class_type": "KSamplerAdvanced", "inputs": {"model": ["6", 0], "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "positive": ["12", 0], "negative": ["12", 1], "latent_image": ["13", 0], "start_at_step": 2, "end_at_step": 10000, "return_with_leftover_noise": "disable"}},
 "15": {"class_type": "VAEDecode", "inputs": {"samples": ["14", 0], "vae": ["8", 0]}},
 "16": {"class_type": "CreateVideo", "inputs": {"images": ["15", 0], "fps": 16.0}},
 "17": {"class_type": "SaveVideo", "inputs": {"video": ["16", 0], "filename_prefix": f"wan22_{a.tag}_{a.w}x{a.h}", "format": "auto", "codec": "auto"}},
}


# preflight: compare our graph with what this ComfyUI actually offers
try:
    oi = json.loads(http("GET", "/object_info"))
    for nid, n in wf.items():
        c = n["class_type"]
        if c not in oi:
            print(f"PREFLIGHT: node class missing on server: {c}"); continue
        req_in = set(oi[c].get("input", {}).get("required", {}).keys())
        given = set(n["inputs"].keys())
        if req_in - given: print(f"PREFLIGHT: {c} missing required inputs {sorted(req_in - given)}")
        opt = set(oi[c].get("input", {}).get("optional", {}).keys())
        unk = given - req_in - opt
        if unk: print(f"PREFLIGHT: {c} has inputs the server does not know {sorted(unk)}")
except Exception as e:
    print("PREFLIGHT skipped:", e)

t0 = time.time()
try:
    r = json.loads(http("POST", "/prompt", json.dumps({"prompt": wf, "client_id": b}).encode(), {"Content-Type": "application/json"}))
except urllib.error.HTTPError as e:
    print("PROMPT REJECTED:", e.read().decode()[:2000]); sys.exit(1)
pid = r["prompt_id"]; print("queued", pid)
while True:
    time.sleep(5)
    h = json.loads(http("GET", f"/history/{pid}"))
    if pid in h:
        st = h[pid].get("status", {})
        if st.get("status_str") == "error":
            print("ERROR:", json.dumps(st)[:3000]); sys.exit(2)
        outs = h[pid].get("outputs", {})
        print(f"DONE in {time.time()-t0:.0f}s ({a.w}x{a.h}, {a.frames} frames)")
        print(json.dumps(outs)[:1000]); break
    if int(time.time() - t0) % 30 < 5: print(f"  ...{time.time()-t0:.0f}s")
