"""Version 2 plates: for each scene a BEFORE (lights off) and AFTER (lit) image at film resolution.
KODA fixtures are the manufacturers' own product cut-outs from kodalighting.com, placed by eye at the stated scale.
All maths in linear light. Run: ~/Developer/.asr-venv/bin/python tools/v2plates.py [scene ...]"""
import sys, subprocess, numpy as np
A = "assets/manufacturer-source/"; OUT = "src/v2/"
def _box(a, r, axis):
    r = max(1, int(r)); a = np.swapaxes(a, 0, axis); p = np.pad(a, [(r + 1, r)] + [(0, 0)] * (a.ndim - 1), mode="edge")
    c = np.cumsum(p, axis=0); o = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1); return np.swapaxes(o[: a.shape[0]], 0, axis)
def blur(a, s):
    r = max(1, int(round(s * 0.87)))
    for _ in range(3): a = _box(_box(a, r, 0), r, 1)
    return a
def dims(p): return [int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.split(",")]
def load(p, W=None, rgba=False):
    w, h = dims(p); W = W or w; H = round(h * W / w)
    fmt = "rgba64le" if rgba else "rgb48le"; n = 4 if rgba else 3
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", fmt, "-"], capture_output=True).stdout
    a = np.frombuffer(raw, "<u2").reshape(H, W, n).astype(np.float64) / 65535
    if rgba: a[..., :3] = a[..., :3] ** 2.2
    else: a = a ** 2.2
    return a
def save(lin, p):
    H, W = lin.shape[:2]; a = np.clip(lin, 0, 1) ** (1 / 2.2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-i", "-", "-q:v", "2", p], input=(a * 65535).astype("<u2").tobytes())
def lights_off(lin, stops=1.0, force=None, glass=None, auto=True):
    """force: list of (x0,y0,x1,y1) fractions always treated as light sources; glass: fractions of lit glazing to turn into dusk glass."""
    H, W = lin.shape[:2]; L = lin @ [0.2126, 0.7152, 0.0722]; R, B = lin[..., 0], lin[..., 2]
    amb = blur(L, W / 40); warm = (R - B) / (L + 1e-4)
    emit = np.zeros((H, W), bool) if not auto else (((L > np.maximum(amb * 1.8, 0.012)) & (warm > 0.25)) | ((L > np.maximum(amb * 2.5, 0.05)) & (B > R * 1.2) & (np.arange(H)[:, None] > H * 0.45)))
    for (x0, y0, x1, y1) in (force or []):
        sl = (slice(int(y0 * H), int(y1 * H)), slice(int(x0 * W), int(x1 * W))); emit[sl] |= L[sl] > np.percentile(L[sl], 78)
    m = np.clip(blur((blur(emit.astype(float), W / 640) > 0.02).astype(float), W / 900) * 1.6, 0, 1)
    ratio = np.clip(np.maximum(amb * 0.9, 1e-4) / (L + 1e-6), 0.04, 1.0); k = 1 - m * (1 - ratio)
    off = lin * k[..., None]
    tint = off.mean(axis=2, keepdims=True) * np.array([0.96, 0.98, 1.02]); off = off * (1 - 0.6 * m[..., None]) + tint * 0.6 * m[..., None]
    off = off * (1 - 0.45 * m[..., None])                                  # a switched-off source sits darker than its surroundings
    spill = blur(m * np.clip(L / (L.max() + 1e-6), 0, 1), W / 45); spill = spill / (spill.max() + 1e-6)
    off = off * (1 - 0.55 * spill[..., None] * np.array([1.0, 0.85, 0.4]))
    for (x0, y0, x1, y1) in (glass or []):        # lit glazing -> dark glass holding a little of the dusk sky
        g = np.zeros((H, W)); g[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 1; g = blur(g, W / 700)
        sky = np.array([0.006, 0.009, 0.020]); detail = blur(L, W / 400)[..., None] * 0.012
        off = off * (1 - g[..., None]) + (sky + detail + lin * 0.012) * g[..., None]
    return off * 2 ** (-stops) * np.array([0.86, 0.94, 1.12])
def ell(H, W, cx, cy, rx, ry, soft=1.0):
    y, x = np.ogrid[:H, :W]; d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2; return np.exp(-d * 2.2 / soft)
def over(dst, spr, x, y):
    """alpha-composite sprite (h,w,4 linear) with its top-left at x,y."""
    h, w = spr.shape[:2]; H, W = dst.shape[:2]; x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y); dx0, dy0 = max(0, x), max(0, y); sx1 = min(w, W - x); sy1 = min(h, H - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    s = spr[sy0:sy1, sx0:sx1]; a = s[..., 3:4]; d = dst[dy0:dy0 + sy1 - sy0, dx0:dx0 + sx1 - sx0]
    d[:] = d * (1 - a) + s[..., :3] * a
def line(dst, x0, y0, x1, y1, w, col, a=0.85):
    H, W = dst.shape[:2]; n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 2
    m = np.zeros((H, W))
    for t in np.linspace(0, 1, n): m[int(round(y0 + (y1 - y0) * t)), int(round(x0 + (x1 - x0) * t))] = 1
    m = np.clip(blur(m, max(0.6, w / 2)) * (w * 1.2), 0, 1) * a; dst[:] = dst * (1 - m[..., None]) + np.array(col) * m[..., None]
WARM = np.array([1.0, 0.72, 0.42]); WARMW = np.array([1.0, 0.86, 0.66])
def sprite_from(p, rows=None, W=None, squash=1.0):
    s = load(p, rgba=True)
    if rows: s = s[rows[0]:rows[1]]
    a = s[..., 3]; ys, xs = np.where(a > 0.05); s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = s.shape[:2]; nw = int(W or w); nh = max(2, int(h * nw / w * squash))
    yi = (np.arange(nh) * h / nh).astype(int); xi = (np.arange(nw) * w / nw).astype(int)
    sm = blur(s, max(0.5, w / nw / 2.5)) if nw < w else s
    return sm[yi][:, xi]
def sprite_from_arr(s, scale):
    h, w = s.shape[:2]; nw, nh = max(2, int(w * scale)), max(2, int(h * scale))
    sm = blur(s, max(0.5, 1 / scale / 2.5)) if scale < 1 else s
    return sm[(np.arange(nh) / scale).astype(int).clip(0, h - 1)][:, (np.arange(nw) / scale).astype(int).clip(0, w - 1)]
def scene(name):
    if name == "d01":
        lin = load(A + "dedon/originals/dedon-secret-lakeside-house-night.jpg", 3840)
        save(lights_off(lin, 1.0), OUT + "d01-off.jpg"); save(lin, OUT + "d01-on.jpg")
    if name == "d02":
        lin = load(A + "dedon/originals/dedon-mood-mysterious-desert-dala-loon-mbrace-sealine-kida.jpg")
        glass = [(0.335, 0.175, 0.528, 0.29), (0.20, 0.345, 0.775, 0.48)]
        save(lights_off(lin, 1.0, glass=glass, force=[(0.0, 0.52, 0.78, 0.68), (0.12, 0.66, 1.0, 0.80)]), OUT + "d02-off.jpg"); save(lin, OUT + "d02-on.jpg")
    if name == "d04":
        lin = load(A + "dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii.jpg", 3840); H, W = lin.shape[:2]; f = W / 1200
        ring = A + "../../src/cutouts/mito-sospeso60-bronze.png"
        lamps = [(495, 575, 535, 632), (672, 592, 722, 668), (848, 648, 874, 678)]
        off = lights_off(lin, 0.9, force=[(a / 1200, b / 1200, c / 1200, d / 1200) for a, b, c, d in lamps], auto=False); on = lin.copy()
        for (cx, cy, rw, top, tcx, tcy, prx) in [(565, 512, 92, 232, 566, 628, 95), (768, 532, 112, 252, 770, 664, 120)]:
            spr = sprite_from(ring, rows=(1380, 2010), W=rw * f, squash=0.52)
            sh, sw = spr.shape[:2]; X, Y = cx * f - sw / 2, cy * f - sh / 2
            for img, lit in ((off, False), (on, True)):
                for dxs in (-0.30, 0.30):   # two suspension cables to the pergola
                    line(img, cx * f + dxs * sw, top * f, cx * f + dxs * sw, Y + sh * 0.3, 1.4 * f / 3, (0.02, 0.018, 0.016), 0.8)
                if lit:
                    img += ell(H, W, tcx * f, tcy * f, prx * 1.5 * f, prx * 0.42 * f)[..., None] * img * 5.0 * WARM + ell(H, W, tcx * f, tcy * f + 40 * f, prx * 2.2 * f, prx * 0.9 * f)[..., None] * img * 1.6 * WARM          # pool on the table top
                    img += ell(H, W, cx * f, cy * f + sh * 0.4, sw * 1.3, sw * 0.55)[..., None] * 0.045 * WARM            # air glow under the ring
                    img += ell(H, W, cx * f, top * f + 6 * f, sw * 1.4, sw * 0.35)[..., None] * img * 1.2 * WARM          # up-light on the slats
                over(img, spr, X, Y)
                if lit:
                    img += ell(H, W, cx * f, Y + sh * 0.70, sw * 0.46, sh * 0.20, 0.22)[..., None] * 1.6 * WARMW + ell(H, W, cx * f, Y + sh * 0.7, sw * 0.7, sh * 0.9)[..., None] * 0.08 * WARMW          # the lit inner band
        save(off, OUT + "d04-off.jpg"); save(on, OUT + "d04-on.jpg")
    if name == "d03":
        lin = load(A + "dedon/originals/dedon-mood-mu-mystique-dusk.jpg", 3840); H, W = lin.shape[:2]; f = W / 1500
        src = [(75, 480, 180, 610), (145, 432, 222, 525), (968, 500, 1066, 610), (330, 300, 505, 385), (0, 305, 70, 380)]
        off = lights_off(lin, 0.8, force=[(a / 1500, b / 1062, c / 1500, d / 1062) for a, b, c, d in src], auto=False); on = lin.copy()
        s0 = load("src/cutouts/mito-largo-bronze.png", rgba=True)[:, ::-1]          # mirrored: base right, ring reaching left
        band = (990, 1330); sq = 0.42                                                 # ring band seen from seated eye height
        mid = s0[band[0]:band[1]]; nh = int((band[1] - band[0]) * sq); idx = (np.arange(nh) / sq).astype(int)
        s1 = np.concatenate([s0[:band[0]], mid[idx], s0[band[1]:]]); floor_y = s1.shape[0] - 137; ring_y = band[0] + nh * 0.55
        cols = np.where(s1[floor_y - 60:floor_y, :, 3].max(0) > 0.3)[0]; base_cx = cols.mean()
        bandrows = s1[band[0]:band[0] + nh, :, 3] > 0.3; r = band[0] + int(np.argmax(bandrows.sum(1)))   # widest row = the ring's far rim
        rc = np.where(s1[r, :, 3] > 0.3)[0]; runs = np.split(rc, np.where(np.diff(rc) > 40)[0] + 1); run = max(runs, key=len)
        ring_cx = (run.min() + run.max()) / 2; ring_w = run.max() - run.min()
        scale = (290 * f) / (floor_y - ring_y)                                       # ring ~145 cm over the floor at ~2.0 px/cm (just behind the coffee table)
        spr = sprite_from_arr(s1, scale)
        sh, sw = spr.shape[:2]; bx, by = 1112 * f, 622 * f                            # base on the floor right of the lantern, clear of the chair
        X = bx - base_cx * scale; Y = by - floor_y * scale
        ringx = X + ring_cx * scale; ringy = Y + ring_y * scale; rw = ring_w * scale
        for img, lit in ((off, False), (on, True)):
            if lit:
                img += ell(H, W, ringx, 655 * f, rw * 0.75, rw * 0.2)[..., None] * img * 4.0 * WARM + ell(H, W, ringx, 680 * f, rw * 1.4, rw * 0.45)[..., None] * img * 1.0 * WARM
                img += ell(H, W, ringx, ringy + rw * 0.25, rw * 0.8, rw * 0.45)[..., None] * 0.03 * WARM
            img[:] = img * (1 - 0.35 * ell(H, W, bx - 20 * f, by + 4 * f, 60 * f, 10 * f)[..., None])
            over(img, spr, X, Y)
            if lit: img += ell(H, W, ringx, ringy + rw * 0.04, rw * 0.46, rw * 0.05, 0.22)[..., None] * 1.4 * WARMW
        print("ring centre", round(ringx / f), round(ringy / f), "ring width", round(rw / f))
        save(off, OUT + "d03-off.jpg"); save(on, OUT + "d03-on.jpg")
    if name == "rest":
        for key, p, w in [("d07", "dedon/originals/dedon-mood-mysterious-desert-loon-mbrace-mbrace-alu-nestrest-sealine.jpg", 3840), ("d05", "dedon/originals/dedon-mood-spiritual-mountain-mbrace-mu-porcini-roii-the others.jpg", 2720),
                          ("d06", "dedon/originals/dedon-mood-secret-lakeside-mbrace-mbrace alu-porcini-mbarq-the others.jpg", 3840), ("p01", "potocco/originals/Izar-Houses__0cdd81c8-bb2e-480b-9b69-027566978ea6.jpg", 3840)]:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", A + p, "-vf", f"scale={w}:-2:flags=lanczos", "-q:v", "2", OUT + key + ".jpg"])
    print("done", name)
import os; os.makedirs(OUT, exist_ok=True)
if __name__ == "__main__":
    for s in (sys.argv[1:] or ["d01", "d02", "d04", "d03", "rest"]): scene(s)
