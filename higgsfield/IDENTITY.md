# Hero identity: Blagoj Nikolov (use these IDs for every future generation with my face)

| Asset | ID | Use with | How |
|---|---|---|---|
| **Soul Cinema** (trained, 20 photos) | `b3ba42a8-305b-465a-b867-83432e48687c` | `soul_cinematic` image model only | `generate_image` `model: soul_cinematic`, `soul_id: <id>`, `quality: 2k` |
| **Reference Element** `Blagoj-face` | `319ccd19-46b7-4d9b-9d51-d74403161d64` | Nano Banana Pro / 2, GPT Image 2, Seedream 4.5 / 5 lite, Cinema Studio Image 2.5, Cinema Studio Video 2 / 3.0, Seedance 2.0, Kling 3.0 (Kling only together with a `start_image`) | put `<<<319ccd19-46b7-4d9b-9d51-d74403161d64>>>` inside the prompt text |

Higgsfield also auto-created an element named `Blagoj` (`8519f8e0-4e1e-4a62-89f3-21767456e5ec`) from one training photo. Prefer `Blagoj-face`: it was hand-picked as frontal, eyes open and evenly lit.

## Training set (provenance)

- Source: 58 phone selfies (Viber-exported JPEG, 1202×1600), Google Drive, 2026-10-30.
- Screened with `tools/face_qc.py dataset`:
  - 11 rejected as blurry or no face detected;
  - 5 excluded by hand (1 with glasses, 4 with eyes closed or squinting);
  - 20 selected for angle diversity (yaw index −2.42 to +0.62, both profiles included).
- Higgsfield media IDs of the 20 crops: `face_dataset/uploaded_media_ids.json` (local only, not in git).

## Known weaknesses of this training set

- **One session**: same shirt, same white office wall, same flat fluorescent light. The Soul may pull the grey shirt or the pale background into results. Counter this with strong wardrobe and set descriptions in the prompt.
- **Arm's-length selfies**: the wide-angle lens slightly enlarges the nose and forehead. Generated "85 mm" portraits may look subtly different from you, and that comes from the input, not the model.
- **Downward gaze** in many photos: the eyes tend to come out heavy-lidded. Add "eyes open, direct gaze" when it matters.
- **Viber compression** has removed fine skin texture.

**To improve later:** do one retraining with 10–15 photos taken by someone else at 2–3 m distance. Use a normal or short-tele lens (2× zoom on a phone), daylight from a window, two different shirts and a darker background. Then compare with `face_qc.py verify`.

## Data protection

These photos are biometric data (GDPR Art. 4(14), Art. 9). They live in `faces/` and `face_dataset/`, which are excluded from git by `.gitignore`. Copies are held by Higgsfield (Soul training + uploads) and in the Google Drive folder, which is **publicly link-shared**. Restrict that folder to "Restricted" sharing now that the download is done.
