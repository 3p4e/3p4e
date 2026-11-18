import json, urllib.request

C = "/workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo"

# 1) README I2V section (plain node chain)
try:
    rd = open(C + "/README.md").read()
    i = rd.lower().find("i2v")
    print("=== README (i2v context) ===")
    print(rd[max(0, i-200): i+1500] if i >= 0 else rd[:1500])
except Exception as e:
    print("README ERR", e)

print("\n=== 2.0 PLAIN EXAMPLE node types ===")
try:
    d = json.load(open(C + "/example_workflows/2.0/LTX-2_I2V_Distilled_wLora.json"))
    nodes = d["nodes"]
    for n in nodes:
        print("  id=" + str(n.get("id")) + " type=" + repr(n.get("type")) + " widgets=" + json.dumps(n.get("widgets_values"))[:120])
    print("  LINKS:")
    for l in d.get("links", []):
        if isinstance(l, dict):
            print("   ", l.get("origin_id"), ":", l.get("origin_slot"), "->", l.get("target_id"), ":", l.get("target_slot"), l.get("type"))
        else:
            print("   RAW", l)
except Exception as e:
    print("2.0 EXAMPLE ERR", e)

# 2) full object_info schemas
def brief(x):
    if isinstance(x, list):
        s = json.dumps(x)
        return s[:160]
    if isinstance(x, dict):
        s = json.dumps(x)
        return s[:160]
    return str(x)[:160]

info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60))
want = ["UNETLoader", "VAELoader", "CLIPLoader", "CLIPTextEncode", "KSamplerSelect",
        "LoadImage", "SaveVideo", "LTXAVTextEncoderLoader", "LTXVConditioning",
        "LTXVScheduler", "LTXVDualCFGGuider", "LTXVBaseSampler", "LTXVImgToVideo",
        "LTXVSpatioTemporalTiledVAEDecode", "LTXVTiledVAEDecode", "LTXVAudioVAELoader",
        "LTXVAudioVAEDecode", "LTXVSeparateAVLatent", "LTXVConcatAVLatent",
        "LTXVVAEForceFloat32"]

print("\n=== FULL SCHEMAS ===")
for t in want:
    if t not in info:
        print("\n### " + t + " MISSING")
        continue
    n = info[t]
    outs = []
    for o in n.get("output", []):
        outs.append(o[0] if isinstance(o, list) and o else str(o))
    print("\n### " + t + "  OUTPUT=" + json.dumps(outs)[:120])
    req = n.get("input", {}).get("required", {})
    for k, v in req.items():
        print("   [req] " + k + " = " + brief(v))
    opt = n.get("input", {}).get("optional", {})
    for k, v in opt.items():
        print("   [opt] " + k + " = " + brief(v))
