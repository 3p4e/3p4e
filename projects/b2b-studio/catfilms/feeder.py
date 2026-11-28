# Ships new category-film keyframes to both Vast boxes as they are generated (sandbox -> KVM4 runner -> ssh), as JPEG q95;
# when the local KF_DONE exists and everything is sent, sets KF_DONE on the boxes so their --loop batches finish.
import os, io, json, time, base64, tarfile, urllib.request
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KF = f"{S}/catfilms/kf"
url = os.environ["RUNNER_URL"].rstrip("/"); H = {"Authorization": "Bearer " + os.environ["RUNNER_TOKEN"], "Content-Type": "application/json"}
def sh(cmd, t=300):
    r = json.loads(urllib.request.urlopen(urllib.request.Request(url + "/shell", data=json.dumps({"cmd": cmd, "timeout": t}).encode(), headers=H), timeout=t + 30).read())
    return (r.get("stdout") or "") + (r.get("stderr") or "")
sent = set(); n = 0
while True:
    done = os.path.exists(f"{KF}/KF_DONE")
    new = sorted(f for f in os.listdir(KF) if f.endswith(".png") and f not in sent and time.time() - os.path.getmtime(f"{KF}/{f}") > 10)[:60]   # skip files still being written
    if new:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            for f in new:
                b = io.BytesIO(); Image.open(f"{KF}/{f}").convert("RGB").save(b, "JPEG", quality=95)
                ti = tarfile.TarInfo(f[:-4] + ".jpg"); ti.size = b.tell(); b.seek(0); tf.addfile(ti, b)
        n += 1; name = f"cffeed_{n}.tgz"
        try:
            urllib.request.urlopen(urllib.request.Request(url + "/file/write", data=json.dumps({"path": f"/opt/abra-v3/{name}", "content_b64": base64.b64encode(buf.getvalue()).decode(), "mkdir": True}).encode(), headers=H), timeout=300)
            out = sh(f"cd /opt/abra-v3 && for b in A B; do timeout 120 ./fv$b.sh 'mkdir -p /workspace/cfbundle/kf && cd /workspace/cfbundle/kf && tar xzf - && ls | wc -l' < {name} | tail -1; done; rm -f {name}")
            print(time.strftime("%H:%M:%S"), name, len(new), out.split(), flush=True); sent.update(new); continue
        except Exception as e: print("feed error", e, flush=True)
    elif done:
        print(sh("cd /opt/abra-v3 && for b in A B; do ./fvB.sh true; ./fv$b.sh 'touch /workspace/cfbundle/KF_DONE && echo KF_DONE_$(hostname)'; done | grep KF_DONE"), flush=True); break
    time.sleep(60)
