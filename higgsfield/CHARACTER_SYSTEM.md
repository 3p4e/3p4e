# Character system: one authentic base, many characters

Every character played by Blagoj Nikolov is built in layers. The **neutral base** never changes. Race, marks and costume are added per character, **in text only**.

```
BASE (Blagoj-Base)  →  + RACE / MARKS layer  →  + COSTUME layer  →  scene
```

## Layer 0: `Blagoj-Base` = `f5e2e917-3a91-4213-a01a-ffbca43c7d4c` (2026-10-30)

Generated directly from five real selfies (08, 14, 06, 03 or 05, 11 or 02). **No generated face was used as an input**, so nothing from Azulon (ears, tattoo) can leak in.

| View | Job | Mean SFace vs 20 real photos | Front geometry vs best selfies |
|---|---|---|---|
| Front | `bc8b3c68-7399-47e4-8b3d-8fedd28fce22` | 0.594 | eye-nose −2.8 %, nose-mouth **+5.3 %**, mouth −7.1 % (**OK**, all within 10 %) |
| ¾ (right cheek) | `41dc17de-1fec-439b-9a1c-265e38f24cd9` | 0.635 | n/a (turned head) |
| ¾ (left cheek) | `02c5bfbf-8477-4522-9b55-6572cf6cacaf` | 0.626 | n/a |
| Right profile | `55fac7e0-951d-48ed-b061-703b5c35ad31` | 0.610 | n/a |

This is the **first identity whose frontal proportions match the real selfies.** Azulon-Master's nose-to-mouth was +24 %.

**Base look:** hairless shaved head, clean-shaven, natural eyebrows, smooth chin, light grey-green eyes, human ears, no earrings, no tattoos, 85 mm lens-corrected proportions, real skin. Charcoal t-shirt, mid-grey studio.

**Visual residuals:** the base looks slightly younger and smoother than the selfies, and the eyes lean blue. Correct these per scene with "real age, unretouched skin, grey-green eyes".

## Base prompt block (paste into every character prompt)

> the man from <<<f5e2e917-3a91-4213-a01a-ffbca43c7d4c>>>, unmistakably the same real person, same face, eyes, nose, mouth, jaw and age; light grey-green eyes; real unretouched skin with pores

Then add the character's hair state, race layer and costume.

## Layer 1: race / marks (examples)

| Character | Layer | Element |
|---|---|---|
| Azulon (Forgotten Realms) | long swept-back high-elf ears + low-contrast Selûne tattoo + super mode | `Azulon-Master` `5b059323…` (see [AZULON_CANON.md](AZULON_CANON.md)) |
| Human hero (Norse, Slavic, Vedic, Egyptian…) | none. Optionally a beard or moustache per role ("short ginger-brown moustache and stubble"), or the original Soul `b3ba42a8…`, which already carries the moustache | `Blagoj-Base` + text |

## Rules (learned the hard way)
1. **Never pass a generated face as a reference image for a feature** (ears, tattoo, costume). The edit model copies the face as well. Describe features in words.
2. **Edit from the highest-likeness base, in as few passes as possible.** Stacked corrections accumulate drift.
3. **Check every new hero still** with `python3 tools/authenticity_check.py face_dataset <dir> --geometry-refs <selfies 08 14 06>`. The mean must be ≥ 0.50. On frontal views, every geometry ratio must be within ±10 %.
4. **Use long set pieces** (10–25 s), with the hero small in wide shots and close-ups only as short inserts. See the critique of *The Remembering* v1 (2026-10-30).
