import cv2, os, glob, numpy as np

CLIPS = '/a0/usr/projects/vast/media/origami_clips'
MODEL = '/a0/usr/projects/vast/tools/models/face_detection_yunet_2023mar.onnx'
MONSTER = {'or_01_corruption_revealed', 'or_04_stain_devours', 'or_10_final_unfold'}
HERO = {'or_02_hunter_descends','or_03_thousand_cranes','or_05_tar_tide','or_06_blade_splits_tide',
        'or_07_colossus_against_cathedral','or_09_thousandfold_dawn','or_11_spear_pierce'}
CLASH = {'or_08_sphere_of_annihilation','or_12_annihilation_ascension'}

os.makedirs('/a0/usr/projects/vast/media/origami_clips/_verify', exist_ok=True)
det = cv2.FaceDetectorYN.create(MODEL, '', (544, 960), 0.7, 0.3, 5000)

for f in sorted(glob.glob(CLIPS + '/or_*.mp4')):
    name = os.path.splitext(os.path.basename(f))[0]
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for t in (0.8, 1.8, 3.2):
        cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        ok, frame = cap.read()
        if not ok: continue
        fr = cv2.resize(frame, (544, 960))
        det.setInputSize((544, 960))
        _, faces = det.detect(fr)
        nf = 0 if faces is None else len(faces)
        big = 0.0
        if faces is not None and len(faces):
            for fc in faces:
                big = max(big, float(fc[2])*float(fc[3]))
        print(f'{name}  t={t:.1f}s  faces={nf}  max_face_area={big:.0f}px')
    cap.release()
