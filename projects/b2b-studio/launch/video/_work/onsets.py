import numpy as np, subprocess, sys
f=sys.argv[1]; sr=22050
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
hop=256;n=2048
fr=np.lib.stride_tricks.sliding_window_view(x,n)[::hop]*np.hanning(n)
S=np.log1p(10*np.abs(np.fft.rfft(fr,axis=1)))
fl=np.maximum(0,np.diff(S,axis=0)).sum(1); fl=np.concatenate([[0],fl]); fps=sr/hop
fl=fl/np.percentile(fl,99)
# local peaks above 0.5
pk=[i for i in range(2,len(fl)-2) if fl[i]>0.45 and fl[i]==fl[i-2:i+3].max()]
for a,b in [(3.5,5),(7.8,8.8),(11.5,13),(23.5,25),(32,34),(35.8,38),(41,43),(49,51.5),(57.5,59.5)]:
    print(a,b,' '.join('%.2f(%.2f)'%(i/fps,fl[i]) for i in pk if a<=i/fps<=b))
