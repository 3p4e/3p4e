#!/usr/bin/env python3
"""VAST #23 K6 full slop/deviation analysis. Per clip (121f): frame-drift vs START keyframe, motion,
face count/identity vs AZ+DD centroids and canonical sheets. Flags slideshow/morph/random-faces/drift."""
import cv2, os, json, glob, numpy as np
ROOT='media/perseus_assets'; OUT=os.path.join(ROOT,'analysis','slop'); os.makedirs(OUT,exist_ok=True)
YUNET='tools/models/face_detection_yunet_2023mar.onnx'
CLIPS=sorted(glob.glob(os.path.join(ROOT,'k6_clips','p23_*_k6.mp4')))
# keyframe map (clip name -> start kf)
def kfpath(name):
    n=name.replace('p23_','').replace('_k6.mp4','')
    for cand in [os.path.join(ROOT,'keyframes',f'kf_{n}_start.png'),os.path.join(ROOT,'keyframes',f'{n}.png')]:
        if os.path.exists(cand): return cand
    return None
# identity refs: AZ + DD centroids (embed via face crop -> small embedding from pixel stats; use correlation of grayscale face patches is weak -> use count+position stability + drift)
# load YuNet
det=cv2.FaceDetectorYN_create(YUNET,'',(320,320),score_threshold=0.6,nms_threshold=0.3,top_k=5000)
def faces(frame):
    h,w=frame.shape[:2]; det.setInputSize((w,h)); _,fs=det.detect(frame)
    return [] if fs is None else [f for f in fs]
def emb(gray_box):
    g=cv2.resize(gray_box,(64,64)).astype(np.float32)/255.0; return g.flatten()
def cos(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-6))
# reference embeddings from canonical sheets (crop largest face)
def ref_emb(path):
    img=cv2.imread(path)
    if img is None: return None
    fs=faces(img)
    if not fs: return None
    x,y,w,h=[max(0,int(v)) for v in fs[0][:4]]
    crop=img[y:y+h,x:x+w]
    return emb(cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)) if crop.size else None
def _first(*ps):
    for p in ps:
        e=ref_emb(p)
        if e is not None: return e
    return None
REFS={'perseus':_first(os.path.join(ROOT,'perseus_sheet_p2.jpg'),os.path.join(ROOT,'perseus_sheet_p1.jpg')),
      'medusa':ref_emb(os.path.join(ROOT,'medusa_sheet_p1.jpg')),
      'athena':ref_emb(os.path.join(ROOT,'athena_sheet_p2.jpg')),
      'andromeda':ref_emb(os.path.join(ROOT,'andromeda_sheet_p2.jpg'))}
print('ref emb present:',{k:v is not None for k,v in REFS.items()})
report={}
for cp in CLIPS:
    name=os.path.basename(cp).replace('p23_','').replace('_k6.mp4','')
    cap=cv2.VideoCapture(cp); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 121
    kfp=kfpath(name); kf=cv2.imread(kfp) if kfp else None
    kfg=cv2.cvtColor(cv2.resize(kf,(416,240)),cv2.COLOR_BGR2GRAY) if kf is not None else None
    prev=None; drifts=[]; mots=[]; nfcs=[]; idd={'perseus':[],'medusa':[],'athena':[],'andromeda':[]}
    f=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        g=cv2.cvtColor(cv2.resize(fr,(416,240)),cv2.COLOR_BGR2GRAY)
        if kfg is not None: drifts.append(cos(emb(g),emb(kfg)))
        if prev is not None: mots.append(float(np.abs(g.astype(np.float32)-prev.astype(np.float32)).mean()))
        prev=g
        if f%6==0:
            fs=faces(fr); nfcs.append(len(fs))
            for fc in fs[:2]:
                x,y,w,h=[max(0,int(v)) for v in fc[:4]]
                crop=fr[y:y+h,x:x+w]
                if crop.size==0: continue
                e=emb(cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY))
                best=max(((k,cos(e,r)) for k,r in REFS.items() if r is not None),key=lambda t:t[1],default=(None,0))
                if best[0]: idd[best[0]].append(best[1])
        f+=1
    cap.release()
    d=np.array(drifts) if drifts else np.array([0]); m=np.array(mots) if mots else np.array([0]); nc=np.array(nfcs)
    report[name]={'frames':f,'drift_mean':float(d.mean()),'drift_end':float(d[-1]) if len(d) else 0,
      'drift_min':float(d.min()),'mot_mean':float(m.mean()),'mot_max':float(m.max()),'pct_static':float((m<0.35).mean()),
      'face_max':int(nc.max()),'face_mean':float(nc.mean()),
      'id_best':{k:float(np.mean(v)) if v else -1 for k,v in idd.items()}}
    print(f"{name}: f={f} drift_end={d[-1]:.2f} mot={m.mean():.2f} static%={(m<0.35).mean()*100:.0f} facemax={nc.max()}")
json.dump(report,open(os.path.join(OUT,'slop_structural.json'),'w'),indent=1)
print("WROTE",os.path.join(OUT,'slop_structural.json'))
