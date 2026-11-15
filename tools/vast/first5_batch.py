#!/usr/bin/env python3
import json, os, sys, time, urllib.request

SERVER = os.environ.get("COMFY", "http://127.0.0.1:8188")
UNET   = "wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors"
CLIP   = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE    = "wan_2.1_vae.safetensors"
LORA   = "Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors"
LENGTH = 81
FPS    = 16

NEG = ("static, frozen, still image, no motion, slideshow, crossfade, dissolve, morphing "
       "faces, identity change, warping, melting, empty hands, weapons vanishing, dropping "
       "weapons, crossbow fading, missing weapons, disappearing weapons, extra limbs, extra "
       "fingers, deformed hands, wings, bat wings, face on the demon, eyes on the demon, "
       "helmet, cartoon, anime, 3d render, blurry, low quality, text, watermark")

def post(p, payload):
    r = urllib.request.Request(SERVER + p, data=json.dumps(payload).encode(),
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.load(resp)

def get(p):
    with urllib.request.urlopen(SERVER + p, timeout=300) as resp:
        return json.load(resp)

def graph(start, end, pos, seed, w, h):
    return {
      "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
      "1b": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": LORA, "strength_model": 1.0}},
      "2": {"class_type": "CLIPLoader",  "inputs": {"clip_name": CLIP, "type": "wan"}},
      "3": {"class_type": "VAELoader",  "inputs": {"vae_name": VAE}},
      "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": pos}},
      "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEG}},
      "6": {"class_type": "LoadImage", "inputs": {"image": start}},
      "7": {"class_type": "LoadImage", "inputs": {"image": end}},
      "8": {"class_type": "WanFirstLastFrameToVideo", "inputs": {
              "positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0],
              "width": w, "height": h, "length": LENGTH, "batch_size": 1,
              "start_image": ["6", 0], "end_image": ["7", 0]}},
      "9": {"class_type": "KSampler", "inputs": {
              "model": ["1b", 0], "positive": ["8", 0], "negative": ["8", 1],
              "latent_image": ["8", 2], "seed": seed, "steps": 8, "cfg": 1.0,
              "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
      "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
      "11": {"class_type": "CreateVideo", "inputs": {"images": ["10", 0], "fps": FPS}},
      "12": {"class_type": "SaveVideo", "inputs": {"video": ["11", 0],
              "filename_prefix": "clip", "format": "mp4", "codec": "h264"}},
    }

def main():
    shots = [int(x) for x in sys.argv[1].split(",")]
    jobs = {int(j["shot"]): j for j in json.load(open("/workspace/wan_flf_jobs_50.json"))}
    for s in shots:
        j = jobs.get(s)
        if not j:
            print("shot", s, "NOT IN JOBFILE, skip", flush=True)
            continue
        start, end = j["start"], j["end"]
        pos = j["prompt"]
        seed = 190000 + s
        print("SHOT %02d start=%s end=%s seed=%d prompt[%d]" % (s, start, end, seed, len(pos)), flush=True)
        g = graph(start, end, pos, seed, int(j.get("w", 1280)), int(j.get("h", 720)))
        try:
            r = post("/prompt", {"prompt": g})
            pid = r.get("prompt_id")
            t0 = time.time()
            while True:
                h = get("/history/" + pid)
                if pid in h and (h[pid].get("outputs") or h[pid].get("status", {}).get("completed")):
                    break
                time.sleep(10)
            dt = time.time() - t0
            outs = h[pid].get("outputs", {})
            print("  DONE shot %02d in %.0fs outputs=%s" % (s, dt, json.dumps(list(outs.keys()))), flush=True)
        except Exception as e:
            print("  ERROR shot %02d: %s" % (s, e), flush=True)

if __name__ == "__main__":
    main()
