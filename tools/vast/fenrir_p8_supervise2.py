#!/usr/bin/env python3
"""P8 supervise2 — manifest-driven tail for box 60343963. Pulls+gates each clip
as it lands; destroys at 46/46 or CAP; alerts if queue dies with <46 rows."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
ROOT = Path('/a0/usr/projects/vast')
IP, PORT, IID, DPH = '192.234.50.251', 1751, 60343963, 0.539
CAP = 2.50
CLIP = ROOT / 'media/fenrir_assets/clips'
CLIP.mkdir(parents=True, exist_ok=True)
LOG = lambda *a: print(f'[SUP2 {time.strftime("%H:%M:%S")}]', *a, flush=True)
K = ''
for line in open(ROOT / '.a0proj/secrets.env'):
    if line.startswith('VASTAI_API='):
        K = line.split('=', 1)[1].strip().strip('"').strip("'")
KEY = '/root/.ssh/vast_karsus'

def credit():
    r = urllib.request.Request('https://console.vast.ai/api/v0/users/current/',
                               headers={'Authorization': 'Bearer ' + K})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())['credit']

def ssh(cmd, timeout=45):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10',
                           '-o', 'StrictHostKeyChecking=no', '-p', str(PORT), '-i', KEY,
                           f'root@{IP}', cmd], capture_output=True, text=True, timeout=timeout)

def scp(src, dst, timeout=600):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                           '-P', str(PORT), '-i', KEY, src, f'root@{IP}:{dst}'],
                          capture_output=True, text=True, timeout=timeout)

def rscps(remote, local, timeout=600):
    return subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                           '-P', str(PORT), '-i', KEY, f'root@{IP}:{remote}', str(local)],
                          capture_output=True, text=True, timeout=timeout)

jobs = json.loads((ROOT / 'tools/vast/jobfiles/fenrir_46_clips_jobfile.json').read_text())['jobs']
expected = [j['job_id'] + '.mp4' for j in jobs]
pulled, gate_fail = set(), []
c0 = credit()
LOG(f'supervise2 start; credit ${c0:.3f}; cap ${CAP:.2f}')
t0 = time.time()
stall_min = 0
while True:
    spent = c0 - credit()
    if spent > CAP:
        LOG(f'CAP TRIP ${spent:.2f} — destroying')
        break
    st = ssh('cat /workspace/out/manifest.tsv 2>/dev/null; echo ===; ps aux | grep -c "[r]ender_queue"').stdout
    rows = [l for l in st.split('===')[0].splitlines() if ' rc=' in l and 'FAILED' not in l]
    for name in expected:
        if name in pulled:
            continue
        if any(name in l for l in rows):
            p = rscps(f'/workspace/out/{name}', CLIP / name)
            dst = CLIP / name
            if p.returncode == 0 and dst.exists() and dst.stat().st_size > 100000:
                pulled.add(name)
                gr = subprocess.run([sys.executable, '-u', str(ROOT / 'tools/gate_fenrir_motion.py'),
                                     str(dst), str(CLIP)], capture_output=True, text=True)
                verdict, why = 'UNPARSED', ''
                try:
                    g = json.loads(gr.stdout[gr.stdout.index('{'):])
                    verdict, why = g['verdict'], g.get('reasons')
                    if verdict != 'PASS':
                        gate_fail.append((name, why))
                except Exception:
                    pass
                LOG(f'[{len(pulled)}/46] {name} gate:{verdict} {why or ""}')
    if len(rows) >= 46:
        LOG('manifest 46/46 complete')
        break
    if '[r]ender_queue' in st and '0' == st.split('===')[1].strip() and not rows:
        stall_min += 1
        if stall_min >= 3:
            LOG('ALERT: queue dead, 0 rows — needs eyes; NOT destroying (no fake-complete)')
            stall_min = -999
    else:
        stall_min = 0
    time.sleep(60)
for name in expected:
    if name not in pulled:
        p = rscps(f'/workspace/out/{name}', CLIP / name)
        if p.returncode == 0 and (CLIP / name).exists():
            pulled.add(name)
LOG(f'clips home {len(pulled)}/46; gate-fails: {gate_fail if gate_fail else "none"}')
subprocess.run(['bash', '-c', f'set -a; . {ROOT}/.a0proj/secrets.env; set +a; bash {ROOT}/tools/vast/stop_instance.sh {IID} destroy'], capture_output=True)
c1 = credit()
LOG(f'DESTROYED {IID}; credit ${c0:.3f} -> ${c1:.3f} (batch ${c0 - c1:.3f})')
LOG('COMPLETE' if len(pulled) == 46 else 'INCOMPLETE ' + str(sorted(set(expected) - pulled)))
