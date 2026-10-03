// HQ190-A attack harness 2: state-transition integrity, dedup keys, capacity race,
// lifecycle/recovery, and real-process behaviour. Disposable fixtures only.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync, spawn } from "node:child_process";

const D = "/Users/matthewsmith/Desktop/Rawlsing/review-hq190a/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const m = await import(D);
const ROOT = "/tmp/hq190a/fixtures/h2";
fs.rmSync(ROOT, { recursive: true, force: true });
fs.mkdirSync(ROOT, { recursive: true });

const results = [];
const rec = (id, claim, outcome, detail) => {
  results.push({ id, claim, outcome, detail: String(detail).slice(0, 400) });
  console.log(`[${outcome}] ${id} :: ${claim} :: ${String(detail).slice(0, 150)}`);
};
const sh = (cwd, args) => spawnSync("git", args, { cwd, encoding: "utf8" });
function mkRepo(name) {
  const dir = path.join(ROOT, name);
  fs.mkdirSync(dir, { recursive: true });
  sh(dir, ["init", "-q"]); sh(dir, ["config", "user.email", "f@x"]); sh(dir, ["config", "user.name", "f"]);
  return dir;
}
const A = "a".repeat(40), B = "b".repeat(40);
function baseTask(over = {}) {
  const wt = mkRepo("wt-" + Math.random().toString(36).slice(2, 7));
  return { task_id: "T1", role: "worker", base_commit: A, worktree: wt, terrain: ["out/**"],
    acceptance_inputs: { x: "1" }, commission_path: "C.md", commission_identity: B,
    model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high", ...over };
}
const store = (n) => new m.Store(path.join(ROOT, n));

// ---- dedup key silently swallows legitimate state transitions -------------
{
  const st = store("dedup-state");
  st.append({ task_id: "T1", attempt: 1, seq: 1, state: "QUEUED" });
  const r2 = st.append({ task_id: "T1", attempt: 1, seq: 1, state: "RUNNING" });
  const events = st.forTask("T1");
  rec("F-state-swallow", "same seq with a DIFFERENT state is silently deduped",
    r2.appended ? "OK" : "FINDING",
    `appended=${r2.appended} dedup=${r2.dedup}; events recorded=${events.length}; states=${events.map(e => e.state)}`);
  // Consequence: a caller advancing state without bumping seq loses the transition.
  rec("F-state-consequence", "state machine integrity depends on caller-chosen seq uniqueness",
    "FINDING", "dedup key is task_id|attempt|seq only; 'state' is not part of identity");
}
// ---- capacity is checked outside the append lock (TOCTOU window) ----------
{
  const st = store("cap");
  const t1 = baseTask({ task_id: "C1", role: "worker", worktree: mkRepo("cw1") });
  m.submitTask(st, t1);
  // Simulate the window: read active count, then let another actor fill the slot.
  const activeBefore = m.activeTaskIds(st, "worker");
  st.append({ task_id: "C2", attempt: 1, seq: 1, state: "QUEUED", role: "worker" });
  try { m.slotGate(st, "worker", { exclude_task: "C3" }); rec("F-cap-toctou", "slotGate reflects concurrent fill", "OK", "gate saw the concurrent write"); }
  catch (e) { rec("F-cap-toctou", "slotGate reflects concurrent fill", "REJECTED", e.code); }
  rec("F-cap-structure", "capacity check and append are separate lock acquisitions (no single atomic admission)",
    "FINDING", `activeBefore=${activeBefore.size}; slotGate+append are distinct _withLock scopes`);
}
// ---- duplicate submission across distinct OS processes -------------------
await (async () => {
  const dir = path.join(ROOT, "race-dup"); 
  const script = `
import { Store, submitTask } from ${JSON.stringify(D)};
const dir = process.argv[2], id = process.argv[3];
const st = new Store(dir);
const t = { task_id: "R1", role: "worker", base_commit: "${A}", worktree: "${ROOT}/race-dup-wt",
  terrain: ["out/**"], acceptance_inputs: {x:"1"}, commission_path: "C.md", commission_identity: "${B}",
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { console.log(JSON.stringify({id, r: submitTask(st, t)})); }
catch(e){ console.log(JSON.stringify({id, code: e.code, detail: e.detail})); }
`;
  fs.mkdirSync(path.join(ROOT, "race-dup-wt"), { recursive: true });
  fs.writeFileSync("/tmp/hq190a/code/race_dup.mjs", script);
  const kids = [0, 1, 2, 3].map((i) => spawn("node", ["/tmp/hq190a/code/race_dup.mjs", dir, String(i)], { stdio: ["ignore", "pipe", "pipe"] }));
  const outs = await Promise.all(kids.map((k) => new Promise((res) => { let s = ""; k.stdout.on("data", (d) => s += d); k.on("exit", () => res(s.trim())); })));
  const st = new m.Store(dir);
  const queued = st.forTask("R1").filter((e) => e.state === "QUEUED");
  const parsed = outs.map((o) => { try { return JSON.parse(o); } catch { return { raw: o.slice(0, 120) }; } });
  const dupAcks = parsed.filter((p) => p.r && (p.r.idempotent || p.r.dedup)).length;
  rec("F-race-dup", "4 concurrent processes submitting the same task yield exactly one QUEUED row",
    queued.length === 1 && dupAcks === 3 ? "OK" : "FINDING",
    `queued=${queued.length} dupAcks=${dupAcks} outcomes=${JSON.stringify(parsed.map(p => p.r ? (p.r.idempotent ? "dup" : "new") : p.code))}`);
})();
// ---- capacity race across distinct OS processes --------------------------
await (async () => {
  const dir = path.join(ROOT, "race-cap");
  const wt = path.join(ROOT, "race-cap-wt"); fs.mkdirSync(wt, { recursive: true });
  const script = `
import { Store, submitTask } from ${JSON.stringify(D)};
const dir = process.argv[2], id = process.argv[3];
const st = new Store(dir);
const t = { task_id: "CAP"+id, role: "worker", base_commit: "${A}", worktree: "${wt}",
  terrain: ["out/**"], acceptance_inputs: {x:"1"}, commission_path: "C.md", commission_identity: "${B}",
  model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high" };
try { console.log(JSON.stringify({id, r: submitTask(st, t)})); }
catch(e){ console.log(JSON.stringify({id, code: e.code})); }
`;
  fs.writeFileSync("/tmp/hq190a/code/race_cap.mjs", script);
  const kids = [0, 1, 2, 3, 4, 5].map((i) => spawn("node", ["/tmp/hq190a/code/race_cap.mjs", dir, String(i)], { stdio: ["ignore", "pipe", "pipe"] }));
  const outs = await Promise.all(kids.map((k) => new Promise((res) => { let s = ""; k.stdout.on("data", (d) => s += d); k.on("exit", () => res(s.trim())); })));
  const st = new m.Store(dir);
  const queued = st.all().filter((e) => e.state === "QUEUED");
  const refused = outs.filter((o) => o.includes("SLOT_CAPACITY")).length;
  rec("F-race-cap", "6 processes racing a cap of 2 admit exactly 2",
    queued.length === 2 ? "OK" : "FINDING",
    `queued=${queued.length} capacityRefusals=${refused} (cap=2)`);
})();
// ---- restart / recovery semantics ---------------------------------------
{
  const st = store("recover");
  const t = baseTask({ task_id: "REC1" });
  m.submitTask(st, t);
  const r1 = m.recover(st);
  const task = r1.tasks.find((x) => x.task_id === "REC1");
  rec("G-restart-before", "restart before launch reconstructs full binding",
    task && task.binding_complete ? "OK" : "FINDING", JSON.stringify(task));
  // exit does not become RETURNED
  const receipt = { schema: "LAUNCH_RECEIPT@1.0.0", pid: 999, exit: { code: 0, signal: null }, model: t.model, reasoning_variant: t.reasoning_variant, finished_at: new Date().toISOString() };
  st.append({ task_id: "REC1", attempt: 1, seq: 2, state: "RETURNED", role: "hq-inbox", candidate: "c".repeat(40), binding: { return_summary: "s", launch_receipt: receipt } });
  const inbox = m.hqInbox(st);
  rec("G-inbox", "delivery visible in HQ inbox without chat copy", inbox.returns.length === 1 ? "OK" : "FINDING", JSON.stringify(inbox.awaiting_adjudication));
  // undelivered RETURNED (no candidate) must not count as a return
  st.append({ task_id: "REC2", attempt: 1, seq: 1, state: "RETURNED", role: "hq-inbox" });
  const inbox2 = m.hqInbox(st);
  rec("G-undelivered", "candidate-less RETURNED is not a return", inbox2.returns.length === 1 && inbox2.undelivered_returned_events === 1 ? "OK" : "FINDING", JSON.stringify({ returns: inbox2.returns.length, undelivered: inbox2.undelivered_returned_events }));
}
// ---- deliverReturn gate --------------------------------------------------
{
  const st = store("deliver");
  try { m.deliverReturn(st, { task_id: "D1", candidate_sha: "c".repeat(40), return_summary: "s", receipt: null }); rec("G-deliver-noreceipt", "delivery without launch receipt refused", "FAIL_ACCEPTED", "delivered"); }
  catch (e) { rec("G-deliver-noreceipt", "delivery without launch receipt refused", "REJECTED", e.code); }
  try { m.deliverReturn(st, { task_id: "D1", candidate_sha: "UNBOUND", return_summary: "s", receipt: { schema: "LAUNCH_RECEIPT@1.0.0", finished_at: "x" } }); rec("G-deliver-badsha", "delivery with placeholder candidate refused", "FAIL_ACCEPTED", "delivered"); }
  catch (e) { rec("G-deliver-badsha", "delivery with placeholder candidate refused", "REJECTED", e.code); }
  try { m.deliverReturn(st, { task_id: "D1", candidate_sha: "c".repeat(40), return_summary: "s", receipt: { schema: "LAUNCH_RECEIPT@1.0.0" } }); rec("G-deliver-unfinished", "delivery of unfinished launch refused", "FAIL_ACCEPTED", "delivered unfinished"); }
  catch (e) { rec("G-deliver-unfinished", "delivery of unfinished launch refused", "REJECTED", e.code); }
}
// ---- publication gate with real git repositories -------------------------
{
  const repo = mkRepo("pub");
  fs.mkdirSync(path.join(repo, "out"), { recursive: true });
  fs.writeFileSync(path.join(repo, "out", "a.txt"), "a");
  sh(repo, ["add", "-A"]); sh(repo, ["commit", "-qm", "base"]);
  const baseSha = sh(repo, ["rev-parse", "HEAD"]).stdout.trim();
  fs.writeFileSync(path.join(repo, "out", "a.txt"), "b");
  sh(repo, ["add", "-A"]); sh(repo, ["commit", "-qm", "cand"]);
  const candSha = sh(repo, ["rev-parse", "HEAD"]).stdout.trim();
  const task = baseTask({ base_commit: baseSha, worktree: repo, terrain: ["out/**"] });
  const review = { candidate_sha: candSha, review_sha: "d".repeat(40), disposition: "APPROVE" };
  const adj = m.buildAdjudication({ decision_id: "DC", task_id: task.task_id, candidate_sha: candSha, review_sha: review.review_sha, disposition: "APPROVE" });
  try {
    const r = m.publicationGate({ repo, task, candidate_ref: candSha, review, adjudication: adj, check_remote: false });
    rec("H-pub-ok", "in-terrain candidate publishes", r.eligible ? "OK" : "FAIL", JSON.stringify(r.changed_paths));
  } catch (e) { rec("H-pub-ok", "in-terrain candidate publishes", "FAIL_REJECTED", e.code + " " + e.detail); }
  // out-of-terrain change
  fs.writeFileSync(path.join(repo, "secret.py"), "x");
  sh(repo, ["add", "-A"]); sh(repo, ["commit", "-qm", "oob"]);
  const oobSha = sh(repo, ["rev-parse", "HEAD"]).stdout.trim();
  const review2 = { candidate_sha: oobSha, review_sha: "d".repeat(40), disposition: "APPROVE" };
  const adj2 = m.buildAdjudication({ decision_id: "DC2", task_id: task.task_id, candidate_sha: oobSha, review_sha: review2.review_sha, disposition: "APPROVE" });
  try { m.publicationGate({ repo, task, candidate_ref: oobSha, review: review2, adjudication: adj2, check_remote: false }); rec("H-terrain", "out-of-terrain rejected from git diff", "FAIL_ACCEPTED", "published OOB"); }
  catch (e) { rec("H-terrain", "out-of-terrain rejected from git diff", e.code === "OUT_OF_TERRAIN" ? "OK" : "FINDING_WRONG_REASON", e.code); }
  // review bound to a different candidate
  const wrongReview = { candidate_sha: baseSha, review_sha: "d".repeat(40), disposition: "APPROVE" };
  try { m.publicationGate({ repo, task, candidate_ref: candSha, review: wrongReview, adjudication: adj, check_remote: false }); rec("H-review-bind", "review bound to another candidate rejected", "FAIL_ACCEPTED", "published"); }
  catch (e) { rec("H-review-bind", "review bound to another candidate rejected", e.code === "IDENTITY_MISMATCH" ? "OK" : "FINDING_WRONG_REASON", e.code); }
  // nonapproving review
  const rejReview = { candidate_sha: candSha, review_sha: "d".repeat(40), disposition: "REJECT" };
  try { m.publicationGate({ repo, task, candidate_ref: candSha, review: rejReview, adjudication: adj, check_remote: false }); rec("H-review-reject", "non-approving review blocks publication", "FAIL_ACCEPTED", "published"); }
  catch (e) { rec("H-review-reject", "non-approving review blocks publication", e.code === "REVIEW_NOT_APPROVING" ? "OK" : "FINDING_WRONG_REASON", e.code); }
  // unrelated base/candidate objects that exist but are not related as claimed
  try { m.publicationGate({ repo, task: baseTask({ base_commit: "9".repeat(40), worktree: repo, terrain: ["out/**"] }), candidate_ref: candSha, review, adjudication: adj, check_remote: false }); rec("H-unrelated", "unresolvable base fails closed", "FAIL_ACCEPTED", "published"); }
  catch (e) { rec("H-unrelated", "unresolvable base fails closed", "OK", e.code); }
}
// ---- launch arg construction (F) ----------------------------------------
{
  const ok = m.buildLaunchArgv({ worktree: "/tmp/w", role: "worker", model: "deepseek/deepseek-v4.1-flash", reasoning_variant: "high", commission_file: "/tmp/c.md", prompt: "P" });
  const iPrompt = ok.indexOf("P"), iFile = ok.indexOf("--file");
  rec("I-argv-order", "prompt precedes --file (array option)", iPrompt >= 0 && iPrompt < iFile ? "OK" : "FINDING", ok.join(" "));
  rec("I-argv-sep", "model and variant are separate flags", ok.includes("--model") && ok.includes("--variant") ? "OK" : "FAIL", ok.join(" "));
  try { m.buildLaunchArgv({ worktree: "/tmp/w", role: "worker", model: "bad", reasoning_variant: "space-bunny-free", commission_file: "/tmp/c.md" }); rec("I-argv-bad", "bad model/variant rejected", "FAIL_ACCEPTED", "accepted"); }
  catch (e) { rec("I-argv-bad", "bad model/variant rejected", "OK", e.code); }
  try { m.buildLaunchArgv({ worktree: "/tmp/w", role: "worker", model: "deepseek/x", reasoning_variant: "high" }); rec("I-argv-nofile", "missing commission_file rejected", "FAIL_ACCEPTED", "accepted"); }
  catch (e) { rec("I-argv-nofile", "missing commission_file rejected", "OK", e.code); }
}

fs.writeFileSync(path.join(ROOT, "results.json"), JSON.stringify(results, null, 1));
console.log("\n=== SUMMARY ===");
console.log(JSON.stringify(results.reduce((a, r) => (a[r.outcome] = (a[r.outcome] || 0) + 1, a), {})));
console.log("findings:");
for (const r of results.filter(r => r.outcome.startsWith("FINDING") || r.outcome.startsWith("FAIL"))) console.log("  -", r.id, "|", r.claim, "|", r.detail.slice(0, 200));
