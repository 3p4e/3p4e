#!/usr/bin/env python3
"""Rent the PROVEN Texas host once (offer 59431050, same IP as the only
working box 61116065), template 2188dfd3 + onstart key injection, wait,
then SSH DIRECT-first with verbose errors. Prints ONE verdict."""
import json, os, sys, time, subprocess, urllib.request, urllib.error

K = os.environ["VASTAI_API"].strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
BASE = "https://console.vast.ai/api/v0"

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

# refuse to double-rent
if any(i.get("status") == "running" or i.get("actual_status") == "running" for i in insts):
    print("ALREADY HAVE RUNNING INSTANCE - NOT RENTING")
    sys.exit(0)

pub1 = open("/root/.ssh/vast_karsus.pub").read().strip()
pub2 = open("/root/.ssh/vast_rsa.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/models /workspace/stills /workspace/hf /workspace/ltx25\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{pub1}' > /root/.ssh/authorized_keys\n"
    f"echo '{pub2}' >> /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    "which sshd >/dev/null 2>&1 || (apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq openssh-server >/dev/null 2>&1)\n"
    "sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config 2>/dev/null\n"
    "mkdir -p /run/sshd 2>/dev/null; (service ssh start 2>/dev/null || /usr/sbin/sshd 2>/dev/null || true)\n"
    "date -u > /workspace/BOOTED; echo KEY_INSTALLED > /workspace/KEYOK\n"
    "nohup setsid bash -c 'sleep 9000' >/dev/null 2>&1 &\n"
)

# rent the proven Texas offer with the PROVEN template
body = {"template_hash_id": "2188dfd3e0a0b83691bb468ddae0a4e5",
        "disk": 200, "label": "sunder-texas-once", "onstart": onstart, "runtype": "ssh"}
r = req("PUT", "/asks/59431050/", body)
if isinstance(r, dict):
    r.pop("instance_api_key", None)
print("RENT:", json.dumps(r)[:400], flush=True)
cid = r.get("new_contract") if isinstance(r, dict) else None
if not cid:
    print("RENT_FAILED"); sys.exit(1)
print("CONTRACT", cid, flush=True)

# patient poll for running + port
ip = port = proxy = None
for i in range(32):
    for x in req("GET", "/instances/").get("instances", []):
        if x.get("id") == cid:
            ip = x.get("public_ipaddr"); port = x.get("ssh_port"); proxy = x.get("ssh_host")
            print(f"{time.strftime('%H:%M:%S')} poll{i}: status={x.get('status')} actual={x.get('actual_status')} msg={x.get('status_msg')!r} port={port}", flush=True)
    if port and (x.get("actual_status") == "running"):
        break
    time.sleep(15)

if not port:
    print("NO_PORT_AFTER_WAIT"); sys.exit(2)

box = {"contract": cid, "ssh_ip": ip, "ssh_port": port, "ssh_host": proxy,
       "ssh_key": "/root/.ssh/vast_karsus", "gpu": x.get("gpu_name"), "dph": x.get("dph_total")}
json.dump(box, open("/a0/usr/projects/vast/.sunder_box.json", "w"), indent=2)
print("SAVED_BOX", json.dumps(box), flush=True)

# wait for onstart to settle
print("settling 90s for onstart sshd...", flush=True)
time.sleep(90)

def ssh(dest, tag):
    cmd = ["ssh", "-v", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes",
           "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
           "-i", "/root/.ssh/vast_karsus", "-p", str(port), f"root@{dest}",
           "echo SSH_OK; cat /workspace/BOOTED /workspace/KEYOK 2>/dev/null; nvidia-smi -L 2>/dev/null | head -1"]
    print(f"--- SSH {tag} {dest}:{port} ---", flush=True)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        print("RC", r.returncode, flush=True)
        if r.stdout: print("OUT:", r.stdout.strip()[:400], flush=True)
        if r.stderr: print("ERR:", r.stderr.strip()[-800:], flush=True)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return False

ok = ssh(ip, "direct")
if not ok:
    ssh(proxy, "proxy")
print("VERDICT:", "DIRECT_OK" if ok else "SSH_FAILED", flush=True)
