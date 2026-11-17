#!/usr/bin/env python3
"""KVM4 runner relay for sandboxes that only have HTTPS (no ssh, no raw TCP). Library + tiny CLI.
Env: KVM4_RUNNER_URL, KVM4_RUNNER_TOKEN, KVM4_VM_ID (Hostinger VM id), HOSTINGER_API_TOKEN (compose fallback) (the env token was stale on 2026-11-01; the live one sits in the runner's compose file
and may be read through the Hostinger API ONLY with the owner's explicit authorisation: --allow-compose-token).
  kvm_relay.py 'hostname'                      run a shell command on KVM4 (inside the runner container, docker.sock mounted)
  put(local, remote) / get(remote, local)      chunked base64 transfer with SHA-256 check (60 KB chunks)
Harnesses WITH normal network access (Agent Zero on KVM4, DeepSeek-TUI/Kimi on your PC) do not need this: use ssh/scp directly.
"""
import base64, hashlib, json, os, re, sys, urllib.request
U = os.environ["KVM4_RUNNER_URL"].rstrip("/")
def _token(allow_compose=False):
    t = os.environ.get("KVM4_RUNNER_TOKEN")
    if t and not allow_compose: return t
    h = {"Authorization": "Bearer " + os.environ["HOSTINGER_API_TOKEN"], "User-Agent": "curl/8"}  # Hostinger returns 403 for the default Python user agent
    raw = urllib.request.urlopen(urllib.request.Request("https://developers.hostinger.com/api/vps/v1/virtual-machines/" + os.environ["KVM4_VM_ID"] + "/docker/kvm4-runner", headers=h), timeout=30).read().decode()
    d = json.loads(raw); c = d.get("contents") or d.get("content") or d.get("data") or raw   # parse the JSON first: raw text has escaped newlines
    c = c if isinstance(c, str) else json.dumps(c)
    return re.search(r"RUNNER_TOKEN=([^\s\"']+)", c).group(1)
T = _token("--allow-compose-token" in sys.argv)
def sh(cmd, timeout=170):
    r = urllib.request.Request(U + "/shell", data=json.dumps({"cmd": cmd, "command": cmd}).encode(), headers={"Authorization": "Bearer " + T, "Content-Type": "application/json"}, method="POST")
    try: return json.load(urllib.request.urlopen(r, timeout=timeout))
    except urllib.error.HTTPError as e: return {"http": e.code, "body": e.read().decode()[:300]}
def put(local, remote, chunk=60000):
    data = open(local, "rb").read(); b = base64.b64encode(data).decode(); sh(f"rm -f {remote}.b64")
    for i in range(0, len(b), chunk): assert sh(f"printf '%s' '{b[i:i+chunk]}' >> {remote}.b64").get("rc") == 0
    out = sh(f"base64 -d {remote}.b64 > {remote} && rm {remote}.b64 && sha256sum {remote} | cut -d' ' -f1")["output"].strip()
    assert out == hashlib.sha256(data).hexdigest(), "checksum mismatch"; return len(data)
def get(remote, local, chunk=150000):
    m = sh(f"base64 -w0 {remote} > {remote}.b64; stat -c%s {remote}; wc -c < {remote}.b64; sha256sum {remote} | cut -d' ' -f1")["output"].split()
    size, blen, sha = int(m[0]), int(m[1]), m[2]; parts = []
    for s in range(0, blen, chunk):
        r = sh(f"cut -b {s+1}-{min(s+chunk, blen)} {remote}.b64"); assert not r.get("truncated"); parts.append(r["output"].strip())
    data = base64.b64decode("".join(parts)); sh(f"rm -f {remote}.b64")
    assert len(data) == size and hashlib.sha256(data).hexdigest() == sha, "checksum mismatch"; open(local, "wb").write(data); return size
if __name__ == "__main__" and len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    r = sh(sys.argv[1]); print(r.get("output", r))
