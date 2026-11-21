"""Rank preview images by how naturally dark / dusk-lit they already are (the brief's most valuable property).
Measures, on a 64x40 thumbnail: mean luminance, share of the frame below 25% grey, sky blueness in the top third,
and warm highlights (existing lamplight). Writes triage.json next to the previews.
Usage: python tools/triage.py <previews-dir> [...]"""
import sys, os, json, subprocess, numpy as np
for d in sys.argv[1:]:
    out = {}
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): continue
        p = os.path.join(d, f)
        try:
            wh = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip().split(",")
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "scale=64:40", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            a = np.frombuffer(raw, np.uint8).reshape(40, 64, 3).astype(float) / 255
        except Exception as e:
            print("skip", f, e); continue
        L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        top = a[:13]; blue = float(np.mean(top[..., 2] - top[..., 0]))
        warm = float(np.mean((a[..., 0] > 0.75) & (a[..., 0] - a[..., 2] > 0.18)))
        mean = float(L.mean()); dark = float(np.mean(L < 0.25)); hi = float(np.mean(L > 0.9))
        dusk = max(0, min(100, 100 * (0.55 * (1 - mean / 0.6) + 0.30 * dark + 0.25 * max(0, blue) * 3 + 0.4 * warm * 4 - 0.6 * hi)))
        out[f] = {"w": int(wh[0]), "h": int(wh[1]), "mean": round(mean, 3), "dark": round(dark, 3), "sky_blue": round(blue, 3), "warm_lights": round(warm, 3), "blown": round(hi, 3), "dusk": round(dusk, 1)}
    json.dump(out, open(os.path.join(d, "..", "triage.json"), "w"), indent=1)
    top = sorted(out.items(), key=lambda kv: -kv[1]["dusk"])
    print(d, len(out), "images; darkest 12:"); [print("  ", round(v["dusk"]), k, v["w"], "x", v["h"]) for k, v in top[:12]]
