// Minimal Chrome DevTools Protocol driver: launch headless Chrome, open a page, evaluate.
import { spawn } from "node:child_process";
import fs from "node:fs";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export async function launch({ width = 1920, height = 1080, port = 9344 } = {}) {
  const profile = fs.mkdtempSync(new URL("./chrome-prof-", import.meta.url).pathname);
  const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
    "--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    `--window-size=${width},${height}`, "--force-device-scale-factor=1", "--no-first-run",
    "--no-default-browser-check", "--hide-scrollbars", "--mute-audio",
    "--autoplay-policy=no-user-gesture-required", "--allow-file-access-from-files", "about:blank",
  ], { stdio: "ignore" });
  let target;
  for (let i = 0; i < 80 && !target; i++) {
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page"); } catch {}
    if (!target) await sleep(150);
  }
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  let id = 0; const pending = new Map(); const logs = [];
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
    if (m.method === "Runtime.exceptionThrown") logs.push("exception: " + (m.params.exceptionDetails.exception?.description ?? m.params.exceptionDetails.text));
    if (m.method === "Runtime.consoleAPICalled") logs.push(m.params.type + ": " + m.params.args.map((a) => a.value ?? a.description).join(" "));
    if (m.method === "Log.entryAdded") logs.push("log: " + m.params.entry.level + " " + m.params.entry.text);
  });
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const evaluate = async (expression) => {
    const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description ?? r.result.exceptionDetails.text);
    return r.result?.result?.value;
  };
  await send("Runtime.enable"); await send("Log.enable"); await send("Page.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
  const goto = async (url) => { await send("Page.navigate", { url }); for (let i = 0; i < 200; i++) { await sleep(100); if (await evaluate("document.readyState") === "complete") return; } };
  const close = () => { ws.close(); chrome.kill(); setTimeout(() => fs.rmSync(profile, { recursive: true, force: true }), 500); };
  return { send, evaluate, goto, close, logs };
}
