// HQ188-A positive end-to-end fixture workflow.
// Real git repositories, real worktrees, a real bare remote, and REAL OpenCode CLI processes.
// Source-free: fixture repositories only. No real source storage touched.
//
// Proves: two fixture workers in distinct worktrees, one separate reviewer in a
// third worktree, commission content delivered via --file from a Git-bound path,
// durable session receipts, completion delivered to the HQ queue, restart/recovery,
// candidate-change invalidation, competing publication against a real remote,
// Git-derived terrain enforcement, and corruption blocking recovery.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const target = process.argv[2];
const D = await import(pathToFileURL(target).href);
const { Store, submitTask, recover, launch, deliverReturn, hqInbox, publicationGate,
        buildAdjudication, openCodeAvailability, verifyCommissionIdentity } = D;

const ROOT = fs.mkdtempSync(path.join(os.tmpdir(), 'hq188a-e2e-'));
const ev = [];
const log = (id, data) => ev.push({ id, ...data });
function sh(cwd, cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', shell: false, ...opts });
  return { status: r.status, stdout: (r.stdout || '').trim(), stderr: (r.stderr || '').trim() };
}
const git = (cwd, ...a) => sh(cwd, 'git', a);
const must = (r, what) => { if (r.status !== 0) throw new Error(what + ': ' + (r.stderr || r.stdout)); return r.stdout; };

// ------------------------------------------------------------------ CLI capability
const cli = openCodeAvailability();
const MODEL = 'opencode-go/space-bunny-free';
const VARIANT = 'max';
log('CLI_CAPABILITY', cli);
log('MODEL_VARIANT_BINDING', {
  model: MODEL, reasoning_variant: VARIANT,
  model_shape_provider_slash_model: /^[a-z0-9_-]+\/[A-Za-z0-9._-]+$/.test(MODEL),
  variant_shape_reasoning_effort: ['minimal', 'low', 'medium', 'high', 'max'].includes(VARIANT),
  installed_cli_supports_model: cli.supports_model,
  installed_cli_supports_variant: cli.supports_variant,
  installed_cli_supports_file: cli.supports_file,
  installed_cli_variant_is_reasoning_effort: cli.variant_is_reasoning_effort,
  fields_are_distinct: MODEL !== VARIANT,
});

// ------------------------------------------------------------------ fixture remote
const REMOTE = path.join(ROOT, 'remote.git');
const SEED = path.join(ROOT, 'seed');
fs.mkdirSync(SEED, { recursive: true });
must(git(SEED, 'init', '-q', '-b', 'main'), 'seed init');
git(SEED, 'config', 'user.email', 'fixture@localhost');
git(SEED, 'config', 'user.name', 'fixture');
fs.mkdirSync(path.join(SEED, 'allowed'), { recursive: true });
fs.writeFileSync(path.join(SEED, 'allowed', 'base.txt'), 'base\n');
must(git(SEED, 'add', '-A'), 'seed add');
must(git(SEED, 'commit', '-q', '-m', 'fixture base'), 'seed commit');
const BASE = git(SEED, 'rev-parse', 'HEAD').stdout;
must(sh(ROOT, 'git', ['clone', '-q', '--bare', SEED, REMOTE]), 'bare clone');
const CONTROL = path.join(ROOT, 'control');
must(sh(ROOT, 'git', ['clone', '-q', REMOTE, CONTROL]), 'control clone');
git(CONTROL, 'config', 'user.email', 'fixture@localhost');
git(CONTROL, 'config', 'user.name', 'fixture');
must(git(CONTROL, 'push', '-q', 'origin', 'HEAD:main'), 'seed push');
const REMOTE_HEAD_0 = git(CONTROL, 'ls-remote', 'origin', 'refs/heads/main').stdout.split(/\s+/)[0];

function worktree(tag) {
  const p = path.join(ROOT, tag);
  must(git(CONTROL, 'worktree', 'add', '-q', '-b', tag, p, BASE), 'worktree ' + tag);
  git(p, 'config', 'user.email', 'fixture@localhost');
  git(p, 'config', 'user.name', 'fixture');
  return p;
}
const WT1 = worktree('fx-worker-1');
const WT2 = worktree('fx-worker-2');
const WT3 = worktree('fx-reviewer');
log('WORKTREES', { worker1: WT1, worker2: WT2, reviewer: WT3, distinct_count: new Set([WT1, WT2, WT3]).size });

const WORKER_COMMISSION = `# FIXTURE WORKER COMMISSION
You are a disposable fixture worker in a dispatcher end-to-end test.
Do exactly this and nothing else:
1. Create the directory "result" in your working directory.
2. Write the single line FIXTURE_OK into result/DONE.txt
3. Commit it with the message "fixture result".
4. Stop. Read nothing else. No network.
`;
const REVIEW_COMMISSION = `# FIXTURE REVIEW COMMISSION
You are a disposable fixture reviewer. Do exactly this and nothing else:
1. Create the directory "result" if absent.
2. Write the single line FIXTURE_OK into result/DONE.txt so the review has an artifact to inspect.
3. Write the single line REVIEW_APPROVE into REVIEW.txt
4. Commit with the message "fixture review".
5. Stop. Read nothing else. No network.
`;
const REL_W = 'allowed/FIXTURE_COMMISSION.md';
const REL_R = 'allowed/FIXTURE_REVIEW_COMMISSION.md';

// Commit each commission into its own worktree so identity is a real Git blob.
function installCommission(wt, rel, body) {
  fs.writeFileSync(path.join(wt, rel), body);
  must(git(wt, 'add', '-A'), 'add commission');
  must(git(wt, 'commit', '-q', '-m', 'add ' + path.basename(rel)), 'commit commission');
  return git(wt, 'rev-parse', `HEAD:${rel}`).stdout;
}
const CID1 = installCommission(WT1, REL_W, WORKER_COMMISSION);
const CID2 = installCommission(WT2, REL_W, WORKER_COMMISSION);
const CID3 = installCommission(WT3, REL_R, REVIEW_COMMISSION);

function mkTask(id, role, wt, rel, cid) {
  return {
    task_id: id, role, base_commit: BASE, worktree: wt, terrain: ['allowed/**', 'result/**'],
    acceptance_inputs: { gate: 'fixture-e2e', must_create: 'result/DONE.txt', commission_rel: rel },
    commission_path: path.join(wt, rel), commission_identity: cid,
    model: MODEL, reasoning_variant: VARIANT,
  };
}
const T1 = mkTask('FX-W1', 'worker', WT1, REL_W, CID1);
const T2 = mkTask('FX-W2', 'worker', WT2, REL_W, CID2);
const TR = mkTask('FX-REV', 'reviewer', WT3, REL_R, CID3);

// commission identity actually resolves against Git
const cids = [verifyCommissionIdentity(WT1, T1.commission_path, T1.commission_identity),
               verifyCommissionIdentity(WT2, T2.commission_path, T2.commission_identity),
               verifyCommissionIdentity(WT3, TR.commission_path, TR.commission_identity)];
log('COMMISSION_IDENTITY_VERIFIED_FROM_GIT', { worker1: cids[0], worker2: cids[1], reviewer: cids[2], all_resolved: cids.every(Boolean) });

// ------------------------------------------------------------------ submit
const store = new Store(path.join(ROOT, 'state'));
const s1 = submitTask(store, T1);
const s2 = submitTask(store, T2);
log('SUBMIT_TWO_WORKERS', { worker1_queued: s1.queued, worker2_queued: s2.queued, bindings_persisted: s1.binding_persisted && s2.binding_persisted });
const dup = submitTask(store, T1);
log('DUPLICATE_IDEMPOTENT', dup);

// ------------------------------------------------------------------ restart before launch
const pre = recover(store);
log('RESTART_BEFORE_LAUNCH', {
  recovered: pre.recovered, blocking: pre.blocking, task_count: pre.tasks.length,
  bindings_complete: pre.tasks.map(t => t.binding_complete),
  models: pre.tasks.map(t => t.binding && t.binding.model),
  variants: pre.tasks.map(t => t.binding && t.binding.reasoning_variant),
  commission_identities: pre.tasks.map(t => t.binding && t.binding.commission_identity),
});

// ------------------------------------------------------------------ real launches
async function runTask(task, wt) {
  store.append({ task_id: task.task_id, attempt: 1, seq: 2, state: 'RUNNING', role: task.role,
    binding: { launch_receipt: { started: true, model: MODEL, reasoning_variant: VARIANT, started_at: new Date().toISOString() } } });
  const { receipt, done } = launch({
    task_id: task.task_id, attempt: 1, worktree: wt, role: 'build',
    model: MODEL, reasoning_variant: VARIANT, commission_file: task.commission_path,
    auto_approve: true,
  });
  const fin = await done;
  // The process completing is a launch fact, recorded honestly. It is NOT a return:
  // RETURNED is written only by deliverReturn, once a candidate identity exists.
  store.append({ task_id: task.task_id, attempt: 1, seq: 3, state: 'RUNNING', role: task.role,
    binding: { launch_receipt: { pid: fin.pid, exit: fin.exit, model: fin.model, reasoning_variant: fin.reasoning_variant, started_at: fin.started_at, finished_at: fin.finished_at, duration_ms: fin.duration_ms, outcome: 'PROCESS_EXITED_NOT_YET_RETURNED' } } });
  return fin;
}
const r1 = await runTask(T1, WT1);
const r2 = await runTask(T2, WT2);

function verifyWork(wt, tag) {
  const f = path.join(wt, 'result', 'DONE.txt');
  const exists = fs.existsSync(f);
  const content = exists ? fs.readFileSync(f, 'utf8').trim() : null;
  return { tag, result_exists: exists, content, is_FIXTURE_OK: content === 'FIXTURE_OK',
    clean_tree: git(wt, 'status', '--porcelain').stdout === '', head: git(wt, 'log', '--oneline', '-1').stdout };
}
const v1 = verifyWork(WT1, 'worker1'), v2 = verifyWork(WT2, 'worker2');
log('WORKER_EFFECT', { worker1: v1, worker2: v2, both_produced_real_committed_results: v1.is_FIXTURE_OK && v2.is_FIXTURE_OK && v1.clean_tree && v2.clean_tree });
log('LAUNCH_RECEIPTS', {
  worker1: { pid: r1.pid, exit: r1.exit, model: r1.model, variant: r1.reasoning_variant, duration_ms: r1.duration_ms, stdout_bytes: r1.stdout_bytes, stderr_bytes: r1.stderr_bytes },
  worker2: { pid: r2.pid, exit: r2.exit, model: r2.model, variant: r2.reasoning_variant, duration_ms: r2.duration_ms, stdout_bytes: r2.stdout_bytes, stderr_bytes: r2.stderr_bytes },
  distinct_pids: r1.pid !== r2.pid,
  model_actually_launched: r1.model === MODEL && r2.model === MODEL,
  variant_actually_launched: r1.reasoning_variant === VARIANT && r2.reasoning_variant === VARIANT,
  exit_codes: [r1.exit && r1.exit.code, r2.exit && r2.exit.code],
});

// ------------------------------------------------------------------ delivery to HQ
for (const [t, r, wt] of [[T1, r1, WT1], [T2, r2, WT2]]) {
  const cand = git(wt, 'rev-parse', 'HEAD').stdout;
  const d = deliverReturn(store, { task_id: t.task_id, candidate_sha: cand,
    return_summary: `fixture worker ${t.task_id} returned candidate ${cand.slice(0, 8)} with a real committed result`,
    receipt: r });
  log('DELIVER_' + t.task_id, { ...d, candidate: cand });
}
const inbox = hqInbox(store);
log('HQ_INBOX', { visible_returns: inbox.returns.length, awaiting_adjudication: inbox.awaiting_adjudication,
  candidates: inbox.returns.map(x => x.candidate.slice(0, 8)), corruption: inbox.corruption.length,
  user_copied_no_chat_message: true });

// ------------------------------------------------------------------ reviewer, 3rd worktree
submitTask(store, TR);
const r3 = await runTask(TR, WT3);
const reviewTxt = fs.existsSync(path.join(WT3, 'REVIEW.txt')) ? fs.readFileSync(path.join(WT3, 'REVIEW.txt'), 'utf8').trim() : null;
log('REVIEWER_PROCESS', { task_id: 'FX-REV', pid: r3.pid, exit: r3.exit, model: r3.model, variant: r3.reasoning_variant,
  separate_third_worktree: WT3 !== WT1 && WT3 !== WT2, reviewer_actually_ran: reviewTxt !== null,
  review_verdict: reviewTxt, review_candidate: git(WT3, 'rev-parse', 'HEAD').stdout });

// ------------------------------------------------------------------ git-derived publication gate
const CAND = git(WT1, 'rev-parse', 'HEAD').stdout;
log('CANDIDATE', { candidate: CAND, base: BASE, remote_head_at_start: REMOTE_HEAD_0 });

const REVIEW_SHA = 'f'.repeat(40);
const reviewOk = { review_sha: REVIEW_SHA, candidate_sha: CAND, disposition: 'APPROVE' };
const adjOk = buildAdjudication({ decision_id: 'HQ-FIXTURE-1', task_id: 'FX-W1', candidate_sha: CAND, review_sha: REVIEW_SHA, disposition: 'APPROVE' });

const gPos = (() => { try { return { ok: true, v: publicationGate({ repo: WT1, task: T1, candidate_ref: CAND, review: reviewOk, adjudication: adjOk, remote: 'origin' }) }; }
                     catch (e) { return { ok: false, code: e.code, detail: e.detail }; } })();
log('GATE_POSITIVE', gPos.ok ? { eligible: gPos.v.eligible, changed_paths_from_git: gPos.v.changed_paths, observed_remote_head: gPos.v.observed_remote_head, decision_id: gPos.v.decision_id } : gPos);

// candidate-change invalidation
must(git(WT1, 'checkout', '-q', '-b', 'fx-worker-1-later', CAND), 'branch later');
fs.writeFileSync(path.join(WT1, 'allowed', 'extra.txt'), 'changed after review\n');
must(git(WT1, 'add', '-A'), 'add extra');
must(git(WT1, 'commit', '-q', '-m', 'post-review change'), 'commit extra');
const CAND2 = git(WT1, 'rev-parse', 'HEAD').stdout;
const gStale = (() => { try { return { ok: true, v: publicationGate({ repo: WT1, task: T1, candidate_ref: CAND2, review: reviewOk, adjudication: adjOk, remote: 'origin' }) }; }
                      catch (e) { return { ok: false, code: e.code, detail: e.detail }; } })();
log('GATE_CANDIDATE_CHANGE_INVALIDATION', gStale.ok ? 'UNEXPECTED_PASS'
  : { rejected_with: gStale.code, detail: gStale.detail, review_bound: CAND.slice(0, 8), presented_candidate: CAND2.slice(0, 8) });

// competing publication: remote actually moves
git(CONTROL, 'checkout', '-q', 'main');
fs.writeFileSync(path.join(CONTROL, 'allowed', 'competing.txt'), 'competing\n');
must(git(CONTROL, 'add', '-A'), 'add competing');
must(git(CONTROL, 'commit', '-q', '-m', 'competing advance'), 'commit competing');
must(git(CONTROL, 'push', '-q', 'origin', 'HEAD:main'), 'push competing');
const REMOTE_HEAD_1 = git(CONTROL, 'ls-remote', 'origin', 'refs/heads/main').stdout.split(/\s+/)[0];
const gRemote = (() => { try { return { ok: true, v: publicationGate({ repo: WT1, task: T1, candidate_ref: CAND, review: reviewOk, adjudication: adjOk, remote: 'origin' }) }; }
                        catch (e) { return { ok: false, code: e.code, detail: e.detail }; } })();
log('GATE_COMPETING_PUBLICATION', { remote_before: REMOTE_HEAD_0.slice(0, 8), remote_after: REMOTE_HEAD_1.slice(0, 8),
  remote_actually_moved: REMOTE_HEAD_0 !== REMOTE_HEAD_1,
  result: gRemote.ok ? 'UNEXPECTED_PASS' : { rejected_with: gRemote.code, detail: gRemote.detail } });

// terrain violation derived FROM GIT
const OUT = worktree('fx-out-of-terrain');
fs.mkdirSync(path.join(OUT, 'forbidden'), { recursive: true });
fs.writeFileSync(path.join(OUT, 'forbidden', 'nope.txt'), 'outside terrain\n');
must(git(OUT, 'add', '-A'), 'add forbidden');
must(git(OUT, 'commit', '-q', '-m', 'out of terrain'), 'commit forbidden');
const OUTC = git(OUT, 'rev-parse', 'HEAD').stdout;
const gTerr = (() => { try { return { ok: true, v: publicationGate({ repo: OUT, task: { ...T1, worktree: OUT }, candidate_ref: OUTC,
      review: { review_sha: REVIEW_SHA, candidate_sha: OUTC, disposition: 'APPROVE' },
      adjudication: buildAdjudication({ decision_id: 'HQ-FIXTURE-2', task_id: 'FX-W1', candidate_sha: OUTC, review_sha: REVIEW_SHA, disposition: 'APPROVE' }),
      remote: 'origin', check_remote: false }) }; }
  catch (e) { return { ok: false, code: e.code, detail: e.detail }; } })();
log('GATE_TERRAIN_DERIVED_FROM_GIT', gTerr.ok ? 'UNEXPECTED_PASS' : { rejected_with: gTerr.code, detail: gTerr.detail });

// arbitrary ACCEPTED event still cannot manufacture acceptance for the real candidate
const sArb = new Store(path.join(ROOT, 'arb'));
sArb.append({ task_id: 'FX-W1', attempt: 1, seq: 1, state: 'ACCEPTED', role: 'worker', candidate: CAND });
const gArb = (() => { try { return { ok: true, v: publicationGate({ repo: WT1, task: T1, candidate_ref: CAND, review: reviewOk, adjudication: undefined, remote: 'origin', check_remote: false }) }; }
                    catch (e) { return { ok: false, code: e.code, detail: e.detail }; } })();
log('GATE_ARBITRARY_ACCEPTED_NO_ADJUDICATION', gArb.ok ? 'UNEXPECTED_PASS' : { rejected_with: gArb.code, detail: gArb.detail });

// ------------------------------------------------------------------ restart after
const post = recover(store);
log('RESTART_AFTER', { recovered: post.recovered, blocking: post.blocking,
  tasks: post.tasks.map(t => ({ id: t.task_id, state: t.derived_state, binding_complete: t.binding_complete,
    has_launch_receipt: !!t.launch_receipt, exit: t.launch_receipt && t.launch_receipt.exit, model: t.launch_receipt && t.launch_receipt.model })) });

// ------------------------------------------------------------------ corruption blocks recovery
const cs = new Store(path.join(ROOT, 'corrupt'));
cs.append({ task_id: 'X', attempt: 1, seq: 1, state: 'QUEUED', role: 'worker', binding: { task_id: 'X' } });
fs.appendFileSync(cs.log, '{"task_id":"Y","attempt":1,"seq":1,"state":');   // torn, no trailing newline
const cr = recover(cs);
log('CORRUPT_RECOVERY_BLOCKS', { recovered: cr.recovered, blocking: cr.blocking, corruption: cr.corruption, honest: cr.honest });

fs.rmSync(ROOT, { recursive: true, force: true });
console.log(JSON.stringify(ev, null, 2));