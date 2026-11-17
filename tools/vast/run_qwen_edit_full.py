#!/usr/bin/env python3
"""Qwen-Image-Edit-2511 FULL-QUALITY keyframe generator (Azulon face-lock).

Same verified recipe as run_qwen_edit.py but WITHOUT the Lightning 4-step LoRA:
  UNETLoader(edit_2511_fp8mixed) -> ModelSamplingAuraFlow(3.1)
  CLIPLoader(qwen_2.5_vl_7b_fp8_scaled, qwen_image) -> TextEncodeQwenImageEditPlus x2
  VAELoader(qwen_image_vae); LoadImage(start) -> FluxKontextImageScale
  KSampler(40 steps, cfg 3.0, euler/simple) -> VAEDecode -> SaveImage

Identity: image1 = the start frame to restage; image2/image3 = Azulon reference photos
(A_bust.png + sheet_front.png) so the face + costume hold while the scene is densified.

jobs.json: [{"tag","seed","image1","image2","image3","prompt","negative"}, ...]
Stdlib only, runs ON the instance. Output -> --out (default /workspace/out).
"""
import argparse, json, os, shutil, sys, time, urllib.request, uuid

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:18188")
ap.add_argument("--jobs", required=True)
ap.add_argument("--out", default="/workspace/out")
ap.add_argument("--comfy-dir", default="/opt/workspace-internal/ComfyUI")
ap.add_argument("--steps", type=int, default=40)
ap.add_argument("--cfg", type=float, default=3.0)
ap.add_argument("--timeout", type=int, default=2400)
a = ap.parse_args()

UNET = "qwen_image_edit_2511_fp8mixed.safetensors"
CLIP = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE  = "qwen_image_vae.safetensors"
SHIFT = 3.1

DEFAULT_NEG = ("blurry, deformed face, distorted eyes, extra limbs, extra fingers, "
               "melted or smudged armor, cartoon, illustration, plastic skin, text, "
               "watermark, low quality, low resolution, different face, moustache, "
               "beard, stubble, hair on head, duplicate face, cropped by frame edge")


def http(method, path, data=None, timeout=60):
    req = urllib.request.Request(a.host + path, data=data, method=method)
    return urllib.request.urlopen(req, timeout=timeout).read()


def log(m): print(json.dumps(m), flush=True)


def preflight():
    oi = json.loads(http("GET", "/object_info"))
    have = set(oi.keys())
    needs = ["UNETLoader", "ModelSamplingAuraFlow", "CLIPLoader", "VAELoader",
             "LoadImage", "FluxKontextImageScale", "TextEncodeQwenImageEditPlus",
             "VAEEncode", "KSampler", "VAEDecode", "SaveImage"]
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
    log({"preflight": "ok", "steps": a.steps, "cfg": a.cfg})


def build(job):
    nid = 1
    def node(name, inputs):
        nonlocal nid
        i = str(nid); nid += 1
        return i, {"class_type": name, "inputs": inputs}
    wf = {}
    unet, n = node("UNETLoader", {"unet_name": UNET, "weight_dtype": "default"}); wf[unet] = n
    msa, n = node("ModelSamplingAuraFlow", {"model": [unet, 0], "shift": SHIFT}); wf[msa] = n
    clip, n = node("CLIPLoader", {"clip_name": CLIP, "type": "qwen_image", "device": "default"}); wf[clip] = n
    vae, n = node("VAELoader", {"vae_name": VAE}); wf[vae] = n
    start, n = node("LoadImage", {"image": job["image1"]}); wf[start] = n
    sc, n = node("FluxKontextImageScale", {"image": [start, 0]}); wf[sc] = n
    pi = {"clip": [clip, 0], "prompt": job["prompt"], "vae": [vae, 0], "image1": [sc, 0]}
    ni = {"clip": [clip, 0], "prompt": job.get("negative", DEFAULT_NEG), "vae": [vae, 0], "image1": [sc, 0]}
    for key, role in (("image2", "image2"), ("image3", "image3")):
        if job.get(key):
            rid, n = node("LoadImage", {"image": job[key]}); wf[rid] = n
            pi[role] = [rid, 0]; ni[role] = [rid, 0]
    pos, n = node("TextEncodeQwenImageEditPlus", pi); wf[pos] = n
    neg, n = node("TextEncodeQwenImageEditPlus", ni); wf[neg] = n
    enc, n = node("VAEEncode", {"pixels": [sc, 0], "vae": [vae, 0]}); wf[enc] = n
    ks, n = node("KSampler", {"model": [msa, 0], "seed": job["seed"], "steps": a.steps,
                              "cfg": a.cfg, "sampler_name": "euler", "scheduler": "simple",
                              "denoise": 1.0, "positive": [pos, 0], "negative": [neg, 0],
                              "latent_image": [enc, 0]}); wf[ks] = n
    dec, n = node("VAEDecode", {"samples": [ks, 0], "vae": [vae, 0]}); wf[dec] = n
    sv, n = node("SaveImage", {"images": [dec, 0], "filename_prefix": job["tag"]}); wf[sv] = n
    return wf


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
            for n in h[pid].get("outputs", {}).values():
                for im in n.get("images", []): imgs.append(im)
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
                log({"tag": job["tag"], "error": "exec error", "detail": json.dumps(h)[:400]}); continue
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
