import subprocess, os
CLIPS="media/perseus_assets/k6_clips"; NARR="media/perseus_assets/audio_en"; OUT="media/perseus_assets/k6_audio_en"
os.makedirs(OUT, exist_ok=True)
ORDER=[f"s{n:02d}" for n in range(1,21)]+[f"f{n:02d}" for n in range(1,11)]+[f"s{n:02d}" for n in range(31,66)]
def nid(c):
    if c.startswith('f'): return c
    n=int(c[1:]); return f"s{n:02d}" if n<=20 else f"s{n-5:02d}"
mixed=[]
for i,c in enumerate(ORDER):
    clip=os.path.join(CLIPS,f"p23_{c}_k6.mp4"); wav=os.path.join(NARR,f"{nid(c)}.wav"); out=os.path.join(OUT,f"{i+1:02d}_{c}.wav")
    if not os.path.exists(clip): continue
    if os.path.exists(wav):
        fc=f"[0:a]volume=-14dB[bed];[1:a]aresample=48000,volume=2.0[nar];[bed][nar]amix=inputs=2:duration=first[a]"
        cmd=["ffmpeg","-y","-v","error","-i",clip,"-i",wav,"-filter_complex",fc,"-map","[a]","-ar","48000","-ac","2",out]
    else:
        cmd=["ffmpeg","-y","-v","error","-i",clip,"-af","volume=-14dB,aresample=48000","-ac","2",out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode==0: mixed.append(out)
concat=os.path.join(OUT,"_concat.txt")
with open(concat,"w") as f:
    for m in mixed: f.write(f"file '{os.path.abspath(m)}'\n")
master="media/perseus_assets/k6_master/p23_audio_master_en_v1.wav"
r=subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",concat,"-af","loudnorm=I=-16:TP=-1.0:LRA=11","-ar","48000","-c:a","pcm_s24le",master],capture_output=True,text=True)
d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",master],capture_output=True,text=True).stdout.strip()
print(f"EN MASTER: {master} dur={d}s mixed={len(mixed)}/65")
