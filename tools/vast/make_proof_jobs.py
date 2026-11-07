#!/usr/bin/env python3
"""Extract shot-19 FLF jobs as a BARE LIST for run_qwen_edit.py.

run_qwen_edit.py does:  jobs = json.load(...); for job in jobs: job['refs']
so the file must be a bare JSON list, not {"jobs": [...]}, and the negative
key must be 'negative' (the renderer reads job.get('negative', DEFAULT_NEG)).
"""
import json, sys

src_path = 'tools/vast/jobfiles/bossfight_flf_jobs.json'
if len(sys.argv) > 1:
    src_path = sys.argv[1]

src = json.load(open(src_path))
jobs = src['jobs'] if isinstance(src, dict) and 'jobs' in src else src
proof = [j for j in jobs if j.get('shot') == 19]

out = []
for j in proof:
    neg = j.get('negative_prompt') or j.get('negative') or ''
    seed = 190119 if j.get('phase') == 'start' else 190120
    out.append({
        'id': j.get('id'),
        'tag': 'proof_s19_' + j.get('phase'),
        'prompt': j.get('prompt'),
        'negative': neg,
        'refs': ['ddface_a.jpg', 'azface_a.jpg'],
        'width': 1280,
        'height': 720,
        'steps': 50,
        'cfg': 4.0,
        'seed': seed,
    })

json.dump(out, open('tools/vast/jobfiles/proof_s19_jobs.json', 'w'), indent=1)
print('wrote', len(out), 'jobs')
for j in out:
    print('  ', j['tag'], '| prompt_chars=', len(j['prompt']),
          '| neg_chars=', len(j['negative']), '| refs=', j['refs'],
          '| seed=', j['seed'])
