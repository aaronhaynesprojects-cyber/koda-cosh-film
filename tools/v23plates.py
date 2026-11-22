"""Version 2.3 plates (art-direction rebuild, docs/v2/V2.3-ASSESSMENT.md).
Rule for every KODA piece: it stands exactly where the manufacturer's own lamp stood in the original image, at its
published size measured in that image plane, so the light on the surfaces is the light the renderer (or the camera)
actually recorded from a lamp of that size, height and kind. The original lamp is removed, never covered.
"Off" plates subtract a physically shaped estimate of that lamp's light (inverse-square, cosine on the supporting plane),
then lower the ambient so the change is a real change of atmosphere, not a brightness fade.
Run: ~/Developer/.asr-venv/bin/python tools/v23plates.py [scene ...]"""
import sys, os, numpy as np
sys.path.insert(0, "tools")
from v2plates import load, save, blur, over, ell, A, lights_off
from v21plates import inpaint
OUT = "src/v23/"; os.makedirs(OUT, exist_ok=True)
LUM = np.float32([0.2126, 0.7152, 0.0722])
K2700 = np.float32([1.0, 0.80, 0.60]); K2200 = np.float32([1.0, 0.68, 0.42]); DUSK = np.float32([0.80, 0.90, 1.12])
UMA = "src/products/uma/Uma.png"; ERA_G = "src/products/era/Era-lusso-marrone-bronze-desktop.png"

def L(img): return img @ LUM
def loadc(path, x0, y0, x1, y1, scale):
    """load only the part of the frame the film uses, at the size it needs, as 32-bit linear light (an 8 GB machine)"""
    import subprocess
    w, h = int((x1 - x0) * scale), int((y1 - y0) * scale)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale={w}:{h}:flags=lanczos",
                          "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, "<u2").reshape(h, w, 3).astype(np.float32) / 65535
    return a ** np.float32(2.2)
def falloff(H, W, cx, cy, rx, ry, h=1.0, y0=0, x0=0):
    """irradiance of a small source at height h above a plane, seen in perspective: the plane metric is an ellipse rx, ry
    (pixels per unit length across / along), E = (1 + d^2/h^2)^-1.5, 1 at the foot of the lamp"""
    y, x = np.ogrid[y0:y0 + H, x0:x0 + W]; y = y.astype(np.float32); x = x.astype(np.float32)
    d2 = ((x - np.float32(cx)) / np.float32(rx)) ** 2 + ((y - np.float32(cy)) / np.float32(ry)) ** 2
    return (1 + d2 / np.float32(h ** 2)) ** np.float32(-1.5)

PARTS = {  # Pablo's renders: crop rows/cols, and the row bands of cap+strap, glowing diffuser, base; height in cm
    "uma":  dict(path=UMA, crop=(42, 689, 250, 511), diff=(172, 632), cap=(145, 172), cm=35.0),        # Uma: dia 15.4, H 35 with strap (body 28)
    "mini": dict(path="src/products/uma/Uma_Mini.png", crop=(223, 862, 325, 705), diff=(272, 790), cap=(223, 272), cm=21.4),  # Uma Mini: 14.2 x H 21.4
}
def uma(total_px, lit, amb=0.02, glow_L=1.6, kind="uma"):
    """Pablo Uma / Uma Mini from Pablo's own render (kodalighting.com feed).
    lit: the polycarbonate diffuser glows at the scene lamp's measured brightness, warm-dim 2700 K; cap, leather and base keep
    their shape but drop to what a dark evening and the lamp's own spill would give them.
    unlit: milky diffuser and every part at the scene's light level, slightly cool."""
    P = PARTS[kind]; y0, y1, x0, x1 = P["crop"]; s = load(P["path"], rgba=True)[y0:y1, x0:x1]; h, w = s.shape[:2]
    rows = np.arange(h)[:, None] * np.ones((1, w)); d0, d1 = P["diff"][0] - y0, P["diff"][1] - y0
    diff = (rows >= d0) & (rows < d1); top = rows < d0; base = rows >= d1
    rgb = s[..., :3].copy(); a = s[..., 3]
    if kind == "mini": diff &= ~((np.arange(w)[None, :] > 612 - x0) & (rows < 285 - y0))     # the leather loop is not lit from inside
    if lit:
        Ld = L(rgb); d = np.where(diff, Ld / (np.percentile(Ld[diff & (a > 0.5)], 60) + 1e-6), 0)
        rgb[diff] = (np.clip(d, 0.6, 1.4)[diff][:, None] * glow_L) * np.float32([1.0, 0.74, 0.50])
        rgb[top & ~diff] = rgb[top & ~diff] * 0.18 + np.float32([0.06, 0.045, 0.03])            # cap and leather in the dark, lit from below
        rgb[base] = rgb[base] * 0.20 + np.float32([0.05, 0.035, 0.022])                           # base under the glow
    else:
        k = amb / (np.median(L(rgb)[a > 0.5]) + 1e-6)
        rgb = rgb * k * 1.15 * DUSK                                            # white polycarbonate: about as pale as a white table beside it
        rgb[base | top] *= 0.7
    sc = total_px / h; nh, nw = max(2, int(h * sc)), max(2, int(w * sc))
    s = np.concatenate([rgb, a[..., None]], -1); sm = blur(s, max(0.5, 1 / sc / 2.5)) if sc < 1 else s
    ri, ci = (np.arange(nh) / sc).astype(int).clip(0, h - 1), (np.arange(nw) / sc).astype(int).clip(0, w - 1)
    out = sm[ri][:, ci]; em = diff[ri][:, ci].astype(float)
    return out, em * (out[..., 3] > 0.5)

def era(total_px, lit, amb=0.02, glow_L=1.2):
    """Occhio Era lusso grande (dia 20.9 x H 25 cm; Occhio's render matches those proportions), bronze.
    Occhio's studio render reflects a white room in the crystal, which is what made V2.2 read as chrome. At night the
    crystal holds darkness and a few highlights; the brass mesh sleeve and the opal sphere inside it carry the light;
    the top lens glows; the base sits in the dark."""
    s = load(ERA_G, rgba=True); a = s[..., 3]
    cols = np.where(a.max(0) > 0.5)[0]; gaps = np.where(np.diff(cols) > 8)[0]; s = s[:, cols[gaps[0]] + 1:]
    ys, xs = np.where(s[..., 3] > 0.05); s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; h, w = s.shape[:2]
    rgb = s[..., :3].copy(); a = s[..., 3]; r = np.arange(h)[:, None] * np.ones((1, w)); rel = r / h
    Lr = L(rgb); sat = (rgb.max(-1) - rgb.min(-1)) / (rgb.max(-1) + 1e-4)
    lens = rel < 0.075                                                        # the top: lens and rim
    shade = (rel >= 0.075) & (rel < 0.62); base = rel >= 0.62
    mesh = shade & (sat > 0.28); crystal = shade & ~mesh
    if lit:
        m = Lr / (np.percentile(Lr[mesh & (a > 0.5)], 60) + 1e-6)
        rgb[mesh] = (np.clip(m, 0.4, 1.8)[mesh][:, None] * glow_L * 0.55) * np.float32([1.0, 0.70, 0.36])   # brass mesh lit from inside, 2700 K
        cx = w / 2; d2 = ((np.arange(w)[None, :] - cx) / (w * 0.16)) ** 2 + ((r - h * 0.40) / (h * 0.13)) ** 2
        sphere = np.exp(-d2) * shade                                          # the opal sphere seen through the mesh
        rgb += (sphere * glow_L * 0.9)[..., None] * np.float32([1.0, 0.82, 0.62]) * a[..., None]
        hi = np.clip((Lr - 0.75) / 0.25, 0, 1)
        rgb[crystal] = rgb[crystal] * 0.05 + (hi[crystal] * 0.35)[:, None] + np.float32([0.035, 0.022, 0.010])   # dark crystal, highlights, warm inner reflection
        rgb[lens] = np.float32([1.0, 0.85, 0.66]) * glow_L * 0.8 * np.clip(Lr[lens] / (Lr[lens].max() + 1e-6), 0.3, 1)[:, None]
        rgb[base] = rgb[base] * 0.25 + np.float32([0.020, 0.012, 0.006])
    else:
        k = amb / (np.median(Lr[a > 0.5]) + 1e-6); rgb = rgb * k * 0.9 * DUSK
    sc = total_px / h; nh, nw = max(2, int(h * sc)), max(2, int(w * sc))
    s2 = np.concatenate([rgb, a[..., None]], -1); sm = blur(s2, max(0.5, 1 / sc / 2.5)) if sc < 1 else s2
    ri, ci = (np.arange(nh) / sc).astype(int).clip(0, h - 1), (np.arange(nw) / sc).astype(int).clip(0, w - 1)
    out = sm[ri][:, ci]; em = (mesh | lens)[ri][:, ci].astype(float)
    return out, em * (out[..., 3] > 0.5)

def fill(img, x0, y0, x1, y1, iters=80, seed=5):
    """fill a rectangle from its border (row-wise interpolation keeps horizontal structure, a short relaxation smooths it),
    then add grain matched to the border's own fine texture, never the texture of what was removed"""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1); H, W = img.shape[:2]; pad = 10
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    reg = img[Y0:Y1, X0:X1].copy(); m = np.zeros(reg.shape[:2], bool); m[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = True
    ring = (~m) & (blur(m.astype(float), 6) > 0.01)
    hp = reg - blur(reg, 1.5); sd = hp[ring].std(0) if ring.any() else np.zeros(3)
    for r in range(reg.shape[0]):
        if m[r].any():
            c = np.where(m[r])[0]; l, rr = max(0, c.min() - 1), min(reg.shape[1] - 1, c.max() + 1)
            t = (np.arange(c.min(), c.max() + 1) - l) / max(1, rr - l); reg[r, c.min():c.max() + 1] = reg[r, l] * (1 - t)[:, None] + reg[r, rr] * t[:, None]
    for _ in range(iters):
        avg = (np.roll(reg, 1, 0) + np.roll(reg, -1, 0) + np.roll(reg, 1, 1) + np.roll(reg, -1, 1)) / 4; reg[m] = avg[m]
    g = np.random.default_rng(seed).normal(size=reg.shape) * sd; g = g - blur(g, 1.5) * 0.3
    reg[m] = np.clip(reg[m] + g[m] * 0.9, 0, None); img[Y0:Y1, X0:X1] = reg

def era_draw(img, cx, foot, Ht, lit, amb=0.02, glow=1.25, refl=0.0):
    """Occhio Era grande (dia 20.9 x H 25 cm), drawn as what it is: a thick clear crystal shade you can see the room through,
    an opal sphere that carries the light, a dark base. Proportions from Occhio's render; light behaviour from Occhio's film
    (bright crystal edges and bottom rim, the sphere's ghost reflections stacked above it). Optional mirror on a glossy table."""
    H, W = img.shape[:2]; Wt = Ht * 20.9 / 25.0
    X0, X1 = int(cx - Wt * 0.6), int(cx + Wt * 0.6) + 1; Y0, Y1 = int(foot - Ht * 1.02), int(foot + (Ht * 0.9 if refl else 2)) + 1
    X0, Y0, X1, Y1 = max(0, X0), max(0, Y0), min(W, X1), min(H, Y1)
    y, x = np.mgrid[Y0:Y1, X0:X1].astype(float); u = (x - cx) / Wt; rel = (y - (foot - Ht)) / Ht
    hw = 0.39 + 0.11 * np.clip((rel - 0.06) / 0.58, 0, 1)
    top = ((u / 0.39) ** 2 + ((rel - 0.06) / 0.03) ** 2) <= 1
    sb = 0.64 + 0.028 * np.sqrt(np.clip(1 - (u / hw) ** 2, 0, 1))                 # the shade's lower rim, seen slightly from above
    shade = (((rel >= 0.06) & (rel <= sb) & (np.abs(u) <= hw)) | top)
    bb = 1.0 - 0.026 * (1 - np.sqrt(np.clip(1 - (u / 0.238) ** 2, 0, 1)))          # the base's round foot
    base = (rel > sb) & (rel <= bb) & (np.abs(u) <= 0.238)
    sph_c, sph_r = 0.47, 0.171                                                   # sphere centre and radius, in Ht
    d2 = (u * Wt / Ht / sph_r) ** 2 + ((rel - sph_c) / sph_r) ** 2; sphere = d2 <= 1
    reg = img[Y0:Y1, X0:X1]; out = reg.copy(); WARMC = np.float32([1.0, 0.80, 0.58])
    edge = np.exp(-(((hw - np.abs(u)) / 0.035) ** 2)) * shade
    rimb = np.exp(-(((sb - rel) / 0.022) ** 2)) * (np.abs(u) <= hw) * (rel <= sb + 0.01)
    rimt = np.exp(-((np.sqrt((u / 0.39) ** 2 + ((rel - 0.06) / 0.03) ** 2) - 1) / 0.12) ** 2) * (rel < 0.1)
    if lit:
        e = (edge * 0.45 + rimb * 0.95 + rimt * 0.55 + shade * 0.05)[..., None] * glow * WARMC
        for k, (dc, rr, a) in enumerate(((-0.13, 0.85, 0.16), (-0.24, 0.7, 0.07))):     # ghost spheres in the crystal
            g2 = (u * Wt / Ht / (sph_r * rr)) ** 2 + ((rel - sph_c - dc) / (sph_r * rr)) ** 2
            e += (np.exp(-np.maximum(g2 - 0.7, 0) * 4) * (g2 <= 1.2) * shade * a)[..., None] * glow * WARMC
        out = np.where(shade[..., None], reg * 0.62 + e, out)
        sp = (0.82 + 0.18 * np.clip(1 - d2, 0, 1)) * glow * 1.15
        out = np.where(sphere[..., None], sp[..., None] * np.float32([1.0, 0.86, 0.68]), out)
        cyl = np.sqrt(np.clip(1 - (u / 0.238) ** 2, 0, 1))                                    # round shading across the cylinder
        bs = 0.012 * (0.35 + 0.65 * cyl) + 0.30 * np.exp(-(((rel - sb - 0.008) / 0.012) ** 2)) * cyl + 0.010 * np.exp(-(((u + 0.10) / 0.03) ** 2))
        out = np.where(base[..., None], bs[..., None] * WARMC, out)
        if refl:                                                                  # the lamp mirrored in the glossy table
            mr = 2 - rel; mi = (mr > 0) & (mr < 1) & (rel > 1.0)
            dm = (u * Wt / Ht / sph_r) ** 2 + ((mr - sph_c) / sph_r) ** 2
            ref = (np.exp(-np.maximum(dm - 0.6, 0) * 3) * 0.9 + np.exp(-(((0.64 - mr) / 0.03) ** 2)) * (np.abs(u) <= 0.5) * 0.4) * mi
            ref = blur(ref, Ht * 0.03) * refl
            out += ref[..., None] * glow * WARMC
    else:
        e = (edge * 2.2 + rimb * 1.5 + rimt * 2.0)[..., None] * amb * DUSK
        out = np.where(shade[..., None], reg * 0.78 + e, out)
        out = np.where(sphere[..., None], (amb * (1.8 + 0.6 * np.clip(1 - d2, 0, 1)))[..., None] * DUSK, out)
        cyl = np.sqrt(np.clip(1 - (u / 0.238) ** 2, 0, 1))
        out = np.where(base[..., None], (amb * (0.2 + 0.25 * cyl))[..., None] * DUSK, out)
    # soft anti-aliased silhouette
    mask = blur((shade | base | sphere | ((rel > 1.0) & bool(refl and lit))).astype(float), 0.8)
    reg[:] = reg * (1 - mask[..., None]) + out * mask[..., None]
    if lit:                                                                       # air glow round the sphere
        g = np.zeros((H, W)); g[Y0:Y1, X0:X1] = sphere * 1.0
        img += (blur(g, Ht * 0.22) * 0.5 + blur(g, Ht * 0.06) * 0.4)[..., None] * glow * 0.10 * WARMC

def stand(img, spr, cx, base_y, em=None, bloom=0.0, contact=0.4):
    """sprite standing on a surface: bottom-centre at (cx, base_y); a soft contact shadow, optional bloom around the glowing part"""
    H, W = img.shape[:2]; h, w = spr.shape[:2]; X, Y = cx - w / 2, base_y - h
    if contact: img *= (1 - contact * ell(H, W, cx, base_y - 1, w * 0.45, max(2, w * 0.06)))[..., None]
    if em is not None and bloom:
        g = np.zeros((H, W)); ys, xs = np.nonzero(em)
        g[(ys + int(Y)).clip(0, H - 1), (xs + int(X)).clip(0, W - 1)] = 1
        img += (blur(g, w * 0.5) * 0.9 + blur(g, w * 0.14) * 0.6)[..., None] * bloom * K2700
    over(img, spr, X, Y)

def crop(img, x0, y0, x1, y1, scale=1.0):
    c = img[y0:y1, x0:x1]
    if scale == 1.0: return c
    h, w = c.shape[:2]; nh, nw = int(h * scale), int(w * scale); c = blur(c, 1 / scale / 2.5) if scale < 1 else c
    return c[(np.arange(nh) / scale).astype(int).clip(0, h - 1)][:, (np.arange(nw) / scale).astype(int).clip(0, w - 1)]

def scene(name):
    if name == "perg":   # DEDON Spiritual Mountain, the dining table under the reed pergola (6000 x 6000 render), worked at 0.8
        src = A + "dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii.jpg"; F = 0.8
        X0, Y0, X1, Y1 = 0, 1900, 6000, 5600                       # the part of the frame the film uses (full-size coordinates)
        full = load(src, int(6000 * F)); lin = full[int(Y0 * F):int(Y1 * F)].copy(); H, W = lin.shape[:2]
        q = lambda v, o=0: (v - o) * F
        lamps = [(2498, 2903, 2645, 3134, 2571, 3131), (3390, 2995, 3587, 3310, 3488, 3306)]   # DEDON's two lamps: bbox, foot
        far = [(4270, 3240, 4360, 3340), (4470, 3330, 4570, 3440)]                             # two small lamps on the far deck
        glowL = float(np.percentile(L(lin[int(q(3055, Y0)):int(q(3250, Y0)), int(q(3420)):int(q(3560))]), 70)); print("DEDON lamp body L", glowL)
        f = np.zeros((H, W))
        for (x0, y0, x1, y1, bx, by) in lamps:
            hp = (y1 - y0) * F; f += falloff(H, W, q(bx), q(by, Y0) - hp * 0.08, hp * 2.4, hp * 0.80, h=0.6)
        for (x0, y0, x1, y1) in far: f += 0.5 * falloff(H, W, q((x0 + x1) / 2), q(y1, Y0), 220 * F, 80 * F, h=0.6)
        frac = np.clip(f * 1.35, 0, 0.90)                                # share of each pixel's light that came from the lamps
        warm = np.clip((lin[..., 0] - lin[..., 2]) / (L(lin) + 1e-4), 0, 1.2) / 1.2
        amb = lin * (1 - frac * (0.55 + 0.45 * warm))[..., None]
        # lens bloom round each glowing body: a blur of the body, removed as a share of each pixel, never below 35 % of it
        body = np.zeros((H, W))
        for (x0, y0, x1, y1, bx, by) in lamps: body[int(q(y0, Y0)):int(q(y1, Y0)), int(q(x0)):int(q(x1))] = 1
        halo = blur(L(lin) * body, 32) * 0.35 + blur(L(lin) * body, 96) * 0.45
        amb *= (1 - np.clip(halo / (L(amb) + 1e-4), 0, 0.65))[..., None]
        box = lambda x0, y0, x1, y1, p=0: (int(q(x0)) - p, int(q(y0, Y0)) - p, int(q(x1)) + p, int(q(y1, Y0)) + p)
        for img in (lin, amb):
            for (x0, y0, x1, y1, bx, by) in lamps: inpaint(img, *box(x0, y0, x1, y1, 6))
            for (x0, y0, x1, y1) in far: inpaint(img, *box(x0, y0, x1, y1))
        lampL = np.clip(lin - amb, 0, None)
        night = amb * 0.30 * DUSK                                        # the same place forty minutes later: 1.7 stops less sky
        on = night + lampL; off = night.copy()
        ambL = float(np.median(L(night[int(q(3150, Y0)):int(q(3300, Y0)), int(q(2700)):int(q(3300))])))   # the white table top beside the lamps
        for (x0, y0, x1, y1, bx, by) in lamps:
            tot = (y1 - y0) * F * 21.4 / 20.0                            # Uma Mini (21.4 cm) where DEDON's lamp (20 cm: table leg 74 cm, dominoes 5 cm) stood
            s1, e1 = uma(tot, True, glow_L=glowL * 1.05, kind="mini"); stand(on, s1, q(bx), q(by, Y0) + 2, e1, bloom=0.10, contact=0.25)
            s0, _ = uma(tot, False, amb=ambL, kind="mini"); stand(off, s0, q(bx), q(by, Y0) + 2, contact=0.35)
        save(off, OUT + "perg-off.jpg"); save(on, OUT + "perg-on.jpg")
        c = (int(2000 * F), int(700 * F), int(4200 * F), int(1900 * F))
        save(off[c[1]:c[3], c[0]:c[2]], OUT + "chk-perg-off.jpg"); save(on[c[1]:c[3], c[0]:c[2]], OUT + "chk-perg-on.jpg")
    if name == "det":    # the same table, close: DEDON's detail render (4244 x 6000), worked at 0.92 so the frame is still 4K wide
        src = A + "dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii-detail.jpg"; F = 0.92
        Y0, Y1 = 2500, 5300
        lin = load(src, int(4244 * F))[int(Y0 * F):int(Y1 * F)].copy(); H, W = lin.shape[:2]
        q = lambda v, o=0: (v - o) * F
        lamps = [(2249, 3429, 2516, 3873, 2383, 3868), (2913, 3509, 3000, 3627, 2957, 3625)]
        glowL = float(np.percentile(L(lin[int(q(3500, Y0)):int(q(3800, Y0)), int(q(2300)):int(q(2470))]), 70)); print("DEDON lamp body L", glowL)
        f = np.zeros((H, W))
        for (x0, y0, x1, y1, bx, by) in lamps:
            hp = (y1 - y0) * F; f += falloff(H, W, q(bx), q(by, Y0) - hp * 0.05, hp * 2.2, hp * 0.55, h=0.6)
        frac = np.clip(f * 1.35, 0, 0.90)
        warm = np.clip((lin[..., 0] - lin[..., 2]) / (L(lin) + 1e-4), 0, 1.2) / 1.2
        amb = lin * (1 - frac * (0.55 + 0.45 * warm))[..., None]
        body = np.zeros((H, W))
        for (x0, y0, x1, y1, bx, by) in lamps: body[int(q(y0, Y0)):int(q(y1, Y0)), int(q(x0)):int(q(x1))] = 1
        halo = blur(L(lin) * body, 40) * 0.35 + blur(L(lin) * body, 120) * 0.45
        amb *= (1 - np.clip(halo / (L(amb) + 1e-4), 0, 0.65))[..., None]
        box = lambda x0, y0, x1, y1, p=0: (int(q(x0)) - p, int(q(y0, Y0)) - p, int(q(x1)) + p, int(q(y1, Y0)) + p)
        for img in (lin, amb):
            for (x0, y0, x1, y1, bx, by) in lamps: inpaint(img, *box(x0, y0, x1, y1, 6))
        lampL = np.clip(lin - amb, 0, None); on = amb * 0.30 * DUSK + lampL
        for (x0, y0, x1, y1, bx, by) in lamps:
            tot = (y1 - y0) * F * 21.4 / 20.0
            s1, e1 = uma(tot, True, glow_L=glowL * 1.05, kind="mini"); stand(on, s1, q(bx), q(by, Y0) + 2, e1, bloom=0.10, contact=0.25)
        save(on, OUT + "det-on.jpg"); save(on[int(q(3300, Y0)):int(q(4000, Y0)), int(q(1900)):int(q(3200))], OUT + "chk-det-on.jpg")
    if name == "izar":   # Potocco project, Izar Houses: the long table in the open hall (real photograph, 4200 x 2800, dusk)
        src = A + "potocco/originals/Izar-Houses__0cdd81c8-bb2e-480b-9b69-027566978ea6.jpg"; F = 0.92
        lin = load(src, int(4200 * F)); H, W = lin.shape[:2]; q = lambda v: v * F
        # four cordless globe lamps (24.5 cm) down the table: foot (x, y); heights follow the table's perspective (eye level y 1475)
        feet = [(1635, 2322), (1636, 1862), (1634, 1702), (1633, 1616)]; hs = [377 * (y - 1475) / 847 for x, y in feet]
        boxes = [(x - 0.30 * h - 6, y - h - 8, x + 0.30 * h + 6, y + 6) for (x, y), h in zip(feet, hs)]
        on = lin.copy()
        for (x0, y0, x1, y1) in boxes: inpaint(on, int(q(x0)), int(q(y0)), int(q(x1)), int(q(y1)), iters=200)
        for (fx, fy), h in zip(feet, hs): fill(on, q(fx - 0.33 * h), q(fy + 4), q(fx + 0.33 * h), q(fy + 0.62 * h), iters=120)   # the globes' mirror images in the table
        # house lights off: the warm, lamp-lit interior falls to the blue light coming in from the two open sides;
        # outside (cool: sky, pines) stays as photographed
        Ln = L(on); warm = np.clip(((on[..., 0] - on[..., 2]) / (Ln + 1e-4) - 0.05) / 0.35, 0, 1); warm = blur(warm, 6)
        illum = blur(Ln, W / 60) + 1e-4
        y, x = np.ogrid[:H, :W]; side = 0.010 + 0.028 * (np.exp(-x / (W * 0.16)) + np.exp(-(W - x) / (W * 0.16))) + 0.012 * (y / H)
        k = np.clip(side / illum, 0.02, 1.0)
        off = on * (1 - warm[..., None]) + on * (k[..., None] * DUSK) * warm[..., None]
        off *= 0.85
        # each Era's own light: the photograph's light near each lamp (its glow on the glossy table, rims of bowls and glasses)
        w8 = np.zeros((H, W))
        for (fx, fy), h in zip(feet, hs): w8 += falloff(H, W, q(fx), q(fy) - q(h) * 0.25, q(h) * 1.9, q(h) * 0.45, h=0.7)
        w8 = np.clip(w8 * 0.9, 0, 0.9)[..., None]
        eraon = off + w8 * np.clip(on - off, 0, None) * np.float32([1.0, 0.86, 0.68])
        on = on + w8 * 0.25 * np.clip(on - off, 0, None) * np.float32([0.10, 0.0, -0.10])   # the table glow a touch warmer than the white globes it replaces
        ambL = float(np.median(L(off[int(q(2200)):int(q(2400)), int(q(1500)):int(q(1780))])))
        for (fx, fy), h in zip(feet, hs):
            Ht = q(h * 25.0 / 24.5)
            era_draw(on, q(fx), q(fy) + 1, Ht, True, refl=0.30); era_draw(eraon, q(fx), q(fy) + 1, Ht, True, refl=0.30)
            era_draw(off, q(fx), q(fy) + 1, Ht, False, amb=ambL)
        save(off, OUT + "izar-off.jpg"); save(eraon, OUT + "izar-era.jpg"); save(on, OUT + "izar-on.jpg")
        c = (int(q(1150)), int(q(1450)), int(q(2350)), int(q(2400)))
        for nm, im in (("off", off), ("era", eraon), ("on", on)): save(im[c[1]:c[3], c[0]:c[2]], OUT + f"chk-izar-{nm}.jpg")
    if name == "izarx":  # Izar Houses from outside: the resolved setting for Act IV (real photograph). Deepened a little towards night.
        src = A + "potocco/originals/Izar-Houses__b5a5179f-fe38-480a-8abd-6c3dd7892f31.jpg"; F = 0.70
        lin = loadc(src, 0, 0, 4200, 2800, F); Ln = L(lin)
        lit = blur(np.clip(((lin[..., 0] - lin[..., 2]) / (Ln + 1e-4) - 0.15) / 0.3, 0, 1) * np.clip(Ln / 0.25, 0, 1), 8)
        k = 0.36 + 0.64 * lit
        save(lin * k[..., None] * (DUSK * (1 - lit[..., None]) + lit[..., None]), OUT + "izarx.jpg")
    if name == "canyon": # DEDON Spiritual Mountain, the canyon pavilion (4248 x 6000), all lamps out, late dusk: Act I
        src = A + "dedon/originals/dedon-mood-spiritual-mountain-mbrace-mu-porcini-roii-the others.jpg"; F = 0.62   # 1080p delivery: 2634 px wide
        Y0, Y1 = 800, 5200
        lin = loadc(src, 0, Y0, 4248, Y1, F); H, W = lin.shape[:2]
        R = lambda x0, y0, x1, y1: (x0 / 4248, (y0 - Y0) / (Y1 - Y0), x1 / 4248, (y1 - Y0) / (Y1 - Y0))
        lamps = [R(1960, 3020, 2150, 3200), R(1900, 3150, 2070, 3320), R(1000, 3560, 1260, 3800), R(3120, 4100, 3580, 4640), R(3150, 3560, 3290, 3700),
                 R(950, 3780, 1300, 4150), R(3100, 4600, 3600, 5000)]                     # hanging pair, deck pair, front lantern, small one, their reflections
        rooms = R(3080, 2980, 4248, 3880)
        off = lights_off(lin, 2.3, force=lamps + [rooms], auto=False)
        m = np.zeros((H, W))
        for (a0, b0, a1, b1) in lamps: m[int(b0 * H):int(b1 * H), int(a0 * W):int(a1 * W)] = 1
        m = np.clip(blur(m, 10) * 1.3, 0, 1); off *= (1 - 0.6 * m)[..., None]
        save(off, OUT + "canyon-dark.jpg")
    if name == "mu":     # DEDON Mysterious Desert, Mu Mystique terrace (6000 x 4248): the fire and one Uma where THE OTHERS stood
        src = A + "dedon/originals/dedon-mood-mu-mystique-dusk.jpg"; F = 0.6    # 3000 px wide: the 1.5x framings still sit at or under 1:1 at 1080p
        X0, Y0, X1, Y1 = 1000, 600, 6000, 3700                     # framed from the fireplace rightwards: the two left lanterns stay out of shot
        lin = loadc(src, X0, Y0, X1, Y1, F); H, W = lin.shape[:2]
        q = lambda v, o: (v - o) * F
        fire = (1660, 1450); lant = (3880, 2010, 4345, 2610, 4110, 2600)   # THE OTHERS lantern: 59 cm (DEDON), foot
        left = [(507, 2500), (750, 2200)]                                       # the two left lanterns, out of frame but lighting the chaise
        def pool(cx, cy, hp, k, h=0.6, flat=0.5): return k * falloff(H, W, q(cx, X0), q(cy, Y0), hp * 1.7 * F, hp * flat * F, h=h)
        fl = np.clip(pool(fire[0], fire[1] + 120, 520, 1.3, h=0.9, flat=0.45) + pool(fire[0], fire[1] - 80, 520, 0.9, h=1.0, flat=0.9), 0, 0.92)
        ll = np.clip(pool(lant[4], lant[5], 580, 0.75) + sum(pool(x, y, 560, 0.8) for x, y in left), 0, 0.6)   # dusk still lights the floor evenly
        warm = np.clip((lin[..., 0] - lin[..., 2]) / (L(lin) + 1e-4), 0, 1.2) / 1.2
        amb = lin * (1 - np.clip(fl + ll, 0, 0.93) * (0.5 + 0.5 * warm))[..., None]
        fx0, fy0, fx1, fy1 = int(q(1330, X0)), int(q(1230, Y0)), int(q(1990, X0)), int(q(1500, Y0))   # the flames themselves
        amb[fy0:fy1, fx0:fx1] *= 0.10
        fireL = np.clip(lin - amb, 0, None) * fl[..., None] / np.maximum(fl + ll, 1e-3)[..., None]
        bx0, by0, bx1, by1 = int(q(lant[0], X0)) - 8, int(q(lant[1], Y0)) - 8, int(q(lant[2], X0)) + 8, int(q(lant[3], Y0)) + 6
        for img in (amb, fireL): fill(img, bx0, by0, bx1, by1, iters=60)
        sx0, sx1, sy1 = int(q(3960, X0)), int(q(4195, X0)), int(q(3100, Y0))   # stops short of the folding chair
        for img in (amb, fireL): fill(img, sx0, by1 - 2, sx1, sy1, iters=60)      # the lantern's mirror streak in the polished floor
        # Uma (35 cm, emitter ~16 cm up) instead of the 59 cm lantern (emitter ~35 cm): its own floor pool, tighter and brighter at the foot
        ux, uy = q(lant[4], X0), q(lant[5], Y0); hpx = 35.0 * 580 / 59 * F
        E = falloff(H, W, ux, uy, hpx * 1.05, hpx * 0.36, h=0.45) + 0.35 * falloff(H, W, ux, uy - hpx * 0.6, hpx * 1.1, hpx * 1.1, h=0.8)
        alb = amb / (blur(L(amb), 60)[..., None] + 1e-3)
        umaL = alb * (E * 0.62)[..., None] * K2700
        mir = np.zeros((H, W)); mx0 = int(ux - hpx * 0.2); mir[int(uy + 2):int(uy + hpx * 0.75), mx0:int(ux + hpx * 0.2)] = 1
        mir *= np.clip(1 - (np.arange(H)[:, None] - uy) / (hpx * 0.75), 0, 1) ** 1.5
        umaL += blur(mir, hpx * 0.06)[..., None] * 0.10 * K2700                 # the lantern mirrored in the polished stone
        dusk = amb * 1.05 * np.float32([0.96, 0.98, 1.04])                        # before: the sky as DEDON rendered it, nothing lit
        night = amb * 0.42 * DUSK                                               # after: an hour later
        on = night + fireL + umaL; off = dusk.copy()
        ambL = float(np.median(L(dusk[int(uy - hpx):int(uy), int(ux - hpx):int(ux + hpx)])))
        s1, e1 = uma(hpx, True, glow_L=0.95); stand(on, s1, ux, uy + 1, e1, bloom=0.08, contact=0.35)
        s0, _ = uma(hpx, False, amb=ambL); stand(off, s0, ux, uy + 1, contact=0.35)
        save(off, OUT + "mu-dusk.jpg"); save(on, OUT + "mu-on.jpg")
        c = (int(q(2900, X0)), int(q(1600, Y0)), int(q(5000, X0)), int(q(3000, Y0)))
        save(off[c[1]:c[3], c[0]:c[2]], OUT + "chk-mu-off.jpg"); save(on[c[1]:c[3], c[0]:c[2]], OUT + "chk-mu-on.jpg")
    print("done", name)

if __name__ == "__main__":
    for s in sys.argv[1:]: scene(s)
