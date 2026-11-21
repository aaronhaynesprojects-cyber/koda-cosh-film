"""Make a 'lights off' plate from a lit dusk/night image, for the BEFORE half of a darkness-to-light reveal.
Finds emitted light (bright and warm, or bright pool/water light), switches it off by filling those areas from
their dusk surroundings, removes the warm spill it threw on nearby surfaces, and drops the ambient by `stops`.
Writes <out>-off.jpg, <out>-on.jpg (same framing) and <out>-mask.png (where the light was).
Usage: python tools/lightsoff.py <in.jpg> <out-prefix> [width=1920] [stops=1.2]"""
import sys, subprocess, numpy as np
def _box(a, r, axis):
    r = max(1, int(r)); a = np.swapaxes(a, 0, axis); p = np.pad(a, [(r + 1, r)] + [(0, 0)] * (a.ndim - 1), mode="edge")
    c = np.cumsum(p, axis=0); out = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1); return np.swapaxes(out[: a.shape[0]], 0, axis)
def gaussian_filter(a, s):            # three box passes per axis approximate a gaussian of sigma s
    r = max(1, int(round(s * 0.87)))
    for _ in range(3): a = _box(_box(a, r, 0), r, 1)
    return a
def binary_dilation(m, iterations=1):
    return gaussian_filter(m.astype(float), iterations / 1.7) > 0.02
src, out = sys.argv[1], sys.argv[2]; W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920; stops = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
w, h = [int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.split(",")]
H = round(h * W / w / 2) * 2
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
img = np.frombuffer(raw, "<u2").reshape(H, W, 3).astype(np.float64) / 65535
lin = img ** 2.2
L = lin @ [0.2126, 0.7152, 0.0722]; R, G, B = lin[..., 0], lin[..., 1], lin[..., 2]
amb = gaussian_filter(L, W / 40)
warm = (R - B) / (L + 1e-4)
emit = ((L > np.maximum(amb * 1.8, 0.012)) & (warm > 0.25)) | ((L > np.maximum(amb * 2.5, 0.05)) & (B > R * 1.2) & (np.arange(H)[:, None] > H * 0.45))
emit = binary_dilation(emit, iterations=max(2, W // 640))
m = np.clip(gaussian_filter(emit.astype(float), W / 900) * 1.6, 0, 1)
# switch the sources off by pulling each lit pixel down to the ambient around it, keeping its texture;
# warm hue drains to a neutral dusk tone as it falls (an unlit window shows the cool sky, not orange)
target = np.maximum(amb * 0.9, 1e-4)
ratio = np.clip(target / (L + 1e-6), 0.04, 1.0)
k = 1 - m * (1 - ratio)
grey = L[..., None] * np.array([0.8, 0.9, 1.1])
off = lin * k[..., None]
off = off * (1 - 0.7 * m[..., None]) + grey * k[..., None] * 0.7 * m[..., None]
# warm spill the sources threw on nearby surfaces
spill = gaussian_filter(m * np.clip(L / (L.max() + 1e-6), 0, 1), W / 45); spill = spill / (spill.max() + 1e-6)
off = off * (1 - 0.55 * spill[..., None] * np.array([1.0, 0.85, 0.4]))
off = off * 2 ** (-stops) * np.array([0.86, 0.94, 1.12])          # dusk ambient, a touch cooler
def save(a, p):
    a = np.clip(a, 0, 1) ** (1 / 2.2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-i", "-", "-q:v", "2", p], input=(a * 65535).astype("<u2").tobytes())
save(off, out + "-off.jpg"); save(lin, out + "-on.jpg")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-i", "-", out + "-mask.png"], input=(m * 255).astype(np.uint8).tobytes())
print(out, f"{W}x{H}", f"lit area {m.mean()*100:.1f}%")
