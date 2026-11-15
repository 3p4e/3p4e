import shutil, hashlib, os, json

V='/a0/usr/projects/vast/'
U='/a0/usr/uploads/'
dest=V+'media/perseus_assets/'
pend=dest+'_p1_pending/'
os.makedirs(pend, exist_ok=True)

receipt={'cast_sheets_2026-11-13':{}