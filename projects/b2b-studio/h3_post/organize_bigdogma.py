#!/usr/bin/env python3
"""Run on the owner's computer. Builds ~/Videos/BIG_DOGMA arranged BY COMPANY, with the LTX and the H3 version of
every film side by side, plus offer PDF, posters, outreach text and the private page link per company.

Inputs (defaults; pass other paths as arguments):
  1) the unzipped LTX package:   ~/Videos/BIG_DOGMA_LTX              (from BIG_DOGMA_LTX.zip)
  2) the downloaded H3 parts:    ~/Videos/H3_Assets/BIG_DOGMA_H3     (BIG_DOGMA_H3_part1..4)
  The 12 films finished on the Japan box are found by name anywhere under ~/Videos.
Files are hard-linked (no extra disk space; originals untouched). Safe to run again."""
import os, sys, re, shutil, glob

HOME = os.path.expanduser("~")
LTX = sys.argv[1] if len(sys.argv) > 1 else f"{HOME}/Videos/BIG_DOGMA_LTX"
H3 = sys.argv[2] if len(sys.argv) > 2 else f"{HOME}/Videos/H3_Assets/BIG_DOGMA_H3"
OUT = f"{HOME}/Videos/BIG_DOGMA"

COMPANIES = {
    "01_Zito_Marketi_MK": ("01_zito_marketi_MK", ["zito_commercial", "zito_opening_film"]),
    "02_Alkaloid_MK": ("02_alkaloid_MK", ["alkaloid_commercial", "alkaloid_employer_film"]),
    "03_Replek_MK": ("03_replek_MK", ["replek_commercial", "replek_export_film"]),
    "04_Vincinni_MK": ("04_vincinni_MK", ["vincinni_family_ad", "vincinni_factory_ad"]),
    "05_Foton_MK": ("05_foton_MK", ["foton_tunland_v9_specs", "foton_showreel_v2"]),
    "06_Beograd_na_vodi_RS": ("06_beograd_na_vodi_RS", ["bw_commercial", "bw_riverside_film"]),
    "07_Millennium_Team_RS": ("07_millennium_team_RS", ["millennium_commercial", "millennium_capability_film"]),
    "08_Nelt_RS": ("08_nelt_RS", ["nelt_commercial", "nelt_logistics_film"]),
    "09_Gener2_AL": ("09_gener2_AL", ["gener2_commercial", "gener2_builder_film"]),
    "10_Concord_AL": ("10_concord_AL", ["concord_commercial", "concord_offplan_film"]),
    "11_Viva_Fresh_XK": ("11_viva_fresh_XK", ["viva_commercial", "viva_expansion_film"]),
    "12_SPEEEX_XK": ("12_speeex_XK", ["speeex_commercial", "speeex_recruitment_film"]),
}
FILM_GROUP = {f: g for g, (_, fs) in COMPANIES.items() for f in fs}
def group_of(fid):
    if fid in FILM_GROUP: return FILM_GROUP[fid]
    if fid.startswith("sector_"): return "13_Sector_demos"
    if fid.startswith("timelapse_"): return "14_Timelapses"
    if "showreel" in fid: return "15_Showreels"
    return None
FIDS = sorted(set(list(FILM_GROUP) + [os.path.basename(p)[:-4] for p in glob.glob(f"{LTX}/01_films_16x9/*.mp4")]), key=len, reverse=True)
def fid_of(name):
    base = re.sub(r"(_H3)?(_pitch)?(_9x16|_1x1|_4x5)?(_poster|_teaser6s)?\.(mp4|gif|jpg|srt)$", "", name)
    base = re.sub(r"(_H3)?\.(mk|sr|sq|en)$", "", base)
    for f in FIDS:
        if base == f: return f
    return None

n = {"linked": 0, "skipped": 0}
def link(src, dst_dir, name=None):
    os.makedirs(dst_dir, exist_ok=True); dst = os.path.join(dst_dir, name or os.path.basename(src))
    if os.path.exists(dst): n["skipped"] += 1; return
    try: os.link(src, dst)
    except OSError: shutil.copy2(src, dst)
    n["linked"] += 1

# ---- LTX: films in every format, subtitles, posters
FMT = {"01_films_16x9": "", "02_films_9x16": "", "03_pitch_16x9": "", "04_pitch_9x16": "", "05_feed_1x1": "", "06_feed_4x5": ""}
if os.path.isdir(LTX):
    for d in FMT:
        for p in glob.glob(f"{LTX}/{d}/*.mp4"):
            fid = fid_of(os.path.basename(p)); g = group_of(fid) if fid else None
            if g: link(p, f"{OUT}/{g}/LTX")
    for p in glob.glob(f"{LTX}/07_subtitles/*.srt"):
        fid = fid_of(os.path.basename(p)); g = group_of(fid) if fid else None
        if g: link(p, f"{OUT}/{g}/LTX/subtitles")
    for p in glob.glob(f"{LTX}/08_posters_teasers/*"):
        fid = fid_of(os.path.basename(p)); g = group_of(fid) if fid else None
        if g: link(p, f"{OUT}/{g}/posters")
    links = {}
    if os.path.exists(f"{LTX}/PITCH_PAGE_LINKS.txt"):
        for line in open(f"{LTX}/PITCH_PAGE_LINKS.txt"):
            if line.strip(): k, v = line.split(None, 1); links[k] = v.strip()
    for g, (cid, _) in COMPANIES.items():
        for p in glob.glob(f"{LTX}/09_offer_pdfs/{cid}*.pdf"): link(p, f"{OUT}/{g}", "offer.pdf")
        p = f"{LTX}/12_outreach_private/{cid}.md"
        if os.path.exists(p): link(p, f"{OUT}/{g}", "outreach.md")
        if cid in links:
            open(f"{OUT}/{g}/private_page_link.txt", "w").write(links[cid] + "\nSend this link only to this company.\n")
    st = f"{OUT}/16_Studio"
    for sub, dst in (("10_how_its_made", "how_its_made"), ("11_brand", "brand"), ("13_launch_kit", "launch_kit")):
        for p in glob.glob(f"{LTX}/{sub}/**/*", recursive=True):
            if os.path.isfile(p): link(p, os.path.join(st, dst, os.path.relpath(os.path.dirname(p), f"{LTX}/{sub}")))
    for f in ("PITCH_PAGE_LINKS.txt", "DELIVERY_AND_LICENCE.md"):
        if os.path.exists(f"{LTX}/{f}"): link(f"{LTX}/{f}", OUT)
    for f in ("outreach_tracker.xlsx", "outreach_tracker.csv"):
        if os.path.exists(f"{LTX}/12_outreach_private/{f}"): link(f"{LTX}/12_outreach_private/{f}", OUT)
else:
    print("LTX package not found at", LTX, "- unzip BIG_DOGMA_LTX.zip into ~/Videos first; H3 is arranged anyway")

# ---- H3: films in every format, subtitles, Foton action, raw clips
H3SUB = ("films_16x9", "films_9x16", "pitch_16x9", "pitch_9x16", "feed_1x1", "feed_4x5")
for part in sorted(glob.glob(f"{H3}/BIG_DOGMA_H3_part*")):
    for sub in H3SUB:
        for p in glob.glob(f"{part}/{sub}/*.mp4"):
            fid = fid_of(os.path.basename(p)); g = group_of(fid) if fid else None
            if g: link(p, f"{OUT}/{g}/H3")
    for p in glob.glob(f"{part}/subtitles/*.srt"):
        fid = fid_of(os.path.basename(p)); g = group_of(fid) if fid else None
        if g: link(p, f"{OUT}/{g}/H3/subtitles")
    for p in glob.glob(f"{part}/foton_action/*.mp4"): link(p, f"{OUT}/17_Foton_FALCON_action_H3")
    for p in glob.glob(f"{part}/raw_clips_foton_action/*.mp4"): link(p, f"{OUT}/17_Foton_FALCON_action_H3/raw_clips")
    for p in glob.glob(f"{part}/raw_clips/*.mp4"): link(p, f"{OUT}/18_H3_raw_clips")
for fid in FILM_GROUP.keys() | {"timelapse_construction", "timelapse_apartment_staging", "showreel_macedonian_industry"}:
    for v in ("", "_9x16"):
        name = f"{fid}_H3{v}.mp4"; g = group_of(fid)
        if os.path.exists(f"{OUT}/{g}/H3/{name}"): continue
        hits = [p for p in glob.glob(f"{HOME}/Videos/**/{name}", recursive=True) if not p.startswith(OUT)]
        if hits: link(hits[0], f"{OUT}/{g}/H3")

open(f"{OUT}/README.txt", "w").write("""BIG DOGMA - all films, both versions, arranged by company

Each company folder (01-12) holds:
  LTX/   the public-safe version of both films: 16:9, 9:16, pitch 16:9 + 9:16, 1:1, 4:5, and subtitles/ (mk sr sq en)
  H3/    the MiniMax H3 version of the same films in the same formats, and subtitles/
  posters/  poster, 6 s GIF and teaser per film (LTX)
  offer.pdf, outreach.md (ready to send, with the real link), private_page_link.txt
13_Sector_demos, 14_Timelapses, 15_Showreels: same LTX/ + H3/ split.
16_Studio: brand files, animated logo, how-it's-made explainers, launch kit (showreel, reels, social images, captions).
17_Foton_FALCON_action_H3: 30 s film, 15 s reel, 6 s bumpers (H3 only) + raw clips.  18_H3_raw_clips: H3 source clips.

H3 RULES (MiniMax H3 licence): show H3 files only in person, outside the EU, UK, USA and South Korea. Never upload,
post, email or link them, never put them on Google Drive or any cloud, never let an AI assistant open them.
For anything online, email or the pitch pages, use LTX only. Each company gets only its own link.
""")
print(f"done: {n['linked']} files linked, {n['skipped']} already there -> {OUT}")
for g in sorted(os.listdir(OUT)):
    p = f"{OUT}/{g}"
    if os.path.isdir(p):
        c = lambda s: len([f for f in glob.glob(f"{p}/{s}/*") if os.path.isfile(f)])
        print(f"{g:32s} LTX {c('LTX'):3d}  H3 {c('H3'):3d}  other {len([f for f in glob.glob(p + '/**/*', recursive=True) if os.path.isfile(f)]) - c('LTX') - c('H3')}")
