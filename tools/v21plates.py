"""Version 2.1 plates, to the luxury brief (docs/v2/BRIEF-V2.1.md):
cordless KODA pieces only outdoors (Occhio Era lusso, Pablo Uma), every piece standing on a surface,
scaled from published dimensions, swapped in where the scene's own lamp stood.
Run: ~/Developer/.asr-venv/bin/python tools/v21plates.py [d04 d03 chelt]"""
import sys, numpy as np
sys.path.insert(0, "tools")
from v2plates import load, save, blur, lights_off, over, ell, WARM, WARMW, A, OUT
OUT21 = "src/v21/"
def inpaint(img, x0, y0, x1, y1, iters=900):
    """fill a rectangle from its border (harmonic fill), then restore a little texture from the surround"""
    H, W = img.shape[:2]; pad = 6; X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    reg = img[Y0:Y1, X0:X1].copy(); m = np.zeros(reg.shape[:2], bool); m[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = True
    # start from row-wise linear interpolation, then relax
    for r in range(reg.shape[0]):
        if m[r].any():
            c = np.where(m[r])[0]; l, rr = max(0, c.min() - 1), min(reg.shape[1] - 1, c.max() + 1)
            t = (np.arange(c.min(), c.max() + 1) - l) / max(1, rr - l); reg[r, c.min():c.max() + 1] = reg[r, l] * (1 - t)[:, None] + reg[r, rr] * t[:, None]
    for _ in range(iters):
        avg = (np.roll(reg, 1, 0) + np.roll(reg, -1, 0) + np.roll(reg, 1, 1) + np.roll(reg, -1, 1)) / 4; reg[m] = avg[m]
    noise = img[Y0:Y1, X0:X1] - blur(img[Y0:Y1, X0:X1], 2.0); rng = np.random.default_rng(3)
    sh = rng.permutation(noise.reshape(-1, 3)).reshape(noise.shape); reg[m] = np.clip(reg[m] + sh[m] * 0.8, 0, None)
    img[Y0:Y1, X0:X1] = reg
def sprite(path, H_px, part=None):
    """product render (linear RGBA), cropped to its alpha, optionally the left/right object of a pair, scaled to H_px tall"""
    s = load(path, rgba=True); a = s[..., 3]
    if part is not None:
        cols = np.where(a.max(0) > 0.05)[0]; gaps = np.where(np.diff(cols) > 8)[0]; cut = cols[gaps[0]] + 1 if len(gaps) else s.shape[1] // 2
        s = s[:, :cut] if part == 0 else s[:, cut:]; a = s[..., 3]
    ys, xs = np.where(a > 0.05); s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = s.shape[:2]; sc = H_px / h; nh, nw = max(2, int(h * sc)), max(2, int(w * sc))
    sm = blur(s, max(0.5, 1 / sc / 2.5)) if sc < 1 else s
    return sm[(np.arange(nh) / sc).astype(int).clip(0, h - 1)][:, (np.arange(nw) / sc).astype(int).clip(0, w - 1)]
def states(spr, bgL, kind):
    """(unlit, lit) versions of a lit studio render, matched to the light level where it stands (bgL, linear median nearby).
    Unlit: the whole object drops to the scene's brightness (studio highlights go with it) and its glowing core goes dark.
    Lit: the render as photographed, a touch under studio level, plus its own glow added in place()."""
    rgb = spr[..., :3]; al = spr[..., 3]; L = rgb @ [0.2126, 0.7152, 0.0722]
    core = np.clip((L - (0.55 if kind == "era" else 0.45)) / 0.3, 0, 1) * (rgb[..., 0] >= rgb[..., 2])
    emis = blur(core, 1.0)
    med = float(np.median(L[al > 0.5])); bgL = max(bgL, 0.07) if kind == "uma" else bgL     # milky polycarbonate stays pale at dusk
    k = float(np.clip(bgL * (0.85 if kind == "era" else 1.6) / (med + 1e-6), 0.03, 1.0))
    grey = rgb.mean(-1, keepdims=True)
    unlit = (rgb * 0.7 + grey * 0.3) * k * (1 - (0.7 if kind == "era" else 0.15) * emis[..., None])
    lit = rgb * (0.85 if kind == "era" else 1.0)
    if kind == "uma": lit = lit * (1 - emis[..., None]) + lit * np.array([1.0, 0.80, 0.58]) * emis[..., None]   # 2000-2700 K warm-dim
    mk = lambda c: np.concatenate([c, spr[..., 3:4]], -1)
    return mk(unlit), mk(lit), emis
def place(img, spr, emis, cx, base_y, lit, surface_k=0.0, pool=(0, 0), glow=0.0):
    """stand the sprite on the surface at (cx, base_y): contact shadow, then light pool and air glow when lit"""
    H, W = img.shape[:2]; h, w = spr.shape[:2]; X, Y = cx - w / 2, base_y - h
    img[:] = img * (1 - 0.45 * ell(H, W, cx, base_y - 1, w * 0.55, max(2, w * 0.07))[..., None])
    if lit:
        if surface_k: img += ell(H, W, cx, base_y + pool[1], w * pool[0], w * pool[0] * 0.22)[..., None] * img * surface_k * WARM
        if glow:
            g = np.zeros((H, W)); ys, xs = np.nonzero(emis > 0.5)
            if len(ys): g[(ys + int(Y)).clip(0, H - 1), (xs + int(X)).clip(0, W - 1)] = 1
            img += blur(g, w * 0.35)[..., None] * glow * WARM + blur(g, w * 0.09)[..., None] * glow * 0.8 * WARMW
    over(img, spr, X, Y)
def amb_at(img, cx, cy, r):
    H, W = img.shape[:2]; y0, y1, x0, x1 = int(max(0, cy - r)), int(min(H, cy + r)), int(max(0, cx - r)), int(min(W, cx + r))
    return float(np.median(img[y0:y1, x0:x1] @ [0.2126, 0.7152, 0.0722]))
ERA_B = "src/products/era/Era-lusso-marrone-bronze-desktop.png"; ERA_R = "src/products/era/Era-lusso-rosso-rose-gold-desktop.png"; UMA = "src/products/uma/Uma.png"
def scene(name):
    import os; os.makedirs(OUT21, exist_ok=True)
    if name == "d04":                                          # pergola dining: DEDON's two table lamps become a pair of Era lusso grande
        lin = load(A + "dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii.jpg", 3840); f = 3840 / 6000
        lamps = [(2498, 2903, 2645, 3134, 2571, 3131), (3390, 2995, 3587, 3310, 3488, 3306)]
        halo = [((x0 - 120) / 6000, (y0 - 60) / 6000, (x1 + 120) / 6000, (y1 + 90) / 6000) for x0, y0, x1, y1, _, _ in lamps]
        off = lights_off(lin, 0.9, force=[(x0 / 6000, y0 / 6000, x1 / 6000, y1 / 6000) for x0, y0, x1, y1, _, _ in lamps] + [(2780 / 6000, 3060 / 6000, 3010 / 6000, 3150 / 6000)], auto=False)
        on = lin.copy()
        for img in (off, on):
            for x0, y0, x1, y1, _, _ in lamps: inpaint(img, int(x0 * f) - 4, int(y0 * f) - 4, int(x1 * f) + 4, int(y1 * f) + 2)
        for (x0, y0, x1, y1, bx, by) in lamps:
            hpx = (y1 - y0) * f * 1.04; spr = sprite(ERA_B, hpx, part=1)
            for img, lit in ((off, False), (on, True)):
                u, l, e = states(spr, amb_at(off, bx * f, (by - 160) * f, 110 * f), "era")
                place(img, l if lit else u, e, bx * f, by * f, lit, surface_k=1.2, pool=(1.6, 4), glow=0.05)
        save(off, OUT21 + "d04-off.jpg"); save(on, OUT21 + "d04-on.jpg")
    if name == "d03":                                          # terrace lounge: Era lusso grande on the coffee table, Uma on the rug
        lin = load(A + "dedon/originals/dedon-mood-mu-mystique-dusk.jpg", 3840); g = 3840 / 1500
        lant = [(75, 480, 180, 610), (145, 432, 222, 525), (968, 500, 1066, 610)]; fire = [(330, 300, 505, 385), (0, 305, 70, 380)]
        R = lambda rs: [(a / 1500, b / 1062, c / 1500, d / 1062) for a, b, c, d in rs]
        on = lights_off(lin, 0.0, force=R(lant), auto=False) / np.array([0.86, 0.94, 1.12]) * np.array([0.97, 0.98, 1.0])  # lanterns out, fire and sky as shot
        off = lights_off(lin, 0.8, force=R(lant + fire), auto=False)
        pieces = [(ERA_B, 1, 82, 690, 634, "era", (2.4, 3), 2.0, 0.07), (UMA, None, 116, 505, 788, "uma", (3.2, 4), 2.4, 0.14)]
        for path, part, hpx, bx, by, kind, pool, sk, gl in pieces:
            spr = sprite(path, hpx * g, part=part)
            for img, lit in ((off, False), (on, True)):
                u, l, e = states(spr, amb_at(off, bx * g, (by - hpx / 2) * g, 60 * g), kind)
                place(img, l if lit else u, e, bx * g, by * g, lit, surface_k=sk, pool=pool, glow=gl)
        save(off, OUT21 + "d03-off.jpg"); save(on, OUT21 + "d03-on.jpg")
    if name == "chelt":                                        # Cosh Living Cheltenham: price ticket out, Era lusso pair on the marble table
        lin = load("src/cosh2/x._All_Images_4.jpg")
        lin[931:982, 881:899] = lin[931:982, 905:923]                               # clone plain wall over the price ticket
        for path, part, hpx, bx, by in [(ERA_B, 1, 100, 628, 939), (ERA_R, 0, 67, 690, 941)]:
            spr = sprite(path, hpx, part=part); u, l, e = states(spr, amb_at(lin, bx, by - 50, 40), "era")
            place(lin, l, e, bx, by, True, surface_k=0.5, pool=(1.3, 2), glow=0.03)
        save(lin, OUT21 + "chelt.jpg")
    print("done", name)
if __name__ == "__main__":
    for s in (sys.argv[1:] or ["d04", "d03", "chelt"]): scene(s)
