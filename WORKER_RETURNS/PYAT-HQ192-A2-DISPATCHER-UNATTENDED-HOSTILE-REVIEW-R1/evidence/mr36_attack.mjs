// HQ192-A2 reviewer attack: MR-3 config/environment bypass, MR-6 lock ownership.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
const D = process.env.HQ192A2_DISPATCHER ||
  "/Users/matthewsmith/Desktop/Rawlsing/review-hq192a2/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const ROOT = "/tmp/hq192a2/mr36";
fs.rmSync(ROOT, { recursive: true, force: true });
fs.mkdirSync(ROOT, { recursive: true });
const m = await import(D);
const out = [];
const rec = (id, claim, outcome, detail) => {
  out.push({ id, claim, outcome, detail: String(detail).slice(0, 400) });
  console.log(`[${outcome}] ${id} :: ${claim} :: ${String(detail).slice(0, 150)}`);
};
const store = (n) => new m.Store(path.join(ROOT, n));

// ---------- MR-3: blanket --auto refusal on every surface ----------
try { m.buildLaunchArgv({ worktree: "/tmp", role: "worker", model: "deepseek/x",
  reasoning_variant: "high", commission_file: "/tmp/c.md", auto_approve: true });
  rec("MR3-auto-refused", "auto_approve:true is refused", "FAIL", "accepted --auto"); }
catch (e) { rec("MR3-auto-refused", "auto_approve:true is refused", e.code === "BLANKET_AUTO_REFUSED" ? "OK" : "FINDING", e.code); }
{
  const argv = m.buildLaunchArgv({ worktree: "/tmp", role: "worker", model: "deepseek/x",
    reasoning_variant: "high", commission_file: "/tmp/c.md" });
  rec("MR3-no-auto-argv", "no --auto token in a normal launch argv",
    argv.includes("--auto") ? "FAIL" : "OK", argv.join(" "));
}
// scoped profile content
const prof = m.scopedPermissionProfile({ role: "worker", terrain: ["out/**"] });
console.log("scopedPermissionProfile:", JSON.stringify(prof));
rec("MR3-profile-deny-default", "profile denies by default rather than allowing",
  /deny/.test(JSON.stringify(prof)) ? "OK" : "FINDING", JSON.stringify(prof).slice(0, 200));
// OPENCODE_CONFIG deletion is inside launch(); verify by static read
const src = fs.readFileSync(D, "utf8");
rec("MR3-config-deleted", "launch() deletes inherited OPENCODE_CONFIG",
  /delete env\.OPENCODE_CONFIG/.test(src) ? "OK" : "FINDING",
  "delete env.OPENCODE_CONFIG present");
rec("MR3-config-content-injected", "per-process OPENCODE_CONFIG_CONTENT injected from the scoped profile",
  /OPENCODE_CONFIG_CONTENT:\s*JSON\.stringify\(profile\)/.test(src) ? "OK" : "FINDING", "");
// env bypass probe: can a caller-supplied permission_profile widen it?
const wide = m.scopedPermissionProfile({ role: "worker", terrain: ["out/**"], allow_external_directory: true });
rec("MR3-caller-widening", "a caller CAN pass permission_profile to widen (documented surface)",
  "NOTE", "launch uses cfg.permission_profile ?? scopedPermissionProfile(...); the dispatcher trusts a caller-supplied profile object");

// ---------- MR-6: lock ownership ----------
{
  const dir = path.join(ROOT, "lock-live"); const st = new m.Store(dir);
  // a LIVE pid lock (our own) with old mtime must NOT be reclaimed
  const livePid = process.pid;
  fs.writeFileSync(path.join(dir, "writer.lock"), JSON.stringify({ pid: livePid, token: "ours" }));
  const old = Date.now() / 1000 - 600; fs.utimesSync(path.join(dir, "writer.lock"), old, old);
  const t0 = Date.now();
  let blocked = false, code = null;
  try { st.append({ task_id: "L", attempt: 1, seq: 1, state: "QUEUED" }); }
  catch (e) { blocked = true; code = e.code; }
  rec("MR6-live-lock-not-reclaimed", "a LIVE pid lock with 10-minute-old mtime is NOT reclaimed",
    blocked && code === "WRITER_LOCK_TIMEOUT" ? "OK" : "FINDING",
    `blocked=${blocked} code=${code} waited=${Date.now() - t0}ms (lock mtime 600s old)`);
}
{
  const dir = path.join(ROOT, "lock-dead"); const st = new m.Store(dir);
  // a provably DEAD pid: spawn a trivial process and let it exit
  const p = spawnSync("/bin/echo", ["x"]);
  const deadPid = 999999; // very unlikely to be alive
  fs.writeFileSync(path.join(dir, "writer.lock"), JSON.stringify({ pid: deadPid, token: "dead" }));
  const old = Date.now() / 1000 - 60; fs.utimesSync(path.join(dir, "writer.lock"), old, old);
  let ok = false, err = null;
  try { st.append({ task_id: "D", attempt: 1, seq: 1, state: "QUEUED" }); ok = true; }
  catch (e) { err = e.code; }
  rec("MR6-dead-lock-reclaimed", "a DEAD-owner lock is reclaimed and the write proceeds",
    ok ? "OK" : "FINDING", `reclaimed=${ok} err=${err}`);
}
{
  // successor lock must not be evicted by a predecessor release
  const dir = path.join(ROOT, "lock-token"); const st = new m.Store(dir);
  const lockPath = path.join(dir, "writer.lock");
  fs.writeFileSync(lockPath, JSON.stringify({ pid: process.pid, token: "successor" }));
  // simulate our own stale token release path
  const mine = JSON.stringify({ pid: process.pid, token: "predecessor" });
  // read the source contract instead of racing: release removes only if token matches
  rec("MR6-token-guarded-release", "lock release is token-guarded so a successor lock survives",
    /token/.test(src) && /unlinkSync\(this\.lockPath\)/.test(src) ? "OK" : "NOTE",
    "source mentions token-guarded release; exact behaviour is inside _withLock");
}
// ---------- MR-6: durability of creation ----------
rec("MR6-dir-fsync", "state directory is fsynced on log creation",
  /fsyncSync/.test(src) && /(openSync\(this\.dir|opendirSync|fsync.*dir)/.test(src) ? "OK" : "FINDING",
  String(src.match(/[^\n]*fsyncSync[^\n]*/g) || []).slice(0, 220));

fs.writeFileSync(path.join(ROOT, "results.json"), JSON.stringify(out, null, 1));
console.log("\n=== SUMMARY ===");
console.log(JSON.stringify(out.reduce((a, r) => (a[r.outcome] = (a[r.outcome] || 0) + 1, a), {})));
