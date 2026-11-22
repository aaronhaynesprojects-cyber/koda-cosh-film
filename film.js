/* KODA AT COSH LIVING — 90 s concept film. Every frame is drawn as a function of time.
   Units are 1920x1080; ?s=2 renders 3840x2160. ?review=1 burns in scene timecodes. */
const Q = new URLSearchParams(location.search), S = +(Q.get("s") || 1), REVIEW = Q.has("review");
const CUT = Q.get("cut") || "film";   // "film" = the 90 s concept film, "broll" = the 62 s footage-only reel
const TITLES_ON = Q.get("titles") !== "0";  // the narrated cut drops the on-screen lines so they do not compete with the voice
const V2 = Q.get("v") === "2";   // Version 2: manufacturer settings (DEDON, Potocco), darkness-to-light
const V23 = Q.get("v") === "2.3"; // Version 2.3: art-direction rebuild — four acts, three environments, the transformation as the reason to watch
const WM = Q.has("wm");           // review copies carry a watermark
const VBEST = Q.get("v") === "best"; // Best-of: authentic manufacturer films and photographs only. No composites, nothing generated.
const NB = CUT === "nb";   // B-roll to "Nothing in Our Way" (Out To The World), 2:15.1 to the end of the track; 93.25 bpm, bar 2.5737 s
const LEAD = Q.has("lead") ? 3 : 0;  // rough cuts: a 3·2·1 leader, then burned-in timecode from 01:00:00:00
const W = 1920, H = 1080, FPS = 25, DUR = { broll: 62, croll: 37, nb: 63.4 }[CUT] || 90, TOTAL = Math.round(FPS * (DUR + LEAD));
const cv = document.getElementById("out"); cv.width = W * S; cv.height = H * S;
const ctx = cv.getContext("2d"); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), lerp = (a, b, t) => a + (b - a) * t;
const prog = (t, a, b) => clamp((t - a) / (b - a)), smooth = (x) => x * x * (3 - 2 * x);
const IVORY = "#f3eee4", STONE = "#cfc6b6", GRAPHITE = "#1b1a18";
const FONT = (w, px) => `${w} ${px}px "Helvetica Neue", "Avenir Next", Arial, sans-serif`;

/* ---------- assets ---------- */
const IMG = {}, SEQ = {};
const load = (src) => new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => bad(new Error("missing " + src)); i.src = src; });
const STILLS = {
  syd1: "src/cosh/0F0A1124.jpg", syd0: "src/cosh/0F0A0969.jpg", rich: "src/cosh2/038A5649.jpg", johanna: "src/cosh/Johanna_Occasional_Gwenton_park.jpg",
  kett: "src/cosh2/erskine-modular-sofa-indoor-furniture-kett-414571.jpg",
  baseA: "src/cosh2/Brisbane_Showroom_2.jpg", baseB: "src/cosh2/x._All_Images_4.jpg", baseC: "src/cosh2/x._All_Images_2.jpg",
  occ4: "src/stills/occhio-04.jpg", occ5: "src/stills/occhio-05.jpg",
  lod6: "src/stills/lodes-06.jpg", lod3: "src/stills/lodes-03.jpg", lod1: "src/stills/lodes-01.jpg", lod9: "src/stills/lodes-09.jpg",
  ark5: "src/stills/arkoslight-05.jpg", ark1: "src/stills/arkoslight-01.jpg",
  luna: "src/cutouts/luna-cloud3.png", largo: "src/cutouts/mito-largo-bronze.png", volum: "src/cutouts/volum.png",
  koda: "src/logos/koda.svg", cosh: "src/logos/cosh.png",
};
if (V2) Object.assign(STILLS, { d01off: "src/v2/d01-off.jpg", d01on: "src/v2/d01-on.jpg", d02off: "src/v2/d02-off.jpg", d02on: "src/v2/d02-on.jpg", d03off: "src/v21/d03-off.jpg", d03on: "src/v21/d03-on.jpg",
  d04off: "src/v21/d04-off.jpg", d04on: "src/v21/d04-on.jpg", chelt: "src/v21/chelt.jpg", bedgold: "src/v21/bed-gold.jpg", beddusk: "src/v21/bed-dusk-on.jpg", d05: "src/v2/d05.jpg", d06: "src/v2/d06.jpg", d07: "src/v2/d07.jpg", p01: "src/v2/p01.jpg" });
if (V23) Object.assign(STILLS, { canyon: "src/v23/canyon-dark.jpg", pergOff: "src/v23/perg-off.jpg", pergOn: "src/v23/perg-on.jpg", det: "src/v23/det-on.jpg",
  muDusk: "src/v23/mu-dusk.jpg", muOn: "src/v23/mu-on.jpg", izOff: "src/v23/izar-off.jpg", izEra: "src/v23/izar-era.jpg", izOn: "src/v23/izar-on.jpg", izx: "src/v23/izarx.jpg" });
if (VBEST || NB) Object.assign(STILLS, { dCanyon: "src/best/dedon-canyon.jpg", dLake: "src/best/dedon-lakehouse.jpg", dTerrace: "src/best/dedon-terrace.jpg", dPergola: "src/best/dedon-pergola.jpg",
  dLodge: "src/best/dedon-lodge.jpg", izHall: "src/best/potocco-izar-hall.jpg", izPav: "src/best/potocco-izar-pavilion.jpg",
  uma1: "src/situ/pablo/Uma-In-Situ-1.png", uma11: "src/situ/pablo/Uma-In-Situ-11.png", uma8: "src/situ/pablo/Uma-In-Situ-8.png", mini13: "src/situ/pablo/Uma_Mini-In-Situ-13.png",
  mini11: "src/situ/pablo/Uma_Mini-In-Situ-11.png", uma10: "src/situ/pablo/Uma-In-Situ-10.png", uma6: "src/situ/pablo/Uma-In-Situ-6.png", uma5: "src/situ/pablo/Uma-In-Situ-5.png" });
const SEQN = { o_dim: 53, o_wide: 38, o_lit: 43, o_wall: 100, o_table: 80, k_open: 105, k_wide: 60, a_room: 65, a_flute: 55, a_chain: 43, a_col: 63, a_hall: 60, p_edge: 87, p_dine: 106, p_trio: 73, p_blue: 84, r_track: 30, r_ceil: 43, r_lens: 25, l_path: 108, l_pleat: 108, l_gate: 95, r_lens2: 70, r_ceil2: 105, o_pend2: 45, p_olive: 81,
  e_macro: 34, e_ring: 31, e_gest: 69, e_carry: 60, e_dim: 112, e_crystal: 40, e_amber: 50, e_walk: 71, e_read: 44, e_on: 18, e_globe: 31, u_close: 46, u_logo: 23, u_side: 37, u_three: 57, u_hero: 21, u_low: 33 };
const fcache = new Map();
function frameImg(seq, i) {
  const key = seq + "/" + i; let p = fcache.get(key);
  if (!p) { p = load(`fr/${seq}/${String(i + 1).padStart(3, "0")}.jpg`); fcache.set(key, p); if (fcache.size > 400) fcache.delete(fcache.keys().next().value); }
  return p;
}
function mk(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; const x = c.getContext("2d"); x.imageSmoothingQuality = "high"; return [c, x]; }

/* ---------- concept composites: real Cosh showroom photograph + real KODA product cut-out ---------- */
function glow(x, cx, cy, r, color, a, sy = 1) {
  x.save(); x.globalCompositeOperation = "screen"; x.translate(cx, cy); x.scale(1, sy);
  const g = x.createRadialGradient(0, 0, 0, 0, 0, r); g.addColorStop(0, color.replace("A", a)); g.addColorStop(0.4, color.replace("A", a * 0.35)); g.addColorStop(1, color.replace("A", 0));
  x.fillStyle = g; x.fillRect(-r, -r, 2 * r, 2 * r); x.restore();
}
const WARM = "rgba(255,214,160,A)", WARMW = "rgba(255,236,208,A)";
function shade(x, cx, cy, rx, ry, a) { x.save(); x.translate(cx, cy); x.scale(1, ry / rx); const g = x.createRadialGradient(0, 0, 0, 0, 0, rx); g.addColorStop(0, `rgba(0,0,0,${a})`); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(-rx, -rx, 2 * rx, 2 * rx); x.restore(); }
function buildConcepts() {
  // A — Occhio Luna Sospeso Cloud 3 over the Kett Portland table (Brisbane showroom)
  { const b = IMG.baseA, [c, x] = mk(b.width, b.height); x.drawImage(b, 0, 0);
    const L = IMG.luna, w = 372, h = w * L.height / L.width, lx = 1030 - w * 0.44, ly = 430 - h;
    // a soft pool on the table and a lift on the panelled wall behind
    glow(x, 1030, 852, 430, WARM, 0.20, 0.16); glow(x, 1010, 330, 520, WARMW, 0.10);
    x.drawImage(L, lx, ly, w, h);
    for (const [fx, fy, r] of [[0.18, 0.589, 60], [0.837, 0.71, 74], [0.40, 0.897, 104]]) { glow(x, lx + fx * w, ly + fy * h, r * 2.6, WARM, 0.34); glow(x, lx + fx * w, ly + fy * h, r * 0.55, WARMW, 0.55); }
    IMG.conA = c; }
  // B — Lodes Volum trio over the dining setting (Cheltenham showroom)
  { const b = IMG.baseB, [c, x] = mk(b.width, b.height); x.drawImage(b, 0, 0);
    const V = IMG.volum, [vc, vx] = mk(V.width, V.height); vx.drawImage(V, 0, 0);
    const d = vx.getImageData(0, 0, V.width, V.height).data; let x0 = 1e9, x1 = 0, y0 = 1e9, y1 = 0; // the globe alone: rows where the opaque run is wider than the cable
    for (let y = 0; y < V.height; y++) { let a = 1e9, b = 0; for (let xx = 0; xx < V.width; xx++) if (d[(y * V.width + xx) * 4 + 3] > 128) { a = Math.min(a, xx); b = xx; } if (b - a > 60) { x0 = Math.min(x0, a); x1 = Math.max(x1, b); y0 = Math.min(y0, y); y1 = y; } }
    const GW = x1 - x0 + 1, GH = y1 - y0 + 1, [g, gx] = mk(GW, GH); gx.drawImage(V, x0, y0, GW, GH, 0, 0, GW, GH); window.VOLUM_BOX = [x0, y0, GW, GH];
    const drops = [[425, 640, 118, 152], [540, 722, 150, 138], [652, 668, 100, 160]]; // x, globe centre y, width, ceiling y
    glow(x, 515, 925, 330, WARM, 0.26, 0.2); glow(x, 520, 600, 430, WARMW, 0.13);
    for (const [cx, cy, w, top] of drops) {
      const hh = w * GH / GW;
      x.strokeStyle = "rgba(70,66,60,0.75)"; x.lineWidth = 1.6; x.beginPath(); x.moveTo(cx, top); x.lineTo(cx, cy - hh * 0.46); x.stroke();
      x.fillStyle = "rgba(236,233,228,0.95)"; x.beginPath(); x.ellipse(cx, top, 13, 4.5, 0, 0, 7); x.fill(); x.fillStyle = "rgba(0,0,0,0.10)"; x.beginPath(); x.ellipse(cx, top + 3, 13, 3, 0, 0, 7); x.fill();
      glow(x, cx, cy, w * 1.9, WARM, 0.30); x.drawImage(g, cx - w / 2, cy - hh / 2, w, hh); glow(x, cx, cy, w * 0.62, WARMW, 0.30);
    }
    IMG.conB = c; }
  // C — Occhio Mito largo arcing over the lounge setting (Cheltenham showroom); its base stands behind the sofa
  { const b = IMG.baseC, [c, x] = mk(b.width, b.height); x.drawImage(b, 0, 0);
    const M = IMG.largo, w = 690, h = w * M.height / M.width, lx = 842 - 0.233 * w, ly = 1252 - h;
    glow(x, 1215, 1135, 300, WARM, 0.22, 0.2); // pool on the coffee tables
    x.save(); x.beginPath(); x.rect(0, 0, b.width, 1086); x.clip();  // the sofa seat hides the stem below this line
    x.globalAlpha = 0.16; x.filter = "blur(9px) brightness(0)"; x.drawImage(M, lx + 34, ly + 26, w, h); x.filter = "none"; x.globalAlpha = 1; // a faint shadow on the wall
    x.drawImage(M, lx, ly, w, h); x.restore();
    const rx = lx + 0.79 * w, ry = ly + 0.455 * h;
    glow(x, rx, ry + 30, 250, WARM, 0.30, 0.5); x.save(); x.globalCompositeOperation = "screen"; x.strokeStyle = "rgba(255,238,210,0.85)"; x.lineWidth = 4; x.filter = "blur(2.5px)"; x.beginPath(); x.ellipse(rx, ry + 16, 0.172 * w, 0.034 * w, 0, 0.12, Math.PI - 0.12); x.stroke(); x.restore();
    IMG.conC = c; }
}

/* ---------- drawing ---------- */
function cover(img, fx, fy, z, alpha = 1, filter) {
  const s = Math.max(W / img.width, H / img.height) * z, dw = img.width * s, dh = img.height * s;
  let dx = W / 2 - fx * dw, dy = H / 2 - fy * dh; dx = Math.min(0, Math.max(W - dw, dx)); dy = Math.min(0, Math.max(H - dh, dy));
  ctx.globalAlpha = alpha; if (filter) ctx.filter = filter; ctx.drawImage(img, dx, dy, dw, dh); ctx.filter = "none"; ctx.globalAlpha = 1;
}
/* Shots. t0 = cut point, x = dissolve-in length (0 = cut). A shot stays up until the next shot has fully arrived. */
const K = (a, b) => ({ a, b }); // camera: [fx, fy, zoom] from a to b
let SHOTS = [
  // 1 THE SPACE
  { t0: 0, x: 1.4, still: "syd1", cam: K([0.46, 0.55, 1.10], [0.54, 0.55, 1.16]) },
  { t0: 3.2, x: 1.0, still: "rich", cam: K([0.60, 0.60, 1.14], [0.46, 0.58, 1.08]) },
  { t0: 6.2, x: 1.0, still: "johanna", cam: K([0.40, 0.56, 1.22], [0.48, 0.52, 1.12]) },
  // 2 THE TRANSFORMATION — Occhio's own film: the room before, and with the light brought up
  { t0: 9.0, x: 1.0, seq: "o_dim", sp: 0.85, f: "brightness(0.82)" },
  { t0: 11.3, x: 1.2, seq: "o_wide", sp: 0.75, from: 7 },
  { t0: 12.9, x: 0, seq: "o_lit", sp: 0.4, from: 9 },
  { t0: 14.9, x: 0, seq: "o_table", sp: 0.5, from: 25 },
  // 3 KODA
  { t0: 18.0, x: 0.9, seq: "k_open", sp: 0.92, z: 1.075 },
  { t0: 21.6, x: 0.8, seq: "k_wide", sp: 0.42, z: 1.075, dim: [23.2, 24.4, 0.30] },
  // 4 THE COLLECTION
  { t0: 26.0, x: 0.7, seq: "o_wall", sp: 0.95, from: 42, brand: "occhio" },
  { t0: 28.2, x: 0, still: "occ4", cam: K([0.42, 0.5, 1.06], [0.5, 0.5, 1.12]) },
  { t0: 30.2, x: 0, still: "occ5", cam: K([0.56, 0.5, 1.12], [0.5, 0.5, 1.05]) },
  { t0: 32.0, x: 0.5, seq: "a_room", sp: 0.95, from: 10, brand: "and" },
  { t0: 34.2, x: 0, seq: "a_col", sp: 0.9, from: 12 },
  { t0: 36.2, x: 0, seq: "a_hall", sp: 1 },
  { t0: 38.0, x: 0.5, still: "lod6", cam: K([0.44, 0.48, 1.08], [0.52, 0.48, 1.14]), brand: "lodes" },
  { t0: 40.1, x: 0, still: "lod3", cam: K([0.5, 0.42, 1.16], [0.5, 0.48, 1.07]) },
  { t0: 42.1, x: 0, still: "lod1", cam: K([0.54, 0.5, 1.07], [0.46, 0.5, 1.13]) },
  { t0: 44.0, x: 0.5, seq: "p_edge", sp: 1, brand: "pablo" },
  { t0: 46.0, x: 0, seq: "p_dine", sp: 1, from: 13 },
  { t0: 48.4, x: 0, seq: "p_trio", sp: 0.8, from: 30 },
  { t0: 50.0, x: 0.5, seq: "r_ceil", sp: 0.95, from: 3, brand: "arkos" },
  { t0: 51.6, x: 0, still: "ark5", cam: K([0.44, 0.5, 1.05], [0.52, 0.5, 1.10]) },
  { t0: 53.6, x: 0, still: "ark1", cam: K([0.5, 0.5, 1.12], [0.5, 0.52, 1.04]) },
  // 5 THE VISION — genuine showroom first, then the proposed KODA lighting arrives in the same photograph
  { t0: 56.0, x: 1.0, still: "syd0", cam: K([0.56, 0.52, 1.12], [0.48, 0.52, 1.06]) },
  { t0: 58.6, x: 0.9, still: "baseA", over: "conA", on: [59.9, 61.5], cam: K([0.5, 0.38, 1.03], [0.52, 0.34, 1.11]), concept: 1 },
  { t0: 63.6, x: 0.9, still: "baseB", over: "conB", on: [64.8, 66.4], cam: K([0.34, 0.5, 1.22], [0.28, 0.46, 1.34]), concept: 1 },
  { t0: 69.0, x: 0.9, still: "baseC", over: "conC", on: [70.2, 71.8], cam: K([0.5, 0.52, 1.02], [0.56, 0.56, 1.12]), concept: 1 },
  // 6 THE OPPORTUNITY
  { t0: 75.0, x: 1.0, still: "kett", cam: K([0.5, 0.5, 1.10], [0.5, 0.5, 1.03]) },
  { t0: 78.0, x: 1.0, still: "lod9", cam: K([0.46, 0.5, 1.04], [0.54, 0.5, 1.09]) },
  { t0: 81.0, x: 1.0, still: "conB", cam: K([0.42, 0.5, 1.06], [0.42, 0.5, 1.0]), concept: 1 },
  // 7 THE REVEAL
  { t0: 84.0, x: 1.2, reveal: true },
];
/* B-roll reel: footage only, cut on the bar lines of the music (112 bpm, bar 2.1437 s). [bar, sequence, first frame, brand, dissolve] */
const BAR = 2.14367;
const BROLL = [
  [0, "k_open", 0, "koda", 1.2], [2, "o_dim", 0, "occhio", 0.8], [3, "o_lit", 9, "occhio", 1.0], [4, "o_table", 25, "occhio", 0], [6, "a_room", 15, "and", 0], [8, "p_edge", 0, "pablo", 0], [10, "l_gate", 2, "lodes", 0],
  [12, "r_lens2", 0, "arkos", 0], [13, "r_ceil2", 7, "arkos", 0], [14, "a_flute", 15, "and", 0], [15, "a_chain", 3, "and", 0], [16, "a_col", 12, "and", 0], [17, "a_hall", 2, "and", 0],
  [18, "o_wide", 16, "occhio", 0], [19, "o_wall", 42, "occhio", 0], [20, "p_dine", 13, "pablo", 0], [21, "p_trio", 30, "pablo", 0], [22, "p_olive", 16, "pablo", 0], [23, "p_blue", 0, "pablo", 0],
  [24, "l_path", 2, "lodes", 0], [25, "l_pleat", 2, "lodes", 0], [26, "k_wide", 0, "koda", 0], [27, null, 0, "koda", 0.5],
];
/* C-roll: Occhio's new Era series, from occhio.com's own 4K campaign films. Eight quiet bars, eight fuller ones. */
const CROLL = [
  [0, "e_macro", 0, "era", 1.0], [1, "e_ring", 0, "era", 0.6], [2, "e_gest", 0, "era", 0], [4, "e_carry", 0, "era", 0], [6, "e_dim", 0, "era", 0],
  [8, "e_crystal", 0, "era", 0], [9, "e_amber", 0, "era", 0], [10, "e_walk", 0, "era", 0], [11, "e_read", 0, "era", 0],
  [12, "u_close", 0, "lusso", 0], [13, "u_logo", 0, "lusso", 0], [14, "u_side", 0, "lusso", 0], [15, "u_three", 0, "lusso", 0], [16, null, 0, "koda", 0.6],
];
const ROLL = { broll: BROLL, croll: CROLL }[CUT];
const B2 = 2.5737;
if (ROLL) SHOTS = ROLL.map(([bar, seq, from, brand, x], i) => {
  const t0 = bar * BAR, next = ROLL[i + 1], t1 = next ? next[0] * BAR + next[4] : DUR;
  const len = { a_flute: 50, a_chain: 36 }[seq] || SEQN[seq];
  return seq ? { t0, x, seq, from, brand, z: seq[0] === "k" ? 1.075 : 1, sp: Math.min(CUT === "croll" ? 1 : 0.92, (len - (CUT === "croll" ? 1.5 : 3) - from) / ((t1 - t0) * FPS)) } : { t0, x, card: true, brand };
});
/* Version 2 replaces the settings, keeps the narration, the KODA brand sections and Cosh Living's own showroom. */
if (V2 && !ROLL) {
  const at = (t) => SHOTS.findIndex((s) => Math.abs(s.t0 - t) < 0.01);
  const put = (t, shot) => { SHOTS[at(t)] = Object.assign({ t0: t }, shot); };
  const DE = "Setting: DEDON, Spirit of Place campaign", PO = "Setting: Potocco project, Izar Houses";
  put(0, { x: 1.6, still: "d01off", cam: K([0.62, 0.56, 1.14], [0.6, 0.55, 1.05]), credit: DE });
  SHOTS.splice(at(3.2), 2);                                                                        // the two Cosh daylight stills give way to dusk
  SHOTS.splice(1, 0, { t0: 5.0, x: 1.2, still: "d07", cam: K([0.42, 0.55, 1.04], [0.48, 0.55, 1.10]), dusk: [5.4, 9.4], credit: DE });
  put(9.0, { x: 1.0, still: "d02off", over: "d02on", on: [11.4, 13.0], cam: K([0.5, 0.45, 1.04], [0.5, 0.45, 1.12]), credit: DE });
  SHOTS.splice(at(11.3), 1);                                                                       // Occhio wide: covered by the villa switching on
  Object.assign(SHOTS[at(12.9)], { t0: 13.6, x: 0.6 }); Object.assign(SHOTS[at(14.9)], { t0: 15.6, x: 0 });
  // V2.1 (luxury brief): cordless KODA pieces outdoors, standing where the scene's own lamps stood; Cosh shown clean
  put(28.2, { x: 0, seq: "e_gest", sp: 1, from: 0 }); put(30.2, { x: 0, seq: "u_three", sp: 1, from: 0 });            // Occhio: the new Era range
  // V2.2 (quality reset): no retail, signage or merchandising; fewer, longer, finer scenes
  put(18.0, { x: 0.9, seq: "k_open", sp: 0.48, z: 1.075, dim: [22.4, 23.6, 0.10] }); SHOTS.splice(at(21.6), 1);   // KODA at night through the glass; the crowded event footage is out
  put(32.0, { x: 0.5, seq: "a_flute", sp: 0.72, from: 15, brand: "and" });                                        // A-N-D: glass detail instead of the logo-backdrop showroom
  put(42.1, { x: 0, still: "lod9", cam: K([0.46, 0.5, 1.04], [0.54, 0.5, 1.09]) });                                // Lodes: living room instead of the merchandise wall
  SHOTS.splice(at(56.0), 1);                                                                                       // Cosh Sydney showroom (signage, retail light) is out
  put(58.6, { t0: 56.0, x: 1.0, still: "d04off", over: "d04on", on: [59.8, 61.4], cam: K([0.5, 0.55, 1.24], [0.54, 0.53, 1.48]), concept: 1, credit: DE });
  put(63.6, { x: 1.0, still: "bedgold", over: "beddusk", on: [64.6, 67.6], cam: K([0.44, 0.56, 1.22], [0.40, 0.60, 1.40]), concept: 1, credit: "Furniture: Kett, at Cosh Living" });
  put(69.0, { x: 0.9, still: "d03off", over: "d03on", on: [70.2, 71.8], cam: K([0.56, 0.5, 1.02], [0.6, 0.52, 1.09]), concept: 1, credit: DE });
  put(75.0, { x: 1.0, still: "d05", cam: K([0.5, 0.18, 1.0], [0.5, 0.62, 1.0]), credit: DE });
  put(78.0, { x: 1.0, still: "d06", cam: K([0.5, 0.5, 1.08], [0.56, 0.52, 1.02]), credit: DE });
  put(81.0, { x: 1.0, still: "p01", cam: K([0.5, 0.5, 1.02], [0.5, 0.52, 1.08]), credit: PO });
}
/* Version 2.3: the environment is the hero, light is what changes it. Cuts fall on the bar lines of Rocket Jr (BAR). */
if (V23 && !ROLL) {
  const DE = "Setting: DEDON, Spirit of Place campaign (render)", PO = "Setting: Izar Houses, furnished by Potocco (photograph)";
  const UMI = "Pablo Designs · Uma Mini", UMA = "Pablo Designs · Uma", ERA = "Occhio · Era grande";
  SHOTS = [
    // ACT I — DARKNESS: the canyon pavilion, then the table beneath its pergola, both before any light
    { t0: 0, x: 2.2, still: "canyon", cam: K([0.5, 0.16, 1.0], [0.5, 0.70, 1.03]), credit: DE },
    { t0: 6 * BAR / 2, x: 1.6, still: "pergOff", over: "pergOn", on: [12.0, 15.4], warm: 1, cam: K([0.50, 0.50, 1.00], [0.54, 0.52, 1.13]), credit: DE, product: UMI },
    // ACT II — LET THERE BE LIGHT: what the light found
    { t0: 9 * BAR, x: 1.3, still: "det", cam: K([0.44, 0.52, 1.03], [0.50, 0.49, 1.12]), credit: DE, product: UMI },
    // ACT III — TRANSFORMATION: the desert terrace, from dusk into a night lit by the fire and one lantern
    { t0: 12 * BAR, x: 1.6, still: "muDusk", over: "muOn", on: [27.6, 33.4], cam: K([0.46, 0.50, 1.00], [0.52, 0.50, 1.08]), credit: DE, product: UMA },
    { t0: 16 * BAR, x: 0, still: "muOn", cam: K([0.61, 0.62, 1.42], [0.59, 0.63, 1.50]), credit: DE, product: UMA },
    { t0: 19 * BAR, x: 0, still: "muOn", cam: K([0.36, 0.51, 1.46], [0.40, 0.52, 1.40]), credit: DE, product: UMA },
    // the Izar Houses hall: dark, then Occhio's Era row, then the house itself
    { t0: 22 * BAR, x: 1.4, still: "izOff", over: "izEra", on: [50.9, 52.9], over2: "izOn", on2: [54.1, 57.4], cam: K([0.50, 0.52, 1.00], [0.50, 0.58, 1.13]), credit: PO, product: ERA },
    { t0: 28 * BAR, x: 0, still: "izOn", cam: K([0.42, 0.70, 1.34], [0.43, 0.68, 1.42]), credit: PO, product: ERA },
    { t0: 29.5 * BAR, x: 0, still: "izOn", cam: K([0.64, 0.64, 1.55], [0.60, 0.62, 1.48]), credit: PO, product: ERA },
    // ACT IV — THE COLLABORATION: the house from outside, resolved; then the signature
    { t0: 32 * BAR, x: 1.8, still: "izx", cam: K([0.50, 0.50, 1.00], [0.53, 0.52, 1.07]), credit: PO },
    { t0: 36 * BAR, x: 0, still: "izx", cam: K([0.62, 0.60, 1.30], [0.58, 0.58, 1.38]), credit: PO },
    { t0: 39 * BAR, x: 1.4, reveal: true },
  ];
}
if (NB) {
  const H0 = (k) => K(k, k), st = (t0, x, still, brand, f = [0.5, 0.5, 1.0]) => ({ t0, x, still, brand, cam: H0(f) }), sq = (t0, x, seq, brand, from = 0) => ({ t0, x, seq, brand, from });
  SHOTS = [
    // the tail of the big section: the places
    st(0, 1.2, "dCanyon", "dedon", [0.5, 0.64, 1.0]), st(1.5 * B2, 0.8, "dLake", "dedon"),
    // the quiet break (0:09-0:31): Occhio Era, the light coming on just before the drop
    sq(3.5 * B2, 1.2, "e_macro", "era"), sq(5 * B2, 0.8, "e_ring", "era"), sq(6.5 * B2, 0.8, "e_read", "era"), sq(8 * B2, 0.8, "e_dim", "era"),
    sq(9.5 * B2, 0.6, "e_crystal", "era"), sq(10.5 * B2, 0.4, "e_globe", "era"),
    // the full section (0:31-0:53): the light in furnished rooms, on the bar
    sq(12 * B2, 0, "u_three", "lusso"), st(13 * B2, 0, "uma6", "uma"), sq(14 * B2, 0, "p_dine", "pablo", 13), st(15 * B2, 0, "lod9", "lodes"),
    sq(16 * B2, 0, "r_lens2", "arkos"), st(17 * B2, 0, "uma10", "uma"), sq(17.5 * B2, 0, "a_flute", "and", 15), st(18 * B2, 0, "izHall", "potocco"),
    sq(19 * B2, 0, "o_wall", "occhio", 42), st(19.5 * B2, 0, "mini13", "mini"), st(20 * B2, 0, "dTerrace", "dedon"),
    // the song's own ending: the house at dusk, then the signature
    st(21 * B2, 1.0, "izPav", "potocco"), { t0: 22.5 * B2, x: 1.4, reveal: true, rt: 84.0 },
  ];
  SHOTS.forEach((s, i) => { if (!s.seq) return; const n = SHOTS[i + 1], t1 = n ? n.t0 + n.x : DUR; s.sp = Math.min(1, (SEQN[s.seq] - 2 - (s.from || 0)) / ((t1 - s.t0) * FPS)); });
}
if (VBEST && !ROLL) {
  const H0 = (k) => K(k, k);                       // photographs are held still: no artificial camera movement
  const st = (t0, x, still, brand, f = [0.5, 0.5, 1.0]) => ({ t0, x, still, brand, cam: H0(f) });
  const sq = (t0, x, seq, brand, from = 0) => ({ t0, x, seq, brand, from });
  SHOTS = [
    // THE ENVIRONMENT — Cosh Living's DEDON, at dusk
    st(0, 1.6, "dCanyon", "dedon", [0.5, 0.64, 1.0]), st(2 * BAR, 1.0, "dLake", "dedon"),
    // OCCHIO ERA — Occhio's own 4K campaign films; the light comes on with "The difference is light"
    sq(4 * BAR, 0.8, "e_macro", "era"), sq(5 * BAR, 0, "e_ring", "era"), sq(11.55, 0, "e_globe", "era"), sq(14.2, 0, "e_crystal", "era"),
    sq(8 * BAR, 0, "e_gest", "era"), sq(9 * BAR, 0, "e_read", "era"), sq(10 * BAR, 0, "e_dim", "era"), sq(11 * BAR, 0.4, "u_close", "lusso"), sq(12 * BAR, 0, "u_three", "lusso"),
    // LIGHT IN FURNISHED ROOMS — the lighting brands' own scenes, then Cosh's DEDON and Potocco lit at dusk
    st(13 * BAR, 0.6, "dTerrace", "dedon"), st(14 * BAR, 0.6, "lod9", "lodes"), sq(15 * BAR, 0.6, "p_dine", "pablo", 13), st(16 * BAR, 0.6, "izHall", "potocco"), st(17 * BAR, 0.6, "ark1", "arkos"),
    // PABLO UMA / UMA MINI — Pablo's own photographs
    st(18 * BAR, 0.6, "uma1", "uma"), st(20 * BAR, 0.7, "mini13", "mini"), st(21 * BAR, 0.7, "uma10", "uma"), st(22 * BAR, 0.8, "uma6", "uma"), st(24 * BAR, 0.9, "uma5", "uma"),
    // ARCHITECTURAL LIGHTING — A-N-D, Arkoslight, Occhio Luna, Lodes
    sq(26 * BAR, 0.6, "a_flute", "and", 15), sq(27 * BAR, 0, "a_col", "and", 12), sq(28 * BAR, 0.6, "r_lens2", "arkos"), sq(30 * BAR, 0.6, "o_wall", "occhio", 42), sq(31 * BAR, 0.6, "l_gate", "lodes", 2), sq(32 * BAR, 0, "l_path", "lodes", 2),
    // THE COLLABORATION — Cosh Living's furniture brands, lit
    st(34 * BAR, 1.0, "izPav", "potocco"), st(36 * BAR, 1.0, "dLodge", "dedon"), st(37.5 * BAR, 1.0, "dPergola", "dedon", [0.5, 0.62, 1.0]),
    { t0: 39 * BAR, x: 1.4, reveal: true },
  ];
  SHOTS.forEach((s, i) => { if (!s.seq) return; const n = SHOTS[i + 1], t1 = n ? n.t0 + n.x : DUR; s.sp = Math.min(1, (SEQN[s.seq] - 2 - (s.from || 0)) / ((t1 - s.t0) * FPS)); });
}
SHOTS.forEach((s, i) => { const n = SHOTS[i + 1]; s.t1 = n ? n.t0 + n.x : DUR; });
const BRANDS = { occhio: ["OCCHIO", "Germany", 26, 32], and: ["A-N-D", "Canada", 32, 38], lodes: ["LODES", "Italy", 38, 44], pablo: ["PABLO DESIGNS", "USA", 44, 50], arkos: ["ARKOSLIGHT", "Spain", 50, 56] };
const TITLES = [
  [3.4, 8.3, "GREAT DESIGN SHAPES A SPACE."], [12.0, 17.2, "LIGHT BRINGS IT TO LIFE."], [19.4, 23.2, "A WORLD OF LIGHTING DESIGN."],
  [60.2, 63.2, "ONE DESTINATION."], [66.2, 73.6, "A MORE COMPLETE DESIGN EXPERIENCE."], [77.0, 83.2, "DESIGNED TO BELONG."],
];
const SCENES = [[0, "THE SPACE"], [9, "THE TRANSFORMATION"], [18, "INTRODUCING KODA"], [26, "THE COLLECTION · OCCHIO"], [32, "THE COLLECTION · A-N-D"], [38, "THE COLLECTION · LODES"], [44, "THE COLLECTION · PABLO DESIGNS"], [50, "THE COLLECTION · ARKOSLIGHT"], [56, "THE VISION"], [75, "THE OPPORTUNITY"], [84, "THE REVEAL"]];

async function needs(t) {
  const out = [];
  for (const s of SHOTS) if (s.seq && t >= s.t0 && t < s.t1) { const [i, j] = seqIdx(s, t); out.push(frameImg(s.seq, i), frameImg(s.seq, j)); }
  const r = await Promise.all(out); let k = 0;
  for (const s of SHOTS) if (s.seq && t >= s.t0 && t < s.t1) { s._a = r[k++]; s._b = r[k++]; }
}
function seqIdx(s, t) { const p = (s.from || 0) + (t - s.t0) * FPS * (s.sp || 1), n = SEQN[s.seq] - 1, i = Math.min(n, Math.floor(p)); s._f = Math.min(1, p - i); return [i, Math.min(n, i + 1)]; }

function track(text, x, y, px, em, weight = 300, align = "left") {
  ctx.font = FONT(weight, px); ctx.letterSpacing = (px * em) + "px"; ctx.textBaseline = "alphabetic"; ctx.textAlign = align;
  ctx.fillText(text, align === "center" ? x + px * em / 2 : x, y); ctx.letterSpacing = "0px";
}
function scrim(a) { const g = ctx.createLinearGradient(0, H * 0.58, 0, H); g.addColorStop(0, "rgba(10,9,8,0)"); g.addColorStop(1, `rgba(10,9,8,${0.62 * a})`); ctx.fillStyle = g; ctx.fillRect(0, H * 0.58, W, H * 0.42); }
function fadeIO(t, a, b, i = 0.9, o = 0.7) { return smooth(prog(t, a, a + i)) * (1 - smooth(prog(t, b - o, b))); }

function drawShot(s, t) {
  const a = s.x ? smooth(prog(t, s.t0, s.t0 + s.x)) : 1, u = prog(t, s.t0, s.t1);
  if (s.reveal) return reveal(s.rt != null ? t - s.t0 + s.rt : t, a);
  if (s.card) { ctx.globalAlpha = a; ctx.fillStyle = GRAPHITE; ctx.fillRect(0, 0, W, H); const h = 150, w = h * 227 / 60; ctx.drawImage(IMG.koda, W / 2 - w / 2, H / 2 - h / 2, w, h); ctx.globalAlpha = 1; return; }
  if (s.seq) {
    const z = s.z || 1.0; cover(s._a, 0.5, 0.5, z, a, s.f); if (s._f > 0.02 && s._b !== s._a) cover(s._b, 0.5, 0.5, z, a * s._f, s.f);
    if (s.dim) { ctx.fillStyle = `rgba(14,13,12,${(1 - s.dim[2]) * smooth(prog(t, s.dim[0], s.dim[1])) * a})`; ctx.fillRect(0, 0, W, H); }
  } else {
    const c = s.cam, fx = lerp(c.a[0], c.b[0], u), fy = lerp(c.a[1], c.b[1], u), z = lerp(c.a[2], c.b[2], u);
    let flt; if (s.dusk) { const d = smooth(prog(t, s.dusk[0], s.dusk[1])); flt = `brightness(${(1 - 0.5 * d).toFixed(3)}) saturate(${(1 - 0.35 * d).toFixed(3)}) hue-rotate(${(-14 * d).toFixed(1)}deg)`; }
    cover(IMG[s.still], fx, fy, z, a, flt);
    if (s.dusk) { const d = smooth(prog(t, s.dusk[0], s.dusk[1])); ctx.globalCompositeOperation = "multiply"; ctx.fillStyle = `rgba(${Math.round(255 - 120 * d)},${Math.round(255 - 95 * d)},255,${a})`; ctx.fillRect(0, 0, W, H); ctx.globalCompositeOperation = "source-over"; }
    if (s.over) { const o = smooth(prog(t, s.on[0], s.on[1])); if (o > 0) cover(IMG[s.over], fx, fy, z, a * o, s.warm && o < 1 ? `sepia(${(0.32 * (1 - o)).toFixed(3)}) saturate(${(1 + 0.25 * (1 - o)).toFixed(3)})` : undefined); }
    if (s.over2) { const o = smooth(prog(t, s.on2[0], s.on2[1])); if (o > 0) cover(IMG[s.over2], fx, fy, z, a * o); }
  }
}
function reveal(t, a) {
  ctx.globalAlpha = a; ctx.fillStyle = GRAPHITE; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1;
  if (VBEST || NB) cover(IMG.izPav, 0.58, 0.56, lerp(1.06, 1.02, prog(t, 83.6, 90)), a * 0.5, "blur(6px) brightness(0.5) saturate(0.85)");
  else if (V23) cover(IMG.izx, 0.58, 0.56, lerp(1.38, 1.30, prog(t, 83.6, 90)), a * 0.55, "blur(5px) brightness(0.55) saturate(0.85)");
  else cover(V2 ? IMG.d01on : IMG.conC, 0.5, 0.5, lerp(1.10, 1.04, prog(t, 84, 90)), a * (V2 ? 0.42 : 0.34), "blur(14px) brightness(0.62) saturate(0.8)");
  const v = ctx.createRadialGradient(W / 2, H / 2, 200, W / 2, H / 2, 1100); v.addColorStop(0, "rgba(20,19,17,0.25)"); v.addColorStop(1, "rgba(12,11,10,0.86)"); ctx.globalAlpha = a; ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1;
  const l = smooth(prog(t, 84.6, 85.7));
  if (l > 0) { // the two identities, balanced either side of a hairline
    const kh = 84, kw = kh * 227 / 60, ch = 58, cw = ch * IMG.cosh.width / IMG.cosh.height, gap = 86, total = kw + cw + gap * 2, x0 = W / 2 - total / 2, y = 372;
    ctx.globalAlpha = l; ctx.drawImage(IMG.koda, x0, y - kh / 2, kw, kh); ctx.drawImage(IMG.coshIvory, x0 + kw + gap * 2, y - ch / 2 + 4, cw, ch);
    ctx.fillStyle = "rgba(243,238,228,0.42)"; ctx.fillRect(x0 + kw + gap - 0.5, y - 44, 1, 88); ctx.globalAlpha = 1;
  }
  const p = smooth(prog(t, 85.2, 86.4)); ctx.fillStyle = IVORY;
  if (p > 0) { ctx.globalAlpha = p; track("KODA AT COSH LIVING", W / 2, 572 + (1 - p) * 8, 62, 0.34, 200, "center"); ctx.globalAlpha = 1; }
  const q = smooth(prog(t, 85.9, 87.0)); if (q > 0) { ctx.globalAlpha = q * 0.92; track("Exceptional furniture. Exceptional light.", W / 2, 652, 30, 0.08, 300, "center"); ctx.globalAlpha = 1; }
  const f = smooth(prog(t, 86.5, 87.6)); if (f > 0) { ctx.globalAlpha = f * 0.8; ctx.fillStyle = STONE; track("A concept for collaboration.", W / 2, 964, 20, 0.22, 300, "center"); ctx.globalAlpha = 1; }
}
const BNAME = { uma: ["PABLO DESIGNS", "Uma"], mini: ["PABLO DESIGNS", "Uma Mini"], dedon: ["DEDON", "at Cosh Living"], potocco: ["POTOCCO", "at Cosh Living"], koda: null, occhio: ["OCCHIO", "Germany"], and: ["A-N-D", "Canada"], lodes: ["LODES", "Italy"], pablo: ["PABLO DESIGNS", "USA"], arkos: ["ARKOSLIGHT", "Spain"], era: ["OCCHIO", "Era · the new series"], lusso: ["OCCHIO", "Era lusso · the new series"] };
function bestLabels(t) {   // the maker's name appears as its passage begins and fades after a few seconds; lighter band
  let i = -1; SHOTS.forEach((s, k) => { if (t >= s.t0 && t < s.t1) i = k; }); if (i < 0) return;
  if (SHOTS[i].reveal) return; let j = i; const fam = (b) => (b === "mini" ? "uma" : b === "lusso" ? "era" : b); while (j > 0 && fam(SHOTS[j - 1].brand) === fam(SHOTS[i].brand)) j--;
  const b = BNAME[SHOTS[i].brand]; if (!b) return; const a = fadeIO(t, SHOTS[j].t0 + 0.5, SHOTS[j].t0 + 4.2, 0.7, 0.9); if (a <= 0) return;
  scrim(0.45 * a); ctx.fillStyle = IVORY; ctx.shadowColor = "rgba(0,0,0,0.45)"; ctx.shadowBlur = 18 * S; ctx.globalAlpha = a; track(b[0], 128, 960, 28, 0.34, 400); ctx.globalAlpha = a * 0.8; track(b[1], 130, 994, 18, 0.22);
  ctx.globalAlpha = 1; ctx.shadowBlur = 0; ctx.shadowColor = "transparent";
}
function brollOverlays(t) {
  let cur = null; for (const s of SHOTS) if (t >= s.t0 && t < s.t1) cur = s; const b = cur && BNAME[cur.brand]; if (!b) return;
  let a = 1; for (const s of SHOTS) if (s.brand !== cur.brand) { if (s.t0 > t) { a = Math.min(a, prog(s.t0 - t, 0, 0.18)); break; } }
  scrim(0.8 * a); ctx.fillStyle = IVORY; ctx.shadowColor = "rgba(0,0,0,0.45)"; ctx.shadowBlur = 18 * S; ctx.globalAlpha = a; track(b[0], 128, 960, 31, 0.34, 400); ctx.globalAlpha = a * 0.8; track(b[1], 130, 997, 20, 0.22);
  ctx.globalAlpha = 1; ctx.shadowBlur = 0; ctx.shadowColor = "transparent";
}
function overlays(t) {
  if (VBEST || NB) return bestLabels(t);
  if (ROLL) return brollOverlays(t);
  let need = 0; if (TITLES_ON) for (const [a, b] of TITLES) need = Math.max(need, fadeIO(t, a, b));
  if (!V23) for (const k in BRANDS) need = Math.max(need, fadeIO(t, BRANDS[k][2] + 0.25, BRANDS[k][3] - 0.05, 0.5, 0.45) * 0.8);
  for (const s of SHOTS) if (s.concept) need = Math.max(need, fadeIO(t, s.on ? s.on[0] : s.t0 + 0.6, s.t1 - 0.3) * 0.5);
  if (need > 0) scrim(need);
  ctx.fillStyle = IVORY; ctx.shadowColor = "rgba(0,0,0,0.45)"; ctx.shadowBlur = 18 * S;
  if (TITLES_ON) for (const [a, b, text] of TITLES) { const o = fadeIO(t, a, b); if (o <= 0) continue; ctx.globalAlpha = o; ctx.fillRect(128, 918, 56 * smooth(prog(t, a, a + 1.2)), 1.5); track(text, 128, 972 + (1 - smooth(prog(t, a, a + 1.0))) * 6, 33, 0.30); }
  if (!V23) for (const k in BRANDS) { const [name, place, a, b] = BRANDS[k], o = fadeIO(t, a + 0.25, b - 0.05, 0.5, 0.45); if (o <= 0) continue; ctx.globalAlpha = o; track(name, 128, 960, 31, 0.34, 400); ctx.globalAlpha = o * 0.8; track(place, 130, 997, 20, 0.22); }
  for (const s of SHOTS) if (s.concept) { const o = fadeIO(t, s.on ? s.on[0] : s.t0 + 0.6, s.t1 - 0.3); if (o <= 0) continue; ctx.globalAlpha = o * 0.86; track("Concept visualisation", W - 128, 996, 20, 0.2, 400, "right"); }
  if (V23) { let p = null; for (const s of SHOTS) if (s.product && t >= s.t0 && t < s.t1) p = s; const nx = SHOTS[SHOTS.indexOf(p) + 1];
    if (p) { let a0 = p.t0, b0 = p.t1; for (const s of SHOTS) if (s.product === p.product && s.t0 < p.t0 && s.t1 >= p.t0) a0 = Math.min(a0, s.t0); for (const s of SHOTS) if (s.product === p.product && s.t0 > p.t0) b0 = Math.max(b0, s.t1);
      const o = fadeIO(t, a0 + 1.2, b0 - 0.6, 0.9, 0.6); if (o > 0) { ctx.globalAlpha = o * 0.80; track(p.product.toUpperCase(), W - 128, 972, 15, 0.22, 400, "right"); ctx.globalAlpha = o * 0.62; track("Concept visualisation", W - 128, 1000, 15, 0.16, 400, "right"); } } }
  for (const s of SHOTS) if (s.credit && t >= s.t0 && t < s.t1) { const o = fadeIO(t, s.t0 + 0.5, s.t1 - 0.2, 0.8, 0.5); if (o > 0) { ctx.globalAlpha = o * 0.72; track(s.credit, 128, 1000, 15, 0.16, 400); } }
  ctx.globalAlpha = 1; ctx.shadowBlur = 0; ctx.shadowColor = "transparent";
  const kl = V23 ? 0 : fadeIO(t, 23.4, 26.25, 1.0, 0.5); // the KODA mark, from KODA's own vector logo
  if (kl > 0) { const h = 118, w = h * 227 / 60; ctx.globalAlpha = kl; ctx.drawImage(IMG.koda, W / 2 - w / 2, H / 2 - h / 2 - 10, w, h); ctx.globalAlpha = 1; }
}
function draw(t) {
  ctx.setTransform(S, 0, 0, S, 0, 0); ctx.globalAlpha = 1; ctx.filter = "none"; ctx.fillStyle = "#000"; ctx.fillRect(0, 0, W, H);
  for (const s of SHOTS) if (t >= s.t0 && t < s.t1) drawShot(s, t);
  if (NB ? t < 22.5 * B2 : ROLL ? t < ROLL[ROLL.length - 1][0] * BAR : t < 84) { const v = ctx.createRadialGradient(W / 2, H / 2, 620, W / 2, H / 2, 1180); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,0.26)"); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); }
  overlays(t);
  const fo = prog(t, DUR - 0.7, DUR - 0.08); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${smooth(fo)})`; ctx.fillRect(0, 0, W, H); }
  if (WM) { ctx.save(); ctx.globalAlpha = 0.5; ctx.fillStyle = IVORY; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 8; track("INTERNAL REVIEW · NOT FOR DISTRIBUTION · KODA × COSH LIVING V2.3", W / 2, 56, 15, 0.28, 500, "center"); ctx.restore(); ctx.textAlign = "left"; }
  if (REVIEW) {
    const SC = V23 ? [[0, "ACT I · DARKNESS"], [11.8, "ACT II · LET THERE BE LIGHT"], [12 * BAR, "ACT III · TRANSFORMATION"], [32 * BAR, "ACT IV · THE COLLABORATION"]] : SCENES;
    let sc = SC[0]; for (const x of SC) if (t >= x[0]) sc = x;
    const fr = Math.round(t * FPS), tc = `00:0${Math.floor(fr / FPS / 60)}:${String(Math.floor(fr / FPS) % 60).padStart(2, "0")}:${String(fr % FPS).padStart(2, "0")}`;
    ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(W - 512, 34, 478, 34); ctx.fillStyle = "#f3eee4"; ctx.font = '500 17px "SF Mono", Menlo, monospace'; ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillText(`${sc[1]}   ${tc}`, W - 48, 52); ctx.textAlign = "left";
  }
}
window.ready = (async () => {
  await Promise.all(Object.entries(STILLS).map(async ([k, v]) => { IMG[k] = await load(v); }));
  { const c = IMG.cosh, [o, x] = mk(c.width, c.height); x.drawImage(c, 0, 0); x.globalCompositeOperation = "source-in"; x.fillStyle = IVORY; x.fillRect(0, 0, c.width, c.height); IMG.coshIvory = o; }
  buildConcepts(); await needs(0); draw(0); return true;
})();
/* ---------- leader and timecode (rough cuts only) ---------- */
const CUTNAME = { nb: "KODA AT COSH LIVING · B-ROLL · NOTHING IN OUR WAY", film: VBEST ? "KODA AT COSH LIVING · BEST OF" : V23 ? "KODA AT COSH LIVING · V2.3" : "KODA AT COSH LIVING", broll: "KODA BRANDS · B-ROLL", croll: "OCCHIO ERA · C-ROLL" }[CUT];
function leader(t) {
  ctx.setTransform(S, 0, 0, S, 0, 0); ctx.globalAlpha = 1; ctx.filter = "none";
  const n = 3 - Math.floor(t), f = t % 1, fl = 0.92 + 0.08 * Math.sin(t * 91) * Math.sin(t * 37); ctx.fillStyle = `rgb(${46 * fl},${44 * fl},${41 * fl})`; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.fillStyle = "rgba(0,0,0,0.30)"; ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, 1300, -Math.PI / 2, -Math.PI / 2 + f * 2 * Math.PI); ctx.closePath(); ctx.fill(); // the sweep
  ctx.strokeStyle = "rgba(243,238,228,0.75)"; ctx.lineWidth = 3; for (const r of [330, 390]) { ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.stroke(); }
  ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(-W, 0); ctx.lineTo(W, 0); ctx.moveTo(0, -H); ctx.lineTo(0, H); ctx.stroke(); ctx.restore();
  ctx.fillStyle = IVORY; ctx.font = FONT(200, 420); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(String(n), W / 2, H / 2 + 22);
  ctx.textBaseline = "alphabetic"; ctx.globalAlpha = 0.8; track(CUTNAME + (V23 || VBEST ? " · REVIEW" : " · ROUGH CUT"), W / 2, 92, 22, 0.3, 400, "center"); ctx.globalAlpha = 1; ctx.textAlign = "left";
  const r = rng(Math.floor(t * 25)); ctx.fillStyle = "rgba(243,238,228,0.28)"; for (let k = 0; k < 3; k++) ctx.fillRect(r() * W, 0, 1.2, H * r()); // scratches
}
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let r = Math.imul(seed ^ (seed >>> 15), 1 | seed); r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r; return ((r ^ (r >>> 14)) >>> 0) / 4294967296; }; }
function timecode(i) {  // programme starts at 01:00:00:00; the leader counts up to it
  const fr = 3600 * FPS + i - LEAD * FPS, p = (v) => String(v).padStart(2, "0"), tc = `${p(Math.floor(fr / FPS / 3600))}:${p(Math.floor(fr / FPS / 60) % 60)}:${p(Math.floor(fr / FPS) % 60)}:${p(fr % FPS)}`;
  ctx.setTransform(S, 0, 0, S, 0, 0); ctx.globalAlpha = 1; ctx.filter = "none"; ctx.fillStyle = "rgba(0,0,0,0.55)"; ctx.fillRect(W / 2 - 150, H - 64, 300, 42);
  ctx.fillStyle = "#f3eee4"; ctx.font = '500 26px "SF Mono", Menlo, monospace'; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(tc, W / 2, H - 42); ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
}
window.frame = async (i, q = 0.93) => { const t = i / FPS - LEAD; if (t < 0) leader(t + LEAD); else { await needs(t); draw(t); } if (LEAD) timecode(i); return cv.toDataURL("image/jpeg", q).slice(23); };
window.png = async (t) => { await needs(t); draw(t); return cv.toDataURL("image/png").slice(22); };
window.conceptPng = (k) => IMG[k].toDataURL("image/png").slice(22);

/* ---------- stills for the deck ---------- */
window.poster = (k = "conC", fx = 0.5, fy = 0.56, z = 1.0) => { ctx.setTransform(S, 0, 0, S, 0, 0); ctx.filter = "none"; ctx.globalAlpha = 1; cover(IMG[k], fx, fy, z);
  ctx.fillStyle = IVORY; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 16 * S; ctx.globalAlpha = 0.9; track("Concept visualisation", W - 128, 996, 20, 0.2, 400, "right"); ctx.globalAlpha = 1; ctx.shadowBlur = 0; ctx.shadowColor = "transparent"; return cv.toDataURL("image/png").slice(22); };
window.keyVisual = () => { ctx.setTransform(S, 0, 0, S, 0, 0); ctx.filter = "none"; ctx.globalAlpha = 1; cover(IMG.conC, 0.5, 0.56, 1.0);
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "rgba(14,13,12,0.08)"); g.addColorStop(0.42, "rgba(14,13,12,0.16)"); g.addColorStop(0.70, "rgba(14,13,12,0.70)"); g.addColorStop(1, "rgba(14,13,12,0.90)"); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const kh = 56, kw = kh * 227 / 60, ch = 39, cw = ch * IMG.cosh.width / IMG.cosh.height, gap = 44, y = 792; ctx.drawImage(IMG.koda, 128, y - kh / 2, kw, kh); ctx.fillStyle = "rgba(243,238,228,0.5)"; ctx.fillRect(128 + kw + gap, y - 30, 1, 60); ctx.drawImage(IMG.coshIvory, 128 + kw + gap * 2, y - ch / 2 + 3, cw, ch);
  ctx.fillStyle = IVORY; track("KODA AT COSH LIVING", 126, 908, 60, 0.30, 200); ctx.globalAlpha = 0.92; track("Exceptional furniture. Exceptional light.", 128, 966, 28, 0.08); ctx.globalAlpha = 0.75; ctx.fillStyle = STONE; track("A concept for collaboration.", 128, 1014, 19, 0.2);
  track("Concept visualisation", W - 128, 1014, 19, 0.2, 400, "right"); ctx.globalAlpha = 1; return cv.toDataURL("image/png").slice(22); };
