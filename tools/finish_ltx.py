"""Finish an LTX establishing shot: scale the 1280x704 generation to 1920x1080 (fill, centre crop), fade the tagline
overlay in over the night sky, and (review copies) add a small "Generated concept" label.
  python3 tools/finish_ltx.py <ltx.mp4> <out.mp4> [--tagline work/tagline-330.png] [--t-in 5.6] [--label]"""
import argparse, subprocess
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--tagline", default="work/tagline-330.png"); ap.add_argument("--t-in", type=float, default=5.6)
ap.add_argument("--label", action="store_true"); a = ap.parse_args()
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"; t0 = a.t_in
v = "[0:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,fps=25[b];"
v += f"[1:v]format=rgba,fade=t=in:st={t0}:d=1.2:alpha=1[t];[b][t]overlay=0:0:shortest=0:eof_action=pass"
if a.label: v += f",drawtext=fontfile={FONT}:text='Generated concept · LTX-2':fontcolor=0xf3eee4:alpha=0.75:fontsize=20:x=w-tw-64:y=h-56:shadowcolor=black@0.5:shadowy=1"
v += ",format=yuv420p[v]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-loop", "1", "-framerate", "25", "-i", a.tagline, "-filter_complex", v, "-map", "[v]",
                "-t", f"{float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.src])):.3f}",
                "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-movflags", "+faststart", a.out], check=True)
print("wrote", a.out)
