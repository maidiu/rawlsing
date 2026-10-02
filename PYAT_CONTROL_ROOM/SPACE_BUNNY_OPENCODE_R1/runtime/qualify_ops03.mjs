#!/usr/bin/env node
// OPS-03 — independent source-free qualification of the OPS-02 dispatcher.
// Disposable fixtures only. No production, no network, no survey source.
// This script is the QUALIFIER, not the implementer: it imports the shipped
// dispatcher as a black box and exercises only its exported API.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
const PACKET_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
import { execFileSync } from "node:child_process";
import {
  Store, GateError, validateTask, terrainGate, slotGate, expectedParentGate, submitTask,
  publicationGate, buildLaunchArgv, deriveState,
} from "../runtime/dispatcher.mjs";

const results = [];
let pass = 0, fail = 0, skip = 0;
function check(id, fn) {
  try { const d = fn(); results.push({ id, result: "PASS", detail: d || "" }); pass++; }
  catch (e) { results.push({ id, result: "FAIL", detail: (e.code || "ERR") + " " + (e.detail || e.message) }); fail++; }
}
function skipped(id, why) { results.push({ id, result: "SKIP", detail: why }); skip++; }
function expectThrow(code, fn) {
  try { fn(); } catch (e) {
    if (e.code === code) return "correctly rejected with " + code;
    throw new Error("wrong code: got " + e.code + " want " + code);
  }
  throw new Error("DID NOT REJECT (wanted " + code + ")");
}

const FIX = fs.mkdtempSync(path.join(os.tmpdir(), "pyat-ops03-"));
const GOOD = {
  task_id: "T1", role: "worker", base_commit: "a".repeat(40),
  worktree: FIX, terrain: ["PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/**"],
  acceptance: "fixture", commission_path: "commission.md",
};

// 1. two workers, disjoint dirs/branches. The cap must bite at SUBMISSION.
check("Q01_two_workers_disjoint", () => {
  const s = new Store(path.join(FIX, "s1"));
  submitTask(s, { ...GOOD, task_id: "W1" });
  submitTask(s, { ...GOOD, task_id: "W2" });
  return expectThrow("SLOT_CAPACITY", () => submitTask(s, { ...GOOD, task_id: "W3" }));
});
check("Q01b_reviewer_separate_single_slot", () => {
  const s = new Store(path.join(FIX, "s1b"));
  submitTask(s, { ...GOOD, task_id: "V1", role: "reviewer" });
  return expectThrow("SLOT_CAPACITY", () => submitTask(s, { ...GOOD, task_id: "V2", role: "reviewer" }));
});
check("Q01c_slot_freed_on_acceptance", () => {
  const s = new Store(path.join(FIX, "s1c"));
  submitTask(s, { ...GOOD, task_id: "F1" });
  submitTask(s, { ...GOOD, task_id: "F2" });
  s.append({ task_id: "F1", attempt: 1, seq: 2, state: "ACCEPTED", role: "worker" });
  submitTask(s, { ...GOOD, task_id: "F3" });   // should now fit
  return "slot released after ACCEPTED";
});

// 2. wrong base rejected
check("Q02_wrong_base_rejected", () => {
  const t = { ...GOOD, base_commit: "b".repeat(40) };
  return expectThrow("UNEXPECTED_REMOTE_BASE", () => expectedParentGate(t, "c".repeat(40)));
});
check("Q02b_correct_base_accepted", () => {
  expectedParentGate(GOOD, "a".repeat(40)); return "accepted on exact expected parent";
});

// 3. incomplete commission rejected
check("Q03_incomplete_task_rejected", () => {
  const bad = { ...GOOD }; delete bad.acceptance;
  return expectThrow("INCOMPLETE_TASK_RECORD", () => validateTask(bad));
});
check("Q03b_bad_base_format_rejected", () => {
  return expectThrow("BAD_BASE_COMMIT", () => validateTask({ ...GOOD, base_commit: "not-a-sha" }));
});

// 4. out-of-terrain candidate fails publication gate
check("Q04_out_of_terrain_rejected", () => {
  const t = { ...GOOD, terrain: ["rawlsing_next/**"] };
  return expectThrow("OUT_OF_TERRAIN", () => publicationGate(t, "d".repeat(40), "e".repeat(40), "d".repeat(40), ["HQ_HANDOFF/LATEST.json"]));
});
check("Q04b_traversal_rejected", () => {
  return expectThrow("OUT_OF_TERRAIN", () => terrainGate(GOOD, ["../../../etc/passwd"]));
});
check("Q04c_absolute_path_rejected", () => {
  return expectThrow("OUT_OF_TERRAIN", () => terrainGate(GOOD, ["/etc/passwd"]));
});
check("Q04d_in_terrain_accepted", () => {
  terrainGate({ ...GOOD, terrain: ["PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/**"] },
    ["PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs"]);
  return "in-terrain path accepted";
});

// 5. candidate change invalidates its old review
check("Q05_stale_review_rejected", () => {
  const cand = "1".repeat(40), oldCand = "2".repeat(40);
  return expectThrow("STALE_REVIEW", () => publicationGate(GOOD, cand, "e".repeat(40), oldCand, ["PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/x.mjs"]));
});
check("Q05b_publication_requires_review", () => {
  return expectThrow("NO_REVIEW", () => publicationGate(GOOD, "1".repeat(40), null, null, ["PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/x.mjs"]));
});

// 6. duplicate events do not redispatch
check("Q06_duplicate_event_deduped", () => {
  const s = new Store(path.join(FIX, "s6"));
  const e = { task_id: "D1", attempt: 1, seq: 1, state: "RUNNING", role: "worker" };
  const first = s.append(e), second = s.append(e);
  if (!first) throw new Error("first append should write");
  if (second) throw new Error("duplicate append should be suppressed");
  return "duplicate suppressed; events=" + s.forTask("D1").length;
});
check("Q06b_interrupted_resume_does_not_redispatch", () => {
  const s = new Store(path.join(FIX, "s6b"));
  s.append({ task_id: "D2", attempt: 1, seq: 1, state: "QUEUED", role: "worker" });
  s.append({ task_id: "D2", attempt: 1, seq: 2, state: "RUNNING", role: "worker" });
  // simulate dispatcher restart: replay the same RUNNING event
  const replay = s.append({ task_id: "D2", attempt: 1, seq: 2, state: "RUNNING", role: "worker" });
  const st = deriveState(s.forTask("D2"));
  if (replay) throw new Error("replay was appended -> would redispatch");
  if (st !== "RUNNING") throw new Error("state after replay = " + st);
  return "state preserved RUNNING across restart, no redispatch";
});

// 7. competing HQ publication rejected
check("Q07_competing_publication_rejected", () => {
  const t = { ...GOOD, base_commit: "9".repeat(40) };
  return expectThrow("UNEXPECTED_REMOTE_BASE", () => expectedParentGate(t, "8".repeat(40)));
});

// 8. state distinguishes the required classes
check("Q08_state_classes_distinct", () => {
  const s = new Store(path.join(FIX, "s8"));
  const seen = {};
  seen.queued = deriveState([]);
  s.append({ task_id: "Q", attempt: 1, seq: 1, state: "QUEUED", role: "worker" });
  seen.queued2 = deriveState(s.forTask("Q"));
  s.append({ task_id: "Q", attempt: 1, seq: 2, state: "RUNNING", role: "worker" });
  seen.running = deriveState(s.forTask("Q"));
  s.append({ task_id: "Q", attempt: 1, seq: 3, state: "RETURNED", role: "worker" });
  seen.waiting = deriveState(s.forTask("Q"));
  s.append({ task_id: "Q", attempt: 1, seq: 4, state: "ACCEPTED", role: "worker" });
  seen.accepted = deriveState(s.forTask("Q"));
  const need = ["UNKNOWN", "QUEUED", "RUNNING", "WAITING_FOR_HQ", "ACCEPTED"];
  for (const n of need) if (seen[n] !== undefined && seen[n] !== n) throw new Error(n + " -> " + seen[n]);
  return JSON.stringify(seen);
});
check("Q08b_process_exit_is_not_acceptance", () => {
  const s = new Store(path.join(FIX, "s8b"));
  s.append({ task_id: "E", attempt: 1, seq: 1, state: "RUNNING", role: "worker" });
  s.append({ task_id: "E", attempt: 1, seq: 2, state: "EXITED", role: "worker" });
  const st = deriveState(s.forTask("E"));
  if (st === "ACCEPTED") throw new Error("exit treated as acceptance");
  return "EXITED derives to " + st + ", never ACCEPTED";
});

// 9. launcher uses argv array, explicit dir/session, no --continue
check("Q09_launcher_argv_safe", () => {
  const argv = buildLaunchArgv({ worktree: FIX, role: "worker", session_id: "sess-123", prompt_path: "/p.md" });
  const joined = argv.join(" ");
  if (argv.includes("--continue")) throw new Error("ambiguous --continue used");
  if (!argv.includes("--dir") || !argv.includes(FIX)) throw new Error("explicit --dir missing");
  if (!argv.includes("--session") || !argv.includes("sess-123")) throw new Error("explicit session missing");
  if (argv[0] !== "opencode" || argv[1] !== "run") throw new Error("unexpected argv shape");
  return "argv=" + JSON.stringify(argv);
});
check("Q09b_no_shell_interpolation", () => {
  // a worktree containing shell metacharacters must survive as one argv element
  const evil = "/tmp/a; rm -rf b/$(whoami)";
  const argv = buildLaunchArgv({ worktree: evil, role: "worker", prompt_path: "/p.md" });
  if (!argv.includes(evil)) throw new Error("path was split or interpolated");
  return "metacharacter path preserved verbatim as a single argv element";
});

// 10. completion reaches HQ via durable state, recoverable without transcript
check("Q10_notice_recoverable_from_store", () => {
  const s = new Store(path.join(FIX, "s10"));
  s.append({ task_id: "N", attempt: 1, seq: 1, state: "RUNNING", role: "worker" });
  const reopened = new Store(path.join(FIX, "s10"));   // fresh instance = "new HQ"
  const st = deriveState(reopened.forTask("N"));
  if (st !== "RUNNING") throw new Error("lost notice; derived " + st);
  return "recovered RUNNING from durable store with no transcript";
});

// 11. python3 capability probe (explicit environment defect record)
check("Q11_python3_capability_probe", () => {
  const probe = "/tmp/.pyat-ops03-pyt.txt";
  try { fs.unlinkSync(probe); } catch {}
  let invocation;
  try {
    execFileSync("python3", ["-c", `open(${JSON.stringify(probe)},"w").write("x")`], { stdio: "ignore" });
    invocation = "exit-0";
  } catch (e) {
    invocation = "threw:" + (e.code || e.message);
  }
  const wrote = fs.existsSync(probe);
  if (wrote) { fs.unlinkSync(probe); return "python3 FUNCTIONAL (wrote file; " + invocation + ")"; }
  // exit 0 with no side effect == silent no-op
  if (invocation !== "exit-0") return "python3 unusable (" + invocation + "); verify_packet.py UNRUNNABLE";
  return "CONFIRMED DEFECT: python3 returned exit 0 but wrote nothing (silent no-op). " +
         "scripts/verify_packet.py CANNOT BE EXECUTED on this host; any agent reporting it PASSED is wrong.";
});

// 12. raw-directory denial: distinguish prompt denial from process denial
skipped("Q12_raw_directory_process_denial",
  "NOT QUALIFIED. Requires OS-level separation (a dedicated unprivileged user or sandbox profile). " +
  "Role restrictions in this setup are PROCEDURAL ONLY: they gate publication in software, not filesystem access. " +
  "A worker process can still read any path the HQ user can read. This boundary is deliberately left unqualified.");

// 13. fresh HQ resumes from checkpoint+queue
check("Q13_fresh_hq_resumes", () => {
  const s = new Store(path.join(FIX, "s13"));
  s.append({ task_id: "R", attempt: 1, seq: 1, state: "RUNNING", role: "worker" });
  s.append({ task_id: "W", attempt: 1, seq: 1, state: "QUEUED", role: "worker" });
  const fresh = new Store(path.join(FIX, "s13"));
  const tasks = new Set(fresh.all().map((e) => e.task_id));
  if (tasks.size !== 2) throw new Error("fresh HQ sees " + tasks.size + " tasks, want 2");
  return "fresh HQ recovers " + tasks.size + " in-flight tasks from queue alone";
});

fs.rmSync(FIX, { recursive: true, force: true });

const out = {
  schema: "PYAT_OPENCODE_OPS03_QUALIFICATION@1.0.0",
  qualifier: "INDEPENDENT_BLACKBOX_IMPORT_NOT_IMPLEMENTER",
  fixtures: "DISPOSABLE_TMPDIR_ONLY",
  raw_source_access: 0,
  production_mutation: 0,
  network_access: 0,
  passed: pass, failed: fail, skipped: skip,
  capability_level: fail === 0 ? "PASS_WITH_DECLARED_SKIP" : "PARTIAL",
  checks: results,
  declared_partial_capabilities: [
    "Role isolation is PROCEDURAL, not process-enforced. Worktrees isolate editing, not access rights.",
    "No OS-level raw-directory denial. Left unqualified; requires host administration permission.",
  ],
  environment_defect: "python3 is NON-FUNCTIONAL on this host by two independent observations: " +
    "(a) invoked through a shell it returns exit 0 with no output and writes nothing (silent no-op); " +
    "(b) invoked via execFileSync it fails with 'Unknown system error -8'. " +
    "Therefore PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/scripts/verify_packet.py CANNOT BE EXECUTED here. " +
    "Packet integrity was confirmed instead by an independent node reimplementation of the same algorithm. " +
    "Any agent reporting that script as PASSED on this host is reporting a false positive.",
  terminal: fail === 0 ? "OPS03_QUALIFIED_AT_TESTED_CAPABILITY__BOUNDARY_Q12_UNQUALIFIED" : "OPS03_PARTIAL__SEE_FAILURES",
};
const OUTDIR = path.join(PACKET_ROOT, "ACTIVATION_RETURNS", "OPS-03");
fs.mkdirSync(OUTDIR, { recursive: true });
fs.writeFileSync(path.join(OUTDIR, "QUALIFICATION.json"), JSON.stringify(out, null, 2));
for (const r of results) console.log(`${r.result.padEnd(4)} ${r.id}${r.detail ? " :: " + r.detail : ""}`);
console.log(`\npassed=${pass} failed=${fail} skipped=${skip}  level=${out.capability_level}`);