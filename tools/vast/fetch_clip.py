#!/usr/bin/env python3
"""Fetch a Vast instance's container log via the API and rebuild any B64BEGIN/B64END files.
Usage: fetch_clip.py <instance_id> [outdir]    (VASTAI_API env var must be set; value never printed)"""
import os, sys, json, time, base64, hashlib, re, urllib.request
iid = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else "."
H = {"Authorization": "Bearer " + os.environ["VASTAI_API"], "Content-Type": "application/json"}
r = urllib.request.Request(f"https://console.vast.ai/api/v0/instances/request_logs/{iid}/", data=json.dumps({"tail": "60000"}).encode(), headers=H, method="PUT")
u = json.load(urllib.request.urlopen(r, timeout=60))["temp_download_url"]
for _ in range(12):
    time.sleep(5)
    try: txt = urllib.request.urlopen(u, timeout=60).read().decode(errors="replace"); break
    except Exception: txt = ""
cur = None; parts = {}; meta = {}; log = []
for ln in txt.splitlines():
    m = re.search(r"B64BEGIN (\S+) (\d+) (\w+)", ln)
    if m: cur = m.group(1); meta[cur] = (int(m.group(2)), m.group(3)); parts[cur] = {}; continue
    if re.search(r"B64END", ln): cur = None; continue
    m = re.match(r"B64 (\d+) (\S+)$", ln.strip())
    if m and cur: parts[cur][int(m.group(1))] = m.group(2); continue
    if "AUTORUN" in ln or "run:" in ln or "job:" in ln: log.append(ln)
print("\n".join(log[-40:]))
for n, p in parts.items():
    if not p: continue
    data = base64.b64decode("".join(p[i] for i in sorted(p)))
    ok = len(data) == meta[n][0] and hashlib.sha256(data).hexdigest() == meta[n][1]
    path = os.path.join(out, "vast_" + n); open(path, "wb").write(data)
    print(f"RECOVERED {path} {len(data)} bytes, checksum {'OK' if ok else 'MISMATCH'} ({len(p)} chunks)")
