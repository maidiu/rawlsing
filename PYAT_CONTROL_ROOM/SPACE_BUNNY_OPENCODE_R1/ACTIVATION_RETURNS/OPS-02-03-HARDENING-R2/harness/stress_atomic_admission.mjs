// MR-1 / MR-2 independent stress. Not derived from the reviewer's harness.
//
// T1: N >> cap concurrent processes; admitted must never exceed cap.
// T2: many repeated trials (a single lucky trial is explicitly insufficient).
// T3: concurrent duplicate submission of ONE task id must stay idempotent
//     (exactly one QUEUED record) even while the slot is contended.
import fs from "node:fs"; import path from "node:path"; import { spawn } from "node:child_process";
const D = new URL("../../../runtime/dispatcher.mjs", import.meta.url).pathname;
const A = "a".repeat(40), B = "b".repeat(40);
const ROOT = "/tmp/hq191a2/stress";
fs.rmSync(ROOT, { recursive: true, force: true }); fs.mkdirSync(ROOT + "/code", { recursive: true });

const child = `
import { Store, submitTask } from ${JSON.stringify(D)};
const [dir, id, wt, taskid, role] = process.argv.slice(2);
const st = new Store(dir);
const t = { task_id: taskid, role, base_commit: "${A}", worktree: wt, terrain: ["out/**"],
  acceptance_inputs: {x:"1"}, commission_path: "C.md", commission_identity: "${B}",
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { const r = submitTask(st, t); console.log(JSON.stringify({id, ok:true, queued:r.queued, dedup:r.dedup})); }
catch(e){ console.log(JSON.stringify({id, ok:false, code:e.code})); }
`;
const CF = ROOT + "/code/c.mjs"; fs.writeFileSync(CF, child);

const runPool = (n, dir, wt, taskidPrefix, role, distinct) =>
  Promise.all(Array.from({ length: n }, (_, i) => new Promise(res => {
    const taskid = distinct ? `${taskidPrefix}${i}` : taskidPrefix;
    const k = spawn("node", [CF, dir, String(i), wt, taskid, role], { stdio: ["ignore", "pipe", "pipe"] });
    let s = ""; k.stdout.on("data", d => s += d); k.on("exit", () => { try { res(JSON.parse(s.trim())); } catch { res({ id: i, ok: false, code: "PARSE" }); } });
  })));

const { Store } = await import(D);
const CAP = 2, N = 24, TRIALS = 40;
let overCapacity = 0, exactCap = 0, t1 = [];
for (let t = 0; t < TRIALS; t++) {
  const base = `${ROOT}/cap-${t}`;
  fs.rmSync(base, { recursive: true, force: true });
  const dir = path.join(base, "state"), wt = path.join(base, "wt");
  fs.mkdirSync(wt, { recursive: true });
  await runPool(N, dir, wt, `CAP${t}-`, "worker", true);
  const queued = new Store(dir).all().filter(e => e.state === "QUEUED").length;
  if (queued > CAP) overCapacity++;
  if (queued === CAP) exactCap++;
  t1.push(queued);
}
console.log(`T1 capacity stress: N=${N} processes vs cap=${CAP}, ${TRIALS} trials`);
console.log(`   admitted values observed: ${JSON.stringify([...new Set(t1)].sort())}`);
console.log(`   trials at exactly cap:   ${exactCap}/${TRIALS}`);
console.log(`   OVER-CAPACITY TRIALS:    ${overCapacity}/${TRIALS}`);
console.log(`   T1 PASS: ${overCapacity === 0 && exactCap === TRIALS}`);

let idemBad = 0, t3 = [];
for (let t = 0; t < TRIALS; t++) {
  const base = `${ROOT}/idem-${t}`;
  fs.rmSync(base, { recursive: true, force: true });
  const dir = path.join(base, "state"), wt = path.join(base, "wt");
  fs.mkdirSync(wt, { recursive: true });
  const res = await runPool(N, dir, wt, "SAME", "worker", false);
  const queued = new Store(dir).all().filter(e => e.state === "QUEUED").length;
  const admitted = res.filter(r => r.ok && r.queued && !r.dedup).length;
  t3.push({ queued, admitted });
  if (queued !== 1) idemBad++;
}
console.log(`\nT3 concurrent duplicate submission: ${N} processes submitting the SAME task id, ${TRIALS} trials`);
console.log(`   QUEUED record counts observed: ${JSON.stringify([...new Set(t3.map(r => r.queued))])}`);
console.log(`   trials not collapsing to exactly 1: ${idemBad}/${TRIALS}`);
console.log(`   T3 PASS: ${idemBad === 0}`);

const pass = overCapacity === 0 && exactCap === TRIALS && idemBad === 0;
console.log(`\nOVERALL: ${pass ? "PASS" : "FAIL"}`);
process.exit(pass ? 0 : 1);
