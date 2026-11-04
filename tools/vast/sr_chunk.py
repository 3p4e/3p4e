import os, time, traceback
import torch
os.environ.setdefault("PYTORCH_ALLOC_CONF","expandable_segments:True")
import imageio.v3 as iio
from diffusers import Kandinsky6SRPipeline
from diffusers.utils import export_to_video

OUT="/workspace/out"
SR="kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers"
CH  = int(os.environ.get("CHUNK","29"))   # must be 1 + k*4
STR = int(os.environ.get("STRIDE","28"))  # must be multiple of 4
def log(*a): print(time.strftime("[SR %H:%M:%S]"),*a,flush=True)
assert CH % 4 == 1, "CHUNK must be 1 mod 4"
assert STR % 4 == 0, "STRIDE must be 0 mod 4"

sr = Kandinsky6SRPipeline.from_pretrained(SR, torch_dtype=torch.bfloat16)
sr.enable_model_cpu_offload()
log("loaded", "CHUNK=%d STRIDE=%d" % (CH,STR))

def spans(n):
    out=[]; s=0
    while True:
        e=min(s+CH,n); L=e-s
        assert L % 4 == 1, f"illegal chunk {s}:{e} = {L}"
        out.append((s,e))
        if e>=n: break
        s+=STR
    return out

ONLY=[x for x in os.environ.get("ONLY","").split(",") if x]
for sid in (ONLY or ["p1_1","p1_2","p1_3","p1_4a"]):
    src=f"{OUT}/k6_{sid}_gen.mp4"; dst=f"{OUT}/k6_{sid}_1080.mp4"
    if not os.path.exists(src): log(sid,"MISSING"); continue
    if os.path.exists(dst) and os.path.getsize(dst)>200000: log(sid,"EXISTS skip"); continue
    try:
        t=time.time()
        frames=[f for f in iio.imiter(src, plugin="pyav")]
        n=len(frames); sp=spans(n)
        log(sid,f"in {n}f {frames[0].shape} chunks={sp}")
        acc=[]
        for k,(s,e) in enumerate(sp):
            chunk=frames[s:e]
            log(sid,f"chunk{k} {s}:{e} L={len(chunk)} vram={torch.cuda.memory_allocated()/2**30:.1f}G")
            up=sr(video=[chunk], resolution_scale=2.25, num_inference_steps=2).frames[0]
            if k>0: up=up[1:]          # drop duplicate overlap frame
            acc.extend(up)
            del up,chunk; torch.cuda.empty_cache()
        log(sid,f"out {len(acc)}f {acc[0].shape}")
        export_to_video(acc, dst, fps=24)
        log(sid,f"OK {time.time()-t:.0f}s {os.path.getsize(dst)/1e6:.1f}MB")
        del frames,acc; torch.cuda.empty_cache()
    except Exception as ex:
        log(sid,"FAIL",str(ex)[:250]); log(traceback.format_exc()[-700:]); torch.cuda.empty_cache()
log("SR DONE")
