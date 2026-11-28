# Build PITCH_KITS_LTX/<prospect>/ with 16:9 + 9:16 films and message.txt (from PITCH_KITS_LTX.md).
import os, re, shutil
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
md = open("/home/user/3p4e/projects/b2b-studio/PITCH_KITS_LTX.md").read()
K = {"01_zito_marketi_MK": ("Žito Marketi", ["zito_commercial", "zito_opening_film"]),
     "02_alkaloid_MK": ("Alkaloid", ["alkaloid_commercial", "alkaloid_employer_film"]),
     "03_replek_MK": ("Replek", ["replek_commercial", "replek_export_film"]),
     "04_vincinni_MK": ("Vincinni / Makprogres", ["vincinni_family_ad", "vincinni_factory_ad"]),
     "05_foton_MK": ("Foton Macedonia", ["foton_tunland_v9_specs", "foton_showreel_v2"]),
     "06_beograd_na_vodi_RS": ("Beograd na vodi", ["bw_commercial", "bw_riverside_film"]),
     "07_millennium_team_RS": ("Millennium Team", ["millennium_commercial", "millennium_capability_film"]),
     "08_nelt_RS": ("Nelt Group", ["nelt_commercial", "nelt_logistics_film"]),
     "09_gener2_AL": ("Gener 2", ["gener2_commercial", "gener2_builder_film"]),
     "10_concord_AL": ("Concord Investment / Kastrati", ["concord_commercial", "concord_offplan_film"]),
     "11_viva_fresh_XK": ("Viva Fresh (Kosovo)", ["viva_commercial", "viva_expansion_film"]),
     "12_speeex_XK": ("SPEEEX (Kosovo)", ["speeex_commercial", "speeex_recruitment_film"])}
root = f"{S}/PITCH_KITS_LTX_MUSIC"; shutil.rmtree(root, ignore_errors=True)
def find(n):
    for d in ("final_music",):
        p = f"{S}/{d}/{n}.mp4"
        if os.path.exists(p): return p
for folder, (head, films) in K.items():
    d = f"{root}/{folder}"; os.makedirs(d)
    for n in films:
        shutil.copy(find(n), f"{d}/{n}_16x9.mp4")
        v = f"{S}/final_music_9x16/{n}_9x16.mp4"
        if os.path.exists(v): shutil.copy(v, f"{d}/{n}_9x16.mp4")
    sec = md.split(f"### {head}")[1].split("\n### ")[0].split("\n---")[0]
    msg = "\n".join(l[2:] for l in sec.splitlines() if l.startswith("> "))
    if folder.startswith("05_foton"): msg = open("/home/user/3p4e/projects/b2b-studio/FOTON_PITCH_MK.md").read()
    open(f"{d}/message.txt", "w").write(msg + "\n")
d = f"{root}/00_studio_showreel_and_sector_demos"; os.makedirs(d)
for f in sorted(os.listdir(f"{S}/final_music")):
    if f.startswith(("studio_showreel", "sector_", "timelapse_", "showreel_")): shutil.copy(f"{S}/final_music/{f}", d)
shutil.copy("/home/user/3p4e/projects/b2b-studio/PITCH_KITS_LTX.md", f"{root}/README_PITCH_KITS.md")
for folder in sorted(os.listdir(root)):
    p = f"{root}/{folder}"
    if os.path.isdir(p): print(folder, len(os.listdir(p)), "files")
