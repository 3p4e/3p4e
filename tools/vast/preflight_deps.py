#!/usr/bin/env python3
"""Preflight dependency + node check for Qwen-Image-Edit-2511 on the rental."""
import importlib, os, sys

print("python", sys.version.split()[0])
mods = ["torch","einops","transformers","tokenizers","safetensors","av",
        "sentencepiece","aimdo","comfy_aimdo","comfy_kitchen","numpy","PIL"]
for m in mods:
    try:
        mod = importlib.import_module(m)
        print("OK   ", m, getattr(mod, "__version__", ""))
    except Exception as e:
        print("MISS ", m, type(e).__name__, str(e)[:80])

import torch
print("torch", torch.__version__, "cuda", torch.version.cuda, "avail", torch.cuda.is_available())

print("\n--- ComfyUI node scan ---")
comfy = "/opt/workspace-internal/ComfyUI"
needle = b"TextEncodeQwenImageEditPlus"
search_roots = [os.path.join(comfy, "comfy_extras"), os.path.join(comfy, "custom_nodes")]
found = []
for root in search_roots:
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.endswith(".py"):
                p = os.path.join(dirpath, fn)
                try:
                    if needle in open(p, "rb").read():
                        found.append(p.replace(comfy, "."))
                except Exception:
                    pass
print("QwenImageEditPlus node files:", found or "NOT FOUND")
print("\n--- qwen weight files present ---")
for sub, names in [
    ("diffusion_models", ["qwen_image_edit_2511_fp8mixed.safetensors"]),
    ("text_encoders", ["qwen_2.5_vl_7b_fp8_scaled.safetensors"]),
    ("vae", ["qwen_image_vae.safetensors"]),
]:
    d = os.path.join(comfy, "models", sub)
    for n in names:
        p = os.path.join(d, n)
        print(f"  {sub}/{n}: {'YES ' + str(os.path.getsize(p)) if os.path.exists(p) else 'no'}")
print("\n--- disk ---")
os.system("df -h /workspace /opt/workspace-internal 2>/dev/null | tail -3")
