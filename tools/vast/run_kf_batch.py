#!/usr/bin/env python3
"""Batch render the 100 bossfight keyframe stills.

Variant of run_qwen_edit.py that supports TWO job modes:
  - hero shots (refs present)  -> face-conditioned edit (image1/image2)
  - boss-only shots (refs [])  -> pure text-to-image (no image inputs)

Graph is identical except the image refs are omitted when refs is empty,
matching the optional image1/image2/image3 inputs on TextEncodeQwenImageEditPlus.

Runs ON the instance (stdlib only).
"""
import argparse, json, os, shutil, sys, time, urllib.request, uuid

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:8188")
ap.add_argument("--jobs", required=True)
ap.add_argument("--out", default="/workspace/out_edit")
ap.add_argument("--comfy-dir", default="/workspace/ComfyUI")
ap.add_argument("--timeout", type=int, default=900)
a = ap.parse_args()

UNET  = "qwen_image_edit_2511_fp8mixed.safetensors"
CLIP  = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE   = "qwen_image_vae.safetensors"
SHIFT = 3.1
STEPS = 40
CFG   = 4.0

DEFAULT_NEG = ("blurry, deformed face, distorted eyes, asymmetrical eyes, extra limbs, "
               "extra fingers, melted or smudged armour, cartoon, illustration, "
               "plastic skin, text, watermark, low quality, low resolution, "
               "overexposed, oversaturated, different person, wrong identity")


def http(method, path, data=None, timeout=120):
    req = urllib.request.Request(a.host + path, data=data, method=method)
    return urllib.request.urlopen(req, timeout=timeout).read()


def log(msg):
    print(json.dumps(msg), flush=True)


def preflight():
    oi = json.loads(http("GET", "/object_info"))
    have = set(oi.keys())
    needs = ["UNETLoader", "ModelSamplingAuraFlow", "CLIPLoader", "VAELoader",
             "LoadImage", "ImageScaleToTotalPixels", "TextEncodeQwenImageEditPlus",
             "EmptySD3LatentImage", "KSampler", "VAEDecode", "SaveImage"]
    missing = [n for n in needs if n not in have]
    if missing:
        log({"fatal": True, "missing_nodes": missing}); sys.exit(2)
    m = os.path.join(a.comfy_dir, "models")
    files = {"unet": os.path.join(m, "diffusion_models", UNET),
             "clip": os.path.join(m, "text_encoders", CLIP),
             "vae":  os.path.join(m, "vae", VAE)}
    for k, p in files.items():
        if not os.path.exists(p):
            log({"fatal": True, "missing_weights": k, "path": p}); sys.exit(2)
    log({"preflight": "ok"})


def build(job):
    w = job.get("width", 1280)
    h = job.get("height", 720)
    refs = job.get("refs", [])
    use_refs = bool(refs)
    wf = {
        "1": {"class_type": "UNETLoader",
              "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2": {"class_type": "ModelSamplingAuraFlow",
              "inputs": {"model": ["1", 0], "shift": SHIFT}},
        "3": {"class_type": "CLIPLoader",
              "inputs": {"clip_name": CLIP, "type": "qwen_image", "device": "default"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "7": {"class_type": "EmptySD3LatentImage",
              "inputs": {"width": w, "height": h, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "seed": job["seed"], "steps": job.get("steps", STEPS),
            "cfg": job.get("cfg", CFG), "sampler_name": "euler", "scheduler": "simple",
            "denoise": 1.0, "positive": ["20", 0], "negative": ["21", 0],
            "latent_image": ["7", 0]}},
        "9": {"class_type": "VAEDecode",
              "inputs": {"samples": ["8", 0], "vae": ["4", 0]}},
        "10": {"class_type": "SaveImage",
               "inputs": {"images": ["9", 0], "filename_prefix": job["tag"]}},
    }
    enc_in = {"clip": ["3", 0], "prompt": job["prompt"], "vae": ["4", 0]}
    if use_refs:
        for i, ref in enumerate(refs[:3], start=1):
            nid = f"ref{i}"
            sid = f"scale{i}"
            wf[nid] = {"class_type": "LoadImage", "inputs": {"image": ref}}
            wf[sid] = {"class_type": "ImageScaleToTotalPixels",
                       "inputs": {"image": [nid, 0], "upscale_method": "lanczos",
                                  "megapixels": 1.0, "resolution_steps": 1}}
            enc_in[f"image{i}"] = [sid, 0]
    wf["20"] = {"class_type": "TextEncodeQwenImageEditPlus", "inputs": enc_in}
    wf["21"] = {"class_type": "TextEncodeQwenImageEditPlus",
                "inputs": {**{k: v for k, v in enc_in.items() if k != "prompt"},
                           "prompt": job.get("negative", DEFAULT_NEG)}}
    return wf


def submit(wf):
    body = json.dumps({"prompt": wf, "client_id": uuid.uuid4().hex}).encode()
    try:
        r = json.loads(http("POST", "/prompt", body))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {detail[:1200]}") from None
    if "prompt_id" not in r:
        raise RuntimeError(json.dumps(r)[:1200])
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
        time.sleep(4)
    return None, None


def main():
    preflight()
    jobs = json.load(open(a.jobs))
    os.makedirs(a.out, exist_ok=True)
    outdir = os.path.join(a.comfy_dir, "output")
    log({"jobs": len(jobs), "hero": sum(1 for j in jobs if j.get("refs")),
         "boss_only": sum(1 for j in jobs if not j.get("refs"))})
    for job in jobs:
        t0 = time.time()
        try:
            for r in job.get("refs", []):
                p = os.path.join(a.comfy_dir, "input", r)
                if not os.path.exists(p):
                    raise FileNotFoundError(f"ref not staged: {p}")
            pid = submit(build(job))
            imgs, h = wait(pid, a.timeout)
            if h is not None and h.get("status", {}).get("status_str") == "error":
                log({"tag": job["tag"], "error": "exec error", "detail": json.dumps(h)[:500]}); continue
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
    log({"all_done": True})


if __name__ == "__main__":
    main()
