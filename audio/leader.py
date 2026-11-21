"""Prepend the 3 s leader to a mix: silence, with a 1 kHz beep on the "1". Sets the level to a target RMS-based gain.
Usage: python audio/leader.py in.wav out.wav gain_dB"""
import sys, numpy as np, wave
w=wave.open(sys.argv[1]); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float64)/32768*10**(float(sys.argv[3])/20)
lead=np.zeros((3*sr,2)); n=int(0.12*sr); t=np.arange(n)/sr; b=0.25*np.sin(2*np.pi*1000*t)*np.minimum(1,np.minimum(t,0.12-t)*400); lead[2*sr:2*sr+n]+=b[:,None]
y=np.concatenate([lead,x]); o=wave.open(sys.argv[2],'wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr); o.writeframes((np.clip(y,-1,1)*32767).astype('<i2').tobytes()); o.close()
