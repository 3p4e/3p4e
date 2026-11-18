#!/usr/bin/env python3
"""PROVEN-RECIPE single rent + verify. Never destroys on early SSH failure.
Template 2188dfd3 + onstart key injection (the combo that worked on box 61116065).
Usage: VASTAI_API=... python3 rent_verify_once.py
"""
import json, os, sys, time, subprocess, urllib.request, urllib.error

K = os.environ["VASTAI_API"].strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
BASE = "https://console.vast.ai/api/v0"
TEMPLATE = "2188dfd3e0a0b83691bb468ddae0a4e5"  # PROVEN on box 61116065

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

# refuse double-rent
if any((i.get("status") == "running" or i.get("actual_status") == "running") for i in insts):
    cid = next(i["id"] for i in insts if i.get("actual_status") == "running" or i.get("status") == "running")
    print("RUNNING_INSTANCE_EXISTS", cid);
else:
    q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
         "verified": {"eq": True}, "gpu_ram": {"gte": 79000}, "disk_space": {"gte": 200},
         "reliability2": {"gte": 0.95}, "type": "ondemand", "limit": 300,
         "order": [["dph_total", "asc"]]}
    offers = req("POST", "/bundles/", q).get("offers", [])
    bad = {"GB10","GB200","GB300","B100","B200","RTX PRO","MAX-Q","5090","5080","5070","BLACKWELL","TESLA V100","TITAN RTX"}
    pick = None
    for x in offers:
        g = (x.get("gpu_name") or "").upper()
        geo = (x.get("geolocation") or "")
        if "SXM4" not in g or "PCIE" in g:
            continue
        if any(b in g for b in bad):
            continue
        if x.get("compute_cap", 0) and x.get("compute_cap") >= 1000:
            continue
        if "AE" in geo or "United Arab Emirates" in geo:
            continue
        pick = x
        break
    if not pick:
        print("NO_VIABLE_OFFER"); sys.exit(1)

    pub1 = open("/root/.ssh/vast_karsus.pub").read().strip()
    pub2 = open("/root/.ssh/vast_rsa.pub").read().strip()
    # MINIMAL correct onstart: write keys, ensure sshd, NO pkill/HUP flapping
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
        "mkdir -p /run/sshd 2>/dev/null; pgrep sshd >/dev/null 2>&1 || (service ssh start 2>/dev/null || /usr/sbin/sshd 2>/dev/null || true)\n"
        "date -u > /workspace/BOOTED; echo KEY_INSTALLED > /workspace/KEYOK\n"
    )
    body = {"template_hash_id": TEMPLATE, "disk": 200,
            "label": "sunder-proven-r1", "onstart": onstart, "runtype": "ssh"}
    r = req("PUT", f"/asks/{pick['id']}/", body)
    if isinstance(r, dict):
        r.pop("instance_api_key", None)
    print("RENT:", json.dumps(r)[:400], flush=True)
    print("CHOSEN:", pick["id"], pick["gpu_name"], f"${pick['dph_total']:.3f}/h", pick.get("geolocation"), flush=True)
    cid = r.get("new_contract") if isinstance(r, dict) else None
    if not cid:
        print("RENT_FAILED"); sys.exit(1)
    print("CONTRACT", cid, flush=True)

# patient wait for running + port (up to ~8 min)
ip = port = proxy = None
x = None
for i in range(32):
    for z in req("GET", "/instances/").get("instances", []):
        if z.get("id") == cid:
            x = z
    if x:
        print(f"{time.strftime('%H:%M:%S')} poll{i}: status={x.get('status')} actual={x.get('actual_status')} port={x.get('ssh_port')}", flush=True)
    if x and x.get("ssh_port") and x.get("actual_status") == "running":
        ip = x.get("public_ipaddr"); port = x.get("ssh_port"); proxy = x.get("ssh_host")
        break
    time.sleep(15)

if not port:
    print("NO_PORT_AFTER_WAIT — box kept alive, check later"); sys.exit(2)

json.dump({"contract": cid, "ssh_ip": ip, "ssh_port": port, "ssh_host": proxy,
           "ssh_key": "/root/.ssh/vast_karsus", "gpu": x.get("gpu_name"),
           "dph": x.get("dph_total")}, open("/a0/usr/projects/vast/.sunder_box.json", "w"), indent=2)
print("SAVED_BOX", flush=True)

# KB §18: boot + onstart takes 3-4 min. Wait patiently.
print("settling 240s for boot+onstart sshd (KB §18, do not destroy on early closed)...", flush=True)
time.sleep(240)

def ssh(dest, tag):
    cmd = ["ssh", "-v", "-o", "ConnectTimeout=20", "-o", "BatchMode=yes",
           "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
           "-i", "/root/.ssh/vast_karsus", "-p", str(port), f"root@{dest}",
           "echo SSH_OK; cat /workspace/BOOTED /workspace/KEYOK 2>/dev/null; nvidia-smi -L 2>/dev/null | head -1"]
    print(f"--- SSH {tag} {dest}:{port} ---", flush=True)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        print("RC", r.returncode, flush=True)
        if r.stdout: print("OUT:", r.stdout.strip()[:400], flush=True)
        if r.stderr: print("ERR:", r.stderr.strip()[-700:], flush=True)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return False

ok = ssh(ip, "direct")
if not ok:
    ssh(proxy, "proxy")
print("VERDICT:", "OK" if ok else "NOT_YET", "— box NOT destroyed", flush=True)