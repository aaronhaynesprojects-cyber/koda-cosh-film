"""Alternative mock-up soundtrack: 'Harbours & Oceans' (Fictions, Epidemic Sound) cut to the film's 90 s.
About 58.7 bpm, bar 4.09 s; each splice jumps a whole number of bars.
  film 0:00-0:38 <- track 0:02-0:40      (its first lift, at 0:20, lands on KODA at 0:18)
  film 0:38-1:24 <- track 0:35.9-1:21.9  (one bar repeated, so the full arrangement arrives with the vision at 0:56)
  film 1:24-1:30 <- track 3:20.5-        (the last bar and the fade)"""
import sys, numpy as np, wave
SR=48000; a=np.frombuffer(sys.stdin.buffer.read(),dtype='<f4').reshape(-1,2).astype(np.float64); N=90*SR; out=np.zeros((N,2)); BAR=4.0904
def lay(f0,f1,t0,fin,fout):
    n=int((f1-f0)*SR); nf=int(fin*SR); no=int(fout*SR); seg=a[int(t0*SR)-nf:int(t0*SR)+n+no].copy(); e=np.ones(len(seg))
    if nf: e[:nf]=np.sin(np.linspace(0,np.pi/2,nf))**2
    if no: e[-no:]=np.cos(np.linspace(0,np.pi/2,no))**2
    j=int(f0*SR)-nf; seg*=e[:,None]; s=max(0,-j); k=min(len(seg),N-j); out[j+s:j+k]+=seg[s:k]
lay(0,38,2.0,0.0,0.25); lay(38,84,40.0-BAR,0.25,0.25); lay(84,90,40.0-BAR+46+29*BAR,0.25,0.0)
t=np.arange(N)/SR; out*=np.interp(t,[0,1.5,86.5,89.9,90],[0,1,1,0,0])[:,None]; out*=10**(-1.2/20)/np.abs(out).max()
w=wave.open('audio/alt-mix-harbours.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes()); w.close()
