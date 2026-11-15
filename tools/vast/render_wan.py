#!/usr/bin/env python3
"""Render the 65-clip Wan2.1-I2V-14B-720P batch for #23 Perseus & Medusa.

Start-frame-only (no END keyframes exist) -> Wan2.1-I2V-14B-720P Diffusers.
Usage: render_wan.py <jobfile> [start] [end]
  jobfile: /workspace/p23_wan65.json
Writes per-clip mp4 to /workspace/out_wan/, logs to stdout.
"""
import json, os, sys, time
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

JOBFILE = sys.argv[1] if len(sys.argv) > 1 else '/workspace/p23_wan65.json'
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 65

MODELS = '/workspace/models/wan_i2v14b'
# Option A resident recipe: 480x832x81 keeps the bf16 transformer + VAE + activations
# inside 45-48GB without per-step PCIe offload (the 178s/step killer).
NUM_FRAMES = int(os.environ.get('FRAMES', '81'))
HEIGHT = int(os.environ.get('H', '480'))
WIDTH = int(os.environ.get('W', '832'))
FPS = int(os.environ.get('FPS', '24'))
GUIDANCE = float(os.environ.get('GUIDANCE', '5.0'))
STEPS = int(os.environ.get('STEPS', '40'))

jobs = json.load(open(JOBFILE))
jobs = sorted([j for j in jobs if START <= j['n'] <= END], key=lambda j: j['n'])
print(f'[WAN] jobfile={JOBFILE} range={START}-{END} count={len(jobs)} '
      f'{WIDTH}x{HEIGHT}@{FPS} frames={NUM_FRAMES} steps={STEPS} g={GUIDANCE}', flush=True)

import torch
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video
from PIL import Image
from transformers import CLIPVisionModel

device = 'cuda'
image_encoder = CLIPVisionModel.from_pretrained(
    MODELS, subfolder='image_encoder', torch_dtype=torch.float32)
vae = AutoencoderKLWan.from_pretrained(
    MODELS, subfolder='vae', torch_dtype=torch.float32)
# 48GB VRAM recipe: slice the VAE decode (methods live on the VAE, not the pipe).
vae.enable_slicing()
vae.enable_tiling()
pipe = WanImageToVideoPipeline.from_pretrained(
    MODELS, vae=vae, image_encoder=image_encoder, torch_dtype=torch.bfloat16)
# Option A resident recipe: everything on GPU (480x832x81 fits). NO model_cpu_offload
# (that streams the 27GB transformer over PCIe every step = 178s/step).
pipe.to(device)
print('[WAN] pipeline loaded (resident, vae slicing/tiling)', flush=True)

# 48GB recipe: Wan2.1-I2V-14B bf16 does NOT fit 48GB with the T5 on GPU.
# Fix: encode ALL prompt embeddings with the text_encoder on CPU (manual
# tokenizer path, bypassing diffusers encode_prompt's device juggling which
# caused a cpu/cuda mismatch), then run transformer+VAE resident on GPU.
neg = ('blurry, low quality, distorted, watermark, text, cartoon, anime, '
       'deformed, extra limbs, lowres, jpeg artifacts')
print('[WAN] encoding prompts on CPU (text_encoder on CPU)...', flush=True)
pipe.text_encoder.to('cpu')
torch.cuda.empty_cache()
import torch.nn.functional as F
def enc(txt):
    ids = pipe.tokenizer(txt, padding='max_length', max_length=226,
                         truncation=True, add_special_tokens=True,
                         return_tensors='pt').input_ids.to('cpu')
    with torch.no_grad():
        h = pipe.text_encoder(ids.to('cpu')).last_hidden_state
    return h.to(device)
prompt_embeds = [enc(j['prompt']) for j in jobs]
neg_embeds = enc(neg)
print(f'[WAN] {len(jobs)} prompts + negative encoded on CPU', flush=True)

for idx, j in enumerate(jobs):
    n, kf, out, seed = j['n'], j['kf'], j['out'], j['seed']
    os.makedirs(os.path.dirname(out), exist_ok=True)
    print(f'[RENDER] START s{n} shot={j["shot"]} seed={seed}', flush=True)
    t0 = time.time()
    try:
        image = Image.open(kf).convert('RGB')
        # Wan wants the conditioning frame at generation resolution.
        if image.size != (WIDTH, HEIGHT):
            image = image.resize((WIDTH, HEIGHT), Image.LANCZOS)
        generator = torch.Generator(device=device).manual_seed(seed)
        out_frames = pipe(
            image=image,
            prompt_embeds=prompt_embeds[idx],
            negative_prompt_embeds=neg_embeds,
            height=HEIGHT,
            width=WIDTH,
            num_frames=NUM_FRAMES,
            guidance_scale=GUIDANCE,
            num_inference_steps=STEPS,
            generator=generator,
        ).frames[0]
        export_to_video(out_frames, out, fps=FPS)
        sz = os.path.getsize(out) if os.path.exists(out) else 0
        print(f'[RENDER] END s{n} size={sz} sec={int(time.time()-t0)}', flush=True)
        if sz == 0:
            print('---ERRTAIL--- zero-size output, aborting', flush=True)
            sys.exit(1)
    except Exception as e:
        print(f'[RENDER] ERR s{n} {type(e).__name__}: {e}', flush=True)
        import traceback; traceback.print_exc()
        sys.exit(1)

print('[RENDER] ALL_BATCH_DONE', flush=True)
