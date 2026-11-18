import json, urllib.request
info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60))

for t in ["UNETLoader", "VAELoader", "CLIPLoader", "LTXAVTextEncoderLoader",
          "LTXVAudioVAELoader", "CreateVideo", "RandomNoise", "SaveImage"]:
    if t not in info:
        print("\n### " + t + " MISSING")
        continue
    n = info[t]
    print("\n### " + t)
    print("  OUTPUT=", json.dumps([o[0] if isinstance(o, list) and o else str(o) for o in n.get("output", [])])[:140])
    req = n.get("input", {}).get("required", {})
    for k, v in req.items():
        if isinstance(v, list) and v and isinstance(v[0], list):
            # combo/list options
            print("   [req] " + k + " OPTIONS=" + json.dumps(v[0])[:600])
        else:
            print("   [req] " + k + " = " + json.dumps(v, default=str)[:500])
    opt = n.get("input", {}).get("optional", {})
    for k, v in opt.items():
        if isinstance(v, list) and v and isinstance(v[0], list):
            print("   [opt] " + k + " OPTIONS=" + json.dumps(v[0])[:600])
        else:
            print("   [opt] " + k + " = " + json.dumps(v, default=str)[:500])
