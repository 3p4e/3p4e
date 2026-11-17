import base64, glob, json, os, time, urllib.request
KEY = os.environ['OPEN_ROUTER_API_KEY']  # never hardcode; §44 + push-protection

MODELS = ['google/gemini-2.5-flash', 'qwen/qwen-2.5-vl-72b-instruct', 'google/gemini-flash-1.5']
SHEETS = sorted(glob.glob('media/fenrir_assets/clips/audit_sheets/s*.jpg'))
CAST = ('Odin: old one-eyed king, dark-gold VOID-SEER robes, eyepatch. Loki: dark-haired young man, INK OF CHAOS dark-ember kit. '
 'Týr: young warrior, ember-gold FINAL OATH plate armor, right hand INTACT. Hel: woman split half-living warm / half-dead pale-cold, dark-ash palette. '
 'Fenrir: ONE grey wolf (pup in act 1, adult later, VOID MAW dark-star eyes). Dwarf smiths: short gruff figures in forge aprons. Jörmungandr: giant serpent.')
def ask(model, images):
    content = [{'type':'text','text':
      'You are auditing frames from a Norse myth film. Each attached image sNN.jpg is a 2x2 grid of 4 frames from ONE clip.'
      f' Known cast: {CAST} '
      'For EACH image, answer strictly as one JSON object per line (no prose): {"file":"sNN","morphing":false,"duplicate_wolves":false,"stray_human":false,"costume_drift":"none","notes":"short"} '
      '- morphing: main subject visibly changes shape/identity across the 4 frames (face melting, wolf changing size/color, extra limbs). '
      '- duplicate_wolves: two or more wolves/pups in any frame when the scene should have one. '
      '- stray_human: a human who matches no cast member (modern clothes, random bystander, faceless extra in closeup). '
      '- costume_drift: "none" or character:what-changed (armor color/pattern different between frames or vs cast description).'}]
    for p in images:
        b64 = base64.b64encode(open(p,'rb').read()).decode()
        content.append({'type':'image_url','image_url':{'url':f'data:image/jpeg;base64,{b64}','detail':'low'}})
    body = json.dumps({'model':model,'messages':[{'role':'user','content':content}],'max_tokens':2000}).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())['choices'][0]['message']['content']
results, fails = [], []
for i in range(0, len(SHEETS), 4):
    batch = SHEETS[i:i+4]
    done = False
    for m in MODELS:
        try:
            txt = ask(m, batch)
            for line in txt.splitlines():
                line = line.strip().strip(',')
                if line.startswith('{'):
                    results.append(json.loads(line))
            print(f'batch {i//4+1}/{(len(SHEETS)+3)//4} OK via {m}', flush=True)
            done = True; break
        except Exception as e:
            print(f'batch {i//4+1} FAIL {m}: {e}', flush=True)
            time.sleep(2)
    if not done: fails.extend(batch)
    time.sleep(1)
json.dump({'results':results,'failed_batches':fails}, open('tools/vast/jobs/fenrir_semantic_audit.json','w'), indent=1)
flags = [r for r in results if r.get('morphing') or r.get('duplicate_wolves') or r.get('stray_human') or r.get('costume_drift','none') not in ('none','')]
print('AUDIT_DONE sheets:', len(results), 'flags:', len(flags))
for f in flags: print('FLAG', f)
