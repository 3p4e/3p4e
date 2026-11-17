#!/usr/bin/env python3
"""K6 Lite full batch: all shots in jobfile, TI2VA + native audio, per-shot seed, resume-safe."""
import json, os, sys, time, traceback
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
JOBFILE='/workspace/p23_wan65.json'
OUT='/workspace/out_k6'
jobs=json.load(open(JOBFILE))
os.makedirs(OUT, exist_ok=True)
import torch
from diffusers import Kandinsky6TI2VAPipeline
from diffusers.utils import load_image, encode_video
pipe=Kandinsky6TI2VAPipeline.from_pretrained('/workspace/models/k6lite', torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
print('[K6BATCH] loaded', flush=True)
done=0
for j in jobs:
    n=j['n']; shot=j['shot']
    out=f'{OUT}/p23_s{int(n):02d}_k6.mp4' if not str(shot).startswith('F') else f'{OUT}/p23_{str(shot).lower()}_k6.mp4'
    if os.path.exists(out) and os.path.getsize(out)>100000:
        done+=1; continue
    kf=j['kf']
    if not os.path.exists(kf):
        print(f'[{shot}] MISSING kf {kf}', flush=True); continue
    try:
        torch.manual_seed(int(j['seed']))
        t=time.time()
        o=pipe(prompt=j['prompt'], image=load_image(kf), height=480, width=832, num_frames=121, num_inference_steps=16, guidance_scale=1.0, sample_audio=True)
        gs=time.time()-t
        aud=getattr(o,'audio',None)
        try:
            if aud is not None:
                encode_video(o.frames[0], fps=24, output_path=out, audio=aud[0][None], audio_sample_rate=pipe.audio_sample_rate)
            else:
                encode_video(o.frames[0], fps=24, output_path=out)
        except Exception:
            encode_video(o.frames[0], fps=24, output_path=out)
        print(f'[{shot}] DONE gen_s={gs:.0f} size={os.path.getsize(out)}', flush=True)
        done+=1
    except Exception as e:
        print(f'[{shot}] FAIL {e}', flush=True)
    finally:
        try: del o
        except: pass
        torch.cuda.empty_cache()
print(f'[K6BATCH] ALL_DONE {done}/{len(jobs)}', flush=True)
