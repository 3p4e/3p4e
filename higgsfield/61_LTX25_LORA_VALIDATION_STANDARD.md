# 61 — LTX-2.5 LoRA Validation Standard (turning a training run into a DD identity asset)

## Core validation config (trainer YAML)
```yaml
validation:
  interval: 100-250
  samples:
    - prompt: "dd_demon_hunter standing in a fungal marsh at dusk, teal hair floating"
      conditions: [{type: first_frame, image_or_video: "/path/to/dd_keyframe.png"}]
    - prompt: "dd_demon_hunter walking through a dark forest, frost-arcane armor, floating teal-blue hair"
  video_dims: [960, 544, 49]
  inference_steps: 30        # Dev; use ~8 / CFG 1.0 for Distilled validation
  generate_audio: true
  seed: 42
checkpoints: {interval: 250, keep_last_n: -1}
```
ALWAYS two samples: (1) first-frame conditioned, (2) text-only with trigger in a NEW setting.

## How to read results
| Observation | Meaning | Action |
|---|---|---|
| Identity weak on both | Undertrained / low capacity | Raise rank (64-128), more steps, better captions |
| Strong identity, every scene identical | Overfitting | Step back to earlier checkpoint; lower LR next run |
| First-frame good, text-only weak | Identity depends on reference | OK for production if always I2V; improve diversity if need pure T2V |
| Audio noisy/bubbling | Overtraining signal | Stop; use earlier checkpoint |
| Samples broken | Settings mismatch | Distilled validation = ~8 steps / CFG 1.0, NOT Dev settings |

## Protocol
1. Train keep_last_n -1, validate every 100-250.
2. Per checkpoint: face + floating teal hair match DD? text-only still shows character in new env?
3. Pick latest checkpoint that holds identity WITHOUT forcing every scene identical.
4. Held-out test: new prompts + new keyframes outside the trainer.
5. Final: load in full ComfyUI two-stage I2V + IC-LoRA pipeline, verify against existing gates.

## Notes
- Trainer validation runner is single-stage; production two-stage (ltx-pipelines/ComfyUI) is more representative.
- First-frame conditioned validation is more reliable than pure T2V for identity.
- Review auto-generated captions before preprocessing — poor captions are the most common weak-identity cause.


---

## Sunder 60s Validation Sequence

1. Train AZ LoRA → validate (3 seeds vs az_cards_final) → pass/fail
2. Train DD LoRA → validate (3 seeds vs dd_cards_final) → pass/fail
3. Only proceed to batch when BOTH LoRAs pass identity gates
