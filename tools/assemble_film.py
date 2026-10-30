#!/usr/bin/env python3
"""Assemble a film from shot clips, dialogue lines and a score (ffmpeg).

  python3 tools/assemble_film.py <edl.json> <out.mp4>

edl.json: {"clips_dir": ..., "audio_dir": ..., "score": ...,
           "shots": [["01", 6.0], ...],                # clip id, seconds used (trimmed from start)
           "lines": [["L01_shar", "01", 0.5, "dry"], ...]}  # file, shot it starts in, offset, fx
fx: dry | echo (fallen angels) | hall (goddess)
"""
import json
import subprocess
import sys
from pathlib import Path

FX = {
    "dry": "anull",
    "echo": "volume=1.6,aecho=0.8:0.6:60|140:0.3|0.15,lowpass=f=6500",
    "hall": "aecho=0.8:0.7:120|260|420:0.35|0.25|0.18",
}


def main(edl_path, out):
    e = json.loads(Path(edl_path).read_text())
    clips, audio = Path(e["clips_dir"]), Path(e["audio_dir"])
    starts, t = {}, 0.0
    for sid, dur in e["shots"]:
        starts[sid] = t
        t += dur
    total = t

    inputs, vf = [], []
    for i, (sid, dur) in enumerate(e["shots"]):
        inputs += ["-i", str(clips / f"shot_{sid}.mp4")]
        vf.append(f"[{i}:v]trim=0:{dur},setpts=PTS-STARTPTS,scale=1920:1080,fps=24,setsar=1[v{i}]")
    n = len(e["shots"])
    vf.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,"
              f"fade=t=in:st=0:d=1,fade=t=out:st={total-1.5}:d=1.5[vout]")

    # Score stretched (pitch preserved) to the cut length, then ducked under dialogue
    score_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                      "csv=p=0", e["score"]], capture_output=True, text=True).stdout)
    inputs += ["-i", e["score"]]
    si = n
    af = [f"[{si}:a]atempo={score_len/total:.4f},volume=0.32,afade=t=out:st={total-3}:d=3,"
          f"aresample=48000,asplit=2[sc][sck]"]
    labels = []
    for j, (name, sid, off, fx) in enumerate(e["lines"]):
        inputs += ["-i", str(audio / f"{name}.wav")]
        ms = int((starts[sid] + off) * 1000)
        af.append(f"[{si+1+j}:a]{FX[fx]},aresample=48000,adelay={ms}|{ms},apad[d{j}]")
        labels.append(f"[d{j}]")
    af.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
              f"atrim=0:{total},asplit=2[dia][key]")
    af.append("[sc][key]sidechaincompress=threshold=0.015:ratio=10:attack=10:release=600[duck]")
    af.append(f"[duck][dia]amix=inputs=2:normalize=0,atrim=0:{total},loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
    af.append("[sck]anullsink")

    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(vf + af),
           "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(f"{out}: {total:.1f}s, {n} shots, {len(labels)} lines")


if __name__ == "__main__":
    main(*sys.argv[1:3])
