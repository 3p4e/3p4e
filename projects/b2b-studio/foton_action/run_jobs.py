# submits jobs.json to the local SGLang MiniMax-H3 server, one at a time; resume-safe
import json, os, time, urllib.request
B="http://127.0.0.1:30010"; OUT="/workspace/h3act_out"; os.makedirs(OUT, exist_ok=True)
jobs=json.load(open("/workspace/h3act/jobs.json"))
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
for j in jobs:
    dst=f"{OUT}/{j['id']}.mp4"
    if os.path.exists(dst) and os.path.getsize(dst)>100000: continue
    body={"model":"MiniMaxAI/MiniMax-H3","prompt":j["prompt"],"seconds":5,"task":j["task"],"conditions":j["conds"],
          "target":{"short_edge":768,"aspect_ratio":"16:9","duration_seconds":5.0},"num_outputs_per_prompt":1,
          "num_inference_steps":50,"flow_shift":12.0,"audio_flow_shift":3.0,"seed":j["seed"]}
    t0=time.time()
    try:
        vid=json.load(urllib.request.urlopen(urllib.request.Request(B+"/v1/videos",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=120))["id"]
    except Exception as e:
        log("SUBMIT_ERR",j["id"],str(e)[:300]); time.sleep(30); continue
    st=None
    while time.time()-t0<3600:
        time.sleep(5)
        try: st=json.load(urllib.request.urlopen(B+f"/v1/videos/{vid}",timeout=30))
        except Exception: continue
        if st.get("status") in ("completed","failed"): break
    if not st or st.get("status")!="completed": log("FAIL",j["id"],json.dumps(st)[:600]); continue
    urllib.request.urlretrieve(B+f"/v1/videos/{vid}/content",dst); log("OK",j["id"],f"{time.time()-t0:.0f}s",os.path.getsize(dst))
log("H3_BATCH_END")
