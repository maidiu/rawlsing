// HQ192-A2 reviewer-authored MR-1 stress: harsher and structurally different from both
// the prior reviewer's reproducer and the worker's harness.
// - N >> cap (32 processes vs cap 2)
// - mixed submission shapes: distinct tasks AND same-task duplicates in the same wave
// - many trials
// - verifies exact cap admission, zero over-capacity, and duplicate idempotence
// Disposable /tmp fixtures only.
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

const D = process.env.HQ192A2_DISPATCHER ||
  "/Users/matthewsmith/Desktop/Rawlsing/review-hq192a2/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const ROOT = "/tmp/hq192a2/mr1";
fs.rmSync(ROOT, { recursive: true, force: true });
fs.mkdirSync(ROOT, { recursive: true });
const A = "a".repeat(40), B = "b".repeat(40);

const childSrc = `
import { Store, submitTask } from ${JSON.stringify(D)};
const [dir, taskId, wt] = process.argv.slice(2);
const st = new Store(dir);
const t = { task_id: taskId, role: "worker", base_commit: "${A}", worktree: wt,
  terrain: ["out/**"], acceptance_inputs: { x: "1" }, commission_path: "C.md",
  commission_identity: "${B}", model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
let out;
try { out = { ok: true, ...submitTask(st, t) }; }
catch (e) { out = { ok: false, code: e.code, detail: String(e.detail).slice(0,120) }; }
process.stdout.write(JSON.stringify(out));
`;
fs.writeFileSync(path.join(ROOT, "child.mjs"), childSrc);
const { Store } = await import(D);

const runWave = async (tasksPerWave, distinct, trials) => {
  const rows = [];
  for (let t = 0; t < trials; t++) {
    const base = path.join(ROOT, `w${tasksPerWave}-${distinct ? "d" : "s"}-${t}`);
    const dir = path.join(base, "state"), wt = path.join(base, "wt");
    fs.mkdirSync(wt, { recursive: true });
    const kids = Array.from({ length: tasksPerWave }, (_, i) => {
      const id = distinct ? `T${i}` : "SAME";
      return spawn("node", [path.join(ROOT, "child.mjs"), dir, id, wt],
        { stdio: ["ignore", "pipe", "pipe"] });
    });
    const outs = await Promise.all(kids.map((k) => new Promise((res) => {
      let s = ""; k.stdout.on("data", (d) => s += d);
      k.on("exit", () => { try { res(JSON.parse(s)); } catch { res({ ok: false, code: "NO_OUTPUT" }); } });
    })));
    const st = new Store(dir);
    const queued = st.all().filter((e) => e.state === "QUEUED");
    const overCap = outs.filter((o) => o.ok && o.appended).length > 2;
    rows.push({ trial: t, queuedRows: queued.length, overCap,
      capacityRefusals: outs.filter((o) => o.code === "SLOT_CAPACITY").length,
      dedupAcks: outs.filter((o) => o.idempotent || o.dedup).length,
      other: outs.filter((o) => !o.ok && o.code !== "SLOT_CAPACITY").map((o) => o.code) });
  }
  return rows;
};

console.log("=== WAVE A: 32 processes, 32 DISTINCT tasks, cap=2, 10 trials ===");
const Arows = await runWave(32, true, 10);
for (const r of Arows) console.log(`  trial ${r.trial}: queued=${r.queuedRows} overCap=${r.overCap} refusals=${r.capacityRefusals} other=${JSON.stringify(r.other)}`);
const Aover = Arows.filter((r) => r.overCap).length;
const AwrongCap = Arows.filter((r) => r.queuedRows !== 2).length;
console.log(`  -> over-capacity trials: ${Aover}/10 ; trials not admitting exactly cap: ${AwrongCap}/10`);

console.log("\n=== WAVE B: 32 processes, ALL SAME task id, 10 trials ===");
const Brows = await runWave(32, false, 10);
for (const r of Brows) console.log(`  trial ${r.trial}: queued=${r.queuedRows} dedupAcks=${r.dedupAcks} other=${JSON.stringify(r.other)}`);
const Bwrong = Brows.filter((r) => r.queuedRows !== 1).length;
console.log(`  -> trials not exactly 1 record: ${Bwrong}/10`);

console.log("\n=== VERDICT ===");
console.log(JSON.stringify({
  waveA_over_capacity: `${Aover}/10`,
  waveA_not_exactly_cap: `${AwrongCap}/10`,
  waveB_not_exactly_one: `${Bwrong}/10`,
  mr1_holds: Aover === 0 && AwrongCap === 0 && Bwrong === 0,
}, null, 1));
process.exitCode = (Aover === 0 && AwrongCap === 0 && Bwrong === 0) ? 0 : 4;
