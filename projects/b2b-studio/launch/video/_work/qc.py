# QC table: duration, streams, loudness (EBU R128 integrated + true peak) for every deliverable video
import glob, os, subprocess, json, re, sys
D = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/launch/video"
for f in sorted(glob.glob(D + "/*.mp4")):
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels",
                                   "-of", "json", f], capture_output=True, text=True).stdout)
    v = [s for s in p["streams"] if "width" in s][0]; a = [s for s in p["streams"] if "sample_rate" in s]
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]; TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    print(f"{os.path.basename(f):38s} {float(p['format']['duration']):6.2f}s {v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} | "
          f"{a[0]['codec_name'] if a else '-'} {a[0]['sample_rate'] if a else ''} | I={I} LUFS TP={TP} dBTP | {int(p['format']['size'])/1e6:.1f} MB")
