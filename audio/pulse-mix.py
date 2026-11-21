"""Alternative soundtrack for the film: 'Pulse Voyage' (Chill Cole, Epidemic Sound). 103 bpm, bar 2.329 s.
  film 0:00-1:24 <- track 1:33.9-2:57.9 in one run (the track's quiet passage opens the film; the band enters with KODA at 0:18)
  film 1:24-1:30 <- two bars later, so the track's own ending closes the film
Run: ffmpeg -i audio/music-pulse-voyage.mp3 -f f32le -ar 48000 -ac 2 - | python audio/pulse-mix.py"""
import sys, numpy as np, wave
SR=48000; a=np.frombuffer(sys.stdin.buffer.read(),dtype='<f4').reshape(-1,2).astype(np.float64); BAR=4*0.58236; N=90*SR; out=np.zeros((N,2))
def lay(f0,f1,t0,fin,fout):
    n=int((f1-f0)*SR); nf=int(fin*SR); no=int(fout*SR); seg=a[int(t0*SR)-nf:int(t0*SR)+n+no].copy(); e=np.ones(len(seg))
    if nf: e[:nf]=np.sin(np.linspace(0,np.pi/2,nf))**2
    if no and len(seg)>no: e[-no:]=np.cos(np.linspace(0,np.pi/2,no))**2
    j=int(f0*SR)-nf; seg*=e[:,None]; s=max(0,-j); k=min(len(seg),N-j); out[j+s:j+k]+=seg[s:k]
lay(0,84,93.875,0,0.04); lay(84,90,177.875+2*BAR,0.04,0)
t=np.arange(N)/SR; out*=np.interp(t,[0,2.0,89.9,90],[0,1,1,0])[:,None]; out*=10**(-1.0/20)/np.abs(out).max()
w=wave.open('audio/pulse-film.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes()); w.close()
