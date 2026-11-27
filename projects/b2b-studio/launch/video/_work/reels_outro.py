# Replaces the outro of reels that were already built (owner 2026-11-27: no drawn logo animation; the 9:16 film masters are
# archived off this machine, so a full reels.py rebuild is not possible here). Each reel = body + 67-frame outro (reels.py):
# the body frames are kept, the old outro is swapped for the still one (seg/outro_9x16.mp4 + png/outro_disc_9x16.png with the
# tagline and the AI disclosure), using the same fades as reels.py outro_chain(). Audio (incl. the sting) is copied untouched.
# usage: python3 reels_outro.py <dir with the original reels> [out_dir]   (default out: /dev/shm/vall/reels_still)
import os, sys, glob, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; SEG = f"{W}/seg"; DISC = f"{W}/png/outro_disc_9x16.png"
SRC = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else "/dev/shm/vall/reels_still"; os.makedirs(OUT, exist_ok=True)
FPS = 24; OUTRO_F = 67                                    # same as reels.py
def probe(f, what):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", f"stream={what}", "-of", "csv=p=0", f],
                          capture_output=True, text=True).stdout.strip()
for src in sorted(glob.glob(f"{SRC}/reel_0*.mp4")):
    nf = int(probe(src, "nb_read_frames")); body = nf - OUTRO_F; out = f"{OUT}/{os.path.basename(src)}"
    od = OUTRO_F / FPS
    fc = (f"[0:v]trim=end_frame={body},setpts=PTS-STARTPTS,format=yuv420p,setsar=1,settb=1/{FPS}[b];"
          f"[1:v]trim=start_frame=0:end_frame={OUTRO_F},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1[oa];"
          f"[2:v]format=rgba,fade=t=in:st=0.6:d=0.5:alpha=1[od];[oa][od]overlay=0:0:format=auto:shortest=1,format=yuv420p,"
          f"fade=t=in:st=0:d=0.18,fade=t=out:st={od - 0.3:.3f}:d=0.3,setsar=1,settb=1/{FPS}[o];[b][o]concat=n=2:v=1:a=0,format=yuv420p[v]")
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-i", src, "-i", f"{SEG}/outro_9x16.mp4", "-loop", "1", "-framerate", str(FPS), "-t", "4", "-i", DISC,
                    "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    got = int(probe(out, "nb_read_frames")); assert got == nf, (out, got, nf)
    print("OK", out, got, "frames", flush=True)
