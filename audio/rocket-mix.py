"""Soundtrack: 'Rocket Jr' (Mustard, Epidemic Sound). 112 bpm, bar 2.1437 s.
  film:   0:00-1:24 <- track 0:38.25-2:02.25 in one run (its quiet passage opens the film, the band enters with KODA at 0:18,
                       the calmer passage arrives with the closing rooms at 1:14); 1:24-1:30 <- the last 2.5 bars, so the track's own hard stop ends the film.
  broll:  the last 28 bars of the track, so the reel ends on the same hard stop at 1:00.
Run: ffmpeg -i audio/music-rocket-jr.mp3 -f f32le -ar 48000 -ac 2 - | python audio/rocket-mix.py"""
import sys, numpy as np, wave
SR=48000; a=np.frombuffer(sys.stdin.buffer.read(),dtype='<f4').reshape(-1,2).astype(np.float64); BAR=2.14367
def build(name,dur,parts,fadein):
    N=int(dur*SR); out=np.zeros((N,2))
    for f0,f1,t0,fin,fout in parts:
        n=int((f1-f0)*SR); nf=int(fin*SR); no=int(fout*SR); seg=a[int(t0*SR)-nf:int(t0*SR)+n+no].copy(); e=np.ones(len(seg))
        if nf: e[:nf]=np.sin(np.linspace(0,np.pi/2,nf))**2
        if no and len(seg)>no: e[-no:]=np.cos(np.linspace(0,np.pi/2,no))**2
        j=int(f0*SR)-nf; seg*=e[:,None]; s=max(0,-j); k=min(len(seg),N-j); out[j+s:j+k]+=seg[s:k]
    t=np.arange(N)/SR; out*=np.interp(t,[0,fadein,dur-0.05,dur],[0,1,1,0])[:,None]; out*=10**(-1.0/20)/np.abs(out).max()
    w=wave.open(name,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes()); w.close()
build('audio/rocket-film.wav',90,[(0,84,38.25,0,0.04),(84,90,122.25+25*BAR,0.04,0)],1.6)
build('audio/rocket-broll.wav',62,[(0,62,181.0-28*BAR,0,0)],1.0)
build('audio/rocket-croll.wav',37,[(0,37,56.25-8*BAR,0,0)],0.9)   # C-roll: eight quiet bars, eight fuller, out on the track's own break
