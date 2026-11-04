#!/usr/bin/env python3
"""Rent exactly one GPU for the SkyReels-V2 Diffusion-Forcing long-video test.

Mirrors rent_sr.py's proven body (a bogus image/runtype made an earlier attempt hang
without renting, so this copies the known-good shape rather than inventing one).

V2 DF-1.3B-540P is small: 24GB VRAM and 60GB disk are ample. Refuses to double-rent
and refuses an offer above MAXPRICE. Files are pushed over SSH after boot.
Env: VASTAI_API (never printed).
"""
import json, os, sys, time, urllib.request, urllib.error

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
API = "https://console.vast.ai/api/v0"

LABEL    = os.environ.get("LABEL", "skyreels-v2-df")
MAXPRICE = float(os.environ.get("MAXPRICE", "0.45"))
MINVRAM  = int(os.environ.get("MINVRAM", "24000"))   # 1.3B @540P needs ~16-20GB
DISK     = int(os.environ.get("DISK", "80"))
TARGET   = os.environ.get("TARGET_ID")                 # pin an exact offer if set
TEMPLATE = os.environ.get("TEMPLATE", "pytorch/pytorch:2.8.0-cuda12.8-cudnn9-devel")
OUTJSON  = "/a0/usr/projects/vast/.v2_instance.json"


def req(m, p, b=None):
    r = urllib.request.Request(API + p,
                               data=json.dumps(b).encode() if b is not None else None,
                               headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())
    except urllib.error.HTTPError as e:
        return {"http": e.code, "body": e.read().decode()[:500]}


credit = req("GET", "/users/current/")["credit"]
insts  = req("GET", "/instances/").get("instances", [])
_DONE = ("exited", "error", "stopped", "destroyed")
active = [z for z in insts if z.get("actual_status") not in _DONE]
print(f"credit ${credit:.4f} | instances {len(insts)} (active {len(active)})")
if active:
    for z in active:
        print("  RUNNING:", z.get("id"), z.get("gpu_name"), z.get("label"), z.get("actual_status"))
    sys.exit("refusing: live instances running - clean up first")

if TARGET:
    print(f"pinned offer {TARGET}")
    offers = req("POST", "/bundles/", {
        "num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
        "type": "ondemand", "limit": 400, "order": [["dph_total", "asc"]]}).get("offers", [])
    match = [o for o in offers if str(o.get("id")) == str(TARGET)]
    if not match:
        sys.exit(f"pinned offer {TARGET} not in current rentable list")
    pick = match[0]
else:
    q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
         "verified": {"eq": True}, "gpu_ram": {"gte": MINVRAM}, "disk_space": {"gte": DISK},
         "reliability2": {"gte": 0.97}, "type": "ondemand", "limit": 400,
         "inet_down": {"gte": 500}, "order": [["dph_total", "asc"]]}
    offers = req("POST", "/bundles/", q).get("offers", [])
    # Ampere or newer: bf16 accumulators matter for the DiT, and pinning a single
    # offer id is fragile (offers churn out of the market between probe and rent).
    GOOD = os.environ.get("GPU_OK",
        "RTX 3090,RTX 4090,RTX A5000,RTX A6000,A100,A100 SXM,A100 PCIE,L40S,L40,RTX 5090,RTX 5080"
    ).split(",")
    ok = [o for o in offers if o["dph_total"] <= MAXPRICE
          and any(g.strip() in o["gpu_name"] for g in GOOD)]
    # avoid unpredictable CN connectivity, then cheapest
    ok.sort(key=lambda o: (1 if ("China" in (o.get("geolocation") or "")
                                or (o.get("geolocation") or "").strip().endswith("CN")) else 0,
                           o["dph_total"]))
    print(f"offers {len(offers)} | <=${MAXPRICE:.2f}/h and >={MINVRAM}MB: {len(ok)}")
    for o in ok[:8]:
        print(f"  {o['id']:>10} {o['gpu_name']:14} {o['gpu_ram']/1024:3.0f}GB "
              f"${o['dph_total']:.3f}/h down={int(o.get('inet_down') or 0):>5}Mbps "
              f"{o.get('geolocation')} rel={o.get('reliability2'):.3f}")
    if not ok:
        sys.exit("no offer under cap")
    pick = ok[0]

if pick["dph_total"] > MAXPRICE:
    sys.exit(f"refusing: ${pick['dph_total']:.3f}/h above cap ${MAXPRICE:.2f}")
print(f"PICK {pick['id']} {pick['gpu_name']} {pick['gpu_ram']/1024:.0f}GB "
      f"${pick['dph_total']:.3f}/h down={int(pick.get('inet_down') or 0)}Mbps "
      f"{pick.get('geolocation')}")

PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "exec > /var/log/onstart.log 2>&1\n"
    "set -x\n"
    "mkdir -p /root/.ssh /workspace/out\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    "if ! command -v sshd >/dev/null 2>&1 && [ ! -x /usr/sbin/sshd ]; then\n"
    "  apt-get update -qq && apt-get install -y -qq openssh-server >/dev/null 2>&1\n"
    "fi\n"
    "mkdir -p /run/sshd /var/run/sshd\n"
    "sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "grep -q '^Port 22' /etc/ssh/sshd_config || echo 'Port 22' >> /etc/ssh/sshd_config\n"
    "/usr/sbin/sshd -D -e &\n"
    "sleep 2\n"
    "echo ONSTART_DONE\n"
)

body = {"client_id": "me", "image": TEMPLATE, "disk": DISK,
        "onstart": onstart, "label": LABEL, "runtype": "ssh_direc ssh_proxy",
        "target_state": "running"}
r = req("PUT", f"/asks/{pick['id']}/", body)
print("rent response:", json.dumps(r)[:400])
cid = r.get("new_contract")
if not cid:
    sys.exit("rental failed - no new_contract")
print(f"CONTRACT {cid}")
json.dump({"id": cid, "label": LABEL, "dph": pick["dph_total"],
           "gpu": pick["gpu_name"], "started": time.time()},
          open(OUTJSON, "w"), indent=2)
print("saved", OUTJSON)
