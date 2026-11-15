import re

GRIM_GRADE="Photoreal grimdark Greek horror cinematic grade, Diablo 2 / Dark Souls aesthetic, 35mm anamorphic, real skin and scale texture, visible film grain, low-key dramatic horror lighting"
GRIM_NEG_ADD=", bright cheerful daylight, saturated cheerful colors, clean sterile look, glossy beauty-shot lighting, whimsical, cute"
OLD_GRADE="Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting"

# ---------- Pack 1: design-look, all 5 active as grim iterations ----------
p1='/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_DESIGN_LOOK_PROMPTS.md'
s=open(p1).read()

# reactivate prompts 1-2 as grimdark iterations
s=s.replace(
"> **STATUS: DIRECTOR-PROVIDED - do not generate.** The director supplies this sheet (AZ face baked in); prompt kept as design record.\n**Save as:** `look_01_perseus.png` (canonical slot, `media/perseus_assets/`)\n**Attach (only if ever regenerating):**",
"> **STATUS: ACTIVE - GRIMDARK ITERATION.** Generate this dark iteration (AZ face attached). The DIRECTOR-PROVIDED sheet stays the locked canon at `media/perseus_assets/look_01_perseus.png`; this grim iteration is exploratory reference and becomes canon only if you adopt it.\n**Save as:** `look_01_perseus_GRIM.png`\n**Attach:**")
s=s.replace(
"> **STATUS: DIRECTOR-PROVIDED - do not generate.** The director supplies this sheet (feminized DD face baked in); prompt kept as design record.\n**Save as:** `look_02_medusa.png` (canonical slot, `media/perseus_assets/`)\n**Attach (only if ever regenerating):**",
"> **STATUS: ACTIVE - GRIMDARK ITERATION.** Generate this dark iteration (DD face attached, feminized by the prompt). The DIRECTOR-PROVIDED sheet stays the locked canon at `media/perseus_assets/look_02_medusa.png`; this grim iteration is exploratory reference and becomes canon only if you adopt it.\n**Save as:** `look_02_medusa_GRIM.png`\n**Attach:**")

# grim grade swap in all prompts
s=s.replace(OLD_GRADE, GRIM_GRADE.replace('skin and scale texture','skin and fur texture'))
# grim negative add (the look pack used its own negatives; extend them)
s=s.replace(
"Negative: cartoon, anime, illustration, 3d render, plastic skin, text, watermark, logo, extra limbs, gore, blood, beard on Perseus or Hermes, snakes on Athena's head, human legs on Medusa, hair instead of snakes on Medusa, cheerful bright daylight look",
"Negative: cartoon, anime, illustration, 3d render, plastic skin, text, watermark, logo, extra limbs, gore, blood, beard on Perseus or Hermes, snakes on Athena's head, human legs on Medusa, hair instead of snakes on Medusa, cheerful bright daylight look"+GRIM_NEG_ADD)

# grim environments inside the look prompts
s=s.replace("standing on a rocky Aegean shore at dawn.","standing on a rocky Aegean shore under a storm-black sky, lightning far out at sea.")
s=s.replace("coiling on dark cave stone;","coiling on weeping cave stone in a cavern of stalactite fangs; cold mist curling around her.")
s=s.replace("standing on a marble temple floor.","standing on a cracked marble temple floor in near-darkness, one shaft of cold light.")
s=s.replace("light running stance on a cloud-lit mountain path.","light running stance on a fog-drowned mountain path, storm-light barely breaking through.")
s=s.replace("vulnerable but dignified, no injury.","vulnerable but dignified, no injury; storm-split silver light, waves like black glass.")
s=s.replace("dramatic cinematic lighting","low-key dramatic horror lighting")

# header revision note
s=s.replace(
"> REVISED 2026-11-12 (director): the **Perseus and Medusa character sheets are DIRECTOR-PROVIDED** (AZ / feminized-DD faces already baked in) - canon by delivery, no Grok generation needed. Prompts 1-2 are kept as the design record only. Prompts 3-5 (AI-default cast) remain for Grok generation unless the director also supplies those sheets. File provided sheets under `media/perseus_assets/` using the canonical names below.",
"> REVISED 2026-11-12 (director): Perseus/Medusa DIRECTOR-PROVIDED sheets stay the locked canon (`media/perseus_assets/`).\n> GRIMDARK PIVOT 2026-11-12: ALL 5 prompts are ACTIVE as **grimdark-horror iterations** — dark, grim, weird-art aesthetics (storm-gloom, fog, ash, low-key light). Perseus/Medusa grim iterations save as `*_GRIM.png` and are exploratory (canon only if the director adopts them). AI-default cast grim looks save as their canonical names.")
open(p1,'w').write(s)
print('pack1: all 5 active grim; GRIM markers:', s.count('GRIMDARK ITERATION'))

# ---------- 5-in-1 lineup: grim rewrite ----------
p5='/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_FIVE_IN_ONE_LOOKS.md'
s=open(p5).read()
s=s.replace("Cinematic photoreal character design lineup sheet, Diablo 2 / World of Warcraft / StarCraft cinematic quality.",
"Cinematic photoreal grimdark Greek horror character design lineup sheet, Diablo 2 / Dark Souls aesthetic.")
s=s.replace("standing heroically on a rocky Aegean shore at dawn.","standing heroically on a rocky Aegean shore under a storm-black sky, lightning far out at sea.")
s=s.replace("coiling on dark cave stone; terrifying but not gory — no blood, no wounds.","coiling on weeping cave stone in a cavern of stalactite fangs, cold mist curling around her; terrifying but not gory — no blood, no wounds.")
s=s.replace("standing on a marble temple floor.","standing on a cracked marble temple floor in near-darkness, one shaft of cold light.")
s=s.replace("light running stance on a cloud-lit mountain path.","light running stance on a fog-drowned mountain path, storm-light barely breaking through.")
s=s.replace("waves calming behind her; vulnerable but dignified, no injury.","waves like black glass behind her under storm-split silver light; vulnerable but dignified, no injury.")
s=s.replace("dramatic cinematic lighting","low-key dramatic horror lighting")
s=s.replace("whimsical, cute","",1)  # safety if duplicated
s=s.replace(
"Negative: cartoon, anime, illustration, low poly, 3d render, plastic skin, text, watermark, logo, extra fingers, deformed hands, merged subjects, overlapping panels, duplicate faces, shared motifs between panels, beard on Perseus or Hermes, snakes on Athena's head, human legs on Medusa, hair instead of snakes on Medusa, gore, blood, decapitation, modern clothing, firearm",
"Negative: cartoon, anime, illustration, low poly, 3d render, plastic skin, text, watermark, logo, extra fingers, deformed hands, merged subjects, overlapping panels, duplicate faces, shared motifs between panels, beard on Perseus or Hermes, snakes on Athena's head, human legs on Medusa, hair instead of snakes on Medusa, gore, blood, decapitation, modern clothing, firearm, bright cheerful daylight, saturated cheerful colors, clean sterile look, glossy beauty-shot lighting, whimsical, cute")
s=s.replace("> OPTIONAL consolidated sheet",
"> GRIMDARK PIVOT 2026-11-12: consolidated 5-panel grimdark-horror lineup — dark, grim, weird-art iterations of all five characters. Perseus/Medusa panels attach the AZ/DD face cards; the DIRECTOR-PROVIDED canon sheets remain the locked canon, this sheet is the dark-iteration overview.\n> OPTIONAL consolidated sheet")
open(p5,'w').write(s)
print('5-in-1: grim applied; grim markers:', s.count('grimdark'))

# ---------- card pack: grim grade + environments ----------
p2='/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_CARD_FILL_PACK_P1P2.md'
s=open(p2).read()
s=s.replace("Diablo 2 cinematic grade, photoreal, 35mm anamorphic, dramatic cinematic lighting","grimdark Greek horror grade, Diablo 2 / Dark Souls aesthetic, photoreal, 35mm anamorphic, low-key dramatic horror lighting")
s=s.replace(
"Negative: cartoon, anime, illustration, 3d render, plastic skin, text, watermark, logo, extra limbs, extra fingers, deformed hands, gore, blood",
"Negative: cartoon, anime, illustration, 3d render, plastic skin, text, watermark, logo, extra limbs, extra fingers, deformed hands, gore, blood, bright cheerful daylight, saturated cheerful colors, clean sterile look, glossy beauty-shot lighting")
s=s.replace("> Perseus/Medusa reference = DIRECTOR-PROVIDED canon sheets",
"> GRIMDARK PIVOT 2026-11-12: all card art in the grimdark-horror register (storm-gloom, fog, ash, low-key light).\n> Perseus/Medusa reference = DIRECTOR-PROVIDED canon sheets")
open(p2,'w').write(s)
print('card pack: grim applied')

# ---------- SPEC: grim canon section + style anchor (idempotent guard) ----------
ps='/a0/usr/projects/vast/storybook_ocr/specs/23_perseus_defeats_medusa_SPEC.md'
s=open(ps).read()
if 'GRIMDARK AEGEAN HORROR' not in s:
    s=s.replace("| style anchor | Diablo 2 cinematic · World of Warcraft cinematic · StarCraft cinematic ·",
                "| style anchor | Diablo 2 cinematic · World of Warcraft cinematic · StarCraft cinematic · grimdark Greek horror (2026-11-12 pivot) ·")
    # safer: append canon section after the negative-prompt code fence
    marker="## 2. Cast"
    canon=("\n---\n\n## 1b. GRIMDARK AEGEAN HORROR - aesthetic canon (2026-11-12 pivot)\n\n"
      "The story is retold in a dark horror register - grim, weird-art, oppressive. NOT gore: dread.\n"
      "- Palette: desaturated cold greys, bone, blackened bronze, bruised storm blues; one sickly accent per scene.\n"
      "- Light: low-key, motivated sources only - storm-gloom, guttering torches, sickly cave reflections, storm-split silver. No warm cheerful daylight.\n"
      "- Weather/texture: creeping fog, wind-stunted thorn scrub, salt-stained stone, weeping cave walls, carrion birds, ash-dust falling like snow.\n"
      "- Weird-art touches: petrified warriors half-merged with living rock, stalactites like fangs, a sea that behaves like a breathing thing, statues that seem to watch.\n"
      "- Per act: Act I decaying citadel under storm-gloom - Act II weeping cavern of the petrified - Act III storm-black sea and drowned-ruin coast.\n"
      "- Not gore: horror is atmospheric; blood/wounds/decapitation stay in the negative prompt; Medusa's defeat reads as stone-stillness, not butchery.\n\n---\n\n")
    s=s.replace(marker, canon+marker, 1)
    open(ps,'w').write(s)
    print('SPEC: grim canon section added')
else:
    print('SPEC: grim canon already present')

# verify pack1 per-prompt state
s1=open(p1).read()
print('pack1 prompts:', len(re.findall(r'## PROMPT \d of 5', s1)), '| GRIM saves:', s1.count('_GRIM.png'), '| old grade left:', s1.count('World of Warcraft'))
