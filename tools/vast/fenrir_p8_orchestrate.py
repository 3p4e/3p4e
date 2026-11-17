#!/usr/bin/env python3
"""FENRIR P8 one-command orchestrator. Fires ONLY on explicit director GO.

Usage: GO=1 CAP_DOLLARS=4.0 python3 tools/vast/fenrir_p8_orchestrate.py
Supervised cycle: rent 48GB host -> push 46 kf + jobfile + runner -> batch render
-> incremental scp pull home as clips land -> per-clip motion gate -> destroy + reconcile.
Refuses to run without GO=1 in env (spend gate). Refuses if any fenrir-p8/p7 label exists.
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
if os.environ.get('GO') != '1':
    sys.exit('refusing: set GO=1 (explicit director approval required)')
CAP = float(os.environ.get('CAP_DOLLARS', '4.0'))
MAXPRICE = float(os.environ.get('MAXPRICE', '0.60'))
LABEL = 'fenrir-p8'
JOBFILE = ROOT / 'tools/vast/jobfiles/fenrir_46_clips_jobfile.json'
KF_DIR = ROOT / 'media/fenrir_assets/keyframes'
CLIP_HOME = ROOT / 'media/fenrir_assets/clips'
CLIP_HOME.mkdir(parents=True, exist_ok=True)
K = os.environ['VASTAI_API']
H = {'Authorization': 'Bearer ' + K, 'Content-Type': 'application/json'}
TEMPLATE = '2188dfd3e0a0b83691bb468ddae0a4e5'
KEY = '/root/.ssh/vast_karsus'

def req(m, p, b=None):
    r = urllib.request.Request('https://console.vast.ai/api/v0' + p,
                               data=json.dumps(b).encode() if b is not None else None,
                               headers=H, method=m)
    return json.loads(urllib.request.urlopen(r, timeout=90).read().decode())

def ssh(ip, port, cmd, timeout=40):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-p', str(port), '-i', KEY,
                           f'root@{ip}', cmd], capture_output=True, text=True, timeout=timeout)

def scp(ip, port, src, dst, timeout=300):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-P', str(port), '-i', KEY,
                           str(src), f'root@{ip}:{dst}'], capture_output=True, text=True, timeout=timeout)

print(f'== P8 ORCHESTRATOR == cap ${CAP:.2f} maxprice ${MAXPRICE:.2f}/h')
credit0 = req('GET', '/users/current/')['credit']
print(f'credit ${credit0:.3f}')
insts = req('GET', '/instances/').get('instances', [])
if any(z.get('label', '').startswith('fenrir-p') for z in insts):
    sys.exit('refusing: a fenrir box already exists -> close it first')

q = {'num_gpus': {'eq': 1}, 'rentable': {'eq': True}, 'rented': {'eq': False},
     'verified': {'eq': True}, 'gpu_ram': {'gte': 44000}, 'disk_space': {'gte': 160},
     'reliability2': {'gte': 0.95}, 'type': 'ondemand', 'limit': 300,
     'order': [['dph_total', 'asc']]}
offers = req('POST', '/bundles/', q).get('offers', [])
bad = {'Tesla V100', 'Q RTX 8000', 'CMP 170HX', 'Titan RTX', 'Tesla P40', 'Tesla P100'}
c = [x for x in offers if x['dph_total'] <= MAXPRICE and x['gpu_name'] not in bad
     and (x.get('cpu_ram') or 0) / 1024 >= 32 and (x.get('cpu_cores_effective') or 0) >= 8
     and (x.get('inet_down') or 0) >= 2000]
if not c:
    sys.exit('no candidate offer')
x = c[0]
print(f"renting offer {x['id']}: {x['gpu_name']} {x['gpu_ram']/1024:.0f}GB ${x['dph_total']:.3f}/h")
PUB = open('/root/.ssh/vast_karsus.pub').read().strip()
PUB2 = open('/root/.ssh/vast_rsa.pub').read().strip()
onstart = ('#!/bin/bash\nmkdir -p /root/.ssh /workspace/out /workspace/stills /workspace/models\n'
           f"echo '{PUB}' > /root/.ssh/authorized_keys\n"
           f"echo '{PUB2}' >> /root/.ssh/authorized_keys\n"
           'chmod 700 /root/.ssh; chmod 600 /root/.ssh/authorized_keys\n')
r = req('PUT', f"/asks/{x['id']}/", {'template_hash_id': TEMPLATE, 'disk': 160, 'label': LABEL, 'onstart': onstart})
if 'new_contract' not in r:
    sys.exit(f'rent failed: {json.dumps(r)[:300]}')
time.sleep(25)
z = [i for i in req('GET', '/instances/').get('instances', []) if i.get('label') == LABEL][0]
iid, ip, port = z['id'], z.get('public_ipaddr'), None
for k, v in (z.get('ports') or {}).get('22/tcp', []):
    port = int(v['HostPort']); break
if not ip or not port:
    sys.exit(f'no direct ip/port in record: {json.dumps(z.get("ports"))[:300]}')
print(f'box {iid} at {ip}:{port} — waiting for sshd')
for _ in range(20):
    if ssh(ip, port, 'echo ALIVE').returncode == 0:
        break
    time.sleep(15)
else:
    sys.exit('sshd never came up')

print('pushing inputs')
subprocess.run('printf "HF_TOKEN=%s\\n" "$HF_TOKEN" > /tmp/p8_hfenv && chmod 600 /tmp/p8_hfenv', shell=True)
for src, dst in [('/tmp/p8_hfenv', '/workspace/.hfenv'),
                 (JOBFILE, '/workspace/jobfile.json'),
                 (ROOT / 'tools/vast/fenrir_p8_batch.sh', '/workspace/fenrir_p8_batch.sh')]:
    p = scp(ip, port, src, dst)
    if p.returncode != 0:
        sys.exit(f'push failed {src}: {p.stderr[-200:]}')
subprocess.run(['bash', '-c',
    f'ssh -o BatchMode=yes -o StrictHostKeyChecking=no -p {port} -i {KEY} root@{ip} '
    f'"mkdir -p /workspace/stills && cat > /dev/null"'], timeout=30)
tar = subprocess.Popen(['tar', 'cf', '-', '-C', str(KF_DIR)] +
                       sorted(f'kf_{i:02d}_start.png' for i in range(1, 47)), stdout=subprocess.PIPE)
ssh_r = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                        '-p', str(port), '-i', KEY, f'root@{ip}', 'tar xf - -C /workspace/stills'],
                       stdin=tar.stdout, capture_output=True, text=True)
tar.wait()
if ssh_r.returncode != 0:
    sys.exit('kf push failed')
n_kf = ssh(ip, port, 'ls /workspace/stills/kf_*_start.png 2>/dev/null | wc -l').stdout.strip()
print(f'keyframes on box: {n_kf}/46')
if n_kf != '46':
    sys.exit('kf count mismatch — abort before spend')
ssh(ip, port, 'chmod +x /workspace/fenrir_p8_batch.sh && nohup bash /workspace/fenrir_p8_batch.sh > /workspace/p8_launch.out 2>&1 & echo FIRED')

t0 = time.time()
done_seen, pulled = set(), set()
jobs = json.loads(JOBFILE.read_text())['jobs']
expected = {j['job_id'] + '.mp4' for j in jobs}
failed = []
while True:
    elapsed_h = (time.time() - t0) / 3600
    spent = elapsed_h * x['dph_total']
    if spent > CAP:
        print(f'CAP TRIPPED: projected spend ${spent:.2f} > ${CAP:.2f} — destroying')
        break
    st = ssh(ip, port, 'ls /workspace/out/ 2>/dev/null; echo ---; tail -2 /workspace/logs/fenrir_p8.log 2>/dev/null').stdout
    for name in sorted(expected - pulled):
        if f'{name}.done' in st or name in st:
            p = scp(ip, port, f'/workspace/out/{name}', str(CLIP_HOME / name), timeout=600)
            if p.returncode == 0 and (CLIP_HOME / name).stat().st_size > 100000:
                pulled.add(name)
                print(f'[{len(pulled)}/46] pulled {name}')
                grun = subprocess.run([sys.executable, str(ROOT / 'tools/gate_fenrir_motion.py'),
                                       str(CLIP_HOME / name), str(CLIP_HOME)],
                                      capture_output=True, text=True)
                try:
                    g = json.loads(grun.stdout[grun.stdout.index('{'):])
                    print(f'    gate {name}: {g["verdict"]} motion={g["motion_mean"]} flicker={g["luma_flicker"]}')
                    if g['verdict'] != 'PASS':
                        failed.append((name, g.get('reasons')))
                except Exception:
                    print('    gate parse issue (non-fatal)')
    if 'ALL_JOBS_COMPLETE' in st:
        print('batch complete marker seen')
        break
    if len(pulled) >= 46:
        print('all 46 clips home')
        break
    time.sleep(60)

final = ssh(ip, port, 'cat /workspace/out/manifest.tsv 2>/dev/null; ls /workspace/out/*.mp4 2>/dev/null | wc -l').stdout
for name in expected - pulled:
    p = scp(ip, port, f'/workspace/out/{name}', str(CLIP_HOME / name), timeout=600)
    if p.returncode == 0:
        pulled.add(name)
print(f'clips home: {len(pulled)}/46')
print('manifest tail:', final[-400:])
subprocess.run(['bash', '-c',
    f'set -a; . {ROOT}/.a0proj/secrets.env; set +a; bash {ROOT}/tools/vast/stop_instance.sh {iid} destroy'],
    capture_output=True)
credit1 = req('GET', '/users/current/')['credit']
print(f'credit ${credit0:.3f} -> ${credit1:.3f}  (run cost ${credit0 - credit1:.3f}, cap ${CAP:.2f})')
print('BOX_DESTROYED', 'COMPLETE' if len(pulled) == 46 else f'INCOMPLETE {sorted(expected - pulled)}')
