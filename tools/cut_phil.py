"""Render a short cut (sizzle / social) of the KODA x Cosh Living reel from an EDL (JSON), on the Shy Millionaire grid.
  python3 tools/cut_phil.py work/cut/edl-<name>.json [--check]      (--check: validate only, print timing)

EDL:
{
 "name": "sizzle-45", "format": "landscape" | "vertical",
 "music": [ {"track": "shy", "from_bar": 13, "to_bar": 29},            # Shy Millionaire bar ranges, joined on the bar
            {"track": "shy", "from_bar": 76, "to_bar": 80, "tail_s": 1.2},
            {"track": "sugoi", "from_s": 0, "to_s": 15.0} ],              # Sugoi opening (seconds; hit at 11.57 s)
 "shots": [ {"id": "<catalogue id>", "beats": 2, "offset_s": 0.0, "cx": 0.5, "cy": 0.5},     # full frame (landscape or vertical)
            {"pillars": [[{"id": "...", "beats": 2}, ...], [...], [...]], "beats": 8},     # landscape only; each lane sums to beats
            {"special": "opening", "beats": 8},          # desert house LTX, slowed to fill (day to Milky Way night)
            {"special": "sugoi_open"},                   # the finished 15.0 s Sugoi opening (lockup on its hit); pair with sugoi music
            {"special": "flyin", "speed": 4, "hold": 1, "beats": 0},   # Superman fly-in; beats is computed (8/speed + 1/speed... + hold bars)
            {"special": "lockup", "beats": 8, "bg": "night" | "graphite"},   # KODA | coshliving + THE HOME OF BRANDED LIGHTING
            {"seconds": 1.5, "id": "..."} ],             # any shot may give seconds instead of beats (only inside sugoi sections)
 "titles": [ {"layer": "pair" | "pairhobl" | "ltbl", "from_beat": 0, "to_beat": 6} ]   # overlays on the cut's own beat timeline
}
A beat is 60/112.99 s. Shot in-points come from work/cut/catalogue.json (safe windows); offset_s + duration must stay within
max_s for video. Captures keep their clean-up crops. Every clip is normalised (limited range, bt709) as in build_phil."""
import json, os, subprocess, sys
sys.path.insert(0, "tools")
import build_phil as B
EDL = json.load(open(sys.argv[1])); CHECK = "--check" in sys.argv
CAT = {e["id"]: e for e in json.load(open("work/cut/catalogue.json"))}
FPS = 25
TRACKS = {  # file, BPM, bar 0 (s), level  (analysis in docs/phil/REMIX-PLAN.md)
  "shy": ("audio/music-shy-millionaire.mp3", 112.99, 0.465, "volume=-4.6dB"),
  "sugoi": ("audio/music-hiyaku-sugoi.mp3", 106.66, 0.316, "volume=4dB,alimiter=limit=0.89:level=false"),
  "berliner": ("audio/music-berliner-skyline.mp3", 72.67, 0.499, "volume=-4.5dB,alimiter=limit=0.89:level=false"),
  "smiling": ("audio/music-smiling-in-the-rain.mp3", 80.0, 0.094, "volume=-3.5dB,alimiter=limit=0.89:level=false")}
GRID = EDL.get("grid", "shy"); BPM = TRACKS[GRID][1]; BEAT = 60 / BPM; BAR = 4 * BEAT; T0 = TRACKS[GRID][2]
B.BPM, B.BEAT = BPM, BEAT                                               # build_phil cuts frames on this grid too
if not os.path.exists("work/cut/black.png"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x0a0a09:s=1920x1920", "-frames:v", "1", "work/cut/black.png"], check=True)
CAT["BLACK"] = {"id": "BLACK", "src": "work/cut/black.png", "t": 0, "kind": "still", "max_s": None, "cx": None, "cy": None}
for s in EDL["shots"]:                                                  # {"black": beats} = lights off
    if "black" in s: s["id"], s["beats"] = "BLACK", s.pop("black")
VERT = EDL.get("format") == "vertical"
W, H = (1080, 1920) if VERT else (1920, 1080)
B.W, B.H = W, H                                                         # build_phil renders at this size (cache keyed by size)
NAME = EDL["name"]; WD = f"work/cut/{NAME}"; os.makedirs(WD, exist_ok=True)
NORM = f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-an"]
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def title_png(layer, text=""):
    import hashlib
    from urllib.parse import quote
    sc = 0.74 if VERT else 1.0                                          # vertical: about 70% of the width, inside Instagram's safe area
    f = f"work/cut/title-{layer}-{hashlib.md5(text.encode()).hexdigest()[:6] if text else ''}-{W}x{H}-ls{sc}.png"
    if not os.path.exists(f):
        q = f"layer={layer}" + (f"&text={quote(text)}" if text else "") + (f"&w={W}&h={H}&ls={sc}&y={H // 2 + 40}" if VERT else "")
        for _ in range(3):
            try:
                subprocess.run(["node", "render.mjs", "png", "0", f], env={**os.environ, "PAGE": "tools/title.html", "Q": q}, check=True, stdout=subprocess.DEVNULL, timeout=60); break
            except Exception: pass
    return f
# ---- timeline
errors, segs, t_beats, sec = [], [], 0.0, 0.0
def dur_of(s):
    if "special" in s:
        if s["special"] == "sugoi_open": return 15.0
        if s["special"] == "flyin":
            sp = s.get("speed", 4); return (9 / sp + s.get("hold", 1)) * BAR
        return s["beats"] * BEAT
    if "pillars" in s: return s["beats"] * BEAT
    return s["seconds"] if "seconds" in s else s["beats"] * BEAT
for i, s in enumerate(EDL["shots"]):
    d = dur_of(s)
    if "id" in s:
        e = CAT.get(s["id"])
        if not e: errors.append(f"shot {i}: unknown id {s['id']}")
        elif e["kind"] == "video" and s.get("offset_s", 0) + d > e["max_s"] + 0.02:
            errors.append(f"shot {i} {s['id']}: {s.get('offset_s', 0) + d:.2f} s exceeds safe window {e['max_s']:.2f} s")
    if "pillars" in s:
        if VERT: errors.append(f"shot {i}: pillars are landscape-only")
        for li, lane in enumerate(s["pillars"]):
            if abs(sum(c["beats"] for c in lane) - s["beats"]) > 1e-6: errors.append(f"shot {i} lane {li}: beats != {s['beats']}")
            for c in lane:
                e = CAT.get(c["id"])
                if not e: errors.append(f"shot {i} lane {li}: unknown id {c['id']}")
                elif e["kind"] == "video" and c.get("offset_s", 0) + c["beats"] * BEAT > e["max_s"] + 0.02:
                    errors.append(f"shot {i} lane {li} {c['id']}: exceeds safe window")
    segs.append((sec, d)); sec += d
pic = sec
mus = 0.0
for m in EDL["music"]:
    mus += (m["to_bar"] - m["from_bar"]) * 240 / TRACKS[m["track"]][1] + m.get("tail_s", 0) if "from_bar" in m else m["to_s"] - m["from_s"]
print(f"{NAME}: {len(EDL['shots'])} shots, picture {pic:.2f} s, music {mus:.2f} s, {W}x{H}")
if abs(pic - mus) > 0.6: errors.append(f"picture {pic:.2f} s and music {mus:.2f} s differ by more than 0.6 s")
if errors:
    print("ERRORS:\n  " + "\n  ".join(errors)); sys.exit(1)
if CHECK: sys.exit(0)
# ---- render shots (frames on cumulative edges of the cut timeline)
def fr(t): return round(t * FPS)
parts = []
for i, ((t0, d), s) in enumerate(zip(segs, EDL["shots"])):
    n = fr(t0 + d) - fr(t0); out = f"{WD}/s{i:03d}.mp4"
    if "id" in s:
        e = CAT[s["id"]]; cy = s.get("cy", e["cy"] if e["cy"] is not None else 0.5); cx = s.get("cx", e["cx"] if e["cx"] is not None else 0.5)
        tmp = B.render(("full", e["src"], e["t"] + s.get("offset_s", 0), d / BEAT, cy, cx), f"{WD}/r{i:03d}.mp4")
        fl = ",fade=t=in:st=0:d=0.16:color=0xf3eee4" if s.get("flash") else ""
        run(["-i", tmp, "-filter_complex", f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration=1{fl}[v]", "-map", "[v]", "-frames:v", str(n), *ENC, out])
    elif "pillars" in s:
        lanes = [[(CAT[c["id"]]["src"], CAT[c["id"]]["t"] + c.get("offset_s", 0), c["beats"], c.get("cx", CAT[c["id"]]["cx"] if CAT[c["id"]]["cx"] is not None else 0.5)) for c in lane] for lane in s["pillars"]]
        tmp = B.render(("pillars", lanes, s["beats"]), f"{WD}/r{i:03d}.mp4")
        run(["-i", tmp, "-filter_complex", f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration=1[v]", "-map", "[v]", "-frames:v", str(n), *ENC, out])
    elif s["special"] == "opening":
        slow = d / 9.0
        run(["-i", "work/ltx/desert-run1.mp4", "-filter_complex", f"[0:v]setpts=PTS*{slow:.4f},framerate=fps={FPS}:interp_start=0:interp_end=255,"
             f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{NORM},tpad=stop_mode=clone:stop_duration=1[v]", "-map", "[v]", "-frames:v", str(n), *ENC, out])
    elif s["special"] == "sugoi_open":
        run(["-i", "out/phil-broll-sugoi-15s-clean.mp4", "-filter_complex",
             f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{NORM}[v]" if VERT else f"[0:v]{NORM}[v]",
             "-map", "[v]", "-frames:v", str(n), *ENC, out])
    elif s["special"] == "flyin":
        sp, hold = s.get("speed", 4), s.get("hold", 1); fly = f"work/cut/flyin-{sp}x-{hold}-{BPM}.mp4"
        if not os.path.exists(fly):
            subprocess.run(["node", "render.mjs", "encode", fly], env={**os.environ, "PAGE": "tools/logowall.html", "Q": f"bpm={BPM}&speed={sp}&hold={hold}", "CRF": "15"}, check=True)
        vf = f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration=2[v]" if not VERT else \
             f"[0:v]scale={W}:-2:flags=lanczos,pad={W}:{H}:0:(oh-ih)/2:color=0x1b1a18,{NORM},tpad=stop_mode=clone:stop_duration=2[v]"
        run(["-i", fly, "-filter_complex", vf, "-map", "[v]", "-frames:v", str(n), *ENC, out])
    elif s["special"] == "lockup":
        D = n / FPS; bg = s.get("bg", "night")
        src = ["-sseof", "-0.04", "-i", "work/ltx/desert-run1.mp4"] if bg == "night" else ["-f", "lavfi", "-i", f"color=c=0x1b1a18:s={W}x{H}:r={FPS}"]
        bgf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{NORM},tpad=stop_mode=clone:stop_duration={D + 1:.2f},eq=brightness=-0.04[bg]"
        run([*src, "-loop", "1", "-i", title_png("pair"), "-loop", "1", "-i", title_png("pairhobl"), "-filter_complex",
             bgf + f";[1:v]format=rgba,fade=t=in:st=0.1:d=0.5:alpha=1[t1];[2:v]format=rgba,fade=t=in:st={min(2 * BEAT, D / 3):.3f}:d=0.5:alpha=1[t2];"
             f"[bg][t1]overlay[o];[o][t2]overlay,fade=t=out:st={max(0, D - 1.0):.2f}:d=1.0[v]", "-map", "[v]", "-frames:v", str(n), *ENC, out])
    parts.append(out)
lst = f"{WD}/parts.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{WD}/picture.mp4"])
P = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{WD}/picture.mp4"]))
# ---- title overlays on the cut timeline
pic_in = f"{WD}/picture.mp4"
if EDL.get("titles"):
    ins, fc, last = ["-i", pic_in], "", "0:v"
    for j, tl in enumerate(EDL["titles"]):
        a, b = tl["from_beat"] * BEAT, tl["to_beat"] * BEAT
        ins += ["-loop", "1", "-i", title_png(tl["layer"], tl.get("text", ""))]; fd = tl.get("fade", 0.45)
        fc += f"[{j + 1}:v]format=rgba,fade=t=in:st={a:.3f}:d={fd}:alpha=1,fade=t=out:st={b - fd:.3f}:d={fd}:alpha=1[t{j}];[{last}][t{j}]overlay=shortest=1[o{j}];"
        last = f"o{j}"
    run([*ins, "-filter_complex", fc + f"[{last}]format=yuv420p[v]", "-map", "[v]", *ENC, f"{WD}/picture-t.mp4"]); pic_in = f"{WD}/picture-t.mp4"
# ---- music: segments joined on the bar (30 ms crossfades)
ins, fc = [], ""
for k, m in enumerate(EDL["music"]):
    tf, tb, t0, lvl = TRACKS[m["track"]]; ins += ["-i", tf]
    if "from_bar" in m:
        a, b = t0 + m["from_bar"] * 240 / tb, t0 + m["to_bar"] * 240 / tb + m.get("tail_s", 0)
        fc += f"[{k}:a]atrim={a:.4f}:{b + 0.03:.4f},asetpts=PTS-STARTPTS,{lvl}[m{k}];"
    else:
        fc += f"[{k}:a]atrim={m['from_s']:.4f}:{m['to_s']:.4f},asetpts=PTS-STARTPTS,{lvl},afade=t=out:st={m['to_s'] - m['from_s'] - 0.25:.3f}:d=0.25[m{k}];"
cur = "m0"
for k in range(1, len(EDL["music"])):
    if "from_bar" in EDL["music"][k] and "from_bar" in EDL["music"][k - 1] and EDL["music"][k]["track"] == EDL["music"][k - 1]["track"]:
        fc += f"[{cur}][m{k}]acrossfade=d=0.03:c1=tri:c2=tri[x{k}];"
    else:
        fc += f"[{cur}][m{k}]concat=n=2:v=0:a=1[x{k}];"
    cur = f"x{k}"
fc += f"[{cur}]afade=t=in:st=0:d=0.05,afade=t=out:st={P - 0.9:.2f}:d=0.9[a]"
run([*ins, "-filter_complex", fc, "-map", "[a]", "-t", f"{P:.3f}", "-c:a", "pcm_s16le", f"{WD}/music.wav"])
out = f"out/phil-{NAME}.mp4"
run(["-i", pic_in, "-i", f"{WD}/music.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-t", f"{P:.3f}", "-movflags", "+faststart", out])
print(f"wrote {out}: {P:.2f} s")
