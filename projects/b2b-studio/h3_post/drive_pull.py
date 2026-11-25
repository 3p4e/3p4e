# runs ON THE H3 BOX: download every file of the shared Drive folder listing by ID into /workspace/old_box_h3out
import re, html, os, subprocess
from concurrent.futures import ThreadPoolExecutor
s = open("/workspace/drive_h3/listing.html", encoding="utf-8", errors="ignore").read()
items = re.findall(r'<a href="https://drive.google.com/file/d/([^/"?]+)[^"]*"[^>]*>.*?<div class="flip-entry-title">(.*?)</div>', s, re.S)
OUT = "/workspace/old_box_h3out"; os.makedirs(OUT, exist_ok=True)
def get(it):
    fid, name = it[0], html.unescape(it[1]).strip(); dst = f"{OUT}/{name}"
    for a in range(4):
        subprocess.run(["curl", "-sL", "-o", dst, f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"])
        ok = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip()
        if ok: return name, os.path.getsize(dst)
    return name, -1
with ThreadPoolExecutor(6) as ex: res = list(ex.map(get, items))
bad = [n for n, sz in res if sz < 0]
print("files", len(res), "ok", len(res) - len(bad), "bytes", sum(sz for _, sz in res if sz > 0), "bad", bad, flush=True)
print("DRIVE_PULL_DONE")
