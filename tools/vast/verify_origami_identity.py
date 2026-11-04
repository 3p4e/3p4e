import cv2, os, glob, numpy as np

CLIPS = '/a0/usr/projects/vast/media/origami_clips'
REF   = '/a0/usr/projects/vast/media/refs/A_bust.png'
YN    = '/a0/usr/projects/vast/tools/models/face_detection_yunet_2023mar.onnx'
SF    = '/a0/usr/projects/vast/tools/models/face_recognition_sface_2021dec.onnx'
MONSTER = {'or_01_corruption_revealed','or_04_stain_devours','or_10_final_unfold'}

det = cv2.FaceDetectorYN.create(YN, '', (544,960), 0.7, 0.3, 5000)
rec = cv2.FaceRecognizerSF.create(SF, '')

def embed_face_bgr(img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    if faces is None or len(faces) == 0:
        return None
    fc = max(faces, key=lambda f: f[2]*f[3])
    face = rec.alignCrop(img, fc)
    return rec.feature(face)

# reference embedding from A_bust.png
ref_img = cv2.imread(REF)
ref_emb = embed_face_bgr(ref_img)
print('REF A_bust.png face embedded:', ref_emb is not None)
ref_emb = ref_emb.flatten()

def cosim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

for f in sorted(glob.glob(CLIPS + '/or_*.mp4')):
    name = os.path.splitext(os.path.basename(f))[0]
    cap = cv2.VideoCapture(f)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sims, motions = [], []
    prev = None
    for t in (0.5, 1.3, 2.1, 2.9, 3.7):
        cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        ok, frame = cap.read()
        if not ok: continue
        small = cv2.resize(frame, (544, 960))
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            motions.append(float(np.mean(np.abs(g - prev))))
        prev = g
        if name not in MONSTER:
            e = embed_face_bgr(small)
            if e is not None:
                sims.append(cosim(e.flatten(), ref_emb))
    motion = float(np.mean(motions)) if motions else 0.0
    if name in MONSTER:
        print(f'{name}: MONSTER  motion={motion:.2f}  (no face expected)')
    else:
        mx = max(sims) if sims else 0.0
        mn = min(sims) if sims else 0.0
        print(f'{name}: faces_sim  max={mx:.3f} min={mn:.3f} n={len(sims)}  motion={motion:.2f}')
    cap.release()
