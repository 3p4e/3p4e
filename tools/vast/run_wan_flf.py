#!/usr/bin/env python3
"""Render first-last-frame clips with Wan2.1-FLF2V-14B-720P on ComfyUI.

Node contract verified against ComfyUI comfy_extras/nodes_wan.py:
  WanFirstLastFrameToVideo(positive, negative, vae, width, height, length,
                           batch_size, start_image, end_image)
  -> (positive, negative, latent)

length must be 81 (4n+1) for the 720P FLF model. The node pins the first and
last latent frames from the supplied stills, which is exactly the FLF
construction the production doctrine requires.

Usage:
  python3 run_wan_flf.py --jobs bossfight_flf_jobs.json --stills-dir kf --out clips
  python3 run_wan_flf.py --jobs ... --only bf_19 --dry-run
"""
import argparse, json, os, sys, time, urllib.request

SERVER = os.environ.get("COMFY", "http://127.0.0.1:8188")
LENGTH = 81          # 4n+1, fixed for Wan 720P FLF
FPS = 16

def post(path, payload):
    req = urllib.request.Request(
        f"{SERVER}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def get(path):
    with urllib.request.urlopen(f"{SERVER}{path}", timeout=60) as r:
        return json.load(r)

def build_graph(job, start_img, end_img):
    """Minimal Wan FLF graph: two stills -> one 81-frame clip."""
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "wan2.1_flf2v_720p_14B_fp16.safetensors",
            "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "umt5_xxl_fp16.safetensors", "type": "wan"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["2", 0], "text": job["prompt"]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["2", 0], "text": job.get("negative_prompt", "")}},
        "6": {"class_type": "LoadImage", "inputs": {"image": start_img}},
        "7": {"class_type": "LoadImage", "inputs": {"image": end_img}},
        "8": {"class_type": "WanFirstLastFrameToVideo", "inputs": {
            "positive": ["4", 0], "negative": ["5", 0], "vae": ["3", 0],
            "width": job.get("width", 1280), "height": job.get("height", 720),
            "length": LENGTH, "batch_size": 1,
            "start_image": ["6", 0], "end_image": ["7", 0]}},
        "9": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "positive": ["8", 0], "negative": ["8", 1],
            "latent_image": ["8", 2], "seed": job.get("seed", 42),
            "steps": job.get("steps", 40), "cfg": 5.0,
            "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
        "11": {"class_type": "CreateVideo", "inputs": {
            "images": ["10", 0], "fps": FPS}},
        "12": {"class_type": "SaveVideo", "inputs": {
            "video": ["11", 0],
            "filename_prefix": f"flf_{job['id']}",
            "format": "mp4", "codec": "h264"}},
    }

def wait_for(prompt_id, timeout=5400):
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = get(f"/history/{prompt_id}")
        if prompt_id in h:
            return h[prompt_id]
        time.sleep(15)
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--stills-dir", default="kf")
    ap.add_argument("--out", default="clips")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    data = json.load(open(a.jobs))
    jobs = data["jobs"]
    if a.only:
        jobs = [j for j in jobs if j["id"].startswith(a.only)]
    jobs = [j for j in jobs if j["phase"] == "start"]

    missing = []
    for j in jobs:
        sid = j["shot"]
        s = os.path.join(a.stills_dir, f"bf_{sid:02d}_start.png")
        e = os.path.join(a.stills_dir, f"bf_{sid:02d}_end.png")
        if not (os.path.exists(s) and os.path.exists(e)):
            missing.append((j["id"], s, e))

    print(f"model      {data['model']}  ({data['license']})")
    print(f"clips      {len(jobs)}")
    print(f"length     {LENGTH} frames @ {FPS} fps = {LENGTH/FPS:.2f} s each")
    print(f"total      {len(jobs)*LENGTH/FPS:.1f} s of film")
    print(f"stills dir {a.stills_dir}")
    print(f"missing    {len(missing)} still pairs")
    for m in missing[:8]:
        print(f"   {m[0]}: {os.path.basename(m[1])} / {os.path.basename(m[2])}")
    if len(missing) > 8:
        print(f"   ... and {len(missing)-8} more")

    if a.dry_run:
        print("\nDRY RUN OK")
        return 0
    if missing:
        print("\nREFUSING: render the missing keyframes first")
        return 1

    os.makedirs(a.out, exist_ok=True)
    ok = fail = 0
    t0 = time.time()
    for n, j in enumerate(jobs, 1):
        sid = j["shot"]
        s = f"bf_{sid:02d}_start.png"
        e = f"bf_{sid:02d}_end.png"
        print(f"\n[{n}/{len(jobs)}] {j['id']}  {time.time()-t0:.0f}s elapsed", flush=True)
        try:
            r = post("/prompt", {"prompt": build_graph(j, s, e)})
            pid = r.get("prompt_id")
            print(f"   queued {pid}", flush=True)
            hist = wait_for(pid)
            if hist is None:
                print("   TIMEOUT", flush=True); fail += 1; continue
            st = hist.get("status", {})
            if st.get("status_str") != "success":
                print(f"   FAILED {st}", flush=True); fail += 1; continue
            print("   done", flush=True); ok += 1
        except Exception as ex:
            print(f"   ERROR {type(ex).__name__} {ex}", flush=True); fail += 1

    print(f"\nALL_DONE ok={ok} fail={fail} elapsed={time.time()-t0:.0f}s")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
