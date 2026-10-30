# Hero identity: Blagoj Nikolov (use these IDs for every future generation with my face)

| Asset | ID | Use with | How |
|---|---|---|---|
| **Soul Cinema** (trained, 20 photos) | `b3ba42a8-305b-465a-b867-83432e48687c` | `soul_cinematic` image model only | `generate_image` `model: soul_cinematic`, `soul_id: <id>`, `quality: 2k` |
| **Reference Element** `Blagoj-face` | `319ccd19-46b7-4d9b-9d51-d74403161d64` | Nano Banana Pro / 2, GPT Image 2, Seedream 4.5 / 5 lite, Cinema Studio Image 2.5, Cinema Studio Video 2 / 3.0, Seedance 2.0, Kling 3.0 (Kling only together with a `start_image`) | put `<<<319ccd19-46b7-4d9b-9d51-d74403161d64>>>` inside the prompt text |

Higgsfield also auto-created an element named `Blagoj` (`8519f8e0-4e1e-4a62-89f3-21767456e5ec`) from one training photo. Prefer `Blagoj-face`: it was hand-picked as frontal, eyes open and evenly lit.

## Mandatory prompt phrase (verified)

The Soul fixes the face, not the head. Every prompt with this identity must contain:

> **"completely shaved bald head, short ginger-brown moustache and light stubble, eyes open"**

| Smoke test 2026-10-30 (soul_cinematic, 16:9, 2k) | Likeness (SFace cosine vs training set) | Head/hair |
|---|---|---|
| A, without phrase | 0.792 | short hair added ✗ |
| B, without phrase | 0.740 | shoulder-length hair + earrings ✗ |
| C, with phrase | 0.870 | correct ✓ |
| D, with phrase | 0.863 | correct ✓ |

Acceptance limit 0.50; same-person threshold 0.363. The face-embedding score **does not see hair**, so check head and hair by eye on every keyframe.

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

## Race: Aasimar (Protector), added 2026-10-30

Azulon is a **Protector Aasimar**, a mortal with celestial blood guided by an angelic spirit. The race was chosen because it fits the story (a paladin of Selûne who restores her fallen celestial Shards) and because it keeps a human face, so the likeness survives.

| Asset | ID | Likeness (SFace) |
|---|---|---|
| Element **`Azulon-Aasimar`** | `287ac548-837e-4d95-bcc7-1c3488298958` | built from the two edits below |
| NB Pro edit, ¾ profile, cloak + pauldron | job `fb7c1ff6-b04a-482e-a99c-614690ce2030` | 0.725 |
| NB Pro edit, frontal, gambeson + crescent gorget | job `2edbe5f7-3749-4a77-b8b2-ddc6495502fb` | 0.779 |
| Soul tests (human-looking; traits too faint) | `504d8189…` 0.879 · `61a9fa83…` 0.741 (Radiant Soul: glowing eyes + spectral wings) · `0acdb460…` 0.722 · `0fefd826…` 0.848 | |

**Racial markers (keep identical in every shot):** luminous moon-silver irises; a silver crescent-moon birthmark on the left temple; fine silver celestial filigree tracing from the crescent over the scalp; a faint pearlescent skin sheen. For **Radiant Soul** moments, add white-glowing eyes and two translucent wings of moonlight.

**Lesson learned:** Soul Cinema pulls everything back to the training face, so the racial markers come out too faint. The working pipeline is a Soul portrait first, then a Nano Banana Pro edit that adds the markers. In video, call `<<<287ac548-837e-4d95-bcc7-1c3488298958>>>`, or use one of the two edits as the Kling start frame.
