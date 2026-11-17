# 57 — Hollow Bloom v2 — operational clarifications (Grok, closed Q1–Q8) + LTX identity-lock
# Received 2026-11-16 ~00:00 CET. All values concrete, production-ready.

## Q1 KEYFRAME WORLD CONSISTENCY
Pin ONE shared header on every keyframe prompt (do NOT restore per-shot env blocks):
"Photoreal 35mm anamorphic, real skin, film grain, dusk light. Dying fungal marsh at dusk:
pale-blue mushroom towers, luminous spore-mist, teal-glowing water, corruption ring.
Teal/slate palette, pale-blue bioluminescence, one molten-gold accent."
Per-shot prompts then only describe action + character state + framing. The header is the lock.

## Q2 DWPOSE CONTROL-VIDEO SOURCING
- Crossbow draw+fire: self-record phone OR stock "archer drawing bow"/"crossbow loading"; full-body, side/3-4 view.
- Greatsword raise+Verdict: self-record or stock "two-handed sword overhead strike" (match AZ one-sided motion).
- Vault+land: stock "parkour vault"/"jump landing"; camera locked.
- Bloom rupture/tendril whip: NO human reference — skip pose; use Video Depth Anything + HOLD, or free I2V.
- DD weightless hair: NOT pose-controllable — start-frame + HOLD only.
Rule: clean realistic single-subject footage; previous-clip extraction = last resort.

## Q3/Q4 MODEL ROUTING (48GB, lightx2v)
| Shot type | Model | Control | Steps/CFG/Strength |
| Extreme CU (face/hair/tattoo) | LTX-2.3 Dev | none (start only) | 30-40 / 3.0-3.5 / start 0.7-0.8 |
| Hero action (DD/AZ combat) | Wan 2.2 Fun Control | DWPose + Depth | 4-step lightx2v / CFG 1.0-1.5 / 0.6-0.8 |
| Environment/wide/Bloom | Wan 2.2 Fun Control | Depth only | 4-step / CFG 1.0 / 0.5-0.7 |
| Fast chaos/secondary | LTX Distilled | none | 8-12 / CFG 2.0-2.5 |
LTX-Dev extreme CUs: #07, #22, #31, #44-45 + the 3 CU inserts. All else = Wan Fun Control.

## Q5 RESOLUTION (16:9 on 48GB)
Keyframes: 1280x720 native 16:9. Video: 864x480 or 960x540 reliable; 1280x720 safe ceiling
(batch 1, fp8 high/low + lightx2v). lightx2v pair valid on Fun Control graph. NEVER 640x640.

## Q6 SYNC BEATS (24fps)
Clip #44 = 40 frames (1.67s), impact frame 28-30. Clip #45 = 35 frames (1.46s), impact 24-26.
D5 MK 1.68s / D6 MK 1.44s land on the impact frames; stems timed to frame.

## Q7 VERIFICATION GATES (reject on 2+ failures)
start-corr >=0.92 (CLIP cosine) · drift-drop <=15% (RAFT/Farneback flow) · face-count exact
(InsightFace/MTCNN) · palette HSV <=12 (OpenCV hist) · motion band 2-18 px/frame · sharp >=80 (Laplacian var).

## Q8 ESCALATION LADDER (max 4 attempts/hero shot)
1) Wan FC + DWPose + HOLD (lightx2v) -> 2) pose strength 0.8-0.9 + seed lock ->
3) LTX Dev 30-40 steps CFG 3.2 start 0.75 same seed family -> 4) LTX Dev + tighter face crop.
Then accept best or hold the start keyframe longer.

## LTX-2.3 IDENTITY LOCK (no native ref-to-video)
Core: start strength 0.75-0.85 · same seed family · tight face crop (face 40-60% of frame) ·
minimal HOLD prompt · clips <=49-97 frames (<=4-5s). Identity prompt line:
"Composition, subjects and palette hold. Only the named action moves. [Char] keeps the exact
same face, glowing teal-blue weightless hair, and frost-arcane armor as the start frame."
Community tools (escalation): LTX-Best-Face-ID LoRA (rank128, TASS-RoPE source_id=2 overlap
conditioning + ArcFace loss; prompt must start 'ref_t2v:'; BFS Nodes Identity Transfer) ->
LTX Likeness Guide node (persistent face anchor) -> IC-LoRA character sheet -> ID-LoRA (talking heads).
DD's weightless glowing hair is the hardest element; face card + Best-Face-ID is the best current lock.
ST-DRC paper: arXiv:2606.02441 (TASS-RoPE mechanism).
