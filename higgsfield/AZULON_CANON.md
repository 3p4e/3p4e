# Azulon: canonical look (paste these blocks verbatim into every prompt)

## Base
completely hairless smooth shaved head, clean-shaven face with no moustache, no beard and no stubble, natural eyebrows kept, natural grey-green eyes, eyes open, mouth closed, no earrings, real skin age and texture, unretouched

## Ears (Aasimar–celestial)
ears elongated into elegant pointed elven tips, extended about two to three centimetres upward and backward, natural anatomy, same skin tone and texture as the face

## Tattoo, dormant state (persistent; every shot)
fine-line tattoo in faded silver-grey and pale moon-blue ink, low contrast, semi-transparent, close to skin tone so it reads at a second glance but clearly covers the body; Selûne lunar sacred-geometry design: a small crescent moon at the centre of the forehead; thin concentric lunar-phase arcs and flowing filigree radiating from the crescent over the crown and down the back of the skull; two thin parallel vertical lines through each eye, running from mid-forehead through the eyebrow, across the eyelid and down the cheekbone to the jawline; a narrow band of tiny moon-phase symbols around the neck; filigree continuing down the neck, over shoulders, along the spine across the back, down both arms in spiralling bands to the backs of the hands and the knuckles; no solid black blocks, no text

## Tattoo, awakened state ("super mode" / Radiant Soul)
the same tattoo lines blaze with arcane moon-white and pale-blue energy and thin licks of silver-blue flame rising from the lines, light spilling onto the skin, eyes glowing white

## Reference assets (2026-10-30)

**Element `Azulon-Celestial` = `b59b6eb8-c814-47de-a273-63372793a15c`.** This is now Azulon's default identity. Put `<<<b59b6eb8-c814-47de-a273-63372793a15c>>>` in the prompt and paste the blocks above verbatim.

The head references come from six real photos chosen to cover every angle (from `face_dataset/`). Each was edited with Nano Banana Pro, keeping the real photo as the base image.

| Real photo # | Angle | Edit job | Likeness (SFace) | In element |
|---|---|---|---|---|
| 08 | frontal | `b129f88f-4a53-49c4-8959-1b928c6640dc` | 0.744 | ✓ |
| 03 | ¾ left | `33235324-ad77-4a2a-82cf-015a69a5c161` | 0.631 | ✓ |
| 05 | ¾ right, high | `cacd4877-af87-4c70-a3b2-146150232ffd` | 0.626 | ✓ |
| 14 | ¾ frontal | `1fd0fc97-f6ef-4eee-a208-c0260007012b` | 0.614 | |
| 11 | right profile | `29d3bef0-217c-47ec-920c-6d66f915b689` | 0.518 | ✓ (ear and tattoo view) |
| 02 | left profile | `64268b3a-93f5-4aab-9926-e9ec5df059e5` | 0.450 (WEAK) | ✗ |

The profile scores are low partly because SFace is weak on profiles. The source photos also show the eyes looking down or closed.

| Body / power state | Job |
|---|---|
| Super mode, back view (mandala, spine crescents, arm bands to the hands, flames) | `af66b588-7214-42b7-84ab-53e8f6fa6bda` |
| Full-body turnaround (front + back, dormant) | `e93d67e5-eeb0-465b-85c9-9c8a05190782` |
| Super mode portrait | `50929453-5255-4511-af86-04cf1337f89f` |

**What stays consistent:** the forehead crescent, two vertical lines through each eye, the moon-phase neck band, and the pointed ears.

**What still drifts:** the crown and scalp filigree pattern differs between images. AI models do not reproduce intricate tattoos line for line. Expect small variations from shot to shot, and use one locked image as the start frame for every video shot.

| Element | ID | Use |
|---|---|---|
| **Azulon-Celestial** | `b59b6eb8-c814-47de-a273-63372793a15c` | default hero, dormant tattoos |
| **Azulon-Radiant** | `7b50aafd-bbcb-496c-9c80-92a437ced884` | super mode (tattoos aflame, eyes glowing); super portrait likeness 0.681 |
| **Azulon-Body-Tattoo** | `cbcca2cc-c2e9-4c5e-b380-ce8b7bb2c763` | full-body tattoo map, front + back |

Known flaw: the turnaround body came out as a sculpted, gym-built physique with a slightly CGI render look. It is not his real build. Use it for the tattoo layout only, never as the body type. Prompt: "lean wiry build, not muscular".

## MASTER identity: `Azulon-Canon` = `eaa589c5-b777-4e6a-90f2-e93b6fe9da4b` (2026-10-30, supersedes Azulon-Celestial)

The four views were generated from six references at once: real selfies 08, 14, 06, 03 and 11, plus the tattoo reference `b129f88f…`. The prompt asked for **lens correction** (85 mm at 2.5 m) and a celestial refinement of at most 5 %.

| View | Job | Likeness |
|---|---|---|
| Front | `d09ff0e7-d9c7-4cce-8257-c57f730ea33a` | 0.742 |
| ¾ (sees left cheek) | `54a00dfb-e99d-40e6-a845-b6c5764af666` | 0.734 |
| ¾ (sees right cheek) | `a576d961-67b2-4137-ad19-18b73491ac21` | 0.722 |
| Right profile, eye open | `89a731e1-4714-4aa5-be13-084d829fdd28` | 0.640 |

**Selfie distortion, measured** (YuNet landmarks, ratio to inter-ocular distance across 6 selfies):
- eye-to-nose 0.62–0.76;
- nose-to-mouth 0.41–0.63;
- face width 1.97–2.24.

That 15–20 % spread is perspective distortion from shooting at arm's length. The most distant selfies (08, 14, 06) are the most faithful, so they were the primary references. In the canon set the dome is rounder and the ears sit at their true size.

**Known deviations:**
- The eyes render brown-hazel instead of grey-green.
- The skin has a slight CGI smoothness.
- Fix both in prompts with "grey-green eyes, unretouched photographic skin".
