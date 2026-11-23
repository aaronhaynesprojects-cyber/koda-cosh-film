"""KODA x Cosh Living, Phil revision: hero-light montage assembler (ffmpeg). Every shot is laid out in bars of the music
grid, so the whole montage re-times when Aaron's final track arrives (change BPM). Manufacturer films and photos only;
stills are held (no fake moves); portrait sources run as diptych panels on graphite.

Shot kinds (durations in beats):
  ("full",  src, t_in, beats)                         one source filling 1920x1080 (stills or video)
  ("dip",   (srcL, inL), (srcR, inR), beats)          two 3:4 portrait panels side by side
  ("flick", [((srcL, inL), (srcR, inR)), ...], beats_each)  pairs of portrait selects, both panels cutting together
  ("clip",  mp4, t_in, beats)                         a finished 1920x1080 clip (fly-in, establishing shot)
A block is (caption_brand, caption_product, [shots]); the caption sits over the block's first two bars.
  python3 tools/build_phil.py <block-name|all> [out.mp4]"""
import json, os, subprocess, sys
FPS, W, H = 25, 1920, 1080
BPM = 112; BEAT = 60 / BPM
GRAPHITE = "0x1b1a18"; PW, PH, GUT = 810, 1080, 24                  # 3:4 panels, full height
PX = [(W - 2 * PW - GUT) // 2, (W - 2 * PW - GUT) // 2 + PW + GUT]  # left, right panel x
AX = "src/phil/lodes/axia/"
SEL = json.load(open("docs/phil/axia-milan-selects.json"))
MIL = {k: (SEL["source"], a) for k, a, b, _ in SEL["selects"]}
# per-source crops to 3:4 (screen captures carry a thin UI strip at the top)
CROP = {AX + "axia-screen-capture-portrait.mov": "crop=774:1032:0:100", SEL["source"]: "crop=700:933:2:8",
        "src/phil/lodes/stitch/stitch-film-capture.mov": "crop=760:1013:2:6"}
ST = "src/phil/lodes/stitch/"; STF = ST + "stitch-film-capture.mov"   # Aaron's capture of the Lodes Stitch film; first pass only (0-16 s)
RD = "src/phil/lodes/random/"; RDF = RD + "random-cloud-film-capture.mov"  # Lodes Random Cloud film: shadows to dusk to light on, 0-13.7 s
AXF = AX + "axia-screen-capture-portrait.mov"
CO = "src/phil/a-n-d/column/"; CF = CO + "column-film-capture.mov"   # A-N-D Column film (capture), shots ~2 s
BI = "src/phil/brokis/ivy/brokis-site/Brokis_IVY_HORIZONTAL_"
AF = "src/video/koda-home-5.mp4"; AS = CO + "and-site/"            # A-N-D's 1080p homepage film; A-N-D's own project photos (credited)
# PILLARS (Aaron, 24 Nov): one block per brand, three 9:16-ish portrait streams playing at once, each cutting on its own beats.
NP, PG = 3, 12; PPW = (W - (NP - 1) * PG) // NP                    # 632 x 1080 pillars, 12 px graphite gutters
CLEAN = {AXF: "crop=770:1222:2:6", SEL["source"]: "crop=700:936:2:6", STF: "crop=760:1018:2:6",
         ST + "stitch-film-capture-wide.mov": "crop=760:1256:2:4", RDF: "crop=760:1256:2:4",
         RD + "random-cloud-capture-2.mov": "crop=774:1262:2:4", RD + "random-solo-capture.mov": "crop=700:954:2:4",
         "src/phil/a-n-d/column/column-film-capture.mov": "crop=764:1280:2:4"}   # strip capture edges / UI
BLOCKS = {
  "stitch": ("Lodes", "Stitch", [                                  # caption right: the terrace lanterns sit lower left
    ("full", ST + "stitch-01.jpg", 0, 6),
    ("dip", (STF, 3.70), (STF, 12.30), 6),                          # film: pergola lounge | dining under three pendants
    ("dip", (STF, 7.75), (ST + "stitch-05.jpg", 0), 4)], "r"),      # film: floor lantern by the bench | pendant pair
  "lodes": ("Lodes", "Stitch  ·  Axia  ·  Random", [               # lanes: Stitch | Axia | Random, staggered cuts
    ("pillars", [
      [(STF, 3.70, 7), (STF, 12.25, 7), (STF, 7.75, 5), (ST + "stitch-01.jpg", 0, 5, 0.1)],
      [(AXF, 0.2, 8), (*MIL["D"], 1), (*MIL["F"], 1), (*MIL["G"], 1), (*MIL["K"], 1), (AXF, 6.0, 8), (AX + "axia-05.png", 0, 4, 0.33)],
      [(RDF, 4.9, 16), (RD + "random-cloud-capture-2.mov", 6.3, 4), (RD + "random-solo-capture.mov", 20.15, 4)]], 24),
    ("full", RD + "random-cloud-hallways-clean.mp4", 0.55, 8)]),     # Random Cloud hallways (YouTube capture, icon-free part), stone to trees
  "and": ("A-N-D", "Column", [                                    # horizontal Column leads: A-N-D's film, then pillars, then amber in situ
    ("full", CO + "column-20.png", 0, 4, 0.45),                     # Aaron's reference: amber Column over the dining table (KODA still 20)
    ("full", AF, 10.24, 2),                                         # A-N-D film: showroom, long horizontal Column + amber vertical
    ("pillars", [
      [(CF, 7.20, 3), (CF, 9.25, 3), (CF, 21.40, 3), (CF, 11.25, 3)],
      [(CO + "column-21.png", 0, 4, 0.4), (CF, 23.10, 3), (CF, 15.20, 3), (CF, 5.50, 2)],
      [(AS + "A-N-D_Column_COSSeoul_PhotoByStudioBrinth_3-WEB.jpg", 0, 4), (CF, 0.05, 2),
       (AS + "A-N-D_Column_Massara_SarahCarpenterStudio_PhotoByBrianFerry_2-WEB.jpg", 0, 3), (CF, 25.10, 3)]], 12),
    ("full", AF, 8.64, 1),                                          # A-N-D film: macro along the horizontal tube
    ("full", AF, 5.52, 1)]),                                        # A-N-D film: clear ribbed segments, close
  "ivy": ("Brokis", "Ivy Horizontal", [                          # Brokis image bank (PF203), 6000-8700 px; no film. Horizontal: full-frame
    ("full", BI + "PC1065_PC1066_PC1067_PC1070__PH8265_c_Suprema_full.jpg", 0, 4),   # lounge, open space
    ("full", BI + "PC1070__PH1466_c_Martin_Chum_full.jpg", 0, 2),                    # Aaron's reference: on dark grey
    ("full", BI + "PC1069_PC1068__PH1397_c_Martin_Chum_full.jpg", 0, 2),             # over the dining table
    ("full", BI + "PC1070_PC1069__PH7568_c_Martin_Chum_full.jpg", 0, 2),             # garden pavilion
    ("full", BI + "PC1070_PC1069__PH7569_c_Martin_Chum_full.jpg", 0, 2),             # stone and glass, garden
    ("dip", (BI + "PC1068__PH1396_c_Martin_Chum_full.jpg", 0), (BI + "PC1065_PC1066__PH1328_c_Martin_Chum_full.jpg", 0), 4)]),
  "pantaya": ("Pablo", "Pantaya", [                               # Pablo's 1080p film (KODA homepage, Vimeo 1245314168)
    ("full", "src/video/koda-home-7.mp4", 14.60, 4),                # dining room, long table
    ("full", "src/video/koda-home-7.mp4", 28.75, 4),                # the trio glowing
    ("full", "src/video/koda-home-7.mp4", 41.95, 2),                # green, over the artwork
    ("full", "src/video/koda-home-7.mp4", 51.35, 2)]),              # blue, in the dark
  "axia": ("Lodes", "Axia", [
    ("dip", (AX + "axia-screen-capture-portrait.mov", 0.2), (AX + "axia-02.png", 0), 8),
    ("flick", [(MIL["D"], MIL["F"]), (MIL["G"], MIL["K"]), (MIL["A"], MIL["B"]), (MIL["E"], (AX + "axia-screen-capture-portrait.mov", 8.6))], 1),
    ("full", AX + "axia-05.png", 0, 8)]),
}
STILL = (".png", ".jpg", ".jpeg", ".webp")
def is_still(p): return p.lower().endswith(STILL)
def nfr(beats, b0=0): return round((b0 + beats) * BEAT * FPS) - round(b0 * BEAT * FPS)   # frames on cumulative beat edges
def src_args(p, t, n):
    return (["-loop", "1", "-framerate", str(FPS), "-i", p] if is_still(p) else ["-ss", f"{t:.3f}", "-i", p])
def panel(p, i):
    c = CROP.get(p, "crop=iw:iw*4/3:0:(ih-iw*4/3)/2" if not is_still(p) else "crop='min(iw,ih*3/4)':'min(ih,iw*4/3)'")
    return f"[{i}:v]{c},scale={PW}:{PH}:flags=lanczos,fps={FPS},setsar=1"
def render(shot, out, b0=0):
    import hashlib                                                   # cache: a shot is re-rendered only when its spec or timing changes
    out = out.replace(".mp4", "-" + hashlib.md5(repr((shot, b0, BPM, FPS, "v2" if shot[0] == "pillars" else "")).encode()).hexdigest()[:8] + ".mp4")
    if os.path.exists(out): return out
    kind, n = shot[0], None
    if kind == "full":
        _, p, t, beats, *cy = shot; n = nfr(beats, b0); cy = cy[0] if cy else 0.5     # cy: vertical crop position (0 top, 1 bottom)
        vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:(iw-ow)/2:(ih-oh)*{cy},fps={FPS},setsar=1[v]"
        ins = src_args(p, t, n)
    elif kind == "clip":
        _, p, t, beats = shot; n = nfr(beats, b0); ins = ["-ss", f"{t:.3f}", "-i", p]; vf = f"[0:v]fps={FPS},setsar=1[v]"
    elif kind == "dip":
        _, (pl, tl), (pr, tr), beats = shot; n = nfr(beats, b0)
        ins = ["-f", "lavfi", "-i", f"color=c={GRAPHITE}:s={W}x{H}:r={FPS}"] + src_args(pl, tl, n) + src_args(pr, tr, n)
        vf = f"{panel(pl, 1)}[l];{panel(pr, 2)}[r];[0:v][l]overlay={PX[0]}:0[a];[a][r]overlay={PX[1]}:0[v]"
    elif kind == "pillars":                                          # each lane rendered as its own pillar, then laid side by side
        _, lanes, beats = shot; n = nfr(beats, b0); lp = []
        for li, lane in enumerate(lanes):
            assert sum(c[2] for c in lane) == beats, (li, sum(c[2] for c in lane), beats)
            parts, lb = [], b0
            for ci, (p, t, bt, *cx) in enumerate(lane):
                f = out.replace(".mp4", f"-L{li}-{ci}.mp4"); m = nfr(bt, lb); a = PPW / H; x = cx[0] if cx else 0.5
                pre = CLEAN.get(p, "null")
                vf1 = (f"[0:v]{pre},crop=w='min(iw,ih*{a:.5f})':h='min(ih,iw/{a:.5f})':x='(iw-ow)*{x}':y='(ih-oh)/2',"
                       f"scale={PPW}:{H}:flags=lanczos,fps={FPS},setsar=1[v]")
                subprocess.run(["ffmpeg", "-v", "error", "-y", *src_args(p, t, m), "-filter_complex", vf1, "-map", "[v]", "-frames:v", str(m), "-an",
                                "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", f], check=True)
                parts.append(f); lb += bt
            lf = out.replace(".mp4", f"-L{li}.mp4"); concat(parts, lf); lp.append(lf)
        ins = ["-f", "lavfi", "-i", f"color=c={GRAPHITE}:s={W}x{H}:r={FPS}"] + sum((["-i", f] for f in lp), [])
        vf = "".join(f"[{i + 1}:v]setpts=N/({FPS}*TB)[p{i}];" for i in range(len(lp)))       # re-time lanes by frame number (joins jitter)
        vf += "".join(f"[{'0:v' if i == 0 else f'o{i}'}][p{i}]overlay={i * (PPW + PG)}:0:eof_action=repeat[o{i + 1}];" for i in range(len(lp)))
        vf = vf.rstrip(";").rsplit("[", 1)[0] + "[v]"
    elif kind == "flick":
        _, pairs, each = shot
        parts = [render(("dip", l, r, each), out.replace(".mp4", f"-{j}.mp4"), b0 + j * each) for j, (l, r) in enumerate(pairs)]
        concat(parts, out); return out
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", vf, "-map", "[v]", "-frames:v", str(n), "-an",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", out], check=True)
    return out
def concat(parts, out):
    lst = out + ".txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True); os.remove(lst)
def caption_png(b, p, side="l"):
    import hashlib
    from urllib.parse import quote
    f = "work/phil/cap-" + hashlib.md5(f"{b}|{p}|{side}".encode()).hexdigest()[:10] + ".png"
    for attempt in range(3):                                         # headless Chrome occasionally stalls: time out and retry
        if os.path.exists(f): break
        try: subprocess.run(["node", "render.mjs", "png", "0", f], env={**os.environ, "PAGE": "tools/caption.html", "Q": f"b={quote(b)}&p={quote(p)}&side={side}"},
                            check=True, stdout=subprocess.DEVNULL, timeout=60)
        except subprocess.TimeoutExpired: subprocess.run(["pkill", "-f", "render.mjs png 0 " + f])
    return f
def block(name):
    b, p, shots, *opt = BLOCKS[name]; os.makedirs("work/phil", exist_ok=True)
    parts, b0 = [], 0
    for i, s in enumerate(shots):
        parts.append(render(s, f"work/phil/{name}-{i:02d}.mp4", b0)); b0 += s[-1] * (len(s[1]) if s[0] == "flick" else 1)
    raw = f"work/phil/{name}-raw.mp4"; concat(parts, raw); out = f"work/phil/{name}.mp4"
    cap, t1 = caption_png(b, p, opt[0] if opt else "l"), 2 * 4 * BEAT                       # caption over the first two bars
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-loop", "1", "-framerate", str(FPS), "-i", cap, "-filter_complex",
                    f"[1:v]format=rgba,fade=t=in:st=0.25:d=0.5:alpha=1,fade=t=out:st={t1 - 0.5:.2f}:d=0.5:alpha=1[c];[0:v][c]overlay=0:0:shortest=1,format=yuv420p[v]",
                    "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "12", out], check=True)
    return out
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outs = [block(k) for k in (BLOCKS if which == "all" else [which])]
    print("\n".join(outs))
