#!/usr/bin/env python3
"""Runs the v3 jobs through ComfyUI LTX-2.5 (distilled, 8 steps, CFG 1) with START + END keyframes.
usage: batch.py [--only id1,id2] ; resume-safe: skips ids whose /workspace/out/<id>.mp4 exists."""
import json, os, shutil, sys, time, urllib.request, glob
BASE = "http://127.0.0.1:8188"; B = "/workspace/v3bundle"; OUT = "/workspace/out"; os.makedirs(OUT, exist_ok=True)
cfg = json.load(open(f"{B}/jobs.json")); jobs = cfg["jobs"]
if "--only" in sys.argv: keep = set(sys.argv[sys.argv.index("--only") + 1].split(",")); jobs = [j for j in jobs if j["id"] in keep]
info = json.load(urllib.request.urlopen(BASE + "/object_info", timeout=120))
sk = list(info["LTXVScheduler"]["input"]["required"].keys()); sh = [k for k in sk if "shift" in k.lower()]
MAXK = "max_shift" if "max_shift" in sk else sh[0]; BASEK = [k for k in sh if k != MAXK][0]
UNET = "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors"
TE = "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors"; VVAE = "ltx-2.5-video-vae-bf16.safetensors"
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def graph(j):
    for k in ("start", "end"): shutil.copy(f"{B}/kf/{j[k]}", f"/workspace/ComfyUI/input/{j[k]}")
    return {
     "1": {"class_type": "LoadImage", "inputs": {"image": j["start"]}},
     "1b": {"class_type": "LoadImage", "inputs": {"image": j["end"]}},
     "1c": {"class_type": "ImageBatch", "inputs": {"image1": ["1", 0], "image2": ["1b", 0]}},
     "2": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
     "3": {"class_type": "VAELoader", "inputs": {"vae_name": VVAE}},
     "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "ltxv"}},
     "5": {"class_type": "CLIPTextEncode", "inputs": {"text": j["prompt"], "clip": ["4", 0]}},
     "6": {"class_type": "CLIPTextEncode", "inputs": {"text": cfg["negative"], "clip": ["4", 0]}},
     "7": {"class_type": "LTXVConditioning", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "frame_rate": cfg["fps"]}},
     "8": {"class_type": "LTXVScheduler", "inputs": {"steps": cfg["steps"], MAXK: 2.05, BASEK: 0.95, "stretch": True, "terminal": 0.1}},
     "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler_ancestral"}},
     "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": j["seed"]}},
     "11": {"class_type": "LTXVDualCFGGuider", "inputs": {"model": ["2", 0], "positive": ["7", 0], "negative": ["7", 1], "video_cfg": cfg["cfg"], "audio_cfg": 1.0}},
     "12": {"class_type": "LTXVBaseSampler", "inputs": {"model": ["2", 0], "vae": ["3", 0], "width": j["w"], "height": j["h"], "num_frames": j["frames"],
            "guider": ["11", 0], "sampler": ["9", 0], "sigmas": ["8", 0], "noise": ["10", 0],
            "optional_cond_images": ["1c", 0], "optional_cond_indices": f"0,{j['frames'] - 1}", "strength": cfg["strength"]}},
     "13": {"class_type": "LTXVSpatioTemporalTiledVAEDecode", "inputs": {"vae": ["3", 0], "latents": ["12", 0], "spatial_tiles": 4, "spatial_overlap": 1,
            "temporal_tile_length": 16, "temporal_overlap": 1, "last_frame_fix": False, "working_device": "auto", "working_dtype": "auto"}},
     "14": {"class_type": "CreateVideo", "inputs": {"images": ["13", 0], "fps": cfg["fps"]}},
     "15": {"class_type": "SaveVideo", "inputs": {"video": ["14", 0], "filename_prefix": "v3_" + j["id"], "format": "auto"}}}
first = True
LOOP = "--loop" in sys.argv   # keep rendering jobs as their keyframes arrive, until /workspace/v3bundle/KF_DONE exists
def ready(j): return all(os.path.exists(f"{B}/kf/{j[k]}") for k in ("start", "end"))
def pending(): return [j for j in jobs if not (os.path.exists(f"{OUT}/{j['id']}.mp4") and os.path.getsize(f"{OUT}/{j['id']}.mp4") > 100000) and j["id"] not in failed]
failed = set()
def next_jobs():
    while True:
        todo = [j for j in pending() if ready(j)]
        if todo: return todo[:1]
        if not LOOP or os.path.exists(f"{B}/KF_DONE") and not [j for j in pending() if ready(j)]: return []
        time.sleep(30)
while True:
  nj = next_jobs()
  if not nj: break
  for j in nj:
    dst = f"{OUT}/{j['id']}.mp4"
    wf = graph(j)
    if first:
        bad = [(n, x["class_type"], k) for n, x in wf.items() for k in x["inputs"]
               if k not in set(info[x["class_type"]]["input"].get("required", {})) | set(info[x["class_type"]]["input"].get("optional", {}))]
        log("VALIDATE", bad or "OK"); first = False
        if bad: sys.exit(2)
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(BASE + "/prompt", data=json.dumps({"prompt": wf}).encode(), headers={"Content-Type": "application/json"}), timeout=120))
    except urllib.error.HTTPError as e:
        log("SUBMIT_ERR", j["id"], e.code, e.read().decode()[:1500]); failed.add(j["id"]); continue
    pid = r["prompt_id"]; done = None
    while time.time() - t0 < 1800:
        time.sleep(8)
        try: h = json.load(urllib.request.urlopen(BASE + "/history/" + pid, timeout=30))
        except Exception: continue
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("completed") or st.get("status_str") == "error": done = h[pid]; break
    if not done or done.get("status", {}).get("status_str") == "error":
        log("FAIL", j["id"], json.dumps((done or {}).get("status", {}))[:1200]); failed.add(j["id"]); continue
    vids = [v for o in done["outputs"].values() for v in (o.get("videos") or o.get("images") or o.get("gifs") or [])]
    src = None
    for v in vids:
        p = os.path.join("/workspace/ComfyUI/output", v.get("subfolder", ""), v["filename"])
        if p.endswith(".mp4") and os.path.exists(p): src = p
    if not src:
        c = sorted(glob.glob(f"/workspace/ComfyUI/output/**/v3_{j['id']}*.mp4", recursive=True)); src = c[-1] if c else None
    if not src: log("NOFILE", j["id"], json.dumps(done["outputs"])[:500]); failed.add(j["id"]); continue
    shutil.move(src, dst); log("OK", j["id"], f"{time.time() - t0:.0f}s", os.path.getsize(dst))
log("BATCH_END")
