#!/usr/bin/env python3
"""Apply reconciliation corrections to build_story41.py, then regenerate the HTML storyboard.
Corrections: casting swap (DD=Hunter/ice, Blagoj=Paladin/light) + canonical v2 ability names.
Also applies two small honesty fixes to 27_MASTER_SPEC.md (combo count)."""
import pathlib, importlib.util, re, json as J, html as H

# ---------- 1. patch build_story41.py ----------
p = pathlib.Path('/a0/usr/projects/vast/tools/build_story41.py')
txt = p.read_text(encoding='utf-8')

repls = [
    # casting (critical: DD=Hunter/ice, Blagoj=Paladin/light)
    ("source='ВАСТ canon · в. блегој сет', face_lock='Blagoj (заклучување подоцна)'",
     "source='faces/dd_cards_final (9 enrolled) · identity_index→dd', face_lock='DD (заклучување подоцна)'"),
    ("source='ВАСТ canon · в. дд сет', face_lock='DD (заклучување подоцна)'",
     "source='Blagoj-shaven 454a359e · IDENTITY.md/CHARACTER_SYSTEM.md', face_lock='Blagoj (заклучување подоцна)'"),
    # canonical ability names (machine fields only)
    ("ICE HALO", "Glacial Aura"),
    ("ICE FORM", "Glacier Form"),
    ("Ice Form", "Glacier Form"),
    ("AVENGER\\'S WRATH", "Avenging Wrath"),
    ("Avenger\\' Wrath", "Avenging Wrath"),
    ("FREEZE-and-SHATTER", "Freeze-and-Sunder"),
    ("ice beams", "Rime Beams"),
    ("ice-beams", "Rime Beams"),
    ("the ice beam", "the Rime Beam"),
    ("Judgement blast", "Verdict blast"),
    ("golden Judgement", "golden Verdict"),
    ("Judgement shockwave", "Templar Verdict shockwave"),
]

for old, new in repls:
    n = txt.count(old)
    assert n > 0, 'NOT FOUND in build_story41.py: ' + repr(old)
    txt = txt.replace(old, new)
    print('OK (%dx) %r -> %r' % (n, old, new))

p.write_text(txt, encoding='utf-8')
print('patched', p)

# ---------- 2. regenerate the HTML ----------
spec = importlib.util.spec_from_file_location('build41_regenerated', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# ---------- 3. verify embedded JSON cast + ability terms ----------
out = pathlib.Path('/a0/usr/projects/vast/storybook_ocr/storyboards/41_lovecot_paladin_gospodar_pepelta.html')
h = out.read_text(encoding='utf-8')
mch = re.search(r'<script type="application/json" id="storyboard-spec">(.*?)</script>', h, re.S)
assert mch, 'embedded JSON not found'
payload = J.loads(H.unescape(mch.group(1)))
print('\nCAST LOCK (from embedded JSON):')
for c in payload['cast']:
    print('  ', c['role'], '=>', c['face_lock'])
terms = ['Glacial Aura', 'Rime Beams', 'Freeze-and-Sunder', 'Glacier Form', 'Avenging Wrath', 'Verdict']
print('ability terms present:', {t: (t in h) for t in terms})
print('section-sign bytes:', out.read_bytes().count(b'\xc2\xa7'))

# ---------- 4. honesty fixes to master spec (combo count) ----------
ps = pathlib.Path('/a0/usr/projects/vast/higgsfield/27_DEMONHUNTER_PALADIN_MASTER_SPEC.md')
pt = ps.read_text(encoding='utf-8')
mrepls = [
    ("| 2 (Freeze-and-Sunder, Hoarfrost Judgement) | add Combo #3 on expansion |",
     "| 2 (Freeze-and-Sunder explicit; Blizzard & Verdict condensed as the dual finale S17–S18) | add Hoarfrost Judgement as its own beat on expansion |"),
    ("and Combo #3 „Blizzard & Verdict\"",
     "and a dedicated Combo #2 „Hoarfrost Judgement\" beat"),
]
for old, new in mrepls:
    n = pt.count(old)
    if n == 0:
        print('\nWARN master-spec NOT FOUND:', repr(old))
    else:
        pt = pt.replace(old, new)
        print('\nOK master-spec (%dx): %r' % (n, old))
ps.write_text(pt, encoding='utf-8')
print('master spec updated', ps)
print('\nALL DONE')
