#!/usr/bin/env python3
"""FENRIR P8 orchestrator v2 — corrected re-run. Rent (free-inet only) -> boot ->
auto CUDA-compat repair if needed -> push -> fire (fresh log) -> supervise (manifest-
based completion, min-time destroy guard) -> pull + gate -> destroy + reconcile.
Fires only with GO=1. Line-logged unbuffered."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
LOG = lambda *a: print(f'[P8V2 {time.strftime("%H:%M:%S")}]', *a, flush=True)
if os.environ.get('GO') != '1':
    sys.exit('refusing: GO=1 required')
CAP = float(os.environ.get('CAP_DOLLARS', '2.5'))
MAXPRICE = float(os.environ.get('MAXPRICE', '0.85'))
LABEL = 'fenrir-p8-v2'
MIN_BOX_MINUTES = 30
K = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('VASTAI_API='):
        K = line.split('=', 1)[1].strip().strip('"').strip("'")
H = {'Authorization': 'Bearer ' + K, 'Content-Type': 'application/json'}
KEY = '/root/.ssh/vast_karsus'
JOBFILE = ROOT / 'tools/vast/jobfiles/fenrir_46_clips_jobfile.json'
KF_DIR = ROOT / 'media/fenrir_assets/keyframes'
CLIP_HOME = ROOT / 'media/fenrir_assets/clips'
CLIP_HOME.mkdir(parents=True, exist_ok=True)

def req(p, b=None, m='GET', tries=4):
    last = None
    for t in range(tries):
        try:
            r = urllib.request.Request('https://console.vast.ai/api/v0' + p,
                                       data=json.dumps(b).encode() if b is not None else None,
                                       headers=H, method=m)
            return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())
        except urllib.error.HTTPError as e:
            last = f'HTTP {e.code}: {e.read().decode()[:300]}'
            LOG(f'API retry {t+1}/{tries} {p}: {last}')
            time.sleep(2 * (t + 1))
        except Exception as e:
            last = str(e)
            LOG(f'API retry {t+1}/{tries} {p}: {last}')
            time.sleep(2 * (t + 1))
    sys.exit(f'API gave up on {p}: {last}')

def ssh(ip, port, cmd, timeout=45):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-p', str(port), '-i', KEY,
                           f'root@{ip}', cmd], capture_output=True, text=True, timeout=timeout)

def scp(ip, port, src, dst, timeout=900):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-P', str(port), '-i', KEY,
                           str(src), f'root@{ip}:{dst}'], capture_output=True, text=True, timeout=timeout)

LOG(f'=== P8V2 START cap ${CAP:.2f} ===')
credit0 = req('/users/current/')['credit']
LOG(f'credit ${credit0:.3f}')
if any(z.get('label', '').startswith('fenrir-p8') for z in req('/instances/').get('instances', [])):
    sys.exit('a fenrir-p8 box exists — close it first')

q = {'num_gpus': {'eq': 1}, 'rentable': {'eq': True}, 'rented': {'eq': False},
     'verified': {'eq': True}, 'gpu_ram': {'gte': 44000}, 'disk_space': {'gte': 160},
     'reliability2': {'gte': 0.95}, 'type': 'ondemand', 'limit': 300,
     'order': [['dph_total', 'asc']]}
offers = req('/bundles/', q, 'POST').get('offers', [])
bad = {'Tesla V100', 'Q RTX 8000', 'CMP 170HX', 'Titan RTX', 'Tesla P40', 'Tesla P100'}
BROKEN = {'38.29.145.10'}  # prior paid-inet host
PROJ_H = 2.2  # projected box hours (pull + 46 clips)
FREE_INET = [x for x in offers if x['gpu_name'] not in bad
             and (x.get('cpu_ram') or 0) / 1024 >= 32 and (x.get('cpu_cores_effective') or 0) >= 8
             and (x.get('inet_down') or 0) >= 2000
             and str(x.get('ssh_host') or x.get('public_ipaddr') or '') not in BROKEN
             and (x['dph_total'] + PROJ_H * ((x.get('inet_down_cost') or 0) + (x.get('inet_up_cost') or 0))) * PROJ_H <= CAP]
for cand in FREE_INET:
    tot = (cand['dph_total'] + PROJ_H * ((cand.get('inet_down_cost') or 0) + (cand.get('inet_up_cost') or 0))) * PROJ_H
    cand['_proj'] = tot
FREE_INET = [c for c in FREE_INET if c['dph_total'] <= MAXPRICE]
FREE_INET.sort(key=lambda c: c['_proj'])
for x in FREE_INET[:4]:
    LOG(f"cand {x['id']} {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h "
        f"proj=${x.get('_proj', 0):.2f} {x.get('geolocation')}")
if not FREE_INET:
    sys.exit('no free-inet candidate — not renting (paid-inet lesson)')
x = FREE_INET[0]

PUB = open('/root/.ssh/vast_karsus.pub').read().strip()
PUB2 = open('/root/.ssh/vast_rsa.pub').read().strip()
onstart = ('#!/bin/bash\nmkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/models\n'
           f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
           f"echo '{PUB2}' >> /root/.ssh/authorized_keys\n"
           'chmod 700 /root/.ssh; chmod 600 /root/.ssh/authorized_keys\n')
r = req(f"/asks/{x['id']}/", {'template_hash_id': '2188dfd3e0a0b83691bb468ddae0a4e5',
                             'disk': 160, 'label': LABEL, 'onstart': onstart}, 'PUT')
if 'new_contract' not in r:
    sys.exit(f'rent failed: {json.dumps(r)[:300]}')
LOG(f"rented offer {x['id']} -> {r['new_contract']}")

iid = r['new_contract']
box_t0 = time.time()
ip = port = None
for i in range(80):
    d = req('/instances/')
    zz = [z for z in d.get('instances', []) if z.get('id') == iid]
    if not zz:
        sys.exit('instance vanished from API')
    zz = zz[0]
    st = zz.get('actual_status')
    ports = zz.get('ports') or {}
    p22 = (ports.get('22/tcp') or [{}])[0].get('HostPort')
    ip = zz.get('public_ipaddr') or ip
    up_h = (time.time() - box_t0) / 3600
    if up_h * x['dph_total'] > CAP:
        sys.exit(f'CAP during boot ${up_h * x["dph_total"]:.2f} — destroy manually')
    if st == 'running':
        cand = (ip, int(p22), 'direct') if ip and p22 else \
               ((zz['ssh_host'], int(zz['ssh_port']), 'proxy') if zz.get('ssh_host') and zz.get('ssh_port') else None)
        if cand and ssh(cand[0], cand[1], 'echo ALIVE').returncode == 0:
            ip, port, mode = cand
            LOG(f'ssh UP via {mode} {ip}:{port} (try {i})')
            break
    if i % 4 == 0:
        LOG(f'boot wait: {st} (~{up_h*60:.0f}min)')
    time.sleep(15)
else:
    sys.exit('never ssh-able')

cuda_ok = ssh(ip, port,
              'cd /workspace 2>/dev/null; test -d LTX-2 || git clone --depth 1 https://github.com/Lightricks/LTX-2.git;'
              ' cd LTX-2 && (uv sync 2>&1 | tail -2);'
              ' ./.venv/bin/python -c "import torch;print(\"CUDA\", torch.cuda.is_available())" 2>/dev/null | tail -1',
              timeout=600).stdout
LOG('torch check:', cuda_ok.strip().splitlines()[-1] if cuda_ok.strip() else 'NO_OUTPUT')
if 'CUDA True' not in cuda_ok:
    LOG('cuda False — applying compat-13-2 repair')
    ssh(ip, port, 'apt-get update -qq 2>&1 | tail -1; apt-get install -y -qq cuda-compat-13-2 2>&1 | tail -2;'
                  " echo '/usr/local/cuda-13.2/compat' > /etc/ld.so.conf.d/cuda-compat.conf; ldconfig", timeout=600)
    v = ssh(ip, port, 'export LD_LIBRARY_PATH=/usr/local/cuda-13.2/compat:$LD_LIBRARY_PATH;'
                      ' /workspace/LTX-2/.venv/bin/python -c "import torch;print(\'CUDA\', torch.cuda.is_available())"').stdout
    LOG('post-repair:', v.strip())
    if 'CUDA True' not in v:
        ssh(ip, port, f'setsid nohup bash -c "sleep 1; true" </dev/null >/dev/null 2>&1 &')
        req(f'/instances/{iid}/destroy/', None, 'DELETE') if False else None
        subprocess.run(['bash', '-c', f'set -a; . {ROOT}/.a0proj/secrets.env; set +a; bash {ROOT}/tools/vast/stop_instance.sh {iid} destroy'], capture_output=True)
        sys.exit('cuda unrecoverable on this host — destroyed, no render spend')

ht = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('HF_TOKEN='):
        ht = line.split('=', 1)[1].strip().strip('"').strip("'")
subprocess.run(f'printf "HF_TOKEN=%s\\n" "{ht}" > /tmp/p8v2_hfenv && chmod 600 /tmp/p8v2_hfenv', shell=True)
for src, dst in [('/tmp/p8v2_hfenv', '/workspace/.hfenv'), (JOBFILE, '/workspace/jobfile.json')]:
    p = scp(ip, port, src, dst)
    if p.returncode != 0:
        sys.exit(f'push failed {src}')
batch_local = ROOT / 'tools/vast/fenrir_p8_batch.sh'
batch_txt = batch_local.read_text()
if 'LD_LIBRARY_PATH' not in batch_txt.splitlines()[2]:
    batch_txt = batch_txt.replace('#!/bin/bash\n', '#!/bin/bash\nexport LD_LIBRARY_PATH=/usr/local/cuda-13.2/compat:$LD_LIBRARY_PATH\n', 1)
batch_txt = batch_txt.replace('uv sync 2>&1 | tail -4', 'test -d .venv || uv sync 2>&1 | tail -4')
batch_txt = batch_txt.replace('exec >> $LOG 2>&1', 'rm -f $LOG\nexec >> $LOG 2>&1')
subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no', '-P', str(port),
                '-i', KEY, '/dev/stdin', f'root@{ip}:/workspace/fenrir_p8_batch.sh'],
               input=batch_txt.encode(), timeout=60)
tar = subprocess.Popen(['tar', 'cf', '-', '-C', str(KF_DIR)] +
                       [f'kf_{i:02d}_start.png' for i in range(1, 47)], stdout=subprocess.PIPE)
subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no', '-p', str(port),
                '-i', KEY, f'root@{ip}', 'mkdir -p /workspace/stills && tar xf - -C /workspace/stills'],
               stdin=tar.stdout, capture_output=True, timeout=300)
tar.wait()
n_kf = ssh(ip, port, 'ls /workspace/stills/kf_*_start.png 2>/dev/null | wc -l').stdout.strip()
LOG(f'kf on box: {n_kf}/46')
if n_kf != '46':
    sys.exit('kf mismatch — abort before render spend')
ssh(ip, port, 'chmod +x /workspace/fenrir_p8_batch.sh && setsid nohup bash /workspace/fenrir_p8_batch.sh > /workspace/p8_launch.out 2>&1 < /dev/null & echo FIRED', timeout=20)
LOG('BATCH FIRED')

jobs = json.loads(JOBFILE.read_text())['jobs']
expected = [j['job_id'] + '.mp4' for j in jobs]
pulled, gate_fail = set(), []
last_state = ''
while True:
    up_h = (time.time() - box_t0) / 3600
    if up_h * x['dph_total'] > CAP:
        LOG(f'CAP TRIPPED ${up_h * x["dph_total"]:.2f}')
        break
    st = ssh(ip, port, 'cat /workspace/out/manifest.tsv 2>/dev/null; echo ===; tail -2 /workspace/logs/fenrir_p8.log 2>/dev/null').stdout
    man = st.split('===')[0]
    done_rows = [l for l in man.splitlines() if ' rc=' in l and 'FAILED' not in l]
    for name in expected:
        if name in pulled:
            continue
        if any(name in l for l in done_rows):
            p = scp(ip, port, f'/workspace/out/{name}', str(CLIP_HOME / name))
            dst = CLIP_HOME / name
            if p.returncode == 0 and dst.exists() and dst.stat().st_size > 100000:
                pulled.add(name)
                gr = subprocess.run([sys.executable, '-u', str(ROOT / 'tools/gate_fenrir_motion.py'),
                                     str(dst), str(CLIP_HOME)], capture_output=True, text=True)
                verdict, why = 'UNPARSED', ''
                try:
                    g = json.loads(gr.stdout[gr.stdout.index('{'):])
                    verdict, why = g['verdict'], g.get('reasons')
                    if verdict != 'PASS':
                        gate_fail.append((name, why))
                except Exception:
                    pass
                LOG(f'[{len(pulled)}/46] {name} gate:{verdict} {why or ""}')
    state = f'{len(done_rows)} rendered, {len(pulled)} pulled'
    if state != last_state:
        LOG(f'box: {state} (~{up_h*60:.0f}min, ~${up_h * x["dph_total"]:.2f})')
        last_state = state
    n_done = len(done_rows)
    if n_done >= 46:
        LOG('manifest complete 46/46')
        break
    if 'ALL_JOBS_COMPLETE' in st.split('===')[1] and up_h * 60 < MIN_BOX_MINUTES:
        LOG(f'ALL_JOBS_COMPLETE but box only {up_h*60:.0f}min old — waiting for manifest')
    time.sleep(60)

for name in expected:
    if name not in pulled:
        p = scp(ip, port, f'/workspace/out/{name}', str(CLIP_HOME / name))
        if p.returncode == 0 and (CLIP_HOME / name).exists():
            pulled.add(name)
LOG(f'clips home: {len(pulled)}/46; gate-failures: {gate_fail if gate_fail else "none"}')
(CLIP_HOME / 'p8_v2_summary.json').write_text(json.dumps(
    {'clips_home': len(pulled), 'gate_failures': gate_fail,
     'host': f"{x['gpu_name']} ${x['dph_total']:.3f}/h free-inet", 'box': iid,
     'hours': round(up_h, 2)}, indent=2))
subprocess.run(['bash', '-c', f'set -a; . {ROOT}/.a0proj/secrets.env; set +a; bash {ROOT}/tools/vast/stop_instance.sh {iid} destroy'], capture_output=True)
credit1 = req('/users/current/')['credit']
LOG(f'DESTROYED {iid}; credit ${credit0:.3f} -> ${credit1:.3f} (run ${credit0 - credit1:.3f})')
LOG('COMPLETE' if len(pulled) == 46 else 'INCOMPLETE ' + str(sorted(set(expected) - pulled)))
