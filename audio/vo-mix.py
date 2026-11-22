"""Narrated soundtrack: places each spoken line on its shot and ducks the music under it.
Usage: python audio/vo-mix.py <marie|mike> <music-mix.wav> <out.wav> [lead]   (lead = prepend the 3 s countdown with its beep)
The recording is split at its own pauses (word timings from faster-whisper, audio/vo-<name>.words.json)."""
import sys, json, subprocess, numpy as np, wave
voice, music, outp = sys.argv[1:4]; LEAD = "lead" in sys.argv[4:]; NONAME = "noname" in sys.argv[4:]; SR = 48000
# noname: both reads spell the name out letter by letter, so this drops "KODA's" from line 11 and the whole of line 18 (the end card shows the name instead)
# programme time each line starts at, in the order spoken
AT = [1.5, 5.6, 11.8, 26.5, 32.5, 38.5, 44.5, 50.6, 54.0, 56.6, 60.0, 63.9, 69.3, 72.1, 75.4, 78.3, 81.2, 85.4, 87.6]
# "best": the best-of cut (v=best). Same read, lines moved onto their pictures: "sculpted in glass" on the Lodes glass globes, "drawn in shadow"
# on Arkoslight, "the smallest detail" on Uma Mini, "KODA's passion" on KODA's own showroom film, "Cosh Living's understanding" on DEDON's Dala terrace,
# "One shared vision" on the Potocco pavilion
if "best" in sys.argv[4:]: AT = [1.5, 5.6, 11.8, 26.5, 30.4, 36.8, 43.3, 50.6, 54.0, 56.6, 60.5, 64.8, 69.3, 73.4, 75.8, 78.3, 81.2, 85.4, 87.6]
raw = subprocess.run(["ffmpeg","-v","error","-i",f"audio/vo-{voice}.mp3","-f","f32le","-ar",str(SR),"-ac","1","-"],capture_output=True).stdout
v = np.frombuffer(raw, dtype="<f4").astype(np.float64)
# the script's lines, by word count, so a read with a short pause still splits in the right places
COUNTS = [7, 6, 4, 5, 3, 3, 5, 7, 3, 6, 5, 6, 3, 3, 4, 4, 5, 4, 3]
raw_words = json.load(open(f"audio/vo-{voice}.words.json")); words = []
for w in raw_words:   # a spelled-out name arrives as "K", ".O", ".D", ".A." — count it as one word
    if w[2].startswith(".") and words: words[-1] = [words[-1][0], w[1], words[-1][2] + w[2]]
    else: words.append(list(w))
ph = []; k0 = 0
for c in COUNTS: ph.append(words[k0:k0 + c]); k0 += c
if k0 < len(words): ph[-1] += words[k0:]
assert len(ph) == len(AT) and all(ph), (len(ph), len(AT))
last = ph[-1]; k = max(i for i, w in enumerate(last) if "possible" in w[2].lower()); ph[-1] = last[:k + 1]   # one read repeats the name after the last line
# snap each line to the real pauses in the recording (word timings alone can run two lines together)
hop = SR // 20; db = [20 * np.log10(np.sqrt(np.mean(v[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(v) - hop, hop)]; sil = []; s0 = None
for i, d in enumerate(db + [0]):
    if d < -45 and s0 is None: s0 = i
    if d >= -45 and s0 is not None:
        if (i - s0) / 20 >= 0.3: sil.append((s0 / 20, i / 20))
        s0 = None
cuts = [sil[0] if sil and sil[0][0] < 0.1 else (0.0, ph[0][0][0])]
for i in range(len(ph) - 1):
    mid = (ph[i][-1][1] + ph[i + 1][0][0]) / 2; c = [x for x in sil if ph[i][0][0] + 0.2 < (x[0] + x[1]) / 2 < ph[i + 1][-1][1] - 0.2]
    cuts.append(min(c, key=lambda x: abs((x[0] + x[1]) / 2 - mid)) if c else (ph[i][-1][1], ph[i + 1][0][0]))
cuts.append((ph[-1][-1][1] + 0.1, len(v) / SR)); tail = [x for x in sil if x[0] > ph[-1][0][0] + 0.3]
if tail: cuts[-1] = tail[0]
w = wave.open(music); m = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2).astype(np.float64) / 32768; N = len(m)
vo = np.zeros(N); duck = np.zeros(N)
act = np.concatenate([v[int(cuts[i][1]*SR):int(cuts[i+1][0]*SR)] for i in range(len(ph))]); vg = 10 ** (-20 / 20) / np.sqrt(np.mean(act ** 2))   # speech at about -20 dBFS RMS
for i, (p, at) in enumerate(zip(ph, AT)):
    a = cuts[i][1] - 0.12; b = cuts[i + 1][0] + 0.30
    if NONAME and i == 17: continue
    if NONAME and i == 18: at = 86.3
    if NONAME and i == 10:   # cut in at the quietest instant between the name and "passion"
        k = [j for j, w_ in enumerate(p) if "passion" in w_[2].lower()][0]; c = p[k][0]; lo = int((c - 0.14) * SR); hop = int(0.004 * SR)
        en = [np.sqrt(np.mean(v[lo + j * hop: lo + j * hop + 2 * hop] ** 2)) for j in range(int(0.24 * SR / hop))]; a = (lo + int(np.argmin(en)) * hop) / SR - 0.004; p = p[k:]; print("   name cut at", round(a, 3), "level", round(20 * np.log10(min(en) + 1e-9), 1), "dB")
    seg = v[int(a*SR):int(b*SR)].copy() * vg; n = len(seg); e = np.ones(n); f = int(0.03*SR); e[:f] = np.linspace(0, 1, f); e[-f:] = np.linspace(1, 0, f); seg *= e
    j = int((at - (0.0 if NONAME and i == 10 else 0.12)) * SR); n = min(n, N - j); vo[j:j+n] += seg[:n]; duck[max(0, j - int(0.1*SR)):j + n + int(0.25*SR)] = 1
    print(f"{at:6.2f}-{at - 0.12 + n/SR:6.2f}  {' '.join(x[2] for x in p)}")
k = int(0.45 * SR); duck = np.convolve(duck, np.hanning(k) / np.hanning(k).sum(), "same")   # smooth ramps into and out of each line
mg = 10 ** (-19.5 / 20) / np.sqrt(np.mean(m ** 2) + 1e-12)                                   # music bed
out = m * mg * (1 - 0.62 * duck)[:, None] + vo[:, None]
out = np.tanh(out * 1.15) / np.tanh(1.15) * 0.97 if np.abs(out).max() > 0.97 else out
if LEAD:
    lead = np.zeros((3 * SR, 2)); n = int(0.12 * SR); t = np.arange(n) / SR; lead[2*SR:2*SR+n] += (0.25 * np.sin(2*np.pi*1000*t) * np.minimum(1, np.minimum(t, 0.12 - t) * 400))[:, None]; out = np.concatenate([lead, out])
o = wave.open(outp, "wb"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(out, -1, 1) * 32767).astype("<i2").tobytes()); o.close()
