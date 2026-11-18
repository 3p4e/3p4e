#!/usr/bin/env python3
"""Submit p23_sunder_*.json shot-spec jobfiles to a local ComfyUI as LTX-2.5 I2V.

This is the MISSING submitter found by the 2026-11-18 pre-render review:
- submit_proof.py is a hardcoded single shot, not a batch runner
- submit_i2v_batch.py reads a different project's ComfyUI-graph format

This script reads the Sunder shot-spec format and builds the EXACT graph that
produced the verified proof (768x448, 97f, 8 steps, euler_ancestral, cfg 1.0,
LTXVBaseSampler + optional_cond_indices='0'), parameterized per shot from the
jobfile (resolution, frames, strength, prompt).

Modes:
  --dry-run          validate jobfile + keyframes locally, no ComfyUI (zero cost)
  (default)          talk to ComfyUI at --comfy (run ON the box)

Proof-of-correctness contract (from submit_proof.py + doc 64):
  * scheduler shift keys are RESOLVED FROM /object_info (the 2nd key name has
    been mangled in dumps); never hardcoded
  * every graph input key is validated against /object_info before POST
  * 32-divisible resolution + 8n+1 frames are enforced before submit
"""
import argparse
import json
import os
import random
import shutil
import sys
import time
import urllib.error
import urllib.request

# --- model constants (byte-verified on box 61265703, doc 64 #4/#6) ---
UNET = "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors"
TE = "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors"
VVAE = "ltx-2.5-video-vae-bf16.safetensors"

DEFAULT_NEG = (
    "blurry, low detail, deformed face, extra people, morphing, flicker, "
    "jitter, watermark, text, duplicate, cartoon"
)


def fail(msg):
    print("ERROR:", msg, flush=True)
    sys.exit(1)


def parse_res(res):
    w, h = res.lower().split("x")
    return int(w), int(h)


def load_entries(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "shots" in d:
        return d["shots"], "dict"
    if isinstance(d, list):
        return d, "list"
    fail(f"unknown jobfile shape: {path} (top keys: {list(d) if isinstance(d, dict) else type(d)})")


def validate_entry(e, kf_base):
    """Return list of problems for one entry (empty list = ok)."""
    probs = []
    eid = e.get("id", "<?>")
    try:
        w, h = parse_res(e["resolution"])
        if w % 32 or h % 32:
            probs.append(f"{eid}: resolution {e['resolution']} not 32-divisible")
    except (KeyError, ValueError):
        probs.append(f"{eid}: bad/missing resolution {e.get('resolution')}")
    nf = e.get("frames")
    try:
        if (int(nf) - 1) % 8 != 0:
            probs.append(f"{eid}: frames {nf} violates 8n+1")
    except (TypeError, ValueError):
        probs.append(f"{eid}: bad/missing frames {nf}")
    start = e.get("start")
    if not start:
        probs.append(f"{eid}: missing start keyframe")
    elif kf_base:
        p = os.path.join(kf_base, os.path.basename(start))
        if not os.path.exists(p):
            probs.append(f"{eid}: start keyframe not found at {p}")
    if not e.get("prompt"):
        probs.append(f"{eid}: empty prompt")
    return probs


def build_graph(e, object_info, seed, shift_kwargs):
    """Build the proven LTX-2.5 I2V workflow dict for one shot."""
    w, h = parse_res(e["resolution"])
    nf = int(e["frames"])
    strength = float(e.get("first_frame_strength", 0.8))
    pos = e["prompt"]
    neg = e.get("negative", DEFAULT_NEG)
    kf = os.path.basename(e["start"])
    fps = int(e.get("fps", 24))
    steps = int(e.get("steps", 8))
    cfg = float(e.get("cfg", 1.0))
    prefix = f"ltx25_{e.get('id', 'shot')}"

    # scheduler shift args are resolved against /object_info by the caller
    sched_args = {"steps": steps, "stretch": True, "terminal": 0.1}
    sched_args.update(shift_kwargs)

    g = {
        "1": {"class_type": "LoadImage", "inputs": {"image": kf}},
        "2": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VVAE}},
        "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "ltxv"}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["4", 0]}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["4", 0]}},
        "7": {"class_type": "LTXVConditioning", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "frame_rate": fps}},
        "8": {"class_type": "LTXVScheduler", "inputs": sched_args},
        "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler_ancestral"}},
        "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "11": {"class_type": "LTXVDualCFGGuider", "inputs": {"model": ["2", 0], "positive": ["7", 0], "negative": ["7", 1], "video_cfg": cfg, "audio_cfg": cfg}},
        "12": {"class_type": "LTXVBaseSampler", "inputs": {
            "model": ["2", 0], "vae": ["3", 0], "width": w, "height": h, "num_frames": nf,
            "guider": ["11", 0], "sampler": ["9", 0], "sigmas": ["8", 0], "noise": ["10", 0],
            "optional_cond_images": ["1", 0], "optional_cond_indices": "0", "strength": strength}},
        "13": {"class_type": "LTXVSpatioTemporalTiledVAEDecode", "inputs": {
            "vae": ["3", 0], "latents": ["12", 0], "spatial_tiles": 4, "spatial_overlap": 1,
            "temporal_tile_length": 16, "temporal_overlap": 1, "last_frame_fix": False,
            "working_device": "auto", "working_dtype": "auto"}},
        "14": {"class_type": "CreateVideo", "inputs": {"images": ["13", 0], "fps": fps}},
        "15": {"class_type": "SaveVideo", "inputs": {"video": ["14", 0], "filename_prefix": prefix, "format": "auto"}},
    }

    # validate every input key against live object_info (same as submit_proof.py)
    problems = []
    for nid, node in g.items():
        ct = node["class_type"]
        if ct not in object_info:
            problems.append((nid, ct, "node-missing"))
            continue
        inp = object_info[ct]["input"]
        allowed = set(inp.get("required", {})) | set(inp.get("optional", {}))
        for k in node["inputs"]:
            if k not in allowed:
                problems.append((nid, ct, k))
    if problems:
        # note: LTXVScheduler shift-key check must happen BEFORE we bake them;
        # the caller resolves them against object_info, so a problem here means
        # the resolved key was wrong — surfaced for the operator
        print("VALIDATE_PROBLEMS", json.dumps(problems), flush=True)
    return g


def resolve_scheduler_keys(object_info):
    """Resolve LTXVScheduler's two shift param names from /object_info."""
    sched = object_info["LTXVScheduler"]["input"]["required"]
    shift_keys = [k for k in sched if "shift" in k.lower()]
    if not shift_keys:
        fail("no shift keys found in LTXVScheduler schema")
    max_key = "max_shift" if "max_shift" in shift_keys else shift_keys[0]
    base_key = [k for k in shift_keys if k != max_key][0]
    print(f"SCHED_SHIFT_KEYS max={max_key!r} base={base_key!r}", flush=True)
    return {max_key: 2.05, base_key: 0.95}


def get_object_info(comfy):
    return json.load(urllib.request.urlopen(comfy + "/object_info", timeout=60))


def dry_run(args):
    entries, shape = load_entries(args.jobfile)
    print(f"JOBFILE: {args.jobfile} ({len(entries)} entries)", flush=True)
    all_probs = []
    for e in entries:
        probs = validate_entry(e, args.kf_base)
        tag = "OK  " if not probs else "FAIL"
        print(f"  {tag} {e.get('id','?')}: {e.get('resolution')} {e.get('frames')}f str={e.get('first_frame_strength')} start={e.get('start')}", flush=True)
        for p in probs:
            print(f"       - {p}", flush=True)
        all_probs.extend(probs)
    print(f"DRY_RUN: {'PASS' if not all_probs else f'FAIL ({len(all_probs)} problems)'}", flush=True)
    return 0 if not all_probs else 1


def submit(args):
    entries, shape = load_entries(args.jobfile)
    if args.limit:
        entries = entries[: args.limit]
    info = get_object_info(args.comfy)
    shift_kwargs = resolve_scheduler_keys(info)

    # ensure ComfyUI input dir
    input_dir = os.path.join(args.comfy_input or (args.comfy.replace(":8188", "") + "/input" if False else "/workspace/ComfyUI/input"))
    if args.comfy_input:
        input_dir = args.comfy_input
    os.makedirs(input_dir, exist_ok=True)

    ok = fail_n = 0
    manifest = []
    for i, e in enumerate(entries):
        probs = validate_entry(e, args.kf_base)
        if probs:
            fail_n += 1
            print(f"FAIL {e.get('id')} pre-validation: {probs}", flush=True)
            continue
        kf = os.path.basename(e["start"])
        src = os.path.join(args.kf_base, kf) if args.kf_base else e["start"]
        dst = os.path.join(input_dir, kf)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
        if not os.path.exists(dst):
            fail_n += 1
            print(f"FAIL {e.get('id')} keyframe unavailable at {dst}", flush=True)
            continue
        seed = args.seed + i if args.seed is not None else random.randint(1, 2**31)
        g = build_graph(e, info, seed, shift_kwargs)
        payload = {"prompt": g, "client_id": "a0-sunder-batch"}
        req = urllib.request.Request(
            args.comfy + "/prompt", data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            pid = r.get("prompt_id")
            if pid:
                ok += 1
                print(f"OK   {pid}  {e.get('id')} seed={seed}", flush=True)
                manifest.append({"id": e.get("id"), "prompt_id": pid, "seed": seed, "start": kf})
            else:
                fail_n += 1
                print(f"FAIL {e.get('id')} no prompt_id: {r}", flush=True)
        except urllib.error.HTTPError as ex:
            fail_n += 1
            print(f"FAIL {e.get('id')} HTTP {ex.code}: {ex.read().decode(errors='replace')[:500]}", flush=True)
        except Exception as ex:  # noqa: BLE001
            fail_n += 1
            print(f"FAIL {e.get('id')} {type(ex).__name__}: {ex}", flush=True)
        time.sleep(0.4)

    print(f"\nSUBMITTED ok={ok} fail={fail_n} total={len(entries)}", flush=True)
    if args.manifest:
        json.dump(manifest, open(args.manifest, "w"), indent=2)
        print(f"MANIFEST: {args.manifest}", flush=True)
    return 0 if fail_n == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobfile", required=True)
    ap.add_argument("--dry-run", action="store_true", help="validate locally, no ComfyUI")
    ap.add_argument("--comfy", default="http://127.0.0.1:8188")
    ap.add_argument("--comfy-input", default=None, help="ComfyUI input dir (default /workspace/ComfyUI/input)")
    ap.add_argument("--kf-base", default=None, help="dir containing start keyframes (local or box)")
    ap.add_argument("--limit", type=int, default=None, help="submit only first N shots")
    ap.add_argument("--seed", type=int, default=None, help="base seed (incremented per shot)")
    ap.add_argument("--manifest", default=None, help="write prompt_id manifest JSON")
    args = ap.parse_args()
    sys.exit(dry_run(args) if args.dry_run else submit(args))


if __name__ == "__main__":
    main()
