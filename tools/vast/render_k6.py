#!/usr/bin/env python3
"""Kandinsky 6.0 Pro-distill (int8) test — same S01 shot as the Wan test.
Proven recipe from paladin_k6_run.py: Kandinsky6TI2VAPipeline, guidance 1.0, native audio.
Usage: render_k6.py <jobfile> <n>
"""
import json, os, sys, time, traceback
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
JOBFILE=sys.argv[1] if len(sys.argv)>1 else '/workspace/p23_wan65.json'
N=int(sys.argv[2]) if len(sys.argv)>2 else 1
jobs={j['n']:j for j in json.load(open(JOBFILE))}
j=jobs[str(N)] if str(N) in jobs else jobs[N]
print(f'[K6] shot {N} kf={j["kf"]}', flush=True)
import torch
from diffusers import Kandinsky6TI2VAPipeline
from diffusers.utils import load_image, encode_video
MODELS='/workspace/models/k6pro_int8'
t0=time.time()
pipe=Kandinsky6TI2VAPipeline.from_pretrained(MODELS, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
print(f'[K6] loaded in {time.time()-t0:.0f}s', flush=True)
torch.manual_seed(int(j['seed']))
t=time.time()
out=pipe(prompt=j['prompt'], image=load_image(j['kf']), height=480, width=832,
         num_frames=121, num_inference_steps=16, guidance_scale=1.0, sample_audio=True)
gen_s=time.time()-t
os.makedirs('/workspace/out_k6', exist_ok=True)
raw=f'/workspace/out_k6/p23_s{int(N):02d}_k6.mp4'
aud=getattr(out,'audio',None)
try:
    if aud is not None:
        encode_video(out.frames[0], fps=24, output_path=raw, audio=aud[0][None], audio_sample_rate=pipe.audio_sample_rate)
        print(f'[K6] native audio muxed @{pipe.audio_sample_rate}Hz', flush=True)
    else:
        encode_video(out.frames[0], fps=24, output_path=raw)
except Exception as e:
    print(f'[K6] audio mux fail {e}; video-only', flush=True)
    encode_video(out.frames[0], fps=24, output_path=raw)
print(f'[K6] DONE shot {N} gen_s={gen_s:.0f} size={os.path.getsize(raw)}', flush=True)
