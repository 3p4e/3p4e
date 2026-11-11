#!/usr/bin/env python3
"""Rent exactly one 48GB-class GPU for the Kandinsky 6.0 batch. Minimal onstart (boot only);
files are pushed over SSH, then k6_autorun.sh is launched. Refuses to double-rent."""
import json, os, sys, time, urllib.request, urllib.error, random

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"
LABEL = os.environ.get("LABEL", "paladin-k6")
MAXPRICE = float(os.environ.get("MAXPRICE", "0.55"))
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
BROKEN_HOSTS = {"32.196.117.67"}
bad = {"Tesla V100", "Q RTX 8000", "CMP 170HX", "Titan RTX", "Tesla P40", "Tesla P100"}
c = [x for x in offers
     if x["dph_total"] <= MAXPRICE and x["gpu_name"] not in bad
     and (x.get("cpu_ram") or 0) / 1024 >= 32
     and (x.get("cpu_cores_effective") or 0) >= 8
     and (x.get("inet_down") or 0) >= 2000
     and (x.get("total_flops") or 0) >= 30
     and str(x.get("ssh_host") or x.get("public_ipaddr") or "") not in BROKEN_HOSTS]
for x in c[:8]:
    print(f"cand {x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h "
          f"rel={x.get('reliability2'):.2f} down={int(x.get('inet_down') or 0)}Mbps {x.get('geolocation')}")
if not c:
    sys.exit("no candidate offer matched")

x = c[0]
PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/hf\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
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
for _ in range(20):
    time.sleep(10)
    y = [z for z in req("GET", "/instances/").get("instances", []) if z["id"] == cid]
    if not y:
        print("instance not listed yet")
        continue
    y = y[0]
    print(y.get("actual_status"), "|", (y.get("status_msg") or "")[:120])
    if y.get("actual_status") == "running" and (y.get("ports") or {}).get("22/tcp"):
        info = {"id": cid, "ip": y["public_ipaddr"],
                "port": y["ports"]["22/tcp"][0]["HostPort"],
                "dph": round(y["dph_total"], 3)}
        break
if not info:
    sys.exit(f"instance {cid} did not reach running+ssh in time; check vast_ctl.py status")
json.dump(info, open("/a0/usr/projects/vast/.k6_instance.json", "w"), indent=2)
print("INSTANCE", json.dumps(info))
