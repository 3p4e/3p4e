#!/usr/bin/env python3
"""Qwen-Image T2I keyframe generator — ORIGINAL characters, full quality.

Verified recipe (Comfy-Org 'Text to Image (Qwen-Image)' blueprint, node schemas from
/object_info on ComfyUI 0.43.0 port 18188):

  UNETLoader(qwen_image_fp8_e4m3fn.safetensors) -> ModelSamplingAuraFlow(3.1)
  CLIPLoader(qwen_2.5_vl_7b_fp8_scaled, qwen_image) -> CLIPTextEncode x2
  VAELoader(qwen_image_vae) ; EmptySD3LatentImage(w,h)
  KSampler(50 steps, cfg 4.0, euler/simple) -> VAEDecode -> SaveImage

NO Lightning LoRA: the blueprint's own note says 'Try 50 steps for the original
Qwen-Image setting' — this is the full-quality path, not the 4-step shortcut that
mushed the last set.

jobs.json: [{"tag":"ash_1_s1","prompt":"...","negative":"...","seed":101,
             "width":1376,"height":768}, ...]
Stdlib only, runs ON the instance. Output saved to --out (default /workspace/out).
"""
import argparse, json, os, shutil, sys, time, urllib.request, uuid

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:18188")
ap.add_argument("--jobs", required=True)
ap.add_argument("--out", default="/workspace/out")
ap.add_argument("--comfy-dir", default="/opt/workspace-internal/ComfyUI")
ap.add_argument("--timeout", type=int, default=2400)
a = ap.parse_args()

UNET  = "qwen_image_2512_fp8_e4m3fn.safetensors"   # 2512 T2I (Apache-2.0, verified in Comfy-Org repo)
CLIP  = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE   = "qwen_image_vae.safetensors"
SHIFT = 3.1
STEPS = 50
CFG   = 4.0


def http(method, path, data=None, timeout=60):
    req = urllib.request.Request(a.host + path, data=data, method=method)
    return urllib.request.urlopen(req, timeout=timeout).read()


def log(msg):
    print(json.dumps(msg), flush=True)


def preflight():
    oi = json.loads(http("GET", "/object_info"))
    have = set(oi.keys())
    needs = ["UNETLoader", "ModelSamplingAuraFlow", "CLIPLoader", "VAELoader",
             "CLIPTextEncode", "EmptySD3LatentImage", "KSampler", "VAEDecode", "SaveImage"]
    missing = [n for n in needs if n not in have]
    if missing:
        log({"fatal": True, "missing_nodes": missing}); sys.exit(2)
    m = os.path.join(a.comfy_dir, "models")
    files = {"unet": os.path.join(m, "diffusion_models", UNET),
             "clip": os.path.join(m, "text_encoders", CLIP),
             "vae":  os.path.join(m, "vae", VAE)}
    missing_f = [k for k, p in files.items() if not os.path.exists(p)]
    if missing_f:
        log({"fatal": True, "missing_files": missing_f}); sys.exit(2)
    log({"preflight": "ok"})


def build(job):
    w = job.get("width", 1376)
    h = job.get("height", 768)
    return {
        "1":  {"class_type": "UNETLoader",
               "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2":  {"class_type": "ModelSamplingAuraFlow",
               "inputs": {"model": ["1", 0], "shift": SHIFT}},
        "3":  {"class_type": "CLIPLoader",
               "inputs": {"clip_name": CLIP, "type": "qwen_image", "device": "default"}},
        "4":  {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "5":  {"class_type": "CLIPTextEncode",
               "inputs": {"text": job["prompt"], "clip": ["3", 0]}},
        "6":  {"class_type": "CLIPTextEncode",
               "inputs": {"text": job.get("negative", DEFAULT_NEG), "clip": ["3", 0]}},
        "7":  {"class_type": "EmptySD3LatentImage",
               "inputs": {"width": w, "height": h, "batch_size": 1}},
        "8":  {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "seed": job["seed"], "steps": STEPS, "cfg": CFG,
            "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0,
            "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0]}},
        "9":  {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["4", 0]}},
        "10": {"class_type": "SaveImage",
               "inputs": {"images": ["9", 0], "filename_prefix": job["tag"]}},
    }


DEFAULT_NEG = ("blurry, deformed face, distorted eyes, extra limbs, extra fingers, "
               "melted or smudged armor, cartoon, illustration, plastic skin, text, "
               "watermark, low quality, low resolution, overexposed, oversaturated")


def submit(wf):
    body = json.dumps({"prompt": wf, "client_id": uuid.uuid4().hex}).encode()
    r = json.loads(http("POST", "/prompt", body))
    if "prompt_id" not in r:
        raise RuntimeError(json.dumps(r)[:600])
    return r["prompt_id"]


def wait(pid, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = json.loads(http("GET", f"/history/{pid}"))
        if pid in h:
            imgs = []
            for node in h[pid].get("outputs", {}).values():
                for im in node.get("images", []):
                    imgs.append(im)
            return imgs, h[pid]
        time.sleep(3)
    return None, None


def main():
    preflight()
    jobs = json.load(open(a.jobs))
    os.makedirs(a.out, exist_ok=True)
    outdir = os.path.join(a.comfy_dir, "output")
    log({"jobs": len(jobs)})
    for job in jobs:
        t0 = time.time()
        try:
            pid = submit(build(job))
            imgs, h = wait(pid, a.timeout)
            if h is not None and h.get("status", {}).get("status_str") == "error":
                log({"tag": job["tag"], "error": "exec error",
                     "detail": json.dumps(h)[:400]}); continue
            if not imgs:
                log({"tag": job["tag"], "error": "no output"}); continue
            src = os.path.join(outdir, imgs[0].get("subfolder", ""), imgs[0]["filename"])
            dst = os.path.join(a.out, job["tag"] + ".png")
            if os.path.exists(src):
                shutil.copy2(src, dst)
                log({"tag": job["tag"], "ok": True, "bytes": os.path.getsize(dst),
                     "secs": round(time.time() - t0, 1), "path": dst})
            else:
                log({"tag": job["tag"], "error": "output missing", "src": src})
        except Exception as e:
            log({"tag": job.get("tag"), "error": f"{type(e).__name__}: {str(e)[:300]}"})


if __name__ == "__main__":
    main()
