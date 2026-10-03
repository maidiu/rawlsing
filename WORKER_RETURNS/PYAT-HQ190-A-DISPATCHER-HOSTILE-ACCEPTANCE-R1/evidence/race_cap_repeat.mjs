import fs from "node:fs"; import path from "node:path"; import { spawn } from "node:child_process";
const D = "/Users/matthewsmith/Desktop/Rawlsing/review-hq190a/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const A = "a".repeat(40), B = "b".repeat(40);
const child = `
import { Store, submitTask } from ${JSON.stringify(D)};
const dir = process.argv[2], id = process.argv[3], wt = process.argv[4];
const st = new Store(dir);
const t = { task_id: "CAP"+id, role: "worker", base_commit: "${A}", worktree: wt, terrain: ["out/**"],
  acceptance_inputs: {x:"1"}, commission_path: "C.md", commission_identity: "${B}",
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { console.log(JSON.stringify({id, ok: submitTask(st, t).queued})); } catch(e){ console.log(JSON.stringify({id, code: e.code})); }
`;
fs.writeFileSync("/tmp/hq190a/code/rc.mjs", child);
const runs = [];
for (let trial = 0; trial < 8; trial++) {
  const base = `/tmp/hq190a/fixtures/caprepeat-${trial}`;
  fs.rmSync(base, { recursive: true, force: true });
  const dir = path.join(base, "state"); const wt = path.join(base, "wt"); fs.mkdirSync(wt, { recursive: true });
  const N = 6;
  const kids = Array.from({length: N}, (_, i) => spawn("node", ["/tmp/hq190a/code/rc.mjs", dir, String(i), wt], { stdio: ["ignore","pipe","pipe"] }));
  const outs = await Promise.all(kids.map(k => new Promise(res => { let s=""; k.stdout.on("data", d=>s+=d); k.on("exit", ()=>res(s.trim())); })));
  const { Store } = await import(D);
  const st = new Store(dir);
  const queued = st.all().filter(e => e.state === "QUEUED").length;
  runs.push({ trial, queued, refusals: outs.filter((o) => o.includes("SLOT_CAPACITY")).length });
}
console.log("cap=2, 6 concurrent processes per trial:");
for (const r of runs) console.log(`  trial ${r.trial}: admitted=${r.queued} over_capacity=${r.queued > 2} refusals=${r.refusals}`);
const over = runs.filter(r => r.queued > 2).length;
console.log(`\nOVER-CAPACITY TRIALS: ${over}/${runs.length}`);
console.log(`max admitted: ${Math.max(...runs.map(r => r.queued))} (cap 2)`);
