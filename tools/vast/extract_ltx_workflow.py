import json
p = "/workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo/example_workflows/2.5/LTX-2.5_T2V_I2V_Single_Stage_Distilled.json"
d = json.load(open(p))
nodes = d["nodes"]
links = d.get("links", [])
print("NODES:")
for n in nodes:
    v = n.get("widgets_values")
    id_ = n.get("id")
    ty = n.get("type")
    tt = n.get("title", "")
    wv = json.dumps(v)[:180] if v is not None else None
    print("  id=" + str(id_) + " type=" + repr(ty) + " title=" + repr(tt) + " widgets=" + str(wv))
print("\nLINKS:")
for l in links:
    if isinstance(l, dict):
        print("  link " + str(l.get("id")) + ": (" + str(l.get("origin_id")) + ":" + str(l.get("origin_slot")) + ") -> (" + str(l.get("target_id")) + ":" + str(l.get("target_slot")) + ") type=" + str(l.get("type")))
    else:
        print("  RAW " + json.dumps(l))
