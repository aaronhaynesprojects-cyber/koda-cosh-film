/* KODA AT COSH LIVING — hero shot: DEDON's Secret Lakeside house at night. The camera is locked off.
   Every pixel of the house, the landscape and the lake is DEDON's own render (src/hero, made by tools/heroprep.py):
   the house starts with its lights off (DEDON's lit render with the light taken out), the moon rises from behind the treeline
   to where DEDON put it, and the lights come back group by group, left to right, on four beats of the music.
   Nothing is drawn into the scene: the light that returns is DEDON's own (on - off), with a soft bloom; the lake gets a gentle
   ripple on its existing reflections. Time h runs from the shot's first frame (film 53.59 s in best-of r4).
   Render: PAGE=hero.html node render.mjs encode out/hero-lake.mp4   (225 frames, 9 s at 25 fps) */
const W = 1920, H = 1080, FPS = 25, DUR = 9.0, TOTAL = Math.round(FPS * DUR);
const cv = document.getElementById("out"); cv.width = W; cv.height = H;
const ctx = cv.getContext("2d"); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
const M = window.HERO, K = W / M.W;                                       // plates are 2560 wide; drawn at 0.75
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), prog = (t, a, b) => clamp((t - a) / (b - a));
const easeOut = (x) => 1 - Math.pow(1 - x, 3), easeInOut = (x) => x * x * (3 - 2 * x);
const BAR = 2.14367, BEAT = BAR / 4;
const LIGHTS = [0, 1, 2, 3].map((k) => 4.287 + k * BEAT);                // bar 27 of the score (film 57.88 s): one group per beat
const MOON = [0.2, 4.1];                                                  // the moon clears the treeline and settles where DEDON placed it

const load = (src) => new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => bad(new Error("missing " + src)); i.src = src; });
function mk(w = W, h = H) { const c = document.createElement("canvas"); c.width = w; c.height = h; const x = c.getContext("2d"); x.imageSmoothingQuality = "high"; return [c, x]; }
const IMG = {}; let BLOOM = [];
window.ready = (async () => {
  for (const k of ["off", "sky", "moon", "light1", "light2", "light3", "light4"]) IMG[k] = await load(`src/hero/${k}.${k === "off" ? "jpg" : "png"}`);
  // bloom: each group's own light, softened twice (a tight glow and a wide one), made once
  BLOOM = [1, 2, 3, 4].map((g) => [16, 52].map((r) => { const [c, x] = mk(); x.filter = `blur(${r}px)`; x.drawImage(IMG["light" + g], 0, 0, W, H); return c; }));
  draw(0); return true;
})();

function lightLevel(h, k) {   // a lamp warming up: quick rise, a touch of overshoot, settle
  const u = prog(h, LIGHTS[k], LIGHTS[k] + 0.42); if (u <= 0) return 0;
  return easeOut(u) * (1 + 0.07 * Math.sin(Math.PI * u));
}
const [F, fx] = mk(), [Mo, mox] = mk();
function draw(h) {
  // the scene: DEDON's house with the lights off, then each group's light added back
  // night settles as the moon rises: about half a stop down, a little more contrast; the lights are added after the grade, at full strength
  const n = easeInOut(prog(h, 0.4, 4.2));
  fx.globalCompositeOperation = "source-over"; fx.globalAlpha = 1;
  fx.filter = `brightness(${(0.97 - 0.27 * n).toFixed(3)}) contrast(${(1.0 + 0.08 * n).toFixed(3)}) saturate(${(1.0 + 0.06 * n).toFixed(3)})`;
  fx.drawImage(IMG.off, 0, 0, W, H); fx.filter = "none";
  fx.globalCompositeOperation = "lighter";
  for (let k = 0; k < 4; k++) {
    const a = lightLevel(h, k); if (a <= 0) continue;
    fx.globalAlpha = clamp(a, 0, 1.1); fx.drawImage(IMG["light" + (k + 1)], 0, 0, W, H);
    fx.globalAlpha = 0.42 * clamp(a, 0, 1.1); fx.drawImage(BLOOM[k][0], 0, 0);
    fx.globalAlpha = 0.22 * clamp(a, 0, 1.1); fx.drawImage(BLOOM[k][1], 0, 0);
  }
  // the moon rises from behind the treeline (masked by the sky), warm and dim low down, clearing to DEDON's moon at the top
  const p = easeOut(prog(h, MOON[0], MOON[1])), [mx, my, mr] = M.moon;
  const startY = M.ridgeAtMoon + mr * 1.3, dy = (1 - p) * (startY - my) * K, dx = -(1 - p) * 26 * K, low = 1 - p;
  mox.globalCompositeOperation = "source-over"; mox.clearRect(0, 0, W, H); mox.globalAlpha = 1;
  mox.filter = `sepia(${(0.55 * low).toFixed(3)}) saturate(${(1 + 0.8 * low).toFixed(3)}) brightness(${(1 - 0.25 * low).toFixed(3)})`;
  mox.drawImage(IMG.moon, dx, dy, W, H); mox.filter = "none";
  mox.globalCompositeOperation = "destination-in"; mox.drawImage(IMG.sky, 0, 0, W, H);
  fx.globalCompositeOperation = "lighter"; fx.globalAlpha = clamp(0.35 + 0.65 * p); fx.drawImage(Mo, 0, 0);
  fx.globalCompositeOperation = "source-over"; fx.globalAlpha = 1;
  // onto the frame, with the lake's reflections rippling gently: each row of water shifted a pixel or two, more toward us
  ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1; ctx.drawImage(F, 0, 0);
  const y0 = Math.round(M.lakeY * K);
  for (let y = y0; y < H; y++) {
    const d = (y - y0) / (H - y0), amp = (0.35 + 2.4 * d * d) * clamp((y - y0) / 14);
    const off = amp * (0.62 * Math.sin(y * 0.29 + h * 2.3) + 0.38 * Math.sin(y * 0.083 - h * 1.25));
    ctx.drawImage(F, 0, y, W, 1, off, y, W, 1);
  }
}
window.TOTAL = TOTAL;
window.frame = async (i, q = 0.95) => { draw(i / FPS); return cv.toDataURL("image/jpeg", q).slice(23); };
