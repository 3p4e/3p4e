#!/usr/bin/env python3
"""Fix Sunder jobfiles per the 2026-11-18 pre-render review.

C2 -> resolution made 32-divisible (768x448 proof parity, 1280x704 film).
C1 -> strip nonexistent character LoRAs; identity becomes keyframe-anchor-only.
I2 -> drop unimplemented fields (two-stage upscale, pose/depth control, end
      keyframes, model-label fields that do not match the real filenames).
      audio set false because the v1 render path has no audio-VAE decode.
Idempotent; keeps a .bak of the original on first run.
"""
import json
import os
import shutil

BASE = "higgsfield/sunder_prompts"

# file -> target resolution (must be divisible by 32 both axes)
TARGETS = {
    "p23_sunder_phase1.json": "768x448",        # proof parity / cheapest
    "p23_sunder_ltx25.json": "1280x704",        # film target
    "p23_sunder_ltx25_121f_90s.json": "1280x704",
    "p23_hb_vx_70s.json": "1280x704",
}

DEAD_KEYS = {
    "character_lora", "lora_strength", "lora_training_order",
    "two_stage", "spatial_upscaler", "control", "control_ref", "end",
    "transformer", "text_encoder", "vae_video", "vae_audio",
    "loras", "characters", "char_lora", "char_lora_strength",
}


def fix_entry(e, res):
    e["resolution"] = res
    for k in DEAD_KEYS:
        e.pop(k, None)
    # identity strategy for the v1 render path: keyframe anchor, no LoRA
    e["identity"] = "keyframe-anchor"
    e["audio"] = False
    e["audio_note"] = (
        "LTX-2.5 native audio is not decoded in the v1 render path; "
        "restore via audio VAE + AV-latent nodes to enable."
    )
    return e


def main():
    for fn, res in TARGETS.items():
        p = os.path.join(BASE, fn)
        if not os.path.exists(p):
            print("MISSING", fn)
            continue
        d = json.load(open(p))
        if isinstance(d, dict) and "shots" in d:
            entries = d["shots"]
            kind = "dict-shots"
        elif isinstance(d, list):
            entries = d
            kind = "list"
        else:
            print("SKIP (unknown shape)", fn)
            continue

        bak = p + ".bak"
        if not os.path.exists(bak):
            shutil.copy(p, bak)
        for e in entries:
            fix_entry(e, res)
        json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
        print(f"FIXED {fn}: {len(entries)} entries -> {res} ({kind})")


if __name__ == "__main__":
    main()
