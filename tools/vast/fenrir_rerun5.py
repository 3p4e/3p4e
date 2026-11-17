#!/usr/bin/env python3
"""FENRIR re-render 5 flagged clips + KEEP BOX ALIVE for the audio phase.
Rent cheapest 48GB host -> cuda compat if needed -> push 5 kf + 5-job jobfile ->
render -> pull to clips/rerun/ -> gate (fixed gate) -> on PASS archive v1 + swap ->
DO NOT DESTROY: write .fenrir_rerun5_box.json for the audio phase, per director.
GO=1 required. Cap via CAP_DOLLARS (default 1.5)."""
import json, os, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
LOG = lambda *a: print(f'[RERUN5 {time.strftime("%H:%M:%S")}]', *a, flush=True)
if os.environ.get('GO') != '1':
    sys.exit('refusing: GO=1 required')
CAP = float(os.environ.get('CAP_DOLLARS', '1.5'))
MAXPRICE = float(os.environ.get('MAXPRICE', '0.85'))
K = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('VASTAI_API='):
        K = line.split('=', 1)[1].strip().strip('"').strip("'")
H = {'Authorization': 'Bearer ' + K, 'Content-Type': 'application/json'}
KEY = '/root/.ssh/vast_karsus'
JOBFILE = ROOT / 'tools/vast/jobfiles/fenrir_rerun5_jobfile.json'
KF_DIR = ROOT / 'media/fenrir_assets/keyframes'
CLIPDIR = ROOT / 'media/fenrir_assets/clips'
RERUN = CLIPDIR / 'rerun'
RERUN.mkdir(exist_ok=True)
SHOOTS = [5, 15, 16, 17, 46]

def req(p, b=None, m='GET', tries=4):
    last = None
    for t in range(tries):
        try:
            r = urllib.request.Request('https://console.vast.ai/api/v0' + p,
                                       data=json.dumps(b).encode() if b is not None else None,
                                       headers=H, method=m)
            return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())
        except Exception as e:
            last = str(e)
            LOG(f'API retry {t+1}/{tries} {p}: {last[:160]}')
            time.sleep(2 * (t + 1))
    sys.exit(f'API gave up on {p}: {last}')

def ssh(ip, port, cmd, timeout=45):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-p', str(port), '-i', KEY,
                           f'root@{ip}', cmd], capture_output=True, text=True, timeout=timeout)

def scp_to(ip, port, src, dst, timeout=900):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                           '-P', str(port), '-i', KEY, str(src), f'root@{ip}:{dst}'],
                          capture_output=True, text=True, timeout=timeout)

def scp_from(ip, port, remote, local, timeout=600):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                           '-P', str(port), '-i', KEY, f'root@{ip}:{remote}', str(local)],
                          capture_output=True, text=True, timeout=timeout)

LOG(f'=== RERUN5 START cap ${CAP:.2f} ===')
c0 = req('/users/current/')['credit']
LOG(f'credit ${c0:.3f}')

q = {'num_gpus': {'eq': 1}, 'rentable': {'eq': True}, 'rented': {'eq': False},
     'verified': {'eq': True}, 'gpu_ram': {'gte': 44000}, 'disk_space': {'gte': 160},
     'reliability2': {'gte': 0.95}, 'cpu_arch': {'eq': 'amd64'}, 'type': 'ondemand', 'limit': 300,
     'order': [['dph_total', 'asc']]}
offers = req('/bundles/', q, 'POST').get('offers', [])
bad = {'Tesla V100', 'Q RTX 8000', 'CMP 170HX', 'Titan RTX', 'Tesla P40', 'Tesla P100'}
BROKEN = {'38.29.145.10'}
PROJ_H = 1.5
cands = []
for x in offers:
    if x['gpu_name'] in bad or x['dph_total'] > MAXPRICE:
        continue
    if (x.get('cpu_ram') or 0) / 1024 < 32 or (x.get('cpu_cores_effective') or 0) < 8:
        continue
    if (x.get('inet_down') or 0) < 2000:
        continue
    if str(x.get('ssh_host') or x.get('public_ipaddr') or '') in BROKEN:
        continue
    proj = (x['dph_total'] + PROJ_H * ((x.get('inet_down_cost') or 0) + (x.get('inet_up_cost') or 0))) * PROJ_H
    if proj <= CAP:
        x['_proj'] = proj
        cands.append(x)
cands.sort(key=lambda c: c['_proj'])
for x in cands[:4]:
    LOG(f"cand {x['id']} {x['gpu_name']} ${x['dph_total']:.3f}/h proj=${x['_proj']:.2f} {x.get('geolocation')}")
if not cands:
    sys.exit('no candidate — not renting')
x = cands[0]

PUB = open('/root/.ssh/vast_karsus.pub').read().strip()
PUB2 = open('/root/.ssh/vast_rsa.pub').read().strip()
onstart = ('#!/bin/bash\nmkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/models /workspace/logs\n'
           f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
           f"echo '{PUB2}' >> /root/.ssh/authorized_keys\n"
           'chmod 700 /root/.ssh; chmod 600 /root/.ssh/authorized_keys\n')
r = req(f"/asks/{x['id']}/", {'template_hash_id': '2188dfd3e0a0b83691bb468ddae0a4e5',
                             'disk': 160, 'label': 'fenrir-rerun5', 'onstart': onstart}, 'PUT')
if 'new_contract' not in r:
    sys.exit(f'rent failed: {json.dumps(r)[:300]}')
iid = r['new_contract']
box_t0 = time.time()
LOG(f"rented offer {x['id']} -> {iid} (${x['dph_total']:.3f}/h)")

ip = port = None
for i in range(80):
    d = req('/instances/')
    zz = [z for z in d.get('instances', []) if z.get('id') == iid]
    if not zz:
        sys.exit('instance vanished')
    zz = zz[0]
    ports = zz.get('ports') or {}
    p22 = (ports.get('22/tcp') or [{}])[0].get('HostPort')
    ip = zz.get('public_ipaddr') or ip
    up_h = (time.time() - box_t0) / 3600
    if up_h * x['dph_total'] > CAP:
        sys.exit(f'CAP during boot ${up_h * x["dph_total"]:.2f} — close manually')
    if zz.get('actual_status') == 'running':
        cand = (ip, int(p22)) if ip and p22 else \
               ((zz['ssh_host'], int(zz['ssh_port'])) if zz.get('ssh_host') and zz.get('ssh_port') else None)
        if cand and ssh(cand[0], cand[1], 'echo ALIVE').returncode == 0:
            ip, port = cand
            LOG(f'ssh UP {ip}:{port} (try {i})')
            break
    time.sleep(15)
else:
    sys.exit('never ssh-able')

cuda_ok = ssh(ip, port,
              'cd /workspace 2>/dev/null; test -d LTX-2 || git clone --depth 1 https://github.com/Lightricks/LTX-2.git;'
              ' cd LTX-2 && (test -d .venv || uv sync 2>&1 | tail -2);'
              ' ./.venv/bin/python -c "import torch;print(\"CUDA\", torch.cuda.is_available())" 2>/dev/null | tail -1',
              timeout=900).stdout
LOG('torch:', cuda_ok.strip().splitlines()[-1] if cuda_ok.strip() else 'NO_OUTPUT')
if 'CUDA True' not in cuda_ok:
    ssh(ip, port, 'apt-get update -qq 2>&1 | tail -1; apt-get install -y -qq cuda-compat-13-2 2>&1 | tail -2;'
                  " echo '/usr/local/cuda-13.2/compat' > /etc/ld.so.conf.d/cuda-compat.conf; ldconfig", timeout=600)
    v = ssh(ip, port, 'export LD_LIBRARY_PATH=/usr/local/cuda-13.2/compat:$LD_LIBRARY_PATH;'
                      ' /workspace/LTX-2/.venv/bin/python -c "import torch;print(\'CUDA\', torch.cuda.is_available())"').stdout
    LOG('post-repair:', v.strip())
    if 'CUDA True' not in v:
        sys.exit('cuda unrecoverable — close box manually')

# push hf token + jobfile + render_lib + fixed batch
tok = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('HF_TOKEN='):
        tok = line.split('=', 1)[1].strip().strip('"').strip("'")
subprocess.run(f'printf "HF_TOKEN=%s\\n" "{tok}" > /tmp/r5_hfenv && chmod 600 /tmp/r5_hfenv', shell=True)
for src, dst in [('/tmp/r5_hfenv', '/workspace/.hfenv'), (JOBFILE, '/workspace/jobfile.json'),
                 ('/tmp/render_lib.sh', '/workspace/render_lib.sh'),
                 ('/tmp/fenrir_p8_batch_fixed2.sh', '/workspace/fenrir_p8_batch.sh')]:
    p = scp_to(ip, port, src, dst)
    if p.returncode != 0:
        sys.exit(f'push failed {src}')

names = [f'kf_{i:02d}_start.png' for i in SHOOTS]
tar = subprocess.Popen(['tar', 'cf', '-', '-C', str(KF_DIR)] + names, stdout=subprocess.PIPE)
subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no', '-p', str(port),
                '-i', KEY, f'root@{ip}', 'mkdir -p /workspace/stills && tar xf - -C /workspace/stills'],
               stdin=tar.stdout, capture_output=True, timeout=300)
tar.wait()
n_kf = ssh(ip, port, 'ls /workspace/stills/kf_*_start.png 2>/dev/null | wc -l').stdout.strip()
LOG(f'kf on box: {n_kf}/5')
if n_kf != '5':
    sys.exit('kf mismatch — abort')
ssh(ip, port, 'rm -f /workspace/out/manifest.tsv /workspace/out/SHA256SUMS.txt /workspace/out/*.done;'
              ' chmod +x /workspace/fenrir_p8_batch.sh;'
              ' cd /workspace && setsid nohup bash /workspace/fenrir_p8_batch.sh > /workspace/p8_launch.out 2>&1 < /dev/null & echo FIRED', timeout=60)
LOG('BATCH FIRED (5 clips)')

jobs = json.loads(JOBFILE.read_text())['jobs']
expected = [j['job_id'] + '.mp4' for j in jobs]
pulled, gate_fail = set(), []
last = ''
while True:
    up_h = (time.time() - box_t0) / 3600
    if up_h * x['dph_total'] > CAP:
        LOG(f'CAP TRIP ${up_h * x["dph_total"]:.2f}')
        break
    st = ssh(ip, port, 'cat /workspace/out/manifest.tsv 2>/dev/null').stdout
    rows = [l for l in st.splitlines() if ' rc=' in l and 'FAILED' not in l]
    for name in expected:
        if name in pulled or not any(name in l for l in rows):
            continue
        p = scp_from(ip, port, f'/workspace/out/{name}', RERUN / name)
        dst = RERUN / name
        if p.returncode == 0 and dst.exists() and dst.stat().st_size > 100000:
            pulled.add(name)
            gr = subprocess.run([sys.executable, '-u', str(ROOT / 'tools/gate_fenrir_motion.py'),
                                 str(dst), str(RERUN)], capture_output=True, text=True)
            verdict, why = 'UNPARSED', ''
            try:
                g = json.loads(gr.stdout[gr.stdout.index('{'):])
                verdict, why = g['verdict'], g.get('reasons')
                if verdict != 'PASS':
                    gate_fail.append((name, why))
            except Exception:
                pass
            LOG(f'[{len(pulled)}/5] {name} gate:{verdict} {why or ""}')
    state = f'{len(rows)} rendered {len(pulled)} pulled'
    if state != last:
        LOG(f'box: {state} (~{up_h*60:.0f}min)')
        last = state
    if len(rows) >= 5:
        break
    time.sleep(45)

for name in expected:
    if name not in pulled:
        scp_from(ip, port, f'/workspace/out/{name}', RERUN / name)
        if (RERUN / name).exists():
            pulled.add(name)

# swap on PASS: archive v1, move rerun into place
ARCH = CLIPDIR / 'archive_v1'
ARCH.mkdir(exist_ok=True)
swapped = []
for name in pulled:
    stem = Path(name).stem
    orig, new = CLIPDIR / name, RERUN / name
    if not new.exists():
        continue
    gr = subprocess.run([sys.executable, '-u', str(ROOT / 'tools/gate_fenrir_motion.py'),
                         str(new), str(RERUN)], capture_output=True, text=True)
    try:
        g = json.loads(gr.stdout[gr.stdout.index('{'):])
    except Exception:
        g = {'verdict': 'UNPARSED'}
    if g['verdict'] == 'PASS' and orig.exists():
        shutil.copy2(orig, ARCH / f'{stem}_v1.mp4')
        shutil.copy2(new, orig)
        swapped.append(stem)
        LOG(f'SWAPPED {stem} (v1 -> archive_v1)')
    else:
        LOG(f'KEPT v1 for {stem} (rerun gate: {g.get("verdict")} {g.get("reasons")})')

# KEEP BOX ALIVE — record for the audio phase, NO destroy
rec = {'instance_id': iid, 'ip': ip, 'port': port, 'gpu': x['gpu_name'],
       'dph_total': x['dph_total'], 'rented_at': time.strftime('%FT%TZ', time.gmtime(box_t0)),
       'purpose': 'rerun5 + audio generation phase (director keep-alive)',
       'ssh': f'ssh -p {port} -i /root/.ssh/vast_karsus root@{ip}'}
(ROOT / '.fenrir_rerun5_box.json').write_text(json.dumps(rec, indent=2))
LOG(f'KEPT ALIVE {iid} for audio phase -> .fenrir_rerun5_box.json')
c1 = req('/users/current/')['credit']
LOG(f'credit ${c0:.3f} -> ${c1:.3f} (rerun ${c0 - c1:.3f})')
LOG('COMPLETE' if len(swapped) == 5 else f'PARTIAL swapped={swapped}')
