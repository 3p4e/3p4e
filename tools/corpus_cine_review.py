#!/usr/bin/env python3
"""Whole-corpus cinematographic review: 40 story packages as ONE film unit.

Metrics per story + corpus: shot count vs doctrine (40-60), camera-grammar
variety (entropy over moves), shot-scale variety, act balance, pacing spread,
screen-direction consistency, beat-timeline hygiene, per-shot strength
calibration (doc-44 C1), frame-count compliance (121 = 8k+1).

Safe corrections applied in-place (content-preserving):
  1. beat_timeline chained (t1[i]==t0[i+1], 0.0..dur) — beat TEXT untouched
  2. screen_dir normalized to story-dominant axis unless the beat is an
     explicit reversal ('revers'/'retreat'/'turn back' in action)
  3. per-shot strength: action/WIDE -> 0.5, identity CLOSE-UP -> 0.7,
     else story midpoint 0.6 (doc-44 C1: strength sets the motion ceiling)
Out-of-doctrine STRUCTURE (shot count, act count) is flagged, not changed.
"""
import json, glob, os, re, math, collections

DATA = 'storybook_ocr/data'
REPORT = 'higgsfield/46_CORPUS_CINE_REVIEW.md'

def entropy(counter):
    tot = sum(counter.values())
    if tot == 0: return 0.0
    return -sum((c/tot)*math.log(c/tot) for c in counter.values())

def norm_entropy(counter):
    n = len([c for c in counter.values() if c > 0])
    if n <= 1: return 0.0
    return entropy(counter) / math.log(n)

def fix_beat_timeline(s):
    bt = s.get('beat_timeline')
    if not isinstance(bt, list) or not bt:
        return False
    dur = float(s.get('dur') or s.get('clip_s') or 3.0)
    out = []
    t = 0.0
    for i, b in enumerate(bt):
        if not isinstance(b, list) or len(b) < 3:
            return False
        beat = b[2]
        t1 = float(b[1]) if i < len(bt)-1 else dur
        if t1 <= t: t1 = t + dur/len(bt)
        out.append([round(t,2), round(t1,2), beat])
        t = t1
    if out[-1][1] != round(dur,2):
        out[-1][1] = round(dur,2)
    if out != bt:
        s['beat_timeline'] = out
        return True
    return False

REVERSAL = re.compile(r'revers|retreat|turn(?:s|ing)? back|withdraw|flee', re.I)

def main():
    rows = []
    applied = collections.Counter()
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        num = os.path.basename(f).split('_')[0]
        d = json.load(open(f, encoding='utf-8'))
        acts = d.get('acts') or []
        moves, sizes, durs, dirs = collections.Counter(), collections.Counter(), [], collections.Counter()
        nshots = 0; frames_bad = 0; strengths_set = 0
        dominant_dir = None
        for a in acts:
            for s in a.get('shots') or []:
                nshots += 1
                moves[s.get('move','static')] += 1
                sizes[s.get('size') or s.get('shot_type','MEDIUM')] += 1
                durs.append(float(s.get('dur') or 0))
                dirs[s.get('screen_dir','L-to-R')] += 1
                if int(s.get('frames') or 121) != 121: frames_bad += 1
                if fix_beat_timeline(s): applied['beat_fixed'] += 1
                # strength calibration (doc-44 C1)
                size = (s.get('size') or '').upper()
                inten = (s.get('intensity') or '').lower()
                if inten in ('action','combat') and size == 'WIDE':
                    target = 0.5
                elif size in ('CLOSE-UP','CLOSEUP','CU','EXTREME CLOSE-UP'):
                    target = 0.7
                else:
                    target = 0.6
                if s.get('strength') != target:
                    s['strength'] = target; strengths_set += 1
        dominant_dir = dirs.most_common(1)[0][0] if dirs else 'L-to-R'
        # screen-dir normalization (skip explicit reversals)
        for a in acts:
            for s in a.get('shots') or []:
                sd = s.get('screen_dir')
                act_txt = s.get('action') or ''
                if sd and sd != dominant_dir and not REVERSAL.search(act_txt):
                    s['screen_dir'] = dominant_dir
                    applied['dir_norm'] += 1
        cam_var = round(norm_entropy(moves), 2)
        scale_var = round(norm_entropy(sizes), 2)
        durs_spread = round((max(durs)-min(durs)) if durs else 0, 1)
        total = round(sum(durs), 1)
        act_shots = [len(a.get('shots') or []) for a in acts]
        bal = round(max(act_shots)/ (sum(act_shots)/len(act_shots)), 2) if act_shots and sum(act_shots) else 0
        rows.append(dict(num=num, shots=nshots, acts=len(acts), cam_var=cam_var,
                         scale_var=scale_var, dur_spread=durs_spread, total=total,
                         balance=bal, frames_bad=frames_bad,
                         static_pct=round(100*moves.get('static',0)/max(nshots,1))))
        applied['strength_set'] += strengths_set
        json.dump(d, open(f,'w',encoding='utf-8'), indent=2, ensure_ascii=False)

    # corpus-level flags
    flags = []
    for r in rows:
        notes = []
        if r['shots'] < 40 or r['shots'] > 60: notes.append(f"shots={r['shots']} outside 40-60 doctrine")
        if r['acts'] < 3: notes.append(f"acts={r['acts']} < 3")
        if r['cam_var'] < 0.5: notes.append(f"camera variety {r['cam_var']} low")
        if r['scale_var'] < 0.5: notes.append(f"scale variety {r['scale_var']} low")
        if r['dur_spread'] < 1.0: notes.append("flat pacing (dur spread <1s)")
        if r['static_pct'] > 50: notes.append(f"static {r['static_pct']}% of shots")
        if r['frames_bad']: notes.append(f"{r['frames_bad']} shots frames!=121")
        if r['balance'] > 2.0: notes.append(f"act imbalance x{r['balance']}")
        if notes: flags.append((r['num'], notes))

    md = ['# 46 — Corpus Cinematographic Review (whole-unit, 2026-11-15)', '',
          '40 story packages reviewed as ONE film unit. Corrections applied in-place are',
          'content-preserving; structural outliers are flagged for director approval.', '',
          '## Corrections applied', '',
          f"- beat_timeline chaining fixed: {applied['beat_fixed']} shots",
          f"- screen_dir normalized to dominant axis: {applied['dir_norm']} shots",
          f"- per-shot strength calibrated (doc-44 C1): {applied['strength_set']} shots",
          '', '## Per-story metrics', '',
          '| # | shots | acts | cam_var | scale_var | dur_spread | total_s | static% | flags |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        fl = '; '.join(n for nm, ns in flags if nm == r['num'] for n in ns) or '-'
        md.append(f"| {r['num']} | {r['shots']} | {r['acts']} | {r['cam_var']} | {r['scale_var']} | "
                  f"{r['dur_spread']} | {r['total']} | {r['static_pct']} | {fl} |")
    md += ['', '## Director-review queue (structure changes NOT auto-applied)', '']
    for nm, ns in flags:
        md.append(f"- **{nm}**: " + '; '.join(ns))
    open(REPORT,'w',encoding='utf-8').write('\n'.join(md))
    print(json.dumps({'applied': dict(applied), 'flagged_stories': len(flags),
                      'report': REPORT}))

if __name__ == '__main__':
    main()
