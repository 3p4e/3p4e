import os, re, json, urllib.request

C = "/workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo"

# find the files defining these two classes
for cls in ["LTXAVTextEncoderLoader", "LTXVAudioVAELoader", "LTXVConditioning"]:
    found = []
    for root, dirs, files in os.walk(C):
        for f in files:
            if f.endswith(".py"):
                p = os.path.join(root, f)
                try:
                    txt = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                if ("class " + cls) in txt:
                    found.append(os.path.relpath(p, C))
    print("\n### " + cls + " defined in: " + str(found))

# grep the relevant import-time folder calls in the whole pack
print("\n================ folder_paths.get_filename_list(...) calls ================")
pat = re.compile(r'folder_paths\.get_filename_list\(["\']([^"\']+)["\']\)')
seen = set()
for root, dirs, files in os.walk(C):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for m in pat.finditer(txt):
                seen.add(m.group(1))
print(sorted(seen))

# live object_info for the two loaders, full raw JSON of required inputs
info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60))
for t in ["LTXAVTextEncoderLoader", "LTXVAudioVAELoader"]:
    n = info.get(t)
    if not n:
        print("\n" + t + " MISSING from object_info")
        continue
    print("\n" + t + " FULL REQUIRED INPUTS:")
    for k, v in n.get("input", {}).get("required", {}).items():
        print("  " + k + " = " + json.dumps(v, default=str))
