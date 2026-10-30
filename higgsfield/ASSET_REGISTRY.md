# Asset registry: everything created for the Azulon films

Rule (B. Nikolov, 2026-10-30): **every generation is saved as a reusable asset, used or not.** New work goes into the Higgsfield project below. Its IDs go into `asset_registry.json` in the same commit.

Machine-readable copy: [`asset_registry.json`](asset_registry.json). Final cut list: [`the_remembering_edl.json`](the_remembering_edl.json).

## Higgsfield project "Azulon Asset Library"

`project_id 3aa118ac-52ba-4e84-9286-83e5b89ce16a` · workspace `bed6a21e-facf-4759-be68-02ac3d31594f`

| Folder | ID | Contents |
|---|---|---|
| 01 Identity | `fd86a534-e2ee-4325-a511-d6cf7684c699` | 20 Soul training crops, 4 smoke tests (A–D) |
| 02 Keyframes | `06f55c1a-01f1-4a0b-8a64-eea970662adf` | 53 keyframes (all takes, including rejected ones) |
| 03 Video clips | `474b4780-ad44-4fb6-aa5d-2a4d4f29ec78` | 24 Kling 3.0 clips (20 in the cut, 4 `_v1` superseded) |
| 04 Audio / score / final | `9db6af67-ef5f-4b7d-b98b-0d4e4d6a9766` | 6 character voice samples, score, *The Remembering v1* (91 s, 1080p) |
| 05 Lunar Purge v1 (rejected) | `c72fb19c-9fb9-4fb2-9a6d-644599b43364` | 8 stills from the abandoned first draft |

## Reference elements (put `<<<id>>>` in the prompt)

These work with Nano Banana Pro/2, GPT Image 2, Seedream 4.5/5 lite, Cinema Studio Image 2.5, Cinema Studio Video 2/3.0, Seedance 2.0, and Kling 3.0 (Kling only together with a `start_image`).

| Element | ID | Source keyframe | Use for |
|---|---|---|---|
| Blagoj-face | `319ccd19-46b7-4d9b-9d51-d74403161d64` | training photo | the hero's face (see [IDENTITY.md](IDENTITY.md)) |
| **Azulon-Master** | `5b059323-b615-45c0-b3b6-16a38f295aa3` | authenticity-checked 4-view set | **FINAL MASTER HERO**: photoreal, WoW-style ears, no chin dimple |
| Azulon-Canon (superseded) | `eaa589c5-b777-4e6a-90f2-e93b6fe9da4b` | 4-view lens-corrected turnaround | **MASTER HERO**, use this first |
| Azulon-Celestial | `b59b6eb8-c814-47de-a273-63372793a15c` | real photos 08/03/05/11, edited | **DEFAULT HERO**: true likeness, hairless, elven ears, Selûne tattoo (see [AZULON_CANON.md](AZULON_CANON.md)) |
| Azulon-Radiant | `7b50aafd-bbcb-496c-9c80-92a437ced884` | super portrait + back | super mode |
| Azulon-Body-Tattoo | `cbcca2cc-c2e9-4c5e-b380-ce8b7bb2c763` | turnaround | full-body tattoo map |
| Blagoj-shaven | `454a359e-cf57-4a41-b088-6d85b15ed816` | authentic shaven edits A/B/C | **default hero face**: clean-shaven, hairless, true likeness; aasimar markers via prompt |
| Azulon-Aasimar-shaven (demoted) | `e9e61b98-cf35-45d9-8d3e-0c1e9037299d` | shaven frontal edit | Radiant Soul look only; face drifted |
| Azulon-Aasimar (superseded) | `287ac548-837e-4d95-bcc7-1c3488298958` | aasimar edits | archived: moustache version |
| Azulon-Abolisher-armor | `136c4f9e-6a19-4189-9b39-af90c7f63c49` | 51 | hero costume; pair with Blagoj-face |
| Angel-of-Decay | `f9ae15c9-2d8b-48c7-82c0-b4ad4844aa1b` | c62 + e60 | corrupted Shard, full figure |
| Angel-of-Decay-face | `d13c93f5-057c-4303-9496-dedc39e723d6` | c110 | corrupted Shard, close-up |
| Shard-of-Selune-restored | `7cfd68a7-8516-4cd4-89ed-a1fae894d38a` | 151 | Shard after liberation |
| Moon-Shrine-set | `ce2b4019-89b3-435e-892d-828efaa6695a` | 11 | Selûne shrine (5-pillar ring) |
| Sanctum-of-Shar | `59721e8b-fcc3-447f-90ba-6f0f4c8f94c4` | f300 | Shar's temple |
| Selune-eclipse-sky | `dbd634f4-36d9-46e4-943f-9c2443a3fe6e` | 91 | eclipse sky plate |

Soul Cinema (`soul_cinematic` only): `b3ba42a8-305b-465a-b867-83432e48687c`. The mandatory phrase is in IDENTITY.md.

## Voices

| Character | ElevenLabs saved voice | Higgsfield voice clone | Sample in folder 04 (`audio_input`) |
|---|---|---|---|
| Azulon | `azvZ1e4ESkFJBQljyj23` | `7a859199-20c0-451e-a3a4-5a91b5aa4b35` ✓ | `742c537f-4851-412d-8614-3b92d44c8dbb` |
| Shar | `fVAgjfbrqAnDt9gAct91` | (not cloned) | `9c801227-2222-4bb3-81c1-1751d4b3e390` |
| Aelyra (fallen) | `RiJ99IDOJaFRrr92IRbN` | (not cloned) | `a59278fa-0ee3-4309-8133-8bf90dbaca3c` |
| Ysolde (fallen) | (cap of 3 reached) | (not cloned) | `6083ea50-89cc-42f9-a068-3bcc1a730d04` |
| Ysolde (restored) | (cap of 3 reached) | (not cloned) | `76ad304b-bd53-4f87-a3ac-34c64c8d8f14` |
| Selûne | (cap of 3 reached) | (not cloned) | `eb18ed66-b6c8-4d9a-9714-9d43cca04097` |

Each Higgsfield clone costs **40 credits**. The other five can be cloned at any time from the confirmed samples above with `create_voice_from_confirmed_audio`, and nothing is lost by waiting. Use clones with `generate_audio` / `voice_change` and `voice_type: "element"`.

## Audio and final film

- Score (ElevenLabs Music v2.5, flow `6Xoi7TYgNTCBKm8d2eik`): `audio_input 3b010d2b-90e7-4b34-a145-c02e12d51937`
- *The Remembering v1*: `video_input afe3b6e4-0450-47ff-a8c2-8ad2ac15ec39`

## Not in the cloud, by design

- Soul training photos and face crops (`faces/`, `face_dataset/`): biometric data, kept local and out of git.
- Local working copies (`keyframes/`, `output/`): they can be re-downloaded from the job IDs in `asset_registry.json`.
