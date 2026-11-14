# 44 — VAST #23 Perseus & Medusa: Error Register + Lessons (2026-11-14)
Every production error encountered, its root cause, the fix, and the durable rule.
Source: live #23 render day — 60-clip v1 batch, v2/v3/v4 prompt iterations, box rentals.

---

## A. Prompt-authoring errors (ours, fixed)

| # | Error | Root cause | Fix | Durable rule |
|---|---|---|---|---|
| A1 | **Slideshow renders** — clips read as Ken Burns zoom stills | Motion prompts were guard-boilerplate only + opened with "slow motion continuing from the start frame" — the only thing the model could do was drift-zoom | v4 rewrite: 60 hand-authored visceral action clauses (active verbs, world reacts, camera energised), "slow motion" banned | Every motion prompt must describe SUBJECT action with concrete verbs; "slow motion" is a banned phrase in VAST render prompts |
| A2 | **S53 shield morph** — a shield materialised that the beat never called for | Prompt invented "shield rises to guard his face" when the beat says nothing about a shield | Re-prompt: kibisis draw only + explicit "No shield appears in his hands" | Never add props to a prompt that the shot's beat doesn't mention — the model materialises anything you name |
| A3 | **S54 serpent body morph** | Two-phase action ("rears then stills") forced a body transformation mid-clip | Single-phase: "already fully reared and still, locks its gaze — only the eyes move" | One phase per clip. Gaze moments = eyes only |
| A4 | **S55 random people** — two invented figures | Beat said "waves over fossilized coils" (no people) but prompt said "the two figures at the rock's edge" — no anchor | Re-prompt: stone reef + sea + gulls, explicit "No people in frame" | Never name a character without an anchor; crowd shots get explicit "no people" unless cast |
| A5 | **S48 near-static** — motion 1.34, flat luma | The prompt's Action was "recounting the offense" — a talking-head beat with no motion vocabulary | Kinetic-grief rewrite: hands gesture, hair slaps, chains swing, breath sobs | Emotional beats must be written as FULL-BODY MOTION, not facial descriptions |
| A6 | **Medusa legs** — model grew human legs instead of her snake body | Prompts described coiling tail but never explicitly NEGATED legs — the model "corrects" to biped | Hard canon guard added to all 13 keyframe blocks + 7 render prompts: "NO legs, NO human lower body, NO feet" + negatives | Every hybrid-creature prompt must carry a body-form guard + leg-negatives. Generators default to bipedal — say it in the negative |

## B. Stack / CLI errors (fixed, some cost paid)

| # | Error | Root cause | Fix | Durable rule |
|---|---|---|---|---|
| B1 | **Silent render failures (size=0)** — script logged END with stale file sizes | Render script piped output through `grep` filters that swallowed argparse errors; `stat` then read the PREVIOUS render's file | Run renders manually with full output capture to see the real error; verify output timestamps, not just sizes | Never trust a filtered log — capture stderr on failure; verify file mtime after render |
| B2 | **`--steps/--guidance` rejected by new CLI** | The LTX-2 clone updated: `--steps/--guidance` removed from `ltx_pipelines.distilled`; defaults now apply | Read `--help` on the box; drop the flags | Always re-check `--help` after any `git clone` — CLI args drift between versions |
| B3 | **Gemma 403 (gated repo)** | `google/gemma-3-12b-it` requires licence acceptance; both HF tokens unauthenticated | Switch to ungated `unsloth/gemma-3-12b-it` mirror | For gated models, pre-verify the mirror is ungated before the paid window opens |
| B4 | **Gemma `processor_config.json` missing** then **preprocessor_config.json missing** | Download script fetched only weights + tokenizer; the new LTX-2 code requires the full processor sidecar chain | Fetched `processor_config.json` + `preprocessor_config.json` (the image-processor fallback sidecar) | Gemma dir for LTX-2.3 = weights + index + config + tokenizer.model/json/config + generation_config + processor_config.json + preprocessor_config.json + special_tokens_map — check the code's sidecar list, not a blog |
| B5 | **curl rc=23 retry loop (silent)** | Download script wrote to a directory that didn't exist; curl failed 16× per file while billing continued | `mkdir -p` the target first; check rc per file | Every download loop must mkdir its target and check exit codes — a silent retry loop on a billing box is money burning |
| B6 | **Mid-rental SSH key-injection death (3 boxes)** | Known account-wide Vast issue: box running but all SSH auth dies after host events; `authorized_keys` gets wiped | Self-heal cron on the box rewrites authorized_keys every 60s; if SSH is dead → destroy + rent replacement | Assume any long rental will lose SSH once. Self-heal cron is mandatory; keep instance JSON + scripts re-pushable |
| B7 | **First render run used a stale clone's CLI flags** | `--prompt-file/--output/--upscale` from the old clone vs `--prompt/--output-path/--spatial-upsampler-path` in the new | Read the actual `--help` on the box before writing the script | Same as B2 — the KB recipe is a starting point; the live `--help` is law |
| B8 | **v3 renders wrote to same paths as v2** (fake "identical sizes") | Output filename came from the JOBFILE not the script; sed on the script couldn't change it | Patch the jobfile's `out` field; verify timestamps | Render scripts take output paths from the jobfile — changing the script doesn't change the output path |

## C. Model-behaviour learnings (not errors — properties of LTX-2.3 distilled)

| # | Learning | Evidence | Consequence |
|---|---|---|---|
| C1 | **Image-conditioning strength controls motion ceiling** | strength 0.7 → gentle; 0.5 → combat beats 10× (S21 0.56→1.20, max 18.7) | Use 0.5 as the default for action scenes; 0.7 only when identity lock outweighs motion |
| C2 | **"Majestic creature" = slow drift, immune to prompt escalation** | S32 Pegasus: 0.16→0.17→0.32 across three prompt generations | Creature wide-shots read as stately cinema regardless. Keyframe must show the body mid-violent-motion to break the prior |
| C3 | **Combat/impact beats respond to lower strength + violent verbs** | S52 ketos: 0.11→1.39 (max 20.6) with escalation | Where the beat is full-body violence, the model delivers it |
| C4 | **The motion gate threshold must match the failure class** | v1 batch "passed" a ≥1.5 gate that measured *anything moving*, not *a scene happening* | Gate per class: static-detect for slideshow, frame-diff max for action-spike, luma curve for flicker |
| C5 | **Smooth light ramps read as flicker by naive std** | S54 flagged 16.12 std but zero spike frames — an intentional storm-light change | Flicker gate needs a spike detector, not just std |

## D. Process rules adopted this day (director decrees)

| # | Rule | Source |
|---|---|---|
| D1 | **Per-clip analysis on every delivery** — after each pull: ffprobe specs, per-frame motion metrics, luma curve, 5-frame contact strip, beat comparison; reported WITH the delivery | Director 2026-11-14 |
| D2 | **Resolution directive in every keyframe prompt** — "generate at 2432×1408 minimum, ideally 3840×2160 (4K landscape)" | Director 2026-11-14 |
| D3 | **AZ face card attached to every Perseus keyframe block** — canonical `az_face_card.jpg` (SHA 0096852430cd4739…) alongside his P1/P2 sheets | Director 2026-11-14 |
| D4 | **Boss-fight doctrine** — fight scenes get a full arc (clash/evade/overwhelm/dominant/near-death/feint/reversal/mechanic/setup/kill), not a quick exchange | Director 2026-11-14 (F01–F10 pack) |
| D5 | **High-contrast action register** — chiaroscuro, hard rim-light, crushed blacks, motion blur in every render prompt | Director 2026-11-14 |

---

Artifacts this register governs:
- `tools/vast/jobs/p23_batch60_v4.json` — 60 action prompts (current canonical render set)
- `storybook_ocr/specs/23_GROK_60_KEYFRAME_PROMPTS.md` — 60 blocks with resolution directive + AZ card + Medusa guard
- `storybook_ocr/specs/23_GROK_FIGHT_EXPANSION_PROMPTS.md` — F01–F10 boss-fight keyframes
- `tools/render_v2.sh / render_v3.sh / render_v3b.sh` — LTX-2.3 new-CLI render scripts
- `tools/build_23_v4_jobfile.py` — the v4 prompt builder (rerunnable)
