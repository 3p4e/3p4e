#!/usr/bin/env python3
"""FLF proof with 4-step Lightning LoRA on the Wan2.1 14B backbone.
Adds LoraLoaderModelOnly between UNETLoader and KSampler.
Lightning requires cfg=1.0 (CFG disabled) and 4 steps.
"""
import json, os, sys, time, urllib.request

SERVER = os.environ.get("COMFY", "http://127.0.0.1:8188")
UNET   = "wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors"
CLIP   = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE    = "wan_2.1_vae.safetensors"
LORA   = "wan21_t2v_4step_lora.safetensors"
LENGTH = 81
FPS    = 16

def post(p, payload):
    r = urllib.request.Request(f"{SERVER}{p}", data=json.dumps(payload).encode(),
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.load(resp)

def get(p):
    with urllib.request.urlopen(f"{SERVER}{p}", timeout=120) as resp:
        return json.load(resp)

def graph(start, end, pos, neg, seed, steps, w, h, cfg, lora_strength, use_lora):
    g = {
      "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
      "2": {"class_type": "CLIPLoader",  "inputs": {"clip_name": CLIP, "type": "wan"}},
      "3": {"class_type": "VAELoader",  "inputs": {"vae_name": VAE}},
      "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": pos}},
      "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": neg}},
      "6": {"class_type": "LoadImage", "inputs": {"image": start}},
      "7": {"class_type": "LoadImage", "inputs": {"image": end}},
      "8": {"class_type": "WanFirstLastFrameToVideo", "inputs": {
              "positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0],
              "width": w, "height": h, "length": LENGTH, "batch_size": 1,
              "start_image": ["6", 0], "end_image": ["7", 0]}},
      "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
      "11": {"class_type": "CreateVideo", "inputs": {"images": ["10", 0], "fps": FPS}},
      "12": {"class_type": "SaveVideo", "inputs": {"video": ["11", 0],
              "filename_prefix": "flf_lora", "format": "mp4", "codec": "h264"}},
    }
    if use_lora:
        g["1b"] = {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["1", 0], "lora_name": LORA, "strength_model": lora_strength}}
        model_ref = ["1b", 0]
    else:
        model_ref = ["1", 0]
    g["9"] = {"class_type": "KSampler", "inputs": {
        "model": model_ref, "positive": ["8", 0], "negative": ["8", 1],
        "latent_image": ["8", 2], "seed": seed, "steps": steps, "cfg": cfg,
        "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}}
    return g

def main():
    a = sys.argv[1:]
    start, end = a[0], a[1]
    steps = int(a[2]) if len(a) > 2 else 4
    cfg   = float(a[3]) if len(a) > 3 else 1.0
    use_lora = (a[4].lower() != "nolora") if len(a) > 4 else True
    seed  = int(a[5]) if len(a) > 5 else 190119
    pos = ("Photoreal cinematic battle motion. The hooded demon hunter in blackened frost-etched "
           "plate fires both hand crossbows, frost smoke and violet muzzle flare. The bald paladin "
           "in gold-trimmed plate with a molten-gold rune across one eye drives his longsword "
           "forward, gold light flaring. Behind them the colossal ember demon recoils as a jagged "
           "blue ice wall erupts from the cracked obsidian ground. Ash falls, heat shimmer, "
           "camera pushes in slowly. Continuous natural movement, real physics.")
    neg = ("static, frozen, still image, no motion, slideshow, crossfade, dissolve, morphing "
           "faces, identity change, warping, melting, extra limbs, extra fingers, deformed hands, "
           "wings, bat wings, face on the demon, eyes on the demon, helmet, cartoon, anime, "
           "3d render, blurry, low quality, text, watermark")
    g = graph(start, end, pos, neg, seed, steps, 1280, 720, cfg, 1.0, use_lora)
    print(json.dumps({"unet": UNET, "lora": LORA if use_lora else None, "steps": steps,
                      "cfg": cfg, "seed": seed, "length": LENGTH}), flush=True)
    t0 = time.time()
    r = post("/prompt", {"prompt": g})
    pid = r.get("prompt_id")
    print(json.dumps({"queued": pid}), flush=True)
    while time.time() - t0 < 5400:
        h = get(f"/history/{pid}")
        if pid in h:
            hist = h[pid]
            st = hist.get("status", {})
            print(json.dumps({"status": st.get("status_str"), "secs": round(time.time()-t0, 1)}), flush=True)
            if st.get("status_str") != "success":
                print(json.dumps({"messages": st.get("messages", [])})[:3000], flush=True)
                return 2
            for node, o in (hist.get("outputs") or {}).items():
                for key, val in o.items():
                    if isinstance(val, list):
                        for v in val:
                            if isinstance(v, dict) and v.get("filename"):
                                print(json.dumps({"output": v}), flush=True)
            return 0
        time.sleep(5)
    print(json.dumps({"timeout": True}), flush=True)
    return 3

if __name__ == "__main__":
    sys.exit(main())
