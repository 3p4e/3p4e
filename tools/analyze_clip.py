#!/usr/bin/env python3
import argparse, json, os, subprocess, sys
import numpy as np

def probe(path):
    r = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True)
    try: return json.loads(r.stdout or "{}")
    except Exception: return {}

def spec(meta):
    st = meta.get("streams",[])
    v = next((s for s in st if s.get("codec_type")=="video"), None)
    a = next((s for s in st if s.get("codec_type")=="audio"), None)
    if not v: return None, None
    n,_,d = (v.get("r_frame_rate") or "0/1").partition("/")
    fps = float(n)/float(d) if d and float(d) else 0.0
    vv = {"codec":v.get("codec_name"),"w":v.get("width"),"h":v.get("height"),"fps":round(fps,3),
          "frames":int(v.get("nb_frames") or 0),"dur":round(float(v.get("duration") or 0),3)}
    if not vv["frames"]:
        dur = float(v.get("duration") or meta.get("format",{}).get("duration") or 0)
        vv["frames"] = int(round(dur*fps))
    aa = None
    if a: aa = {"codec":a.get("codec_name"),"ch":a.get("channels"),"sr":a.get("sample_rate")}
    return vv, aa

def frames_gray(path,w=96,h=54):
    r = subprocess.run(["ffmpeg","-v","error","-i",path,"-vf","scale=%d:%d,format=gray"%(w,h),"-f","rawvideo","-"],capture_output=True)
    raw = r.stdout
    fb = w*h
    n = len(raw)//fb
    if n<1: return np.zeros((0,h,w),dtype=np.uint8)
    return np.frombuffer(raw[:n*fb],dtype=np.uint8).reshape(n,h,w)

def motion(fr):
    if len(fr)<2: return {"frames":len(fr),"mean":0.0,"max":0.0,"frozen":0,"frozen_pct":0.0}
    f = fr.astype(np.float32)
    d = np.abs(np.diff(f,axis=0)).mean(axis=(1,2))
    frozen = int((d<0.05).sum())
    return {"frames":int(len(fr)),"mean":round(float(d.mean()),3),"min":round(float(d.min()),3),
            "max":round(float(d.max()),3),"frozen":frozen,"frozen_pct":round(100.0*frozen/max(len(d),1),1)}

def luma(fr):
    if not len(fr): return {}
    m = fr.reshape(len(fr),-1).mean(axis=1)
    s = fr.reshape(len(fr),-1).std(axis=1)
    return {"mean":round(float(m.mean()),2),"std":round(float(m.std()),2),"min":round(float(m.min()),2),
            "max":round(float(m.max()),2),"black":int((m<8.0).sum()),"detail_std_mean":round(float(s.mean()),2)}

def strip(path,out_png,count=5,width=320):
    vv,_ = spec(probe(path))
    total = max((vv or {}).get("frames",1),1)
    idxs = [int(round((total-1)*i/(count-1))) for i in range(count)] if total>1 else [0]
    d = os.path.dirname(out_png) or "."
    files=[]
    for i in idxs:
        fp = os.path.join(d,"_s_%d.png"%i)
        subprocess.run(["ffmpeg","-v","error","-y","-i",path,"-vf","select=eq(n\\,%d),scale=%d:-1"%(i,width),"-vsync","0","-frames:v","1",fp],capture_output=True)
        if os.path.exists(fp): files.append(fp)
    if not files: return None
    args=["ffmpeg","-v","error","-y"]
    for fp in files: args += ["-i",fp]
    args += ["-filter_complex","hstack=inputs=%d"%len(files),out_png]
    subprocess.run(args,capture_output=True)
    for fp in files:
        try: os.remove(fp)
        except OSError: pass
    return out_png if os.path.exists(out_png) else None

ap = argparse.ArgumentParser()
ap.add_argument("clip"); ap.add_argument("--tag",default=None)
ap.add_argument("--strip-dir",default=None); ap.add_argument("--json",default=None)
a = ap.parse_args()
p = a.clip
if not os.path.exists(p):
    print("MISSING:",p); sys.exit(1)
stem = os.path.splitext(os.path.split(p)[1])[0]
tag = a.tag or stem
vv,aa = spec(probe(p))
fr = frames_gray(p)
rep = {"clip":p,"tag":tag,"video":vv,"audio":aa,"motion":motion(fr),"luma":luma(fr)}
if a.strip_dir:
    os.makedirs(a.strip_dir,exist_ok=True)
    rep["strip"] = strip(p,os.path.join(a.strip_dir,tag+"_strip.png"))
print(json.dumps(rep,indent=2,ensure_ascii=False))
if a.json:
    os.makedirs(os.path.dirname(a.json) or ".",exist_ok=True)
    open(a.json,"w",encoding="utf-8").write(json.dumps(rep,indent=2,ensure_ascii=False))
