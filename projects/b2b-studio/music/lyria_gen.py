import json,urllib.request,base64,time,os
from moods import MOODS
k=open("../.gemini_paid").read().strip()
for name,p in MOODS.items():
    out=f"lyria/{name}.mp3"
    if os.path.exists(out): continue
    body={"contents":[{"parts":[{"text":"Instrumental only, no vocals. About 60 seconds. "+p}]}]}
    for a in range(4):
        try:
            r=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/lyria-3.5:generateContent?key={k}",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300).read())
            d=[x for x in r["candidates"][0]["content"]["parts"] if "inlineData" in x][0]
            open(out,"wb").write(base64.b64decode(d["inlineData"]["data"])); print("OK",name,flush=True); break
        except Exception as e: print("retry",name,str(e)[:120],flush=True); time.sleep(15)
print("LYRIA_DONE")
