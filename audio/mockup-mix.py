"""Mock-up soundtrack: 'Out To The World' (Zeroing, Epidemic Sound) cut to the film's 90 s.
The track runs at 80 bpm, so a bar is 3.0 s and every splice below jumps a whole number of bars.
  film 0:00-0:56  <- track 0:06-1:02   (its first lift, at 0:32, lands on the collection at 0:26)
  film 0:56-1:24  <- track 1:26-1:54   (two quiet seconds over the genuine showroom, second lift at 0:58)
  film 1:24-1:30  <- track 3:12-       (the final chord, ringing out under the end card)
Run: ffmpeg -i audio/mockup-music-out-to-the-world.mp3 -f f32le -ar 48000 -ac 2 - | python audio/mockup-mix.py"""
import sys, numpy as np, wave
SR=48000; a=np.frombuffer(sys.stdin.buffer.read(),dtype='<f4').reshape(-1,2).astype(np.float64)
N=90*SR; out=np.zeros((N,2))
def lay(film0,film1,track0,fin,fout):
    n=int((film1-film0)*SR); i=int(film0*SR); seg=a[int(track0*SR)-int(fin*SR):int(track0*SR)+n+int(fout*SR)].copy()
    e=np.ones(len(seg)); nf=int(fin*SR); no=int(fout*SR)
    if nf: e[:nf]=np.sin(np.linspace(0,np.pi/2,nf))**2
    if no: e[-no:]=np.cos(np.linspace(0,np.pi/2,no))**2
    j=i-nf; seg*=e[:,None]; s=max(0,-j); k=min(len(seg),N-j); out[j+s:j+k]+=seg[s:k]
lay(0,56,6.0,0.0,0.30); lay(56,84,86.0,0.30,0.03); lay(84,90,192.0,0.03,0.0)
t=np.arange(N)/SR; out*=np.interp(t,[0,1.5,87.2,89.9,90],[0,1,1,0,0])[:,None]
out*=10**(-1.2/20)/np.abs(out).max()
w=wave.open('audio/mockup-mix.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes()); w.close()
