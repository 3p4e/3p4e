# ON KVM4: build the tidy LTX package from the uploaded pitch-materials zip + the plain film folders, zip it (stored).
import os, sys, shutil, zipfile
DL = sys.argv[1]; P = "/opt/bigdogma_pkg"; T = f"{P}/tmp"; ST = f"{P}/stage"; OUT = f"{P}/BIG_DOGMA_LTX"
shutil.rmtree(T, ignore_errors=True); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(T); os.makedirs(OUT)
zipfile.ZipFile(f"{DL}/BIG_DOGMA_PITCH_MATERIALS_LTX.zip").extractall(T); M = f"{T}/BIG_DOGMA_PITCH_MATERIALS_LTX"
def mv(src, dst):
    if os.path.exists(src): shutil.move(src, f"{OUT}/{dst}")
    else: print("MISSING", src)
mv(f"{ST}/final_music", "01_films_16x9"); mv(f"{ST}/final_music_9x16", "02_films_9x16")
mv(f"{M}/1_pitch_16x9", "03_pitch_16x9"); mv(f"{M}/2_pitch_9x16", "04_pitch_9x16")
mv(f"{ST}/final_1x1", "05_feed_1x1"); mv(f"{ST}/final_4x5", "06_feed_4x5"); mv(f"{M}/6_subtitles", "07_subtitles")
mv(f"{M}/3_posters_teasers", "08_posters_teasers"); mv(f"{M}/4_offer_pdfs", "09_offer_pdfs"); mv(f"{M}/5_how_its_made", "10_how_its_made")
os.makedirs(f"{OUT}/11_brand"); mv(f"{M}/brand", "11_brand/brand_files"); mv(f"{M}/gfx", "11_brand/graphics"); mv(f"{M}/logo_animation", "11_brand/logo_animation")
mv(f"{M}/outreach_private", "12_outreach_private")
os.makedirs(f"{OUT}/13_launch_kit")
for sub in ("launch_video", "launch_static"):
    for f in os.listdir(f"/opt/bigdogma_backup/{sub}"): shutil.copy(f"/opt/bigdogma_backup/{sub}/{f}", f"{OUT}/13_launch_kit/{f}")
for f in ("PITCH_PAGE_LINKS.txt", "DELIVERY_AND_LICENCE.md"): mv(f"{M}/{f}", f)
open(f"{OUT}/README.txt", "w").write("""BIG DOGMA - LTX version (public-safe, AI-generated; client concepts are not for publication without written approval)

Same layout as the H3 set on the owner's computer (BIG_DOGMA/H3), folder for folder.
01_films_16x9      45 films, 16:9, music + local-language voice-over
02_films_9x16      the same 45 films, vertical
03_pitch_16x9      pitch versions (BIG DOGMA intro, concept watermark, email outro)
04_pitch_9x16      pitch versions, vertical
05_feed_1x1        square feed versions
06_feed_4x5        4:5 feed versions
07_subtitles       .srt in mk / sr / sq / en (timed to 01/02; pitch versions add a 2.2 s intro)
08_posters_teasers poster JPG, 6 s GIF and silent 6 s teaser per film
09_offer_pdfs      one-page offer per company (MK / RS / AL)
10_how_its_made    "how it's made" explainers
11_brand           logo files, font, brand.json, lower-thirds/transition, animated logo
12_outreach_private ready-to-send outreach per company WITH the real private page links (do not forward)
13_launch_kit      studio showreel 16:9 + 9:16, 6 reels, post images, profile/cover images, social_copy.md (captions + calendar)
PITCH_PAGE_LINKS.txt  the 12 private pitch pages (each company gets only its own link)
DELIVERY_AND_LICENCE.md  licence and delivery terms
Audio: films -16 LUFS, 48 kHz stereo. Contact: inf.unit@proton.me
""")
n = 0; z = f"{DL}/BIG_DOGMA_LTX.zip.part"
with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED, allowZip64=True) as zf:
    for root, _, files in os.walk(OUT):
        for f in sorted(files):
            p = os.path.join(root, f); zf.write(p, "BIG_DOGMA_LTX/" + os.path.relpath(p, OUT)); n += 1
os.rename(z, f"{DL}/BIG_DOGMA_LTX.zip"); os.chmod(f"{DL}/BIG_DOGMA_LTX.zip", 0o644)
for d in sorted(os.listdir(OUT)): print(d, len(os.listdir(f"{OUT}/{d}")) if os.path.isdir(f"{OUT}/{d}") else "")
print("ZIP_FILES", n, os.path.getsize(f"{DL}/BIG_DOGMA_LTX.zip"))
