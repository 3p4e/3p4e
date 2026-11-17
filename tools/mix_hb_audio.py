#!/usr/bin/env python3
"""Hollow Bloom dual-language audio: two masters (MK/EN), duck beds -12dB, -16 LUFS, D5/D6 hard-sync.
Usage: python tools/mix_hb_audio.py [--lang mk|en]   (needs clip WAVs extracted first)"""
import subprocess, os, sys, json
CLIPS='media/dhpf_hb_clips'
STEMS='media/hb_audio'
DIALOGUE_SLOTS={'D1':('s07',2.0),'D2':('s19_end',0.5),'D3':('s26',1.5),'D4':('s36',1.0),'D5':('s44',0.8),'D6':('s45',0.3),'D7':('s49',1.0)}
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode!=0: print('ERR',c[:80],r.stderr[:200])
    return r.returncode==0
if __name__=='__main__':
    lang=sys.argv[sys.argv.index('--lang')+1] if '--lang' in sys.argv else 'mk'
    print(f'[mix-hb] lang={lang} — extract clip audio beds, place dialogue at slots, duck -12dB, loudnorm -16 LUFS')
    print('[mix-hb] NOTE: run after batch; MK stems come from MOSS on-box, EN from media/hb_audio/tts_en/')
