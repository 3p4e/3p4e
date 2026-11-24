# Re-brand the two KAM films as Žito Marketi (green staff shirts match Žito's green brand); same footage, new VO line + end card with the official logo.
import os, sys
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
exec(open(f"{S}/cut/cut2.py").read().split("\nonly = sys.argv")[0])
logo = f"{S}/qc/zlogo.png"
OUT1 = f"{S}/final_commercials"
build("zito_commercial", "mk", "Жито маркети", "Жито маркети",
      [(f"{S}/ltx610/comm_kam_{i}.mp4", f"{TR}/zito_{i}.wav") for i in range(1, 6)], "Свежината започнува тука.", logo)
shots = ["prop_kam_skopje_s3", "prop_kam_skopje_s1", "prop_kam_skopje_s4", "prop_kam_skopje_s2"]
parts = []
for i, cid in enumerate(shots):
    p = f"tmp/zito_b2_{i}.mp4"; seg2(clip(cid), f"{TR}/b2_zito_opening_film_{i+1}.wav", p); parts.append(p)
card("tmp/zito_b2_card.mp4", "mk", "Жито маркети", "Жито маркети", "Секогаш блиску до вас.", logo); parts.append("tmp/zito_b2_card.mp4")
join(parts, f"{S}/final_commercials_b2/zito_opening_film.mp4", 0.35); print("zito_opening_film", round(dur(f"{S}/final_commercials_b2/zito_opening_film.mp4"), 1))
