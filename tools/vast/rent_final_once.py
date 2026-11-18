#!/usr/bin/env python3
"""ONE decisive rental using the recipe that ACTUALLY worked (box 61116065):
  - template 2188dfd3 (vastai/comfy image)
  - MINIMAL onstart: write keys + markers only, NEVER restart sshd (flapping sshd
    was causing the kex-closings). Account keys are already registered, so Vast
    injects them at boot anyway.
  - fresh live offers (no stale id), prefer 80GB+ A100 SXM4, prefer Texas 104.37.174.11
  - poll until running+port, then SSH DIRECT-first with verbose errors.
Prints ONE verdict."""
import json, os, sys, time, subprocess, urllib.request, urllib.error

K = os.environ["VASTAI_API"].strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
BASE = "https://console.vast.ai/api/v0"
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"  # vastai/comfy:v0.43.0-cuda-12.9-py312 (PROVEN)
PREFER_IP = "104.37.174.11"  # Texas host where 61116065 worked

def req(m, p, b=None):
    r = urllib.request.Request(BASE + p,
        data=json.dumps(b).encode() if b is not None else None, headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=60).read().decode())
    except urllib.error.HTTPError as e:
        try: return {"http": e.code, "body": e.read().decode()[:400]}
        except: return {"http": e.code}
    except Exception as e:
        return {"error": str(e)}

print("CREDIT:", req("GET", "/users/current/").get("credit"), flush=True)
insts = req("GET", "/instances/").get("instances", [])
print("LIVE:", [(i.get("id"), i.get("status"), i.get("actual_status"), i.get("label")) for i in insts], flush=True)

# already have a running box? don't double-rent
for i in insts:
    if i.get("actual_status") == "running" and i.get("status") not in ("exited",):
        print("ALREADY_RUNNING", i.get("id")); sys.exit(0)

# fresh offers
q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
     "verified": {"eq": True}, "gpu_ram": {"gte": 79000}, "disk_space": {"gte": 200},
     "reliability2": {"gte": 0.97}, "type": "ondemand", "limit": 300,
     "order": [["dph_total", "asc"]]}
offers = req("POST", "/bundles/", q).get("offers", [])
BAD = {"GB10","GB200","GB300","B100","B200","RTX PRO","MAX-Q","5090","5080","5070",
       "BLACKWELL","TESLA V100","TITAN RTX","CMP 170HX","P40","P100","K80","T4"}
cand = []
for x in offers:
    g = (x.get("gpu_name") or "").upper()
    if any(b in g for b in BAD):
        continue
    if (x.get("compute_cap") or 0) >= 1000:
        continue
    if "SXM4" not in g:
        continue
    cand.append(x)
if not cand:
    print("NO_SXM4_OFFERS"); sys.exit(1)

# prefer the proven Texas host, else cheapest reliable
cand.sort(key=lambda x: (x.get("public_ipaddr") != PREFER_IP, x.get("dph_total", 9)))
x = cand[0]
print(f"CHOSEN id={x['id']} {x['gpu_name']} ${x['dph_total']:.3f}/h ip={x.get('public_ipaddr')} "
      f"rel={x.get('reliability2')} {x.get('geolocation')}", flush=True)

# MINIMAL onstart: write keys + markers, NO sshd restart
pub1 = open("/root/.ssh/vast_karsus.pub").read().strip()
pub2 = open("/root/.ssh/vast_rsa.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/models /workspace/stills /workspace/hf /workspace/ltx25\n"
    "chmod 700 /root/.ssh; touch /root/.ssh/authorized_keys; chmod 600 /root/.ssh/authorized_keys\n"
    f"grep -qF '{pub1}' /root/.ssh/authorized_keys || echo '{pub1}' >> /root/.ssh/authorized_keys\n"
    f"grep -qF '{pub2}' /root/.ssh/authorized_keys || echo '{pub2}' >> /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    "date -u > /workspace/BOOTED; echo KEY_INSTALLED > /workspace/KEYOK\n"
    "nohup setsid bash -c 'sleep 9000' >/dev/null 2>&1 &\n"
)

body = {"template_hash_id": TEMPLATE, "disk": 200, "label": "sunder-final",
        "onstart": onstart, "runtype": "ssh"}
r = req("PUT", f"/asks/{x['id']}/", body)
if isinstance(r, dict):
    r.pop("instance_api_key", None)
print("RENT:", json.dumps(r)[:400], flush=True)
cid = r.get("new_contract") if isinstance(r, dict) else None
if not cid:
    print("RENT_FAILED"); sys.exit(2)
print("CONTRACT", cid)

# patient poll
ip = port = proxy = None
for i in range(36):
    for y in req("GET", "/instances/").get("instances", []):
        if y.get("id") == cid:
            ip = y.get("public_ipaddr"); port = y.get("ssh_port"); proxy = y.get("ssh_host")
            print(f"{time.strftime('%H:%M:%S')} poll{i}: st={y.get('status')} act={y.get('actual_status')} msg={y.get('status_msg')!r} port={port}", flush=True)
            if port and y.get("actual_status") == "running" and i > 3:
                break
    if port and i > 3:
        break
    time.sleep(15)

if not port:
    print("NO_PORT"); sys.exit(3)
json.dump({"contract": cid, "ssh_ip": ip, "ssh_port": port, "ssh_host": proxy,
           "ssh_key": "/root/.ssh/vast_karsus", "gpu": y.get("gpu_name"),
           "dph": y.get("dph_total")}, open("/a0/usr/projects/vast/.sunder_box.json", "w"), indent=2)
print("SAVED_BOX port", port, flush=True)

# wait 60s after running for Vast's own sshd to be up (it injects account keys at boot)
print("settling 60s...", flush=True); time.sleep(60)

def ssh(dest, tag):
    cmd = ["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes",
           "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
           "-i", "/root/.ssh/vast_karsus", "-p", str(port), f"root@{dest}",
           "echo SSH_OK; cat /workspace/BOOTED /workspace/KEYOK 2>/dev/null; nvidia-smi -L 2>/dev/null | head -1"]
    print(f"--- SSH {tag} {dest}:{port} ---", flush=True)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        print("RC", r.returncode, flush=True)
        if r.stdout: print("OUT:", r.stdout.strip()[:400], flush=True)
        if r.stderr: print("ERR:", r.stderr.strip()[-700:], flush=True)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return False

ok = ssh(ip, "direct")
if not ok:
    ssh(proxy, "proxy")
print("FINAL_VERDICT:", "SSH_OK" if ok else "SSH_STILL_FAILING", flush=True)
