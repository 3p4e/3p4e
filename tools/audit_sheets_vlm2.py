import base64, glob, json, time, urllib.request
KEY = os.environ['OPEN_ROUTER_API_KEY']  # never hardcode; §44 + push-protection
MODELS = ['google/gemini-2.5-flash', 'google/gemini-flash-1.5', 'qwen/qwen-2.5-vl-72b-instruct']
SHEETS = sorted(glob.glob('media/fenrir_assets/clips/audit_sheets/s*.jpg'), key=lambda p: int(''.join(c for c in p.split('/')[-1] if c.isdigit())))
CAST = ('Odin: old one-eyed king, dark-gold VOID-SEER robes, eyepatch. Loki: dark-haired young man, INK OF CHAOS dark-ember kit. '
 'Týr: YOUNG warrior, ember-gold FINAL OATH plate armor, right hand INTACT (never missing). Hel: woman split half-living warm / half-dead pale-cold. '
 'Fenrir: EXACTLY ONE grey wolf per shot (small pup in shots 01-10, giant adult from shot 11 on, VOID MAW dark-star eyes). Dwarf smiths: short gruff forge figures.')
def ask(model, path):
    fn = path.split('/')[-1]
    b64 = base64.b64encode(open(path,'rb').read()).decode()
    content = [{'type':'text','text':f'Image {fn} is a 2x2 grid of 4 frames from ONE film clip of a Norse myth film. Cast: {CAST} '
      'Reply with ONLY one JSON object: {"file":"'+fn+'","morphing":bool,"duplicate_wolves":bool,"stray_human":bool,"costume_drift":"none|CHARACTER:what","wrong_count":"","notes":"max 15 words"} '
      'morphing=subject changes shape/identity across frames. duplicate_wolves=2+ wolves/pups in any frame. stray_human=human matching no cast member. costume_drift=armor/robe differs from cast description or changes across frames. wrong_count=any person/animal count that contradicts the cast line, e.g. "two Tyr".'},
      {'type':'image_url','image_url':{'url':f'data:image/jpeg;base64,{b64}','detail':'low'}}]
    body = json.dumps({'model':model,'messages':[{'role':'user','content':content}],'max_tokens':400}).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())['choices'][0]['message']['content']
results = []
for p in SHEETS:
    fn = p.split('/')[-1]
    for m in MODELS:
        try:
            txt = ask(m, p).strip()
            d = json.loads(txt[txt.find('{'):txt.rfind('}')+1]); d['file'] = fn
            results.append(d); print(fn, 'OK', flush=True); break
        except Exception as e:
            time.sleep(2)
    else:
        print(fn, 'ALLFAIL', flush=True)
    time.sleep(0.4)
json.dump(results, open('tools/vast/jobs/fenrir_semantic_audit2.json','w'), indent=1)
print('DONE', len(results))
