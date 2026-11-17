#!/usr/bin/env python3
"""Build the Fenrir 46-clip jobfile for LTX-2.3 22B distilled (start-frame-only, 43 sec.2).

Reads the story data JSON, ensures the LTX-2.3 distilled spec fields, and writes
tools/vast/jobfiles/fenrir_46_clips_jobfile.json with one job per shot:
start frame + continuation prompt + distilled render params (38/42 recipe).
Zero GPU; deterministic; no LLM.
"""
import json
import pathlib

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA = ROOT / 'storybook_ocr/data/13_fenrir_the_wolf_of_asgard_data.json'
OUT = ROOT / 'tools/vast/jobfiles/fenrir_46_clips_jobfile.json'

LTX_SPEC = {
    'model': 'LTX-2.3-22B-distilled-1.1',
    'resolution': '1216x704',
    'aspect': '16:9',
    'fps': 24,
    'frames': 121,
    'frames_rule': '8k+1',
    'frames_fallback': 81,
    'steps': 8,
    'cfg': 1.0,
    'lora': 'ltx-2.3-22b-distilled-lora-384-1.1.safetensors @ 0.5',
    'spatial_upscaler': 'ltx-2.3-spatial-upscaler-x2-1.1.safetensors',
    'image_strength': '0.7 (img2video distilled recipe, 42 note)',
    'audio_mode': 'native-ltx23',
    'negative_prompt': ('deformed, extra limbs, morphing, watermark, text, static frame, '
                        'blurry, low quality, cropped head, cut-off face'),
    'clip_model': 'N-clip start-frame-only (43 sec.2)',
    'clip_seconds': 5.04,
}


def main():
    d = json.load(open(DATA, encoding='utf-8'))
    d['spec'].update(LTX_SPEC)
    json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    jobs = []
    for act in d['acts']:
        for s in act['shots']:
            n = int(s['id'][1:])
            jobs.append({
                'job_id': 'fenrir_s%02d' % n,
                'shot': s['id'],
                'act': act['id'],
                'start_frame': 'media/fenrir_assets/keyframes/kf_%02d_start.png' % n,
                'prompt': (s.get('continuation_prompt') or '').strip(),
                'negative_prompt': LTX_SPEC['negative_prompt'],
                'resolution': LTX_SPEC['resolution'],
                'frames': LTX_SPEC['frames'],
                'fps': LTX_SPEC['fps'],
                'steps': LTX_SPEC['steps'],
                'cfg': LTX_SPEC['cfg'],
                'seed': n,
                'size': s.get('size'),
                'move': s.get('move'),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump({'spec': LTX_SPEC, 'clip_count': len(jobs), 'jobs': jobs},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('JOBFILE OK:', OUT)
    print('jobs:', len(jobs))
    print('spec:', LTX_SPEC['model'], LTX_SPEC['resolution'],
          str(LTX_SPEC['frames']) + 'f', str(LTX_SPEC['fps']) + 'fps',
          'steps', LTX_SPEC['steps'], 'cfg', LTX_SPEC['cfg'])


if __name__ == '__main__':
    main()
