"""Hero shot plates from DEDON's own lake-house render (Secret Lakeside, night): nothing is drawn into the house or the landscape.
From the original it writes, in src/hero/ (2560 x 1440, the 16:9 band original y 380-3755: peaks, moon, house and its whole reflection):
  on.jpg       DEDON's render with its moon (and the moon's reflection) lifted out, so the moon can rise
  off.jpg      the same with the house lights switched off (the lightsoff.py method, without the global darkening)
  light1-4.png the light each group of lamps adds (on - off), grouped left to right; the reflections go with their lamps
  sky.png      alpha matte of the sky above the ridge and treeline; stars.png the same with the clouds held out
  lake.png     alpha matte of the water
  moon.png     the moon and its halo (original minus the fill), drawn back with "lighter" as it rises
  hero.json / meta.js  positions: the moon, its lift radius, the treeline under it, the light groups, the waterline
Adding off + all four light layers + the moon at its original place gives DEDON's render back.
Usage: python tools/heroprep.py"""
import json, subprocess, numpy as np, os
SRC = "assets/manufacturer-source/dedon/originals/dedon-secret-lakeside-house-night.jpg"; OUT = "src/hero"; os.makedirs(OUT, exist_ok=True)
W, H = 2560, 1440; Y0, Y1 = 380, 3755
def _box(a, r, axis):
    r = max(1, int(r)); a = np.swapaxes(a, 0, axis); p = np.pad(a, [(r + 1, r)] + [(0, 0)] * (a.ndim - 1), mode="edge")
    c = np.cumsum(p, axis=0); out = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1); return np.swapaxes(out[: a.shape[0]], 0, axis)
def blur(a, s):
    r = max(1, int(round(s * 0.87)))
    for _ in range(3): a = _box(_box(a, r, 0), r, 1)
    return a
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"crop=6000:{Y1 - Y0}:0:{Y0},scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
img = np.frombuffer(raw, "<u2").reshape(H, W, 3).astype(np.float64) / 65535          # sRGB 0-1
L = img @ [0.2126, 0.7152, 0.0722]

# ---- the moon first, so the sky walk does not mistake it for the ridge
def blob(cx, cy, r):
    win = L[cy - r:cy + r, cx - r:cx + r]; thr = win.max() * 0.85; ys, xs = np.nonzero(win > thr)
    return int(xs.mean() + cx - r), int(ys.mean() + cy - r), float(np.sqrt(len(xs) / np.pi))
mx, my, mr = blob(465, 456, 90)
# ---- sky matte: walk down each column from the top; the sky changes colour gradually (clouds, gradient),
# the ridge, snow and treeline arrive as an abrupt jump away from the running sky colour
ridge = np.zeros(W, int); sm = blur(img, 1.0)
for x in range(W):
    ref = sm[2, x].copy(); hit = 0; r = H // 2
    inmoon = abs(x - mx) < mr * 3.4
    for y in range(3, int(H * 0.62)):
        if inmoon and abs(y - my) < mr * 3.4: continue
        d = np.abs(sm[y, x] - ref).sum()
        if d > 0.16: hit += 1
        else: hit = 0; ref = ref * 0.7 + sm[y, x] * 0.3
        if hit >= 3: r = y - 3; break
    ridge[x] = r
ridge = np.minimum(ridge, int(H * 0.62))
med = np.array([np.median(ridge[max(0, x - 15):x + 16]) for x in range(W)]); ridge = np.minimum(ridge, med + 6).astype(int)   # no downward spikes
mx7 = np.array([ridge[max(0, x - 3):x + 4].max() for x in range(W)]); ridge = np.array([mx7[max(0, x - 3):x + 4].min() for x in range(W)])   # no hairline upward spikes
m1, m2 = blur(L, 3), blur(L * L, 3); tex = np.sqrt(np.maximum(m2 - m1 * m1, 0)); ground = tex > 0.02
# refine the edge per pixel: how much like the sky just above vs the ground just below
yy = np.arange(H)[:, None]; sky = (yy < ridge[None, :]).astype(float)
band = np.abs(yy - ridge[None, :]) <= 10
for x in range(W):
    r = ridge[x]; a, b = max(0, r - 22), max(1, r - 10); c, d = min(H - 1, r + 10), min(H, r + 22)
    sc, gc = img[a:b, x].mean(0), img[c:d, x].mean(0); ax = sc - gc; n = (ax * ax).sum()
    if n < 1e-5: continue
    ys = np.arange(max(0, r - 10), min(H, r + 11)); t = ((img[ys, x] - gc) @ ax) / n
    sky[ys, x] = np.clip(t, 0, 1)
sky = np.clip(blur(sky, 1.2), 0, 1)
# clouds: brighter than the smooth sky around them; stars are held out behind them
cloud = np.clip((L - blur(L, 60)) / 0.06, 0, 1); cloud = np.clip(blur(cloud, 6) * 1.4, 0, 1)
stars = sky * (1 - cloud) * np.clip((ridge[None, :] - yy) / 40, 0, 1) ** 0.5

# ---- the moon: find it, then lift it and its halo out of the sky by filling each row from the sky either side
R0 = int(mr * 3.2); on = img.copy(); fill = img.copy()
prev = None
for y in range(max(0, my - R0), min(H, my + R0)):        # each row from the clear sky either side; below the treeline, carry the row above
    a_, b_ = max(0, mx - R0 - 6), min(W - 1, mx + R0 + 6)
    ls, rs = slice(max(0, a_ - 24), a_), slice(b_, b_ + 24)
    lw, rw = (sky[y, ls] > 0.97), (sky[y, rs] > 0.97)
    if lw.sum() >= 4 and rw.sum() >= 4: left, right = img[y, ls][lw].mean(0), img[y, rs][rw].mean(0); prev = (left, right)
    elif prev is not None: left, right = prev
    else: continue
    xs_ = np.arange(a_, b_); t = (xs_ - a_) / (b_ - a_); fill[y, a_:b_] = left[None] * (1 - t[:, None]) + right[None] * t[:, None]
yy_, xx_ = np.mgrid[0:H, 0:W]; d = np.hypot(xx_ - mx, yy_ - my); hole = np.clip((R0 - d) / (R0 * 0.4), 0, 1) * sky
on = img * (1 - hole[..., None]) + fill * hole[..., None]; moon = np.clip(img - on, 0, 1)
# ---- lights off (lightsoff.py method, ambient kept)
lin = on ** 2.2; Ll = lin @ [0.2126, 0.7152, 0.0722]; R, B = lin[..., 0], lin[..., 2]
amb = blur(Ll, W / 40); warm = (R - B) / (Ll + 1e-4)
emit = (Ll > np.maximum(amb * 1.8, 0.012)) & (warm > 0.25) & (yy > ridge[None, :] + 20)
emit = blur(emit.astype(float), max(2, W // 640) / 1.7) > 0.02
m = np.clip(blur(emit.astype(float), W / 700) * 1.5, 0, 1)
# dim the light the way a dimmer would: one smooth factor per area (not per pixel), so DEDON's brick, stone and glass texture survives;
# the warm colour drains toward a cool unlit tone as it goes
Lsm = blur(Ll, 3); target = np.maximum(amb * 0.5, 1e-4); ratio = np.clip(target / (Lsm + 1e-6), 0.05, 1.0); k = 1 - m * (1 - ratio)
lakeM = np.clip((yy - 1080) / 34, 0, 1); k = k * (1 - lakeM) + np.minimum(blur(k, 14), 1.0) * lakeM   # reflections are soft: dim them softly
grey = Ll[..., None] * np.array([0.74, 0.86, 1.10]); off = lin * k[..., None]
off = off * (1 - 0.6 * m[..., None]) + grey * k[..., None] * 0.6 * m[..., None]
spill = blur(m * np.clip(Ll / (Ll.max() + 1e-6), 0, 1), W / 45); spill = spill / (spill.max() + 1e-6)
off = off * (1 - 0.55 * spill[..., None] * np.array([1.0, 0.85, 0.4]))
off = np.clip(off, 0, 1) ** (1 / 2.2)
light = np.clip(on - off, 0, 1)
# groups left to right by equal light energy, split at the quietest column near each quarter
col = light.sum(axis=(0, 2)); cum = np.cumsum(col) / col.sum(); cuts = [0]
for q in (0.25, 0.5, 0.75):
    i = int(np.searchsorted(cum, q)); lo, hi = max(1, i - 60), min(W - 1, i + 60); cuts.append(lo + int(np.argmin(blur(col[None, :], 4)[0][lo:hi])))
cuts.append(W); xx = np.arange(W)[None, :]
# the water: below the shoreline (DEDON's waterline sits at about y 1080-1110 in this band); feathered
lake = np.clip((yy - 1080) / 34, 0, 1) * np.ones((1, W))
def save(a, p, alpha=None):
    a = np.clip(a, 0, 1)
    if alpha is None:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-i", "-"] + (["-q:v", "2"] if p.endswith(".jpg") else []) + [p], input=(a * 65535).astype("<u2").tobytes())
    else:
        rgba = np.dstack([a, np.clip(alpha, 0, 1)]); subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba64le", "-s", f"{W}x{H}", "-i", "-", p], input=(rgba * 65535).astype("<u2").tobytes())
save(on, f"{OUT}/on.jpg"); save(off, f"{OUT}/off.jpg")
for g in range(4):
    gm = ((xx >= cuts[g]) & (xx < cuts[g + 1])).astype(float); save(light * gm[..., None], f"{OUT}/light{g + 1}.png")
one = np.ones((H, W, 3))
save(one, f"{OUT}/sky.png", sky); save(one, f"{OUT}/stars.png", stars); save(one, f"{OUT}/lake.png", lake)
save(moon, f"{OUT}/moon.png")
meta = {"W": W, "H": H, "moon": [mx, my, mr], "moonR": R0, "cuts": cuts, "ridgeAtMoon": int(ridge[max(0, mx - 60):mx + 60].min()), "lakeY": 1080}
json.dump(meta, open(f"{OUT}/hero.json", "w")); open(f"{OUT}/meta.js", "w").write("window.HERO = " + json.dumps(meta) + ";\n")
print("moon", (mx, my, round(mr, 1)), "ridge at moon", int(ridge[mx]), "groups", cuts, "lit area", f"{m.mean() * 100:.1f}%", "sky", f"{sky.mean() * 100:.1f}%")
