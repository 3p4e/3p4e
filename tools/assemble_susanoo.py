#!/usr/bin/env python3
"""Assemble the Susanoo & Oroki film: 6 photoreal clips + 6 Macedonian narration lines.

Local only, zero GPU cost. Each beat is stretched (max 1.25x) and padded with a
brief frame hold so the narration fits without cutting the line short.
"""
import os
import subprocess

D = "/a0/usr/projects/vast"
CLIP = f"{D}/media/susanoo_v3_photoreal"
AUD = f"{D}/media/susanoo_audio"
OUT = f"{D}/media/susanoo_film"
W, H, FPS = 832, 1104, 24
MAX_STRETCH = 1.25
LEAD = 0.35          # narration starts this long after the beat begins
TAIL = 0.55          # guaranteed silence after the line

BEATS = [
    ("kf_1_descent", "nar_1"),
    ("kf_1_thunder", "nar_2"),
    ("kf_3_argument", "nar_3"),
    ("kf_4_decision", "nar_4"),
    ("kf_2_sword", "nar_5"),
    ("kf_3_wedding", "nar_6"),
]


def dur(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path]
    ).decode().strip()
    return float(out)


def run(cmd):
    subprocess.run(cmd, check=True)


os.makedirs(OUT, exist_ok=True)
parts = []
clock = 0.0
print(f"{'beat':<16}{'clip':>7}{'line':>7}{'beat_T':>8}{'stretch':>9}{'start':>8}")
for clip, nar in BEATS:
    cpath = f"{CLIP}/{clip}_v3.mp4"
    apath = f"{AUD}/{nar}.wav"
    cd, ad = dur(cpath), dur(apath)
    target = max(cd, ad + LEAD + TAIL)
    stretch = min(target / cd, MAX_STRETCH)
    held = max(target - cd * stretch, 0.0)
    tmp = f"{OUT}/b_{clip}.mp4"
    vf = (
        f"setpts={stretch:.6f}*PTS,fps={FPS},"
        f"tpad=stop_mode=clone:stop_duration={held:.3f},"
        f"scale={W}:{H},setsar=1"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", cpath, "-an",
         "-filter:v", vf, "-t", f"{target:.3f}",
         "-c:v", "libx264", "-crf", "17", "-preset", "medium",
         "-pix_fmt", "yuv420p", tmp])
    print(f"{clip:<16}{cd:>7.2f}{ad:>7.2f}{target:>8.2f}{stretch:>9.2f}{clock:>8.2f}")
    parts.append((tmp, apath, clock, target))
    clock += target

# video concat
listing = f"{OUT}/concat.txt"
with open(listing, "w") as fh:
    for p, _, _, _ in parts:
        fh.write(f"file '{p}'\n")
video = f"{OUT}/_video.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
     "-i", listing, "-c", "copy", video])

# narration laid at each beat start, then mixed
inputs, filters, labels = [], [], []
for i, (_, apath, start, _) in enumerate(parts):
    inputs += ["-i", apath]
    ms = int(round(start * 1000))
    filters.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,"
                   f"loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,"
                   f"adelay={ms}|{ms}[a{i}]")
    labels.append(f"[a{i}]")
mix = "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,"
mix += f"apad,atrim=0:{clock:.3f},afade=t=out:st={clock - 1.2:.3f}:d=1.2[aout]"
filters.append(mix)
audio = f"{OUT}/_audio.wav"
run(["ffmpeg", "-y", "-v", "error", *inputs,
     "-filter_complex", ";".join(filters), "-map", "[aout]",
     "-c:a", "pcm_s16le", audio])

final = f"{OUT}/susanoo_photoreal_832x1104.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", audio,
     "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
     "-movflags", "+faststart", final])
print(f"\nFINAL {final}")
print(f"video {dur(video):.3f}s  audio {dur(audio):.3f}s  film {dur(final):.3f}s")
