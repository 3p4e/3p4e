#!/usr/bin/env python3
"""Rent exactly one 48GB-class GPU for the Fenrir P7 proof (LTX-2.3 22B distilled, S10).
Adapted from the proven rent_k6.py pattern. Refuses to double-rent by label."""
import json, os, sys, urllib.request, urllib.error

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"  # pytorch template (proven on k6/ltx23 runs)
LABEL = os.environ.get("LABEL", "fenrir-p7")
MAXPRICE = float(os.environ.get("MAXPRICE", "0.60"))
MINVRAM = int(os.environ.get("MINVRAM", "44000"))
DISK = int(os.environ.get("DISK", "160"))


def req(m, p, b=None):
    r = urllib.request.Request("https://console.vast.ai/api/v0" + p,
                               data=json.dumps(b).encode() if b is not None else None,
                               headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())
    except urllib.error.HTTPError as e:
        return {"http": e.code, "body": e.read().decode()[:500]}


credit = req("GET", "/users/current/")["credit"]
insts = req("GET", "/instances/").get("instances", [])
print(f"credit ${credit:.3f} | instances {len(insts)}")
if any(z.get("label") == LABEL for z in insts):
    sys.exit(f"refusing: label {LABEL} already exists -> {[z['id'] for z in insts if z.get('label')==LABEL]}")

q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
     "verified": {"eq": True}, "gpu_ram": {"gte": MINVRAM}, "disk_space": {"gte": DISK},
     "reliability2": {"gte": 0.95}, "type": "ondemand", "limit": 300,
     "order": [["dph_total", "asc"]]}
offers = req("POST", "/bundles/", q).get("offers", [])
BROKEN_HOSTS = {"32.196.117.67", "3.87.100.167", "23.158.136.85", "32.200.23.213", "54.82.210.84"}
bad = {"Tesla V100", "Q RTX 8000", "CMP 170HX", "Titan RTX", "Tesla P40", "Tesla P100"}
c = [x for x in offers
     if x["dph_total"] <= MAXPRICE and x["gpu_name"] not in bad
     and (x.get("cpu_ram") or 0) / 1024 >= 32
     and (x.get("cpu_cores_effective") or 0) >= 8
     and (x.get("inet_down") or 0) >= 2000
     and (x.get("total_flops") or 0) >= 30
     and str(x.get("ssh_host") or x.get("public_ipaddr") or "") not in BROKEN_HOSTS]
for x in c[:6]:
    print(f"cand {x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h "
          f"rel={x.get('reliability2'):.2f} down={int(x.get('inet_down') or 0)}Mbps {x.get('geolocation')}")
if not c:
    sys.exit("no candidate offer matched")

x = c[0]
PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
PUB2 = open("/root/.ssh/vast_rsa.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/hf\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
    f"echo '{PUB2}' >> /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    "echo BOOT_OK > /workspace/BOOT_OK\n"
)

r = req("PUT", f"/asks/{x['id']}/", {"template_hash_id": TEMPLATE, "disk": DISK,
                                     "label": LABEL, "onstart": onstart})
print("rent:", json.dumps(r)[:600])
if "new_contract" not in r:
    sys.exit("rent failed")

import time
time.sleep(25)
insts = req("GET", "/instances/").get("instances", [])
mine = [z for z in insts if z.get("label") == LABEL]
if not mine:
    sys.exit("no instance with label after rent")
z = mine[0]
print("INSTANCE", json.dumps({k: z.get(k) for k in ("id", "label", "status", "ssh_host", "ssh_port", "actual_status")}))
open("/a0/usr/projects/vast/.fenrir_p7_box.json", "w").write(json.dumps(
    {"id": z["id"], "ip": z.get("ssh_host"), "port": z.get("ssh_port"),
     "dph": x["dph_total"], "gpu": x["gpu_name"], "offer": x["id"]}, indent=2))
print("BOX_SAVED .fenrir_p7_box.json")
