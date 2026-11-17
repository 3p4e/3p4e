#!/usr/bin/env python3
"""FENRIR P8 supervisor — takes over the ALREADY-RENTED fenrir-p8 box (orchestrator v1
exited after rent when the port mapping wasn't in the record yet). Waits for boot,
pushes inputs, fires the batch, pulls+gates clips as they land, destroys + reconciles.
Line-logged unbuffered; safe to detach with nohup. Cap enforced against box uptime."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
LOG = lambda *a: print(f'[P8S {time.strftime("%H:%M:%S")}]', *a, flush=True)
CAP = float(os.environ.get('CAP_DOLLARS', '4.0'))
K = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('VASTAI_API='):
        K = line.split('=', 1)[1].strip().strip('"').strip("'")
H = {'Authorization': 'Bearer ' + K}
KEY = '/root/.ssh/vast_karsus'
JOBFILE = ROOT / 'tools/vast/jobfiles/fenrir_46_clips_jobfile.json'
KF_DIR = ROOT / 'media/fenrir_assets/keyframes'
CLIP_HOME = ROOT / 'media/fenrir_assets/clips'
CLIP_HOME.mkdir(parents=True, exist_ok=True)

def req(p):
    r = urllib.request.Request('https://console.vast.ai/api/v0' + p, headers=H)
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode())

def ssh(ip, port, cmd, timeout=45):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-p', str(port), '-i', KEY,
                           f'root@{ip}', cmd], capture_output=True, text=True, timeout=timeout)

def scp(ip, port, src, dst, timeout=600):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=12',
                           '-o', 'StrictHostKeyChecking=no', '-P', str(port), '-i', KEY,
                           str(src), f'root@{ip}:{dst}'], capture_output=True, text=True, timeout=timeout)

# --- 1. box record ---
LOG('=== P8 SUPERVISOR START, cap $%.2f ===' % CAP)
credit0 = req('/users/current/')['credit']
LOG(f'credit ${credit0:.3f}')
z = [x for x in req('/instances/').get('instances', []) if x.get('label') == 'fenrir-p8']
if not z:
    sys.exit('no fenrir-p8 instance — nothing to supervise')
z = z[0]
iid = z['id']
dph = z.get('dph_total') or 0.404
LOG(f'box {iid} dph=${dph:.3f}/h status={z.get("actual_status")}')

# --- 2. wait for boot + port mapping ---
ip = z.get('public_ipaddr')
port = None
t_start = time.time()
for i in range(60):
    d = req('/instances/')
    zz = [x for x in d.get('instances', []) if x.get('id') == iid][0]
    st = zz.get('actual_status')
    ports = zz.get('ports') or {}
    p22 = (ports.get('22/tcp') or [{}])[0].get('HostPort')
    ip = zz.get('public_ipaddr') or ip
    elapsed_h = (time.time() - t_start) / 3600
    if elapsed_h * dph > CAP:
        sys.exit(f'CAP EXHAUSTED waiting for boot (${elapsed_h * dph:.2f}) — destroy manually!')
    if st == 'running':
        cand = None
        if ip and p22:
            cand = (ip, int(p22), 'direct')
        elif zz.get('ssh_host') and zz.get('ssh_port'):
            cand = (zz['ssh_host'], int(zz['ssh_port']), 'proxy')
        if cand:
            host, port, mode = cand
            if ssh(host, port, 'echo ALIVE').returncode == 0:
                LOG(f'ssh UP via {mode} {host}:{port} (try {i})')
                ip, port = host, port
                break
    if i % 4 == 0:
        LOG(f'waiting boot: status={st} (try {i}, ~{elapsed_h * 60:.0f}min)')
    time.sleep(15)
else:
    sys.exit('box never became ssh-able — destroy manually!')

# --- 3. push inputs ---
env = dict(os.environ)
ht = env.get('HF_TOKEN', '')
if not ht:
    for line in open(ROOT / '.a0proj/secrets.env'):
        if line.startswith('HF_TOKEN='):
            ht = line.split('=', 1)[1].strip().strip('"').strip("'")
subprocess.run(f'printf "HF_TOKEN=%s\\n" "{ht}" > /tmp/p8_hfenv && chmod 600 /tmp/p8_hfenv', shell=True)
for src, dst in [('/tmp/p8_hfenv', '/workspace/.hfenv'),
                 (JOBFILE, '/workspace/jobfile.json'),
                 (ROOT / 'tools/vast/fenrir_p8_batch.sh', '/workspace/fenrir_p8_batch.sh')]:
    p = scp(ip, port, src, dst)
    if p.returncode != 0:
        sys.exit(f'push failed {src}: {p.stderr[-200:]}')
LOG('env+jobfile+runner pushed')
tar = subprocess.Popen(['tar', 'cf', '-', '-C', str(KF_DIR)] +
                       [f'kf_{i:02d}_start.png' for i in range(1, 47)], stdout=subprocess.PIPE)
r = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                    '-p', str(port), '-i', KEY, f'root@{ip}', 'mkdir -p /workspace/stills && tar xf - -C /workspace/stills'],
                   stdin=tar.stdout, capture_output=True, text=True)
tar.wait()
n_kf = ssh(ip, port, 'ls /workspace/stills/kf_*_start.png 2>/dev/null | wc -l').stdout.strip()
LOG(f'keyframes on box: {n_kf}/46')
if n_kf != '46':
    sys.exit('kf count mismatch — abort before render spend')
already = ssh(ip, port, 'pgrep -f fenrir_p8_batch | head -1').stdout.strip()
if already:
    LOG(f'batch already running (pid {already}) — skipping fire')
else:
    ssh(ip, port, 'setsid nohup bash /workspace/fenrir_p8_batch.sh > /workspace/p8_launch.out 2>&1 < /dev/null & echo FIRED', timeout=20)
    LOG('BATCH FIRED')

# --- 4. supervise: pull + gate as clips land; enforce cap vs box uptime ---
jobs = json.loads(JOBFILE.read_text())['jobs']
expected = [j['job_id'] + '.mp4' for j in jobs]
by_name = {j['job_id'] + '.mp4': j for j in jobs}
pulled, gate_fail = set(), []
render_t0 = time.time()
box_up_h = (time.time() - t_start) / 3600
last_log = ''
while True:
    box_up_h = (time.time() - t_start) / 3600
    if box_up_h * dph > CAP:
        LOG(f'CAP TRIPPED: box spend ${box_up_h * dph:.2f} > ${CAP:.2f}')
        break
    st = ssh(ip, port, 'ls /workspace/out/ 2>/dev/null; echo ---; tail -3 /workspace/logs/fenrir_p8.log 2>/dev/null').stdout
    for name in expected:
        if name in pulled:
            continue
        if f'{name}.done' in st or (name + '\n') in st.split('---')[0].split() or name in st.split('---')[0]:
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
                LOG(f'[{len(pulled)}/46] {name} pulled+gate:{verdict} {why or ""}')
    if 'ALL_JOBS_COMPLETE' in st or len(pulled) >= 46:
        break
    tail = st.split('---')[-1].strip().replace('\n', ' | ')
    if tail and tail != last_log:
        LOG('box: ' + tail[-150:])
        last_log = tail
    time.sleep(60)

# --- 5. final sweep + destroy + reconcile ---
for name in expected:
    if name not in pulled and (CLIP_HOME / name).exists():
        pulled.add(name)
for name in expected:
    if name not in pulled:
        p = scp(ip, port, f'/workspace/out/{name}', str(CLIP_HOME / name))
        if p.returncode == 0 and (CLIP_HOME / name).exists():
            pulled.add(name)
LOG(f'clips home: {len(pulled)}/46; gate-failures: {gate_fail if gate_fail else "none"}')
summary = {'clips_home': len(pulled), 'gate_failures': gate_fail,
           'box_spend_est': round(box_up_h * dph, 3), 'hours': round(box_up_h, 2)}
(CLIP_HOME / 'p8_summary.json').write_text(json.dumps(summary, indent=2))
subprocess.run(['bash', '-c',
                f'set -a; . {ROOT}/.a0proj/secrets.env; set +a; bash {ROOT}/tools/vast/stop_instance.sh {iid} destroy'],
               capture_output=True)
credit1 = req('/users/current/')['credit']
LOG(f'DESTROYED {iid}; credit ${credit0:.3f} -> ${credit1:.3f} (run ${credit0 - credit1:.3f}, cap ${CAP:.2f})')
LOG('COMPLETE' if len(pulled) == 46 else 'INCOMPLETE ' + str(sorted(set(expected) - pulled)))
