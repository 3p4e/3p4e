#!/usr/bin/env python3
"""One-shot: inspect a Vast.ai instance fully, wait for its onstart marker
to be reachable, then run a single SSH test. No renting, no destroying.
Usage: VASTAI_API=<key> python3 box_status.py <contract_id> [wait_minutes]"""
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
        return {"http": e.code, "body": e.read().decode()[:300]}
    except Exception as e:
        return {"error": str(e)}

def get_inst(cid):
    insts = req("GET", "/instances/").get("instances", [])
    return next((x for x in insts if x.get("id") == cid), None)

def main():
    cid = int(sys.argv[1])
    wait_m = int(sys.argv[2]) if len(sys.argv) > 2 else 8

    print("CREDIT:", req("GET", "/users/current/").get("credit"), flush=True)
    t = get_inst(cid)
    if t is None:
        print("INSTANCE NOT FOUND"); return 1

    for f in ("id","label","status","actual_status","status_msg","ssh_host","ssh_port",
              "public_ipaddr","image_uuid","image","gpu_name","dph_total","geolocation",
              "disk_space","ram_used","num_minutes_billed","fail_reason"):
        print(f"{f}: {t.get(f)}", flush=True)

    ip, port, proxy = t.get("public_ipaddr"), t.get("ssh_port"), t.get("ssh_host")
    if not port:
        print("NO SSH PORT YET"); return 1

    # Wait until status stabilizes and onstart has had time to run.
    deadline = time.time() + wait_m * 60
    prev_msg = t.get("status_msg")
    while time.time() < deadline:
        t = get_inst(cid)
        msg = t.get("status_msg")
        if msg != prev_msg:
            print(f"[{time.strftime('%H:%M:%S')}] status_msg changed -> {msg!r}", flush=True)
            prev_msg = msg
        # readiness signal: /ssh appears in status_msg (field-proven) OR marker reachable
        if t.get("actual_status") == "running" and not msg:
            break
        time.sleep(20)

    # Persist box details
    box = {"contract": cid, "ssh_ip": ip, "ssh_port": port, "ssh_host": proxy,
           "ssh_key": "/root/.ssh/vast_karsus", "gpu": t.get("gpu_name"),
           "dph": t.get("dph_total"), "status_msg": t.get("status_msg")}
    json.dump(box, open("/a0/usr/projects/vast/.sunder_box.json", "w"), indent=2)
    print("SAVED_MSG:", t.get("status_msg"), flush=True)

    def tcp(dest):
        r = subprocess.run(["timeout", "10", "bash", "-c",
                            f"cat < /dev/null > /dev/tcp/{dest}/{port}"],
                           capture_output=True, text=True)
        return "OPEN" if r.returncode == 0 else "FAIL"

    print("TCP_PROXY", proxy, tcp(proxy), flush=True)
    print("TCP_DIRECT", ip, tcp(ip), flush=True)

    def ssh(dest, tag):
        cmd = ["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes",
               "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
               "-i", "/root/.ssh/vast_karsus", "-p", str(port), f"root@{dest}",
               "echo SSH_OK; cat /workspace/BOOTED /workspace/KEYOK 2>/dev/null; nvidia-smi -L 2>/dev/null | head -1"]
        print(f"--- SSH {tag} {dest}:{port} ---", flush=True)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            print("RC", r.returncode, flush=True)
            if r.stdout: print("OUT:", r.stdout.strip()[:400], flush=True)
            if r.stderr: print("ERR:", r.stderr.strip()[-500:], flush=True)
            return r.returncode == 0
        except subprocess.TimeoutExpired:
            print("TIMEOUT", flush=True); return False

    ok = ssh(proxy, "proxy")
    if not ok:
        ssh(ip, "direct")
    return 0

if __name__ == "__main__":
    sys.exit(main())
