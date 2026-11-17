#!/usr/bin/env python3
"""Mix Fenrir final masters MK + EN: narration + scene SFX beds + cues + ducked
dark-Norse score over the glitch-free seamless video. -16 LUFS, 48kHz.
Uses uniform clips as video source (identical to master_v2_master)."""
import subprocess, sys, numpy as np, soundfile as sf
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
MA = ROOT / 'media/fenrir_assets'
UNI = MA / 'uniform'; AUD = MA / 'audio'
SFX = AUD / 'sfx'; NAR = AUD / 'narration'; SCORE = AUD / 'score'
OUT = MA / 'mixed'; OUT.mkdir(exist_ok=True)
SR = 48000

# 1) score (fluidsynth CLI — the in-script call 255'd; CLI is proven)
if not (SCORE / 'fenrir_theme.wav').exists():
    r = subprocess.run(['fluidsynth', '-ni', '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                        str(SCORE / 'fenrir_theme.mid'), '-F', str(SCORE / 'fenrir_theme.wav'), '-r', str(SR)],
                       capture_output=True, text=True)
    print('fluidsynth rc', r.returncode, r.stderr[-200:] if r.returncode else '')
    assert r.returncode == 0

# scene beds per shot (storyboard geography)
def bed_for(i):
    if i <= 14: return 'bed_hall'                    # Act 1 Asgard halls
    if i <= 17: return 'bed_hall'                    # Týr closeups
    if i <= 22: return 'bed_wind'                    # growth / two wolves outdoor
    if i <= 26: return 'bed_hall'                    # Gleipnir counsel
    if i <= 29: return 'bed_wind'                    # binding attempt outdoor
    if i <= 31: return 'bed_forge'                   # dwarfs forge
    if i <= 36: return 'bed_hall'                    # final binding
    if i <= 40: return 'bed_hall'                    # sacrifice
    if i <= 45: return 'bed_trail'                   # the trail
    return 'bed_trail'                               # pale light
CUES = {19: 'cue_chain', 27: 'cue_sword', 30: 'cue_chain', 39: 'cue_bite',
        40: 'cue_bite', 44: 'cue_howl_formant', 45: 'cue_howl_formant'}

def nar_file(i, lang):
    p = NAR / f's{i:02d}_{lang}.mp3'
    if p.exists(): return p
    cands = sorted(NAR.glob(f'*{i:02d}*{lang}*.mp3'))
    return cands[0] if cands else None

def build_lang(lang):
    outs = []
    for i in range(1, 47):
        v = UNI / f'fenrir_s{i:02d}.mp4'
        n = nar_file(i, lang)
        bed = SFX / f'{bed_for(i)}.wav'
        cue = SFX / f'{CUES[i]}.wav' if i in CUES else None
        dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(v)],
                                   capture_output=True,text=True).stdout.strip())
        inputs = [v, n, bed, SCORE / 'fenrir_theme.wav'] + ([cue] if cue else [])
        f = ["[1:a]aformat=sample_rates=48000,volume=1.6,adelay=250|250[nar]",
             f"[2:a]aloop=loop=999:size=1e6,atrim=0:{dur:.3f},volume=0.30[bed]",
             f"[3:a]aloop=loop=999:size=1e6,atrim=0:{dur:.3f},volume=0.20[mus]"]
        mix = "[bed][mus]amix=inputs=2:normalize=0[bm]"
        last = "[bm]"; tail = ""
        if cue:
            pos = 2.0 if i in (44,45) else 1.2
            f.append(f"[4:a]adelay={int(pos*1000)}|{int(pos*1000)}[cue]")
            mix += ";[bm][cue]amix=inputs=2:normalize=0[bmc]"; last = "[bmc]"
        f.append(mix)
        f.append(f"{last}[nar]sidechaincompress=threshold=0.03:ratio=8:attack=25:release=500[duck]")
        f.append("[duck][nar]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")
        o = OUT / f's{i:02d}_{lang}.mp4'
        cmd = ['ffmpeg','-y','-loglevel','error','-i',str(v),'-i',str(n),'-i',str(bed),'-i',str(SCORE / 'fenrir_theme.wav')]
        if cue: cmd += ['-i',str(cue)]
        cmd += ['-filter_complex',';'.join(f),'-map','0:v','-map','[aout]','-c:v','copy',
                '-c:a','aac','-b:a','192k','-ar','48000','-shortest',str(o)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode: print('MIXFAIL', i, lang, r.stderr[-300:])
        outs.append(o)
        print('mixed', lang, i, flush=True)
    lst = OUT / f'_concat_{lang}.txt'
    lst.write_text('\n'.join(f"file '{p}'" for p in outs) + '\n')
    fin = MA / f'fenrir_{lang}_master.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(lst),
                    '-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-movflags','+faststart',str(fin)], check=True)
    print('FINAL', fin)

for lang in ('MK','EN'):
    build_lang(lang)
print('ALL_MIXED')
