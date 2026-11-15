#!/usr/bin/env python3
"""Apply director look-lock corrections (2026-11-12) to the Fenrir card fill pack.

Sources (director-supplied reference screenshots, filed under media/fenrir_assets/):
  loki: INK OF CHAOS dark-ember look (kit GOLDEN LIE / FALSE SALVATION unchanged)
  hel:  OPTION 5 HALF-GOD HALF-DEAD, Twin Verdict Blades, Choose Your Half
  tyr:  OPTION 5 FINAL OATH ember-gold gear (OL face awaited; intact right hand)
Zero GPU. Authoring only.
"""
import hashlib
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path('/a0/usr/projects/vast')
ASSETS = ROOT / 'media' / 'fenrir_assets'
PACK = ROOT / 'storybook_ocr' / 'specs' / '13_GROK_CARD_FILL_PACK_P1P2.md'
DATA = ROOT / 'storybook_ocr' / 'data' / '13_fenrir_the_wolf_of_asgard_data.json'

REFS = {
    'loki': '/a0/usr/uploads/clipboard-ab184014-58b7-4c18-9dca-5ed0ea21eeb1.png',
    'hel': '/a0/usr/uploads/clipboard-7db524a6-ceaa-4b7d-aca1-75e387db97d2.png',
    'tyr': '/a0/usr/uploads/clipboard-84f30034-1a4d-4af0-ab7f-e0bddb512bd8.png',
}

LOKI_NEW = '''## 2. LOKI  (face = enrolled identity AZ - attach az_master_sheet.jpg / AZ face card)

**Attach:** template P1, template P2, az_master_sheet.jpg (face lock: keep his exact face, hair,
eyes, clean-shaven look - only the costume changes), loki_director_reference.png (approved LOOK).
**Output names:** `loki_card_p1.png`, `loki_card_p2.png`
> DIRECTOR LOOK LOCK 2026-11-12: the design in loki_director_reference.png ("INK OF CHAOS",
> sha LOKI_SHA) is the canonical Loki look - dark ember/chaos garb. The first word of the card
> title was not machine-readable; director to confirm exact loadout spelling before batch.

### P1 FIELDS
- NAME: LOKI - LOADOUT: INK OF CHAOS [director-locked; confirm first word]
- TAGLINE BOX - ROLE: GOD OF TRICKERY - FATHER OF FENRIR - TAGLINE SHORT: "Salvation is the sweetest lie."
- TURNAROUND (4 views): the AZ face on a LEAN, light build - NOT the broad paladin silhouette.
  DARK EMBER/CHAOS garb per the director reference: layered black-and-charcoal wrapped tunic and
  mantle, torn-dark edges, muted bronze trim and bindings, pale warm-ash accents, ember-warm
  highlights in the shadows. NO armor plates, NO hood over head, NO helmet, NO greatsword,
  NO holy fire.
- FACE CLOSEUP: AZ's exact face, lit from below by faint ember light.
- DETAILS & MATERIALS callouts: c1 = torn-wrap tunic layers; c2 = muted bronze bindings;
  c3 = ember glow caught in the weave; c4 = charcoal mantle drape; c5 = worn dark boots.
- MATERIAL 1-4: charcoal-black cloth - dark cracked leather - muted bronze - pale warm ash.
- LORE/NOTES: father of Fenrir, Jormungandr and Hel; loves his children and lies to everyone;
  the gentlest voice in any room is the most dangerous. Palette owned: near-black, warm dark
  brown, muted bronze, pale warm ash.
- ABILITY STRIP: 1. GILDED PROMISE 2. HOLLOW BARGAIN 3. SERPENT'S TONGUE 4. TRICKSTER'S STEP 5. FALSE SALVATION
  (kit names CONFIRMED via director title card GOLDEN LIE / FALSE SALVATION - the look re-theme
  does not touch the kit; the weapon card still carries the GOLDEN LIE dirk)

### P2 FIELDS
- PORTRAIT INSET: AZ face, 3/4, faint ember rim light.
- ABILITIES:
  1. GILDED PROMISE - an illusion double steps out in gold-green light, acts three heartbeats, dissolves
     into fool's-gold spores. ILLUSION | LOW | SELF | 6s | 25s
  2. HOLLOW BARGAIN - chains of shimmering gold light coil a target's feet. SNARE | MED | MID | 8s | 45s
  3. SERPENT'S TONGUE - whisper becomes an emerald serpent of smoke; the target sees salvation and
     walks into a trap. CHARM/DEBUFF | MED | LONG | 10s | 60s
  4. TRICKSTER'S STEP - swaps places with his illusion double (proposed). MOBILITY | NONE | MID | 1s | 30s
  5. FALSE SALVATION (ULTIMATE) - a radiant golden doorway opens like rescue; what steps through is
     swallowed by emerald dark. ULTIMATE | ULT | ZONE | 6s | 300s
- ARMOR DETAILS (dark ember outfit): 1 CHEST = torn-wrap charcoal tunic; 2 PAULDRON = none -
  ragged mantle knot on the right shoulder; 3 GAUNTLET = dark leather wraps, bronze ring bindings;
  4 BACK-CAPE = tattered charcoal mantle, ember-lit hem; 5 BOOT = worn black boots, bronze buckles.
- HERO VIEW: Loki turning toward camera out of shadow, the GOLDEN LIE dirk reversed along his
  forearm, embers drifting.
- WEAPON: THE GOLDEN LIE "THE HALF-TRUE REFLECTION" - a slender golden dirk whose blade never
  reflects the room truthfully. QUOTE: "The kindest-looking thing on the battlefield is the lie."

'''

HEL_NEW = '''## 5. HEL

**Attach:** template P1, template P2, hel_director_reference.png (approved LOOK - "OPTION 5
HALF-GOD HALF-DEAD", sha HEL_SHA).
**Output names:** `hel_card_p1.png`, `hel_card_p2.png`
> DIRECTOR LOOK LOCK 2026-11-12: OPTION 5 - HALF-GOD HALF-DEAD, weapon Twin Verdict Blades,
> signature ability "Choose Your Half". Card header and ability names must use exactly these.

### P1 FIELDS
- NAME: HEL - LOADOUT: HALF-GOD HALF-DEAD
- TAGLINE BOX - ROLE: GODDESS OF THE UNDERWORLD - DAUGHTER OF LOKI - TAGLINE SHORT: "Half alive. Half beyond. All patient."
- TURNAROUND (4 views): a quiet pale young woman, eerily calm; face split vertically in ONE clean
  division - LEFT half living (soft pale skin, ash-brown hair, gentle grey eye), RIGHT half dead
  (ash-grey skin, hollow cheek, faint dark veins, dull eye). Dark gown with muted bronze and bone
  accents per the director reference, twin blade sheaths crossed at the back, no jewelry.
- FACE CLOSEUP: the split face straight-on - the living eye warm, the dead eye empty.
- DETAILS & MATERIALS callouts: c1 = the clean vertical divide line; c2 = dead-side veins; c3 =
  crossed twin-blade sheaths at the back; c4 = muted bronze gown trim; c5 = bone-white clasp.
- MATERIAL 1-4: pale living skin - ash-grey dead skin - dark gown cloth - muted bronze and bone.
- LORE/NOTES: sent below while her brothers were thrown out; does not rage - she waits; the dead
  are not her prisoners, they are her guests. Palette owned: near-black, warm brown, bronze, pale bone.
- ABILITY STRIP: 1. CHOOSE YOUR HALF 2. VERDICT EDGE - LIVING 3. VERDICT EDGE - DEAD 4. GLOOM WARD 5. HEL'S HUSH

### P2 FIELDS
- PORTRAIT INSET: same split face, underworld gloom light.
- ABILITIES:
  1. CHOOSE YOUR HALF (CONFIRMED, director) - splits her stance: one half heals allies, the other
     withers foes; the battlefield chooses which it meets. DUAL | HIGH | ZONE | 12s | 60s
  2. VERDICT EDGE - LIVING - the living blade cuts curses and fear off allies. CLEANSE | MED | MID | 4s | 30s
  3. VERDICT EDGE - DEAD - the dead blade passes through armor to the life beneath. EXECUTE | HIGH | MELEE | 2s | 45s
  4. GLOOM WARD - a veil of cold mist that blunts all damage entering it. WARD | MED | ZONE | 12s | 60s
  5. HEL'S HUSH (ULTIMATE) - silence falls; no spell, shout, or prayer functions inside it. ULTIMATE | ULT | ZONE | 8s | 300s
- ARMOR DETAILS: 1 CHEST = dark gown bodice with bronze trim; 2 PAULDRON = none - bare divided
  shoulders; 3 GAUNTLET = none - bare divided hands; 4 BACK-CAPE = crossed sheaths for the Twin
  Verdict Blades; 5 BOOT = simple dark slippers.
- HERO VIEW: Hel descending her stone steps, a Verdict Blade in each hand, the dead parting for her.
- WEAPON: TWIN VERDICT BLADES "THE LIVING AND THE DEAD" - one pale blade that mends what it
  touches, one grey blade that ends it. QUOTE: "Choose your half."

'''

TYR_NEW = '''## 4. TYR  (face = enrolled identity OL - attach the OL character sheet when provided)

**Attach:** template P1, template P2, ol_character_sheet.png (AWAITED from director - until it
arrives, render with the written face below and re-anchor on delivery), tyr_director_reference.png
(approved LOOK - "OPTION 5 FINAL OATH", sha TYR_SHA).
**Output names:** `tyr_card_p1.png`, `tyr_card_p2.png`
> DIRECTOR LOOK LOCK 2026-11-12: OPTION 5 - FINAL OATH, fiery ember-gold oath-sworn war-gear.
> The OL face replaces the generic model face on the card; RIGHT HAND stays PRESENT and INTACT on
> both cards (pre-loss design - the sacrifice happens on camera at S39-S40).

### P1 FIELDS
- NAME: TYR - LOADOUT: FINAL OATH
- TAGLINE BOX - ROLE: GOD OF WAR - KEEPER OF OATHS - TAGLINE SHORT: "One hand for the wolf; one name for the ages."
- TURNAROUND (4 views): the OL face on an athletic upright build, sandy-blond hair tied at the nape,
  short neat blond beard, calm fearless eyes. FINAL OATH war-gear per the director reference:
  ember-gold and warm bronze armor over dark under-cloth - bright oath-fire tones against deep
  shadow, a glowing oath-core at the chest, leather-and-bronze bracers, round shield with an
  ember-lit boss on the back, an ember-lit straight sword at the hip. RIGHT HAND PRESENT AND
  INTACT IN EVERY VIEW (guard).
- FACE CLOSEUP: the OL face, level gaze, ember light from the side.
- DETAILS & MATERIALS callouts: c1 = glowing oath-core at the chest; c2 = ember-gold plate edges;
  c3 = bronze bracer bindings; c4 = ember-lit shield boss; c5 = oath-fire seams along the greaves.
- MATERIAL 1-4: ember-gold steel - warm bronze - dark oath-cloth - oath-fire light.
- LORE/NOTES: the only god brave enough to feed the wolf his own hand; keeps every oath, even the
  costly ones - especially the costly ones. Palette owned: ember gold, warm bronze, deep shadow.
- ABILITY STRIP: 1. OATHBOUND STRIKE 2. SHIELDWALL OF THE JUST 3. JUSTICE SIGIL 4. UNFLINCHING 5. THE PRICE PAID

### P2 FIELDS
- PORTRAIT INSET: the OL face, 3/4, ember-gold key light.
- ABILITIES:
  1. OATHBOUND STRIKE - a blow that lands harder the more it costs him. HOLY/PHYSICAL | HIGH | MELEE | 1s | 20s
  2. SHIELDWALL OF THE JUST - plants shield; allies behind him cannot be moved. GUARD | MED | FRONT | 12s | 45s
  3. JUSTICE SIGIL - chest oath-core flares; taunts foes to face him. TAUNT | LOW | AURA | 10s | 60s
  4. UNFLINCHING - pain cannot stagger him for a time. SELF-BUFF | MED | SELF | 15s | 90s
  5. THE PRICE PAID (ULTIMATE) - channels the sacrifice: a sun-bright strike born of loss. ULTIMATE | ULT | MELEE | 2s | 300s
- ARMOR DETAILS: 1 CHEST = ember-gold plate with glowing oath-core; 2 PAULDRON = bronze oath-
  plates; 3 GAUNTLET = bronze-bound bracers (RIGHT GAUNTLET COMPLETE - intact hand); 4 BACK-CAPE =
  round ember-lit shield on the back; 5 BOOT = ember-seamed war boots.
- HERO VIEW: TYR striding forward, shield up, ember-lit sword low - both hands whole.
- WEAPON: OATHBRAND "THE FINAL OATH" - an ember-lit straight sword that brightens with every
  promise kept. QUOTE: "An oath kept is a debt the world owes you."

'''


def main():
    ASSETS.mkdir(exist_ok=True)
    sha = {}
    for key, src in REFS.items():
        dst = ASSETS / f'{key}_director_reference.png'
        shutil.copy(src, dst)
        sha[key] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
        print(f'{key}: filed {dst.name} sha {sha[key][:16]}')

    t = PACK.read_text(encoding='utf-8')

    blocks = [
        ('## 2. LOKI', '## 3. FENRIR', LOKI_NEW, 'loki'),
        ('## 4. TÝR', '## 5. HEL', TYR_NEW, 'tyr'),
        ('## 5. HEL', '## 6. JÖRMUNGANDR', HEL_NEW, 'hel'),
    ]
    for start, end, new, key in blocks:
        pat = re.compile(re.escape(start) + r'.*?(?=^' + re.escape(end) + r')', re.S | re.M)
        m = pat.search(t)
        assert m, f'section not found: {start}'
        body = new.replace(key.upper() + '_SHA', sha[key][:16])
        t = t[:m.start()] + body + t[m.end():]
        print(f'{start} section rewritten')

    receipt = (
        '## DIRECTOR LOOK REFERENCES (filed 2026-11-12, media/fenrir_assets/)\n'
        f'- loki_director_reference.png  sha {sha["loki"][:16]} - INK OF CHAOS dark-ember look '
        '(first word of title unread by OCR; confirm spelling)\n'
        f'- hel_director_reference.png   sha {sha["hel"][:16]} - OPTION 5 HALF-GOD HALF-DEAD, '
        'Twin Verdict Blades, Choose Your Half\n'
        f'- tyr_director_reference.png   sha {sha["tyr"][:16]} - OPTION 5 FINAL OATH ember-gold gear '
        '(face on ref is a generic model; OL replaces at card time)\n\n'
    )
    anchor = '================================================================\n## 1. ODIN'
    assert anchor in t, 'pack anchor missing'
    t = t.replace(anchor, receipt + anchor, 1)

    PACK.write_text(t, encoding='utf-8')
    print('pack header receipt added')

    d = json.load(open(DATA, encoding='utf-8'))
    notes = {
        'loki': f'director look lock 2026-11-12: INK OF CHAOS dark-ember look (media/fenrir_assets/loki_director_reference.png, sha {sha["loki"][:12]}); kit GOLDEN LIE/FALSE SALVATION unchanged',
        'hel': f'director look lock 2026-11-12: OPTION 5 HALF-GOD HALF-DEAD, Twin Verdict Blades, Choose Your Half (media/fenrir_assets/hel_director_reference.png, sha {sha["hel"][:12]})',
        'tyr': f'director look lock 2026-11-12: OPTION 5 FINAL OATH ember-gold gear (media/fenrir_assets/tyr_director_reference.png, sha {sha["tyr"][:12]}); OL face awaited; right hand intact on cards',
    }
    for key, note in notes.items():
        d['spec']['card_canon']['characters'][key]['director_reference'] = note
    json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('data JSON: card_canon director_reference notes for loki/hel/tyr')
    print('DONE')


if __name__ == '__main__':
    main()
