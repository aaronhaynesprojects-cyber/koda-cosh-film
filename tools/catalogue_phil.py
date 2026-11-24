"""Export every shot used in the Phil montage blocks as a catalogue of proven-clean shots (already checked for people,
hands and burned-in text), with safe durations, plus labelled contact sheets for editors.
  python3 tools/catalogue_phil.py      -> work/cut/catalogue.json, work/cut/sheet-*.jpg"""
import json, os, subprocess, sys
sys.path.insert(0, "tools")
import build_phil as B
os.makedirs("work/cut/thumbs", exist_ok=True)
dims = {}
def size(p):
    if p not in dims:
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip().split("\n")[0]
        w, h = (int(v) for v in o.split(",")[:2]); dims[p] = (w, h)
    return dims[p]
cat, seen = [], set()
def add(block, brand, product, p, t, beats, x=None, y=None, note=""):
    key = (p, round(t, 2))
    if key in seen: return
    seen.add(key); w, h = size(p); still = B.is_still(p)
    # effective size after the capture clean-up crop
    c = B.CLEAN.get(p)
    if c and c.startswith("crop="): w, h = (int(v) for v in c[5:].split(":")[:2])
    cat.append({"id": f"{block}-{len(cat):03d}", "block": block, "brand": brand, "product": product, "src": p, "t": round(t, 3),
                "kind": "still" if still else "video", "max_s": None if still else round(beats * B.BEAT, 3), "w": w, "h": h,
                "orient": "portrait" if h > w else "landscape", "cx": x, "cy": y, "note": note})
for name, (brand, product, shots, *opt) in B.BLOCKS.items():
    if name in ("stitch", "axia"): pass                                # their shots also live in the Lodes block; keep both
    for s in shots:
        k = s[0]
        if k == "full": add(name, brand, product, s[1], s[2], s[3], None, s[4] if len(s) > 4 else None)
        elif k == "dip": [add(name, brand, product, p, t, s[3]) for (p, t) in (s[1], s[2])]
        elif k == "flick": [add(name, brand, product, p, t, s[2]) for pair in s[1] for (p, t) in pair]
        elif k == "pillars": [add(name, brand, product, c[0], c[1], c[2], c[3] if len(c) > 3 else None) for lane in s[1] for c in lane]
# special assets
SP = [("opening", "KODA", "Desert house LTX (day to Milky Way night; generated concept)", "work/ltx/desert-run1.mp4", 0.0, 9.0),
      ("showroom", "KODA", "Showroom V2, blurred motion, orange KODA mark at 4.8-6.7 s of this window", "src/phil/koda/showroom-v2-capture.mov", 1.95, 7.6)]
for b, br, pr, p, t, d in SP:
    w, h = size(p); cat.append({"id": f"{b}-{len(cat):03d}", "block": b, "brand": br, "product": pr, "src": p, "t": t, "kind": "video", "max_s": d,
                                "w": w, "h": h, "orient": "landscape", "cx": None, "cy": None, "note": "special"})
json.dump(cat, open("work/cut/catalogue.json", "w"), indent=1)
# thumbnails (mid-point, after clean-up crop) and sheets of 40
for e in cat:
    f = f"work/cut/thumbs/{e['id']}.png"
    if os.path.exists(f): continue
    tt = e["t"] + (e["max_s"] / 2 if e["max_s"] else 0)
    pre = B.CLEAN.get(e["src"], "null")
    ins = ["-loop", "1", "-i", e["src"]] if e["kind"] == "still" else ["-ss", f"{tt:.3f}", "-i", e["src"]]
    lab = f"{e['id']} {'S' if e['kind'] == 'still' else 'V'} {e['orient'][0].upper()}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-frames:v", "1", "-vf",
        f"{pre},scale=220:220:force_original_aspect_ratio=decrease,pad=220:220:(ow-iw)/2:(oh-ih)/2:color=0x222222,"
        f"drawtext=fontfile=/System/Library/Fonts/HelveticaNeue.ttc:text='{lab}':x=3:y=3:fontsize=12:fontcolor=yellow:box=1:boxcolor=black@0.7", f], check=True)
for i in range(0, len(cat), 40):
    lst = f"work/cut/sheet-{i // 40 + 1}.txt"; chunk = cat[i:i + 40]
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", f"work/cut/thumbs/{e['id']}.png"] for e in chunk), []), "-filter_complex",
        "".join(f"[{j}:v]" for j in range(len(chunk))) + f"xstack=inputs={len(chunk)}:layout=" + "|".join(f"{(j % 8) * 222}_{(j // 8) * 222}" for j in range(len(chunk))) + ":fill=black",
        "-frames:v", "1", "-q:v", "4", f"work/cut/sheet-{i // 40 + 1}.jpg"], check=True)
print(len(cat), "shots;", sum(e["kind"] == "video" for e in cat), "video;", sum(e["orient"] == "portrait" for e in cat), "portrait; sheets:", (len(cat) + 39) // 40)
