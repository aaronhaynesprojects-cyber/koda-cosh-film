"""Soundtrack alternative: 'Friction (Instrumental Version)' (Saarah, Epidemic Sound). 103 bpm, bar 2.3301 s, hard stop at 2:27.25.
  film: 0:00-0:17.1 <- track 1:29.75-1:46.85 (the end of its quiet break and the build; the band enters at 0:17.1 with the Era switch-on, as Rocket Jr does)
        0:17.1-1:24.7 <- track 0:13.65-1:21.2 (the main section; its calmer passage arrives at about 1:13, under the closing rooms)
        1:24.7-1:30 <- track 2:21.8-2:27.1 (the last bars, so the track's own final hit ends the film)
  Every join is on a bar line of the track's own grid (first downbeat 0:02.0), so the beat runs on through each one.
Run: ffmpeg -i audio/music-friction-saarah.mp3 -f f32le -ar 48000 -ac 2 - | python audio/friction-mix.py"""
import sys, numpy as np, wave
SR = 48000; a = np.frombuffer(sys.stdin.buffer.read(), dtype="<f4").reshape(-1, 2).astype(np.float64); BAR = 240 / 103
G = 2.0                                     # first downbeat; bar k starts at G + k * BAR
bar = lambda k: G + k * BAR
SW = 17.1                                   # film time of the Era switch-on (8 Rocket Jr bars), where the band should enter
A = bar(45) - SW                            # bar 45 (1:46.85) is where the full section comes back in after the quiet break
B = bar(5) - SW                             # main section from bar 5 (0:13.65), so its calmer passage (bar 29, 1:09.6) falls at film 1:13
c = B + 26 * BAR                            # last part: bar 60 onwards, the final hit (bar 62) rings out by film 1:30
F = bar(34) - B                             # join into the ending on a bar line, about film 1:24.7
def build(name, dur, parts, fadein, xf=0.04):
    N = int(dur * SR); out = np.zeros((N, 2))
    for f0, f1, off in parts:
        t0 = f0 + off; nf = int(xf * SR) if f0 > 0 else 0; no = int(xf * SR) if f1 < dur else 0; n = int((f1 - f0) * SR)
        seg = a[int(t0 * SR) - nf:int(t0 * SR) + n + no].copy(); e = np.ones(len(seg))
        if nf: e[:nf] = np.sin(np.linspace(0, np.pi / 2, nf)) ** 2
        if no: e[-no:] = np.cos(np.linspace(0, np.pi / 2, no)) ** 2
        j = int(f0 * SR) - nf; seg *= e[:, None]; s = max(0, -j); k = min(len(seg), N - j); out[j + s:j + k] += seg[s:k]
    t = np.arange(N) / SR; out *= np.interp(t, [0, fadein, dur - 0.05, dur], [0, 1, 1, 0])[:, None]; out *= 10 ** (-1.0 / 20) / np.abs(out).max()
    w = wave.open(name, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype("<i2").tobytes()); w.close()
    print(name, [(f0, f1, round(f0 + off, 2)) for f0, f1, off in parts])
build("audio/friction-film.wav", 90, [(0, SW, A), (SW, F, B), (F, 90, c)], 1.0)
