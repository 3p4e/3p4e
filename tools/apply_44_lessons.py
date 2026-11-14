#!/usr/bin/env python3
"""Apply doc-44 (P23 error lessons 2026-11-14) durable rules to all story data.

A6: hybrid-creature body-form guards (NO legs / NO human lower body / NO feet)
    on every prompt that names a hybrid creature.
D2: resolution directive in every image-gen keyframe prompt
    ('generate at 2432x1408 minimum, ideally 3840x2160 (4K landscape)').
Idempotent: skips prompts that already carry the guard/directive.
"""
import json, glob, re, os

DATA = 'storybook_ocr/data'
RES_DIRECTIVE = (' Generate at 2432x1408 minimum, ideally 3840x2160 (4K landscape).')
LEG_GUARD = (' Body-form canon: NO legs, NO human lower body, NO feet — '
             'the lower body is exactly as designed, never corrected to bipedal.')
NEG_GUARD = 'legs, human legs, feet, human feet, bipedal, standing on legs'

HYBRID_PATTERNS = re.compile(
    r'\b(jormungandr|medusa|ladon|hydra|lernean_hydra|snake_king|xiangliu|'
    r'serpent|gorgon|snake[_ -]?(man|woman|king|queen)|merfolk|mermaid|merman|'
    r'siren|harpy|centaur|naga|lamia|scylla|chimera|sphinx|kraken|ketos|'
    r'coiled tail|snake tail|serpent tail)\b', re.I)

def is_hybrid_shot(s):
    blob = ' '.join(str(v) for v in s.values() if isinstance(v, (str, list)))
    return bool(HYBRID_PATTERNS.search(blob))

def touch(prompt, add, marker):
    if not prompt:
        return prompt, False
    if marker in prompt:
        return prompt, False
    # append before any trailing negative clause split
    return prompt.rstrip() + add, True

def main():
    stats = {'res': 0, 'guard': 0, 'files': 0}
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        d = json.load(open(f, encoding='utf-8'))
        changed = False
        for a in d['acts']:
            for s in a['shots']:
                # D2: resolution directive on image-gen prompts
                for fld in ('image_prompt_start', 'image_prompt_end'):
                    p = s.get(fld)
                    if p and '2432x1408' not in p and '2432×1408' not in p and '3840' not in p:
                        s[fld] = p.rstrip() + RES_DIRECTIVE
                        stats['res'] += 1; changed = True
                # A6: body-form guard on any prompt of a hybrid shot
                if is_hybrid_shot(s):
                    for fld in ('image_prompt_start', 'image_prompt_end',
                                'video_prompt_start', 'video_prompt_end'):
                        p = s.get(fld)
                        if p and 'NO legs' not in p and 'NO human lower body' not in p:
                            s[fld] = p.rstrip() + LEG_GUARD
                            stats['guard'] += 1; changed = True
        if changed:
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            stats['files'] += 1
    print(json.dumps(stats))

if __name__ == '__main__':
    main()
