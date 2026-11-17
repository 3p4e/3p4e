import re, json

base='/a0/usr/projects/vast/storybook_ocr/'
kfp=base+'specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
jp=base+'data/23_perseus_defeats_medusa_data.json'

kf=open(kfp).read()
fixes=[]

# --- fix 1: S01 'at dawn' residue ---
# find the S01 block and locate the exact 'at dawn' phrase
if 'at dawn' in kf:
    m=re.search(r'.{60}at dawn.{60}', kf, re.I)
    if m:
        fixes.append('S01 dawn context: '+m.group(0)[:140])
    kf=kf.replace('at dawn','under storm-gloom')
    fixes.append("FIXED: 'at dawn' -> 'under storm-gloom' (global, KF pack)")

# --- fix 2: S23 gore word in pre-negative section ---
b23_match=re.search(r'(## SHOT S23.*?)(?=\n## SHOT |\Z)', kf, re.S)
if b23_match:
    b23=b23_match.group(1)
    pre_neg=b23.split('**Negative:**')[0]
    for m2 in re.finditer(r'.{30}(blood|gore|wound\w*|decapitat\w*).{30}', pre_neg, re.I):
        fixes.append('S23 pre-negative match: '+m2.group(0))
    # replace only in pre-negative portion of S23 block
    new_pre=re.sub(r'\b(blood|gore)\b','darkness',pre_neg,flags=re.I)
    new_pre=re.sub(r'\b(wound\w*)\b','scar',new_pre,flags=re.I)
    new_pre=re.sub(r'\b(decapitat\w*)\b','the fall',new_pre,flags=re.I)
    if new_pre!=pre_neg:
        kf=kf[:b23_match.start()]+new_pre+b23[b23.index('**Negative:**'):]+kf[b23_match.end():]
        fixes.append('FIXED: S23 gore wording in pre-negative section')

open(kfp,'w').write(kf)

# --- fix 3: data JSON time_of_day ---
d=json.load(open(jp))
for a in d['acts']:
    if a.get('time_of_day')=='dawn':
        a['time_of_day']='storm-dusk'
        fixes.append(f"FIXED: {a['num']} time_of_day dawn -> storm-dusk")
json.dump(d,open(jp,'w'),indent=1,ensure_ascii=False)

# --- attach census (correct regex) ---
atts=re.findall(r'\*\*Attach:\*\* (.+)', kf)
import collections
for t,c in collections.Counter(x.strip() for x in atts).most_common():
    fixes.append(f'ATTACH {c:2d}x {t}')

# --- final verification ---
print('--- re-verify ---')
print('at dawn remaining:', len(re.findall(r'at dawn', open(kfp).read(), re.I)))
b23=re.search(r'(## SHOT S23.*?)(?=\n## SHOT |\Z)', open(kfp).read(), re.S).group(1)
print('S23 gore in pre-negative:', bool(re.search(r'\b(blood|gore|wound\w*|decapitat\w*)\b', b23.split("**Negative:**")[0], re.I)))
d2=json.load(open(jp))
print('time_of_day values:', [a.get('time_of_day') for a in d2['acts']])
print()
print('FIXES APPLIED:')
for f in fixes: print(' -',f)
