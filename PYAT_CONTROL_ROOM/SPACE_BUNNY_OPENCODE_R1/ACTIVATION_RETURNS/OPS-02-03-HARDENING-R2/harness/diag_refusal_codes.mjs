import fs from "node:fs"; import { spawn } from "node:child_process";
const D = new URL("../../../runtime/dispatcher.mjs", import.meta.url).pathname;
const A = "a".repeat(40), B = "b".repeat(40);
const ROOT = "/tmp/hq191a2/diag";
fs.rmSync(ROOT, { recursive: true, force: true }); fs.mkdirSync(ROOT + "/code", { recursive: true });

fs.writeFileSync(ROOT + "/code/c.mjs", `
import { Store, submitTask } from ${JSON.stringify(D)};
const [dir, id, wt] = process.argv.slice(2);
const st = new Store(dir);
const t = { task_id: "C"+id, role: "worker", base_commit: ${JSON.stringify(A)}, worktree: wt,
  terrain: ["out/**"], acceptance_inputs: {x:"1"}, commission_path: "C.md",
  commission_identity: ${JSON.stringify(B)}, model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { const r = submitTask(st, t); console.log(JSON.stringify({id, ok:true, dedup:r.dedup})); }
catch(e) { console.log(JSON.stringify({id, ok:false, code:e.code, msg:String(e.message).slice(0,120)})); }
`);

const N = 24, base = ROOT + "/t0", dir = base + "/state", wt = base + "/wt";
fs.mkdirSync(wt, { recursive: true });
const kids = Array.from({ length: N }, (_, i) =>
  spawn("node", [ROOT + "/code/c.mjs", dir, String(i), wt], { stdio: ["ignore", "pipe", "pipe"] }));
const outs = await Promise.all(kids.map(k => new Promise(r => {
  let s = ""; k.stdout.on("data", d => s += d); k.on("exit", () => r(s.trim())); })));

const codes = {};
for (const o of outs) {
  try {
    const j = JSON.parse(o);
    const k = j.ok ? "ADMITTED" : "refuse:" + j.code;
    codes[k] = (codes[k] || 0) + 1;
    if (!j.ok && j.code !== "SLOT_CAPACITY") console.log("  non-capacity refusal:", JSON.stringify(j));
  } catch { codes["PARSE"] = (codes["PARSE"] || 0) + 1; console.log("  RAW:", o.slice(0, 160)); }
}
console.log("code histogram:", JSON.stringify(codes));
const { Store } = await import(D);
console.log("QUEUED records:", new Store(dir).all().filter(e => e.state === "QUEUED").length);
