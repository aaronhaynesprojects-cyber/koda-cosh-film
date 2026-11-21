"""Contact sheets of a previews folder, darkest first, each tile numbered with its dusk score.
Writes <brand>/sheets/sheet-NN.jpg and sheets/index.json (tile number -> file).
Usage: python tools/sheet.py <brand-dir> [per-sheet=30] [cols=6]"""
import sys, os, json, subprocess
d = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 30; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
tri = json.load(open(os.path.join(d, "triage.json"))); items = sorted(tri.items(), key=lambda kv: -kv[1]["dusk"])
os.makedirs(os.path.join(d, "sheets"), exist_ok=True); index = {}
for s in range(0, len(items), per):
    chunk = items[s:s + per]; ins = []; fl = []
    for j, (f, v) in enumerate(chunk):
        n = s + j; index[n] = f; ins += ["-i", os.path.join(d, "previews", f)]
        fl.append(f"[{j}:v]scale=398:265:force_original_aspect_ratio=decrease,pad=400:267:(ow-iw)/2:(oh-ih)/2:color=0x202020,drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:text='{n}  {round(v['dusk'])}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.7[a{j}]")
    lay = "|".join(f"{(j % cols) * 400}_{(j // cols) * 267}" for j in range(len(chunk)))
    fc = ";".join(fl) + ";" + "".join(f"[a{j}]" for j in range(len(chunk))) + f"xstack=inputs={len(chunk)}:layout={lay}:fill=0x101010"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-frames:v", "1", "-q:v", "4", os.path.join(d, "sheets", f"sheet-{s // per:02d}.jpg")], stderr=subprocess.DEVNULL)
json.dump(index, open(os.path.join(d, "sheets", "index.json"), "w"), indent=0); print(d, len(items), "tiles,", (len(items) + per - 1) // per, "sheets")
