#!/usr/bin/env python3
"""Rent exactly one 80GB-class GPU for LTX-2.5 Sunder cut (weights + dual LoRA + batch).
Refuses to double-rent. Injects both SSH keys via onstart."""
import json, os, sys, time, urllib.request, urllib.error

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"
LABEL = os.environ.get("LABEL", "sunder-ltx25")
MAXPRICE = float(os.environ.get("MAXPRICE", "1.50"))
MINVRAM = int(os.environ.get("MINVRAM", "79000"))
DISK = int(os.environ.get("DISK", "200"))

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
bad = {"Tesla V100", "Q RTX 8000", "CMP 170HX", "Titan RTX", "Tesla P40", "Tesla P100", "Tesla T4", "Tesla K80"}
# Blackwell-generation GPUs (sm_100/sm_120) have no working PyTorch kernels.
# Exclude by compute capability AND by name so we never rent another incompatible box.
BLACKWELL_NAMES = {"GB10", "GB200", "GB300", "B100", "B200", "RTX PRO", "MAX-Q", "5090", "5080", "5070", "BLACKWELL"}
c = [x for x in offers
     if x["dph_total"] <= MAXPRICE and x["gpu_name"] not in bad
     and (x.get("compute_cap") or 0) < 1000
     and not any(b.lower() in (x.get("gpu_name") or "").lower() for b in BLACKWELL_NAMES)
     and (x.get("cpu_ram") or 0) / 1024 >= 64
     and (x.get("cpu_cores_effective") or 0) >= 16
     and (x.get("inet_down") or 0) >= 500
     and str(x.get("ssh_host") or x.get("public_ipaddr") or "") not in BROKEN_HOSTS
     and "AE" not in (x.get("geolocation") or "")
     and "United Arab Emirates" not in (x.get("geolocation") or "")]

print(f"80GB+ offers: {len(c)}")
for x in c[:8]:
    print(f"  cand {x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h "
          f"rel={x.get('reliability2'):.2f} down={int(x.get('inet_down') or 0)}Mbps {x.get('geolocation')}")
if not c:
    sys.exit("no 80GB candidate offer matched at MAXPRICE")

x = c[0]
PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
PUB2 = open("/root/.ssh/vast_rsa.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/hf /workspace/ltx25\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
    f"echo '{PUB2}' >> /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    "sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config 2>/dev/null\n"
    "pkill -HUP sshd 2>/dev/null || (service ssh restart 2>/dev/null || /usr/sbin/sshd 2>/dev/null)\n"
    "date -u > /workspace/BOOTED\n"
    "echo KEY_INSTALLED > /workspace/KEYOK\n"
    "nohup setsid bash -c 'sleep 9000' >/dev/null 2>&1 &\n"
)
r = req("PUT", f"/asks/{x['id']}/", {"template_hash_id": TEMPLATE, "disk": DISK,
                                      "label": LABEL, "onstart": onstart})
r.pop("instance_api_key", None)
print("rent:", json.dumps(r)[:500])
if not r.get("success") or not r.get("new_contract"):
    sys.exit(f"RENT FAILED: {r}")
cid = r["new_contract"]
print(f"contract {cid} at ${x['dph_total']:.3f}/h")

info = None
for _ in range(30):
    time.sleep(10)
    info = req("GET", f"/instances/{cid}/")
    if info.get("ssh_host") and info.get("ssh_port"):
        break
print(json.dumps({"contract": cid, "ssh_host": info.get("ssh_host"), "ssh_port": info.get("ssh_port"),
                  "label": LABEL, "gpu": x['gpu_name'], "rate": x['dph_total']}, indent=2))
