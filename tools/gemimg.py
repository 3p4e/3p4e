#!/usr/bin/env python3
"""Gemini image generation (keyframes). Env: BN_GEMINI_API (never printed). Model gemini-2.5-flash-image, 16:9, optional reference images.
  python3 gemimg.py "prompt" out.png [model]   or   from gemimg import gen; gen(prompt, out, model, refs=[paths])
If the key is rejected, use another GEMINI key variable; the main GEMINI_API_KEY was flagged leaked and returned 403."""
import os,sys,json,base64,urllib.request
def gen(prompt,out,model="gemini-2.5-flash-image",refs=()):
    k=os.environ["BN_GEMINI_API"]
    parts=[{"text":prompt}]
    for r in refs: parts.append({"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(r,"rb").read()).decode()}})
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=180))
    for p in d["candidates"][0]["content"]["parts"]:
        inl=p.get("inlineData") or p.get("inline_data")
        if inl: open(out,"wb").write(base64.b64decode(inl["data"])); return True
    print("no image:",json.dumps(d)[:300]); return False
if __name__=="__main__":
    print(gen(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else "gemini-2.5-flash-image"))
