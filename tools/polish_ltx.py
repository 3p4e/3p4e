import json, os, sys, time, urllib.request
jobs = json.load(open('/a0/usr/projects/vast/tools/vast/jobfiles/ltx_jobs_100.json'))
KEY = os.environ.get('NVIDIA_API', '')
if not KEY or KEY.startswith('PLACEHOLDER'):
    import subprocess
    KEY = subprocess.run(['bash','-c','echo "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"'], capture_output=True, text=True).stdout.strip()
URL = 'https://integrate.api.nvidia.com/v1/chat/completions'
SYS = ('You are an expert LTX-2.3 video prompt writer. LTX-2.3 distilled generates by EXTENDING the start frame. '
 'Rewrite each prompt to be a strict CONTINUATION of its start frame: present tense, motion-first, describe only motion '
 'continuing what is in the frame, NEVER new/different content or a scene change. Keep the camera move. '
 'Frames ending in _end are STARTS of NEW clips: rewrite the camera phrase as a fresh opening (remove "the end of the movement", keep just the move). '
 'Keep all character identity + weapon-anchor clauses (crossbows/greatsword never leaving). Single coherent subject. Output ONLY a JSON array [{"frame":"...","prompt":"..."},...]')
def polish(batch, retry=2):
    items = [{'frame': j['frame'], 'prompt': j['prompt']} for j in batch]
    body = {'model': 'deepseek-ai/deepseek-v4.1-flash', 'messages': [
        {'role': 'system', 'content': SYS}, {'role': 'user', 'content': json.dumps(items)}],
        'temperature': 0.3, 'max_tokens': 4096}
    for attempt in range(retry):
        try:
            r = urllib.request.Request(URL, data=json.dumps(body).encode(),
                headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(r, timeout=180) as resp:
                d = json.load(resp)
            txt = d['choices'][0]['message']['content']
            txt = txt[txt.find('['):txt.rfind(']') + 1]
            out = json.loads(txt)
            if len(out) == len(batch):
                return out
        except Exception as e:
            print('  retry', attempt, type(e).__name__, str(e)[:100], flush=True)
            time.sleep(3)
    return None
polished = {}
B = 10
for i in range(0, len(jobs), B):
    batch = jobs[i:i + B]
    out = polish(batch)
    if out:
        for o in out:
            polished[o['frame']] = o['prompt']
        print(f'batch {i//B+1}/10 OK ({len(out)})', flush=True)
    else:
        for j in batch:
            polished[j['frame']] = j['prompt']
        print(f'batch {i//B+1}/10 FALLBACK-ORIGINAL', flush=True)
    time.sleep(1)
out_jobs = []
for j in jobs:
    nj = dict(j)
    nj['prompt'] = polished.get(j['frame'], j['prompt'])
    nj['polished'] = j['frame'] in polished and polished[j['frame']] != j['prompt']
    out_jobs.append(nj)
json.dump(out_jobs, open('/a0/usr/projects/vast/tools/vast/jobfiles/ltx_jobs_100_polished.json', 'w'), indent=1)
npol = sum(1 for j in out_jobs if j['polished'])
print(f'DONE {len(out_jobs)} jobs, {npol} polished, {len(out_jobs)-npol} original')
print('sample:', out_jobs[0]['prompt'][:220])
