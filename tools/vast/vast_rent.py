#!/usr/bin/env python3
"""Search and rent ONE on-demand Vast.ai GPU for the ComfyUI/Wan workflow, then wait until it runs.
Env: VASTAI_API (never printed).  Example:
  python3 vast_rent.py --max-price 0.45 --min-vram 31 --disk 120 --label karsus-wan-batch --skip-tests
Rules learned the hard way: on-demand only (interruptible offers often never start), verified hosts,
>= 48 GB RAM, >= 8 cores, >= 500 Mbps; ids in /bundles/ cannot be filtered, so scan the list.
"""
import argparse, json, os, random, sys, time, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("--max-price", type=float, default=0.45); ap.add_argument("--min-vram", type=int, default=31000)
ap.add_argument("--disk", type=int, default=120); ap.add_argument("--label", default="karsus-wan")
ap.add_argument("--skip-tests", action="store_true", help="models + ComfyUI only (recommended for the batch)")
ap.add_argument("--maxmin", type=int, default=150, help="self-stop after N minutes")
ap.add_argument("--branch", default="claude/elegant-thompson-uqhred"); ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--id", type=int, default=0, help="rent this exact offer id, ignoring the price ranking")
a = ap.parse_args()
K = os.environ["VASTAI_API"]; H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"  # official vastai/comfy template
def req(m, p, b=None):
    r = urllib.request.Request("https://console.vast.ai/api/v0" + p, data=json.dumps(b).encode() if b is not None else None, headers=H, method=m)
    try: return json.load(urllib.request.urlopen(r, timeout=90))
    except urllib.error.HTTPError as e: return {"http": e.code, "body": e.read().decode()[:500]}
print("credit:", round(req("GET", "/users/current/")["credit"], 3), "| instances:", len(req("GET", "/instances/").get("instances", [])))
offers = req("POST", "/bundles/", {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False}, "verified": {"eq": True},
    "gpu_ram": {"gte": a.min_vram}, "disk_space": {"gte": 100}, "reliability2": {"gte": 0.98}, "direct_port_count": {"gte": 1},
    "type": "ondemand", "limit": 300, "order": [["dph_total", "asc"]]}).get("offers", [])
bad = {"Tesla V100", "Q RTX 8000", "CMP 170HX", "Titan RTX", "Tesla P40"}
c = [x for x in offers if x["dph_total"] <= a.max_price and x["gpu_name"] not in bad and x.get("cpu_ram", 0) / 1024 >= 48
     and (x.get("cpu_cores_effective") or 0) >= 8 and x.get("inet_down", 0) >= 500 and x.get("total_flops", 0) >= 50]
if a.id:
    exact = [x for x in offers if x["id"] == a.id]
    if not exact: sys.exit(f"offer {a.id} not in the rentable list right now")
    c = exact
for x in c[:6]:
    print(f"cand id={x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h TF={x['total_flops']:.0f} down={int(x['inet_down'])}Mbps {x['geolocation']}")
if not c or a.dry_run: sys.exit("no candidate" if not c else 0)
# refuse to double-rent: an existing karsus-wan-v3 instance means we already paid
_ex = [z for z in req("GET", "/instances/").get("instances", []) if z.get("label") == a.label]
if _ex and not a.dry_run:
    sys.exit(f"refusing: already have {a.label} -> {[z['id'] for z in _ex]}")
x = c[0]
raw = f"https://raw.githubusercontent.com/3p4e/3p4e/{a.branch}/tools/vast/autorun.sh?c={random.randint(1, 10**9)}"
env = "SKIP_TESTS=1 " if a.skip_tests else ""
onstart = f"#!/bin/bash\nmkdir -p /workspace\nnohup setsid bash -c 'curl -fsSL \"{raw}\" | {env}MAXMIN={a.maxmin} bash' >/workspace/onstart.out 2>&1 &\n"
r = req("PUT", f"/asks/{x['id']}/", {"template_hash_id": TEMPLATE, "disk": a.disk, "label": a.label, "onstart": onstart})
r.pop("instance_api_key", None); print("rent:", r)
if not r.get("success") or not r.get("new_contract"):
    sys.exit(f"RENT FAILED - no contract. response={r}")
cid = r.get("new_contract")
for _ in range(12):
    time.sleep(10)
    y = [z for z in req("GET", "/instances/").get("instances", []) if z["id"] == cid]; y = y[0] if y else {}
    print(y.get("actual_status"), y.get("status_msg"))
    if y.get("actual_status") == "running":
        print(json.dumps({"id": cid, "ip": y["public_ipaddr"], "ssh_direct_port": y["ports"]["22/tcp"][0]["HostPort"], "ssh_proxy": f"{y['ssh_host']}:{y['ssh_port']}", "dph": round(y["dph_total"], 3)})); break
