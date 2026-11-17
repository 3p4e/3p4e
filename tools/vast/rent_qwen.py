#!/usr/bin/env python3
"""Rent ONE native-FP8 GPU for Qwen-Image-Edit-2511 keyframes.

WHY AN ALLOWLIST: Turing/Ampere (SM < 8.9) have no fp8 storage, so the 20.5 GB
fp8mixed checkpoint upcasts to ~41 GB fp16 and the 9.4 GB text encoder to ~19 GB
=> ~60 GB, which OOMs a 48 GB card. Only Ada (SM 8.9) / Blackwell hold fp8 natively.

NO self-stop watchdog: the director asked to keep the instance for follow-on runs.
Refuses to double-rent. Refuses if the offer is gone or above cap.
"""
import json, os, sys, time, urllib.request, urllib.error

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
LABEL = os.environ.get("LABEL", "paladin-qwen")
MAXPRICE = float(os.environ.get("MAXPRICE", "0.65"))
CAPUSD = float(os.environ.get("CAPUSD", "0.50"))
ESTMIN = float(os.environ.get("ESTMIN", "25"))
MINVRAM = int(os.environ.get("MINVRAM", "44000"))
DISK = int(os.environ.get("DISK", "120"))
TARGET_ID = os.environ.get("TARGET_ID", "58502697")
TEMPLATE = os.environ.get("TEMPLATE", "2188dfd3e0a0b83691bb468ddae0a4e5")

FP8_OK = ("4090", "6000Ada", "6000 Ada", "L40S", "L40 ", "L40", "PRO 5000",
          "PRO 6000", "B200", "RTX 5090", "RTX 5080")


def req(m, p, b=None):
    r = urllib.request.Request("https://console.vast.ai/api/v0" + p,
                               data=json.dumps(b).encode() if b is not None else None,
                               headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())
    except urllib.error.HTTPError as e:
        return {"http": e.code, "body": e.read().decode()[:400]}


credit = req("GET", "/users/current/")["credit"]
insts = req("GET", "/instances/").get("instances", [])
_DONE = ("exited", "error", "stopped", "destroyed")
active = [z for z in insts if z.get("actual_status") not in _DONE]
print(f"credit ${credit:.4f} | instances {len(insts)} (active {len(active)})")
for z in active:
    print("  RUNNING:", z.get("id"), z.get("gpu_name"), z.get("label"), z.get("actual_status"))
if any(z.get("label") == LABEL for z in active):
    sys.exit(f"refusing: {LABEL} already running")
if active:
    sys.exit("refusing: instances running - clean up first")

q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
     "verified": {"eq": True}, "gpu_ram": {"gte": MINVRAM}, "disk_space": {"gte": DISK},
     "reliability2": {"gte": 0.98}, "type": "ondemand", "limit": 400,
     "order": [["dph_total", "asc"]]}
offers = req("POST", "/bundles/", q).get("offers", [])
ada = [o for o in offers if any(k in o["gpu_name"] for k in FP8_OK)
       and int(o.get("inet_down") or 0) >= 1500 and o["dph_total"] <= MAXPRICE]
# prefer non-China hosts, then cheapest: CN connectivity is the least predictable
ada.sort(key=lambda o: (1 if ("China" in (o.get("geolocation") or "") or (o.get("geolocation") or "").strip().endswith("CN")) else 0, o["dph_total"]))
print(f"offers {len(offers)} | native-FP8 + fast-net + <=${MAXPRICE}: {len(ada)}")
for o in ada[:8]:
    print(f"  {o['id']:>10} {o['gpu_name']:14} {o['gpu_ram']/1024:3.0f}GB ${o['dph_total']:.3f}/h "
          f"down={int(o.get('inet_down') or 0):>5}Mbps {o.get('geolocation')} rel={o.get('reliability2'):.3f}")

pick = None
if TARGET_ID:
    pick = next((o for o in offers if str(o["id"]) == str(TARGET_ID)), None)
    if pick is None:
        sys.exit(f"TARGET_ID {TARGET_ID} gone")
    if not any(k in pick["gpu_name"] for k in FP8_OK):
        sys.exit(f"refusing: {pick['gpu_name']} has no native fp8")
if pick is None:
    if not ada:
        sys.exit("refusing: no native-fp8 offer under cap")
    pick = ada[0]

est = pick["dph_total"] * ESTMIN / 60.0
print(f"PICK {pick['id']} {pick['gpu_name']} {pick['gpu_ram']/1024:.0f}GB ${pick['dph_total']:.3f}/h "
      f"down={int(pick.get('inet_down') or 0)}Mbps {pick.get('geolocation')} | est {ESTMIN:.0f}min = ${est:.3f}")
if est > CAPUSD:
    sys.exit(f"refusing: est ${est:.2f} above cap ${CAPUSD:.2f}")

PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "exec > /var/log/onstart.log 2>&1\n"
    "set -x\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/in\n"
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
    "ss -ltnp 2>/dev/null | grep 22 || netstat -ltnp 2>/dev/null | grep 22\n"
    "echo ONSTART_DONE\n"
)

body = {"client_id": "me", "template_hash_id": TEMPLATE, "disk": DISK,
        "onstart": onstart, "label": LABEL, "runtype": "ssh_direc ssh_proxy",
        "target_state": "running"}
r = req("PUT", f"/asks/{pick['id']}/", body)
print("rent:", json.dumps(r)[:300])
cid = r.get("new_contract")
if not cid:
    sys.exit("rental failed")
print(f"CONTRACT {cid}  ({pick['gpu_name']} @ ${pick['dph_total']:.3f}/h)  KEEPING ALIVE")
json.dump({"id": cid, "label": LABEL, "dph": pick["dph_total"], "gpu": pick["gpu_name"],
           "started": time.time(), "keep_alive": True},
          open("/a0/usr/projects/vast/.qwen_instance.json", "w"), indent=2)
print("saved .qwen_instance.json")
