// HQ190-A MINIMAL DECISIVE REPRODUCER
// Counterexample: the capacity invariant (SLOTS[role]) is violated under real
// multi-process concurrency because slotGate() and append() are separate lock scopes.
//
// Run:  node minimal_capacity_counterexample.mjs
// Expect (pre-fix): admitted > 2 in a substantial fraction of trials, max observed 4.
//
// Disposable fixtures only. Nothing outside /tmp is touched.
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

const DISPATCHER =
  process.env.HQ190A_DISPATCHER ||
  "/Users/matthewsmith/Desktop/Rawlsing/review-hq190a/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const A = "a".repeat(40);
const B = "b".repeat(40);
const ROOT = "/tmp/hq190a/counterexample";
const N_CHILDREN = 6;
const TRIALS = 12;
const CAP = 2; // SLOTS.worker

const childSource = `
import { Store, submitTask } from ${JSON.stringify(DISPATCHER)};
const dir = process.argv[2], id = process.argv[3], wt = process.argv[4];
const st = new Store(dir);
const t = { task_id: "CAP"+id, role: "worker", base_commit: "${A}", worktree: wt,
  terrain: ["out/**"], acceptance_inputs: { x: "1" }, commission_path: "C.md",
  commission_identity: "${B}", model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { console.log(JSON.stringify({ id, queued: submitTask(st, t).queued })); }
catch (e) { console.log(JSON.stringify({ id, code: e.code })); }
`;
fs.rmSync(ROOT, { recursive: true, force: true });
fs.mkdirSync(ROOT, { recursive: true });
const childPath = path.join(ROOT, "child.mjs");
fs.writeFileSync(childPath, childSource);

const { Store } = await import(DISPATCHER);
const trials = [];
for (let t = 0; t < TRIALS; t++) {
  const base = path.join(ROOT, `trial-${t}`);
  const stateDir = path.join(base, "state");
  const worktree = path.join(base, "wt");
  fs.mkdirSync(worktree, { recursive: true });
  const kids = Array.from({ length: N_CHILDREN }, (_, i) =>
    spawn("node", [childPath, stateDir, String(i), worktree], { stdio: ["ignore", "pipe", "pipe"] })
  );
  await Promise.all(
    kids.map((k) => new Promise((res) => { k.on("exit", res); k.on("error", res); }))
  );
  const st = new Store(stateDir);
  const admitted = st.all().filter((e) => e.state === "QUEUED").length;
  trials.push({ trial: t, admitted, over_capacity: admitted > CAP });
}
const over = trials.filter((r) => r.over_capacity);
console.log(`capacity invariant: SLOTS.worker = ${CAP}, ${N_CHILDREN} concurrent OS processes per trial`);
for (const r of trials) console.log(`  trial ${r.trial}: admitted=${r.admitted}${r.over_capacity ? "  <-- OVER CAPACITY" : ""}`);
console.log(`\nOVER-CAPACITY TRIALS: ${over.length}/${TRIALS}`);
console.log(`MAX ADMITTED: ${Math.max(...trials.map((r) => r.admitted))} (cap ${CAP})`);
console.log(over.length ? "\nCOUNTEREXAMPLE CONFIRMED" : "\nnot reproduced this run (race is timing-dependent; retry)");
process.exitCode = over.length ? 0 : 3;
