#!/usr/bin/env python3
"""Small Vast.ai control tool. Env: VASTAI_API.
  vast_ctl.py status | stop ID | start ID | destroy ID --yes | attach-key ID PUBKEYFILE | revoke-key ID KEYID | logs ID [N]
Stop keeps the disk (storage still bills); destroy deletes everything. Destroy only after outputs are checksummed.
"""
import json, os, sys, time, urllib.request
K = os.environ["VASTAI_API"]; H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
def req(m, p, b=None):
    r = urllib.request.Request("https://console.vast.ai/api/v0" + p, data=json.dumps(b).encode() if b is not None else None, headers=H, method=m)
    try: return json.load(urllib.request.urlopen(r, timeout=90))
    except urllib.error.HTTPError as e: return {"http": e.code, "body": e.read().decode()[:300]}
c = sys.argv[1] if len(sys.argv) > 1 else "status"
if c == "status":
    for x in req("GET", "/instances/").get("instances", []):
        print(x["id"], x.get("label"), x["actual_status"], x.get("cur_state"), f"${x['dph_total']:.3f}/h", x.get("gpu_name"), x.get("public_ipaddr"), ((x.get("ports") or {}).get("22/tcp") or [{}])[0].get("HostPort"))
    print("credit:", round(req("GET", "/users/current/")["credit"], 3))
elif c in ("stop", "start"): print(req("PUT", f"/instances/{sys.argv[2]}/", {"state": "stopped" if c == "stop" else "running"}))
elif c == "destroy":
    if "--yes" not in sys.argv: sys.exit("refusing: add --yes (destroy deletes the disk)")
    print(req("DELETE", f"/instances/{sys.argv[2]}/"))
elif c == "attach-key": print(req("POST", f"/instances/{sys.argv[2]}/ssh/", {"ssh_key": open(sys.argv[3]).read().strip()}))
elif c == "revoke-key": print(req("DELETE", f"/instances/{sys.argv[2]}/ssh/{sys.argv[3]}/"))
elif c == "logs":
    d = req("PUT", f"/instances/request_logs/{sys.argv[2]}/", {"tail": sys.argv[3] if len(sys.argv) > 3 else "80"}); time.sleep(8)
    print(urllib.request.urlopen(d["temp_download_url"], timeout=60).read().decode(errors="replace")[-6000:])  # snapshots are cached for minutes
