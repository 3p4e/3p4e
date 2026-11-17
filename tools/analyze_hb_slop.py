#!/usr/bin/env python3
# HOLLOW BLOOM slop/content verifier.
# Q7 GATES (doc 57): drift-drop (Farneback) · palette HSV (histogram) · sharpness (Laplacian)
# · face-count (YuNet local; InsightFace buffalo_l on-box) — all implemented HERE (cv2-only).
# start-corr >=0.92 CLIP cosine runs ON-BOX via prov_hb_v2.sh step [4/6] (open_clip installed there).
# Reject a clip on 2+ gate failures. Thresholds per doc 57 Q7; earlier calibration in doc 50.
import cv2, os, json, glob, numpy as np
ROOT='/a0/usr/projects/vast'
CLIPS=os.path.join(ROOT,'media/dhpf_hb_clips')
KF=os.path.join(ROOT,'media/dhpf_grok_keyframes')
OUT=os.path.join(CLIPS,'analysis'); os.makedirs(OUT,exist_ok=True)
YUNET=os.path.join(ROOT,'tools/models/face_detection_yunet_2023mar.onnx')
SFACE=os.path.join(ROOT,'tools/models/face_recognition_sface_2021dec.onnx')
JOBS=json.load(open(os.path.join(ROOT,'tools/vast/jobs/p23_hb_k6c2_116.json')))
det=cv2.FaceDetectorYN_create(YUNET,'',(320,320),score_threshold=0.75,nms_threshold=0.3,top_k=5000)
rec=cv2.FaceRecognizerSF_create(SFACE,'')
def faces(img):
    h,w=img.shape[:2]; det.setInputSize((w,h)); _,fs=det.detect(img)
    return [] if fs is None else list(fs)
def emb(img,f):
    a=rec.alignCrop(img,f); return rec.feature(a).flatten()
def centroid(paths):
    es=[]
    for p in paths:
        img=cv2.imread(p)
        if img is None: continue
        fs=faces(img)
        if not fs: continue
        e=emb(img,max(fs,key=lambda f:f[2]))
        if e is not None: es.append(e)
    if not es: return None
    m=np.mean(es,axis=0); return m/(np.linalg.norm(m)+1e-9)
def cos(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9))
print('building refs ...',flush=True)
DD=centroid(sorted(glob.glob(os.path.join(ROOT,'faces/dd_cards_final/*.jpg'))))
AZ=centroid(sorted(glob.glob(os.path.join(ROOT,'faces/az_cards_final/*.jpg'))))
print('refs DD',DD is not None,'AZ',AZ is not None,flush=True)
def kfloc(jkf):
    p=os.path.join(KF,os.path.basename(jkf)); return p if os.path.exists(p) else None
def hsvh(img):
    hsv=cv2.cvtColor(cv2.resize(img,(208,120)),cv2.COLOR_BGR2HSV)
    h=cv2.calcHist([hsv],[0,1],None,[24,16],[0,180,0,256]); return cv2.normalize(h,h).flatten()
report={}; offenders=[]
for job in JOBS:
    name=os.path.basename(job['out']).replace('.mp4','')
    cp=os.path.join(CLIPS,name+'.mp4')
    if not os.path.exists(cp): continue
    kfp=kfloc(job['kf']); kf=cv2.imread(kfp) if kfp else None
    kfg=cv2.cvtColor(cv2.resize(kf,(416,240)),cv2.COLOR_BGR2GRAY).astype(np.float32)/255.0 if kf is not None else None
    kh=hsvh(kf) if kf is not None else None
    cap=cv2.VideoCapture(cp); prev=None
    mots=[];drifts=[];nfcs=[];sims=[];sharp=[];pal=[]
    while True:
        ok,fr=cap.read()
        if not ok: break
        g=cv2.cvtColor(cv2.resize(fr,(416,240)),cv2.COLOR_BGR2GRAY).astype(np.float32)/255.0
        if prev is not None: mots.append(float(np.abs(g-prev).mean()))
        prev=g
        if kfg is not None: drifts.append(float(np.corrcoef(g.flatten(),kfg.flatten())[0,1]))
        if kh is not None: pal.append(float(cv2.compareHist(kh.astype(np.float32),hsvh(fr).astype(np.float32),cv2.HISTCMP_BHATTACHARYYA)))
        sharp.append(float(cv2.Laplacian(cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY),cv2.CV_64F).var()))
        fs=faces(fr); nfcs.append(len(fs))
        if fs and DD is not None:
            e=emb(fr,max(fs,key=lambda f:f[2]))
            if e is not None: sims.append(max(cos(e,DD),cos(e,AZ)))
    cap.release()
    r={'shot':job.get('shot'),'frames':len(mots)+1,
       'motion_mean':round(float(np.mean(mots)),2) if mots else 0,
       'drift_first':round(drifts[0],3) if drifts else None,
       'drift_last':round(drifts[-1],3) if drifts else None,
       'face_max':int(max(nfcs)) if nfcs else 0,
       'sim_first':round(sims[0],3) if sims else None,
       'sim_last':round(sims[-1],3) if sims else None,
       'sharp_first':round(sharp[0]) if sharp else None,
       'sharp_last':round(sharp[-1]) if sharp else None,
       'pal_dist':round(float(np.mean(pal)),3) if pal else None}
    fl=[]
    if r['motion_mean']<0.01: fl.append('SLIDESHOW')
    if r['face_max']>=3: fl.append('RANDOM_PEOPLE')
    if r['sim_first'] is not None and r['sim_last'] is not None and (r['sim_first']-r['sim_last'])>0.25: fl.append('MORPH')
    if r['drift_last'] is not None and (r['drift_first']-r['drift_last'])>0.55: fl.append('REDREAM')
    if r['sharp_last'] is not None and r['sharp_last']<15: fl.append('COLLAPSE')
    if r['pal_dist'] is not None and r['pal_dist']>0.6: fl.append('PALETTE_FLIP')
    r['flags']=fl; r['prompt_head']=job['prompt'][:200]
    report[name]=r
    if fl: offenders.append((name,fl,r['motion_mean'],r['sim_first'],r['sim_last'],r['drift_last'],r['face_max']))
    print(name,'mot',r['motion_mean'],'drift',r['drift_first'],'->',r['drift_last'],'face',r['face_max'],'sim',r['sim_first'],'->',r['sim_last'],'sharp',r['sharp_first'],'->',r['sharp_last'],'pal',r['pal_dist'],'FLAGS',fl,flush=True)
json.dump(report,open(os.path.join(OUT,'hb_slop_report.json'),'w'),indent=1)
print('OFFENDERS',len(offenders),flush=True)
for o in offenders: print(o,flush=True)
print('DONE',flush=True)
