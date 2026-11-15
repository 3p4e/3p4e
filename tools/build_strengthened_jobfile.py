import json, os

flags = json.load(open('tools/vast/jobs/fenrir_semantic_audit2.json'))
flagged = {}
for f in flags:
    n = int(''.join(c for c in f['file'] if c.isdigit()))
    drift = str(f.get('costume_drift', 'none')).lower()
    if f.get('morphing') or f.get('duplicate_wolves') or f.get('stray_human') or drift not in ('none', ''):
        flagged[n] = f

INFLIGHT = {5, 15, 16, 17, 46}
R = sorted(set(flagged) | INFLIGHT)
print('RE-RENDER SET (%d):' % len(R), R)
for n in sorted(flagged):
    f = flagged[n]
    print(' s%02d | morph=%s dup=%s stray=%s drift=%s' % (
        n, f.get('morphing'), f.get('duplicate_wolves'), f.get('stray_human'), f.get('costume_drift')))

GUARDS = (" Exactly one grey wolf Fenrir in frame - no duplicate wolves, no second pup, no extra animals."
          " Only the characters named in this description are present - no bystanders, no crowd, no guards,"
          " no children, no extras."
          " Every character's face, armor and costume stays completely identical to the reference image"
          " across the whole shot - no morphing, no changing outfits, no changing colors.")
ANCHOR = (" Odin wears dark-gold VOID-SEER robes and an eyepatch."
          " Týr is a young warrior in ember-gold FINAL OATH plate armor with his right hand intact."
          " Loki wears the INK OF CHAOS dark-ember kit."
          " Fenrir is a grey wolf with VOID MAW dark-star eyes."
          " Hel has a half-living warm / half-dead pale-cold split face.")

base = json.load(open('tools/vast/jobfiles/fenrir_46_clips_jobfile.json'))
jobs = []
for j in base['jobs']:
    n = int(j['job_id'].split('_s')[1])
    if n in R:
        j2 = dict(j)
        prompt_key = 'continuation_prompt' if 'continuation_prompt' in j else ('prompt' if 'prompt' in j else 'description')
        j2['continuation_prompt'] = j[prompt_key].rstrip() + GUARDS + ANCHOR
        j2['seed'] = n + 3000
        j2['image_strength'] = 0.85
        j2['strengthened'] = True
        jobs.append(j2)
json.dump({'jobs': jobs}, open('tools/vast/jobfiles/fenrir_strengthened_jobfile.json', 'w'), indent=1)

lines = ['#!/bin/bash', 'set -uo pipefail', 'cd /workspace/ltx23', 'source .venv/bin/activate || true',
         'export HF_HUB_ENABLE_HF_TRANSFER=0 LTX2_ATTENTION_BACKEND=SAGE LTX2_VAE_CACHE=/workspace/vae_cache',
         'echo "$(date +%H:%M:%S) waiting for models..."',
         'while [ ! -f /workspace/models/ltx23/ltx-2.3-22b-distilled-1.1.safetensors ] || [ ! -f /workspace/models/ltx23/ltx2.3-spatial-upscaler-lora-384.safetensors ]; do sleep 20; done',
         'echo "$(date +%H:%M:%S) models present - rendering"',
         'render() {',
         '  local kf="$1" prompt="$2" seed="$3" out="$4" strength="${5:-0.85}"',
         '  /workspace/ltx23/.venv/bin/python -m ltx_video.inference \\',
         '    --ckpt_path /workspace/models/ltx23/ltx-2.3-22b-distilled-1.1.safetensors \\',
         '    --lora_checkpoint /workspace/models/ltx23/ltx2.3-spatial-upscaler-lora-384.safetensors \\',
         '    --lora_weight 0.5 --vae_checkpoint /workspace/models/ltx23/ltx2.3-spatial-upscaler-vae.safetensors \\',
         '    --gemma_root /workspace/models/gemma/gemma-3-12b-it \\',
         '    --height 704 --width 1216 --num_frames 121 --fps 24 --steps 8 --cfg 1.0 \\',
         '    --seed "$seed" --input_file "${kf}.txt" \\',
         '    --image "/workspace/stills/$kf" 0 "$strength" \\',
         '    --output_dir /workspace/out --output_filename "${out}.mp4" >/workspace/logs/r_${out}.log 2>&1',
         '  local rc=$?',
         '  if [ $rc -eq 0 ] && [ -f "/workspace/out/${out}.mp4" ]; then echo "$(date +%H:%M:%S) ${out} rc=0"; sha256sum "/workspace/out/${out}.mp4" >> /workspace/out/manifest.tsv; else echo "$(date +%H:%M:%S) ${out} rc=$rc FAIL"; fi',
         '}']
for j in jobs:
    kf = os.path.basename(j['start_frame']).replace('.png', '')
    lines.append('render %s %s %s %s %s' % (kf, j['job_id'], j['seed'], j['job_id'], j['image_strength']))
lines.append('echo "$(date +%H:%M:%S) BATCH22_DONE"')
open('/tmp/fenrir_batch22.sh', 'w').write('\n'.join(lines) + '\n')

os.makedirs('/tmp/stills_txt', exist_ok=True)
for j in jobs:
    kf = os.path.basename(j['start_frame']).replace('.png', '')
    open('/tmp/stills_txt/%s.txt' % kf, 'w').write(j['continuation_prompt'])
print('jobfile + batch22 + %d prompt txts ready' % len(jobs))
