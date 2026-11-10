import json, os, shutil, sys, time, urllib.request

SERVER = os.environ.get("COMFY", "http://127.0.0.1:8188")
UNET = "wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors"
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE = "wan_2.1_vae.safetensors"
LORA = "Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors"
LENGTH = 81
FPS = 16
NEG = ("static, frozen, still image, no motion, slideshow, crossfade, dissolve, "
       "morphing faces, identity change, warping, melting, extra limbs, extra "
       "fingers, deformed hands, cartoon, anime, 3d render, blurry, low quality, "
       "text, watermark")

def post(p, pl):
    r = urllib.request.Request(SERVER + p, data=json.dumps(pl).encode(),
                               headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=120))

def get(p):
    return json.load(urllib.request.urlopen(SERVER + p, timeout=120))

def graph(start, end, pos, seed, w, h):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "1b": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": LORA, "strength_model": 1.0}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "wan"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": pos}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEG}},
        "6": {"class_type": "LoadImage", "inputs": {"image": start}},
        "7": {"class_type": "LoadImage", "inputs": {"image": end}},
        "8": {"class_type": "WanFirstLastFrameToVideo", "inputs": {"positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0], "width": w, "height": h, "length": LENGTH, "batch_size": 1, "start_image": ["6", 0], "end_image": ["7", 0]}},
        "9": {"class_type": "KSampler", "inputs": {"model": ["1b", 0], "positive": ["8", 0], "negative": ["8", 1], "latent_image": ["8", 2], "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
        "11": {"class_type": "CreateVideo", "inputs": {"images": ["10", 0], "fps": FPS}},
        "12": {"class_type": "SaveVideo", "inputs": {"video": ["11", 0], "filename_prefix": "flf", "format": "mp4", "codec": "h264"}},
    }

def main():
    watchdog(int(__import__('os').environ.get('WATCHDOG_SECS','21600')))
    jobs = json.load(open("/workspace/wan_flf_jobs_35.json"))
    outdir = "/workspace/v3_out"
    os.makedirs(outdir, exist_ok=True)
    done = fail = 0
    for j in jobs:
        tag = j["tag"]
        st = "/workspace/kf/" + j["start"]
        en = "/workspace/kf/" + j["end"]
        mp4 = os.path.join(outdir, tag + ".mp4")
        if os.path.exists(mp4) and os.path.getsize(mp4) > 1e5:
            done += 1
            continue
        pos = (j["prompt"][:900] + ". Continuous natural motion, real physics, photoreal cinematic.")
        try:
            r = post("/prompt", {"prompt": graph(st, en, pos, int(j["shot"]) * 7919, 1280, 720)})
            pid = r.get("prompt_id")
            t0 = time.time()
            ok = False
            while time.time() - t0 < 5400:
                h = get("/history/" + pid)
                if pid in h:
                    s = h[pid].get("status", {})
                    if s.get("status_str") != "success":
                        print(tag, "FAIL", str(s.get("messages"))[:200], flush=True)
                        fail += 1
                        ok = True
                        break
                    for node, o in (h[pid].get("outputs") or {}).items():
                        for k, v in o.items():
                            if isinstance(v, list):
                                for it in v:
                                    if isinstance(it, dict) and it.get("filename"):
                                        src = os.path.join("/opt/workspace-internal/ComfyUI/output", it["filename"])
                                        shutil.copy(src, mp4)
                    print(tag, "OK", round(time.time() - t0, 1), "s",
                          os.path.getsize(mp4) if os.path.exists(mp4) else 0, flush=True)
                    done += 1
                    ok = True
                    break
                time.sleep(10)
            if not ok:
                print(tag, "TIMEOUT", flush=True)
                fail += 1
        except Exception as e:
            print(tag, "ERR", str(e)[:200], flush=True)
            fail += 1
            try:
                get('/system_stats')
            except Exception:
                print("SERVER DEAD - stopping batch to halt burn", flush=True)
                return

def watchdog(max_secs):
    import threading
    def _w():
        import time as _t
        _t.sleep(max_secs)
        print("WATCHDOG EXPIRED - batch self-terminating", flush=True)
        import os as _os
        _os._exit(3)
    threading.Thread(target=_w, daemon=True).start()

if __name__ == "__main__":
    main()
