import os, re
C = "/workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo"

print("=== LTX-Video node source: folder / filename-list / class defs ===")
pat = re.compile(r'(folder_names|get_filename_list|MODELS_DIR|models_dir|text_encoders|checkpoints|vae|loras|upscale|diffusion_model|latent_upscale|audio)')
for root, dirs, files in os.walk(C):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, C)
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            hits = [ln.strip() for ln in txt.splitlines() if pat.search(ln) and len(ln.strip()) < 160]
            if hits:
                print("\n--- " + rel + " ---")
                for h in hits[:25]:
                    print("   " + h)
