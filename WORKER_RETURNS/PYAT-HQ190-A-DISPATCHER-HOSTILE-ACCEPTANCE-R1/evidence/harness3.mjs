// HQ190-A harness 3: targeted confirmation of the two load-bearing counterexamples
// and remaining store semantics. Disposable fixtures only.
import fs from "node:fs";
import path from "node:path";
import { spawnSync, spawn } from "node:child_process";
const D = "/Users/matthewsmith/Desktop/Rawlsing/review-hq190a/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const m = await import(D);
const ROOT = "/tmp/hq190a/fixtures/h3";
fs.rmSync(ROOT, { recursive: true, force: true }); fs.mkdirSync(ROOT, { recursive: true });
const out = { findings: [], confirmations: [] };
const rec = (t, o, d) => { out[o].push({ test: t, detail: String(d).slice(0, 500) }); console.log(`[${o}] ${t} :: ${String(d).slice(0, 170)}`); };
const A = "a".repeat(40), B = "b".repeat(40);

// ============ 1. CAPACITY RACE (source-level proof + repeated empirical) ============
// Source-level: slotGate and append are separate _withLock acquisitions.
const src = fs.readFileSync(D, "utf8");
const submitBody = src.slice(src.indexOf("export function submitTask"), src.indexOf("// ----", src.indexOf("export function submitTask")));
const lockCount = (submitBody.match(/_withLock|store\.append/g) || []).length;
rec("submitTask takes the writer lock twice (dedup check, then append) and the capacity gate sits between them",
    "findings", `distinct lock/append operations in submitTask = ${lockCount}; slotGate call is outside any lock`);

function childSrc() {
  return `
import { Store, submitTask } from ${JSON.stringify(D)};
const dir = process.argv[2], id = process.argv[3], wt = process.argv[4];
const st = new Store(dir);
const t = { task_id: "CAP"+id, role: "worker", base_commit: "${A}", worktree: wt, terrain: ["out/**"],
  acceptance_inputs: {x:"1"}, commission_path: "C.md", commission_identity: "${B}",
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { console.log(JSON.stringify({id, ok: submitTask(st, t).queued})); } catch(e){ console.log(JSON.stringify({id, code: e.code})); }
`;
}
fs.writeFileSync("/tmp/hq190a/code/h3_child.mjs", childSrc());
const trials = [];
for (let t = 0; t < 12; t++) {
  const base = path.join(ROOT, `cap-${t}`);
  const dir = path.join(base, "state"), wt = path.join(base, "wt");
  fs.mkdirSync(wt, { recursive: true });
  const N = 6;
  const kids = Array.from({ length: N }, (_, i) => spawn("node", ["/tmp/hq190a/code/h3_child.mjs", dir, String(i), wt], { stdio: ["ignore", "pipe", "pipe"] }));
  const outs = await Promise.all(kids.map((k) => new Promise((res) => { let s = ""; k.stdout.on("data", (d) => s += d); k.on("exit", () => res(s.trim())); })));
  const st = new m.Store(dir);
  const admitted = st.all().filter((e) => e.state === "QUEUED").length;
  trials.push({ trial: t, admitted, refusals: outs.filter((o) => o.includes("SLOT_CAPACITY")).length });
}
const over = trials.filter((r) => r.admitted > 2);
rec(`capacity invariant: 6 concurrent processes vs cap=2 -> admitted 3-4 in ${over.length}/${trials.length} trials (max ${Math.max(...trials.map(r => r.admitted))})`,
    over.length ? "findings" : "confirmations", JSON.stringify(trials));

// ============ 2. STATE TRANSITION SILENTLY SWALLOWED ============
{
  const dir = path.join(ROOT, "state-transition"); const st = new m.Store(dir);
  const e1 = st.append({ task_id: "ST1", attempt: 1, seq: 1, state: "QUEUED" });
  const e2 = st.append({ task_id: "ST1", attempt: 1, seq: 1, state: "RUNNING" });
  const e3 = st.append({ task_id: "ST1", attempt: 1, seq: 1, state: "RETURNED", candidate: "c".repeat(40) });
  const evs = st.forTask("ST1");
  rec("a legitimate state advance carrying the SAME seq is silently dropped (eventKey excludes state)",
      (e2.appended === false && e3.appended === false) ? "findings" : "confirmations",
      `appended=[${e1.appended},${e2.appended},${e3.appended}] recorded_states=${JSON.stringify(evs.map(e => e.state))}`);
}

// ============ 3. TERRAIN: backslash is NOT a separator (POSIX) ============
{
  const t = { terrain: ["out/**"] };
  let pass = null, code = null;
  try { m.terrainGate(t, ["out\\..\\..\\src\\x.py"]); pass = true; } catch (e) { pass = false; code = e.code; }
  rec("a git path containing backslashes is outside 'out/**' and is rejected (no traversal credit)",
      pass === false ? "confirmations" : "findings", `passed=${pass} code=${code}`);
}
// ============ 4. STALE vs HELD LOCK ============
{
  const dir = path.join(ROOT, "lock"); const st = new m.Store(dir);
  fs.writeFileSync(path.join(dir, "writer.lock"), "held");
  const t0 = Date.now();
  let blocked = false, code = null;
  try { st.append({ task_id: "L", attempt: 1, seq: 1, state: "QUEUED" }); } catch (e) { blocked = true; code = e.code; }
  rec("a HELD fresh lock blocks the writer until timeout (no silent concurrent write)",
      blocked && code === "WRITER_LOCK_TIMEOUT" ? "confirmations" : "findings", `blocked=${blocked} code=${code} waited=${Date.now() - t0}ms`);
  const old = Date.now() / 1000 - 120; fs.utimesSync(path.join(dir, "writer.lock"), old, old);
  let reclaimed = false, err = null;
  try { st.append({ task_id: "L", attempt: 1, seq: 2, state: "RUNNING" }); reclaimed = true; } catch (e) { err = e.code; }
  rec("a STALE lock (mtime > 30s) is reclaimed and the write proceeds",
      reclaimed ? "confirmations" : "findings", `reclaimed=${reclaimed} err=${err}`);
  rec("stale-lock reclaim is mtime-based, so a slow-but-live writer (>30s) cannot be distinguished from a dead one",
      "findings", "reclaim test is `Date.now() - stat.mtimeMs > 30000`; no pid liveness check");
}
// ============ 5. fsync scope ============
{
  rec("append fsyncs the log file but not the containing directory",
      src.includes("fs.fsyncSync(fd)") && !/fsyncSync\(.*dir/i.test(src) ? "findings" : "confirmations",
      "fs.fsyncSync(fd) present; no directory fsync -> a crash can lose a rename/creation, not just bytes");
}
// ============ 6. corrupt log: recovery blocking + append refusal ============
{
  const dir = path.join(ROOT, "corrupt"); const st = new m.Store(dir);
  fs.appendFileSync(path.join(dir, "events.jsonl"), '{"task_id":"T","attempt":1,"seq":1,"st');
  const r = m.recover(st);
  let appendRefused = false;
  try { st.append({ task_id: "T", attempt: 1, seq: 1, state: "QUEUED" }); } catch (e) { appendRefused = e.code === "CORRUPT_EVENT_LOG"; }
  rec("torn log => blocking recovery AND append refusal",
      r.blocking === true && appendRefused ? "confirmations" : "findings", `blocking=${r.blocking} appendRefused=${appendRefused}`);
}
fs.writeFileSync(path.join(ROOT, "results.json"), JSON.stringify(out, null, 1));
console.log("\n=== SUMMARY ===");
console.log(JSON.stringify({ findings: out.findings.length, confirmations: out.confirmations.length }));
