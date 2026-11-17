#!/usr/bin/env python3
"""VAST #23 v4 audio mix: per-clip duck K6 native bed -14dB + overlay MOSS narration -> concat -> loudnorm -16 LUFS."""
import subprocess, os, glob, json
CLIPS="media/perseus_assets/k6_clips"
NARR="media/perseus_assets/audio_narration"
OUT="media/perseus_assets/k6_audio"
os.makedirs(OUT, exist_ok=True)
# picture-lock order: clips s01-s20, f01-f10, s31-s65 ; narration v3 ids: s01-s20, f01-f10, s26-s60
ORDER=[f"s{n:02d}" for n in range(1,21)]+[f"f{n:02d}" for n in range(1,11)]+[f"s{n:02d}" for n in range(31,66)]
def narr_id(clip):
    if clip.startswith('f'): return clip
    n=int(clip[1:])
    return f"s{n:02d}" if n<=20 else f"s{n-5:02d}"  # s31->s26 ... s65->s60
print(f"mixing {len(ORDER)} clips...")
mixed=[]
for i,c in enumerate(ORDER):
    clip=os.path.join(CLIPS,f"p23_{c}_k6.mp4")
    wav=os.path.join(NARR,f"{narr_id(c)}.wav")
    out=os.path.join(OUT,f"{i+1:02d}_{c}.wav")
    if not os.path.exists(clip): print(f"  MISSING clip {c}"); continue
    # build filter: bed ducked -14dB (or silent if no bed) + narration overlay
    has_narr=os.path.exists(wav)
    if has_narr:
        fc=f"[0:a]volume=-14dB[bed];[1:a]aresample=48000,volume=2.0[nar];[bed][nar]amix=inputs=2:duration=first[a]"
        cmd=["ffmpeg","-y","-v","error","-i",clip,"-i",wav,"-filter_complex",fc,"-map","[a]","-ar","48000","-ac","2",out]
    else:
        cmd=["ffmpeg","-y","-v","error","-i",clip,"-af","volume=-14dB,aresample=48000","-ac","2",out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0: print(f"  MIX FAIL {c}: {r.stderr[:120]}"); continue
    mixed.append(out)
    if (i+1)%10==0: print(f"  {i+1}/{len(ORDER)}")
print(f"mixed {len(mixed)}/{len(ORDER)}")
# concat mixed wavs
concat=os.path.join(OUT,"_concat.txt")
with open(concat,"w") as f:
    for m in mixed: f.write(f"file '{os.path.abspath(m)}'\n")
master="media/perseus_assets/k6_master/p23_audio_master_v1.wav"
os.makedirs(os.path.dirname(master),exist_ok=True)
r=subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",concat,"-af","loudnorm=I=-16:TP=-1.0:LRA=11","-ar","48000","-c:a","pcm_s24le",master],capture_output=True,text=True)
print("concat+loudnorm:", "OK" if r.returncode==0 else r.stderr[:200])
if r.returncode==0:
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",master],capture_output=True,text=True).stdout.strip()
    print(f"AUDIO MASTER: {master} dur={d}s")
