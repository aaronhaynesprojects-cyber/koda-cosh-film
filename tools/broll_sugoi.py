"""15 s B-roll on Hiyaku "Sugoi" (Aaron, 24 Nov 2026): the desert house LTX shot slowed across 15 s (star reveal, darkness
rising), the KODA main title landing on the track's first hit (bar 5 = 11.57 s; 106.66 BPM, first beat 0.316 s), then
the KODA | coshliving partnership lockup on the hit, THE HOME OF BRANDED LIGHTING on the next beat.   python3 tools/broll_sugoi.py [--clean]"""
import subprocess, sys
FPS, D = 25, 15.0
BEAT = 60 / 106.66; HIT = 0.316 + 5 * 4 * BEAT
CLEAN = "--clean" in sys.argv; FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
NORM = "fps=25,scale=1920:1080:flags=lanczos,setsar=1,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
def fade(i, a, fi=0.7): return f"[{i}:v]format=rgba,fade=t=in:st={a:.3f}:d={fi}:alpha=1[t{i}]"
lab = "" if CLEAN else f",drawtext=fontfile={FONT}:text='Concept visualisation':fontcolor=0xf3eee4:alpha=0.7:fontsize=19:x=w-tw-64:y=h-54"
out = "out/phil-broll-sugoi-15s" + ("-clean" if CLEAN else "-review") + ".mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/ltx/desert-run1.mp4", "-loop", "1", "-i", "work/reel/title-pair.png", "-loop", "1", "-i", "work/reel/title-pairhobl.png",
    "-i", "audio/music-hiyaku-sugoi.mp3", "-filter_complex",
    f"[0:v]setpts=PTS*{D / 9.0:.4f},framerate=fps={FPS}:interp_start=0:interp_end=255,{NORM},tpad=stop_mode=clone:stop_duration=1[bg];"
    + ";".join([fade(1, HIT - 0.15, 0.5), fade(2, HIT + BEAT)])
    + f";[bg][t1]overlay[o1];[o1][t2]overlay{lab},fade=t=in:st=0:d=0.6[v];[3:a]atrim=0:{D},volume=4dB,alimiter=limit=0.89:level=false,afade=t=out:st={D - 1.2}:d=1.2[a]",
    "-map", "[v]", "-map", "[a]", "-t", str(D), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k",
    "-movflags", "+faststart", out], check=True)
print("wrote", out, f"(title on the hit at {HIT:.2f} s)")
