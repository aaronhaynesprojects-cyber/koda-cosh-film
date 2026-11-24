"""Rough preview of the Phil reel so far: establishing shot (trimmed to 4 bars) + brands fly-in + brand blocks, on the
Rocket Jr placeholder from bar 0, so every section starts on a downbeat. Then the First Creek run-in and countdown.
  python3 tools/preview_phil.py [blocks...]"""
import subprocess, sys, os
BEAT = 60 / 112; BAR = 4 * BEAT; FPS = 25
blocks = sys.argv[1:] or ["lodes", "and", "ivy", "pantaya"]
parts = [("out/phil-establishing-ltx-take1-review.mp4", 4 * BAR), ("out/phil-brands-flyin-clean.mp4", None)] + [(f"work/phil/{b}.mp4", None) for b in blocks]
ins, fc = [], ""
for i, (p, d) in enumerate(parts):
    ins += ["-i", p]; fc += f"[{i}:v]" + (f"trim=duration={d:.4f}," if d else "") + f"setpts=PTS-STARTPTS,fps={FPS},scale=1920:1080,setsar=1,format=yuv420p[v{i}];"
fc += "".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v]"
os.makedirs("out", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "work/phil/preview-picture.mp4"], check=True)
D = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "work/phil/preview-picture.mp4"]))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/phil/preview-picture.mp4", "-i", "audio/music-rocket-jr.mp3", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-af", f"volume=-4.6dB,afade=t=out:st={D - 1.2:.2f}:d=1.2", "-c:a", "aac", "-b:a", "320k", "-t", f"{D:.3f}", "-movflags", "+faststart", "out/phil-preview-clean.mp4"], check=True)
print(f"preview {D:.2f} s")
