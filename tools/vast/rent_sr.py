#!/usr/bin/env python3
"""Rent exactly one 80GB-class GPU for the SkyReels-V3 R2V test.
Minimal onstart (SSH key only); files pushed over SSH, then sr_setup.sh launched.
Refuses to double-rent. Pins an exact offer id when TARGET_ID is set."""
import json, os, sys, urllib.request, urllib.error

K = os.environ["VASTAI_API"]
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
LABEL = os.environ.get("LABEL", "skyreels-v3")
MAXPRICE = float(os.environ.get("MAXPRICE", "1.20"))
MINVRAM = int(os.environ.get("MINVRAM", "78000"))
DISK = int(os.environ.get("DISK", "200"))
TARGET = os.environ.get("TARGET_ID", "49067605")
TEMPLATE = os.environ.get("TEMPLATE", "pytorch/pytorch:2.8.0-cuda12.8-cudnn9-devel")


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
print(f"credit ${credit:.4f} | instances {len(insts)}")
if insts:
    for z in insts:
        print("  RUNNING:", z.get("id"), z.get("gpu_name"), z.get("label"), z.get("actual_status"))
    sys.exit("refusing: instances already running - clean up first")

q = {"num_gpus": {"eq": 1}, "rentable": {"eq": True}, "rented": {"eq": False},
     "verified": {"eq": True}, "gpu_ram": {"gte": MINVRAM}, "disk_space": {"gte": DISK},
     "reliability2": {"gte": 0.95}, "type": "ondemand", "limit": 300,
     "order": [["dph_total", "asc"]]}
offers = req("POST", "/bundles/", q).get("offers", [])
print(f"offers >= {MINVRAM//1000}GB: {len(offers)}")

pick = None
if TARGET:
    pick = next((x for x in offers if str(x["id"]) == str(TARGET)), None)
    if pick is None:
        print(f"TARGET_ID {TARGET} not in filtered set; listing alternatives:")
        for x in offers[:6]:
            print(f"  {x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h {x.get('geolocation')}")
        sys.exit("exact offer unavailable")
else:
    pick = offers[0]

if pick["dph_total"] > MAXPRICE:
    sys.exit(f"refusing: ${pick['dph_total']:.3f}/h above cap ${MAXPRICE:.2f}")

print(f"PICK {pick['id']} {pick['gpu_name']} {pick['gpu_ram']/1024:.0f}GB "
      f"${pick['dph_total']:.3f}/h down={int(pick.get('inet_down') or 0)}Mbps {pick.get('geolocation')}")

PUB = open("/root/.ssh/vast_karsus.pub").read().strip()
onstart = (
    "#!/bin/bash\n"
    "exec > /var/log/onstart.log 2>&1\n"
    "set -x\n"
    "mkdir -p /root/.ssh /workspace/out /workspace/refs\n"
    "chmod 700 /root/.ssh\n"
    f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
    "chmod 600 /root/.ssh/authorized_keys\n"
    # install sshd if the base image lacks it (this failure already cost a rental)
    "if ! command -v sshd >/dev/null 2>&1 && [ ! -x /usr/sbin/sshd ]; then\n"
    "  apt-get update -qq && apt-get install -y -qq openssh-server >/dev/null 2>&1\n"
    "fi\n"
    "mkdir -p /run/sshd /var/run/sshd\n"
    "sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null\n"
    "sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config 2>/dev/null\n"
    "grep -q '^Port 22' /etc/ssh/sshd_config || echo 'Port 22' >> /etc/ssh/sshd_config\n"
    "/usr/sbin/sshd -D -e &\n"
    "sleep 2\n"
    "ss -ltnp 2>/dev/null | grep 22 || netstat -ltnp 2>/dev/null | grep 22\n"
    "echo ONSTART_DONE\n"
)

body = {"client_id": "me", "image": TEMPLATE, "disk": DISK,
        "onstart": onstart, "label": LABEL, "runtype": "ssh_direc ssh_proxy",
        "target_state": "running"}
r = req("PUT", f"/asks/{pick['id']}/", body)
print("rent response:", json.dumps(r)[:400])
if "new_contract" not in r and "success" not in r:
    sys.exit("rental failed")

cid = r.get("new_contract")
print(f"CONTRACT {cid}")
json.dump({"id": cid, "label": LABEL, "dph": pick["dph_total"],
           "gpu": pick["gpu_name"], "started": __import__("time").time()},
          open("/a0/usr/projects/vast/.sr_instance.json", "w"), indent=2)
print("saved /a0/usr/projects/vast/.sr_instance.json")
