#!/usr/bin/env python3
"""Build all Fenrir sound assets: procedural SFX beds+cues, the Howl (formant layer),
and a dark-Norse score (MIDI -> fluidsynth). Everything in-house, no stock audio.
Outputs WAVs into media/fenrir_assets/audio/{sfx,score}."""
import os, subprocess, numpy as np, soundfile as sf
from pathlib import Path

ROOT = Path('/a0/usr/projects/vast')
A = ROOT / 'media/fenrir_assets/audio'
SFX = A / 'sfx'; SCORE = A / 'score'
for d in (SFX, SCORE): d.mkdir(parents=True, exist_ok=True)
SR = 48000
rng = np.random.default_rng(13)

def write(name, x):
    x = np.clip(x, -1, 1).astype(np.float32)
    sf.write(str(SFX / name), x, SR)
    print('sfx', name, len(x)/SR, 's')

def noise(n): return rng.standard_normal(n).astype(np.float32)
def lowpass(x, alpha):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += alpha * (x[i] - acc); y[i] = acc
    return y

def env(n, a, d, sustain=0.0):
    e = np.ones(n, np.float32)
    ai = int(a*SR); di = int(d*SR)
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if di: e[-di:] *= np.linspace(1, sustain, di)
    return e

# ---- scene beds (5s each, loop-ready-ish) ----
def bed_hall():
    x = lowpass(noise(5*SR), 0.02) * 0.35          # deep room tone
    x += lowpass(noise(5*SR), 0.005) * 0.20        # sub rumble
    for _ in range(6):                              # torch crackle
        i = rng.integers(0, 5*SR-2000)
        x[i:i+1500] += noise(1500) * np.exp(-np.linspace(0,6,1500)) * 0.10
    return x * env(5*SR, 0.4, 0.4)
def bed_wind():
    base = lowpass(noise(5*SR), 0.03)
    lfo = 0.5 + 0.5*np.sin(np.linspace(0, 6*np.pi, 5*SR))   # gusts
    return base * (0.15 + 0.35*lfo) * env(5*SR, 0.6, 0.6)
def bed_forge():
    x = lowpass(noise(5*SR), 0.06) * 0.30          # fire roar
    for _ in range(4):                              # hammer strikes
        i = rng.integers(1000, 5*SR-8000)
        t = np.arange(6000)/SR
        clank = (np.sin(2*np.pi*820*t) + 0.6*np.sin(2*np.pi*1240*t) + 0.4*noise(6000)) * np.exp(-t*22)
        x[i:i+6000] += clank * 0.55
    return x * env(5*SR, 0.3, 0.3)
def bed_ocean():
    t = np.arange(5*SR)/SR
    x = lowpass(noise(5*SR), 0.02)
    lfo = 0.5 + 0.5*np.sin(2*np.pi*0.25*t)          # slow swell
    return x * (0.12 + 0.30*lfo) * env(5*SR, 0.8, 0.8)
def bed_trail():
    x = lowpass(noise(5*SR), 0.012) * 0.30
    x += lowpass(noise(5*SR), 0.004) * 0.15
    return x * env(5*SR, 0.8, 0.8)

# ---- one-shots ----
def cue_chain():
    n = int(1.2*SR); x = np.zeros(n, np.float32)
    for _ in range(8):
        i = rng.integers(0, n-3000)
        x[i:i+2500] += lowpass(noise(2500), 0.5) * np.exp(-np.linspace(0,9,2500)) * 0.5
    return x
def cue_bite():
    n = int(0.5*SR); t = np.arange(n)/SR
    thud = lowpass(noise(n), 0.3) * np.exp(-t*28)
    snap = noise(n) * np.exp(-t*60) * 0.6
    return (thud + snap) * 0.9
def cue_sword():
    n = int(1.0*SR); t = np.arange(n)/SR
    return (noise(n)*np.exp(-t*15)*0.5 + np.sin(2*np.pi*2400*t)*np.exp(-t*30)*0.3)
def cue_howl_formant():
    # the in-house howl: rising glissando through wolf formants
    n = int(2.8*SR); t = np.arange(n)/SR
    f0 = 280 + 180*np.sin(np.pi*np.clip(t/2.8, 0, 1)**0.8)   # rise & fall
    formants = [(340, 60), (720, 90), (1100, 120), (2500, 200)]
    x = np.zeros(n, np.float32)
    ph = np.cumsum(2*np.pi*f0/SR)
    saw = ((ph/np.pi) % 2) - 1
    for fc, bw in formants:
        # rough band-pass via heterodyne + lowpass
        car = np.sin(2*np.pi*fc*t)
        m = saw * car
        x += lowpass(m, bw/ (SR/2)) * 2.0
    am = env(n, 0.5, 1.0)
    return lowpass(x * am, 0.4) * 0.8

BEDS = {'hall': bed_hall, 'wind': bed_wind, 'forge': bed_forge, 'ocean': bed_ocean, 'trail': bed_trail}
for k, fn in BEDS.items(): write(f'bed_{k}.wav', fn())
write('cue_chain.wav', cue_chain())
write('cue_bite.wav', cue_bite())
write('cue_sword.wav', cue_sword())
write('cue_howl_formant.wav', cue_howl_formant())

# ---- score: dark Norse MIDI -> fluidsynth ----
midi = SCORE / 'fenrir_theme.mid'
import mido
m = mido.MidiFile(ticks_per_beat=480)
track = mido.MidiTrack(); m.tracks.append(track)
track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(72)))
DRONE = 29   # GM: overdrive guitar? use 32 acoustic bass for drone
STRINGS = 48
PERC = 116   # GM timpani-ish; frame drum approximated
LOW_STRING_NOTES = [38, 45, 41, 36]   # D2 A2 F2 C2 — dark loop
for bar in range(8):
    t0 = bar*480*4
    track.append(mido.Message('program_change', program=32, time=0))
    for n in LOW_STRING_NOTES:
        track.append(mido.Message('note_on', note=n+12, velocity=52, time=t0 if n==LOW_STRING_NOTES[0] else 0))
        track.append(mido.Message('note_off', note=n+12, time=480*3))
    # frame-drum hits on 1 & 3
    track.append(mido.Message('program_change', program=116, time=0))
    for beat in (0, 2):
        track.append(mido.Message('note_on', note=36, velocity=80, time=t0 + beat*480))
        track.append(mido.Message('note_off', note=36, time=120))
m.save(str(midi))
sf2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
wav = SCORE / 'fenrir_theme.wav'
subprocess.run(['fluidsynth', '-ni', sf2, str(midi), '-F', str(wav), '-r', str(SR)], check=True)
# normalize score, trim/pad to a loopable 8 bars (~26.7s)
y, sr = sf.read(str(wav))
if y.ndim > 1: y = y.mean(axis=1)
y = y / (np.abs(y).max() + 1e-9) * 0.8
sf.write(str(wav), y.astype(np.float32), SR)
print('score', wav, len(y)/SR, 's')
print('AUDIO_BUILD_DONE')
