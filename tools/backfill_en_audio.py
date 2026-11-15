#!/usr/bin/env python3
"""Backfill EN translations into all NN_AUDIO_SCRIPT_MK_EN.md files.

Reads storybook_ocr/translations/NN_en.json (validated EN lines keyed by S-id),
replaces the blank EN slot  / ""  with  / "EN text"  per shot.
Skips 13 and 23 (already complete, excluded from this sweep).
"""
import json, glob, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'storybook_ocr/translations/*_en.json'))):
    num = os.path.basename(p).split('_')[0]
    T[num] = json.load(open(p, encoding='utf-8'))
print('loaded translations for stories:', len(T))

scripts = sorted(glob.glob(os.path.join(ROOT, 'storybook_ocr/specs/[0-9][0-9]_AUDIO_SCRIPT_MK_EN.md')))
print('audio scripts found:', len(scripts))

total_filled = 0
total_remaining = 0
for sp in scripts:
    num = os.path.basename(sp).split('_')[0]
    if num not in T:
        print('  SKIP', os.path.basename(sp), '(no translation — expected for 13/23)')
        continue
    en_map = T[num]
    raw = open(sp, encoding='utf-8').read()
    filled = [0]
    def repl(m):
        shot = 'S' + m.group(1)
        en = en_map.get(shot, '')
        if not en:
            return m.group(0)
        filled[0] += 1
        return m.group(0).replace('/ ""', '/ "' + en + '"')
    new = re.sub(r'\*\*S(\d{2})\*\*[^\n]*?/ ""', repl, raw)
    open(sp, 'w', encoding='utf-8').write(new)
    remaining = new.count('/ ""')
    total_filled += filled[0]
    total_remaining += remaining
    print('  %s: filled=%d, remaining blanks=%d' % (os.path.basename(sp), filled[0], remaining))

print('TOTAL filled:', total_filled)
print('TOTAL remaining blanks:', total_remaining)
