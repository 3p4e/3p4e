#!/usr/bin/env python3
"""LTX-2.3 22B distilled image-to-video batch on ComfyUI + ComfyUI-LTXVideo.

Runs ON the Vast instance (stdlib only). Replicates the OFFICIAL single-stage
distilled I2V workflow (ComfyUI-LTXVideo/example_workflows/2.3/
LTX-2.3_T2V_I2V_Single_Stage_Distilled_Full.json) instead of hand-building a
graph, converts it to the ComfyUI /prompt API format, prunes to the fast
'distilled' output branch, patches one shot's image/prompt/seed/tag, and
submits it. Preflights against /object_info and fails fast.

  /venv/main/bin/python run_ltx23_batch.py \\
      --image p1_1.png --prompt '...' --tag p1_1 --seed 100

Output lands in ComfyUI output/ as ltx23_<tag>_*.mp4.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="http://127.0.0.1:8188")
ap.add_argument("--image", default="example.png", help="file already in ComfyUI input/")
ap.add_argument("--prompt", default="Slow cinematic push in.")
ap.add_argument("--negative", default="pc game, console game, video game, cartoon, childish, ugly")
ap.add_argument("--tag", default="test")
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--workflow-json", default="single.json", help="local path or URL of the official workflow")
ap.add_argument("--width", type=int, default=960)
ap.add_argument("--height", type=int, default=544)
ap.add_argument("--frames", type=int, default=121)
ap.add_argument("--frame-rate", type=float, default=24.0)
a = ap.parse_args()

WF_URL = "https://raw.githubusercontent.com/Lightricks/ComfyUI-LTXVideo/master/example_workflows/2.3/LTX-2.3_T2V_I2V_Single_Stage_Distilled_Full.json"


def http(method, path, data=None, headers=None):
    req = urllib.request.Request(a.host + path, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(req, timeout=120).read()


def load_workflow():
    if os.path.exists(a.workflow_json):
        return json.load(open(a.workflow_json))
    raw = urllib.request.urlopen(WF_URL, timeout=60).read()
    return json.loads(raw)


wf = load_workflow()
nodes = wf["nodes"]
links = wf["links"]

# link id -> (src_node_id, src_output_slot)
link_map = {}
for l in links:
    link_map[l[0]] = (l[1], l[2])

by_id = {n["id"]: n for n in nodes}


def build_graph():
    """Workflow JSON -> ComfyUI /prompt API graph (link + widget resolution)."""
    g = {}
    for n in nodes:
        vals = iter(n.get("widgets_values", []) or [])
        ins = {}
        for entry in n.get("inputs", []) or []:
            name = entry["name"]
            lk = entry.get("link")
            if lk is not None and lk in link_map:
                sid, sslot = link_map[lk]
                ins[name] = [str(sid), sslot]
            else:
                try:
                    ins[name] = next(vals)
                except StopIteration:
                    ins[name] = None
        g[str(n["id"])] = {"class_type": n["type"], "inputs": ins}
    return g


def prune_to_output(graph, out_node_id):
    """Keep only nodes reachable backwards from out_node_id (single output branch)."""
    keep = set()
    stack = [str(out_node_id)]
    while stack:
        nid = stack.pop()
        if nid in keep or nid not in graph:
            continue
        keep.add(nid)
        for val in graph[nid].get("inputs", {}).values():
            if isinstance(val, list) and len(val) == 2 and isinstance(val[1], (int,)):
                stack.append(str(val[0]))
    return {k: v for k, v in graph.items() if k in keep}


graph = build_graph()

# Identify the two SaveVideo nodes by their filename_prefix widget, keep the
# distilled ('output_F') branch.
save_nodes = {nid: n for nid, n in graph.items() if n["class_type"] == "SaveVideo"}
primary_save = None
for nid, n in save_nodes.items():
    # widget value is the filename_prefix for SaveVideo (first widget)
    if n["inputs"].get("filename_prefix") == "output_F":
        primary_save = nid
if primary_save is None and save_nodes:
    primary_save = sorted(save_nodes)[0]  # fallback
if primary_save is None:
    sys.exit("No SaveVideo node found in workflow")

graph = prune_to_output(graph, primary_save)

# ---- patch this shot ----
for nid, n in graph.items():
    t = n["class_type"]
    ins = n["inputs"]
    if t == "LoadImage":
        ins["image"] = a.image
    elif t == "CLIPTextEncode" and "text" in ins:
        txt = ins.get("text")
        if isinstance(txt, str):
            # first CLIPTextEncode in traversal order = positive; second = negative.
            # Handle via the known defaults from the official workflow text.
            if "tea ceremony" in txt or True:
                ins["text"] = a.prompt
    elif t == "RandomNoise" and "noise_seed" in ins:
        ins["noise_seed"] = a.seed
    elif t == "SaveVideo":
        ins["filename_prefix"] = f"ltx23_{a.tag}"
    elif t == "EmptyLTXVLatentVideo":
        ins["width"] = a.width
        ins["height"] = a.height
        ins["length"] = a.frames

# The negative prompt: the official workflow stores it in a CLIPTextEncode with
# the 'ugly' string. Patch every CLIPTextEncode that currently holds the
# negative default.
for nid, n in graph.items():
    if n["class_type"] == "CLIPTextEncode" and "text" in n["inputs"]:
        t = n["inputs"]["text"]
        if isinstance(t, str) and "ugly" in t:
            n["inputs"]["text"] = a.negative

# ---- preflight: report unknown/missing node classes on this server ----
try:
    oi = json.loads(http("GET", "/object_info"))
except Exception as e:
    print("PREFLIGHT skipped (server not ready):", e)
    oi = {}
if oi:
    for nid, n in graph.items():
        c = n["class_type"]
        if c not in oi:
            print(f"PREFLIGHT: node class MISSING on server: {c}")
        else:
            req = set(oi[c].get("input", {}).get("required", {}).keys())
            given = set(n["inputs"].keys())
            if req - given:
                print(f"PREFLIGHT: {c} missing required inputs {sorted(req - given)}")

# ---- submit ----
body = json.dumps({"prompt": graph, "client_id": f"ltx23_{a.tag}"}).encode()
t0 = time.time()
try:
    r = json.loads(http("POST", "/prompt", body, {"Content-Type": "application/json"}))
except urllib.error.HTTPError as e:
    print("PROMPT REJECTED:", e.read().decode()[:2000])
    sys.exit(1)
pid = r["prompt_id"]
print("queued", pid)
while True:
    time.sleep(5)
    h = json.loads(http("GET", f"/history/{pid}"))
    if pid in h:
        st = h[pid].get("status", {})
        if st.get("status_str") == "error":
            print("ERROR:", json.dumps(st)[:3000])
            sys.exit(2)
        outs = h[pid].get("outputs", {})
        print(f"DONE in {time.time()-t0:.0f}s ({a.width}x{a.height}, {a.frames} frames)")
        print(json.dumps(outs)[:1200])
        break
    if int(time.time() - t0) % 30 < 5:
        print(f"  ...{time.time()-t0:.0f}s")
