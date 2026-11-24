# Lay a music bed under every LTX film: music ~-20 dB under the voice-over, ducked further by the VO (sidechain),
# 0.8 s fade-in, 2.5 s fade-out ending with the film, loudness-normalised to -16 LUFS. Then 9:16 versions.
import os, sys, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
MUSIC = sys.argv[1] if len(sys.argv) > 1 else f"{S}/music/ace_final"
OUT = f"{S}/final_music"; VOUT = f"{S}/final_music_9x16"
os.makedirs(OUT, exist_ok=True); os.makedirs(VOUT, exist_ok=True)
FAM, CORP, CON, AUTO, LUX, IND, UP, SHOW = "1_family", "2_corporate", "3_construction", "4_automotive", "5_luxury", "6_industrial", "7_upbeat", "8_showreel"
MAP = {
 # batch 1
 "bw_commercial": LUX, "gener2_commercial": CON, "concord_commercial": LUX, "zito_commercial": FAM, "viva_commercial": FAM,
 "alkaloid_commercial": CORP, "replek_commercial": CORP, "millennium_commercial": IND, "nelt_commercial": UP, "speeex_commercial": UP,
 "vincinni_family_ad": FAM, "vincinni_factory_ad": FAM, "foton_tunland_v9_specs": AUTO,
 # batch 2: company films
 "bw_riverside_film": LUX, "gener2_builder_film": CON, "concord_offplan_film": LUX, "zito_opening_film": FAM, "viva_expansion_film": FAM,
 "alkaloid_employer_film": CORP, "replek_export_film": CORP, "millennium_capability_film": IND, "nelt_logistics_film": UP, "speeex_recruitment_film": UP,
 # timelapse demos
 "timelapse_construction": CON, "timelapse_developer": CON, "timelapse_road": CON, "timelapse_solar": CON, "timelapse_expo_stand": UP,
 "timelapse_store_fitout": UP, "timelapse_office_fitout": UP, "timelapse_renovation": UP, "timelapse_landscaping": FAM,
 "timelapse_apartment_staging": LUX, "timelapse_interior_design": LUX,
 # sector demos and reels
 "sector_automotive": AUTO, "sector_pharma": CORP, "sector_food": FAM, "sector_wine": LUX, "sector_steel_cement": IND,
 "sector_recruitment": UP, "sector_product_launch": SHOW, "sector_real_estate": LUX,
 "showreel_macedonian_industry": IND, "studio_showreel_ltx": SHOW, "foton_showreel_v2": AUTO,
}
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def mix(film, track, out):
    d = dur(film); fo = max(0.0, d - 2.5)
    fc = (f"[1:a]aloop=loop=-1:size=2e9,atrim=0:{d:.2f},volume=0.16,afade=t=in:st=0:d=0.8,afade=t=out:st={fo:.2f}:d=2.5,aformat=sample_rates=48000:channel_layouts=stereo[m];"
          f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][key];"
          f"[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=400[md];"
          f"[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]")
    subprocess.run(["ffmpeg","-v","error","-y","-i",film,"-i",track,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",out],check=True)
def vertical(src, out):
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex","[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2",
                    "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",out],check=True)
only = sys.argv[2:]
for d in ("final_commercials", "final_commercials_b2"):
    for f in sorted(os.listdir(f"{S}/{d}")):
        n = f[:-4]
        if not f.endswith(".mp4") or n not in MAP or (only and n not in only): continue
        track = f"{MUSIC}/{MAP[n]}.mp3"
        mix(f"{S}/{d}/{f}", track, f"{OUT}/{f}")
        if not only or "--vertical" in sys.argv: vertical(f"{OUT}/{f}", f"{VOUT}/{n}_9x16.mp4")
        print("OK", n, MAP[n], flush=True)
missing = [n for n in MAP if not os.path.exists(f"{OUT}/{n}.mp4")]
print("MIX_DONE missing:", missing)
