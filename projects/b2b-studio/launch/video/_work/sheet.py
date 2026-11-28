import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; W=sys.argv[2]
clips=sorted(glob.glob(S+'/ltx25/br_c0[3-9]*.mp4')+glob.glob(S+'/ltx25/br_c1[0-2]*.mp4'))+sorted(glob.glob(S+'/ltx25/tl_*.mp4'))+sorted(glob.glob(S+'/ltx25/st_*.mp4'))+sorted(glob.glob(S+'/ltx610/x_*.mp4'))+sorted(glob.glob(S+'/ltx610/tl2_*.mp4'))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
tw,th=300,165
rows=[]
for c in clips:
    n=os.path.basename(c)[:-4]
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',c]))
    ims=[]
    for i,t in enumerate([0.3,d/2,d-0.3]):
        o=f'{W}/sheet/fr/{n}_{i}.jpg'
        if not os.path.exists(o):
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',c,'-frames:v','1','-vf',f'scale={tw}:{th}',o])
        ims.append(Image.open(o))
    rows.append((n,ims))
per=20
for p in range(0,len(rows),per):
    chunk=rows[p:p+per]
    # 2 clips per row
    cols=2
    nr=(len(chunk)+1)//2
    sheet=Image.new('RGB',(cols*(3*tw+20),nr*(th+24)),'black')
    dr=ImageDraw.Draw(sheet)
    for k,(n,ims) in enumerate(chunk):
        x0=(k%2)*(3*tw+20); y0=(k//2)*(th+24)
        dr.text((x0+4,y0+2),n,fill='yellow',font=font)
        for i,im in enumerate(ims): sheet.paste(im,(x0+i*tw,y0+22))
    sheet.save(f'{W}/sheet/sheet_{p//per}.jpg',quality=80)
    print(f'{W}/sheet/sheet_{p//per}.jpg')
