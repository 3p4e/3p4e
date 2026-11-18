import json, os, shutil, random, time, urllib.request

BASE = "http://127.0.0.1:8188"
info = json.load(urllib.request.urlopen(BASE + "/object_info", timeout=60))

UNET = "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors"
TE = "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors"
VVAE = "ltx-2.5-video-vae-bf16.safetensors"

# copy first keyframe into ComfyUI input dir
src = "/workspace/stills/kf_01_start.png"
dst = "/workspace/ComfyUI/input/kf_01_start.png"
if os.path.exists(src) and not os.path.exists(dst):
    shutil.copy(src, dst)
print("KF_INPUT_EXISTS", os.path.exists(dst), flush=True)

# resolve the exact LTXVScheduler shift-parameter names (the 2nd shift key is mangled in dumps)
sched_keys = list(info["LTXVScheduler"]["input"]["required"].keys())
shift_keys = [k for k in sched_keys if "shift" in k.lower()]
max_shift_key = "max_shift" if "max_shift" in sched_keys else shift_keys[0]
base_shift_key = [k for k in shift_keys if k != max_shift_key][0]
print("SCHED_KEYS", sched_keys, "MAX", max_shift_key, "BASE", base_shift_key, flush=True)

seed = random.randint(1, 2**31)
POS = ("The armored paladin stands ready in the cavern, then slowly raises his sword "
       "as blue embers ignite along the blade; the camera pushes in steadily and settles "
       "on a close-up of his helmed face.")
NEG = "blurry, low detail, deformed face, extra people, morphing, flicker, jitter, watermark, text, duplicate, cartoon"

wf = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "kf_01_start.png"}},
    "2": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": VVAE}},
    "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "ltxv"}},
    "5": {"class_type": "CLIPTextEncode", "inputs": {"text": POS, "clip": ["4", 0]}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["4", 0]}},
    "7": {"class_type": "LTXVConditioning", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "frame_rate": 24}},
    "8": {"class_type": "LTXVScheduler", "inputs": {"steps": 8, max_shift_key: 2.05, base_shift_key: 0.95, "stretch": True, "terminal": 0.1}},
    "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler_ancestral"}},
    "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
    "11": {"class_type": "LTXVDualCFGGuider", "inputs": {"model": ["2", 0], "positive": ["7", 0], "negative": ["7", 1], "video_cfg": 1.0, "audio_cfg": 1.0}},
    "12": {"class_type": "LTXVBaseSampler", "inputs": {
        "model": ["2", 0], "vae": ["3", 0], "width": 768, "height": 448, "num_frames": 97,
        "guider": ["11", 0], "sampler": ["9", 0], "sigmas": ["8", 0], "noise": ["10", 0],
        "optional_cond_images": ["1", 0], "optional_cond_indices": "0", "strength": 0.8}},
    "13": {"class_type": "LTXVSpatioTemporalTiledVAEDecode", "inputs": {
        "vae": ["3", 0], "latents": ["12", 0], "spatial_tiles": 4, "spatial_overlap": 1,
        "temporal_tile_length": 16, "temporal_overlap": 1, "last_frame_fix": False,
        "working_device": "auto", "working_dtype": "auto"}},
    "14": {"class_type": "CreateVideo", "inputs": {"images": ["13", 0], "fps": 24}},
    "15": {"class_type": "SaveVideo", "inputs": {"video": ["14", 0], "filename_prefix": "ltx25_proof_s01", "format": "auto"}},
}

# validate every input key against live object_info
problems = []
for nid, node in wf.items():
    inp = info[node["class_type"]]["input"]
    allowed = set(inp.get("required", {})) | set(inp.get("optional", {}))
    for k in node["inputs"]:
        if k not in allowed:
            problems.append((nid, node["class_type"], k, sorted(allowed)))
if problems:
    print("VALIDATE_PROBLEMS", json.dumps(problems, indent=1), flush=True)
else:
    print("VALIDATE_OK", flush=True)

payload = {"prompt": wf, "client_id": "a0-proof-1"}
req = urllib.request.Request(BASE + "/prompt", data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"}, method="POST")
try:
    r = json.load(urllib.request.urlopen(req, timeout=120))
    print("SUBMIT", json.dumps(r), flush=True)
    pid = r.get("prompt_id")
except urllib.error.HTTPError as e:
    print("SUBMIT_ERR", e.code, e.read().decode()[:2500], flush=True)
    raise SystemExit(1)

# poll history briefly
for i in range(12):
    time.sleep(10)
    try:
        h = json.load(urllib.request.urlopen(BASE + "/history/" + pid, timeout=30))
    except Exception as ex:
        print("HIST_ERR", str(ex), flush=True); continue
    if pid in h:
        rec = h[pid]
        st = rec.get("status", {})
        print("POLL", i, "status=", json.dumps(st)[:300], flush=True)
        if st.get("completed") or st.get("status_str") == "error":
            outs = rec.get("outputs", {})
            for nid, o in outs.items():
                if "gifs" in o or "videos" in o:
                    print("OUTPUT", nid, json.dumps(o)[:500], flush=True)
            break
    else:
        print("POLL", i, "no-entry", flush=True)
print("DONE", flush=True)
