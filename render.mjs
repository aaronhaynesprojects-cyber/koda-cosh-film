// node render.mjs stills <t,t,..> [prefix] | sheet <name> <t,t,..> [cols] | encode <out.mp4> [audio.wav]   (env: S=2 for 4K, REVIEW=1, CRF=14)
import fs from "node:fs"; import { spawn, execFileSync } from "node:child_process"; import { launch } from "./cdp.mjs";
const [mode, a1, a2, a3] = process.argv.slice(2), S = +(process.env.S || 1), W = 1920 * S, H = 1080 * S;
const b = await launch({ width: W, height: H, port: 9600 + Math.floor(Math.random() * 60) });
await b.goto("file://" + new URL("./film.html", import.meta.url).pathname + `?s=${S}` + (process.env.REVIEW ? "&review=1" : "") + (process.env.CUT ? "&cut=" + process.env.CUT : "") + (process.env.LEAD ? "&lead=1" : "") + (process.env.TITLES === "0" ? "&titles=0" : ""));
await b.evaluate("window.ready"); fs.mkdirSync("out", { recursive: true });
try {
  if (mode === "stills") for (const t of a1.split(",").map(Number)) { const f = `out/${a2 || "still"}-${t.toFixed(2)}.jpg`; fs.writeFileSync(f, Buffer.from(await b.evaluate(`frame(${Math.round(t * 25)},0.92)`), "base64")); console.log(f); }
  else if (mode === "png") { fs.writeFileSync(a2, Buffer.from(await b.evaluate(`png(${Number(a1)})`), "base64")); console.log(a2); }
  else if (mode === "js") { fs.writeFileSync(a2, Buffer.from(await b.evaluate(a1), "base64")); console.log(a2); }
  else if (mode === "concept") { fs.writeFileSync(a2, Buffer.from(await b.evaluate(`conceptPng(${JSON.stringify(a1)})`), "base64")); console.log(a2); }
  else if (mode === "sheet") {
    const ts = a2.split(",").map(Number), cols = +(a3 || 4), dir = fs.mkdtempSync("out/sheet-"); let i = 0;
    for (const t of ts) fs.writeFileSync(`${dir}/${String(i++).padStart(3, "0")}.jpg`, Buffer.from(await b.evaluate(`frame(${Math.round(t * 25)},0.85)`), "base64"));
    execFileSync("ffmpeg", ["-v", "error", "-y", "-framerate", "1", "-i", `${dir}/%03d.jpg`, "-vf", `scale=640:-1,tile=${cols}x${Math.ceil(ts.length / cols)}`, "-frames:v", "1", "-q:v", "4", `out/${a1}.jpg`], { stdio: "ignore" });
    fs.rmSync(dir, { recursive: true }); console.log(`out/${a1}.jpg`);
  } else if (mode === "encode") {
    const args = ["-v", "error", "-y", "-f", "image2pipe", "-framerate", "25", "-c:v", "mjpeg", "-i", "-"]; if (a2) args.push("-i", a2);
    args.push("-c:v", "libx264", "-preset", "slow", "-crf", process.env.CRF || "15", "-pix_fmt", "yuv420p", "-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart");
    args.push("-vf", "scale=in_range=pc:out_range=tv" + (process.env.OUT_H ? `,scale=-2:${process.env.OUT_H}:flags=lanczos` : ""), "-color_range", "tv");
    if (a2) args.push("-af", `volume=${process.env.GAIN || "-4.6"}dB`, "-c:a", "aac", "-b:a", "320k", "-shortest"); args.push(a1);
    const N = await b.evaluate("TOTAL"), ff = spawn("ffmpeg", args, { stdio: ["pipe", "inherit", "inherit"] }), t0 = Date.now();
    for (let i = 0; i < N; i++) { const buf = Buffer.from(await b.evaluate(`frame(${i},0.95)`), "base64"); if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r)); if (i % 250 === 0) console.log(i, ((Date.now() - t0) / 1000).toFixed(0) + "s"); }
    ff.stdin.end(); await new Promise((r) => ff.on("close", r)); console.log("wrote", a1, (fs.statSync(a1).size / 1e6).toFixed(1), "MB");
  }
} finally { const e = b.logs.filter((l) => /exception|error/i.test(l)); if (e.length) console.log("console:", e.slice(0, 8)); b.close(); }
