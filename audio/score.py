"""Original score for KODA AT COSH LIVING — synthesised here, so there is nothing to license.
120 bpm from 0:18; chord changes sit on the edit. Run: ~/Developer/.asr-venv/bin/python audio/score.py"""
import numpy as np, wave
SR=48000; DUR=90.0; N=int(SR*DUR); rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N); wetL=np.zeros(N); wetR=np.zeros(N)
hz=lambda m: 440*2**((m-69)/12)
def add(buf_l,buf_r,sig,t,pan=0.0,g=1.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0 or i<0: return
    buf_l[i:i+n]+=sig[:n]*g*np.sqrt((1-pan)/2); buf_r[i:i+n]+=sig[:n]*g*np.sqrt((1+pan)/2)
def env(n,a,r):
    e=np.ones(n); na=int(a*SR); nr=int(r*SR)
    e[:na]=np.sin(np.linspace(0,np.pi/2,na))**2; e[-nr:]*=np.cos(np.linspace(0,np.pi/2,nr))**2; return e
CH={'Dm9':(38,[57,60,64,65]),'Bb':(34,[57,62,65,69]),'F':(41,[57,60,64,67]),'C':(36,[55,57,62,64]),'D':(38,[57,62,64,66])}
T=[0,4.5,9,13.5,18,22,26,29,32,35,38,41,44,47,50,53,56,60,64,68,72,75,78,81,84]
SEQ=['Dm9','Bb','F','C']; chords=[(T[i],(T[i+1] if i+1<len(T) else DUR),SEQ[i%4] if i<24 else 'D') for i in range(len(T))]
lvl=lambda t: np.interp(t,[0,3,18,26,56,58,84,90],[0.0,0.55,0.62,0.74,0.86,1.0,1.0,0.9])
for t0,t1,name in chords:                                   # pad: soft additive voices, each detuned left/right
    bass,notes=CH[name]; d=t1-t0+1.6; n=int(d*SR); tt=np.arange(n)/SR; e=env(n,1.5,1.6)
    for k,m in enumerate(notes+([notes[0]+12,notes[2]+12] if t0>=56 else [])):
        for det,pan in ((-0.07,-0.6),(0.07,0.6)):
            f=hz(m+det); v=np.sin(2*np.pi*f*tt+rng.uniform(0,6))+0.32*np.sin(2*np.pi*2*f*tt+rng.uniform(0,6))+0.10*np.sin(2*np.pi*3*f*tt)
            v*=1+0.12*np.sin(2*np.pi*(0.11+0.03*k)*tt+k)
            add(L,R,v*e,t0-0.7 if t0>0 else 0,pan,0.030*lvl(t0)); add(wetL,wetR,v*e,t0-0.7 if t0>0 else 0,-pan,0.018*lvl(t0))
    if t0>=18:                                              # sub bass
        f=hz(bass); b=(np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt))*env(n,0.25,1.4)
        add(L,R,b,t0,0,np.interp(t0,[18,26,56,84],[0.05,0.10,0.17,0.17]))
def pluck(m,d=0.9,bright=0.3):
    n=int(d*SR); tt=np.arange(n)/SR; f=hz(m)
    return (np.sin(2*np.pi*f*tt)+bright*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*9)+0.12*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*14))*np.exp(-tt*4.2)*np.minimum(1,tt*400)
def bell(m,d=3.2):
    n=int(d*SR); tt=np.arange(n)/SR; f=hz(m)
    return (np.sin(2*np.pi*f*tt)+0.4*np.sin(2*np.pi*2.01*f*tt)*np.exp(-tt*2)+0.2*np.sin(2*np.pi*3.02*f*tt)*np.exp(-tt*4))*np.exp(-tt*1.5)*np.minimum(1,tt*200)
def chord_at(t):
    for t0,t1,name in chords:
        if t0<=t<t1: return CH[name][1]
PAT=[0,2,1,3,2,1,3,2]
t=18.0;k=0
while t<84:                                                 # eighth-note arpeggio, an octave above the pad
    notes=chord_at(t); m=notes[PAT[k%8]%len(notes)]+12+(12 if (k%16 in (6,14) and t>=44) else 0)
    g=np.interp(t,[18,26,44,56,58,82,84],[0.0,0.040,0.058,0.062,0.078,0.078,0.03])*(1.0 if k%2==0 else 0.72)
    p=pluck(m); pan=0.45*np.sin(k*0.9); add(L,R,p,t,pan,g); add(wetL,wetR,p,t,-pan,g*0.8); add(wetL,wetR,p,t+0.375,-pan,g*0.35)
    t+=0.25;k+=1
def kick():
    n=int(0.36*SR); tt=np.arange(n)/SR; ph=2*np.pi*(44*tt+(62/22)*(1-np.exp(-tt*22))); return np.sin(ph)*np.exp(-tt*10)*np.minimum(1,tt*500)
t=26.0
while t<84:                                                 # a soft pulse, never a drum kit
    add(L,R,kick(),t,0,np.interp(t,[26,32,56,58,84],[0.10,0.20,0.22,0.30,0.30]))
    if t>=56: add(L,R,kick(),t+0.75,0,0.10)
    t+=1.0
t=32.0;k=0
while t<84:                                                 # shaker: short high noise ticks
    n=int(0.07*SR); s=np.diff(rng.standard_normal(n+2),2)*np.exp(-np.arange(n)/SR*70)
    g=np.interp(t,[32,44,56,84],[0.004,0.009,0.013,0.013])*(1.0 if k%4==2 else 0.45); add(L,R,s,t,0.3 if k%2 else -0.3,g); t+=0.25;k+=1
for tb,m,g in [(3.4,81,0.05),(7.6,76,0.045),(12.9,81,0.07),(15.4,84,0.045),(59.9,86,0.06),(64.8,88,0.06),(70.2,81,0.06),(84.0,78,0.07),(84.0,90,0.05)]:
    b=bell(m); add(L,R,b,tb,0.2,g*0.6); add(wetL,wetR,b,tb,-0.2,g)        # light arriving
def swell(t1,d,g):                                          # an air swell into each new chapter
    n=int(d*SR); x=rng.standard_normal(n); y=np.cumsum(x-np.mean(x)); y=np.diff(np.concatenate([[0],np.convolve(x,np.ones(40)/40,'same')]))
    e=np.linspace(0,1,n)**3; s=np.convolve(x,np.ones(24)/24,'same')*e; add(wetL,wetR,s,t1-d,0,g); add(L,R,s,t1-d,0,g*0.4)
swell(18,2.2,0.035); swell(26,1.6,0.03); swell(56,2.6,0.06); swell(84,2.0,0.04)
air=np.convolve(rng.standard_normal(N),np.ones(60)/60,'same')*np.interp(np.arange(N)/SR,[0,2,16,20],[0,0.02,0.02,0.0]); L+=air; R+=np.roll(air,900)
# reverb: convolve the send with decaying noise
n=int(3.2*SR); tt=np.arange(n)/SR
def ir(): x=rng.standard_normal(n)*np.exp(-tt*1.9); x=np.convolve(x,np.ones(6)/6,'same'); x[:int(0.012*SR)]=0; return x/np.sqrt(np.sum(x*x))
def conv(a,h): m=1<<int(np.ceil(np.log2(len(a)+len(h)))); return np.fft.irfft(np.fft.rfft(a,m)*np.fft.rfft(h,m),m)[:len(a)]
L+=conv(wetL,ir())*1.7; R+=conv(wetR,ir())*1.7
tt=np.arange(N)/SR; fade=np.interp(tt,[0,1.2,87.6,89.9,90],[0,1,1,0,0]); L*=fade; R*=fade
pk=max(np.abs(L).max(),np.abs(R).max()); L=np.tanh(L/pk*1.25)/np.tanh(1.25); R=np.tanh(R/pk*1.25)/np.tanh(1.25)
out=(np.stack([L,R],1)*0.89*32767).astype('<i2')
w=wave.open('audio/score.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
rms=lambda a,b: 20*np.log10(np.sqrt(np.mean(L[int(a*SR):int(b*SR)]**2))+1e-9)
print('rms dB', [round(rms(a,b),1) for a,b in ((1,9),(9,18),(18,26),(26,56),(56,84),(84,89))])
