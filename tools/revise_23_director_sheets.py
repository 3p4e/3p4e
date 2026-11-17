import os

# --- Pack 3: keyframe canon lines -> director-provided canon sheets ---
p3='/a0/usr/projects/vast/storybook_ocr/specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
s=open(p3).read()
s=s.replace(
 "Perseus - BRONZE VOW loadout per approved look card look_01_perseus.png (face = AZ, bronze hoplite, mirrored shield, harpe)",
 "Perseus - BRONZE VOW per the DIRECTOR-PROVIDED canon character sheet look_01_perseus.png (AZ face baked in)")
s=s.replace(
 "Medusa - GORGON CURSE loadout per approved look card look_02_medusa.png (face = feminized DD, snake-hair, golden eyes, snake-tail, no gore)",
 "Medusa - GORGON CURSE per the DIRECTOR-PROVIDED canon character sheet look_02_medusa.png (feminized DD face baked in)")
anchor="> Generator: Grok (image). Casting CONFIRMED 2026-11-12: Perseus = AZ (enrolled face), Medusa = feminized DD (enrolled face), all others AI-default."
s=s.replace(anchor, anchor+"\n> Character reference: Perseus/Medusa = DIRECTOR-PROVIDED canon sheets (faces baked in, canon by delivery); AI-default cast = look cards from the design-look run.")
open(p3,'w').write(s)

# --- Pack 1: design-look -> prompts 1-2 director-provided, 3-5 stay for Grok ---
p1='/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_DESIGN_LOOK_PROMPTS.md'
s=open(p1).read()
a1="> Casting decision 2026-11-12: **Perseus = AZ** (enrolled), **Medusa = feminized DD face**, all others AI-default."
s=s.replace(a1, a1+"\n> REVISED 2026-11-12 (director): the **Perseus and Medusa character sheets are DIRECTOR-PROVIDED** (AZ / feminized-DD faces already baked in) - canon by delivery, no Grok generation needed. Prompts 1-2 are kept as the design record only. Prompts 3-5 (AI-default cast) remain for Grok generation unless the director also supplies those sheets. File provided sheets under `media/perseus_assets/` using the canonical names below.")
s=s.replace(
 "| look_01_perseus | `faces/az_cards_final/MVIMG_20261105_201334_1024.jpg` (AZ master face card) | Perseus face-lock = enrolled AZ identity |",
 "| look_01_perseus | **DIRECTOR-PROVIDED** - file at `media/perseus_assets/look_01_perseus.png` | Perseus canon sheet, AZ face baked in |")
s=s.replace(
 "| look_02_medusa | `faces/dd_cards_final/DD_viber_image_2026-11-04_15-48-05-999_1024.jpg` (DD master face card) | Medusa face = DD, feminized by prompt wording |",
 "| look_02_medusa | **DIRECTOR-PROVIDED** - file at `media/perseus_assets/look_02_medusa.png` | Medusa canon sheet, feminized DD face baked in |")
s=s.replace(
 "## PROMPT 1 of 5 - PERSEUS\n**Save as:** `look_01_perseus.png`\n**Attach:** AZ master face card (`faces/az_cards_final/MVIMG_20261105_201334_1024.jpg`)",
 "## PROMPT 1 of 5 - PERSEUS\n> **STATUS: DIRECTOR-PROVIDED - do not generate.** The director supplies this sheet (AZ face baked in); prompt kept as design record.\n**Save as:** `look_01_perseus.png` (canonical slot, `media/perseus_assets/`)\n**Attach (only if ever regenerating):** AZ master face card (`faces/az_cards_final/MVIMG_20261105_201334_1024.jpg`)")
s=s.replace(
 "## PROMPT 2 of 5 - MEDUSA\n**Save as:** `look_02_medusa.png`\n**Attach:** DD master face card (`faces/dd_cards_final/DD_viber_image_2026-11-04_15-48-05-999_1024.jpg`)",
 "## PROMPT 2 of 5 - MEDUSA\n> **STATUS: DIRECTOR-PROVIDED - do not generate.** The director supplies this sheet (feminized DD face baked in); prompt kept as design record.\n**Save as:** `look_02_medusa.png` (canonical slot, `media/perseus_assets/`)\n**Attach (only if ever regenerating):** DD master face card (`faces/dd_cards_final/DD_viber_image_2026-11-04_15-48-05-999_1024.jpg`)")
s=s.replace("1. Send me the 5 files (or a Drive link). I read each sheet **before flagging** anything.",
 "1. Director provides look_01_perseus.png + look_02_medusa.png (canon by delivery). I run prompts 3-5 for the AI-default cast (Athena / Hermes / support plate) unless the director supplies those sheets too.")
s=s.replace("2. I verify Perseus's face matches the AZ reference and Medusa's face matches the feminized DD reference (SFace ≥ 0.50 vs the respective centroids).",
 "2. I verify the provided Perseus sheet against the AZ centroid and the Medusa sheet against the feminized-DD read (SFace ≥ 0.50), then hash-lock both under the canonical names.")
open(p1,'w').write(s)

# --- Pack 2: card pack -> attach director-provided sheets ---
p2='/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_CARD_FILL_PACK_P1P2.md'
s=open(p2).read()
a2="> Casting: Perseus = AZ (enrolled), Medusa = feminized DD (enrolled), all others AI-default."
s=s.replace(a2, a2+"\n> Perseus/Medusa reference = DIRECTOR-PROVIDED canon sheets (faces baked in), filed at `media/perseus_assets/look_01_perseus.png` / `look_02_medusa.png`.")
s=s.replace("**Attach:** template P1, template P2, `faces/az_cards_final/MVIMG_20261105_201334_1024.jpg`",
 "**Attach:** template P1, template P2, `media/perseus_assets/look_01_perseus.png` (director-provided canon sheet - AZ face baked in)")
s=s.replace("**Attach:** template P1, template P2, `faces/dd_cards_final/DD_viber_image_2026-11-04_15-48-05-999_1024.jpg`",
 "**Attach:** template P1, template P2, `media/perseus_assets/look_02_medusa.png` (director-provided canon sheet - feminized DD face baked in)")
s=s.replace("## 1. PERSEUS  (face = enrolled identity AZ - attach az_master_sheet.jpg / AZ face card)",
 "## 1. PERSEUS  (face = DIRECTOR-PROVIDED canon sheet - AZ baked in)")
s=s.replace("## 2. MEDUSA  (face = feminized DD - attach dd_master_sheet.jpg / DD face card)",
 "## 2. MEDUSA  (face = DIRECTOR-PROVIDED canon sheet - feminized DD baked in)")
open(p2,'w').write(s)

# --- create the canonical drop location ---
d='/a0/usr/projects/vast/media/perseus_assets'
os.makedirs(d, exist_ok=True)
open(d+'/README.txt','w').write(
 "Canonical character-sheet slots for story 23 (Perseus & Medusa).\n"
 "DIRECTOR-PROVIDED sheets (canon by delivery):\n"
 "  look_01_perseus.png  - Perseus, AZ face baked in\n"
 "  look_02_medusa.png   - Medusa, feminized DD face baked in\n"
 "GENERATED (design-look pack prompts 3-5):\n"
 "  look_03_athena.png / look_04_hermes.png / look_05_support_cast.png\n"
 "Cards (P1/P2) built per storybook_ocr/specs/23_GROK_CARD_FILL_PACK_P1P2.md.\n")

print('done')
for pp in (p1,p2,p3):
    t=open(pp).read()
    print(pp.split('/')[-1],
          '| director-provided:', t.upper().count('DIRECTOR-PROVIDED'),
          '| media/perseus_assets refs:', t.count('media/perseus_assets'))
