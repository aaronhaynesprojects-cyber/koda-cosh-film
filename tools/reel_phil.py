"""KODA x Cosh Living, Phil revision: assemble the full reel on "Shy Millionaire" (Aaron, 24 Nov 2026).
Every segment sits on exact bar edges of the track (112.99 BPM, bar 0 at 0.465 s in the file). No First Creek run-in.

  bars  0-7    Desert house (LTX take 1, slowed to fill the intro); "Let There Be Light", then the lockup:
               KODA logo / THE HOME OF BRANDED LIGHTING / AT coshliving
  bars  7-52   Brand montage (revision 2: music bars 44-48 skipped; picture bars below are music bars) (blocks from tools/build_phil.py; a missing block becomes a labelled placeholder card)
  bars 56-59.5 KODA showroom V2 (Aaron's capture, blurred motion) in the breakdown; THE HOME OF BRANDED LIGHTING
               completes the KODA mark when it appears
  bars 59.5-68 Superman fly-in at double speed; the board lands on the return (bar 64) and holds
  bars 68-     End card: the lockup over the Milky Way, on the track's own ending (music jumps bar 68 -> bar 76)

  python3 tools/reel_phil.py [--clean]     (--clean: no "Concept visualisation" label on the generated opening)"""
import os, subprocess, sys
FPS, W, H = 25, 1920, 1080
BPM = 112.99; BAR = 240 / BPM; T0 = 0.465
MUSIC = "audio/music-shy-millionaire.mp3"
LTX = "work/ltx/desert-run1.mp4"
SHOWROOM = "src/phil/koda/showroom-v2-capture.mov"
FLY = "work/reel/flyin-2x.mp4"
T = {k: f"work/reel/title-{k}.png" for k in ("pair", "pairhobl", "ltbl")}
VERSION_B = "--b" in sys.argv                                         # Final Version "B": the Sugoi B-roll opens the feature
SUGOI = "audio/music-hiyaku-sugoi.mp3"
HOBL_LOW = "work/reel/title-hobl-low.png"
# Revision 2 (Phil's call and Aaron's notes, 25 Nov 2026): the Clouds bar block is out, Charlotte is cut back to one image,
# MUG's new Celine follows it, and Mori loses its bar shot. The montage is 4 bars shorter, so the music jumps bar 44 -> 48
# on the cut into MUG (bars 40-47 and 48-55 are the same 8-bar phrase), and everything after keeps its musical mark.
MONTAGE = [("lodes", 8), ("and", 5), ("ivy", 4), ("pantaya", 5), ("cilia", 4), ("tempo", 4), ("nevo", 3),
           ("totem", 4), ("charlotte", 1.5), ("celine", 2.5), ("mori", 4)]
CUT, JUMP = 4, 44                     # bars removed from the montage; picture bar where the music jumps ahead by CUT bars
NAMES = {"celine": "MUG · Celine", "cilia": "David Pompa · Cilia", "tempo": "a-emotional light · Tempo", "clouds": "a-emotional light · Clouds",
         "totem": "Pablo · Totem", "charlotte": "MUG · Charlotte", "mori": "RBW · Mori"}
CLEAN = "--clean" in sys.argv
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
os.makedirs("work/reel", exist_ok=True)
def fr(bars): return round(bars * BAR * FPS)
def nframes(a, b): return fr(b) - fr(a)
def run(args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-an"]
NORM = f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
def fade(i, a, b, fi=0.6, fo=0.6):     # overlay input i visible a..b with fades
    return f"[{i}:v]format=rgba,fade=t=in:st={a:.3f}:d={fi}:alpha=1,fade=t=out:st={b - fo:.3f}:d={fo}:alpha=1[t{i}]"
segs = []
# ---- 1. opening, bars 0-7
n = nframes(0, 7); D = n / FPS; slow = D / 9.0
f = "work/reel/s01-opening.mp4"
lab = "" if CLEAN else f",drawtext=fontfile={FONT}:text='Concept visualisation':fontcolor=0xf3eee4:alpha=0.7:fontsize=19:x=w-tw-64:y=h-54"
b = lambda x: x * BAR
if VERSION_B:                                                        # Sugoi opening (15.0 s, lockup on Sugoi's hit at 11.57 s)
    src = "out/phil-broll-sugoi-15s-" + ("clean" if CLEAN else "review") + ".mp4"; OPEN_N = round(15.0 * FPS)
    run(["-i", src, "-filter_complex", f"[0:v]{NORM}[v]", "-map", "[v]", "-frames:v", str(OPEN_N), *ENC, f])
else:
    OPEN_N = n
    run(["-i", LTX, "-loop", "1", "-i", T["ltbl"], "-loop", "1", "-i", T["pair"], "-loop", "1", "-i", T["pairhobl"], "-filter_complex",
         f"[0:v]setpts=PTS*{slow:.4f},framerate=fps={FPS}:interp_start=0:interp_end=255,{NORM}[bg];"
         + ";".join([fade(1, b(2.25), b(4.0)), fade(2, b(4.25), b(6.85), 0.8), fade(3, b(4.75), b(6.85))])
         + f";[bg][t1]overlay[o1];[o1][t2]overlay[o2];[o2][t3]overlay{lab},fade=t=in:st=0:d=0.5[v]",
         "-map", "[v]", "-frames:v", str(n), *ENC, f])
segs.append(f)
# ---- 2. montage, bars 7-56
bar = 7
for name, bars in MONTAGE:
    n = nframes(bar, bar + bars); f = f"work/reel/s02-{name}.mp4"; src = f"work/phil/{name}.mp4"
    if os.path.exists(src):
        run(["-i", src, "-filter_complex", f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration=1[v]", "-map", "[v]", "-frames:v", str(n), *ENC, f])
    else:
        txt = f"ASSET NEEDED · {NAMES.get(name, name)}"
        run(["-f", "lavfi", "-i", f"color=c=0x1b1a18:s={W}x{H}:r={FPS}", "-vf",
             f"drawtext=fontfile={FONT}:text='{txt}':fontcolor=0xcfc6b6:fontsize=34:x=(w-tw)/2:y=(h-th)/2,{NORM}", "-frames:v", str(n), *ENC, f])
    segs.append(f); bar += bars
assert bar == 56 - CUT, bar
# ---- 3. showroom V2, bars 56-59.5 of the music
n = nframes(56 - CUT, 59.5 - CUT); f = "work/reel/s03-showroom.mp4"
if not os.path.exists(HOBL_LOW):
    subprocess.run(["node", "render.mjs", "png", "0", HOBL_LOW], env={**os.environ, "PAGE": "tools/title.html", "Q": "layer=hobl&y=680"}, check=True, stdout=subprocess.DEVNULL)
run(["-ss", "1.95", "-i", SHOWROOM, "-loop", "1", "-i", HOBL_LOW, "-filter_complex",
     f"[0:v]crop=2700:1519:65:60,{NORM}[bg];" + fade(1, 4.85, n / FPS + 0.6, 0.7) + ";[bg][t1]overlay[v]",
     "-map", "[v]", "-frames:v", str(n), *ENC, f]); segs.append(f)
# ---- 4. fly-in at double speed, bars 59.5-68 of the music
n = nframes(59.5 - CUT, 68 - CUT); f = "work/reel/s04-flyin.mp4"
run(["-i", FLY, "-filter_complex", f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration=1[v]", "-map", "[v]", "-frames:v", str(n), *ENC, f]); segs.append(f)
# ---- 5. end card, bars 68-72 plus the track's tail
tail = 1.2; n = nframes(68 - CUT, 72 - CUT) + round(tail * FPS); D = n / FPS; f = "work/reel/s05-endcard.mp4"
run(["-sseof", "-0.04", "-i", LTX, "-loop", "1", "-i", T["pair"], "-loop", "1", "-i", T["pairhobl"], "-filter_complex",
     f"[0:v]{NORM},tpad=stop_mode=clone:stop_duration={D + 1:.2f},eq=brightness=-0.04[bg];"
     + ";".join([fade(1, 0.2, D + 5, 0.8), fade(2, b(0.75), D + 5)])
     + f";[bg][t1]overlay[o1];[o1][t2]overlay{lab},fade=t=out:st={D - 1.6:.2f}:d=1.6[v]",
     "-map", "[v]", "-frames:v", str(n), *ENC, f]); segs.append(f)
# ---- picture: concat
lst = "work/reel/segs.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "work/reel/picture.mp4"])
P = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "work/reel/picture.mp4"]))
# ---- music: bars 0-44, 48-68, then bars 76 to the end (bar-aligned jumps; the last one to the track's own ending)
a0, aj0, aj1, a1, a2 = T0, T0 + JUMP * BAR, T0 + (JUMP + CUT) * BAR, T0 + 68 * BAR, T0 + 76 * BAR
out = "out/phil-final-v2" + ("-B-sugoi-open" if VERSION_B else "") + ("-clean" if CLEAN else "-review") + ".mp4"
XF = "acrossfade=d=0.03:c1=tri:c2=tri"
if VERSION_B:                    # Sugoi for the opening 15 s (its own fade), handing over to Shy Millionaire at bar 7 as the montage starts
    a7 = T0 + 7 * BAR; ob = OPEN_N / FPS
    af = (f"[3:a]atrim=0:{ob:.4f},asetpts=PTS-STARTPTS,volume=4dB,alimiter=limit=0.89:level=false,afade=t=out:st={ob - 0.25:.3f}:d=0.25[s0];"
          f"[1:a]atrim={a7:.4f}:{aj0 + 0.03:.4f},asetpts=PTS-STARTPTS,volume=-4.6dB[m0];[1:a]atrim={aj1:.4f}:{a1 + 0.03:.4f},asetpts=PTS-STARTPTS,volume=-4.6dB[m1];"
          f"[2:a]atrim={a2:.4f},asetpts=PTS-STARTPTS,volume=-4.6dB[m2];"
          f"[m0][m1]{XF}[mj];[mj][m2]{XF}[m];[s0][m]concat=n=2:v=0:a=1,afade=t=out:st={P - 1.4:.2f}:d=1.4[a]")
else:
    af = (f"[1:a]atrim={a0:.4f}:{aj0 + 0.03:.4f},asetpts=PTS-STARTPTS[m0];[1:a]atrim={aj1:.4f}:{a1 + 0.03:.4f},asetpts=PTS-STARTPTS[m1];"
          f"[2:a]atrim={a2:.4f},asetpts=PTS-STARTPTS[m2];"
          f"[m0][m1]{XF}[mj];[mj][m2]{XF},volume=-4.6dB,afade=t=out:st={P - 1.4:.2f}:d=1.4[a]")
run(["-i", "work/reel/picture.mp4", "-i", MUSIC, "-i", MUSIC, "-i", SUGOI, "-filter_complex", af,
     "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-t", f"{P:.3f}", "-movflags", "+faststart", out])
print(f"wrote {out}: {P:.2f} s ({int(P // 60)}:{P % 60:04.1f}); montage blocks missing: {[m for m, _ in MONTAGE if not os.path.exists(f'work/phil/{m}.mp4')]}")
