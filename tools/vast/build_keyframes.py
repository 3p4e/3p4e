#!/usr/bin/env python3
"""Build the 100 bossfight KEYFRAME still jobs from bossfight_flf_jobs.json.

Each FLF video job (shot, phase=start|end) becomes one keyframe still job.
Reference policy (Higgsfield method — image locks, not text):
  - solo hero shot  -> [look card, face crop]   (costume+weapon+hood/tattoo + identity)
  - multi-hero shot -> [look card per hero]     (baked faces carry identity)
  - boss shot       -> [boss look card] ONLY once the asset exists; else ref-less
                      T2I (no hero face leak on faceless boss)
Every ref-bearing prompt gets the appearance-only scoping clause appended.

Output: tools/vast/jobfiles/bossfight_kf_jobs.json (BARE LIST for run_kf_batch.py)
"""
import json, argparse

# LOCK REFERENCE POLICY (Higgsfield method: image locks, not text).
# Look cards carry costume+weapon+hood/tattoo + full figure; face crops
# strengthen identity. TextEncodeQwenImageEditPlus holds max 3 image slots.
#
# Data-driven choice (verified 2026-11-06 keyword scan of all 100 FLF jobs):
#   every DD shot = hooded + glacier-state  -> dd_look_glacier_v3 (twin crossbows baked)
#   every AZ shot = wrath-state             -> az_look_wrath_v2  (gold rune tattoo baked)
LOOK_CARDS = {
    'dd': 'dd_look_glacier_v3.png',
    'az': 'az_look_wrath_v2.png',
}
FACE_CARDS = {
    'dd': 'ddface_a.jpg',
    'az': 'azface_a.jpg',
}
BOSS_CARD = 'malgarot_look_card.png'   # MISSING asset — build before batch (handover §5.4)

# Higgsfield appearance-only scoping, appended to every ref-bearing prompt
APPEARANCE_CLAUSE = (" Appearance, texture and color reference ONLY; "
                     "ignore the reference's background and lighting.")

import os

def look_dir():
    # local check for whether the boss card asset exists yet
    import pathlib
    return str(pathlib.Path(__file__).resolve().parents[3] / 'media' / 'dhpf_looks')

def refs_for_cast(cast, check_dir=None):
    """Solo hero -> [look, face]. Multi-hero -> [look per hero] (their baked faces
    carry identity; 3 slots can't hold two faces + two look cards). Boss ref only
    once the boss card actually exists on disk."""
    cast = set(cast or [])
    heroes = [h for h in ('dd', 'az') if h in cast]
    refs = []
    if len(heroes) == 1:
        refs += [LOOK_CARDS[heroes[0]], FACE_CARDS[heroes[0]]]
    elif len(heroes) >= 2:
        refs += [LOOK_CARDS[h] for h in heroes]
    if 'boss' in cast and check_dir and os.path.exists(os.path.join(check_dir, BOSS_CARD)):
        refs.append(BOSS_CARD)
    return refs[:3]

ap = argparse.ArgumentParser()
ap.add_argument('--src', default='tools/vast/jobfiles/bossfight_flf_jobs.json')
ap.add_argument('--out', default='tools/vast/jobfiles/bossfight_kf_jobs.json')
ap.add_argument('--steps', type=int, default=50)
ap.add_argument('--cfg', type=float, default=4.0)
a = ap.parse_args()

src = json.load(open(a.src))
jobs = src['jobs'] if isinstance(src, dict) and 'jobs' in src else src

out = []
_look_dir = look_dir()
for j in jobs:
    shot = int(j['shot'])
    phase = j['phase']
    # deterministic seed per shot+phase so renders are reproducible
    seed = 190000 + shot * 2 + (0 if phase == 'start' else 1)
    refs = refs_for_cast(j.get('cast', []), check_dir=_look_dir)
    prompt = j['prompt']
    if refs:
        # keep the blocking preamble (start) and appearance clause (end) intact
        # by trimming the base prompt from the END if the clause overflows the cap
        MAX_PROMPT = 1400
        room = MAX_PROMPT - len(APPEARANCE_CLAUSE)
        if len(prompt) > room:
            prompt = prompt[:room].rstrip()
        prompt = prompt + APPEARANCE_CLAUSE
    out.append({
        'id': j.get('id', f'bf_{shot:02d}_{phase}'),
        'tag': f'kf_{shot:02d}_{phase}',
        'shot': shot,
        'phase': phase,
        'cast': sorted(j.get('cast', [])),
        'prompt': prompt,
        'negative': j.get('negative_prompt') or j.get('negative') or '',
        'refs': refs,
        'width': j.get('width', 1280),
        'height': j.get('height', 720),
        'steps': a.steps,
        'cfg': a.cfg,
        'seed': seed,
    })

json.dump(out, open(a.out, 'w'), indent=1)

# verification report
from collections import Counter
n = len(out)
shots = sorted(set(j['shot'] for j in out))
phases = Counter(j['phase'] for j in out)
no_ref = [j['tag'] for j in out if not j['refs']]
hero_ref = [j['tag'] for j in out if j['refs']]
over_cap = [j['tag'] for j in out if len(j['prompt']) > 1400]
leak = [j['tag'] for j in out if 'boss' in j['cast'] and ('dd' in j['refs'] or j['refs'])]
# face-leak check: pure boss shots (cast == ['boss']) must have zero refs
leak = [j['tag'] for j in out if set(j['cast']) == {'boss'} and j['refs']]

print(f'wrote {n} jobs -> {a.out}')
print(f'shots: {len(shots)} (min {min(shots)}, max {max(shots)})')
print(f'phases: {dict(phases)}')
print(f'boss-only (no ref): {len(no_ref)}  hero shots (refs): {len(hero_ref)}')
print(f'over 1400 chars: {len(over_cap)} {over_cap[:5]}')
print(f'FACE LEAK (boss-only with refs): {len(leak)} {leak[:5]}')
print(f'max prompt chars: {max(len(j["prompt"]) for j in out)}')
