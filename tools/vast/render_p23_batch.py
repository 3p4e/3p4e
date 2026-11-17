#!/usr/bin/env python3
import json, subprocess, sys, os, time

JOBFILE = sys.argv[1] if len(sys.argv) > 1 else '/workspace/p23_batch60_v4.json'
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 60

PY = '/workspace/LTX-2/.venv/bin/python'
MODELS = '/workspace/models/ltx23'
STRENGTH = os.environ.get('STRENGTH', '0.5')

jobs = json.load(open(JOBFILE))
jobs = sorted([j for j in jobs if START <= j['n'] <= END], key=lambda j: j['n'])
print(f'[BATCH] jobfile={JOBFILE} range={START}-{END} count={len(jobs)} strength={STRENGTH}', flush=True)

for j in jobs:
    n = j['n']; kf = j['kf']; out = j['out']; seed = j['seed']; prompt = j['prompt']
    mk = os.path.dirname(out)
    os.makedirs(mk, exist_ok=True)
    cmd = [
        PY, '-m', 'ltx_pipelines.distilled',
        '--distilled-checkpoint-path', f'{MODELS}/ltx-2.3-22b-distilled-1.1.safetensors',
        '--gemma-root', f'{MODELS}/gemma-3-12b-it',
        '--prompt', prompt,
        '--output-path', out,
        '--image', kf, '0', STRENGTH,
        '--height', '704', '--width', '1216', '--num-frames', '121', '--frame-rate', '24', '--seed', str(seed),
        '--lora', f'{MODELS}/ltx-2.3-22b-distilled-lora-384-1.1.safetensors', '0.5',
        '--spatial-upsampler-path', f'{MODELS}/ltx-2.3-spatial-upscaler-x2-1.1.safetensors',
    ]
    print(f'[RENDER] START s{n} seed={seed}', flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, cwd='/workspace/LTX-2', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f'[RENDER] END s{n} size={sz} rc={r.returncode} sec={int(time.time()-t0)}', flush=True)
    if r.returncode != 0 or sz == 0:
        tail = r.stdout.decode(errors='replace').splitlines()[-40:]
        print('---ERRTAIL---', flush=True)
        print('\n'.join(tail), flush=True)
        print('---ENDBATCH_ABORT---', flush=True)
        sys.exit(1)

print('[RENDER] ALL_BATCH_DONE', flush=True)
