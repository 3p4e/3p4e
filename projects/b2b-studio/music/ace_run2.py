# ACE-Step 1.5 v2: 3 takes per mood with fixed caption + bpm + key + 4/4, LM planning on, caption rewriting off; WAV out.
import json, time, urllib.request, os, sys
sys.path.insert(0, "/workspace"); from moods2 import MOODS2
B = "http://127.0.0.1:8001"; OUT = "/workspace/ace_out2"; os.makedirs(OUT, exist_ok=True)
def post(p, d): return json.loads(urllib.request.urlopen(urllib.request.Request(B + p, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}), timeout=600).read())
for i in range(240):
    try: urllib.request.urlopen(B + "/v1/models", timeout=5); break
    except Exception: time.sleep(10)
for name, m in MOODS2.items():
    for take in range(1, 4):
        dst = f"{OUT}/{name}_t{take}.wav"
        if os.path.exists(dst): continue
        t0 = time.time()
        r = post("/release_task", {"prompt": m["caption"], "lyrics": "[Instrumental]", "audio_duration": 70, "bpm": m["bpm"],
                                    "key_scale": m["key"], "time_signature": "4", "thinking": True, "use_cot_caption": False,
                                    "use_cot_metas": False, "use_cot_language": False, "batch_size": 1, "inference_steps": 8,
                                    "seed": 1000 * take + len(name), "audio_format": "wav"})
        tid = r["data"]["task_id"]
        while True:
            time.sleep(3)
            q = post("/query_result", {"task_id_list": [tid]})["data"][0]
            if q["status"] in (1, 2): break
        res = json.loads(q["result"])[0] if q.get("result") else {}
        f = res.get("file", "")
        if q["status"] != 1 or not f: print("FAIL", name, take, str(res.get("error") or q)[:300], flush=True); continue
        urllib.request.urlretrieve(B + f, dst); print("OK", name, take, f"{time.time()-t0:.0f}s", res.get("metas", {}).get("bpm"), res.get("metas", {}).get("keyscale"), flush=True)
print("ACE2_DONE")
