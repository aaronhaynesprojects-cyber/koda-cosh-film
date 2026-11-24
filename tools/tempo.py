"""Estimate tempo and beat phase of a track with numpy only: onset envelope (spectral flux) -> autocorrelation for BPM,
then the beat-grid phase that best matches onsets; reports first strong downbeat and section changes (RMS jumps).
  python tools/tempo.py <audio> [max_seconds]"""
import sys, subprocess, numpy as np
f = sys.argv[1]; T = float(sys.argv[2]) if len(sys.argv) > 2 else 120
sr = 22050
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-t", str(T), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
hop, n = 512, 2048
frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
S = np.log1p(np.abs(np.fft.rfft(frames, axis=1)))
flux = np.maximum(0, np.diff(S, axis=0)).sum(1); flux = (flux - flux.mean()) / (flux.std() + 1e-9)
fps = sr / hop
ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
lags = np.arange(len(ac)); bpm = 60 * fps / np.maximum(lags, 1)
ok = (bpm > 70) & (bpm < 180); best = lags[ok][np.argmax(ac[ok])]
# refine with parabolic interpolation
y0, y1, y2 = ac[best - 1], ac[best], ac[best + 1]; best_f = best + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
BPM = 60 * fps / best_f; period = fps * 60 / BPM
phases = np.linspace(0, period, 64, endpoint=False)
scores = [flux[np.clip((p + period * np.arange(int(len(flux) / period) - 1)).astype(int), 0, len(flux) - 1)].sum() for p in phases]
ph = phases[int(np.argmax(scores))] / fps
rms = np.sqrt((frames ** 2).mean(1)); sec = len(rms) / (len(x) / sr)
print(f"BPM {BPM:.2f}  beat {60 / BPM:.4f} s  bar {240 / BPM:.4f} s  first beat {ph:.3f} s")
# loudness profile per bar to find intro/drop
bar = 240 / BPM; t = ph; out = []
while t + bar < len(x) / sr:
    a, b = int(t * sec), int((t + bar) * sec); out.append(20 * np.log10(rms[a:b].mean() + 1e-9)); t += bar
print("bar dB:", " ".join(f"{i}:{v:.0f}" for i, v in enumerate(out)))
