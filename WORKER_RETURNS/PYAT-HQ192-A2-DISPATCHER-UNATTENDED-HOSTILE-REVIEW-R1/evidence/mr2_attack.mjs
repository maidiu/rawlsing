// HQ192-A2 reviewer attack: MR-2 state/sequence ownership + the worker's own
// "return redelivery idempotence" fix. Disposable fixtures only.
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

const D = process.env.HQ192A2_DISPATCHER ||
  "/Users/matthewsmith/Desktop/Rawlsing/review-hq192a2/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const ROOT = "/tmp/hq192a2/mr2";
fs.rmSync(ROOT, { recursive: true, force: true });
fs.mkdirSync(ROOT, { recursive: true });
const m = await import(D);
const out = [];
const rec = (id, claim, outcome, detail) => {
  out.push({ id, claim, outcome, detail: String(detail).slice(0, 400) });
  console.log(`[${outcome}] ${id} :: ${claim} :: ${String(detail).slice(0, 160)}`);
};
const store = (n) => new m.Store(path.join(ROOT, n));
const mkReceipt = () => ({ schema: "LAUNCH_RECEIPT@1.0.0", pid: 1, exit: { code: 0, signal: null },
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high", finished_at: new Date().toISOString() });
const CAND = "c".repeat(40);

// ---- MR-2: store-owned sequence makes collisions structurally impossible ----
{
  const st = store("seq");
  st.recordTaskEvent({ task_id: "T1", attempt: 1, state: "QUEUED", role: "worker" });
  st.recordTaskEvent({ task_id: "T1", attempt: 1, state: "RUNNING", role: "worker" });
  st.recordTaskEvent({ task_id: "T1", attempt: 1, state: "RETURNED", role: "worker", candidate: CAND });
  const evs = st.forTask("T1");
  const states = evs.map((e) => `${e.seq}:${e.state}`);
  rec("MR2-chain", "QUEUED -> RUNNING -> RETURNED fully recorded, none swallowed",
    (evs.length === 3 && evs.map(e => e.state).join(",") === "QUEUED,RUNNING,RETURNED") ? "OK" : "FINDING",
    JSON.stringify(states));
  // caller-supplied seq must be ignored by recordTaskEvent
  const r = st.recordTaskEvent({ task_id: "T1", attempt: 1, seq: 1, state: "FAILED", role: "worker" });
  const evs2 = st.forTask("T1");
  rec("MR2-caller-seq-ignored", "caller-supplied seq is overridden by the store",
    r.appended === true && evs2.length === 4 ? "OK" : "FINDING",
    `appended=${r.appended} total=${evs2.length} seqs=${evs2.map(e => e.seq).join(",")}`);
}
// ---- MR-2: attempt isolation ----
{
  const st = store("attempts");
  st.recordTaskEvent({ task_id: "T2", attempt: 1, state: "QUEUED" });
  st.recordTaskEvent({ task_id: "T2", attempt: 2, state: "QUEUED" });
  const a1 = st.forTask("T2").filter(e => e.attempt === 1), a2 = st.forTask("T2").filter(e => e.attempt === 2);
  rec("MR2-attempt-isolation", "distinct attempts get independent sequences",
    a1.length === 1 && a2.length === 1 && a1[0].seq === 1 && a2[0].seq === 1 ? "OK" : "FINDING",
    JSON.stringify({ a1: a1.map(e => e.seq), a2: a2.map(e => e.seq) }));
}
// ---- MR-2: raw append() still allows caller-supplied seq (legacy escape hatch) ----
{
  const st = store("rawseq");
  st.append({ task_id: "T3", attempt: 1, seq: 1, state: "QUEUED" });
  const r2 = st.append({ task_id: "T3", attempt: 1, seq: 1, state: "RUNNING" });
  rec("MR2-raw-append-collision", "raw append() with a reused seq is still deduped (legacy path)",
    r2.appended === false ? "OK" : "FINDING",
    `appended=${r2.appended} dedup=${r2.dedup} recorded=${JSON.stringify(st.forTask("T3").map(e => e.state))}`);
  rec("MR2-raw-path-note", "public append() remains a caller-seq path; only recordTaskEvent owns seq",
    "NOTE", "documented escape hatch: append() does not set allocateSeq");
}
// ---- worker fix: return redelivery idempotence (sequential case) ----
{
  const st = store("redeliver-seq");
  const r1 = m.deliverReturn(st, { task_id: "R1", candidate_sha: CAND, return_summary: "s", receipt: mkReceipt() });
  const r2 = m.deliverReturn(st, { task_id: "R1", candidate_sha: CAND, return_summary: "s", receipt: mkReceipt() });
  const returns = st.all().filter(e => e.state === "RETURNED");
  rec("redeliver-sequential", "sequential redelivery of the same return is idempotent",
    returns.length === 1 ? "OK" : "FINDING",
    `returns=${returns.length} r1=${JSON.stringify(r1)} r2=${JSON.stringify(r2)}`);
}
// ---- worker fix: return redelivery under CONCURRENT delivery (race attack) ----
const childSrc = `
import { Store, deliverReturn } from ${JSON.stringify(D)};
const [dir, id] = process.argv.slice(2);
const st = new Store(dir);
const receipt = { schema: "LAUNCH_RECEIPT@1.0.0", pid: 1, exit: { code: 0, signal: null },
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high", finished_at: new Date().toISOString() };
let r; try { r = deliverReturn(st, { task_id: "RACE", candidate_sha: "${CAND}", return_summary: "s", receipt }); }
catch (e) { r = { error: e.code || String(e) }; }
process.stdout.write(JSON.stringify({ id, r }));
`;
fs.writeFileSync(path.join(ROOT, "deliver_child.mjs"), childSrc);
const raceTrials = [];
for (let t = 0; t < 14; t++) {
  const dir = path.join(ROOT, `redeliver-race-${t}`);
  fs.mkdirSync(dir, { recursive: true });
  const N = 8;
  const kids = Array.from({ length: N }, (_, i) =>
    spawn("node", [path.join(ROOT, "deliver_child.mjs"), dir, String(i)], { stdio: ["ignore", "pipe", "pipe"] }));
  const outs = await Promise.all(kids.map((k) => new Promise((res) => {
    let s = ""; k.stdout.on("data", (d) => s += d);
    k.on("exit", () => { try { res(JSON.parse(s)); } catch { res({ error: "NO_OUTPUT" }); } });
  })));
  const st = new m.Store(dir);
  const returns = st.all().filter((e) => e.state === "RETURNED");
  const inbox = m.hqInbox(st);
  raceTrials.push({ trial: t, returnedRecords: returns.length,
    inboxReturns: inbox.returns.length, doubleDelivered: returns.length > 1 });
}
const dupTrials = raceTrials.filter((r) => r.doubleDelivered);
rec("redeliver-concurrent", "8 concurrent deliveries of the SAME logical return yield exactly ONE RETURNED record",
  dupTrials.length === 0 ? "OK" : "FINDING",
  `over-delivered in ${dupTrials.length}/14 trials; max RETURNED records=${Math.max(...raceTrials.map(r => r.returnedRecords))}; detail=${JSON.stringify(raceTrials.slice(0, 6))}`);
console.log(JSON.stringify(raceTrials));

fs.writeFileSync(path.join(ROOT, "results.json"), JSON.stringify(out, null, 1));
console.log("\n=== SUMMARY ===");
console.log(JSON.stringify(out.reduce((a, r) => (a[r.outcome] = (a[r.outcome] || 0) + 1, a), {})));
